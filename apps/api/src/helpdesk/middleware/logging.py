"""Per-request structured log line. Body content is never logged."""

from __future__ import annotations

import time

import structlog
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

logger = structlog.get_logger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):  # type: ignore[no-untyped-def]
        start = time.perf_counter()
        response: Response | None = None
        try:
            response = await call_next(request)
            return response
        finally:
            duration_ms = (time.perf_counter() - start) * 1000.0
            logger.info(
                "http.request",
                method=request.method,
                path=request.url.path,
                status=getattr(response, "status_code", 0),
                duration_ms=round(duration_ms, 2),
                ua=request.headers.get("user-agent", "-"),
                ip=(request.client.host if request.client else "-"),
            )
