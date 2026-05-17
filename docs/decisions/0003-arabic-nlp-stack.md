# 3. Arabic NLP encoder stack

* **Status:** Accepted
* **Date:** 2026-05-17

## Context

We need encoder models for ticket categorization, sentiment, urgency, and NER. Models must handle MSA, Gulf/Saudi dialect, Egyptian and Levantine dialects, plus heavy code-switching with English.

See [research/arabic-nlp-models.md](../research/arabic-nlp-models.md).

## Decision

* **Primary encoder for ticket text (dialect-heavy):** `UBC-NLP/MARBERT`.
* **Secondary encoder for KB articles (MSA-heavy):** `CAMeL-Lab/bert-base-arabic-camelbert-msa`.
* **Inference format:** distill + quantize to **ONNX INT8** for production. Source PyTorch checkpoints retained for retraining.
* **Routing:** language/dialect detector picks the model; below a confidence threshold we run both and ensemble by max-prob.

## Consequences

* Two model files in the container (~200 MB combined post-quantization).
* Training scripts must produce both ONNX exports; CI smoke-runs both heads on a 50-example sanity set.
* If a future Arabic encoder clearly dominates both, we revisit — but architecture is model-agnostic via `nlp/classification/` interface.
