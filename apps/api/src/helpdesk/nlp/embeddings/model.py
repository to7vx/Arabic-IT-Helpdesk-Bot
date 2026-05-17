"""Embedding model loader. Lazy + singleton.

We use BGE-M3 (see ADR-0004). Loading is deferred to first use so importing
this module never pulls torch into memory unless we actually embed.
"""

from __future__ import annotations

from functools import lru_cache
from typing import Any

from helpdesk.config import get_settings


@lru_cache(maxsize=1)
def get_model() -> Any:
    from sentence_transformers import SentenceTransformer

    name = get_settings().embedding_model
    return SentenceTransformer(name)


def embed_text(text: str) -> list[float]:
    model = get_model()
    vec = model.encode(text, normalize_embeddings=True)
    return [float(x) for x in vec.tolist()]


def embed_batch(texts: list[str], batch_size: int = 32) -> list[list[float]]:
    model = get_model()
    vecs = model.encode(texts, batch_size=batch_size, normalize_embeddings=True)
    return [[float(x) for x in v.tolist()] for v in vecs]
