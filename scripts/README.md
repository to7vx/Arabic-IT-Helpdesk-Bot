# `scripts/`

Project-wide scripts that don't belong inside a single app.

| Script | Purpose | Lands in |
|---|---|---|
| `setup.sh` | Bootstrap a fresh dev machine | Phase 1 |
| `seed_db.py` | Seed users, teams, categories, sample tickets | Phase 2 |
| `seed_kb.py` | Seed bilingual KB articles | Phase 2 |
| `train_classifier.py` | Train category / priority / sentiment / urgency classifiers | Phase 4 |
| `run_evals.sh` | Wrapper around `helpdesk.nlp.evals.run_eval` | Phase 4 |
| `load_test.sh` | k6 load test against a running stack | Phase 11 |
| `backup.sh` | pg_dump + qdrant snapshot + minio mirror | Phase 7 |
| `check_messages.py` | Verify ar/en translation key parity | Phase 5 |

> **Status:** README only in Phase 1. Scripts land in their respective phases.
