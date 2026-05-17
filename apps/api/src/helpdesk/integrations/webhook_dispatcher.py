"""Outbound webhook dispatcher.

Every payload is signed with HMAC-SHA256 over the JSON body using the
operator-supplied secret. Receivers verify with the same secret.

We retry on 5xx and connection errors with exponential backoff (3 tries
max). 4xx responses are surfaced once; the receiver presumably
misconfigured the endpoint.
"""

from __future__ import annotations

import asyncio
import hmac
import json
from hashlib import sha256
from typing import Any

import httpx
import structlog

logger = structlog.get_logger(__name__)

SIGNATURE_HEADER = "X-Helpdesk-Signature"
EVENT_HEADER = "X-Helpdesk-Event"


def sign(body: bytes, secret: str) -> str:
    return "sha256=" + hmac.new(secret.encode("utf-8"), body, sha256).hexdigest()


async def dispatch(
    *,
    url: str,
    secret: str,
    event: str,
    payload: dict[str, Any],
    extra_headers: dict[str, str] | None = None,
    timeout_seconds: float = 5.0,
    max_attempts: int = 3,
) -> tuple[int, str]:
    """POST `payload` to `url`, signed. Returns (status_code, body_preview)."""
    body = json.dumps(payload, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    headers = {
        "Content-Type": "application/json",
        SIGNATURE_HEADER: sign(body, secret),
        EVENT_HEADER: event,
        **(extra_headers or {}),
    }
    async with httpx.AsyncClient(timeout=timeout_seconds) as client:
        last_exc: Exception | None = None
        for attempt in range(1, max_attempts + 1):
            try:
                response = await client.post(url, content=body, headers=headers)
                if response.status_code < 500:
                    return response.status_code, response.text[:512]
                logger.warning("webhook.5xx", url=url, attempt=attempt, status=response.status_code)
            except httpx.HTTPError as exc:
                last_exc = exc
                logger.warning("webhook.error", url=url, attempt=attempt, error=str(exc))
            await asyncio.sleep(0.5 * 2 ** (attempt - 1))
    raise RuntimeError(f"webhook failed after {max_attempts} attempts: {last_exc}")
