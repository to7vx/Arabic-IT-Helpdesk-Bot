# 4. Embeddings and vector store

* **Status:** Accepted
* **Date:** 2026-05-17

## Context

KB suggestion and "similar past tickets" features rely on dense retrieval. The corpus contains Arabic, English, and mixed text. Operators need self-hosting.

See [research/multilingual-embeddings.md](../research/multilingual-embeddings.md).

## Decision

* **Embedding model:** `BAAI/bge-m3` (dense + sparse + multi-vector in one model).
* **Vector store:** **Qdrant**, self-hosted, with payload index on `lang`, `category`, `org_id`.
* **Hybrid retrieval:** dense + sparse fused with Reciprocal Rank Fusion (RRF) at k=60.
* **Reranker:** `BAAI/bge-reranker-v2-m3`, applied to top 50 → keep top 5.
* **Cache:** Redis cache of `hash(text) → vector` with 7-day TTL.

## Consequences

* One model serves both Arabic and English; we don't maintain a parallel BM25 corpus.
* Qdrant adds an extra container in `docker-compose`; sensible default footprint (~512 MB RAM).
* Reranker is the slowest step — only invoked when `top_k_score < threshold` or operator enables "high-precision mode".
