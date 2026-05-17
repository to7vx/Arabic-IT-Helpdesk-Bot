# Installation

## Prerequisites

| Tool | Version | Why |
|---|---|---|
| Docker + Compose v2 | 24+ | Local dev stack |
| Node.js | 20+ | apps/web |
| pnpm | 9+ | Workspace package manager |
| Python | 3.12+ | apps/api |
| [uv](https://docs.astral.sh/uv/) | 0.5+ | Python deps |
| Make | any | Run the canonical targets |
| Git | 2.30+ | Conventional commits |

## One-shot setup

```bash
git clone https://github.com/USER/arabic-helpdesk-bot
cd arabic-helpdesk-bot
cp .env.example .env
make setup    # installs Python + Node deps, generates JWT keys, sets up pre-commit
make dev      # boots Postgres, Redis, Qdrant, MinIO, API, Web
```

Visit:

* **Web:** http://localhost:3000
* **API docs:** http://localhost:8000/docs
* **MinIO console:** http://localhost:9001 (`minioadmin` / `minioadmin`)
* **MailHog:** http://localhost:8025

## Seed bilingual demo data

```bash
make demo
```

Logs in: `admin@example.com` / `DemoPassword!123`.
