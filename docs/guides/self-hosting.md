# Self-hosting guide

The product is designed to run well on a single VPS. This guide walks through a production-grade single-host install on Ubuntu 22.04+, then points at the Helm chart for clustered installs.

## Minimum hardware

| Resource | Minimum | Recommended (50 agents) |
|---|---|---|
| vCPU | 2 | 4 |
| RAM | 4 GB | 8 GB (+4 GB if running local Jais) |
| Disk | 40 GB SSD | 100 GB SSD with snapshots |
| Network | 100 Mbit | 1 Gbit |

If you enable the NLP `[nlp]` extra with embedding inference on the same host, add 4 GB RAM. If you run a local Jais LLM, plan for 24 GB+ vRAM or use a separate GPU host.

## Domain and TLS

Point a hostname (e.g. `helpdesk.example.com`) at the host's public IP, then update `infra/docker/nginx/nginx.conf` with the hostname and enable the `ssl_certificate` lines once certbot has issued a cert.

## Backups

```bash
make backup
```

writes a dated directory under `./backups/YYYY-MM-DD/` containing the Postgres dump, the Qdrant snapshot, and a MinIO mirror. Move this off-host every day (any S3-compatible bucket with retention works).

## Updates

```bash
git fetch
git checkout v1.x.y          # pick the tag
make build && make stop && make dev
```

Database migrations run automatically on API startup; the migration plan is reviewed in every release's CHANGELOG.

## Going multi-host

When you outgrow a single VPS — typically when you cross ~100 concurrent agents — move to Kubernetes via the bundled Helm chart:

```bash
helm install helpdesk infra/k8s/helm/arabic-helpdesk \
  -n helpdesk --create-namespace \
  -f my-values.yaml
```

Override the conservative defaults in `values.yaml` and provide a real Secret (`externalSecrets.enabled=true`) backed by your secret manager.
