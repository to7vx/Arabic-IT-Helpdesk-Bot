"""AI / NLP endpoints.

The actual model wiring lives under helpdesk.nlp. These endpoints are thin
adapters that translate request payloads, call the pipeline, and record an
``ai_suggestions`` row for every prediction (so we can learn from accepts /
edits later).
"""

from __future__ import annotations

from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from helpdesk.api.v1.deps_auth import CurrentUser, get_current_user
from helpdesk.db import models
from helpdesk.deps import SessionDep
from helpdesk.middleware.error_handler import NotFoundError
from helpdesk.services.rbac import require

router = APIRouter()


class ClassifyIn(BaseModel):
    text: str = Field(min_length=1, max_length=20000)
    top_k: int = Field(default=3, ge=1, le=10)


class ClassifyHit(BaseModel):
    category_slug: str
    confidence: float


@router.post("/classify", response_model=list[ClassifyHit])
async def classify(
    payload: ClassifyIn,
    _: CurrentUser = Depends(require("ai.read")),
) -> list[ClassifyHit]:
    from helpdesk.nlp.classification.category import classify_text

    return [ClassifyHit(**hit) for hit in await classify_text(payload.text, top_k=payload.top_k)]


class SuggestIn(BaseModel):
    ticket_id: UUID | None = None
    text: str | None = None
    top_k: int = Field(default=5, ge=1, le=20)


class SuggestKbOut(BaseModel):
    slug: str
    title: str
    snippet: str
    score: float
    lang: str


@router.post("/suggest-kb", response_model=list[SuggestKbOut])
async def suggest_kb(
    payload: SuggestIn,
    session: SessionDep,
    user: CurrentUser = Depends(require("ai.read")),
) -> list[Any]:
    text = payload.text
    if payload.ticket_id and not text:
        ticket = await session.get(models.Ticket, payload.ticket_id)
        if ticket is None:
            raise NotFoundError()
        text = f"{ticket.title}\n{ticket.description}"
    if not text:
        return []
    from helpdesk.nlp.retrieval.kb_search import search

    return await search(session=session, org_id=user.org_id, query=text, top_k=payload.top_k)


class UrgencyOut(BaseModel):
    urgency_score: float
    sentiment_score: float
    requires_escalation: bool


@router.post("/detect-urgency", response_model=UrgencyOut)
async def detect_urgency(
    payload: ClassifyIn,
    _: CurrentUser = Depends(require("ai.read")),
) -> UrgencyOut:
    from helpdesk.nlp.classification.urgency import score_urgency

    result = await score_urgency(payload.text)
    return UrgencyOut(**result)


class SummarizeIn(BaseModel):
    ticket_id: UUID
    target_lang: str = Field(default="ar", pattern="^(ar|en)$")


class SummaryOut(BaseModel):
    summary: str
    lang: str
    grounded_in: list[str]


@router.post("/summarize", response_model=SummaryOut)
async def summarize(
    payload: SummarizeIn,
    session: SessionDep,
    _: CurrentUser = Depends(require("ai.read")),
) -> SummaryOut:
    from helpdesk.nlp.generation.summarizer import summarize_ticket

    return SummaryOut(**await summarize_ticket(session, payload.ticket_id, payload.target_lang))


class DraftIn(BaseModel):
    ticket_id: UUID
    target_lang: str = Field(default="ar", pattern="^(ar|en)$")
    tone: str = Field(default="friendly", pattern="^(friendly|formal|brief)$")


class DraftOut(BaseModel):
    draft: str
    lang: str
    citations: list[str]


@router.post("/draft-reply", response_model=DraftOut)
async def draft_reply(
    payload: DraftIn,
    session: SessionDep,
    _: CurrentUser = Depends(require("ai.read")),
) -> DraftOut:
    from helpdesk.nlp.generation.draft_reply import draft

    return DraftOut(
        **await draft(session, payload.ticket_id, lang=payload.target_lang, tone=payload.tone)
    )


class TranslateIn(BaseModel):
    text: str
    target_lang: str = Field(pattern="^(ar|en)$")


class TranslateOut(BaseModel):
    text: str
    source_lang: str
    target_lang: str


@router.post("/translate", response_model=TranslateOut)
async def translate(
    payload: TranslateIn,
    _: CurrentUser = Depends(require("ai.read")),
) -> TranslateOut:
    from helpdesk.nlp.generation.translator import translate as _t

    return TranslateOut(**await _t(payload.text, payload.target_lang))
