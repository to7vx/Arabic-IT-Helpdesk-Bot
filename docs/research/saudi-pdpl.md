# Saudi PDPL & Regional Compliance

**Researched:** 2026-05  
**Decision affected:** [ADR-0014 Data residency and PDPL compliance](../decisions/0014-data-residency-and-pdpl-compliance.md)

## Question

What concrete obligations does the Saudi Personal Data Protection Law (PDPL) impose on a self-hosted IT helpdesk product, and how do they shape architecture?

## Legal framing

* **Instrument:** Royal Decree M/19 (09/02/1443H ≈ 16 Sept 2021); enforceable since Sept 2024 (grace period expired).
* **Regulator:** Saudi Data and AI Authority (SDAIA).
* **Scope:** processes personal data of individuals **in Saudi Arabia**, including extraterritorial processors.
* **Penalty:** warning or fine up to **SAR 5 million**, doubled for repeat violations. SDAIA confirmed 48 enforcement decisions in 2025–2026 — the law is actively enforced.

## Core obligations relevant to this product

| Obligation | Architectural implication |
|---|---|
| Clear, documented, withdrawable **consent** | Consent records table; export endpoint; revocation flow; immutable audit log |
| **Purpose limitation** | Data-field-level tagging (`purpose`, `retention_days`); enforced via column policies |
| **Cross-border transfer controls** (SCCs / BCRs approved by SDAIA) | LLM provider abstraction with hard "in-Kingdom only" mode; transfer destinations enumerated in admin UI |
| **Breach notification ≤ 72h** to SDAIA | Built-in incident workflow with SDAIA-format report template |
| **Data subject rights** (access, rectification, erasure, portability) | First-class API endpoints, not bolt-ons |
| **Controller registration** on SDAIA's National Data Governance Platform | Operator-facing checklist; product doesn't register on operator's behalf |
| **Security measures** (organizational, technical, administrative) | Encryption at rest + in transit; RBAC; audit log; documented policies template |

## Adjacent regimes (covered by the same architecture)

* **GDPR** — substantially overlapping; our DSR endpoints satisfy both.
* **UAE PDPL** (Federal Decree-Law 45/2021) — similar consent + cross-border framework.

## Recommendation

1. Ship a **PDPL Compliance Toolkit** as a first-class feature: consent inventory, DSR endpoints, retention policies, transfer log, breach-report template.
2. Default deployment mode: **all data + LLM in-Kingdom**. Cross-border transfer requires explicit admin opt-in with a confirmation captcha and audit entry.
3. Bundle a `docs/compliance/pdpl-checklist.md` that operators sign off on at install time.
4. **Disclaimer:** product reduces compliance friction; it does not constitute legal advice. Operator remains the data controller.

## Sources

- ICLG, *Data Protection Laws and Regulations Report 2025-2026: Saudi Arabia*: https://iclg.com/practice-areas/data-protection-laws-and-regulations/saudi-arabia
- SDAIA, *Guide to the Saudi Personal Data Protection Law*: https://dgp.sdaia.gov.sa/wps/portal/pdp/knowledgecenter/details/GPDPL/
- IAPP, *Saudi PDPL's first anniversary: Amendments, enforcement and ongoing developments*: https://iapp.org/news/a/saudi-pdpl-s-first-anniversary-amendments-enforcement-and-ongoing-developments
- PwC Middle East, *Saudi Arabia Personal Data Protection Law*: https://www.pwc.com/m1/en/services/consulting/technology/cyber-security/navigating-data-privacy-regulations/ksa-data-protection-law.html
- SecureLink, *Saudi Personal Data Protection Law: Compliance Guide 2026*: https://www.securelink.sa/blogs/saudi-personal-data-protection-law-compliance-guide-2026/
