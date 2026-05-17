"""Tests for the Arabic preprocessing pipeline."""

from __future__ import annotations

from helpdesk.nlp.preprocessing import normalize
from helpdesk.nlp.preprocessing.language_detect import detect


def test_normalize_strips_tatweel() -> None:
    assert "ـ" not in normalize("مرحــبا")


def test_normalize_folds_alef_forms() -> None:
    out = normalize("إنت أنت آن")
    assert "إ" not in out and "أ" not in out and "آ" not in out


def test_normalize_strips_diacritics() -> None:
    assert normalize("مَرْحَبَا") == "مرحبا"


def test_normalize_folds_eastern_digits() -> None:
    assert "1234567890" in normalize("١٢٣٤٥٦٧٨٩٠")


def test_normalize_keeps_semantic_emoji_as_marker() -> None:
    assert "[URGENT]" in normalize("VPN down 🚨 plz fix")


def test_detect_arabic() -> None:
    res = detect("الطابعة لا تعمل")
    assert res.primary == "ar"
    assert not res.is_arabizi


def test_detect_english() -> None:
    res = detect("Printer is not working at all")
    assert res.primary == "en"


def test_detect_arabizi() -> None:
    res = detect("msh 3aref el password")
    assert res.is_arabizi
    assert res.primary == "ar"


def test_detect_mixed() -> None:
    res = detect("الـ VPN ما يشتغل from home")
    assert res.primary in {"mixed", "ar"}
