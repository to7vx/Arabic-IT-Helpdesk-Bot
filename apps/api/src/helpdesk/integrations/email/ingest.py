"""IMAP poller that converts unseen messages into tickets.

Runs as a Celery beat task. Each message becomes a ticket via the same
ticket_service so the rest of the system (NLP enqueue, audit log,
events) behaves identically to web-created tickets.
"""

from __future__ import annotations

from dataclasses import dataclass

import structlog
from sqlalchemy import select

from helpdesk.config import get_settings
from helpdesk.db import models
from helpdesk.db.session import session_scope
from helpdesk.services import ticket_service

logger = structlog.get_logger(__name__)


@dataclass(slots=True)
class IngestedMessage:
    sender: str
    subject: str
    body: str
    message_id: str


async def poll_once(limit: int = 50) -> int:
    """Fetch unseen messages, create tickets, return count."""
    settings = get_settings()
    if not settings.email_ingest_enabled or not settings.imap_host:
        return 0
    try:
        from imap_tools import MailBox, A
    except ImportError:
        logger.warning("email.ingest.imap_tools_missing")
        return 0

    created = 0
    with MailBox(settings.imap_host).login(
        settings.imap_user, settings.imap_password.get_secret_value()
    ) as mailbox:
        for msg in mailbox.fetch(A(seen=False), limit=limit, mark_seen=True):
            await _convert_to_ticket(
                IngestedMessage(
                    sender=msg.from_,
                    subject=msg.subject or "(no subject)",
                    body=(msg.text or msg.html or "").strip(),
                    message_id=msg.uid or "",
                )
            )
            created += 1
    return created


async def _convert_to_ticket(msg: IngestedMessage) -> None:
    async with session_scope() as session:
        org = await session.scalar(
            select(models.Organization).where(models.Organization.slug == "default")
        )
        if org is None:
            logger.warning("email.ingest.no_org")
            return
        requester = await session.scalar(
            select(models.User).where(models.User.email == msg.sender)
        )
        if requester is None:
            requester = models.User(org_id=org.id, email=msg.sender, role="end_user")
            session.add(requester)
            await session.flush()
        await ticket_service.create_ticket(
            session,
            org_id=org.id,
            requester_id=requester.id,
            title=msg.subject,
            description=msg.body,
            source="email",
        )
