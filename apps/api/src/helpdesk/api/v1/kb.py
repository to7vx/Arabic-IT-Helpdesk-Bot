"""Knowledge-base routes."""

from __future__ import annotations

from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from pydantic import BaseModel, Field
from sqlalchemy import or_, select

from helpdesk.api.v1.deps_auth import CurrentUser, get_current_user
from helpdesk.db import models
from helpdesk.deps import SessionDep
from helpdesk.middleware.error_handler import NotFoundError
from helpdesk.services.rbac import require

router = APIRouter()


class ArticleIn(BaseModel):
    slug: str = Field(min_length=2, max_length=255, pattern=r"^[a-z0-9-]+$")
    title_en: str
    title_ar: str
    body_en: str
    body_ar: str
    category: str | None = None
    tags: list[str] | None = None
    is_public: bool = True


class ArticleOut(BaseModel):
    id: str
    slug: str
    title_en: str
    title_ar: str
    body_en: str
    body_ar: str
    category: str | None
    tags: list[str] | None
    is_public: bool
    view_count: int
    helpful_count: int
    not_helpful_count: int


def _serialize(article: models.KbArticle) -> ArticleOut:
    return ArticleOut(
        id=str(article.id),
        slug=article.slug,
        title_en=article.title_en,
        title_ar=article.title_ar,
        body_en=article.body_en,
        body_ar=article.body_ar,
        category=article.category,
        tags=article.tags,
        is_public=article.is_public,
        view_count=article.view_count,
        helpful_count=article.helpful_count,
        not_helpful_count=article.not_helpful_count,
    )


@router.get("")
async def list_articles(
    session: SessionDep,
    user: CurrentUser = Depends(get_current_user),
    q: str | None = None,
    category: str | None = None,
    limit: int = Query(default=50, le=200),
) -> list[ArticleOut]:
    stmt = select(models.KbArticle).where(
        models.KbArticle.org_id == user.org_id, models.KbArticle.deleted_at.is_(None)
    )
    if user.role == "end_user":
        stmt = stmt.where(models.KbArticle.is_public.is_(True))
    if category:
        stmt = stmt.where(models.KbArticle.category == category)
    if q:
        like = f"%{q}%"
        stmt = stmt.where(
            or_(
                models.KbArticle.title_en.ilike(like),
                models.KbArticle.title_ar.ilike(like),
                models.KbArticle.body_en.ilike(like),
                models.KbArticle.body_ar.ilike(like),
            )
        )
    stmt = stmt.limit(limit)
    rows = await session.scalars(stmt)
    return [_serialize(a) for a in rows]


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_article(
    payload: ArticleIn,
    session: SessionDep,
    user: CurrentUser = Depends(require("kb.write")),
) -> ArticleOut:
    article = models.KbArticle(
        org_id=user.org_id,
        slug=payload.slug,
        title_en=payload.title_en,
        title_ar=payload.title_ar,
        body_en=payload.body_en,
        body_ar=payload.body_ar,
        category=payload.category,
        tags=payload.tags,
        is_public=payload.is_public,
    )
    session.add(article)
    await session.flush()
    return _serialize(article)


@router.get("/{slug}")
async def get_article(
    slug: str,
    session: SessionDep,
    user: CurrentUser = Depends(get_current_user),
) -> ArticleOut:
    article = await session.scalar(
        select(models.KbArticle).where(
            models.KbArticle.org_id == user.org_id,
            models.KbArticle.slug == slug,
            models.KbArticle.deleted_at.is_(None),
        )
    )
    if article is None:
        raise NotFoundError()
    article.view_count += 1
    await session.flush()
    return _serialize(article)


class FeedbackIn(BaseModel):
    helpful: bool
    comment: str | None = None


@router.post("/{slug}/feedback", status_code=status.HTTP_204_NO_CONTENT)
async def submit_feedback(
    slug: str,
    payload: FeedbackIn,
    session: SessionDep,
    user: CurrentUser = Depends(get_current_user),
) -> None:
    article = await session.scalar(
        select(models.KbArticle).where(
            models.KbArticle.org_id == user.org_id,
            models.KbArticle.slug == slug,
            models.KbArticle.deleted_at.is_(None),
        )
    )
    if article is None:
        raise NotFoundError()
    session.add(
        models.KbFeedback(
            article_id=article.id, user_id=user.id, helpful=payload.helpful, comment=payload.comment
        )
    )
    if payload.helpful:
        article.helpful_count += 1
    else:
        article.not_helpful_count += 1
    await session.flush()


class KbSearchHit(BaseModel):
    slug: str
    title: str
    snippet: str
    score: float
    lang: str


@router.get("/search/hybrid", response_model=list[KbSearchHit])
async def hybrid_search(
    q: str,
    session: SessionDep,
    user: CurrentUser = Depends(get_current_user),
    top_k: int = Query(default=5, le=20),
) -> list[Any]:
    # The real implementation calls helpdesk.nlp.retrieval.kb_search
    # (Phase 4). Here we delegate to its facade which gracefully degrades
    # to ILIKE matching when the NLP optional deps are not installed.
    from helpdesk.nlp.retrieval.kb_search import search

    return await search(session=session, org_id=user.org_id, query=q, top_k=top_k)
