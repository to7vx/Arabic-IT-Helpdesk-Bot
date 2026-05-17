# 18. Container strategy: Docker + Helm

* **Status:** Accepted
* **Date:** 2026-05-17

## Context

Operators range from "one VPS with Docker Compose" to "managed Kubernetes cluster." We target both without two parallel build systems.

## Decision

* **Image format:** multi-arch (amd64, arm64) OCI images via Docker Buildx, published to **ghcr.io** primary, Docker Hub mirror.
* **Local dev:** `docker compose -f infra/docker/docker-compose.dev.yml up`.
* **Production single-host:** `docker-compose.prod.yml` with nginx + Let's Encrypt sidecar.
* **Kubernetes:** Helm chart in `infra/k8s/helm/arabic-helpdesk` with sane defaults and a `values-ha.yaml` overlay for HA installs.
* **Base images:** `python:3.12-slim` (api/worker), `node:20-alpine` (web) → distroless final stage where possible.
* **CI image scanning:** Trivy + Grype; fail on `HIGH` or `CRITICAL`.

## Consequences

* Two delivery surfaces (compose + Helm) to maintain — accepted because target operators are evenly split.
* Image size budget: API < 800 MB, web < 250 MB, worker < 900 MB (with NLP libs).
