# 19. NLP evaluation methodology

* **Status:** Accepted
* **Date:** 2026-05-17

## Context

NLP changes silently regress in ways unit tests don't catch. Without a real golden set, "F1 = 0.85" is an aspiration not a fact.

## Decision

* **Golden set:** ≥ 500 manually labeled Arabic tickets covering MSA, Gulf/Saudi, Egyptian, Levantine, Arabizi, code-switch. Stored in `data/golden-tickets/` as JSONL with labels: category, priority, sentiment, urgency, entities, suggested_kb_ids.
* **Labeling provenance:** every item annotates `labeler_id`, `labeled_at`, `dialect`. Two annotators per item where possible; disagreements resolved by a third.
* **Metrics tracked per run:**
  * Macro and per-category F1 for category classifier.
  * Macro F1 for sentiment + urgency.
  * MRR@10 and Recall@5 for KB retrieval.
  * Median + p95 inference latency per stage.
  * Hallucination rate on generated drafts (LLM-judge w/ Claude, then human spot-check).
* **CI gate:** PRs that change `nlp/` must run `scripts/run_evals.sh`; thresholds in `nlp/evals/thresholds.yml` enforced; regressions fail the build.
* **Public dashboard:** results published to GitHub Pages on every merge to `main`.
* **Adversarial set:** small (~50 items) of typos, sarcasm, mixed dialect, intentionally ambiguous tickets; metric is "does the model say 'low confidence' rather than guess wrong?"

## Consequences

* Golden-set maintenance is a continuous cost; we onboard labelers via `docs/guides/labeling-guidelines.md`.
* CI for NLP PRs takes ~5 minutes longer — accepted price.
* Shipping the golden set in the repo requires anonymization (every name/email/phone synthetic).
