# 13. Observability stack

* **Status:** Accepted
* **Date:** 2026-05-17

## Context

"If it can't be measured, it's broken." We need metrics, logs, and traces with bilingual-friendly dashboards and PDPL-compatible log handling (no raw PII in logs).

## Decision

* **Metrics:** Prometheus scrape of `/metrics`; pre-built Grafana dashboards committed in `infra/grafana/dashboards/`.
* **Logs:** structlog → JSON → stdout → Loki (Helm chart) or rotated files (`docker-compose`).
* **Traces:** OpenTelemetry SDK → OTLP → Tempo (Helm) or Jaeger (compose).
* **Alerting:** Alertmanager with bundled rules for: API error rate, NLP queue depth, SLA-breach rate, embedding index lag.
* **PII redaction:** structlog processor strips fields tagged `sensitive=True`; ticket text is **never** logged verbatim, only token counts and language tag.

## Consequences

* Observability stack adds ~6 extra containers in the dev compose; behind a `--profile observability` flag so the default `make dev` stays light.
* Operators can swap in their own backends — we only emit OTLP / Prometheus / structured JSON.
