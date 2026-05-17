"""FastAPI dependency providers used across routers."""

from __future__ import annotations

from collections.abc import AsyncIterator
from typing import Annotated

from fastapi import Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession

from helpdesk.config import Settings, get_settings
from helpdesk.db.session import get_session


async def session_dep() -> AsyncIterator[AsyncSession]:
    async for session in get_session():
        yield session


SessionDep = Annotated[AsyncSession, Depends(session_dep)]
SettingsDep = Annotated[Settings, Depends(get_settings)]
IdempotencyKey = Annotated[str | None, Header(alias="Idempotency-Key")]
