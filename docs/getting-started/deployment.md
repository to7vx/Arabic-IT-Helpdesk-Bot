# Deployment

Two supported paths: single-host Docker Compose, and Kubernetes via the bundled Helm chart.

## Single host (Docker Compose)

```bash
cp .env.example .env   # edit POSTGRES_PASSWORD, SECRET_KEY, S3 keys, etc.
docker compose -f infra/docker/docker-compose.prod.yml up -d
```

`nginx` terminates TLS and `certbot` renews Let's Encrypt certs every 12 hours. Edit `infra/docker/nginx/nginx.conf` and uncomment the `ssl_certificate` lines once the cert exists.

## Kubernetes (Helm)

```bash
helm install helpdesk infra/k8s/helm/arabic-helpdesk \
  --create-namespace -n helpdesk \
  --set ingress.host=helpdesk.example.com \
  --set image.tag=0.1.0
```

`values.yaml` is conservative (`LLM_PROVIDER=disabled`, two API replicas, one worker). Override with `-f values-prod.yaml` for HA.

## Cloud providers

* **AWS:** Terraform scaffold in `infra/terraform/aws/`. Region defaults to `me-south-1` (Bahrain) to keep data in-Kingdom-adjacent.
* **GCP:** module surface lives under `infra/terraform/gcp/` (lands in Phase 7b).
* **One-click deploys:** Railway / Render / Fly buttons in `README.md` once a public release exists.

## Disaster recovery

```bash
make backup    # pg_dump + qdrant snapshot + minio mirror → ./backups/YYYY-MM-DD/
```

Restore by reversing the script; the full runbook lives at `docs/guides/disaster-recovery.md` (Phase 11b).
