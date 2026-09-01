"""Auth flow tests: register/verify/login/me/logout, rate limiting, error messages."""

from uuid import uuid4

import httpx
from fastapi_users.jwt import generate_jwt
from fastapi_users.manager import VERIFY_USER_TOKEN_AUDIENCE
from redis.asyncio import Redis

from plot_backend.app.config import get_settings

PASSWORD = "Str0ngPass!1"


def _unique_email() -> str:
    return f"user{uuid4().hex}@example.com"


async def _register(client: httpx.AsyncClient, email: str) -> str:
    response = await client.post("/auth/register", json={"email": email, "password": PASSWORD})
    assert response.status_code == 201, response.text
    return response.json()["id"]


async def _verify(client: httpx.AsyncClient, user_id: str, email: str) -> None:
    settings = get_settings()
    token = generate_jwt(
        {"sub": user_id, "email": email, "aud": VERIFY_USER_TOKEN_AUDIENCE},
        settings.secret_key,
        3600,
    )
    response = await client.post("/auth/verify", json={"token": token})
    assert response.status_code == 200, response.text


async def test_register_verify_login_me_logout(client: httpx.AsyncClient) -> None:
    email = _unique_email()
    user_id = await _register(client, email)
    await _verify(client, user_id, email)

    login = await client.post("/auth/jwt/login", data={"username": email, "password": PASSWORD})
    assert login.status_code == 200, login.text
    body = login.json()
    assert body["token_type"] == "bearer"
    assert body["access_token"]
    assert body["refresh_token"]
    headers = {"Authorization": f"Bearer {body['access_token']}"}

    me = await client.get("/users/me", headers=headers)
    assert me.status_code == 200
    assert me.json()["email"] == email
    assert me.json()["is_verified"] is True

    logout = await client.post("/auth/jwt/logout", headers=headers)
    assert logout.status_code == 204


async def test_login_rate_limit_returns_429(client: httpx.AsyncClient) -> None:
    email = _unique_email()
    user_id = await _register(client, email)
    await _verify(client, user_id, email)

    for _ in range(5):
        response = await client.post(
            "/auth/jwt/login", data={"username": email, "password": "wrong-password"}
        )
        assert response.status_code == 400, response.text

    sixth = await client.post(
        "/auth/jwt/login", data={"username": email, "password": "wrong-password"}
    )
    assert sixth.status_code == 429
    assert sixth.json()["detail"] == "TOO_MANY_ATTEMPTS"


async def test_login_distinct_errors(client: httpx.AsyncClient) -> None:
    unknown = await client.post(
        "/auth/jwt/login",
        data={"username": "nobody@example.com", "password": PASSWORD},
    )
    assert unknown.status_code == 400
    assert unknown.json()["detail"] == "EMAIL_NOT_FOUND"

    email = _unique_email()
    user_id = await _register(client, email)
    await _verify(client, user_id, email)

    wrong_password = await client.post(
        "/auth/jwt/login", data={"username": email, "password": "wrong-password"}
    )
    assert wrong_password.status_code == 400
    assert wrong_password.json()["detail"] == "INVALID_PASSWORD"


async def test_login_unverified_returns_403(client: httpx.AsyncClient) -> None:
    email = _unique_email()
    await _register(client, email)

    login = await client.post("/auth/jwt/login", data={"username": email, "password": PASSWORD})
    assert login.status_code == 403
    assert login.json()["detail"] == "LOGIN_USER_NOT_VERIFIED"


async def test_login_fail_open_when_redis_down(migrated_test_db: str) -> None:
    """27.14: a Redis outage must never turn login into a 500."""
    from plot_backend.app.auth.rate_limit import get_redis
    from plot_backend.app.main import create_app

    app = create_app()
    app.dependency_overrides[get_redis] = lambda: Redis.from_url(
        "redis://localhost:6399/0", decode_responses=True, socket_connect_timeout=1
    )
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as c:
        email = _unique_email()
        user_id = await _register(c, email)
        await _verify(c, user_id, email)

        login = await c.post("/auth/jwt/login", data={"username": email, "password": PASSWORD})
        assert login.status_code == 200, login.text
