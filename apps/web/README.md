# `apps/web` — Next.js Frontend

Bilingual (ar/en, RTL/LTR) Next.js 14 App Router application.

> **Status:** scaffolded in Phase 1. Implementation lands in Phase 5 per the [PRD](../../docs/PRD.md). See [ADR-0007](../../docs/decisions/0007-nextjs-app-router.md) and [ADR-0008](../../docs/decisions/0008-next-intl-for-i18n.md) for the choices baked into this layout.

## Layout (target)

```
src/
  app/[locale]/         # ar | en routing
  components/           # shadcn primitives + feature components
  lib/                  # api client, auth, arabic-utils
  hooks/
  stores/               # Zustand
  styles/               # globals, rtl, arabic-fonts
  messages/             # ar.json, en.json (next-intl)
public/
  fonts/                # IBM Plex Sans Arabic, Tajawal, Cairo
tests/
  e2e/                  # Playwright — one spec per locale
  unit/                 # Vitest
  visual/               # snapshots
```

## Local dev

From the repo root: `make dev`.

To run only the web: `pnpm --filter ./apps/web dev`.
