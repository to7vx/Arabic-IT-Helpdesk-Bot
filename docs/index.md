# Arabic IT Helpdesk Bot

Open-source, self-hosted IT helpdesk with first-class Arabic-language support, dialect-aware NLP, a bilingual UI (Arabic RTL + English LTR), and a PDPL-aware deployment story for the Saudi and GCC market.

```mermaid
flowchart LR
  U([End user / Agent]) -->|HTTPS| W[Web<br/>Next.js 14]
  W -->|REST + WS| A[API<br/>FastAPI]
  A --> P[(PostgreSQL 16)]
  A --> R[(Redis 7)]
  A --> Q[(Qdrant)]
  A --> M[(MinIO)]
  A --> N[NLP pipeline<br/>MARBERT · BGE-M3 · CAMeL Tools]
  N -.optional.-> L[LLM<br/>Claude · Jais · disabled]
  A --> WK[Celery workers]
```

## Where to go next

* **[Quickstart](getting-started/quickstart.md)** — `git clone` to running stack in under 10 minutes.
* **[Arabic NLP deep-dive](guides/arabic-nlp.md)** — how the pipeline handles MSA, Gulf, Egyptian, Levantine, Arabizi, and code-switching.
* **[ADRs](decisions/README.md)** — every architecture decision with rationale.
* **[PDPL checklist](compliance/pdpl-checklist.md)** — sign-off list for operators in the Kingdom.

## License

[Apache 2.0](https://github.com/USER/arabic-helpdesk-bot/blob/main/LICENSE). Commercial-friendly forks welcome.
