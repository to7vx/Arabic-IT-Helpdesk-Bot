# 12. Authentication and authorization model

* **Status:** Accepted
* **Date:** 2026-05-17

## Context

The system has four primary roles (`end_user`, `agent`, `manager`, `admin`) plus multi-tenant enterprise deployments that need SSO.

## Decision

* **Local accounts:** email + Argon2id-hashed password; mandatory TOTP for `agent`/`manager`/`admin`.
* **Federation:** OAuth2 (Google, Microsoft Entra ID), SAML 2.0, and OIDC. Enterprise tenants can disable local accounts.
* **Tokens:**
  * Short-lived JWT access token (15 min, RS256).
  * Refresh token rotation, stored httpOnly + Secure cookie.
  * Revocation list in Redis for forced logout.
* **Authorization:** RBAC + per-object permissions. Permissions are explicit (`ticket.assign`, `kb.publish`, `admin.users.write`) — no role hardcoding in business logic.
* **Account lockout:** exponential backoff after 5 failed logins; unlocked by admin or password reset.
* **Audit:** every auth event (login, refresh, role change, MFA reset) recorded in `audit_log`.

## Consequences

* SSO is a Day-1 feature, not a paywall — fits the OSS positioning.
* JWT rotation and Redis revocation add complexity but eliminate "stuck session" risk after role change.
* Argon2id parameters tuned in `config.py` per deployment size.
