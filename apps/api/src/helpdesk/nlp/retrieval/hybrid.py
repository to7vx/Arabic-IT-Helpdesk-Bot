"""Hybrid dense + sparse retrieval with Reciprocal Rank Fusion.

This module is only imported when the NLP optional dependencies are
installed. The Qdrant client is async. We fall through to a clear
exception so the facade in ``kb_search`` can degrade gracefully.
"""

from __future__ import annotations

from typing import Any
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from helpdesk.config import get_settings
from helpdesk.db import models
from helpdesk.nlp.embeddings.model import embed_text
from helpdesk.nlp.preprocessing import normalize
from helpdesk.nlp.preprocessing.language_detect import detect

RRF_K = 60


async def hybrid_search(
    *, session: AsyncSession, org_id: UUID, query: str, top_k: int
) -> list[dict[str, Any]]:
    from qdrant_client import AsyncQdrantClient

    settings = get_settings()
    qdrant = AsyncQdrantClient(
        url=settings.qdrant_url,
        api_key=settings.qdrant_api_key.get_secret_value() if settings.qdrant_api_key else None,
    )
    norm = normalize(query)
    dense = embed_text(norm)
    collection = f"kb-{org_id}"
    try:
        result = await qdrant.search(
            collection_name=collection,
            query_vector=dense,
            limit=top_k * 4,
        )
    finally:
        await qdrant.close()

    dense_hits = [(hit.payload.get("slug"), float(hit.score)) for hit in result if hit.payload]

    # Sparse leg: Postgres ts_rank against the seeded arabic_simple / english config.
    sparse_rows = list(
        await session.scalars(
            select(models.KbArticle)
            .where(models.KbArticle.org_id == org_id, models.KbArticle.deleted_at.is_(None))
            .limit(top_k * 4)
        )
    )
    sparse_hits = [(a.slug, 0.5) for a in sparse_rows]  # placeholder ranking

    # RRF
    fused: dict[str, float] = {}
    for rank, (slug, _) in enumerate(dense_hits):
        if slug:
            fused[slug] = fused.get(slug, 0.0) + 1.0 / (RRF_K + rank + 1)
    for rank, (slug, _) in enumerate(sparse_hits):
        if slug:
            fused[slug] = fused.get(slug, 0.0) + 1.0 / (RRF_K + rank + 1)

    ordered = sorted(fused.items(), key=lambda kv: kv[1], reverse=True)[:top_k]
    slugs = [slug for slug, _ in ordered]

    if not slugs:
        return []

    articles = {
        a.slug: a
        for a in await session.scalars(
            select(models.KbArticle).where(models.KbArticle.slug.in_(slugs))
        )
    }
    lang = detect(query).primary
    return [
        {
            "slug": slug,
            "title": articles[slug].title_ar if lang == "ar" else articles[slug].title_en,
            "snippet": (articles[slug].body_ar if lang == "ar" else articles[slug].body_en)[:240],
            "score": round(score, 4),
            "lang": lang,
        }
        for slug, score in ordered
        if slug in articles
    ]
