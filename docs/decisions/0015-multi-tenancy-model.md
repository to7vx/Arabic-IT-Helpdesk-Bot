# 15. Multi-tenancy model

* **Status:** Accepted
* **Date:** 2026-05-17

## Context

Most installs are single-tenant (one IT shop). But MSPs and large enterprises with separate business units need isolated tenants in the same install.

## Decision

* **Default:** single tenant. Schema includes `org_id` on every personal-data and ticket-data row.
* **Multi-tenant mode:** enable via `MULTI_TENANT=true`. Tenants share the schema but every query is scoped via Postgres **Row-Level Security (RLS)** policies plus a `current_setting('app.org_id')` set by the API session.
* **Tenant onboarding:** admin-only `POST /api/v1/admin/organizations`. Provisioning hooks create per-tenant Qdrant collections.
* **Hard isolation:** offered as separate deployments (one DB per tenant). RLS is for "logical" multi-tenancy.

## Consequences

* RLS adds a small per-query cost; mitigated by ensuring the GUC is set once per connection in pool checkout.
* Background workers must set the org context explicitly when consuming tasks.
* Migration tests run with RLS on to catch missing policies.
