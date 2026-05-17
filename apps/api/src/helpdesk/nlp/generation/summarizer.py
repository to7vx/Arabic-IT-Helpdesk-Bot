"""Ticket summarization."""

from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from helpdesk.db import models
from helpdesk.middleware.error_handler import NotFoundError
from helpdesk.nlp.generation.llm_client import generate
from helpdesk.nlp.generation.prompts import summary_system


async def summarize_ticket(session: AsyncSession, ticket_id: UUID, lang: str) -> dict[str, object]:
    ticket = await session.get(models.Ticket, ticket_id)
    if ticket is None:
        raise NotFoundError()
    messages = list(
        await session.scalars(
            select(models.TicketMessage)
            .where(models.TicketMessage.ticket_id == ticket_id)
            .order_by(models.TicketMessage.created_at.asc())
        )
    )
    transcript = "\n\n".join(
        [f"### {ticket.title}\n{ticket.description}"]
        + [f"- {m.body}" for m in messages]
    )
    result = await generate(system=summary_system(lang), user=transcript, max_tokens=200)
    return {
        "summary": result.text,
        "lang": lang,
        "grounded_in": [ticket.public_id] + [str(m.id) for m in messages],
    }
