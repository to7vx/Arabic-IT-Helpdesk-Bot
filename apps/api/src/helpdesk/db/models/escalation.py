"""SLA policies and escalation rules."""

from __future__ import annotations

from typing import Any
from uuid import UUID

from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from helpdesk.db.base import Base, TimestampMixin, UuidPK


class SlaPolicy(Base, TimestampMixin):
    """SLA policy. Operators can scope by category, priority, or team."""

    __tablename__ = "sla_policies"

    id: Mapped[UuidPK]
    org_id: Mapped[UuidPK] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    priority: Mapped[str | None] = mapped_column(String(16))
    category_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("categories.id", ondelete="SET NULL")
    )
    team_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("teams.id", ondelete="SET NULL")
    )
    first_response_minutes: Mapped[int] = mapped_column(Integer, nullable=False)
    resolution_minutes: Mapped[int] = mapped_column(Integer, nullable=False)
    business_hours: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False)
    """Per-region business hours, including Friday-Saturday weekend support."""
    active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


class EscalationRule(Base, TimestampMixin):
    """Conditional rule to escalate, reassign, or notify."""

    __tablename__ = "escalation_rules"

    id: Mapped[UuidPK]
    org_id: Mapped[UuidPK] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    condition: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False)
    """JSON DSL evaluated by ``EscalationService``."""
    action: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
