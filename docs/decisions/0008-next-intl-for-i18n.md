# 8. next-intl for i18n with ar/en

* **Status:** Accepted
* **Date:** 2026-05-17

## Context

Bilingual UI is a hard product requirement. Locale must influence routing (`/ar/...`, `/en/...`), `dir="rtl"` on the HTML root, date/number formatting (Gregorian + Hijri), and translation message catalogs.

## Decision

Use **next-intl** v3 with App Router middleware:

* Locales: `ar`, `en`. Default: detected from `Accept-Language`; persisted in cookie.
* Messages: ICU MessageFormat in `apps/web/src/messages/{ar,en}.json`.
* Routing: locale segment is required (`/[locale]/...`).
* Direction: derived from locale (`ar` → `rtl`).
* Dates: `Intl.DateTimeFormat`; Hijri via the `ar-SA-u-ca-islamic` calendar.

## Consequences

* Every page lives under `app/[locale]/...`; layouts set `<html lang dir>`.
* Translation review is part of PR review — we add a `messages-lint` step that fails if a key exists in one locale but not the other.
* No runtime locale switching without a route change (keeps SSR cache predictable).
