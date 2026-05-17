# syntax=docker/dockerfile:1.7
ARG PYTHON_VERSION=3.12-slim

FROM python:${PYTHON_VERSION} AS base
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never

RUN apt-get update && apt-get install -y --no-install-recommends \
      build-essential libpq-dev curl \
    && rm -rf /var/lib/apt/lists/*

# uv is statically linked; copy it from the official image
COPY --from=ghcr.io/astral-sh/uv:0.5 /uv /uvx /usr/local/bin/

WORKDIR /app

# Dependency layer (cached unless pyproject changes)
COPY pyproject.toml ./
COPY uv.lock* ./
RUN uv sync --frozen --no-dev || uv sync --no-dev

# Application source
COPY src ./src
COPY alembic ./alembic
COPY alembic.ini ./
COPY scripts ./scripts

ENV PATH="/app/.venv/bin:${PATH}"

EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
  CMD curl -fsS http://localhost:8000/healthz || exit 1

USER 1001:1001
CMD ["uvicorn", "helpdesk.main:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers"]
