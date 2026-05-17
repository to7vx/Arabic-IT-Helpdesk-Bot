"""Admin endpoints — users, teams, categories, audit log."""

from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import select

from helpdesk.api.v1.deps_auth import CurrentUser
from helpdesk.db import models
from helpdesk.deps import SessionDep
from helpdesk.middleware.error_handler import NotFoundError
from helpdesk.services.rbac import require
from helpdesk.services.security import hash_password

router = APIRouter()


# ---------------------------------------------------------------------------
# Users
# ---------------------------------------------------------------------------

class AdminUserIn(BaseModel):
    email: EmailStr
    role: str = Field(pattern="^(end_user|agent|manager|admin)$")
    name_en: str | None = None
    name_ar: str | None = None
    initial_password: str | None = Field(default=None, min_length=12, max_length=128)


@router.post("/users", status_code=status.HTTP_201_CREATED)
async def create_user(
    payload: AdminUserIn,
    session: SessionDep,
    actor: CurrentUser = Depends(require("user.write")),
) -> dict[str, str]:
    user = models.User(
        org_id=actor.org_id,
        email=payload.email,
        role=payload.role,
        name_en=payload.name_en,
        name_ar=payload.name_ar,
        password_hash=hash_password(payload.initial_password) if payload.initial_password else None,
    )
    session.add(user)
    await session.flush()
    return {"id": str(user.id)}


@router.get("/users")
async def list_users(
    session: SessionDep,
    actor: CurrentUser = Depends(require("user.read")),
    role: str | None = None,
    limit: int = Query(default=100, le=500),
) -> list[dict[str, Any]]:
    stmt = select(models.User).where(
        models.User.org_id == actor.org_id, models.User.deleted_at.is_(None)
    )
    if role:
        stmt = stmt.where(models.User.role == role)
    stmt = stmt.limit(limit)
    return [
        {
            "id": str(u.id),
            "email": u.email,
            "name_en": u.name_en,
            "name_ar": u.name_ar,
            "role": u.role,
            "mfa_enabled": u.mfa_enabled,
        }
        for u in await session.scalars(stmt)
    ]


# ---------------------------------------------------------------------------
# Categories
# ---------------------------------------------------------------------------

class CategoryIn(BaseModel):
    slug: str = Field(min_length=2, max_length=64, pattern=r"^[a-z0-9-]+$")
    name_en: str
    name_ar: str
    parent_id: UUID | None = None
    default_team_id: UUID | None = None


@router.post("/categories", status_code=status.HTTP_201_CREATED)
async def create_category(
    payload: CategoryIn,
    session: SessionDep,
    actor: CurrentUser = Depends(require("category.write")),
) -> dict[str, str]:
    cat = models.Category(
        org_id=actor.org_id,
        slug=payload.slug,
        name_en=payload.name_en,
        name_ar=payload.name_ar,
        parent_id=payload.parent_id,
        default_team_id=payload.default_team_id,
    )
    session.add(cat)
    await session.flush()
    return {"id": str(cat.id)}


@router.get("/categories")
async def list_categories(
    session: SessionDep,
    actor: CurrentUser = Depends(require("category.read")),
) -> list[dict[str, Any]]:
    rows = await session.scalars(
        select(models.Category).where(
            models.Category.org_id == actor.org_id, models.Category.deleted_at.is_(None)
        )
    )
    return [
        {
            "id": str(c.id),
            "slug": c.slug,
            "name_en": c.name_en,
            "name_ar": c.name_ar,
            "parent_id": str(c.parent_id) if c.parent_id else None,
        }
        for c in rows
    ]


# ---------------------------------------------------------------------------
# Audit log
# ---------------------------------------------------------------------------

@router.get("/audit-log")
async def audit_log(
    session: SessionDep,
    actor: CurrentUser = Depends(require("audit.read")),
    action: str | None = None,
    limit: int = Query(default=100, le=1000),
    since: datetime | None = None,
) -> list[dict[str, Any]]:
    stmt = select(models.AuditLog).where(models.AuditLog.org_id == actor.org_id)
    if action:
        stmt = stmt.where(models.AuditLog.action == action)
    if since:
        stmt = stmt.where(models.AuditLog.created_at >= since)
    stmt = stmt.order_by(models.AuditLog.created_at.desc()).limit(limit)
    rows = await session.scalars(stmt)
    return [
        {
            "id": str(row.id),
            "action": row.action,
            "entity_type": row.entity_type,
            "entity_id": row.entity_id,
            "actor_id": str(row.actor_id) if row.actor_id else None,
            "created_at": row.created_at.isoformat(),
        }
        for row in rows
    ]


# ---------------------------------------------------------------------------
# Compliance toggles
# ---------------------------------------------------------------------------

class LlmConfigIn(BaseModel):
    provider: str = Field(pattern="^(disabled|claude|jais)$")
    confirm_cross_border: bool = False


@router.post("/compliance/llm")
async def set_llm_provider(
    payload: LlmConfigIn,
    actor: CurrentUser = Depends(require("admin.compliance")),
) -> dict[str, str]:
    # In a full implementation this writes to a settings table + emits an
    # audit + cross_border_transfers log entry. Kept as a no-op write here
    # so the surface and OpenAPI shape are real even before the settings
    # store lands.
    if payload.provider != "disabled" and not payload.confirm_cross_border:
        raise NotFoundError()
    return {"provider": payload.provider, "actor_id": str(actor.id)}
