"""Organization (tenant) and team models."""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from helpdesk.db.base import Base, SoftDeleteMixin, TimestampMixin, UuidPK

if TYPE_CHECKING:
    from helpdesk.db.models.user import User


class Organization(Base, TimestampMixin, SoftDeleteMixin):
    """A tenant. In single-tenant deployments there is exactly one row."""

    __tablename__ = "organizations"

    id: Mapped[UuidPK]
    slug: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    name_en: Mapped[str] = mapped_column(String(255), nullable=False)
    name_ar: Mapped[str] = mapped_column(String(255), nullable=False)
    locale_default: Mapped[str] = mapped_column(String(8), default="ar", nullable=False)
    timezone: Mapped[str] = mapped_column(String(64), default="Asia/Riyadh", nullable=False)

    teams: Mapped[list[Team]] = relationship(back_populates="organization")


class Team(Base, TimestampMixin, SoftDeleteMixin):
    """A team within an organization (e.g. Network, Apps, Hardware)."""

    __tablename__ = "teams"
    __table_args__ = (UniqueConstraint("org_id", "slug", name="uq_teams_org_slug"),)

    id: Mapped[UuidPK]
    org_id: Mapped[UuidPK] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False
    )
    slug: Mapped[str] = mapped_column(String(64), nullable=False)
    name_en: Mapped[str] = mapped_column(String(255), nullable=False)
    name_ar: Mapped[str] = mapped_column(String(255), nullable=False)
    skills: Mapped[list[str]] = mapped_column(
        # Postgres-native ARRAY at migration time; portable to SQLite via JSON.
        String, default=list, nullable=False
    )

    organization: Mapped[Organization] = relationship(back_populates="teams")
    members: Mapped[list[TeamMember]] = relationship(back_populates="team")


class TeamMember(Base, TimestampMixin):
    """User <-> team association with workload cap."""

    __tablename__ = "team_members"
    __table_args__ = (
        UniqueConstraint("team_id", "user_id", name="uq_team_members_team_user"),
    )

    id: Mapped[UuidPK]
    team_id: Mapped[UuidPK] = mapped_column(
        ForeignKey("teams.id", ondelete="CASCADE"), nullable=False
    )
    user_id: Mapped[UuidPK] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    workload_cap: Mapped[int] = mapped_column(default=20, nullable=False)

    team: Mapped[Team] = relationship(back_populates="members")
    user: Mapped[User] = relationship()
