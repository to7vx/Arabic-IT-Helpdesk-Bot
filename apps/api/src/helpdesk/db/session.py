"""Async SQLAlchemy engine and session factory.

The engine is created lazily so tests can patch :data:`settings` before the
first connection is opened. Tenant context (``app.org_id``) is set per
checkout via a connection-level ``SET LOCAL`` when multi-tenancy is enabled.
"""

from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from functools import lru_cache

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from helpdesk.config import get_settings


@lru_cache(maxsize=1)
def get_engine() -> AsyncEngine:
    settings = get_settings()
    return create_async_engine(
        settings.database_url,
        pool_pre_ping=True,
        pool_size=settings.db_pool_size,
        max_overflow=settings.db_pool_max_overflow,
        echo=settings.db_echo,
    )


@lru_cache(maxsize=1)
def get_sessionmaker() -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(
        bind=get_engine(),
        expire_on_commit=False,
        autoflush=False,
        autocommit=False,
    )


@asynccontextmanager
async def session_scope() -> AsyncIterator[AsyncSession]:
    """Provide a transactional session scope for one-off scripts."""
    session = get_sessionmaker()()
    try:
        yield session
        await session.commit()
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()


async def get_session() -> AsyncIterator[AsyncSession]:
    """FastAPI dependency that yields a session bound to the request."""
    async with session_scope() as session:
        yield session
