"""Celery application.

Discovers tasks under ``helpdesk.workers.tasks.*``. Beat schedule reads
from a DB-backed scheduler so admins can edit cadence at runtime once
the schedule editor lands in Phase 7b.
"""

from __future__ import annotations

from celery import Celery

from helpdesk.config import get_settings

settings = get_settings()

app = Celery(
    "helpdesk",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
    include=[
        "helpdesk.workers.tasks.email_ingest",
        "helpdesk.workers.tasks.webhook_dispatch",
        "helpdesk.workers.tasks.embedding",
    ],
)

app.conf.update(
    task_default_queue="default",
    task_track_started=True,
    task_time_limit=600,
    task_soft_time_limit=540,
    worker_prefetch_multiplier=1,
    timezone="UTC",
)

app.conf.beat_schedule = {
    "email-ingest-every-2-min": {
        "task": "helpdesk.workers.tasks.email_ingest.poll_inbox",
        "schedule": 120.0,
    },
}
