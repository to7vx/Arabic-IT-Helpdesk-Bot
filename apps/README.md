# Applications

Two deployable apps live here:

* [`web/`](web) — Next.js 14 App Router frontend (TypeScript).
* [`api/`](api) — FastAPI backend with the NLP pipeline and Celery workers (Python 3.12).

Both are built from this monorepo and share OpenAPI-generated types via [`packages/shared-types`](../packages/shared-types).
