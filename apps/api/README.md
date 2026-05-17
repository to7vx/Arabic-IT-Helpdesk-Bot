# `apps/api` — FastAPI Backend

FastAPI service plus Celery workers, Arabic NLP pipeline, and Alembic migrations.

> **Status:** scaffolded in Phase 1. Implementation lands in Phases 2–4 per the [PRD](../../docs/PRD.md). See [ADR-0002](../../docs/decisions/0002-use-fastapi.md), [ADR-0003](../../docs/decisions/0003-arabic-nlp-stack.md), [ADR-0006](../../docs/decisions/0006-arabic-preprocessing-pipeline.md), [ADR-0009](../../docs/decisions/0009-postgres-arabic-fts.md), and [ADR-0010](../../docs/decisions/0010-redis-celery-workers.md).

## Layout (target)

```
src/helpdesk/
  api/v1/               # REST endpoints
  api/ws/               # WebSocket
  middleware/
  domain/               # domain models
  db/                   # SQLAlchemy session + models
  repositories/
  services/             # business logic
  nlp/                  # Arabic NLP pipeline (the centerpiece)
    preprocessing/
    classification/
    ner/
    embeddings/
    retrieval/
    generation/         # LLM client (claude | jais | disabled)
    routing/
    evals/              # golden set + thresholds
  workers/              # Celery
  integrations/         # email, slack, teams, whatsapp_business
alembic/
tests/
```

## Tooling

* Package manager: [uv](https://docs.astral.sh/uv/) (`uv sync`, `uv run`).
* Format / lint: ruff.
* Types: mypy --strict.
* Tests: pytest, testcontainers for integration, custom runner for NLP evals.

## Local dev

From the repo root: `make dev` (full compose) or `cd apps/api && uv run uvicorn helpdesk.main:app --reload`.
