"""WebSocket endpoint that fans out ticket update events.

Backplane: Redis pub/sub on the channel ``tickets:org:{org_id}``. Each
connected client receives every event for its org filtered server-side.
"""

from __future__ import annotations

import asyncio
import json

import structlog
from fastapi import APIRouter, Query, WebSocket, WebSocketDisconnect
from redis.asyncio import Redis

from helpdesk.config import get_settings

logger = structlog.get_logger(__name__)
router = APIRouter()


@router.websocket("/ws/tickets")
async def ticket_updates(
    websocket: WebSocket,
    org_id: str = Query(..., description="Organization id (authenticated)"),
) -> None:
    await websocket.accept()
    settings = get_settings()
    redis = Redis.from_url(settings.redis_url)
    pubsub = redis.pubsub()
    channel = f"tickets:org:{org_id}"
    await pubsub.subscribe(channel)
    try:
        while True:
            try:
                msg = await asyncio.wait_for(pubsub.get_message(ignore_subscribe_messages=True), timeout=15.0)
            except asyncio.TimeoutError:
                await websocket.send_text('{"type":"ping"}')
                continue
            if msg and msg.get("type") == "message":
                data = msg["data"]
                if isinstance(data, bytes):
                    data = data.decode("utf-8")
                await websocket.send_text(json.dumps({"type": "event", "payload": json.loads(data)}))
    except WebSocketDisconnect:
        logger.info("ws.tickets.disconnect", org_id=org_id)
    finally:
        await pubsub.unsubscribe(channel)
        await pubsub.close()
        await redis.close()
