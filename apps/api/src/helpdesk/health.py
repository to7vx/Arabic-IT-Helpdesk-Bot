"""Readiness probe — best-effort checks of every external dependency."""

from __future__ import annotations

from typing import Any

import structlog
from sqlalchemy import text

from helpdesk.db.session import session_scope

logger = structlog.get_logger(__name__)


async def readiness() -> dict[str, Any]:
    """Aggregate readiness across DB, Redis, Qdrant. Best-effort, non-fatal."""
    checks: dict[str, str] = {}

    # Database
    try:
        async with session_scope() as session:
            await session.execute(text("SELECT 1"))
        checks["db"] = "ok"
    except Exception as exc:  # noqa: BLE001
        logger.warning("health.db_failed", error=str(exc))
        checks["db"] = "fail"

    # Redis (lazy import to keep startup quick)
    try:
        from redis.asyncio import Redis

        from helpdesk.config import get_settings
        client = Redis.from_url(get_settings().redis_url)
        await client.ping()
        await client.close()
        checks["redis"] = "ok"
    except Exception as exc:  # noqa: BLE001
        logger.warning("health.redis_failed", error=str(exc))
        checks["redis"] = "fail"

    # Qdrant
    try:
        from qdrant_client import AsyncQdrantClient

        from helpdesk.config import get_settings
        settings = get_settings()
        api_key = settings.qdrant_api_key.get_secret_value() if settings.qdrant_api_key else None
        qdrant = AsyncQdrantClient(url=settings.qdrant_url, api_key=api_key, timeout=2.0)
        await qdrant.get_collections()
        checks["qdrant"] = "ok"
    except Exception as exc:  # noqa: BLE001
        logger.info("health.qdrant_unavailable", error=str(exc))
        checks["qdrant"] = "fail"

    all_ok = all(v == "ok" for v in checks.values())
    return {"status": "ok" if all_ok else "degraded", "checks": checks}
