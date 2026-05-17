"""WhatsApp Business inbound webhook.

PDPL note: enabling this integration triggers cross-border transfers to
Meta. Operators must consent via the admin UI and the transfer is
logged in cross_border_transfers.
"""

from __future__ import annotations


async def handle_webhook(payload: dict[str, object]) -> dict[str, object]:
    return {"received": True, "note": "WhatsApp ingestion wires in Phase 6b."}
