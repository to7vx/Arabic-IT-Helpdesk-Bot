"""Ticket domain service.

Routers call into this; the service is also reused by integrations (email
ingest, Slack, etc.) so the same business rules — public_id minting, event
logging, NLP enqueue — apply regardless of entry point.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from helpdesk.db import models
from helpdesk.middleware.error_handler import ConflictError, NotFoundError


async def mint_public_id(session: AsyncSession) -> str:
    year = datetime.now(timezone.utc).year
    prefix = f"TKT-{year}-"
    count = await session.scalar(
        select(func.count())
        .select_from(models.Ticket)
        .where(models.Ticket.public_id.like(f"{prefix}%"))
    )
    return f"{prefix}{(count or 0) + 1:05d}"


async def create_ticket(
    session: AsyncSession,
    *,
    org_id: UUID,
    requester_id: UUID,
    title: str,
    description: str,
    source: str = "web",
    category_id: UUID | None = None,
    team_id: UUID | None = None,
    priority: str = "medium",
    language_detected: str | None = None,
    dialect_detected: str | None = None,
) -> models.Ticket:
    public_id = await mint_public_id(session)
    ticket = models.Ticket(
        public_id=public_id,
        org_id=org_id,
        requester_id=requester_id,
        title=title.strip(),
        description=description.strip(),
        category_id=category_id,
        team_id=team_id,
        priority=priority,
        source=source,
        language_detected=language_detected,
        dialect_detected=dialect_detected,
    )
    session.add(ticket)
    await session.flush()
    session.add(
        models.TicketEvent(
            ticket_id=ticket.id,
            actor_id=requester_id,
            event_type="created",
            payload={"source": source},
        )
    )
    await session.flush()
    return ticket


async def assign(
    session: AsyncSession, *, ticket_id: UUID, assignee_id: UUID, actor_id: UUID
) -> models.Ticket:
    ticket = await session.get(models.Ticket, ticket_id)
    if ticket is None:
        raise NotFoundError()
    previous = ticket.assignee_id
    ticket.assignee_id = assignee_id
    session.add(
        models.TicketEvent(
            ticket_id=ticket.id,
            actor_id=actor_id,
            event_type="assigned",
            payload={"from": str(previous) if previous else None, "to": str(assignee_id)},
        )
    )
    await session.flush()
    return ticket


async def change_status(
    session: AsyncSession, *, ticket_id: UUID, new_status: str, actor_id: UUID
) -> models.Ticket:
    ticket = await session.get(models.Ticket, ticket_id)
    if ticket is None:
        raise NotFoundError()
    if ticket.status == new_status:
        raise ConflictError(details={"current_status": ticket.status})
    old_status = ticket.status
    ticket.status = new_status
    if new_status == "resolved" and ticket.resolved_at is None:
        ticket.resolved_at = datetime.now(timezone.utc)
    session.add(
        models.TicketEvent(
            ticket_id=ticket.id,
            actor_id=actor_id,
            event_type="status_changed",
            payload={"from": old_status, "to": new_status},
        )
    )
    await session.flush()
    return ticket


async def add_message(
    session: AsyncSession,
    *,
    ticket_id: UUID,
    author_id: UUID,
    body: str,
    internal_note: bool = False,
) -> models.TicketMessage:
    ticket = await session.get(models.Ticket, ticket_id)
    if ticket is None:
        raise NotFoundError()
    message = models.TicketMessage(
        ticket_id=ticket.id,
        author_id=author_id,
        body=body,
        internal_note=internal_note,
    )
    session.add(message)
    if ticket.first_response_at is None and not internal_note and author_id != ticket.requester_id:
        ticket.first_response_at = datetime.now(timezone.utc)
    await session.flush()
    return message


async def list_tickets(
    session: AsyncSession,
    *,
    org_id: UUID,
    status: str | None = None,
    assignee_id: UUID | None = None,
    requester_id: UUID | None = None,
    limit: int = 50,
    cursor: datetime | None = None,
) -> list[models.Ticket]:
    stmt = select(models.Ticket).where(
        models.Ticket.org_id == org_id, models.Ticket.deleted_at.is_(None)
    )
    if status:
        stmt = stmt.where(models.Ticket.status == status)
    if assignee_id is not None:
        stmt = stmt.where(models.Ticket.assignee_id == assignee_id)
    if requester_id is not None:
        stmt = stmt.where(models.Ticket.requester_id == requester_id)
    if cursor is not None:
        stmt = stmt.where(models.Ticket.created_at < cursor)
    stmt = stmt.order_by(models.Ticket.created_at.desc()).limit(min(limit, 200))
    rows: list[models.Ticket] = list(await session.scalars(stmt))
    return rows


async def serialize(ticket: models.Ticket) -> dict[str, Any]:
    return {
        "id": str(ticket.id),
        "public_id": ticket.public_id,
        "title": ticket.title,
        "description": ticket.description,
        "status": ticket.status,
        "priority": ticket.priority,
        "source": ticket.source,
        "language_detected": ticket.language_detected,
        "dialect_detected": ticket.dialect_detected,
        "requester_id": str(ticket.requester_id),
        "assignee_id": str(ticket.assignee_id) if ticket.assignee_id else None,
        "team_id": str(ticket.team_id) if ticket.team_id else None,
        "category_id": str(ticket.category_id) if ticket.category_id else None,
        "tags": ticket.tags or [],
        "created_at": ticket.created_at.isoformat(),
        "updated_at": ticket.updated_at.isoformat(),
        "first_response_at": ticket.first_response_at.isoformat() if ticket.first_response_at else None,
        "resolved_at": ticket.resolved_at.isoformat() if ticket.resolved_at else None,
        "sla_due_at": ticket.sla_due_at.isoformat() if ticket.sla_due_at else None,
        "sentiment_score": ticket.sentiment_score,
        "urgency_score": ticket.urgency_score,
    }
