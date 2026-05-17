"""User accounts, roles, and federated identities."""

from __future__ import annotations

from enum import StrEnum

from sqlalchemy import Boolean, DateTime, ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from helpdesk.db.base import Base, SoftDeleteMixin, TimestampMixin, UuidPK


class UserRole(StrEnum):
    end_user = "end_user"
    agent = "agent"
    manager = "manager"
    admin = "admin"


class User(Base, TimestampMixin, SoftDeleteMixin):
    """Local or federated user account."""

    __tablename__ = "users"
    __table_args__ = (
        UniqueConstraint("org_id", "email", name="uq_users_org_email"),
        Index("ix_users_email", "email"),
    )

    id: Mapped[UuidPK]
    org_id: Mapped[UuidPK] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False
    )

    email: Mapped[str] = mapped_column(String(320), nullable=False)
    name_en: Mapped[str | None] = mapped_column(String(255))
    name_ar: Mapped[str | None] = mapped_column(String(255))
    locale_pref: Mapped[str] = mapped_column(String(8), default="ar", nullable=False)

    role: Mapped[UserRole] = mapped_column(
        String(32), default=UserRole.end_user, nullable=False
    )

    # Local-auth fields. May be NULL if the account is federation-only.
    password_hash: Mapped[str | None] = mapped_column(String(255))
    mfa_secret: Mapped[str | None] = mapped_column(String(64))
    mfa_enabled: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Audit / lockout
    last_login_at: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True))
    failed_login_count: Mapped[int] = mapped_column(default=0, nullable=False)
    locked_until: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True))


class OAuthAccount(Base, TimestampMixin):
    """Federated identity from an OIDC / OAuth2 provider."""

    __tablename__ = "oauth_accounts"
    __table_args__ = (
        UniqueConstraint("provider", "subject", name="uq_oauth_provider_subject"),
    )

    id: Mapped[UuidPK]
    user_id: Mapped[UuidPK] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    provider: Mapped[str] = mapped_column(String(32), nullable=False)  # google | microsoft | saml | oidc
    subject: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str | None] = mapped_column(String(320))
