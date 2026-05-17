"""Character-ratio language and Arabizi detection.

A real implementation calls into fasttext-langdetect or a transformer LID
model; this lightweight heuristic is correct enough for routing and
covers our needs without an extra model dependency. We trade a few
percentage points of accuracy on edge cases for a 100x smaller install.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

ARABIC_BLOCK = re.compile(r"[؀-ۿݐ-ݿࢠ-ࣿﭐ-﷿ﹰ-﻿]")
LATIN_BLOCK = re.compile(r"[A-Za-z]")
DIGITS = re.compile(r"\d")

# Common Arabizi cues: digits standing in for Arabic phonemes.
ARABIZI_DIGIT_CUES = {"3", "5", "7", "8", "9", "2"}
ARABIZI_HINT_WORDS = {
    "msh", "mish", "mafi", "fi", "ana", "anta", "enta", "law", "lazm",
    "ya3ni", "ya'ni", "el", "al", "wa", "bs", "bas", "kde", "keda",
}


@dataclass(frozen=True, slots=True)
class LanguageDetection:
    primary: str  # "ar" | "en" | "mixed" | "unknown"
    is_arabizi: bool
    arabic_ratio: float
    latin_ratio: float
    confidence: float


def detect(text: str) -> LanguageDetection:
    if not text or not text.strip():
        return LanguageDetection("unknown", False, 0.0, 0.0, 0.0)

    total = max(len(text), 1)
    arabic = len(ARABIC_BLOCK.findall(text))
    latin = len(LATIN_BLOCK.findall(text))

    arabic_ratio = arabic / total
    latin_ratio = latin / total

    primary = "unknown"
    if arabic_ratio > 0.4 and latin_ratio < 0.1:
        primary = "ar"
    elif latin_ratio > 0.4 and arabic_ratio < 0.05:
        primary = "en"
    elif arabic_ratio > 0.1 and latin_ratio > 0.1:
        primary = "mixed"
    elif latin_ratio > 0:
        primary = "en"

    # Arabizi heuristic: Latin-dominant + Arabizi digit cues + hint words.
    tokens = re.findall(r"\b[\w'’]+\b", text.lower())
    digit_cue_hits = sum(1 for t in tokens for ch in t if ch in ARABIZI_DIGIT_CUES)
    hint_hits = sum(1 for t in tokens if t in ARABIZI_HINT_WORDS)
    is_arabizi = primary in {"en", "mixed"} and (digit_cue_hits >= 1 or hint_hits >= 2)
    if is_arabizi and primary == "en":
        primary = "ar"  # treat as Arabic for routing purposes

    confidence = abs(arabic_ratio - latin_ratio)
    return LanguageDetection(
        primary=primary,
        is_arabizi=is_arabizi,
        arabic_ratio=arabic_ratio,
        latin_ratio=latin_ratio,
        confidence=round(confidence, 3),
    )
