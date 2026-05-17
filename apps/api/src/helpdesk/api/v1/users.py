"""User-facing user-management routes (the admin-only surface lives in admin.py)."""

from __future__ import annotations

from fastapi import APIRouter, Depends
from pydantic import BaseModel, EmailStr
from sqlalchemy import select

from helpdesk.api.v1.deps_auth import CurrentUser, get_current_user
from helpdesk.db import models
from helpdesk.deps import SessionDep

router = APIRouter()


class UserOut(BaseModel):
    id: str
    email: EmailStr
    name_en: str | None
    name_ar: str | None
    role: str
    locale_pref: str
    mfa_enabled: bool


@router.get("/me", response_model=UserOut)
async def get_me(session: SessionDep, user: CurrentUser = Depends(get_current_user)) -> UserOut:
    db_user = await session.get(models.User, user.id)
    assert db_user is not None
    return UserOut(
        id=str(db_user.id),
        email=db_user.email,
        name_en=db_user.name_en,
        name_ar=db_user.name_ar,
        role=db_user.role,
        locale_pref=db_user.locale_pref,
        mfa_enabled=db_user.mfa_enabled,
    )


class UpdateProfileIn(BaseModel):
    name_en: str | None = None
    name_ar: str | None = None
    locale_pref: str | None = None


@router.patch("/me", response_model=UserOut)
async def update_me(
    payload: UpdateProfileIn,
    session: SessionDep,
    user: CurrentUser = Depends(get_current_user),
) -> UserOut:
    db_user = await session.get(models.User, user.id)
    assert db_user is not None
    if payload.name_en is not None:
        db_user.name_en = payload.name_en
    if payload.name_ar is not None:
        db_user.name_ar = payload.name_ar
    if payload.locale_pref is not None:
        db_user.locale_pref = payload.locale_pref
    await session.flush()
    return UserOut(
        id=str(db_user.id),
        email=db_user.email,
        name_en=db_user.name_en,
        name_ar=db_user.name_ar,
        role=db_user.role,
        locale_pref=db_user.locale_pref,
        mfa_enabled=db_user.mfa_enabled,
    )


class TeamMemberOut(BaseModel):
    id: str
    email: EmailStr
    name_en: str | None
    name_ar: str | None
    role: str


@router.get("/agents", response_model=list[TeamMemberOut])
async def list_agents(
    session: SessionDep,
    user: CurrentUser = Depends(get_current_user),
) -> list[TeamMemberOut]:
    rows = await session.scalars(
        select(models.User).where(
            models.User.org_id == user.org_id,
            models.User.role.in_(("agent", "manager", "admin")),
            models.User.deleted_at.is_(None),
        )
    )
    return [
        TeamMemberOut(
            id=str(u.id), email=u.email, name_en=u.name_en, name_ar=u.name_ar, role=u.role
        )
        for u in rows
    ]
