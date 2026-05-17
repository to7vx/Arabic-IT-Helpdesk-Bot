"""Tiny dependency-free metric helpers used by the eval runner."""

from __future__ import annotations

from collections import Counter
from collections.abc import Iterable


def precision_recall_f1(y_true: list[str], y_pred: list[str]) -> tuple[float, float, float]:
    if not y_true:
        return 0.0, 0.0, 0.0
    tp = sum(1 for t, p in zip(y_true, y_pred, strict=True) if t == p and t)
    fp = sum(1 for t, p in zip(y_true, y_pred, strict=True) if p and t != p)
    fn = sum(1 for t, p in zip(y_true, y_pred, strict=True) if t and t != p)
    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) else 0.0
    return precision, recall, f1


def macro_f1(y_true: list[str], y_pred: list[str]) -> float:
    classes = set(y_true) | set(y_pred)
    f1s: list[float] = []
    for cls in classes:
        per_true = [1 if t == cls else 0 for t in y_true]
        per_pred = [1 if p == cls else 0 for p in y_pred]
        tp = sum(1 for t, p in zip(per_true, per_pred, strict=True) if t == p == 1)
        fp = sum(1 for t, p in zip(per_true, per_pred, strict=True) if t == 0 and p == 1)
        fn = sum(1 for t, p in zip(per_true, per_pred, strict=True) if t == 1 and p == 0)
        if tp + fp == 0 or tp + fn == 0:
            f1s.append(0.0)
            continue
        prec = tp / (tp + fp)
        rec = tp / (tp + fn)
        f1s.append((2 * prec * rec / (prec + rec)) if (prec + rec) else 0.0)
    return sum(f1s) / max(len(f1s), 1)


def mrr_at_k(predictions: list[list[str]], gold: list[str], k: int = 10) -> float:
    """Mean reciprocal rank with truncation at ``k``."""
    if not predictions:
        return 0.0
    ranks: list[float] = []
    for preds, g in zip(predictions, gold, strict=True):
        rank = next((i + 1 for i, p in enumerate(preds[:k]) if p == g), 0)
        ranks.append(1.0 / rank if rank else 0.0)
    return sum(ranks) / len(ranks)


def recall_at_k(predictions: list[list[str]], gold: list[str], k: int = 5) -> float:
    if not predictions:
        return 0.0
    hits = sum(1 for preds, g in zip(predictions, gold, strict=True) if g in preds[:k])
    return hits / len(predictions)


def distribution(items: Iterable[str]) -> dict[str, int]:
    return dict(Counter(items))
