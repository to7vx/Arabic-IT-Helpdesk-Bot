"""ticket_service unit tests against SQLite in-memory."""

from __future__ import annotations

import pytest

from helpdesk.db import models
from helpdesk.middleware.error_handler import ConflictError
from helpdesk.services import ticket_service


@pytest.fixture
async def seed_org_and_user(db_session):  # type: ignore[no-untyped-def]
    org = models.Organization(slug="default", name_en="Default", name_ar="افتراضي")
    db_session.add(org)
    await db_session.flush()
    user = models.User(org_id=org.id, email="u@example.com", role="end_user")
    db_session.add(user)
    await db_session.flush()
    agent = models.User(org_id=org.id, email="a@example.com", role="agent")
    db_session.add(agent)
    await db_session.flush()
    return org, user, agent


async def test_create_ticket_mints_public_id(db_session, seed_org_and_user):  # type: ignore[no-untyped-def]
    org, user, _ = await seed_org_and_user
    t1 = await ticket_service.create_ticket(
        db_session,
        org_id=org.id,
        requester_id=user.id,
        title="VPN issue",
        description="cannot connect",
    )
    t2 = await ticket_service.create_ticket(
        db_session,
        org_id=org.id,
        requester_id=user.id,
        title="Printer issue",
        description="paper jam",
    )
    assert t1.public_id != t2.public_id
    assert t1.public_id.startswith("TKT-")


async def test_assign_logs_event(db_session, seed_org_and_user):  # type: ignore[no-untyped-def]
    org, user, agent = await seed_org_and_user
    ticket = await ticket_service.create_ticket(
        db_session, org_id=org.id, requester_id=user.id, title="x", description="y"
    )
    await ticket_service.assign(
        db_session, ticket_id=ticket.id, assignee_id=agent.id, actor_id=agent.id
    )
    events = list(
        (await db_session.execute(
            __import__("sqlalchemy").select(models.TicketEvent)
            .where(models.TicketEvent.ticket_id == ticket.id)
        )).scalars()
    )
    assert any(e.event_type == "assigned" for e in events)


async def test_change_status_rejects_no_op(db_session, seed_org_and_user):  # type: ignore[no-untyped-def]
    org, user, _ = await seed_org_and_user
    ticket = await ticket_service.create_ticket(
        db_session, org_id=org.id, requester_id=user.id, title="x", description="y"
    )
    with pytest.raises(ConflictError):
        await ticket_service.change_status(
            db_session, ticket_id=ticket.id, new_status=ticket.status, actor_id=user.id
        )
