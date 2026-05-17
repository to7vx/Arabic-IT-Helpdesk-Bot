"""Agent draft-reply generator. Retrieves KB, then synthesizes a grounded reply."""

from __future__ import annotations

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from helpdesk.db import models
from helpdesk.middleware.error_handler import NotFoundError
from helpdesk.nlp.generation.llm_client import generate
from helpdesk.nlp.generation.prompts import draft_system
from helpdesk.nlp.retrieval.kb_search import search


async def draft(
    session: AsyncSession, ticket_id: UUID, *, lang: str, tone: str  # noqa: ARG001
) -> dict[str, object]:
    ticket = await session.get(models.Ticket, ticket_id)
    if ticket is None:
        raise NotFoundError()

    kb_hits = await search(
        session=session,
        org_id=ticket.org_id,
        query=f"{ticket.title}\n{ticket.description}",
        top_k=3,
    )
    grounding = "\n\n".join(
        f"### KB: {hit['slug']}\n{hit['snippet']}" for hit in kb_hits
    )
    user = (
        f"# Ticket\n{ticket.title}\n{ticket.description}\n\n"
        f"# Knowledge base excerpts (cite by slug):\n{grounding or '(no matching KB articles)'}"
    )
    result = await generate(system=draft_system(lang), user=user, max_tokens=400)
    return {
        "draft": result.text,
        "lang": lang,
        "citations": [hit["slug"] for hit in kb_hits],
    }
