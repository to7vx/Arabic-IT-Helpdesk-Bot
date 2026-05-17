# Security Policy

We take the security of this project seriously. Thank you for taking the time to disclose responsibly.

## Reporting a vulnerability

**Do not open a public GitHub issue for security reports.**

Please email **security@arabic-helpdesk.dev** with:

* a description of the issue,
* steps to reproduce or proof of concept,
* impact assessment,
* any suggested mitigation,
* your name / handle if you'd like credit in the advisory.

For sensitive reports, encrypt with our PGP key (fingerprint published at `https://arabic-helpdesk.dev/.well-known/pgp-key.txt`).

## Response timeline

| Step | Target |
|---|---|
| Acknowledgement | within 2 business days |
| Triage and severity classification | within 5 business days |
| Fix in `main` for HIGH/CRITICAL | within 14 days |
| Public advisory (GHSA) and CVE | concurrent with the fix release |

## Supported versions

| Version | Supported |
|---|---|
| 1.x (latest minor) | Yes |
| 1.x (previous minor) | Security fixes for 90 days after a new minor |
| 0.x | No |

## Scope

In scope:

* The code in this repository (`apps/`, `packages/`, `infra/`, `scripts/`).
* Default container images we publish to `ghcr.io`.
* Documentation that could mislead a user into an insecure deployment.

Out of scope:

* Vulnerabilities in self-hosted operator deployments due to misconfiguration documented as risky.
* Third-party services (Slack, Microsoft Teams, WhatsApp) — report directly to those vendors.
* Social engineering, physical attacks, denial of service from a single source.

## Disclosure policy

We follow a 90-day coordinated disclosure window from the date you report. We will work with you on a timeline that accounts for fix complexity and operator upgrade windows.

## Compliance note

This product is designed to support PDPL, GDPR, and similar regimes — it does **not** constitute legal advice. Operators are responsible for their own compliance posture. See [docs/decisions/0014-data-residency-and-pdpl-compliance.md](docs/decisions/0014-data-residency-and-pdpl-compliance.md).
