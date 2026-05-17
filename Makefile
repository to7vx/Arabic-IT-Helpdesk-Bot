# =============================================================================
# Arabic IT Helpdesk Bot — top-level Makefile
# =============================================================================
# Conventions:
#   - Every target is .PHONY (no real files produced at the root).
#   - Targets compose well: `make setup && make dev` is the canonical onboarding.
#   - Each target prints what it's about to do so output stays readable in CI.
# =============================================================================

.DEFAULT_GOAL := help
SHELL         := /bin/bash
COMPOSE_DEV   := docker compose -f infra/docker/docker-compose.dev.yml
COMPOSE_PROD  := docker compose -f infra/docker/docker-compose.prod.yml

.PHONY: help setup dev dev-observability stop demo \
        test test-api test-web evals lint format typecheck \
        build build-api build-web docs docs-serve \
        db-reset db-migrate db-seed \
        notices clean ci

help: ## Show this help
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  \033[36m%-22s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

# -----------------------------------------------------------------------------
# Bootstrap
# -----------------------------------------------------------------------------
setup: ## One-shot install (python deps, node deps, pre-commit, JWT keys)
	@echo "==> Checking required tools"
	@command -v uv     >/dev/null || { echo "Missing tool: uv (https://docs.astral.sh/uv/)"; exit 1; }
	@command -v pnpm   >/dev/null || { echo "Missing tool: pnpm (https://pnpm.io/)"; exit 1; }
	@command -v docker >/dev/null || { echo "Missing tool: docker"; exit 1; }
	@echo "==> Installing Python deps (apps/api)"
	@cd apps/api && uv sync --all-extras
	@echo "==> Installing Node deps (workspace)"
	@pnpm install --frozen-lockfile || pnpm install
	@echo "==> Installing pre-commit hooks"
	@command -v pre-commit >/dev/null && pre-commit install --install-hooks || echo "(pre-commit not installed; skipping)"
	@echo "==> Generating dev JWT keys (./secrets/)"
	@mkdir -p secrets
	@test -f secrets/jwt-private.pem || openssl genrsa -out secrets/jwt-private.pem 4096
	@test -f secrets/jwt-public.pem  || openssl rsa -in secrets/jwt-private.pem -pubout -out secrets/jwt-public.pem
	@test -f .env || cp .env.example .env
	@echo "==> Setup complete. Run 'make dev' next."

# -----------------------------------------------------------------------------
# Development
# -----------------------------------------------------------------------------
dev: ## Boot full local stack (api, web, postgres, redis, qdrant, minio)
	$(COMPOSE_DEV) up --build

dev-observability: ## Boot dev stack including Prometheus, Grafana, Loki, Tempo
	$(COMPOSE_DEV) --profile observability up --build

stop: ## Stop and remove dev containers
	$(COMPOSE_DEV) down --remove-orphans

demo: ## Boot stack and seed bilingual demo data
	$(COMPOSE_DEV) up -d --build
	@echo "==> Waiting for API readiness"
	@until curl -sf http://localhost:8000/readyz >/dev/null; do sleep 2; done
	@cd apps/api && uv run python -m scripts.seed_db --demo
	@cd apps/api && uv run python -m scripts.seed_kb --demo
	@echo "==> Demo ready: http://localhost:3000 (admin/admin)"

# -----------------------------------------------------------------------------
# Tests / quality
# -----------------------------------------------------------------------------
test: test-api test-web ## Run all tests

test-api: ## Backend tests (pytest)
	@cd apps/api && uv run pytest -q

test-web: ## Frontend tests (vitest + playwright)
	@pnpm --filter ./apps/web test

evals: ## Run NLP eval suite against thresholds
	@cd apps/api && uv run python -m helpdesk.nlp.evals.run_eval

lint: ## Lint everything (ruff, mypy, eslint, prettier --check, hadolint)
	@cd apps/api && uv run ruff check . && uv run mypy src
	@pnpm -r lint
	@pnpm exec prettier --check "**/*.{ts,tsx,js,jsx,json,md,yml,yaml}"

format: ## Auto-format Python and JS
	@cd apps/api && uv run ruff format . && uv run ruff check --fix .
	@pnpm exec prettier --write "**/*.{ts,tsx,js,jsx,json,md,yml,yaml}"

typecheck: ## Strict typecheck only
	@cd apps/api && uv run mypy src
	@pnpm -r typecheck

# -----------------------------------------------------------------------------
# Build / deploy
# -----------------------------------------------------------------------------
build: build-api build-web ## Build all production images

build-api: ## Build API container image
	docker build -t arabic-helpdesk/api:dev -f apps/api/Dockerfile apps/api

build-web: ## Build web container image
	docker build -t arabic-helpdesk/web:dev -f apps/web/Dockerfile apps/web

# -----------------------------------------------------------------------------
# Documentation
# -----------------------------------------------------------------------------
docs: ## Build the MkDocs site
	@cd docs && uv run mkdocs build

docs-serve: ## Serve docs locally with live reload
	@cd docs && uv run mkdocs serve -a 0.0.0.0:8001

# -----------------------------------------------------------------------------
# Database
# -----------------------------------------------------------------------------
db-reset: ## Drop, recreate, migrate, seed the dev database
	$(COMPOSE_DEV) exec -T postgres dropdb -U helpdesk --if-exists helpdesk
	$(COMPOSE_DEV) exec -T postgres createdb -U helpdesk helpdesk
	@$(MAKE) db-migrate
	@$(MAKE) db-seed

db-migrate: ## Run Alembic migrations
	@cd apps/api && uv run alembic upgrade head

db-seed: ## Seed bilingual sample data
	@cd apps/api && uv run python -m scripts.seed_db
	@cd apps/api && uv run python -m scripts.seed_kb

# -----------------------------------------------------------------------------
# Misc
# -----------------------------------------------------------------------------
notices: ## Regenerate THIRD_PARTY_NOTICES files
	@cd apps/api && uv run pip-licenses --format=plain --output-file=THIRD_PARTY_NOTICES
	@pnpm --filter ./apps/web exec license-checker --production --csv > apps/web/THIRD_PARTY_NOTICES

clean: ## Remove caches, build artefacts, node_modules
	@find . -type d -name "__pycache__" -prune -exec rm -rf {} + 2>/dev/null || true
	@find . -type d \( -name ".pytest_cache" -o -name ".ruff_cache" -o -name ".mypy_cache" \) -prune -exec rm -rf {} + 2>/dev/null || true
	@rm -rf apps/web/.next apps/web/out apps/web/node_modules
	@rm -rf node_modules .turbo coverage htmlcov

ci: lint typecheck test evals ## Full CI suite (used by Actions)
