# Multilingual Sentence Embeddings

**Researched:** 2026-05  
**Decision affected:** [ADR-0004 Embeddings and vector store](../decisions/0004-embeddings-and-vector-store.md)

## Question

Which embedding model should index our Knowledge Base for retrieval-augmented suggestions across mixed Arabic/English tickets?

## Candidates

| Model | Dim | Strengths | Weaknesses |
|---|---|---|---|
| `intfloat/multilingual-e5-large-instruct` | 1024 | Instruction-tuned, strong baseline on MS MARCO / Mr. TyDi | Slightly weaker on low-resource langs |
| **`BAAI/bge-m3`** | 1024 | 100+ languages; dense + sparse + multi-vector in one model; long-context (8192) | Larger inference cost |
| `Cohere embed-multilingual-v3` | 1024 | Hosted, high recall | Closed source, vendor lock-in, PDPL transfer concerns |
| `text-embedding-3-large` (OpenAI) | 3072 | High accuracy | Same compliance/lock-in concerns |

## Empirical signal

* BGE-M3 supports 100+ languages and reports **stable performance on Arabic** where multilingual baselines (mDPR, mContriever) degrade (arXiv:2402.03216 §4).
* BGE-M3 dense embeddings alone match a Mistral-7B-backed E5 on English **and exceed it on non-English including Arabic** (BGE M3 paper, §4).
* BGE-M3's combined dense + sparse + ColBERT-style retrieval yields SOTA on MIRACL.

## Recommendation

* **Primary:** `BAAI/bge-m3` — single model gives us dense vectors, BM25-equivalent sparse weights, and ColBERT-style late interaction.
* Hybrid retrieval: dense + sparse fused with RRF, then cross-encoder rerank with `BAAI/bge-reranker-v2-m3`.
* Vector store: **Qdrant** (self-hosted, payload filtering, gRPC). Indexed payload includes `lang`, `category`, `org_id`, `published_at`.
* Caching: hash(text) → vector cached in Redis with 7-day TTL.

## Sources

- *M3-Embedding: Multi-Linguality, Multi-Functionality, Multi-Granularity Text Embeddings* (arXiv:2402.03216): https://arxiv.org/abs/2402.03216
- BGE-M3 model card: https://huggingface.co/BAAI/bge-m3
- BGE documentation: https://bge-model.com/bge/bge_m3.html
- *The Best Open-Source Embedding Models in 2026* (BentoML blog): https://www.bentoml.com/blog/a-guide-to-open-source-embedding-models
