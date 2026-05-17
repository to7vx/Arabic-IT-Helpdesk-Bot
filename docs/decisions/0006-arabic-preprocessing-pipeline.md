# 6. Arabic preprocessing pipeline

* **Status:** Accepted
* **Date:** 2026-05-17

## Context

Arabic text needs normalization (alef forms, ya/alef-maqsura, diacritics, tatweel, Eastern Arabic digits), Arabizi handling, code-switching detection, and morphological analysis for sparse retrieval.

See [research/arabic-tokenizers.md](../research/arabic-tokenizers.md).

## Decision

Preprocessing is a single composable pipeline in `apps/api/src/helpdesk/nlp/preprocessing/`:

1. Unicode NFC normalization.
2. Configurable alef / ya normalization (default: on for retrieval, off for storage).
3. Strip tatweel `ـ`; strip diacritics with preserve-option.
4. Eastern Arabic digit fold (`٠-٩` ↔ `0-9`).
5. Emoji handling: strip presentation, preserve semantic (😡, 🚨) as `[NEG]`, `[URGENT]` tokens.
6. Arabizi detection (`bidi.is_arabic` ratio + character n-gram model) → transliterate to Arabic via CAMeL Tools `transliterator` then re-run pipeline.
7. Code-switch segmentation: per-sentence language tag.
8. **Morphology / lemmatization:** **CAMeL Tools** (Disambiguator + MorphologyDB). Farasa available behind `--fast` flag for batch jobs.

Transformer inputs use the model's own tokenizer; preprocessing runs upstream only for sparse retrieval and rule-based features.

## Consequences

* CAMeL Tools is heavy at first load (~600 MB). We lazy-load inside the worker process and pin the singleton.
* Original raw text is preserved (we never replace it); normalized text lives in `tickets.normalized_text`.
* Every transformation is reversible or auditable; preprocessing config is serialized into `ai_suggestions.preprocessing_version` so we can re-run evals on historical data.
