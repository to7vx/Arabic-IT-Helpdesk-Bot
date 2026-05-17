"""Test fixtures.

We split tests into two flavors:

* ``unit`` — fully in-process, no containers. SQLAlchemy talks to an
  in-memory SQLite where compatible (most model code works); tests that
  exercise Postgres-only features are marked ``integration``.
* ``integration`` — uses testcontainers to spin up Postgres and Redis.

This file wires both modes.
"""

from __future__ import annotations

import asyncio
import os
from collections.abc import AsyncIterator, Iterator
from typing import Any

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from helpdesk.db.base import Base


# ---------------------------------------------------------------------------
# Event loop
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session")
def event_loop() -> Iterator[asyncio.AbstractEventLoop]:
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


# ---------------------------------------------------------------------------
# SQLite in-memory engine for unit tests
# ---------------------------------------------------------------------------

@pytest_asyncio.fixture(scope="function")
async def db_engine() -> AsyncIterator[Any]:
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def db_session(db_engine: Any) -> AsyncIterator[AsyncSession]:
    sm = async_sessionmaker(bind=db_engine, expire_on_commit=False)
    async with sm() as session:
        yield session


# ---------------------------------------------------------------------------
# Test app
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session")
def app() -> Any:
    os.environ.setdefault("DATABASE_URL", "sqlite+aiosqlite:///:memory:")
    os.environ.setdefault("LLM_PROVIDER", "disabled")
    os.environ.setdefault("APP_ENV", "development")
    from helpdesk.main import create_app

    return create_app()


@pytest_asyncio.fixture(scope="function")
async def client(app: Any) -> AsyncIterator[AsyncClient]:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c
