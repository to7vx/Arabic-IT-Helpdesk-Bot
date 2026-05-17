"""Arabic text normalization.

Implements the rules from [ADR-0006](../../../../../docs/decisions/0006-arabic-preprocessing-pipeline.md):

* Unicode NFC.
* Strip tatweel (kashida) ``ـ``.
* Optional alef-form folding (``إ أ آ`` → ``ا``).
* Optional ya / alef-maqsura folding (``ى`` → ``ي``).
* Optional diacritic stripping (tashkeel).
* Eastern-Arabic digit folding (``٠-٩`` ↔ ``0-9``).
* Emoji handling: keep semantic emojis as marker tokens, drop the rest.

Pure-Python, no heavy deps — safe to use everywhere.
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass

TATWEEL = "ـ"  # ـ
DIACRITICS = re.compile(r"[ً-ْٰۖ-ۭ]")
ALEF_FORMS = str.maketrans({"إ": "ا", "أ": "ا", "آ": "ا"})
YA_FORMS = str.maketrans({"ى": "ي"})

EASTERN_DIGITS = str.maketrans({chr(0x0660 + i): str(i) for i in range(10)})
PERSIAN_DIGITS = str.maketrans({chr(0x06F0 + i): str(i) for i in range(10)})

SEMANTIC_EMOJI: dict[str, str] = {
    "🚨": "[URGENT]",
    "⚠": "[WARNING]",
    "⚠️": "[WARNING]",
    "😡": "[NEG]",
    "😠": "[NEG]",
    "😤": "[NEG]",
    "🔥": "[CRITICAL]",
    "💥": "[CRITICAL]",
    "🆘": "[URGENT]",
    "❗": "[URGENT]",
    "‼": "[URGENT]",
}

# Pre-compiled regex to find any single emoji codepoint we want to drop.
_EMOJI_RANGES = re.compile(
    "[\U0001F300-\U0001FAFF☀-➿\U0001F900-\U0001F9FF\U0001F600-\U0001F64F]"
)


@dataclass(frozen=True, slots=True)
class NormalizationOptions:
    fold_alef: bool = True
    fold_ya: bool = True
    strip_diacritics: bool = True
    strip_tatweel: bool = True
    fold_digits: bool = True
    semantic_emoji: bool = True


DEFAULT_OPTS = NormalizationOptions()


def normalize(text: str, options: NormalizationOptions = DEFAULT_OPTS) -> str:
    """Return a normalized copy of ``text`` per ``options``.

    The original text is never mutated; callers should keep raw text for
    storage and use normalized text only for retrieval and feature
    extraction.
    """
    if not text:
        return text
    out = unicodedata.normalize("NFC", text)

    if options.semantic_emoji:
        for emo, marker in SEMANTIC_EMOJI.items():
            out = out.replace(emo, f" {marker} ")
    out = _EMOJI_RANGES.sub(" ", out)

    if options.strip_tatweel:
        out = out.replace(TATWEEL, "")
    if options.strip_diacritics:
        out = DIACRITICS.sub("", out)
    if options.fold_alef:
        out = out.translate(ALEF_FORMS)
    if options.fold_ya:
        out = out.translate(YA_FORMS)
    if options.fold_digits:
        out = out.translate(EASTERN_DIGITS).translate(PERSIAN_DIGITS)

    return re.sub(r"\s+", " ", out).strip()
