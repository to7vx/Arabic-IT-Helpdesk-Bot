"""Test the static permission map for sanity."""

from __future__ import annotations

from helpdesk.services.rbac import PERMISSIONS


def test_every_role_has_at_least_one_permission() -> None:
    assert all(PERMISSIONS[role] for role in PERMISSIONS)


def test_admin_is_superset_of_manager() -> None:
    assert PERMISSIONS["manager"].issubset(PERMISSIONS["admin"])


def test_manager_is_superset_of_agent() -> None:
    assert PERMISSIONS["agent"].issubset(PERMISSIONS["manager"])


def test_end_user_cannot_write_kb() -> None:
    assert "kb.write" not in PERMISSIONS["end_user"]
    assert "user.write" not in PERMISSIONS["end_user"]
    assert "ticket.assign" not in PERMISSIONS["end_user"]
