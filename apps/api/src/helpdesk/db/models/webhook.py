"""Outbound webhooks. HMAC signature scheme documented in the API guide."""

from __future__ import annotations

from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.dialects.postgresql import ARRAY, JSONB
from sqlalchemy.orm import Mapped, mapped_column

from helpdesk.db.base import Base, SoftDeleteMixin, TimestampMixin, UuidPK


class Webhook(Base, TimestampMixin, SoftDeleteMixin):
    """An operator-registered outbound webhook."""

    __tablename__ = "webhooks"

    id: Mapped[UuidPK]
    org_id: Mapped[UuidPK] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    url: Mapped[str] = mapped_column(String(2048), nullable=False)
    secret: Mapped[str] = mapped_column(String(255), nullable=False)
    """Used as the HMAC-SHA256 key over the JSON body."""
    events: Mapped[list[str]] = mapped_column(ARRAY(String(64)), nullable=False)
    headers: Mapped[dict[str, str] | None] = mapped_column(JSONB)
    active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
