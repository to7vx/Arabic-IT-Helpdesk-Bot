# 14. Data residency and PDPL compliance

* **Status:** Accepted
* **Date:** 2026-05-17

## Context

The product targets Saudi Arabia and the wider GCC; PDPL is actively enforced and treats every LLM call abroad as a regulated cross-border transfer.

See [research/saudi-pdpl.md](../research/saudi-pdpl.md).

## Decision

Architecture treats PDPL as a first-class concern, not an optional add-on:

1. **In-Kingdom default mode:** fresh installs default to LLM provider `disabled`. Enabling any cross-border feature requires explicit admin confirmation that is logged.
2. **Data subject rights as API:** `POST /api/v1/dsr/export`, `POST /api/v1/dsr/delete`, `POST /api/v1/dsr/rectify`. Webhooks fire on submission so operators can wire human review.
3. **Consent ledger:** dedicated `consents` table — purpose, basis, granted_at, withdrawn_at — referenced from every personal-data write.
4. **Cross-border transfer log:** every outbound call that includes PII is logged with destination, transferred field set, lawful basis, retention.
5. **Breach workflow:** an `incidents` table + bundled "SDAIA breach notification" template (Arabic + English) to support the 72-hour clock.
6. **Retention:** column-level `retention_days`; nightly job hard-deletes expired rows.
7. **Compliance documentation:** `docs/compliance/pdpl-checklist.md` ships with the product; operator signs off at install.

## Consequences

* Some features (Claude-generated drafts, WhatsApp Business) are off by default and require explicit cross-border opt-in.
* Anonymization helpers used by the eval suite ensure that golden ticket data shipped in the repo cannot identify real customers.
* We don't provide legal advice — disclaimer prominent in `SECURITY.md` and on the admin compliance screen.
