# OWASP Top 10 (2021) — Mitigations

A mapping of OWASP's current top 10 web-app risks to where they are handled in this codebase. Reviewed each release.

| ID | Risk | Where we mitigate |
|---|---|---|
| **A01** Broken Access Control | RBAC with explicit permission strings (`helpdesk.services.rbac`); router dependencies enforce; `ticket_service` checks `org_id` before any read or write; multi-tenant deployments add Postgres RLS. Tests in `tests/unit/test_rbac.py` cover hierarchy invariants. |
| **A02** Cryptographic Failures | Argon2id password hashing with tuned parameters (`services.security.hash_password`); JWT signed with RS256 and keys loaded from disk (HS256 only in tests); TLS terminated by nginx with HSTS + HTTP/2; secrets never logged (`observability.logging._redact_pii`). |
| **A03** Injection | SQLAlchemy parameterized queries throughout — raw SQL only in Alembic migrations; Pydantic strict validation at every request boundary; React escapes JSX output by default; sanitize KB Markdown with DOMPurify on render. |
| **A04** Insecure Design | Architecture choices documented as ADRs; threat model lives in `docs/security/threat-model.md`; every PR template asks for a PDPL impact analysis when personal data or outbound integrations are touched. |
| **A05** Security Misconfiguration | Security-headers middleware applies a conservative set on every response; `next.config.js` adds platform-level headers; container images run as non-root; Helm chart ships a sane default `values.yaml`; pre-commit + CI catch leaked secrets via gitleaks. |
| **A06** Vulnerable & Outdated Components | Dependabot weekly across npm, pip, docker, github-actions, grouped to keep PR noise low; Trivy + OSV-Scanner + Semgrep run on every PR; container scans block HIGH/CRITICAL CVEs. |
| **A07** Identification & Authentication Failures | TOTP MFA mandatory for agent/manager/admin (`auth.mfa_enroll/verify`); exponential lockout after 5 failed logins; refresh-token rotation; SSO via Authlib (OAuth2, OIDC) and SAML for enterprise tenants; password policy enforced on register (≥12 chars). |
| **A08** Software & Data Integrity Failures | Container images built with Buildx provenance + SBOM (`docker.yml` workflow); semantic-release pins versions; outbound webhooks signed with HMAC-SHA256 (`integrations.webhook_dispatcher`); inbound Slack/Teams verified with the vendor's signature scheme. |
| **A09** Security Logging & Monitoring Failures | Structured JSON logs with PII redaction; `audit_log` table is append-only with a hash chain; Prometheus alert rules ship pre-configured for auth-failure spikes and webhook-failure rates; nginx denies `/metrics` from the public ingress. |
| **A10** Server-Side Request Forgery (SSRF) | The only outbound HTTP we make is to operator-configured webhook URLs and the configured LLM provider; both are admin-only inputs and additional URL allow-lists land with the integrations editor in Phase 7b. |

## OWASP API Top 10 (parallel mapping)

Covered in `docs/security/owasp-api-top-10.md` (a thin extension of the table above with API-specific notes on BOLA, mass assignment, and excessive data exposure).
