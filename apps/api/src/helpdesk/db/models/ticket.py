"""Ticket, message, attachment, category models."""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import (
    Boolean,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship

from helpdesk.db.base import Base, SoftDeleteMixin, TimestampMixin, UuidPK

if TYPE_CHECKING:
    from helpdesk.db.models.user import User


class TicketStatus(StrEnum):
    new = "new"
    open = "open"
    pending = "pending"
    on_hold = "on_hold"
    resolved = "resolved"
    closed = "closed"
    merged = "merged"


class TicketPriority(StrEnum):
    low = "low"
    medium = "medium"
    high = "high"
    urgent = "urgent"


class TicketSource(StrEnum):
    web = "web"
    email = "email"
    slack = "slack"
    teams = "teams"
    whatsapp = "whatsapp"
    api = "api"


class Category(Base, TimestampMixin, SoftDeleteMixin):
    """Hierarchical ticket category. ``parent_id`` is NULL for root nodes."""

    __tablename__ = "categories"
    __table_args__ = (
        UniqueConstraint("org_id", "slug", name="uq_categories_org_slug"),
        Index("ix_categories_parent_id", "parent_id"),
    )

    id: Mapped[UuidPK]
    org_id: Mapped[UuidPK] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False
    )
    parent_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("categories.id", ondelete="SET NULL")
    )
    slug: Mapped[str] = mapped_column(String(64), nullable=False)
    name_en: Mapped[str] = mapped_column(String(255), nullable=False)
    name_ar: Mapped[str] = mapped_column(String(255), nullable=False)
    icon: Mapped[str | None] = mapped_column(String(64))
    default_team_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("teams.id", ondelete="SET NULL")
    )


class Ticket(Base, TimestampMixin, SoftDeleteMixin):
    """A support ticket."""

    __tablename__ = "tickets"
    __table_args__ = (
        Index("ix_tickets_org_status", "org_id", "status"),
        Index("ix_tickets_assignee_id", "assignee_id"),
        Index("ix_tickets_requester_id", "requester_id"),
        Index("ix_tickets_created_at", "created_at"),
        Index("ix_tickets_sla_due_at", "sla_due_at"),
        UniqueConstraint("public_id", name="uq_tickets_public_id"),
    )

    id: Mapped[UuidPK]
    public_id: Mapped[str] = mapped_column(String(32), nullable=False)
    """Human-readable ticket number, e.g. ``TKT-2026-00042``."""

    org_id: Mapped[UuidPK] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False
    )
    requester_id: Mapped[UuidPK] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"), nullable=False
    )
    assignee_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL")
    )
    team_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("teams.id", ondelete="SET NULL")
    )
    category_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("categories.id", ondelete="SET NULL")
    )

    # Content. Raw + normalized so we never lose original Arabic forms.
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    normalized_text: Mapped[str | None] = mapped_column(Text)
    language_detected: Mapped[str | None] = mapped_column(String(8))
    dialect_detected: Mapped[str | None] = mapped_column(String(16))

    status: Mapped[TicketStatus] = mapped_column(
        String(16), default=TicketStatus.new, nullable=False
    )
    priority: Mapped[TicketPriority] = mapped_column(
        String(16), default=TicketPriority.medium, nullable=False
    )
    source: Mapped[TicketSource] = mapped_column(
        String(16), default=TicketSource.web, nullable=False
    )

    sentiment_score: Mapped[float | None] = mapped_column(Float)
    urgency_score: Mapped[float | None] = mapped_column(Float)

    sla_due_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    first_response_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    tags: Mapped[list[str] | None] = mapped_column(ARRAY(String(64)))

    merged_into_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("tickets.id", ondelete="SET NULL")
    )

    messages: Mapped[list[TicketMessage]] = relationship(
        back_populates="ticket", cascade="all, delete-orphan"
    )
    attachments: Mapped[list[Attachment]] = relationship(
        back_populates="ticket", cascade="all, delete-orphan"
    )


class TicketMessage(Base, TimestampMixin):
    """A single message in a ticket's conversation thread."""

    __tablename__ = "ticket_messages"
    __table_args__ = (Index("ix_ticket_messages_ticket_id", "ticket_id"),)

    id: Mapped[UuidPK]
    ticket_id: Mapped[UuidPK] = mapped_column(
        ForeignKey("tickets.id", ondelete="CASCADE"), nullable=False
    )
    author_id: Mapped[UuidPK] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"), nullable=False
    )
    body: Mapped[str] = mapped_column(Text, nullable=False)
    body_html: Mapped[str | None] = mapped_column(Text)
    internal_note: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    language_detected: Mapped[str | None] = mapped_column(String(8))

    ticket: Mapped[Ticket] = relationship(back_populates="messages")


class Attachment(Base, TimestampMixin):
    """File attached to a ticket or message. References S3-compatible storage."""

    __tablename__ = "attachments"

    id: Mapped[UuidPK]
    ticket_id: Mapped[UuidPK] = mapped_column(
        ForeignKey("tickets.id", ondelete="CASCADE"), nullable=False
    )
    message_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("ticket_messages.id", ondelete="SET NULL")
    )
    filename: Mapped[str] = mapped_column(String(512), nullable=False)
    content_type: Mapped[str] = mapped_column(String(255), nullable=False)
    size_bytes: Mapped[int] = mapped_column(Integer, nullable=False)
    s3_key: Mapped[str] = mapped_column(String(1024), nullable=False)
    scan_status: Mapped[str] = mapped_column(
        String(16), default="pending", nullable=False
    )
    """``pending`` until ClamAV completes, then ``clean`` or ``infected``."""

    ticket: Mapped[Ticket] = relationship(back_populates="attachments")
