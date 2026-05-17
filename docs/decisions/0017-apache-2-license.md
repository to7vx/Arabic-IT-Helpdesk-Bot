# 17. Apache 2.0 license

* **Status:** Accepted
* **Date:** 2026-05-17

## Context

We want broad commercial adoption (system integrators, government contractors), explicit patent grants, and freedom to fork — without surprising contributors who expect "open source means I can put it in my product."

## Decision

* **License:** Apache License 2.0.
* **NOTICE file** lists third-party attributions (CAMeL Tools, Farasa, MARBERT, BGE-M3, Jais).
* **CLA:** none. We accept inbound contributions under the inbound-equals-outbound rule.
* **SPDX headers** in every source file: `SPDX-License-Identifier: Apache-2.0`.

## Alternatives considered

* **AGPL** — would limit commercial integrations; not in the spirit of regional-market goals.
* **BSL** — fashionable but excludes the very system-integrator audience we want.

## Consequences

* Anyone can fork and commercialize; we get adoption breadth.
* Patent grant protects contributors and users symmetrically.
* Linting check fails PRs that add files without an SPDX header (config in `.pre-commit-config.yaml`).
