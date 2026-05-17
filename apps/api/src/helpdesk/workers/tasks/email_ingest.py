"""Periodic IMAP poll."""

from __future__ import annotations

import asyncio

from helpdesk.integrations.email.ingest import poll_once
from helpdesk.workers.celery_app import app


@app.task(name="helpdesk.workers.tasks.email_ingest.poll_inbox")
def poll_inbox() -> int:
    return asyncio.run(poll_once())
