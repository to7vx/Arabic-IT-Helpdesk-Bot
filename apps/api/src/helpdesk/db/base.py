"""SQLAlchemy declarative base and shared column types.

All ORM models inherit from :class:`Base`. The base configures naming
conventions for indexes and constraints so Alembic produces stable,
predictable migration scripts.
"""

from __future__ import annotations

from datetime import datetime
from typing import Annotated
from uuid import UUID, uuid4

from sqlalchemy import DateTime, MetaData, String, func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


class Base(DeclarativeBase):
    """Declarative base with stable naming convention."""

    metadata = MetaData(naming_convention=NAMING_CONVENTION)


UuidPK = Annotated[
    UUID,
    mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4),
]
"""Primary-key column type backed by ``uuid`` for portability."""

ShortStr = Annotated[str, mapped_column(String(255))]


class TimestampMixin:
    """``created_at`` / ``updated_at`` columns managed by the database."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


class SoftDeleteMixin:
    """``deleted_at`` column; queries filter by ``deleted_at IS NULL`` in repos."""

    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
