"""Role-based access control with named permissions.

Permissions are explicit strings, not role checks scattered through the code.
A router declares ``require("ticket.assign")`` and the dependency walks the
permission map for the caller's role. This keeps adding a role straightforward
later — only the table below needs to change.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Annotated

from fastapi import Depends, HTTPException, status

from helpdesk.api.v1.deps_auth import CurrentUser, get_current_user

PERMISSIONS: dict[str, set[str]] = {
    "admin": {
        "ticket.read", "ticket.write", "ticket.assign", "ticket.escalate", "ticket.merge", "ticket.delete",
        "kb.read", "kb.write", "kb.publish",
        "user.read", "user.write", "user.invite",
        "team.read", "team.write",
        "category.read", "category.write",
        "sla.read", "sla.write",
        "rule.read", "rule.write",
        "webhook.read", "webhook.write",
        "audit.read",
        "ai.read", "ai.write", "ai.config",
        "admin.compliance",
    },
    "manager": {
        "ticket.read", "ticket.write", "ticket.assign", "ticket.escalate",
        "kb.read", "kb.write",
        "user.read", "team.read", "team.write",
        "category.read", "sla.read",
        "rule.read", "webhook.read",
        "audit.read",
        "ai.read",
    },
    "agent": {
        "ticket.read", "ticket.write", "ticket.assign", "ticket.escalate",
        "kb.read", "kb.write",
        "user.read", "team.read",
        "category.read", "sla.read",
        "ai.read",
    },
    "end_user": {
        "ticket.read.own", "ticket.write.own",
        "kb.read",
    },
}


def require(*needed: str) -> Callable[..., CurrentUser]:
    """FastAPI dependency factory that enforces a permission set."""

    async def _enforce(user: Annotated[CurrentUser, Depends(get_current_user)]) -> CurrentUser:
        granted = PERMISSIONS.get(user.role, set())
        if not set(needed).issubset(granted):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"missing permission: {', '.join(sorted(set(needed) - granted))}",
            )
        return user

    return _enforce
