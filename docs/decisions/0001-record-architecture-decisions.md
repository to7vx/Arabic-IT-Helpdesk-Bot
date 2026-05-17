# 1. Record architecture decisions

* **Status:** Accepted
* **Date:** 2026-05-17

## Context

Architecturally significant decisions on this project span Arabic NLP, data residency, infrastructure, and licensing. Decisions that are not written down get re-litigated.

## Decision

We will record every architecturally significant decision in this `docs/decisions/` directory using a short, dated ADR file. New ADRs are added via pull request and reviewed by code owners. Superseded ADRs are kept and annotated.

## Consequences

* New contributors can read `docs/decisions/` and understand "why is it like this?" without asking.
* Pull requests that change architecture must include an ADR (enforced by PR template).
* Slight overhead — judged worth it for a multi-year OSS project.

## References

* Michael Nygard, *Documenting Architecture Decisions*: https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions.html
