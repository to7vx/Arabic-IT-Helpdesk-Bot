# 10. Redis + Celery for background work

* **Status:** Accepted
* **Date:** 2026-05-17

## Context

Background jobs: NLP inference for batch reclassification, email IMAP polling, webhook dispatch, embedding (re)indexing, SLA timers, breach notifications.

## Decision

* **Broker + result backend:** Redis 7.
* **Worker framework:** Celery 5 with `prefork` pool for CPU-bound NLP and `gevent` pool for I/O-bound integrations.
* **Scheduler:** Celery Beat with `django-celery-beat`-style DB backend so admins can edit schedules at runtime.
* **Real-time pub/sub:** Redis pub/sub for WebSocket ticket-update fanout across API replicas.

## Alternatives considered

* **Dramatiq / Arq** — simpler but smaller ecosystems, fewer operator-familiar dashboards (Flower).
* **NATS** — overkill for our throughput.

## Consequences

* Two long-running services per environment (`worker`, `beat`).
* Redis is a single point of failure — Helm chart ships Redis Sentinel for HA.
* Flower dashboard available behind admin auth in non-production.
