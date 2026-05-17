# PDPL Compliance Checklist

> **Disclaimer:** this checklist helps operators meet Saudi Arabia's Personal Data Protection Law (PDPL). It is **not** legal advice. Operators remain the data controller and are responsible for their own compliance posture.

Sign off on each item before going to production. Re-review at every major release.

## 1. Lawful basis & consent

- [ ] Identified the lawful basis for every category of personal data we process (consent, contract, legitimate interest, legal obligation).
- [ ] Consent records are stored in the `consents` table with `purpose`, `lawful_basis`, `granted_at`, and `withdrawn_at`.
- [ ] End users can withdraw consent at any time via the portal Settings page.

## 2. Purpose limitation & data minimization

- [ ] No personal data is processed beyond the documented purpose.
- [ ] Ticket attachments are scanned and stored only for the retention window configured in `sla_policies` (default 365 days).

## 3. Data subject rights

- [ ] `POST /api/v1/dsr/export` works end-to-end; tested in `tests/integration/test_dsr.py` (Phase 11b).
- [ ] `POST /api/v1/dsr/rectify` is wired to a human-review queue.
- [ ] `POST /api/v1/dsr/delete` honors deletion within 30 days unless a legal hold applies.

## 4. Cross-border transfers

- [ ] `LLM_PROVIDER` is set deliberately. The default `disabled` means no transfer.
- [ ] If `LLM_PROVIDER=claude`, executed Standard Contractual Clauses (SCCs) with Anthropic and recorded the SCC reference in `cross_border_transfers.payload_summary`.
- [ ] If `LLM_PROVIDER=jais` and hosting is in-Kingdom, no cross-border transfer occurs.
- [ ] Slack, Teams, and WhatsApp integrations are **disabled by default**; enabling each appends an admin-confirmed entry to the transfer log.

## 5. Security

- [ ] Encryption in transit: TLS 1.2+ enforced at the ingress.
- [ ] Encryption at rest: Postgres, MinIO, and Qdrant volumes encrypted by the cloud provider or LUKS.
- [ ] Secrets (`SECRET_KEY`, JWT keys, OAuth secrets) live in a secret manager (Vault / Secrets Manager / sealed-secrets), not in git.
- [ ] MFA is required for `agent`/`manager`/`admin` roles.
- [ ] Audit log integrity check (hash chain) verified on a recurring schedule.

## 6. Breach notification

- [ ] Incident response runbook in `docs/security/incident-response.md` (Phase 8b).
- [ ] SDAIA notification template populated within 4 hours of detection so the 72-hour window is comfortable.
- [ ] Designated DPO contact email configured (`incident@<your-domain>`).

## 7. Controller registration & DPIA

- [ ] Registered as a data controller on SDAIA's National Data Governance Platform if required.
- [ ] Completed a Data Protection Impact Assessment (DPIA) before enabling any LLM provider that involves cross-border transfer.

## 8. Vendor due diligence

- [ ] Identified every sub-processor (Anthropic, Slack, Microsoft Teams, Meta/WhatsApp, your cloud provider, your CDN).
- [ ] Reviewed and documented each sub-processor's PDPL posture.

## 9. Retention

- [ ] Configured `retention_days` per data class; nightly job deletes expired rows.
- [ ] Backups are encrypted and rotated per the same retention policy.

## 10. Transparency

- [ ] Public privacy notice in Arabic and English linked from the portal footer.
- [ ] Cookie banner if any non-essential cookies are used.

---

**Signed off by:** ______________________  **Date:** ______________________
