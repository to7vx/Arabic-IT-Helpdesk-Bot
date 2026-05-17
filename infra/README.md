# `infra/`

Everything operators need to run the system.

* [`docker/`](docker) — Compose files for dev, prod, and observability profiles. See [ADR-0018](../docs/decisions/0018-container-strategy.md).
* [`k8s/`](k8s) — Helm chart in `helm/arabic-helpdesk/` plus Kustomize overlays for dev/staging/prod.
* [`terraform/`](terraform) — AWS and GCP modules.
* [`ansible/`](ansible) — Optional bare-metal deployment playbooks.

> **Status:** scaffolded in Phase 1. Real manifests land in Phase 7 per the [PRD](../docs/PRD.md).
