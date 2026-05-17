"""Urgency + sentiment scoring.

v0 baseline uses lexical cues and the preprocessing-injected semantic
emoji markers ([URGENT], [CRITICAL], [NEG]). Returns:

* sentiment_score in [-1, 1]
* urgency_score   in [0, 1]
* requires_escalation: bool gated on urgency_score >= NLP_URGENCY_THRESHOLD
"""

from __future__ import annotations

from helpdesk.config import get_settings
from helpdesk.nlp.preprocessing import normalize

URGENT_TERMS = [
    "urgent", "asap", "immediately", "critical", "emergency", "down",
    "[URGENT]", "[CRITICAL]", "[WARNING]",
    "عاجل", "ضروري", "حالا", "الان", "متعطل", "متوقف", "مشكله كبيره",
]
NEGATIVE_TERMS = [
    "broken", "doesn't work", "can't", "won't", "fail", "crash", "hang",
    "[NEG]",
    "ما يشتغل", "ما تشتغل", "تعطل", "تعطلت", "لا يعمل", "لا تعمل",
    "ما اقدر", "ما استطيع", "ما تقدر",
]
POSITIVE_TERMS = [
    "thanks", "thank you", "great", "appreciate",
    "شكرا", "مشكور", "مشكوره", "ممتاز",
]


async def score_urgency(text: str) -> dict[str, object]:
    norm = normalize(text).lower()
    urgent = sum(1 for term in URGENT_TERMS if term.lower() in norm)
    negative = sum(1 for term in NEGATIVE_TERMS if term.lower() in norm)
    positive = sum(1 for term in POSITIVE_TERMS if term.lower() in norm)

    urgency_score = min(1.0, urgent * 0.30 + negative * 0.10)
    sentiment_score = max(-1.0, min(1.0, (positive - negative) * 0.20))

    threshold = get_settings().nlp_urgency_threshold
    return {
        "urgency_score": round(urgency_score, 3),
        "sentiment_score": round(sentiment_score, 3),
        "requires_escalation": urgency_score >= threshold,
    }
