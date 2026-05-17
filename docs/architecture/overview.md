# Architecture Overview

```mermaid
flowchart LR
  subgraph Edge
    NX[nginx / Ingress]
  end
  subgraph Web
    WB[Next.js 14<br/>apps/web]
  end
  subgraph API
    AP[FastAPI<br/>apps/api]
    WK[Celery worker<br/>apps/api Dockerfile.worker]
  end
  subgraph Data
    PG[(PostgreSQL 16)]
    RD[(Redis 7)]
    QD[(Qdrant)]
    MN[(MinIO / S3)]
  end
  subgraph NLP
    PR[Preprocessing<br/>normalize · dialect · arabizi]
    CL[Classifiers<br/>category · sentiment · urgency]
    RT[Retrieval<br/>BGE-M3 + RRF + reranker]
    LL[LLM client<br/>claude · jais · disabled]
  end

  NX --> WB
  NX --> AP
  WB --> AP
  AP --> PG
  AP --> RD
  AP --> QD
  AP --> MN
  AP --> PR --> CL
  PR --> RT --> LL
  WK --> AP
  WK --> PG
```

## Request lifecycle (create ticket)

1. `apps/web` POSTs to `/api/v1/tickets`.
2. `tickets.create_ticket` router authenticates the caller, calls `ticket_service.create_ticket` which mints `public_id`, logs `created` event, and returns the serialized ticket.
3. Async work — NLP classify, embedding index update, webhook fan-out — is enqueued on Celery so the user does not wait.
4. A Redis pub/sub message fans the event to every connected `/ws/tickets` subscriber for that org.

## Modules

* `helpdesk.api.v1` — REST.
* `helpdesk.api.ws` — WebSocket.
* `helpdesk.services` — domain services (the only place that mutates state).
* `helpdesk.repositories` — read-only queries (Phase 3b).
* `helpdesk.nlp` — preprocessing, classification, retrieval, generation, evals.
* `helpdesk.integrations` — email, slack, teams, whatsapp, webhooks, csv.
* `helpdesk.workers` — Celery tasks.
* `helpdesk.middleware` — request-id, logging, security headers, rate limit, error handler.
* `helpdesk.observability` — structlog + OTLP.

## Cross-cutting concerns

* **Auth:** RS256 JWT short-lived access + rotating refresh in httpOnly cookie. RBAC via explicit permission strings (`helpdesk.services.rbac`).
* **Multi-tenancy:** Postgres RLS when `MULTI_TENANT=true`; otherwise every query still scopes by `org_id` because the seed always creates the `default` org.
* **PDPL:** `LLM_PROVIDER=disabled` default; every cross-border call appended to `cross_border_transfers`.

See [ADRs](../decisions/README.md) for rationale on every choice.
