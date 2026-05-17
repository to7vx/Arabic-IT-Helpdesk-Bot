"""Slack slash-command + signature-verification handler.

POST /api/v1/integrations/slack/command receives Slack slash commands;
this module verifies the signature (X-Slack-Signature) and routes to
the right handler. Currently supports /ticket new.
"""

from __future__ import annotations

import hashlib
import hmac
import time
from typing import Any

import structlog

from helpdesk.config import get_settings

logger = structlog.get_logger(__name__)


def verify_signature(*, body: bytes, timestamp: str, signature: str) -> bool:
    secret = get_settings().slack_signing_secret.get_secret_value()
    if not secret:
        return False
    try:
        if abs(time.time() - int(timestamp)) > 60 * 5:
            return False
    except (TypeError, ValueError):
        return False
    base = f"v0:{timestamp}:".encode() + body
    expected = "v0=" + hmac.new(secret.encode(), base, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)


async def handle_slash_command(form: dict[str, str]) -> dict[str, Any]:
    cmd = form.get("command", "")
    text = form.get("text", "").strip()
    user_id = form.get("user_id", "")
    if cmd == "/ticket" and text.startswith("new "):
        subject = text[4:].strip() or "(no subject)"
        # Real implementation calls ticket_service. Kept thin here so the
        # full Slack handler lives alongside its tests in Phase 6b.
        logger.info("slack.ticket_new", user=user_id, subject=subject)
        return {
            "response_type": "ephemeral",
            "text": f"Ticket queued: *{subject}* (creation wires to ticket_service in 6b).",
        }
    return {"response_type": "ephemeral", "text": "Try: `/ticket new <subject>`"}
