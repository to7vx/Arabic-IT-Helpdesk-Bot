"""Bilingual ticket-category classifier.

v0 implementation is a rule + keyword scorer over the canonical category
slugs seeded by ``scripts/seed_db.py``. It is intentionally simple so
the system has a credible NLP path the moment you ``make demo`` without
pulling 4 GB of PyTorch weights.

The interface (`classify_text`) returns a list of ``{category_slug,
confidence}`` dicts ordered by descending confidence. A future v1
implementation will train a MARBERT head and swap behind the same
signature — callers stay unchanged.
"""

from __future__ import annotations

from helpdesk.nlp.preprocessing import normalize

# Keyword cues per category slug. Keep ASCII Arabic identical to the
# normalized output of normalize() so matches survive normalization.
CUES: dict[str, list[str]] = {
    "hardware-printer": ["printer", "print", "paper", "toner", "طابعه", "طباعه", "حبر", "ورق"],
    "hardware-laptop":  ["laptop", "battery", "screen", "حاسوب", "محمول", "بطاريه", "شاشه"],
    "hardware-desktop": ["desktop", "pc", "tower", "حاسوب مكتبي", "كومبيوتر"],
    "software-office":  ["office", "word", "excel", "powerpoint", "outlook", "اوفيس", "اكسل", "وورد"],
    "software-os":      ["windows", "update", "bsod", "blue screen", "ويندوز", "تحديث"],
    "network-vpn":      ["vpn", "tunnel", "في بي ان", "في بي إن", "vpn 720", "720"],
    "network-wifi":     ["wifi", "wi-fi", "wireless", "ssid", "واي فاي", "وايرلس"],
    "network-internet": ["internet", "no connection", "down", "انترنت", "اتصال"],
    "account-password": ["password", "reset", "forgot", "كلمه السر", "كلمه المرور", "نسيت"],
    "account-mfa":      ["mfa", "totp", "2fa", "two-factor", "authenticator", "ثنائي"],
    "account-access":   ["access", "permission", "share", "صلاحيه", "صلاحيات", "وصول"],
    "email-outlook":    ["outlook", "ost", "pst", "اوتلوك", "بريد"],
    "email-spam":       ["spam", "phishing", "junk", "تصيد", "مزعج"],
    "security-phishing": ["phishing", "phish", "scam", "تصيد", "احتيال"],
    "security-malware": ["malware", "virus", "trojan", "فيروس", "برمجيات خبيثه"],
    "collab-teams":     ["teams", "تيمز", "مايكروسوفت تيمز"],
    "collab-zoom":      ["zoom", "زووم"],
    "collab-sharepoint": ["sharepoint", "شيربوينت"],
    "erp-sap":          ["sap", "ساب"],
    "erp-oracle":       ["oracle", "اوراكل"],
    "mobile-mdm":       ["mdm", "intune", "enroll", "تسجيل جهاز"],
    "telephony-handset": ["phone", "handset", "ip phone", "سماعه", "هاتف"],
}


async def classify_text(text: str, *, top_k: int = 3) -> list[dict[str, object]]:
    """Score each category against the normalized input text.

    Confidence is the share of cue hits that mapped to this category,
    plus a small length-aware smoothing so that single-token tickets do
    not get 100% confidence.
    """
    if not text or not text.strip():
        return []
    norm = normalize(text).lower()
    raw_scores: dict[str, int] = {}
    for slug, cues in CUES.items():
        hits = sum(1 for cue in cues if cue in norm)
        if hits:
            raw_scores[slug] = hits
    if not raw_scores:
        return [{"category_slug": "other", "confidence": 0.10}]
    total = sum(raw_scores.values()) + 1.0  # smoothing
    scored = [
        {"category_slug": slug, "confidence": round(min(1.0, score / total + 0.05), 3)}
        for slug, score in raw_scores.items()
    ]
    scored.sort(key=lambda d: d["confidence"], reverse=True)  # type: ignore[arg-type]
    return scored[:top_k]
