# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

From the first tagged release onward, this file is maintained by `semantic-release` and should not be edited by hand except for the *Migration notes* subsections.

## [Unreleased]

### Added

**Phase 0 — research, ADRs, PRD**
- `docs/research/` with 6 cited notes (Arabic NLP encoders, multilingual embeddings, Arabic LLMs, Arabic tokenizers, Saudi PDPL, competitive landscape).
- `docs/decisions/` with 20 ADRs (record-decisions, FastAPI, NLP stack, embeddings, LLM strategy, preprocessing, Next.js, next-intl, Postgres FTS, Redis + Celery, MinIO, AuthN/AuthZ, observability, PDPL, multi-tenancy, monorepo, Apache 2.0, container strategy, NLP evals, Conventional Commits) + template + index.
- `docs/PRD.md` covering vision, 5 personas, 15 functional requirements, NFRs, 8 success metrics, explicit non-goals, open questions.

**Phase 1 — repository foundation**
- Apache 2.0 `LICENSE` + `NOTICE` with upstream attributions.
- `CONTRIBUTING`, `CODE_OF_CONDUCT` (Contributor Covenant 2.1), `SECURITY`, `SUPPORT`.
- Bilingual READMEs (`README.md` + `README.ar.md`).
- `Makefile` with 18 targets including `setup`, `dev`, `demo`, `test`, `evals`, `lint`, `format`, `build`, `docs`, `db-*`, `ci`.
- Project config: `.gitignore`, `.gitattributes`, `.editorconfig`, `.env.example`, `.pre-commit-config.yaml`, `.prettierrc`/`.prettierignore`, `.codespellignore`, `.license-header.txt`, `pnpm-workspace.yaml`, root `package.json`.
- 5 GitHub Actions workflows: `ci`, `release` (semantic-release), `docker` (multi-arch + SBOM), `security` (CodeQL + Trivy + OSV + Semgrep), `docs` (GitHub Pages).
- 3 issue templates incl. `arabic_nlp_issue`, PR template with bilingual screenshot + PDPL impact sections, `CODEOWNERS`, `FUNDING.yml`, `dependabot.yml` with grouped updates.

**Phase 2 — database**
- `apps/api/pyproject.toml` (uv-managed) with `[nlp]`, `[llm]`, `[integrations]`, `[dev]` extras.
- Full SQLAlchemy 2.0 async ORM (organizations, teams, users, oauth_accounts, categories, tickets, ticket_messages, attachments, ticket_events, kb_articles, kb_versions, kb_feedback, audit_log, ai_suggestions, embeddings, sla_policies, escalation_rules, consents, cross_border_transfers, webhooks).
- Hand-written Alembic initial migration creating all extensions, the custom `arabic_simple` text-search config, and the `tickets_tsvector_update` trigger.
- `scripts/seed_db.py` (org, teams, 20 users, 50 categories, 50/500 tickets) and `scripts/seed_kb.py` (paired-by-slug bilingual markdown loader).
- 3 matched bilingual KB articles under `data/kb-seed/`.
- `docs/architecture/db.md` with ER diagram.

**Phase 3 — FastAPI backend**
- App factory in `helpdesk.main` with full middleware stack (request-id, structured logging, security headers, gzip, CORS, token-bucket rate limit) and bilingual error envelope.
- `helpdesk.observability` wires structlog with PII redaction and OTLP tracing.
- `helpdesk.services.security` (Argon2id, TOTP, RS256/HS256 JWT) and `helpdesk.services.rbac` (explicit permission map + `require(...)` dependency).
- API v1 routers: `auth` (register, login w/ MFA, refresh, OAuth stubs, `/me`), `users`, `tickets`, `kb` (incl. hybrid search), `ai` (classify, suggest-kb, detect-urgency, summarize, draft-reply, translate), `admin`, `webhooks`, `dsr`.
- WebSocket `/ws/tickets` with Redis pub/sub fanout.
- `helpdesk.services.ticket_service` centralizes business rules.
- Unit tests under `apps/api/tests/unit/` (security primitives, RBAC hierarchy, error envelope, ticket_service against SQLite, health + OpenAPI shape).

**Phase 4 — Arabic NLP pipeline**
- `helpdesk.nlp.preprocessing` (normalize + language/dialect detect with Arabizi handling).
- `helpdesk.nlp.classification` (v0 category + urgency baselines, signature-compatible with future MARBERT).
- `helpdesk.nlp.retrieval` (BGE-M3 + Qdrant hybrid with RRF + Postgres-sparse fallback to ILIKE).
- `helpdesk.nlp.embeddings.model` (lazy-loaded BGE-M3 wrapper).
- `helpdesk.nlp.generation` (LLM client w/ claude / jais / disabled providers; bilingual prompts; summarizer, draft_reply, translator).
- `helpdesk.nlp.evals` (golden-set runner, metrics module, CI-enforced thresholds.yml).
- 20-row labeled golden set in `data/golden-tickets/v0_seed.jsonl`.
- Preprocessing + classifier unit tests.

**Phase 5 — Next.js frontend**
- App Router with `[locale]` segment, next-intl middleware, parity ar/en messages.
- Pages: home (bilingual hero), `/tickets` list, `/tickets/new` form, `/kb` browser, `/(auth)/login`, `/(dashboard)/agent/[id]` AI Copilot split-pane.
- Vendored `Button` + `LanguageToggle` UI primitives.
- Tailwind w/ brand palette + Arabic font stack; RTL-aware focus rings.
- Next.js platform security headers.
- Multi-stage Dockerfile.

**Phase 6 — integrations**
- `webhook_dispatcher` (HMAC-SHA256, exponential-backoff retry).
- `email/ingest` IMAP poller routed through `ticket_service`.
- `slack/handler` with Slack-spec signature verification.
- `teams`, `whatsapp_business` surface placeholders (PDPL-flagged).
- `csv_io` UTF-8-with-BOM round-trip preserving Arabic.
- Tests for webhook sig, CSV round-trip, Slack sig accept + stale reject.

**Phase 7 — DevOps**
- `apps/api/Dockerfile` + `Dockerfile.worker` multi-stage uv-based builds, non-root.
- `helpdesk.workers.celery_app` w/ email-ingest beat schedule and retrying webhook dispatch.
- `docker-compose.dev.yml` (full stack + optional observability profile), `docker-compose.prod.yml` (nginx + Let's Encrypt).
- `nginx.conf` with TLS, HSTS, security headers, `/metrics` denied externally.
- Helm chart skeleton (`infra/k8s/helm/arabic-helpdesk`).
- Terraform AWS scaffold defaulting to `me-south-1`.

**Phase 8 — security**
- `docs/security/threat-model.md` (STRIDE w/ trust-boundary diagram).
- `docs/security/owasp-top-10.md` (per-risk mapping to code).
- `docs/compliance/pdpl-checklist.md` (operator sign-off list).

**Phase 9 — docs site**
- `mkdocs.yml` (MkDocs Material + mermaid2).
- Getting-started: installation, quickstart, deployment.
- Architecture overview + DB ER.
- **Flagship `docs/guides/arabic-nlp.md`** (~2300 words, the deep-dive).
- `docs/guides/self-hosting.md`.

**Phase 10 — blog post**
- `docs/blog/launch.md` and `launch.ar.md` (bilingual launch essay).

### Known limitations at v0.1
- Category classifier is a keyword baseline; MARBERT v1 head is the next major piece.
- Golden set is 20 rows; target is ≥ 500.
- Backend tests are unit-only; integration suite via testcontainers is Phase 11b.
- No live demo deployment yet.
- shadcn/ui primitive set is intentionally minimal; expanded as features land.
- OAuth/SAML callbacks return 501; real wiring lands with production secrets.
