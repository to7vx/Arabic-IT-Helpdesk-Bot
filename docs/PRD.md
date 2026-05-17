# Product Requirements Document — Arabic IT Helpdesk Bot

* **Version:** 0.1.0 (Phase 0 draft)
* **Owner:** Project maintainers
* **Status:** Living document. Updated per phase; major changes require an ADR.

---

## 1. Vision

An **open-source, self-hosted IT helpdesk** that treats Arabic — including Saudi/Gulf dialect, Arabizi, and Arabic–English code-switching — as a first-class language, not a translated afterthought. It uses modern Arabic NLP to triage tickets, suggest knowledge-base answers, and surface urgency, while remaining deployable on a single VPS by a small IT team.

## 2. Why now

* **Saudi Vision 2030** is driving large-scale enterprise digitization across the GCC.
* **Saudi PDPL** is now actively enforced (48 enforcement decisions in 2025–2026 per IAPP). Operators want local-first, residency-compliant tooling.
* **Off-the-shelf SaaS** (Zendesk, Freshdesk, Jira Service Management) has weak Arabic NLP and cross-border data-transfer concerns.
* **Open-source competitors** (Zammad, FreeScout, osTicket, Chatwoot) lack Arabic-specific NLP entirely.

## 3. Non-goals (v1)

* Live agent chat (we ship asynchronous ticketing first; chat is on the v1.x roadmap).
* Mobile native apps (PWA only at v1).
* Customer-facing AI chatbot that responds without human review.
* Translation of UI strings into languages other than Arabic and English.
* On-call / paging stack (we expose webhook hooks; operators wire PagerDuty/Opsgenie themselves).

## 4. Personas

### 4.1 Layla — End User (Riyadh, marketing manager)
* Speaks Arabic at home and at work; reads English in technical documents.
* Submits 2–4 tickets per quarter: "Outlook won't open," "VPN يطلب رمز إضافي."
* Wants: minimum effort to file a ticket, instant suggestion if her problem is in a KB article, status visibility, Arabic UI.

### 4.2 Ahmed — Tier-1 Agent (Jeddah, IT desk)
* Handles 30+ tickets/day across Arabic and English requesters.
* Pain today: translating tickets in his head, hunting KB articles by hand.
* Wants: auto-categorized inbox, top-5 KB suggestions per ticket, draft reply he can edit, ar↔en toggle, keyboard shortcuts that work in RTL.

### 4.3 Maha — Service-Desk Manager
* Owns SLAs across three teams (Network, Apps, Hardware).
* Wants: real-time SLA-breach view, agent workload, weekly category trends, exportable reports in Hijri + Gregorian dates.

### 4.4 Omar — Admin / IT Director
* Owns deployment, compliance, integrations.
* Wants: simple install (`make demo` for evaluation, Helm for prod), SSO, audit log, PDPL toolkit, no surprise outbound calls.

### 4.5 Noura — System Integrator (Dubai consultancy)
* Forks the project to deploy at customers.
* Wants: clean Apache 2.0 licence, customization points, language packs, theming, easy upgrades.

## 5. Top user stories (selected)

* **US-01** As an end user I can submit a ticket in Arabic and receive **suggested KB articles within 2 seconds** while typing.
* **US-02** As an agent I open a ticket and see an **AI-generated 3-sentence summary** plus the **top 5 ranked KB articles** with relevance scores.
* **US-03** As an agent I can apply the **suggested category** with one click; the suggestion is recorded as training data only if I edit it.
* **US-04** As a manager I view an **SLA dashboard** where dates can be toggled between Gregorian and Hijri without losing context.
* **US-05** As an admin I receive a **breach-notification draft** within minutes of a flagged incident, in the SDAIA-required format.
* **US-06** As an admin I can run the system in **fully air-gapped mode** with `LLM_PROVIDER=disabled` and all NLP features degrade gracefully.

(Full backlog maintained as GitHub Issues from Phase 2 onward.)

## 6. Functional requirements

| ID | Requirement | Phase |
|---|---|---|
| F-01 | Bilingual UI (ar + en) with proper RTL/LTR rendering on every page | 5 |
| F-02 | Ticket CRUD, threaded conversation, attachments with virus scan | 3 |
| F-03 | SLA tracking with configurable business hours per region | 3 |
| F-04 | Auto-escalation rules editable in UI | 3 |
| F-05 | Hybrid KB search (BM25 + dense + rerank) | 4 |
| F-06 | Multi-label category classifier (≥ 20 categories) | 4 |
| F-07 | Sentiment + urgency detection with confidence scores | 4 |
| F-08 | LLM-generated ticket summaries and draft replies (provider-pluggable) | 4 |
| F-09 | Email, Slack, Teams, WhatsApp Business, generic webhook integrations | 6 |
| F-10 | Admin: users, teams, categories, SLA policies, escalation rules | 3 |
| F-11 | DSR endpoints (export, delete, rectify) | 3 |
| F-12 | Audit log, append-only, hash-chained | 3 |
| F-13 | OpenAPI 3.1 spec with bilingual examples | 3 |
| F-14 | Real-time ticket updates over WebSocket | 3 |
| F-15 | Bilingual READMEs, docs site, ADRs | 1, 9 |

## 7. Non-functional requirements

| Category | Requirement |
|---|---|
| **Performance** | API p95 < 200 ms at 1000 RPS; NLP p95 < 500 ms (no LLM) / < 3 s (with LLM) |
| **Availability** | Single-host install: best-effort. HA Helm: 99.9% with three replicas |
| **Accessibility** | WCAG 2.2 AA minimum; axe-core CI gate; manual screen-reader pass each release |
| **Security** | OWASP Top 10 & OWASP API Top 10 mitigations documented and tested; STRIDE threat model |
| **Compliance** | PDPL, GDPR-compatible DSR endpoints; cross-border transfer ledger |
| **Operability** | One-command local install; Prometheus + Loki + Tempo out of the box |
| **Internationalization** | All UI strings localized; RTL parity verified by Playwright in both locales |
| **Quality** | ≥ 85% backend test coverage; ≥ 80% frontend; type-checked end-to-end |

## 8. Success metrics

| Metric | Target at v1.0 |
|---|---|
| Macro-F1 category classification (golden set) | ≥ 0.85 |
| Urgency-detection recall | ≥ 0.90 |
| KB retrieval MRR@10 | ≥ 0.75 |
| First-response time reduction (vs. baseline self-report) | -25% in 90-day pilot |
| Time-to-deploy for a fresh operator | < 10 minutes for `make demo`, < 1 hour for production Helm |
| Lighthouse score on portal | ≥ 95 each axis |
| Operators running v1 in production | ≥ 10 within 6 months of release |
| GitHub stars | ≥ 500 within 6 months (vanity but tracked) |

## 9. Out-of-scope explicitly

* On-prem Active Directory password reset bot (separate product surface).
* Hardware asset CMDB (we expose a webhook so existing CMDBs can integrate).
* Knowledge graph editing (KB is article-shaped, not graph-shaped, in v1).
* Per-ticket cost attribution.

## 10. Open questions (track in GitHub Issues)

* Q-01: Do we need an Egyptian-dialect-specific classifier head, or does MARBERT suffice?
* Q-02: How aggressive should we be about silently swapping Arabizi for Arabic before the user sees the suggestion?
* Q-03: Is Hijri date input required in tier-1 admin forms (e.g., SLA policy effective date)?

## 11. References

* [ADRs index](decisions/README.md)
* [Research notes](research/README.md)
