"""PDPL primitives: consent ledger and cross-border transfer log."""

from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, Index, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from helpdesk.db.base import Base, TimestampMixin, UuidPK


class Consent(Base, TimestampMixin):
    """Recorded consent or its withdrawal."""

    __tablename__ = "consents"
    __table_args__ = (
        Index("ix_consents_data_subject_id", "data_subject_id"),
        Index("ix_consents_purpose", "purpose"),
    )

    id: Mapped[UuidPK]
    org_id: Mapped[UuidPK] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False
    )
    data_subject_id: Mapped[UuidPK] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    purpose: Mapped[str] = mapped_column(String(128), nullable=False)
    lawful_basis: Mapped[str] = mapped_column(String(64), nullable=False)
    granted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    withdrawn_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    proof: Mapped[str | None] = mapped_column(Text)


class CrossBorderTransfer(Base, TimestampMixin):
    """Log every outbound transfer of personal data outside KSA."""

    __tablename__ = "cross_border_transfers"
    __table_args__ = (Index("ix_cbt_destination", "destination"),)

    id: Mapped[UuidPK]
    org_id: Mapped[UuidPK] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False
    )
    data_subject_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL")
    )
    destination: Mapped[str] = mapped_column(String(255), nullable=False)
    """Service name, e.g. ``anthropic.com``."""
    fields: Mapped[list[str]] = mapped_column(JSONB, nullable=False)
    lawful_basis: Mapped[str] = mapped_column(String(64), nullable=False)
    retention_days: Mapped[int | None] = mapped_column()
    payload_summary: Mapped[dict[str, Any] | None] = mapped_column(JSONB)
