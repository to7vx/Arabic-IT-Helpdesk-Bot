"""API v1 — versioned at the URL so breaking changes get a new prefix."""

from fastapi import APIRouter

from helpdesk.api.v1 import admin, ai, auth, dsr, kb, tickets, users, webhooks

router = APIRouter()
router.include_router(auth.router, prefix="/auth", tags=["auth"])
router.include_router(users.router, prefix="/users", tags=["users"])
router.include_router(tickets.router, prefix="/tickets", tags=["tickets"])
router.include_router(kb.router, prefix="/kb", tags=["kb"])
router.include_router(ai.router, prefix="/ai", tags=["ai"])
router.include_router(admin.router, prefix="/admin", tags=["admin"])
router.include_router(webhooks.router, prefix="/webhooks", tags=["webhooks"])
router.include_router(dsr.router, prefix="/dsr", tags=["pdpl"])
