# 7. Next.js App Router for the web app

* **Status:** Accepted
* **Date:** 2026-05-17

## Context

We need a bilingual (ar/en, RTL/LTR), accessible web app with a rich agent workspace, dashboards, and a public end-user portal.

## Decision

* **Framework:** Next.js 14+ App Router, TypeScript strict.
* **Styling:** Tailwind CSS with logical properties (`ms-`/`me-`) so a single CSS works in RTL and LTR.
* **Component library:** shadcn/ui (vendored) — copy-in components we can edit, no runtime dependency on a library that may not test RTL.
* **State:** TanStack Query for server state, Zustand for ephemeral client state. No Redux.
* **Real-time:** native `WebSocket` + a thin reconnect wrapper.

## Consequences

* SSR and streaming work well for slow Arabic font payloads.
* Vercel-style deploy is *possible* but not assumed — operators can run `next start` behind nginx.
* shadcn vendoring means we own component code; we accept the maintenance cost in exchange for RTL polish.
