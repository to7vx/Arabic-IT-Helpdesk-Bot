"""WebSocket routes. Registered on the FastAPI app from main.py."""

from __future__ import annotations

from fastapi import FastAPI

from helpdesk.api.ws import tickets


def register_websocket_routes(app: FastAPI) -> None:
    app.include_router(tickets.router)
