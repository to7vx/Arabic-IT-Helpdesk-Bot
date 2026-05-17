# Contributing

Thanks for considering a contribution. This document covers the local setup, conventions, and the review process. The shorter the path between "interesting idea" and "merged PR," the better.

---

## TL;DR

1. Fork → branch from `main` → write code with tests → open a PR with a Conventional Commit title.
2. CI must be green. NLP changes also need eval thresholds to hold.
3. Add an ADR if you're changing an architectural decision.

---

## Local setup

You need:

* Python 3.12+ (managed via [uv](https://docs.astral.sh/uv/))
* Node.js 20+ and pnpm 9+
* Docker + Docker Compose v2
* Make

```bash
git clone https://github.com/<org>/arabic-helpdesk-bot
cd arabic-helpdesk-bot
make setup          # installs python + node deps, sets up pre-commit, generates JWT keys
make dev            # boots postgres/redis/qdrant/minio + api + web
```

Visit:

* Web: http://localhost:3000
* API docs: http://localhost:8000/docs
* Grafana (optional): `make dev-observability` then http://localhost:3001

---

## Branches and commits

* Branch off `main`. Naming: `feat/<short-slug>`, `fix/<short-slug>`, `docs/<short-slug>`.
* **Conventional Commits** required on PR titles and commit messages. Examples:
  * `feat(nlp): add Arabizi transliterator`
  * `fix(api): retry IMAP fetch on transient ssl error`
  * `docs(adr): add ADR-0021 for outbox pattern`
  * Breaking changes append `!` (`feat(api)!: remove deprecated v0 endpoints`) and include a `BREAKING CHANGE:` footer.

`commitlint` runs as a pre-commit hook and a CI check.

---

## Code style

* **Python:** ruff format + ruff lint + mypy --strict. Type everything.
* **TypeScript:** strict TS, ESLint, Prettier. No `any` without a comment justifying it.
* **SQL:** keep migrations forward-compatible with the previous app version (zero-downtime deploys).
* **Comments:** write *why*, not *what*. Identifiers do the *what*.
* **Arabic content:** use NFC normalization. Avoid mixing ALEF forms in literals — pick one and add a comment when it matters.

---

## Tests

| Surface | Tooling | Where to add |
|---|---|---|
| API unit | pytest | `apps/api/tests/unit/` |
| API integration | pytest + testcontainers | `apps/api/tests/integration/` |
| NLP evals | custom runner | `apps/api/src/helpdesk/nlp/evals/` |
| Web unit | Vitest + Testing Library | `apps/web/tests/unit/` |
| Web E2E | Playwright | `apps/web/tests/e2e/` (one spec per locale) |
| Load | k6 | `scripts/load/` |

Coverage gates: backend ≥ 85%, frontend ≥ 80%.

---

## Adding an Architecture Decision Record

If your change is architecturally significant — a new dependency at the layer level, a change to data residency, a swap of vector store, etc. — add an ADR under `docs/decisions/`:

1. Pick the next zero-padded number.
2. Copy the format of `0001-record-architecture-decisions.md`.
3. Reference your sources.
4. Link the ADR from the PR description.

---

## NLP changes

NLP code lives under `apps/api/src/helpdesk/nlp/`. Any change there must:

* Include unit tests.
* Run `scripts/run_evals.sh` and **not regress** the thresholds in `nlp/evals/thresholds.yml`.
* If the change affects preprocessing, bump `PREPROCESSING_VERSION` so historical comparisons stay honest.

For new datasets, see `docs/guides/labeling-guidelines.md`.

---

## Internationalization

* All user-visible strings go through `next-intl` (frontend) or `gettext`-style helpers (backend error messages).
* Every key must exist in **both** `ar.json` and `en.json` — `scripts/check_messages.py` enforces this in CI.
* When adding RTL-sensitive layout, prefer logical CSS (`ms-`, `me-`, `text-start`).

---

## Security

If you find a vulnerability **do not** open a public issue. See [SECURITY.md](SECURITY.md).

---

## Code of Conduct

By participating, you agree to abide by the [Code of Conduct](CODE_OF_CONDUCT.md).
