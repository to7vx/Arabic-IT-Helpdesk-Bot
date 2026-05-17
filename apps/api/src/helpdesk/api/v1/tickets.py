"""Ticket REST routes."""

from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from pydantic import BaseModel, Field

from helpdesk.api.v1.deps_auth import CurrentUser, get_current_user
from helpdesk.deps import SessionDep
from helpdesk.middleware.error_handler import ForbiddenError, NotFoundError
from helpdesk.services import ticket_service
from helpdesk.services.rbac import require

router = APIRouter()


class TicketIn(BaseModel):
    title: str = Field(min_length=3, max_length=500)
    description: str = Field(min_length=1, max_length=20000)
    category_id: UUID | None = None
    team_id: UUID | None = None
    priority: str = Field(default="medium", pattern="^(low|medium|high|urgent)$")


class MessageIn(BaseModel):
    body: str = Field(min_length=1, max_length=20000)
    internal_note: bool = False


class AssignIn(BaseModel):
    assignee_id: UUID


class StatusIn(BaseModel):
    status: str = Field(pattern="^(new|open|pending|on_hold|resolved|closed)$")


@router.get("", summary="List tickets")
async def list_tickets(
    session: SessionDep,
    user: CurrentUser = Depends(require("ticket.read")),
    status_: str | None = Query(default=None, alias="status"),
    assignee_id: UUID | None = None,
    mine: bool = False,
    limit: int = Query(default=50, le=200),
    cursor: datetime | None = None,
) -> dict[str, Any]:
    tickets = await ticket_service.list_tickets(
        session,
        org_id=user.org_id,
        status=status_,
        assignee_id=assignee_id or (user.id if mine and user.role == "agent" else None),
        requester_id=user.id if user.role == "end_user" else None,
        limit=limit,
        cursor=cursor,
    )
    serialized = [await ticket_service.serialize(t) for t in tickets]
    next_cursor = tickets[-1].created_at.isoformat() if len(tickets) == limit else None
    return {"items": serialized, "next_cursor": next_cursor}


@router.post("", status_code=status.HTTP_201_CREATED, summary="Create a ticket")
async def create_ticket(
    payload: TicketIn,
    session: SessionDep,
    user: CurrentUser = Depends(get_current_user),
) -> dict[str, Any]:
    ticket = await ticket_service.create_ticket(
        session,
        org_id=user.org_id,
        requester_id=user.id,
        title=payload.title,
        description=payload.description,
        category_id=payload.category_id,
        team_id=payload.team_id,
        priority=payload.priority,
        source="web",
    )
    return await ticket_service.serialize(ticket)


async def _load_ticket_for_user(session, ticket_id: UUID, user: CurrentUser):  # type: ignore[no-untyped-def]
    from helpdesk.db import models

    ticket = await session.get(models.Ticket, ticket_id)
    if ticket is None or ticket.deleted_at is not None:
        raise NotFoundError()
    if ticket.org_id != user.org_id:
        raise ForbiddenError()
    if user.role == "end_user" and ticket.requester_id != user.id:
        raise ForbiddenError()
    return ticket


@router.get("/{ticket_id}")
async def get_ticket(
    ticket_id: UUID,
    session: SessionDep,
    user: CurrentUser = Depends(get_current_user),
) -> dict[str, Any]:
    ticket = await _load_ticket_for_user(session, ticket_id, user)
    return await ticket_service.serialize(ticket)


@router.post("/{ticket_id}/messages", status_code=status.HTTP_201_CREATED)
async def post_message(
    ticket_id: UUID,
    payload: MessageIn,
    session: SessionDep,
    user: CurrentUser = Depends(get_current_user),
) -> dict[str, str]:
    if payload.internal_note and user.role == "end_user":
        raise ForbiddenError()
    await _load_ticket_for_user(session, ticket_id, user)
    message = await ticket_service.add_message(
        session,
        ticket_id=ticket_id,
        author_id=user.id,
        body=payload.body,
        internal_note=payload.internal_note,
    )
    return {"id": str(message.id)}


@router.post("/{ticket_id}/assign")
async def assign(
    ticket_id: UUID,
    payload: AssignIn,
    session: SessionDep,
    user: CurrentUser = Depends(require("ticket.assign")),
) -> dict[str, Any]:
    ticket = await ticket_service.assign(
        session, ticket_id=ticket_id, assignee_id=payload.assignee_id, actor_id=user.id
    )
    return await ticket_service.serialize(ticket)


@router.post("/{ticket_id}/status")
async def change_status(
    ticket_id: UUID,
    payload: StatusIn,
    session: SessionDep,
    user: CurrentUser = Depends(require("ticket.write")),
) -> dict[str, Any]:
    ticket = await ticket_service.change_status(
        session, ticket_id=ticket_id, new_status=payload.status, actor_id=user.id
    )
    return await ticket_service.serialize(ticket)
