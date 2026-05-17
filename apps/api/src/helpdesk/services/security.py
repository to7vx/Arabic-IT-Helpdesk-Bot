"""Password hashing, TOTP, JWT issuance and verification.

We use Argon2id for password hashing (winner of PHC, OWASP-recommended)
with parameters tuned for ~50 ms on a 2 vCPU container. JWTs use RS256
with keys loaded from disk paths in :class:`Settings`. Tokens carry
the user id, org id, role, and a short JTI used for revocation lookups
in Redis.
"""

from __future__ import annotations

import secrets
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any

import pyotp
from jose import JWTError, jwt
from passlib.hash import argon2

from helpdesk.config import Settings, get_settings


def hash_password(password: str) -> str:
    return argon2.using(time_cost=3, memory_cost=64 * 1024, parallelism=2).hash(password)


def verify_password(password: str, hashed: str) -> bool:
    try:
        return argon2.verify(password, hashed)
    except (ValueError, TypeError):
        return False


def generate_totp_secret() -> str:
    return pyotp.random_base32()


def verify_totp(secret: str, code: str) -> bool:
    return pyotp.TOTP(secret).verify(code, valid_window=1)


def totp_provisioning_uri(secret: str, account: str, issuer: str = "Arabic Helpdesk") -> str:
    return pyotp.TOTP(secret).provisioning_uri(name=account, issuer_name=issuer)


# ---------------------------------------------------------------------------
# JWT
# ---------------------------------------------------------------------------

@dataclass(slots=True)
class TokenPair:
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int = 0


def _load_keys(settings: Settings) -> tuple[str, str]:
    if settings.jwt_algorithm == "HS256":
        secret = settings.secret_key.get_secret_value()
        return secret, secret
    priv = settings.jwt_private_key_path.read_text(encoding="utf-8")
    pub = settings.jwt_public_key_path.read_text(encoding="utf-8")
    return priv, pub


def issue_tokens(*, sub: str, org_id: str, role: str) -> TokenPair:
    settings = get_settings()
    private_key, _ = _load_keys(settings)
    now = datetime.now(timezone.utc)
    access_exp = now + timedelta(minutes=settings.jwt_access_ttl_min)
    refresh_exp = now + timedelta(days=settings.jwt_refresh_ttl_days)
    common: dict[str, Any] = {"sub": sub, "org_id": org_id, "role": role}
    access = jwt.encode(
        {**common, "type": "access", "iat": now, "exp": access_exp, "jti": secrets.token_urlsafe(16)},
        private_key,
        algorithm=settings.jwt_algorithm,
    )
    refresh = jwt.encode(
        {**common, "type": "refresh", "iat": now, "exp": refresh_exp, "jti": secrets.token_urlsafe(16)},
        private_key,
        algorithm=settings.jwt_algorithm,
    )
    return TokenPair(
        access_token=access,
        refresh_token=refresh,
        expires_in=int((access_exp - now).total_seconds()),
    )


def decode_token(token: str, *, expected_type: str = "access") -> dict[str, Any]:
    settings = get_settings()
    _, public_key = _load_keys(settings)
    try:
        payload = jwt.decode(token, public_key, algorithms=[settings.jwt_algorithm])
    except JWTError as exc:
        raise ValueError(f"invalid token: {exc}") from exc
    if payload.get("type") != expected_type:
        raise ValueError(f"expected {expected_type} token, got {payload.get('type')!r}")
    return payload  # type: ignore[no-any-return]
