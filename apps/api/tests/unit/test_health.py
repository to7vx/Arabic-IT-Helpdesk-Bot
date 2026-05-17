"""Smoke test that healthz returns 200 even with no infra running."""

from __future__ import annotations


async def test_healthz(client):  # type: ignore[no-untyped-def]
    response = await client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


async def test_openapi_present(client):  # type: ignore[no-untyped-def]
    response = await client.get("/openapi.json")
    assert response.status_code == 200
    schema = response.json()
    # Sanity: every router we registered shows up in the spec.
    paths = schema["paths"].keys()
    assert any(p.startswith("/api/v1/auth") for p in paths)
    assert any(p.startswith("/api/v1/tickets") for p in paths)
    assert any(p.startswith("/api/v1/kb") for p in paths)
    assert any(p.startswith("/api/v1/ai") for p in paths)
