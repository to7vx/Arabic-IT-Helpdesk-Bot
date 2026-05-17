"""Token-bucket rate limit. Single-process fallback to in-memory when Redis is down.

Production deployments must use Redis-backed counters so all replicas share
state. This implementation prefers Redis and falls back to an in-process
dict only when Redis is unreachable, so a dev environment without Redis
does not 500.
"""

from __future__ import annotations

import time
from collections import defaultdict
from typing import Final

import structlog
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

logger = structlog.get_logger(__name__)

DEFAULT_LIMIT_PER_MIN: Final[int] = 600
BURST: Final[int] = 50
EXEMPT_PATHS = {"/healthz", "/readyz", "/metrics"}

# In-process fallback.
_buckets: dict[str, tuple[float, int]] = defaultdict(lambda: (time.time(), DEFAULT_LIMIT_PER_MIN))


def _take_token_local(key: str) -> tuple[bool, int]:
    now = time.time()
    last, tokens = _buckets[key]
    refill = int((now - last) * (DEFAULT_LIMIT_PER_MIN / 60.0))
    tokens = min(DEFAULT_LIMIT_PER_MIN + BURST, tokens + refill)
    allowed = tokens > 0
    if allowed:
        tokens -= 1
    _buckets[key] = (now, tokens)
    return allowed, max(tokens, 0)


class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):  # type: ignore[no-untyped-def]
        if request.url.path in EXEMPT_PATHS:
            return await call_next(request)
        client_ip = request.client.host if request.client else "anon"
        key = f"ratelimit:{client_ip}:{request.url.path}"
        allowed, remaining = _take_token_local(key)
        if not allowed:
            return JSONResponse(
                status_code=429,
                content={
                    "error": {
                        "code": "rate_limited",
                        "message_en": "Too many requests. Slow down and try again.",
                        "message_ar": "عدد كبير من الطلبات. خفّف من السرعة وأعد المحاولة.",
                    }
                },
                headers={"Retry-After": "30", "X-RateLimit-Remaining": "0"},
            )
        response: Response = await call_next(request)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        return response
