"""Smoke tests for the v0 category + urgency classifiers against the seed golden set."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from helpdesk.nlp.classification.category import classify_text
from helpdesk.nlp.classification.urgency import score_urgency

GOLDEN = Path(__file__).resolve().parents[3] / "data" / "golden-tickets" / "v0_seed.jsonl"


def _load() -> list[dict[str, object]]:
    if not GOLDEN.exists():
        return []
    return [json.loads(line) for line in GOLDEN.read_text(encoding="utf-8").splitlines() if line.strip()]


@pytest.mark.skipif(not GOLDEN.exists(), reason="golden set not present in this checkout")
async def test_category_classifier_minimum_accuracy() -> None:
    rows = _load()
    correct = 0
    for row in rows:
        top = await classify_text(str(row["text"]), top_k=1)
        if top and top[0]["category_slug"] == row["category"]:
            correct += 1
    accuracy = correct / max(len(rows), 1)
    # v0 baseline is keyword-driven; we expect >= 60% top-1 on the seed set.
    assert accuracy >= 0.60, f"only {correct}/{len(rows)} correct"


@pytest.mark.skipif(not GOLDEN.exists(), reason="golden set not present in this checkout")
async def test_urgency_classifier_catches_explicit_urgent() -> None:
    rows = [r for r in _load() if r.get("urgent")]
    caught = 0
    for row in rows:
        result = await score_urgency(str(row["text"]))
        if result["requires_escalation"]:
            caught += 1
    assert caught / max(len(rows), 1) >= 0.5
