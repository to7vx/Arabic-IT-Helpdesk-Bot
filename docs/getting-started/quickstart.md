# Quickstart

The shortest path to a running stack with seeded data:

```bash
git clone https://github.com/USER/arabic-helpdesk-bot
cd arabic-helpdesk-bot
cp .env.example .env
make demo
```

Then open http://localhost:3000 in Arabic (default) or http://localhost:3000/en for English.

## What just happened

1. `make setup` installs every dep and generates an RS256 keypair for JWT in `./secrets/`.
2. `make demo` brings up Postgres, Redis, Qdrant, MinIO, the FastAPI backend, the Celery worker, and the Next.js web app.
3. Once `/readyz` returns OK, the seed scripts populate:
   * one organization (`default`),
   * five teams (Hardware, Network, Apps, Security, Onboarding),
   * twenty users including the demo admin,
   * the fifty-entry bilingual category tree,
   * 500 sample tickets across MSA, Saudi, and Arabizi.
   * the bundled bilingual KB articles.

## Login credentials

| Role | Email | Password |
|---|---|---|
| Admin | `admin@example.com` | `DemoPassword!123` |
| Agent | `ahmed.agent@example.com` | `DemoPassword!123` |
| Manager | `maha.manager@example.com` | `DemoPassword!123` |
| End user | `layla.user@example.com` | `DemoPassword!123` |

> **Note:** demo credentials are intentionally weak so users can explore. Run `make db-reset` and re-seed with a non-default password before exposing the stack on the public internet.
