"""PDPL Data Subject Rights endpoints.

Every data subject can:

* request a copy of their personal data (``/export``)
* request rectification of inaccurate data (``/rectify``)
* request deletion when there is no remaining lawful basis (``/delete``)

These endpoints capture the request; operators wire human review via
the ``dsr.requested`` outbound webhook.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel

from helpdesk.api.v1.deps_auth import CurrentUser, get_current_user
from helpdesk.db import models
from helpdesk.deps import SessionDep

router = APIRouter()


class ExportOut(BaseModel):
    user: dict[str, Any]
    tickets: list[dict[str, Any]]
    messages: list[dict[str, Any]]
    requested_at: str


@router.post("/export", response_model=ExportOut)
async def export_my_data(
    session: SessionDep, user: CurrentUser = Depends(get_current_user)
) -> ExportOut:
    db_user = await session.get(models.User, user.id)
    assert db_user is not None
    from sqlalchemy import select

    tickets = await session.scalars(
        select(models.Ticket).where(models.Ticket.requester_id == user.id)
    )
    tickets_list = list(tickets)
    msg_ids = [t.id for t in tickets_list]
    messages: list[models.TicketMessage] = []
    if msg_ids:
        messages = list(
            await session.scalars(
                select(models.TicketMessage).where(models.TicketMessage.ticket_id.in_(msg_ids))
            )
        )

    return ExportOut(
        user={
            "id": str(db_user.id),
            "email": db_user.email,
            "name_en": db_user.name_en,
            "name_ar": db_user.name_ar,
            "locale_pref": db_user.locale_pref,
            "created_at": db_user.created_at.isoformat(),
        },
        tickets=[
            {
                "id": str(t.id),
                "public_id": t.public_id,
                "title": t.title,
                "description": t.description,
                "status": t.status,
                "created_at": t.created_at.isoformat(),
            }
            for t in tickets_list
        ],
        messages=[
            {
                "id": str(m.id),
                "ticket_id": str(m.ticket_id),
                "body": m.body,
                "created_at": m.created_at.isoformat(),
            }
            for m in messages
        ],
        requested_at=datetime.now(timezone.utc).isoformat(),
    )


class RectifyIn(BaseModel):
    field: str
    new_value: str
    reason: str


@router.post("/rectify", status_code=status.HTTP_202_ACCEPTED)
async def request_rectification(
    payload: RectifyIn,
    session: SessionDep,
    user: CurrentUser = Depends(get_current_user),
) -> dict[str, str]:
    session.add(
        models.AuditLog(
            org_id=user.org_id,
            actor_id=user.id,
            action="dsr.rectify_requested",
            entity_type="user",
            entity_id=str(user.id),
            after={"field": payload.field, "reason": payload.reason},
        )
    )
    await session.flush()
    return {"status": "queued"}


class DeleteIn(BaseModel):
    reason: str


@router.post("/delete", status_code=status.HTTP_202_ACCEPTED)
async def request_deletion(
    payload: DeleteIn,
    session: SessionDep,
    user: CurrentUser = Depends(get_current_user),
) -> dict[str, str]:
    session.add(
        models.AuditLog(
            org_id=user.org_id,
            actor_id=user.id,
            action="dsr.deletion_requested",
            entity_type="user",
            entity_id=str(user.id),
            after={"reason": payload.reason},
        )
    )
    await session.flush()
    return {"status": "queued"}
