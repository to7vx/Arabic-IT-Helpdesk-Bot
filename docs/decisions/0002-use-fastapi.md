# 2. Use FastAPI for the backend API

* **Status:** Accepted
* **Date:** 2026-05-17

## Context

The backend must serve REST + WebSocket, host inference for Python NLP libraries (CAMeL Tools, transformers, Qdrant client), generate an OpenAPI spec for the typed frontend client, and run as a small footprint container.

## Decision

Use **FastAPI** (Python 3.12) with **Pydantic v2**, **SQLAlchemy 2.0 async**, **Alembic**, and **uv** for dependency management.

## Alternatives considered

* **Django + DRF** — heavier, ORM model less ergonomic for async NLP work, OpenAPI is an add-on.
* **Litestar** — promising but smaller ecosystem, fewer hires comfortable with it.
* **Node/NestJS** — would force us to call Python NLP via subprocess or HTTP, splitting the deployment.
* **Go** — best raw performance but Arabic NLP libraries are all Python-first.

## Consequences

* Native async fits well with WebSocket ticket updates and concurrent NLP calls.
* OpenAPI 3.1 spec auto-generated; `apps/web` consumes typed client via `openapi-fetch`.
* Workers (Celery) share the same Python codebase and models.
* We accept Python's per-request overhead vs. Go; mitigated by ONNX-quantized models and Redis caching.
