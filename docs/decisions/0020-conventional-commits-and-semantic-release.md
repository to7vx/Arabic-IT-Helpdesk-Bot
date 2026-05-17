# 20. Conventional Commits and semantic-release

* **Status:** Accepted
* **Date:** 2026-05-17

## Context

We want a maintained CHANGELOG, predictable versioning, and zero "what version is this?" ambiguity on a public project that issues frequent patches.

## Decision

* **Commit style:** [Conventional Commits 1.0](https://www.conventionalcommits.org/).
* **Branch model:** trunk-based on `main`; feature branches → PR → squash merge with a conventional title.
* **Release automation:** `semantic-release` runs on every merge to `main`:
  * Determines next version from commit types (`feat` → minor, `fix` → patch, `feat!` / `BREAKING CHANGE:` → major).
  * Generates GitHub Release + tags.
  * Updates `CHANGELOG.md`.
  * Triggers Docker image publish and Helm chart push.
* **Enforcement:** `commitlint` pre-commit + PR title lint in CI.

## Consequences

* Contributors must learn ~7 commit prefixes — `CONTRIBUTING.md` shows examples.
* CHANGELOG is generated, not hand-written; humans only edit the "Migration notes" subsection.
* No pre-release flag in v0.x — once tagged, version goes only forward.
