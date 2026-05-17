"""FastAPI application factory.

Run with:
    uv run uvicorn helpdesk.main:app --reload
"""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import Any

import structlog
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import make_asgi_app
from starlette.middleware.gzip import GZipMiddleware

from helpdesk import __version__
from helpdesk.api.v1 import router as api_v1_router
from helpdesk.api.ws import register_websocket_routes
from helpdesk.config import get_settings
from helpdesk.middleware.error_handler import install_error_handlers
from helpdesk.middleware.logging import LoggingMiddleware
from helpdesk.middleware.rate_limit import RateLimitMiddleware
from helpdesk.middleware.request_id import RequestIdMiddleware
from helpdesk.middleware.security_headers import SecurityHeadersMiddleware
from helpdesk.observability.logging import configure_logging
from helpdesk.observability.tracing import configure_tracing

logger = structlog.get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):  # type: ignore[no-untyped-def]
    settings = get_settings()
    configure_logging(settings.log_level, json=settings.is_production)
    configure_tracing(settings)
    logger.info("api.startup", version=__version__, env=settings.app_env.value)
    try:
        yield
    finally:
        logger.info("api.shutdown")


def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title="Arabic IT Helpdesk Bot — API",
        version=__version__,
        description=(
            "Open-source Arabic-language IT helpdesk API. "
            "Every endpoint provides request/response examples in both Arabic and English. "
            "See docs/decisions/ for architecture rationale."
        ),
        openapi_url="/openapi.json",
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan,
        contact={"name": "Arabic IT Helpdesk Bot", "url": "https://arabic-helpdesk.dev"},
        license_info={"name": "Apache-2.0", "url": "https://www.apache.org/licenses/LICENSE-2.0"},
    )

    # Middleware order matters: outermost first.
    app.add_middleware(RequestIdMiddleware)
    app.add_middleware(LoggingMiddleware)
    app.add_middleware(SecurityHeadersMiddleware)
    app.add_middleware(GZipMiddleware, minimum_size=1024)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["X-Request-ID", "X-RateLimit-Remaining"],
    )
    app.add_middleware(RateLimitMiddleware)

    install_error_handlers(app)

    # Health and metrics. Health endpoints intentionally minimal so load
    # balancers can poll cheaply.
    @app.get("/healthz", tags=["meta"], include_in_schema=False)
    async def healthz() -> dict[str, Any]:
        return {"status": "ok"}

    @app.get("/readyz", tags=["meta"], include_in_schema=False)
    async def readyz() -> dict[str, Any]:
        # Real readiness checks (DB/Redis/Qdrant) live in helpdesk.health.
        from helpdesk.health import readiness  # local import to keep startup fast
        return await readiness()

    app.mount("/metrics", make_asgi_app())

    # Routers
    app.include_router(api_v1_router, prefix="/api/v1")
    register_websocket_routes(app)

    return app


app = create_app()
