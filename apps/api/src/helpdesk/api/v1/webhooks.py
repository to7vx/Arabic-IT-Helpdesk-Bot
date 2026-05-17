"""Outbound webhook management."""

from __future__ import annotations

import secrets
from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, Field, HttpUrl
from sqlalchemy import select

from helpdesk.api.v1.deps_auth import CurrentUser
from helpdesk.db import models
from helpdesk.deps import SessionDep
from helpdesk.middleware.error_handler import NotFoundError
from helpdesk.services.rbac import require

router = APIRouter()


class WebhookIn(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    url: HttpUrl
    events: list[str] = Field(min_length=1)
    headers: dict[str, str] | None = None


class WebhookOut(BaseModel):
    id: str
    name: str
    url: str
    events: list[str]
    active: bool
    secret_preview: str
    """First and last 4 characters of the HMAC secret. The full secret is
    only returned at creation time."""


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_webhook(
    payload: WebhookIn,
    session: SessionDep,
    actor: CurrentUser = Depends(require("webhook.write")),
) -> dict[str, str]:
    secret = secrets.token_urlsafe(32)
    wh = models.Webhook(
        org_id=actor.org_id,
        name=payload.name,
        url=str(payload.url),
        secret=secret,
        events=payload.events,
        headers=payload.headers,
    )
    session.add(wh)
    await session.flush()
    return {"id": str(wh.id), "secret": secret}


@router.get("")
async def list_webhooks(
    session: SessionDep, actor: CurrentUser = Depends(require("webhook.read"))
) -> list[WebhookOut]:
    rows = await session.scalars(
        select(models.Webhook).where(
            models.Webhook.org_id == actor.org_id, models.Webhook.deleted_at.is_(None)
        )
    )
    return [
        WebhookOut(
            id=str(w.id),
            name=w.name,
            url=w.url,
            events=w.events,
            active=w.active,
            secret_preview=f"{w.secret[:4]}…{w.secret[-4:]}",
        )
        for w in rows
    ]


@router.delete("/{webhook_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_webhook(
    webhook_id: UUID,
    session: SessionDep,
    actor: CurrentUser = Depends(require("webhook.write")),
) -> None:
    wh = await session.get(models.Webhook, webhook_id)
    if wh is None or wh.org_id != actor.org_id:
        raise NotFoundError()
    from datetime import datetime, timezone

    wh.deleted_at = datetime.now(timezone.utc)
    await session.flush()
