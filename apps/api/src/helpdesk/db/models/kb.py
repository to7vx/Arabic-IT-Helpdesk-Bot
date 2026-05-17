"""Knowledge base article, version, and feedback models."""

from __future__ import annotations

from sqlalchemy import Boolean, ForeignKey, Index, Integer, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column

from helpdesk.db.base import Base, SoftDeleteMixin, TimestampMixin, UuidPK


class KbArticle(Base, TimestampMixin, SoftDeleteMixin):
    """Bilingual knowledge-base article."""

    __tablename__ = "kb_articles"
    __table_args__ = (
        UniqueConstraint("org_id", "slug", name="uq_kb_articles_org_slug"),
        Index("ix_kb_articles_org_id", "org_id"),
    )

    id: Mapped[UuidPK]
    org_id: Mapped[UuidPK] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False
    )
    slug: Mapped[str] = mapped_column(String(255), nullable=False)
    title_en: Mapped[str] = mapped_column(String(500), nullable=False)
    title_ar: Mapped[str] = mapped_column(String(500), nullable=False)
    body_en: Mapped[str] = mapped_column(Text, nullable=False)
    body_ar: Mapped[str] = mapped_column(Text, nullable=False)
    category: Mapped[str | None] = mapped_column(String(64))
    tags: Mapped[list[str] | None] = mapped_column(ARRAY(String(64)))
    is_public: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    view_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    helpful_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    not_helpful_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)


class KbVersion(Base, TimestampMixin):
    """Append-only version history of a KB article."""

    __tablename__ = "kb_versions"
    __table_args__ = (Index("ix_kb_versions_article_id", "article_id"),)

    id: Mapped[UuidPK]
    article_id: Mapped[UuidPK] = mapped_column(
        ForeignKey("kb_articles.id", ondelete="CASCADE"), nullable=False
    )
    editor_id: Mapped[UuidPK] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"), nullable=False
    )
    title_en: Mapped[str] = mapped_column(String(500), nullable=False)
    title_ar: Mapped[str] = mapped_column(String(500), nullable=False)
    body_en: Mapped[str] = mapped_column(Text, nullable=False)
    body_ar: Mapped[str] = mapped_column(Text, nullable=False)
    change_note: Mapped[str | None] = mapped_column(Text)


class KbFeedback(Base, TimestampMixin):
    """Helpful / not-helpful vote on a KB article."""

    __tablename__ = "kb_feedback"

    id: Mapped[UuidPK]
    article_id: Mapped[UuidPK] = mapped_column(
        ForeignKey("kb_articles.id", ondelete="CASCADE"), nullable=False
    )
    user_id: Mapped[UuidPK] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    helpful: Mapped[bool] = mapped_column(Boolean, nullable=False)
    comment: Mapped[str | None] = mapped_column(Text)
