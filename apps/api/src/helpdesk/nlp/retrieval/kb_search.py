"""KB hybrid search facade.

Tries dense + sparse + RRF when the optional NLP deps and Qdrant are
available; falls back to a Postgres ILIKE query when they are not. The
calling router code does not need to know which path it got.
"""

from __future__ import annotations

from typing import Any
from uuid import UUID

import structlog
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from helpdesk.db import models
from helpdesk.nlp.preprocessing import normalize
from helpdesk.nlp.preprocessing.language_detect import detect

logger = structlog.get_logger(__name__)


async def search(
    *, session: AsyncSession, org_id: UUID, query: str, top_k: int = 5
) -> list[dict[str, Any]]:
    if not query.strip():
        return []
    try:
        from helpdesk.nlp.retrieval.hybrid import hybrid_search  # noqa: WPS433

        return await hybrid_search(session=session, org_id=org_id, query=query, top_k=top_k)
    except Exception as exc:  # noqa: BLE001
        logger.info("kb.search.fallback_to_ilike", error=str(exc))
        return await _ilike_fallback(session, org_id, query, top_k)


async def _ilike_fallback(
    session: AsyncSession, org_id: UUID, query: str, top_k: int
) -> list[dict[str, Any]]:
    lang = detect(query).primary
    norm = normalize(query)
    like = f"%{norm}%"
    stmt = (
        select(models.KbArticle)
        .where(
            models.KbArticle.org_id == org_id,
            models.KbArticle.deleted_at.is_(None),
            or_(
                models.KbArticle.title_ar.ilike(like),
                models.KbArticle.title_en.ilike(like),
                models.KbArticle.body_ar.ilike(like),
                models.KbArticle.body_en.ilike(like),
            ),
        )
        .limit(top_k)
    )
    rows = list(await session.scalars(stmt))
    return [
        {
            "slug": a.slug,
            "title": a.title_ar if lang == "ar" else a.title_en,
            "snippet": (a.body_ar if lang == "ar" else a.body_en)[:240],
            "score": 0.5,
            "lang": lang,
        }
        for a in rows
    ]
