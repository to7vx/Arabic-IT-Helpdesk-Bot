# Architecture Decision Records (ADRs)

This directory captures the architecturally significant decisions taken on this project. We use a lightweight variant of [Michael Nygard's ADR template](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions.html).

Every ADR has:

* a four-digit zero-padded number,
* a status (`Proposed` | `Accepted` | `Superseded by NNNN` | `Deprecated`),
* a date,
* a short rationale grounded in either [research](../research/) or operational reality,
* an explicit list of consequences (the trade-offs we are accepting).

If an ADR is superseded, **leave the old file in place** and add a note pointing to its replacement. The history is the point.

## Index

| # | Title | Status |
|---|---|---|
| 0001 | [Record architecture decisions](0001-record-architecture-decisions.md) | Accepted |
| 0002 | [Use FastAPI for the backend API](0002-use-fastapi.md) | Accepted |
| 0003 | [Arabic NLP encoder stack](0003-arabic-nlp-stack.md) | Accepted |
| 0004 | [Embeddings and vector store](0004-embeddings-and-vector-store.md) | Accepted |
| 0005 | [LLM provider strategy](0005-llm-provider-strategy.md) | Accepted |
| 0006 | [Arabic preprocessing pipeline](0006-arabic-preprocessing-pipeline.md) | Accepted |
| 0007 | [Next.js App Router for the web app](0007-nextjs-app-router.md) | Accepted |
| 0008 | [next-intl for i18n with ar/en](0008-next-intl-for-i18n.md) | Accepted |
| 0009 | [PostgreSQL with Arabic-aware full-text search](0009-postgres-arabic-fts.md) | Accepted |
| 0010 | [Redis + Celery for background work](0010-redis-celery-workers.md) | Accepted |
| 0011 | [MinIO for object storage](0011-minio-object-storage.md) | Accepted |
| 0012 | [Authentication and authorization model](0012-authn-authz-model.md) | Accepted |
| 0013 | [Observability stack](0013-observability-stack.md) | Accepted |
| 0014 | [Data residency and PDPL compliance](0014-data-residency-and-pdpl-compliance.md) | Accepted |
| 0015 | [Multi-tenancy model](0015-multi-tenancy-model.md) | Accepted |
| 0016 | [Monorepo with pnpm workspaces and uv](0016-monorepo-with-pnpm-and-uv.md) | Accepted |
| 0017 | [Apache 2.0 license](0017-apache-2-license.md) | Accepted |
| 0018 | [Container strategy: Docker + Helm](0018-container-strategy.md) | Accepted |
| 0019 | [NLP evaluation methodology](0019-nlp-evaluation-methodology.md) | Accepted |
| 0020 | [Conventional Commits and semantic release](0020-conventional-commits-and-semantic-release.md) | Accepted |
