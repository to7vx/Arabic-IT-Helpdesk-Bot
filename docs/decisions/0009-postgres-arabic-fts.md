# 9. PostgreSQL with Arabic-aware full-text search

* **Status:** Accepted
* **Date:** 2026-05-17

## Context

Tickets and KB articles need fast keyword search in addition to vector search. The corpus is bilingual; an English-only `tsvector` config silently breaks Arabic queries.

## Decision

* **Database:** PostgreSQL 16, single database, schema-per-tenant where row-level security is insufficient.
* **Extensions enabled at install:** `pg_trgm`, `unaccent`, `btree_gin`, `pgcrypto`, `uuid-ossp`.
* **Full-text search:**
  * English: built-in `english` config.
  * Arabic: custom `arabic_simple` config built from `simple` + `unaccent` + a lemma dictionary derived from CAMeL Tools, materialized via an out-of-band job (since Postgres has no shipped Arabic snowball stemmer).
  * Tickets get **two `tsvector` columns** (`fts_ar`, `fts_en`) populated by trigger; search merges them.
* **Migrations:** Alembic, autogenerate disabled in CI (manual diff required).

## Consequences

* Custom FTS config means migrations include SQL that creates the dictionary on a fresh DB. We ship a verification script that confirms dictionaries are loaded at boot.
* Trigram indexes on `title_ar`, `title_en` give cheap fuzzy "did-you-mean" suggestions.
* Vector search remains in Qdrant; Postgres FTS is the BM25-style sparse leg, fused via RRF in the app layer.
