"""NLP evaluation runner.

Usage:
    uv run python -m helpdesk.nlp.evals.run_eval [--enforce-thresholds]

Reads ``data/golden-tickets/*.jsonl``, runs each classifier, prints a
report, and (when ``--enforce-thresholds`` is given) exits non-zero
on regression.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
import time
from pathlib import Path
from typing import Any

import yaml

from helpdesk.nlp.classification.category import classify_text
from helpdesk.nlp.classification.urgency import score_urgency
from helpdesk.nlp.evals.metrics import macro_f1, precision_recall_f1

REPO_ROOT = Path(__file__).resolve().parents[5]
GOLDEN_DIR = REPO_ROOT / "data" / "golden-tickets"
THRESHOLDS = Path(__file__).parent / "thresholds.yml"


def _load_golden() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if not GOLDEN_DIR.exists():
        return rows
    for path in GOLDEN_DIR.glob("*.jsonl"):
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            rows.append(json.loads(line))
    return rows


async def run() -> dict[str, Any]:
    golden = _load_golden()
    if not golden:
        print(f"No golden set under {GOLDEN_DIR}; skipping.")
        return {"n": 0}

    cat_true: list[str] = []
    cat_pred: list[str] = []
    urg_true: list[int] = []
    urg_pred: list[int] = []

    t0 = time.perf_counter()
    for row in golden:
        text = row["text"]
        # Category — top-1 prediction
        top = await classify_text(text, top_k=1)
        pred = top[0]["category_slug"] if top else "other"
        cat_true.append(row.get("category", "other"))
        cat_pred.append(pred)
        # Urgency
        urgency = await score_urgency(text)
        urg_true.append(int(row.get("urgent", False)))
        urg_pred.append(int(urgency["requires_escalation"]))
    duration_ms = (time.perf_counter() - t0) * 1000.0

    cat_macro_f1 = macro_f1(cat_true, cat_pred)
    urg_p, urg_r, urg_f1 = precision_recall_f1(
        [str(x) for x in urg_true], [str(x) for x in urg_pred]
    )

    report = {
        "n": len(golden),
        "duration_ms": round(duration_ms, 2),
        "classification_macro_f1": round(cat_macro_f1, 3),
        "urgency_precision": round(urg_p, 3),
        "urgency_recall": round(urg_r, 3),
        "urgency_f1": round(urg_f1, 3),
    }
    return report


def _check_thresholds(report: dict[str, Any]) -> list[str]:
    if not THRESHOLDS.exists():
        return []
    cfg = yaml.safe_load(THRESHOLDS.read_text(encoding="utf-8"))
    failures: list[str] = []
    cf1 = report.get("classification_macro_f1", 0.0)
    if cf1 < cfg["classification"]["macro_f1_min"]:
        failures.append(
            f"classification.macro_f1 {cf1} < {cfg['classification']['macro_f1_min']}"
        )
    urec = report.get("urgency_recall", 0.0)
    if urec < cfg["urgency"]["recall_min"]:
        failures.append(f"urgency.recall {urec} < {cfg['urgency']['recall_min']}")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--enforce-thresholds", action="store_true")
    args = parser.parse_args()
    report = asyncio.run(run())
    print(json.dumps(report, indent=2, ensure_ascii=False))
    if args.enforce_thresholds:
        failures = _check_thresholds(report)
        if failures:
            print("\nThreshold failures:", file=sys.stderr)
            for f in failures:
                print(f"  - {f}", file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
