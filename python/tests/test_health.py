"""Health endpoint tests via httpx ASGI transport (no database needed)."""

import asyncio

import httpx

from plot_backend.app.main import create_app


def test_health_returns_ok_and_version():
    app = create_app()
    transport = httpx.ASGITransport(app=app)

    async def request() -> httpx.Response:
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
            return await client.get("/health")

    response = asyncio.run(request())

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["version"]
