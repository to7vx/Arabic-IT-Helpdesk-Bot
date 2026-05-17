# 11. MinIO for object storage

* **Status:** Accepted
* **Date:** 2026-05-17

## Context

Tickets accept file attachments (screenshots, logs). We need S3-compatible storage that works on a single VPS and scales to managed cloud later.

## Decision

* **Default:** **MinIO**, S3-compatible, single-binary, runs in `docker-compose` and Helm.
* **Production option:** swap `S3_ENDPOINT` to AWS S3, GCS (via S3 compatibility), or Backblaze B2.
* **Virus scanning:** **ClamAV** sidecar; uploads written to a quarantine bucket, scanned, then moved to canonical bucket. Tickets reference the canonical URL only after scan passes.
* **Access:** pre-signed URLs with short TTL; backend never proxies attachments.

## Consequences

* One library (`boto3`) covers MinIO and every major cloud.
* Attachments are scanned before any user can download them — important for IT helpdesk where users upload "suspicious file" samples.
* Encryption at rest via server-side encryption with operator-supplied keys; documented in security guide.
