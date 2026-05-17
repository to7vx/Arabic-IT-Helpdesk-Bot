# 🤖 MASTER PROMPT: Arabic-Language IT Helpdesk Bot
## Complete A-to-Z Production Specification for Autonomous AI Build

---

## 📋 INSTRUCTIONS TO THE AI AGENT (READ FIRST)

You are tasked with building a **complete, production-ready, open-source Arabic IT Helpdesk Bot** from absolute zero to final deployment. This is **not a prototype** — this is the final shipped product.

### Mandatory Operating Principles

1. **Use EVERY available agent, skill, tool, and subagent** at your disposal. Do not skip any capability that could improve quality. This includes but is not limited to:
   - File creation skills (docx, pdf, pptx, xlsx)
   - Frontend design skills
   - Code execution & testing environments
   - Web search for current best practices, library versions, and Arabic NLP research
   - Skill-creator for any custom skills needed
   - Theme-factory for UI styling
   - Any agentic loop, planner, or verifier available

2. **Do NOT optimize for time.** Take as many days, iterations, and tool calls as required. Quality > speed.

3. **Do NOT stop at "good enough."** Every component must be production-grade: tested, documented, secure, performant, accessible, and internationalized.

4. **Self-verify at every stage.** After building each module, run it, test it, write evals for it, and fix everything that breaks. Never hand off broken code.

5. **Document as you go.** Every file gets comments. Every module gets a README. Every API gets OpenAPI specs. Every decision gets an ADR (Architecture Decision Record).

6. **Think in commits.** Structure work as atomic, well-described git commits with conventional commit messages. Push to a feature branch, then merge via PR with full description.

7. **If you encounter ambiguity**, make the most defensible engineering decision and document why in `docs/decisions/`. Do not pause to ask.

8. **Final deliverable**: A repository the maintainer can `git clone`, run `make setup && make dev`, and have a working bot in under 10 minutes — with a one-click deploy option to a cloud provider.

---

## 🎯 PROJECT OVERVIEW

### What We're Building
An **open-source IT helpdesk ticketing system** with first-class Arabic language support, designed for the Saudi/GCC market (Jeddah, Riyadh, Dammam, Dubai, Doha, etc.). It uses Arabic NLP to:

- **Auto-categorize** incoming tickets (hardware, software, network, account, security, etc.)
- **Suggest relevant Knowledge Base (KB) articles** to agents and end-users
- **Detect urgency and sentiment** to escalate critical tickets automatically
- **Handle code-switching** (mixed Arabic/English text, "Arabizi" Latin-script Arabic)
- **Support dialects**: MSA (Modern Standard Arabic), Saudi/Gulf, Egyptian, Levantine
- **Provide a bilingual UI** (Arabic RTL + English LTR with seamless switching)

### Why It Matters
Saudi Vision 2030 is driving massive digitization. Most off-the-shelf helpdesk tools (Zendesk, Freshdesk, Jira Service Desk) have weak Arabic support. This product fills a real gap and showcases bilingual IT engineering skill — a premium differentiator in the Jeddah/Riyadh job market.

### License
**Apache 2.0** — permissive, business-friendly, allows commercial forks.

---

## 🏗️ HIGH-LEVEL ARCHITECTURE

```
┌──────────────────────────────────────────────────────────────────┐
│                         FRONTEND (Next.js 14)                     │
│   - Bilingual UI (ar/en) with next-intl                          │
│   - RTL/LTR auto-switching                                       │
│   - Ticket inbox, KB browser, admin dashboard                    │
│   - Agent workspace with AI suggestions panel                    │
└─────────────────────┬────────────────────────────────────────────┘
                      │ REST + WebSocket
┌─────────────────────▼────────────────────────────────────────────┐
│                    API GATEWAY (FastAPI)                          │
│   - Auth (JWT + OAuth2)                                          │
│   - Rate limiting, RBAC, audit logging                           │
│   - WebSocket for real-time ticket updates                       │
└──┬───────────────┬──────────────┬─────────────────┬──────────────┘
   │               │              │                 │
   ▼               ▼              ▼                 ▼
┌──────┐    ┌───────────┐  ┌────────────┐    ┌────────────┐
│Tickets│   │ NLP Engine│  │ KB Service │    │Notification│
│Service│   │ (Arabic)  │  │ (RAG)      │    │  Service   │
└──┬────┘   └─────┬─────┘  └──────┬─────┘    └──────┬─────┘
   │              │                │                 │
   ▼              ▼                ▼                 ▼
┌──────────────────────────────────────────────────────────────┐
│  PostgreSQL  │  Redis  │  Qdrant (vector DB)  │  MinIO (S3)  │
└──────────────────────────────────────────────────────────────┘
```

### Tech Stack (NON-NEGOTIABLE choices unless agent has stronger reason)

| Layer | Choice | Why |
|---|---|---|
| Frontend | Next.js 14 (App Router) + TypeScript + Tailwind + shadcn/ui | Modern, bilingual-friendly |
| i18n | next-intl | Best-in-class for ar/en |
| Backend | Python 3.12 + FastAPI + Pydantic v2 | Async, typed, fast |
| DB | PostgreSQL 16 + SQLAlchemy 2.0 + Alembic | Battle-tested |
| Cache/Queue | Redis 7 + Celery | Standard |
| Vector DB | Qdrant | Self-hosted, fast |
| Object Storage | MinIO (S3-compatible) | Self-hosted |
| Arabic NLP | CAMeL Tools, Farasa, AraBERT, MARBERT, sentence-transformers (multilingual-e5-large) | Research-grade |
| LLM (optional) | Anthropic Claude API (with fallback to local Ollama + Jais-30B or AceGPT) | High quality Arabic |
| Auth | Authlib + OAuth2 + JWT, optional SSO (SAML/OIDC) | Enterprise-ready |
| Observability | OpenTelemetry + Prometheus + Grafana + Loki | Production standard |
| Container | Docker + docker-compose + Kubernetes (Helm chart) | Cloud-portable |
| CI/CD | GitHub Actions | Free for OSS |
| Testing | pytest + Playwright + k6 (load) | Comprehensive |
| Docs | MkDocs Material + Mermaid | Beautiful |

---

## 📂 REPOSITORY STRUCTURE (CREATE EXACTLY THIS)

```
arabic-helpdesk-bot/
├── .github/
│   ├── workflows/           # CI/CD pipelines
│   │   ├── ci.yml          # lint, test, build on every PR
│   │   ├── release.yml     # semantic-release on main
│   │   ├── docker.yml      # build & push images
│   │   ├── security.yml    # CodeQL, Trivy, Snyk
│   │   └── docs.yml        # deploy docs to GitHub Pages
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   ├── feature_request.md
│   │   └── arabic_nlp_issue.md   # special template for NLP bugs
│   ├── PULL_REQUEST_TEMPLATE.md
│   ├── CODEOWNERS
│   ├── FUNDING.yml
│   └── dependabot.yml
├── apps/
│   ├── web/                 # Next.js frontend
│   │   ├── src/
│   │   │   ├── app/
│   │   │   │   ├── [locale]/        # ar | en
│   │   │   │   │   ├── (auth)/
│   │   │   │   │   │   ├── login/
│   │   │   │   │   │   └── register/
│   │   │   │   │   ├── (dashboard)/
│   │   │   │   │   │   ├── tickets/
│   │   │   │   │   │   ├── kb/
│   │   │   │   │   │   ├── analytics/
│   │   │   │   │   │   ├── settings/
│   │   │   │   │   │   └── admin/
│   │   │   │   │   ├── portal/      # end-user portal
│   │   │   │   │   └── layout.tsx
│   │   │   │   └── api/             # Next.js API routes (BFF)
│   │   │   ├── components/
│   │   │   │   ├── ui/              # shadcn primitives
│   │   │   │   ├── tickets/
│   │   │   │   ├── kb/
│   │   │   │   ├── ai-suggestions/  # the "AI copilot" panel
│   │   │   │   ├── rtl/             # RTL-aware wrappers
│   │   │   │   └── shared/
│   │   │   ├── lib/
│   │   │   │   ├── api-client.ts    # typed API client (openapi-fetch)
│   │   │   │   ├── auth.ts
│   │   │   │   ├── arabic-utils.ts  # diacritic normalize, etc.
│   │   │   │   └── utils.ts
│   │   │   ├── hooks/
│   │   │   ├── stores/              # Zustand stores
│   │   │   ├── styles/
│   │   │   │   ├── globals.css
│   │   │   │   ├── rtl.css
│   │   │   │   └── arabic-fonts.css  # IBM Plex Arabic, Tajawal, Cairo
│   │   │   └── messages/
│   │   │       ├── ar.json
│   │   │       └── en.json
│   │   ├── public/
│   │   │   ├── fonts/               # self-host Arabic fonts
│   │   │   └── locales/
│   │   ├── tests/
│   │   │   ├── e2e/                 # Playwright
│   │   │   ├── unit/                # Vitest
│   │   │   └── visual/              # Percy / Chromatic snapshots
│   │   ├── playwright.config.ts
│   │   ├── next.config.js
│   │   ├── tailwind.config.ts
│   │   ├── tsconfig.json
│   │   ├── package.json
│   │   └── Dockerfile
│   │
│   └── api/                 # FastAPI backend
│       ├── src/
│       │   ├── helpdesk/
│       │   │   ├── __init__.py
│       │   │   ├── main.py              # FastAPI app factory
│       │   │   ├── config.py            # pydantic-settings
│       │   │   ├── deps.py              # dependency injection
│       │   │   ├── middleware/
│       │   │   │   ├── auth.py
│       │   │   │   ├── rate_limit.py
│       │   │   │   ├── logging.py
│       │   │   │   ├── tracing.py
│       │   │   │   └── error_handler.py
│       │   │   ├── api/
│       │   │   │   ├── v1/
│       │   │   │   │   ├── tickets.py
│       │   │   │   │   ├── kb.py
│       │   │   │   │   ├── users.py
│       │   │   │   │   ├── auth.py
│       │   │   │   │   ├── analytics.py
│       │   │   │   │   ├── admin.py
│       │   │   │   │   ├── webhooks.py
│       │   │   │   │   └── ai.py        # NLP endpoints
│       │   │   │   └── ws/
│       │   │   │       └── tickets.py   # WebSocket
│       │   │   ├── domain/              # domain models
│       │   │   │   ├── ticket.py
│       │   │   │   ├── user.py
│       │   │   │   ├── kb_article.py
│       │   │   │   └── audit.py
│       │   │   ├── db/
│       │   │   │   ├── base.py
│       │   │   │   ├── session.py
│       │   │   │   └── models/          # SQLAlchemy models
│       │   │   ├── repositories/        # repository pattern
│       │   │   ├── services/            # business logic
│       │   │   │   ├── ticket_service.py
│       │   │   │   ├── kb_service.py
│       │   │   │   ├── notification_service.py
│       │   │   │   ├── escalation_service.py
│       │   │   │   └── sla_service.py
│       │   │   ├── nlp/                 # ⭐ THE CORE
│       │   │   │   ├── __init__.py
│       │   │   │   ├── pipeline.py      # orchestrator
│       │   │   │   ├── preprocessing/
│       │   │   │   │   ├── normalizer.py     # Arabic normalization
│       │   │   │   │   ├── diacritics.py
│       │   │   │   │   ├── tokenizer.py      # Farasa wrapper
│       │   │   │   │   ├── arabizi.py        # Latin→Arabic transliteration
│       │   │   │   │   └── code_switch.py    # detect ar/en mix
│       │   │   │   ├── classification/
│       │   │   │   │   ├── category.py       # category classifier
│       │   │   │   │   ├── priority.py
│       │   │   │   │   ├── sentiment.py
│       │   │   │   │   └── urgency.py
│       │   │   │   ├── ner/
│       │   │   │   │   └── entities.py       # extract usernames, app names, error codes
│       │   │   │   ├── embeddings/
│       │   │   │   │   ├── model.py          # multilingual-e5-large
│       │   │   │   │   └── cache.py
│       │   │   │   ├── retrieval/
│       │   │   │   │   ├── kb_search.py      # hybrid: BM25 + dense
│       │   │   │   │   ├── reranker.py       # cross-encoder
│       │   │   │   │   └── qdrant_client.py
│       │   │   │   ├── generation/
│       │   │   │   │   ├── llm_client.py     # Anthropic / Ollama
│       │   │   │   │   ├── prompts.py        # Arabic-aware prompts
│       │   │   │   │   └── summarizer.py     # ticket summary
│       │   │   │   ├── routing/
│       │   │   │   │   └── agent_routing.py  # assign to right team
│       │   │   │   └── evals/                # NLP test suite
│       │   │   │       ├── golden_set.jsonl
│       │   │   │       ├── run_eval.py
│       │   │   │       └── metrics.py
│       │   │   ├── workers/
│       │   │   │   ├── celery_app.py
│       │   │   │   └── tasks/
│       │   │   │       ├── ticket_tasks.py
│       │   │   │       ├── nlp_tasks.py
│       │   │   │       ├── notification_tasks.py
│       │   │   │       └── embedding_tasks.py
│       │   │   ├── integrations/
│       │   │   │   ├── email/             # IMAP/SMTP ingest
│       │   │   │   ├── slack/
│       │   │   │   ├── teams/
│       │   │   │   ├── whatsapp_business/
│       │   │   │   └── webhook_dispatcher.py
│       │   │   └── utils/
│       │   ├── tests/
│       │   │   ├── unit/
│       │   │   ├── integration/
│       │   │   ├── e2e/
│       │   │   ├── conftest.py
│       │   │   └── fixtures/
│       │   ├── alembic/
│       │   ├── pyproject.toml
│       │   ├── uv.lock           # use `uv` package manager
│       │   ├── Dockerfile
│       │   └── Dockerfile.worker
│       │
├── packages/
│   └── shared-types/        # OpenAPI-generated types shared by FE/BE
│       └── package.json
│
├── infra/
│   ├── docker/
│   │   ├── docker-compose.yml
│   │   ├── docker-compose.dev.yml
│   │   ├── docker-compose.prod.yml
│   │   └── nginx/
│   ├── k8s/
│   │   ├── base/
│   │   ├── overlays/
│   │   │   ├── dev/
│   │   │   ├── staging/
│   │   │   └── prod/
│   │   └── helm/
│   │       └── arabic-helpdesk/
│   ├── terraform/
│   │   ├── aws/
│   │   ├── gcp/
│   │   └── modules/
│   └── ansible/             # optional bare-metal deploy
│
├── data/
│   ├── kb-seed/             # seed Arabic+English KB articles
│   │   ├── ar/
│   │   └── en/
│   ├── golden-tickets/      # 500+ labeled tickets for eval
│   ├── dialects/            # dialect samples for testing
│   └── README.md
│
├── docs/                    # MkDocs site
│   ├── index.md
│   ├── getting-started/
│   │   ├── installation.md
│   │   ├── quickstart.md
│   │   └── deployment.md
│   ├── architecture/
│   │   ├── overview.md
│   │   ├── nlp-pipeline.md
│   │   ├── data-flow.md
│   │   └── diagrams/        # mermaid + drawio
│   ├── api/                 # auto-gen from OpenAPI
│   ├── guides/
│   │   ├── arabic-nlp.md    # the centerpiece deep-dive
│   │   ├── adding-categories.md
│   │   ├── customizing-prompts.md
│   │   └── self-hosting.md
│   ├── decisions/           # ADRs
│   │   ├── 0001-record-architecture-decisions.md
│   │   ├── 0002-why-fastapi.md
│   │   ├── 0003-arabic-nlp-stack.md
│   │   └── ...
│   ├── contributing.md
│   ├── code-of-conduct.md
│   ├── security.md
│   └── mkdocs.yml
│
├── scripts/
│   ├── setup.sh             # one-command bootstrap
│   ├── seed_db.py
│   ├── seed_kb.py
│   ├── train_classifier.py
│   ├── run_evals.sh
│   ├── load_test.sh
│   └── backup.sh
│
├── .editorconfig
├── .gitignore
├── .gitattributes
├── .pre-commit-config.yaml
├── .env.example
├── LICENSE                  # Apache 2.0
├── README.md                # bilingual: English + Arabic sections
├── README.ar.md             # full Arabic version
├── CHANGELOG.md
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── SECURITY.md
├── SUPPORT.md
├── Makefile                 # `make setup`, `make dev`, `make test`, `make deploy`
└── package.json             # workspace root (pnpm)
```

---

## 🎬 PHASE-BY-PHASE BUILD PLAN

> **Execute every phase in order. Do not skip. After each phase, run the verification checklist before moving on.**

---

### **PHASE 0 — Research & Planning** (Use web search extensively)

**Tasks:**
1. Web-search latest (2026) best practices for:
   - Arabic NLP models (compare AraBERT v2/v02, MARBERT, CAMeLBERT, AraT5, Jais, AceGPT)
   - Multilingual sentence embeddings (BGE-M3, multilingual-e5-large-instruct, Cohere embed-multilingual-v3)
   - Arabic tokenization (Farasa vs CAMeL Tools vs Stanza)
   - Open-source helpdesk competitors (Zammad, FreeScout, OSTicket) — what they lack in Arabic
2. Survey Saudi/GCC regulations:
   - PDPL (Personal Data Protection Law)
   - SDAIA AI ethics framework
   - Data residency requirements
3. Generate `docs/research/` folder with markdown summaries of every finding, with sources cited.
4. Produce final `docs/decisions/` ADRs for every major tech choice based on this research.
5. Generate **product requirements doc** (`docs/PRD.md`) covering user personas, use cases, non-goals, success metrics.

**Verification:** ✅ At least 15 ADRs, all backed by citations. ✅ PRD reviewed for completeness.

---

### **PHASE 1 — Repository Foundation**

**Tasks:**
1. Initialize git repo with main branch protection rules documented.
2. Create entire folder structure above.
3. Write `.gitignore`, `.gitattributes` (handle Arabic file names & LF endings).
4. Write `LICENSE` (Apache 2.0 with NOTICE file).
5. Create `README.md` and `README.ar.md`:
   - Hero banner (use frontend-design skill to create SVG)
   - Badges (CI, coverage, license, downloads, Arabic NLP score)
   - Demo GIF placeholder
   - Quick-start (3 commands)
   - Architecture diagram (mermaid)
   - Feature list (bilingual)
   - Screenshots
   - Roadmap
   - Contributing link
   - Acknowledgments (CAMeL Lab, Farasa team, etc.)
6. Set up `Makefile` with targets: `setup`, `dev`, `test`, `lint`, `format`, `build`, `deploy`, `docs`, `evals`, `clean`.
7. Configure `pre-commit` (ruff, black, mypy, eslint, prettier, hadolint, gitleaks, codespell).
8. Set up GitHub Actions:
   - `ci.yml`: lint → test → build → upload coverage
   - `docker.yml`: build multi-arch images, push to ghcr.io
   - `security.yml`: CodeQL, Trivy, Snyk, OSV-Scanner
   - `release.yml`: semantic-release with conventional commits
   - `docs.yml`: build MkDocs, deploy to GitHub Pages
9. Add issue templates, PR template, CODEOWNERS, CONTRIBUTING, SECURITY.md, CODE_OF_CONDUCT.md.
10. Configure Dependabot for npm, pip, docker, github-actions.

**Verification:** ✅ Empty repo passes `make lint`. ✅ All CI workflows pass on empty PR. ✅ README renders correctly with RTL Arabic.

---

### **PHASE 2 — Database Schema & Migrations**

**Design these tables (use SQLAlchemy 2.0 + Alembic):**

- `users` (id, email, name_ar, name_en, role, locale_pref, sso_subject, password_hash, mfa_secret, created_at, ...)
- `organizations` (multi-tenant ready)
- `teams` (IT, network, security, apps, hardware, ...)
- `tickets` (id, public_id (TKT-YYYY-NNNNN), org_id, requester_id, assignee_id, team_id, title, description, language_detected, status, priority, category, subcategory, sentiment_score, urgency_score, sla_due_at, first_response_at, resolved_at, source, ...)
- `ticket_messages` (threaded conversation, internal_note flag, attachments)
- `ticket_events` (audit log: created, assigned, escalated, ai_suggested, ...)
- `kb_articles` (id, slug, title_ar, title_en, body_ar, body_en, category, tags[], embedding_vector_id, view_count, helpful_count, ...)
- `kb_feedback`
- `categories` (hierarchical: tree of categories with ar/en names)
- `sla_policies`
- `escalation_rules`
- `webhooks`
- `audit_log` (every state change with actor, before, after, ip, user_agent)
- `ai_suggestions` (track every NLP prediction for evals & training data)
- `attachments` (S3/MinIO refs, virus-scan status)

**Requirements:**
- All `text` columns must be `TEXT` (not VARCHAR) to handle Arabic.
- Use `pg_trgm` extension for fuzzy Arabic search.
- Add `tsvector` columns with Arabic-aware configuration.
- Row-level security policies for multi-tenancy.
- Soft-delete for tickets and KB articles.
- Indexes on every foreign key and common filter column.

**Tasks:**
1. Write Alembic migrations.
2. Write seed scripts: 50 categories (bilingual), 100 KB articles (50 ar + 50 en, real IT topics), 500 sample tickets, 20 users.
3. Write a `db.md` doc with ER diagram (mermaid) and column dictionary.

**Verification:** ✅ `make db-reset` recreates fresh DB. ✅ Seed data loads cleanly. ✅ All queries < 50ms on seed dataset.

---

### **PHASE 3 — Backend API (FastAPI)**

**Build out, fully:**

#### 3a. Core infrastructure
- App factory with lifespan
- Settings via pydantic-settings (env + secrets manager)
- Structured logging (structlog → JSON)
- OpenTelemetry instrumentation
- Health checks: `/healthz`, `/readyz`, `/metrics` (Prometheus)
- Error handlers with bilingual error messages
- CORS, security headers (helmet equivalent), CSRF for cookie auth

#### 3b. Auth
- Email/password with argon2id
- TOTP-based 2FA
- OAuth2 (Google, Microsoft Entra ID)
- SAML 2.0 for enterprise SSO
- OIDC support
- JWT (short-lived) + refresh tokens (rotating, in httpOnly cookie)
- RBAC: roles (admin, manager, agent, end_user) + permissions (granular)
- Password reset with rate limiting
- Account lockout after N failed attempts
- Audit every auth event

#### 3c. Tickets API (REST + WebSocket)
- Full CRUD + filters + pagination (cursor-based)
- Bulk operations
- Merge tickets
- Split tickets
- Internal notes vs public replies
- Attachment upload (multipart, virus scan via ClamAV)
- Real-time updates via WebSocket (Redis pub/sub backplane)
- SLA tracking with background timers
- Auto-escalation engine (rules: priority + age + sentiment)

#### 3d. KB API
- CRUD with bilingual content
- Markdown rendering with sanitization
- Versioning (track every edit)
- Public vs internal articles
- Search endpoint (hybrid BM25 + dense)
- Helpful/not-helpful voting

#### 3e. AI/NLP endpoints
- `POST /api/v1/ai/classify` — category prediction
- `POST /api/v1/ai/summarize` — ticket summary (ar/en)
- `POST /api/v1/ai/suggest-kb` — RAG over KB
- `POST /api/v1/ai/detect-urgency` — sentiment + urgency
- `POST /api/v1/ai/draft-reply` — agent assist
- `POST /api/v1/ai/translate` — ar↔en
- All endpoints: stream tokens via SSE where applicable
- All endpoints: cache hot results in Redis

#### 3f. Admin API
- User/team/role management
- Category management
- SLA policy editor
- Escalation rule builder
- Audit log viewer
- Bulk import (CSV) of tickets, KB articles
- Data export (GDPR-compliant)

**Requirements:**
- 100% type coverage (mypy --strict)
- OpenAPI 3.1 spec auto-generated, served at `/docs` and `/redoc`
- Every endpoint has request/response examples in **both Arabic and English**
- Every endpoint has unit + integration tests
- Pagination cursor never exposes IDs
- All write endpoints support idempotency keys

**Verification:** ✅ ≥ 85% test coverage. ✅ k6 load test: 1000 RPS with p95 < 200ms. ✅ OpenAPI lints clean.

---

### **PHASE 4 — Arabic NLP Pipeline (THE HEART)**

**This is the differentiator. Spend as long as needed here.**

#### 4a. Preprocessing
- Unicode normalization (NFC)
- Strip tatweel (kashida) `ـ`
- Normalize alef forms (إ أ آ → ا) configurably
- Normalize ya/alef-maqsura (ى ↔ ي) configurably
- Remove diacritics (tashkeel) with option to preserve
- Handle Eastern Arabic numerals (٠-٩ ↔ 0-9)
- Strip emojis but keep semantic ones
- Detect & route Arabizi (e.g., "msh 3aref el password") through transliteration
- Detect code-switching and segment

#### 4b. Tokenization & Morphology
- Wrap Farasa segmenter
- Wrap CAMeL Tools morphological analyzer
- Lemmatization for both MSA and Gulf dialect
- POS tagging

#### 4c. Language & Dialect Detection
- Language ID (ar vs en vs mixed) with confidence
- Dialect classification (MSA, Gulf, Egyptian, Levantine, Maghrebi)
- Fallback to character n-gram if model uncertain

#### 4d. Classification Models
- Train a **multi-label category classifier** on MARBERT/AraBERT
- Train a **priority classifier** (low/medium/high/urgent)
- Train a **sentiment model** (5-point: very_negative → very_positive)
- Train an **urgency detector** (binary: needs immediate escalation)
- Use distillation to produce small (< 100MB) ONNX models for fast inference
- Provide fallback zero-shot classification via Claude/LLM for unknown categories

#### 4e. NER
- Detect entities: usernames, emails, phone numbers, IP addresses, hostnames, error codes, application names (Microsoft Teams, Outlook, ...), department names
- Hybrid: regex + transformer NER

#### 4f. Embeddings & Vector Search
- Use `intfloat/multilingual-e5-large-instruct` for multilingual embeddings
- Index all KB articles in Qdrant with payload (lang, category, tags)
- Hybrid search: BM25 (Arabic-aware via Elasticsearch arabic analyzer OR rank_bm25 with custom tokenizer) + dense embeddings, fused with RRF
- Cross-encoder reranking with `BAAI/bge-reranker-v2-m3`

#### 4g. RAG for KB Suggestions
- Given ticket text → retrieve top-k KB articles
- Rerank
- LLM (Claude or local Jais) generates a concise answer **citing** the articles
- Response is bilingual or matches ticket language
- Strict citation: every claim grounded in retrieved chunks

#### 4h. Ticket Summarization
- Long thread → 3-sentence summary
- Available in ar/en

#### 4i. Auto-routing
- Map (category, priority, entities, business hours, agent skills) → team/agent
- Round-robin within team, respecting workload caps

#### 4j. Evaluation Suite
- Build a **golden dataset**: ≥500 manually-labeled Arabic tickets across dialects
- Metrics: F1 (macro/micro), precision@k for KB retrieval, MRR, latency, hallucination rate
- Run eval on every PR via GitHub Actions
- Publish results to a public dashboard
- Include adversarial test cases: typos, Arabizi, code-switch, sarcasm, dialect

**Tasks:**
1. Build the entire pipeline as composable Python modules.
2. Each component: unit-tested + benchmarked.
3. Provide model training scripts (`scripts/train_*.py`) with HuggingFace + Weights & Biases logging.
4. Quantize and export to ONNX for production.
5. Document everything in `docs/guides/arabic-nlp.md` (this should be a deep-dive article worthy of publication).

**Verification:**
- ✅ Macro-F1 ≥ 0.85 on category classification (golden set)
- ✅ MRR@10 ≥ 0.75 on KB retrieval
- ✅ p95 NLP latency < 500ms (without LLM) / < 3s (with LLM)
- ✅ Zero PII leakage in logs

---

### **PHASE 5 — Frontend (Next.js)**

#### 5a. Foundation
- Next.js 14 App Router, TypeScript strict, ESLint, Prettier
- Tailwind + shadcn/ui (install full set of components)
- next-intl with ar/en, automatic locale detection from Accept-Language + cookie
- **RTL handled correctly**: `dir="rtl"` on `<html>` when locale=ar, logical CSS properties everywhere (`ms-`/`me-` not `ml-`/`mr-`)
- Self-host Arabic fonts: IBM Plex Sans Arabic (primary), Tajawal, Cairo as fallbacks
- Dark mode + high-contrast mode
- Color palette: Saudi-flag-green accent + neutral grays, WCAG AAA

#### 5b. Authentication flows
- Login / Register / Forgot password / 2FA / SSO buttons
- All forms validated client + server, accessible (proper labels, error announcements)
- Smooth language toggle in top-right (persists)

#### 5c. End-User Portal
- Submit new ticket form
  - As user types, **live AI assistance** suggests:
    - Did you mean this category?
    - Have you tried these KB articles? (show top 3 with snippets)
  - File attachments with drag-drop
  - Language detected & shown with override option
- "My Tickets" list with status filters
- Ticket detail view with conversation thread, status timeline
- KB browser with search, categories, breadcrumbs, helpful voting

#### 5d. Agent Workspace
- Inbox with smart filters (assigned to me, urgent, breaching SLA, new)
- Ticket detail (split-pane):
  - Left: conversation + customer info + entity highlights
  - Right: **AI Copilot panel** with:
    - Auto-generated summary
    - Suggested category/priority (one-click to apply)
    - Top 5 KB articles (with relevance score)
    - Draft reply (editable, bilingual toggle)
    - Translate button (ar↔en for whole conversation)
    - Sentiment indicator
    - Similar past tickets
  - Quick actions: assign, escalate, merge, close, snooze
- Keyboard shortcuts (with RTL-friendly mappings)
- Macros / canned responses (bilingual)
- Internal vs public reply tabs

#### 5e. Manager Dashboard
- Charts: ticket volume, SLA compliance, agent performance, category breakdown, sentiment trend
- **Use Recharts**; all chart labels bilingual, axes flip for RTL
- Date-range picker (Hijri + Gregorian)
- Drill-down to ticket list
- Export to CSV/Excel

#### 5f. Admin Console
- User management
- Team management with skills
- Category tree editor (drag-drop, bilingual fields)
- SLA policy editor
- Escalation rule builder (visual if-then)
- AI settings (model, thresholds, prompts)
- Audit log viewer with search & export

#### 5g. Cross-cutting
- Toast notifications (sonner)
- Modal/dialog system
- Optimistic updates
- Real-time updates via WebSocket
- Offline support (PWA, service worker, queue actions)
- Empty states, skeleton loaders, error boundaries
- 404 / 500 pages (bilingual, helpful)
- Print stylesheet for ticket export

#### 5h. Testing
- Unit tests (Vitest) for components and hooks
- E2E (Playwright) — full user journeys in **both ar and en**
- Visual regression snapshots
- Accessibility: axe-core in CI, manual screen-reader pass

**Verification:**
- ✅ Lighthouse ≥ 95 on all metrics
- ✅ axe-core 0 violations
- ✅ Works perfectly RTL & LTR
- ✅ E2E suite passes in 2 languages
- ✅ Bundle size < 250KB initial JS

---

### **PHASE 6 — Integrations**

- **Email ingest**: IMAP poller + SES/SendGrid webhook → create ticket; SMTP for outbound
- **Slack**: slash commands `/ticket new`, thread sync, button actions
- **Microsoft Teams**: bot framework, adaptive cards
- **WhatsApp Business API**: receive customer messages → create tickets
- **Webhooks**: outbound (HMAC-signed) for ticket events
- **Zapier/Make**: publish triggers/actions
- **CSV/Excel import-export**

Each integration: own module, own tests, own docs page.

---

### **PHASE 7 — DevOps & Deployment**

- **docker-compose.yml** for one-command local dev (api, web, db, redis, qdrant, minio, mailhog, prometheus, grafana)
- **Production docker-compose** with nginx + Let's Encrypt
- **Helm chart** for Kubernetes with sane defaults + values for HA
- **Terraform modules** for AWS (ECS Fargate + RDS + ElastiCache + S3) and GCP (Cloud Run + Cloud SQL)
- **One-click deploy buttons**: Railway, Render, DigitalOcean App Platform, Vercel (frontend only)
- **Backup script**: pg_dump + qdrant snapshot + minio mirror → encrypted off-site
- **Disaster recovery runbook**
- **Observability stack**:
  - Prometheus scrape + Grafana dashboards (pre-built)
  - Loki for logs
  - Tempo for traces
  - Alerts via Alertmanager → Slack/Email/PagerDuty

**Verification:**
- ✅ `git clone && make setup && make dev` works on macOS, Linux, Windows (WSL2)
- ✅ Deploy to Kubernetes cluster end-to-end via Helm
- ✅ Chaos test: kill any pod, system recovers
- ✅ Backup → wipe → restore cycle works

---

### **PHASE 8 — Security Hardening**

- **OWASP Top 10**: explicit mitigation per item, documented
- **OWASP API Top 10**: same
- **Input validation everywhere** (Pydantic + zod)
- **SQL injection**: only parameterized queries (SQLAlchemy enforces)
- **XSS**: React escapes by default; sanitize KB markdown with DOMPurify
- **CSRF**: double-submit cookie pattern
- **Authn/Authz**: defense in depth
- **Secrets**: never in git; .env.example only; use SOPS or sealed-secrets for k8s
- **Dependency scanning**: Dependabot + Snyk + OSV
- **Container scanning**: Trivy + Grype in CI
- **SAST**: CodeQL, Semgrep
- **DAST**: ZAP scan in nightly CI
- **PII handling**: data classification doc; redaction in logs; encrypt at rest (DB + object storage)
- **GDPR + PDPL compliance**: data export endpoint, deletion endpoint, retention policies, data processing agreement template
- **Audit log**: append-only, hash-chained
- **Threat model**: STRIDE analysis documented in `docs/security/threat-model.md`
- **SECURITY.md** with disclosure policy and PGP key
- **Penetration test checklist**: provide for users to run themselves

---

### **PHASE 9 — Documentation Site**

Build a beautiful MkDocs Material site with:
- Landing page (hero + features + screenshots)
- Bilingual content (en primary, ar mirror)
- Getting Started → Installation → Configuration → Deployment
- User Guides (end-user, agent, manager, admin) — with screenshots
- **Arabic NLP Deep-Dive** — a flagship article (~5000 words) explaining the pipeline, with diagrams, benchmarks, and "lessons learned"
- API Reference (auto from OpenAPI)
- Developer Guide (architecture, contributing, testing, releasing)
- ADRs (all of them, browsable)
- Changelog
- Roadmap
- Glossary (bilingual)

Deploy to GitHub Pages on every main push.

---

### **PHASE 10 — Community & Launch Prep**

- **Demo data**: a `make demo` command that spins up the system with realistic Arabic-language tickets, KB articles, and users so visitors can try it
- **Live demo deployment**: deploy to a free tier (Fly.io or Railway) at `demo.<project>.dev` with read-mostly mode
- **Demo video**: write a script + storyboard (deliver as `.md`); leave actual recording to maintainer
- **Blog post draft** (`docs/blog/launch.md`): "Why I built an Arabic IT Helpdesk Bot" — story-driven, with technical highlights
- **LinkedIn post draft** in English and Arabic (3 variations each)
- **Hacker News "Show HN" draft**
- **Product Hunt** launch page copy
- **Twitter/X thread** draft (10 tweets, en + ar)
- **Submission to awesome lists**: awesome-arabic-nlp, awesome-selfhosted, awesome-helpdesk
- **Badges & shields**: collect everything in README

---

### **PHASE 11 — Final QA & Release**

1. Run **full regression test suite** end-to-end in both languages.
2. Run **load test** at 2x expected production load.
3. Run **security scan suite** — zero high/critical issues.
4. Run **accessibility audit** — zero violations.
5. Run **NLP eval suite** — meet all benchmarks.
6. **User testing simulation**: write a script that drives Playwright through 20 realistic Arabic & English user journeys and report any UX friction.
7. **Manually proofread** every Arabic UI string — no translation artifacts, proper grammar, correct dialect (MSA for UI, friendly tone).
8. **Tag v1.0.0**, generate release notes via semantic-release.
9. Publish Docker images to ghcr.io and Docker Hub.
10. Publish Helm chart to artifacthub.io.
11. Publish npm packages (shared-types) if applicable.
12. Update README with all final links.
13. **Pin the issue**: "v1.0.0 released — feedback welcome".

---

## ✅ FINAL DEFINITION OF DONE

The project is complete only when **ALL** of these are true:

### Code Quality
- [ ] `make lint` passes with zero warnings
- [ ] `make test` runs ≥ 800 tests, all pass
- [ ] Coverage ≥ 85% backend, ≥ 80% frontend
- [ ] `mypy --strict` and `tsc --noEmit --strict` both clean
- [ ] No `TODO`, `FIXME`, `XXX` left unaddressed (or all linked to issues)

### Functionality
- [ ] All 11 phases complete with their verification checklists ticked
- [ ] Every API endpoint documented with bilingual examples
- [ ] Every UI page works in both ar and en
- [ ] All 6 integrations (Email, Slack, Teams, WhatsApp, Webhooks, CSV) functional

### NLP Quality
- [ ] Category macro-F1 ≥ 0.85
- [ ] Urgency detection recall ≥ 0.90
- [ ] KB retrieval MRR@10 ≥ 0.75
- [ ] Handles all 5 dialects + Arabizi + code-switching
- [ ] Golden eval results published

### DevOps
- [ ] `git clone && make demo` works in under 10 minutes on a fresh machine
- [ ] Helm chart deploys cleanly to kind/minikube
- [ ] Terraform applies cleanly to a real AWS or GCP account
- [ ] Backup/restore tested and documented
- [ ] All container images scanned, zero high/critical CVEs

### Security
- [ ] OWASP Top 10 mitigations documented and tested
- [ ] PDPL + GDPR compliance checklist signed off
- [ ] Threat model published
- [ ] Penetration test checklist provided
- [ ] No secrets in git history (verified with gitleaks on full history)

### Documentation
- [ ] MkDocs site live on GitHub Pages
- [ ] README beautiful, badges accurate, screenshots up-to-date
- [ ] Arabic README (`README.ar.md`) parity with English
- [ ] ADRs cover every major decision (≥ 20 ADRs)
- [ ] Arabic NLP deep-dive published
- [ ] CONTRIBUTING guide makes it easy for new contributors

### Open Source Hygiene
- [ ] Apache 2.0 license + NOTICE
- [ ] Code of Conduct (Contributor Covenant 2.1)
- [ ] Security disclosure policy
- [ ] Issue templates, PR template, CODEOWNERS
- [ ] Dependabot configured
- [ ] Semantic versioning + automated releases
- [ ] CHANGELOG maintained

### Launch Readiness
- [ ] Live demo deployment accessible
- [ ] Demo video script written
- [ ] Launch blog post drafted (en + ar)
- [ ] Social media drafts ready (LinkedIn, Twitter, HN, PH)
- [ ] Submitted to ≥ 3 awesome lists

---

## 🧭 GUIDING PRINCIPLES (reminder during long build)

1. **Arabic is first-class**, not an afterthought. Every feature works equally well in ar as en.
2. **Saudi/GCC context matters**: support Hijri dates, Friday-Saturday weekends as configurable, business hours per region.
3. **Self-hosted-first**: a small IT shop with one VPS should be able to run this.
4. **No vendor lock-in**: optional cloud LLM, optional cloud anything. Everything works offline if needed.
5. **Composable**: every piece (NLP, KB, ticketing) should be usable standalone.
6. **Observable**: if it can't be measured, it's broken.
7. **Honest**: when the AI is unsure, it says so. No hallucinations dressed as facts.
8. **Inclusive**: accessibility is a hard requirement, not a stretch goal.

---

## 🚀 BEGIN

Start with **Phase 0** now. Use web search aggressively. Use every skill in your toolbox. Take as long as you need. Commit early, commit often, with conventional commit messages on a `develop` branch, opening PRs to `main` per phase.

When you complete the final phase and every checkbox above is ticked, tag `v1.0.0`, write the release notes, and present the maintainer with:

1. The GitHub repo URL (or git bundle)
2. The live demo URL
3. The docs site URL
4. A summary report (`FINAL_REPORT.md`) covering: what was built, what was learned, metrics achieved, known limitations, and roadmap for v1.1.

**Do not declare the project complete until every single item in "Final Definition of Done" is verified.**

Good luck. Build something the Jeddah/Riyadh tech community will be proud to use.

— End of master prompt —
