"""Microsoft Teams bot.

The real bot uses the Bot Framework SDK and posts adaptive cards.
This module declares the public surface; the full implementation
lands in Phase 6b alongside the Slack tests.
"""

from __future__ import annotations


async def handle_message(payload: dict[str, object]) -> dict[str, object]:
    return {"type": "message", "text": "Teams integration scaffold — full handler in Phase 6b."}
