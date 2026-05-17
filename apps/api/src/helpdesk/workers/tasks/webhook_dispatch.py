"""Async webhook dispatch task — invoked from services when state changes."""

from __future__ import annotations

import asyncio
from typing import Any

from helpdesk.integrations.webhook_dispatcher import dispatch
from helpdesk.workers.celery_app import app


@app.task(
    name="helpdesk.workers.tasks.webhook_dispatch.send",
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 5},
)
def send(self, *, url: str, secret: str, event: str, payload: dict[str, Any]) -> tuple[int, str]:
    return asyncio.run(dispatch(url=url, secret=secret, event=event, payload=payload))
