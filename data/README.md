# `data/`

Seed data and evaluation corpora shipped with the project.

* [`kb-seed/`](kb-seed) — Knowledge-base articles split by language (`ar/`, `en/`). Loaded by `make db-seed`.
* [`golden-tickets/`](golden-tickets) — Labeled ticket JSONL used by the NLP eval suite (see [ADR-0019](../docs/decisions/0019-nlp-evaluation-methodology.md)).
* [`dialects/`](dialects) — Small dialect samples used for tokenizer and language-detection tests.

**Privacy:** every entry must be synthetic or fully anonymized. Real customer text never ships in this directory.
