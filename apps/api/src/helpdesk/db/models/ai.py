"""AI suggestions log and embedding registry.

The ``ai_suggestions`` table records every prediction (category, priority,
sentiment, urgency, KB suggestions, draft reply) along with the model
version and preprocessing version. Combined with whether the agent
accepted or edited the suggestion, this becomes the training signal for
future model iterations.
"""

from __future__ import annotations

from typing import Any
from uuid import UUID

from sqlalchemy import Boolean, ForeignKey, Index, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from helpdesk.db.base import Base, TimestampMixin, UuidPK


class AiSuggestion(Base, TimestampMixin):
    """A single AI prediction for a ticket."""

    __tablename__ = "ai_suggestions"
    __table_args__ = (
        Index("ix_ai_suggestions_ticket_id", "ticket_id"),
        Index("ix_ai_suggestions_kind", "kind"),
    )

    id: Mapped[UuidPK]
    ticket_id: Mapped[UuidPK] = mapped_column(
        ForeignKey("tickets.id", ondelete="CASCADE"), nullable=False
    )
    kind: Mapped[str] = mapped_column(String(32), nullable=False)
    """``category`` | ``priority`` | ``sentiment`` | ``urgency`` | ``kb_suggest`` | ``draft_reply`` | ``summary``."""

    model_version: Mapped[str] = mapped_column(String(64), nullable=False)
    preprocessing_version: Mapped[str] = mapped_column(String(64), nullable=False)
    payload: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False)
    confidence: Mapped[float | None] = mapped_column()
    accepted: Mapped[bool | None] = mapped_column(Boolean)
    """``NULL`` = not yet reviewed; ``True`` = applied as-is; ``False`` = edited or rejected."""
    accepted_by: Mapped[UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL")
    )


class Embedding(Base, TimestampMixin):
    """Tracks which entities have been indexed in Qdrant and at what model version."""

    __tablename__ = "embeddings"
    __table_args__ = (
        Index(
            "ix_embeddings_entity",
            "entity_type",
            "entity_id",
            unique=True,
        ),
    )

    id: Mapped[UuidPK]
    entity_type: Mapped[str] = mapped_column(String(32), nullable=False)
    """``kb_article`` | ``ticket``."""
    entity_id: Mapped[str] = mapped_column(String(64), nullable=False)
    model: Mapped[str] = mapped_column(String(128), nullable=False)
    qdrant_collection: Mapped[str] = mapped_column(String(128), nullable=False)
    qdrant_point_id: Mapped[str] = mapped_column(String(64), nullable=False)
    content_hash: Mapped[str] = mapped_column(String(64), nullable=False)
