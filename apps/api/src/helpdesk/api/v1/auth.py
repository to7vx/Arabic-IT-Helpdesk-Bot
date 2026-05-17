"""Authentication routes — login, refresh, TOTP, OAuth start/callback."""

from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import select

from helpdesk.api.v1.deps_auth import CurrentUser, get_current_user
from helpdesk.db import models
from helpdesk.deps import SessionDep
from helpdesk.middleware.error_handler import ForbiddenError
from helpdesk.services.security import (
    TokenPair,
    decode_token,
    generate_totp_secret,
    hash_password,
    issue_tokens,
    totp_provisioning_uri,
    verify_password,
    verify_totp,
)

router = APIRouter()

MAX_FAILED_LOGINS = 5


class LoginIn(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    totp_code: str | None = Field(default=None, min_length=6, max_length=6)


class TokenOut(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class RefreshIn(BaseModel):
    refresh_token: str


class RegisterIn(BaseModel):
    email: EmailStr
    password: str = Field(min_length=12, max_length=128)
    name_en: str | None = None
    name_ar: str | None = None
    locale_pref: str = "ar"


class MfaEnrollOut(BaseModel):
    secret: str
    provisioning_uri: str


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=TokenOut)
async def register(payload: RegisterIn, session: SessionDep) -> TokenPair:
    existing = await session.scalar(select(models.User).where(models.User.email == payload.email))
    if existing is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="email already registered")
    org = await session.scalar(select(models.Organization).where(models.Organization.slug == "default"))
    if org is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="default org missing")
    user = models.User(
        org_id=org.id,
        email=payload.email,
        password_hash=hash_password(payload.password),
        name_en=payload.name_en,
        name_ar=payload.name_ar,
        locale_pref=payload.locale_pref,
        role="end_user",
    )
    session.add(user)
    await session.flush()
    return issue_tokens(sub=str(user.id), org_id=str(user.org_id), role=user.role)


@router.post("/login", response_model=TokenOut)
async def login(payload: LoginIn, session: SessionDep) -> TokenPair:
    user = await session.scalar(
        select(models.User).where(models.User.email == payload.email, models.User.deleted_at.is_(None))
    )
    if user is None or not user.password_hash:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid credentials")
    if user.locked_until and user.locked_until > datetime.now(timezone.utc):
        raise HTTPException(status_code=status.HTTP_423_LOCKED, detail="account locked, try later")
    if not verify_password(payload.password, user.password_hash):
        user.failed_login_count += 1
        if user.failed_login_count >= MAX_FAILED_LOGINS:
            from datetime import timedelta
            user.locked_until = datetime.now(timezone.utc) + timedelta(minutes=15)
        await session.flush()
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid credentials")
    if user.mfa_enabled:
        if not payload.totp_code or not user.mfa_secret or not verify_totp(user.mfa_secret, payload.totp_code):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="mfa code required or invalid")
    user.failed_login_count = 0
    user.locked_until = None
    user.last_login_at = datetime.now(timezone.utc)
    await session.flush()
    return issue_tokens(sub=str(user.id), org_id=str(user.org_id), role=user.role)


@router.post("/refresh", response_model=TokenOut)
async def refresh(payload: RefreshIn, session: SessionDep) -> TokenPair:
    try:
        claims = decode_token(payload.refresh_token, expected_type="refresh")
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from exc
    user = await session.scalar(
        select(models.User).where(models.User.id == claims["sub"], models.User.deleted_at.is_(None))
    )
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="user not found")
    return issue_tokens(sub=str(user.id), org_id=str(user.org_id), role=user.role)


@router.post("/mfa/enroll", response_model=MfaEnrollOut)
async def mfa_enroll(
    session: SessionDep, user: CurrentUser = Depends(get_current_user)
) -> MfaEnrollOut:
    if user.role == "end_user":
        raise ForbiddenError()
    db_user = await session.get(models.User, user.id)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    secret = generate_totp_secret()
    db_user.mfa_secret = secret
    db_user.mfa_enabled = False  # confirmed by /mfa/verify
    await session.flush()
    return MfaEnrollOut(
        secret=secret,
        provisioning_uri=totp_provisioning_uri(secret, account=db_user.email),
    )


class MfaVerifyIn(BaseModel):
    code: str = Field(min_length=6, max_length=6)


@router.post("/mfa/verify", status_code=status.HTTP_204_NO_CONTENT)
async def mfa_verify(
    payload: MfaVerifyIn,
    session: SessionDep,
    user: CurrentUser = Depends(get_current_user),
) -> None:
    db_user = await session.get(models.User, user.id)
    if db_user is None or not db_user.mfa_secret:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="enroll first")
    if not verify_totp(db_user.mfa_secret, payload.code):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid code")
    db_user.mfa_enabled = True
    await session.flush()


@router.get("/me")
async def me(user: CurrentUser = Depends(get_current_user)) -> dict[str, str]:
    return {"id": str(user.id), "org_id": str(user.org_id), "role": user.role, "email": user.email}


# OAuth/SAML/OIDC are stubbed at this layer; the actual provider dance is in
# helpdesk.integrations.oauth (Phase 6). These routes exist so the typed
# OpenAPI client can codegen the surface today.

@router.get("/oauth/{provider}/start", response_model=dict[str, str])
async def oauth_start(provider: str) -> dict[str, str]:
    if provider not in {"google", "microsoft"}:
        raise HTTPException(status_code=400, detail="unsupported provider")
    # Real implementation issues a state token and returns the IdP redirect URL.
    return {"redirect_url": f"https://example.invalid/oauth/{provider}/authorize?stub=1"}


@router.get("/oauth/{provider}/callback", response_model=TokenOut)
async def oauth_callback(provider: str, code: str) -> TokenPair:  # noqa: ARG001
    raise HTTPException(status_code=501, detail="OAuth callback wiring lands in Phase 6")
