"""Test fixtures: plot_test database, migrated schema, ASGI client, Redis.

``PLOT_DATABASE_URL`` is pointed at ``plot_test`` at import time so the app
engine (created lazily on first use) targets the test database. The
session-scoped ``migrated_test_db`` fixture creates the database and applies
Alembic migrations once per run.
"""

import os
import subprocess
from pathlib import Path

import httpx
import pytest
import pytest_asyncio
from redis.asyncio import Redis

TEST_DB_NAME = "plot_test"
TEST_DATABASE_URL = f"postgresql+asyncpg://plot:plot@localhost:5432/{TEST_DB_NAME}"

# Point the app at the test database before any app import.
os.environ["PLOT_DATABASE_URL"] = TEST_DATABASE_URL

PYTHON_DIR = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="session")
def migrated_test_db() -> str:
    """Create ``plot_test`` and apply Alembic migrations (once per session)."""
    subprocess.run(
        ["docker", "exec", "carto-postgres-1", "createdb", "-U", "plot", TEST_DB_NAME],
        check=False,
        capture_output=True,
    )
    env = {**os.environ, "PLOT_DATABASE_URL": TEST_DATABASE_URL}
    subprocess.run(
        ["uv", "run", "alembic", "upgrade", "head"],
        check=True,
        env=env,
        cwd=PYTHON_DIR,
        capture_output=True,
    )
    return TEST_DATABASE_URL


@pytest_asyncio.fixture(autouse=True)
async def _dispose_engine() -> None:
    """Close pooled DB connections after each test.

    The module-level async engine keeps its pool across pytest-asyncio's
    per-test event loops; without disposal the next test reuses connections
    bound to a closed loop ("Event loop is closed").
    """
    yield
    from plot_backend.app.db.session import engine

    await engine.dispose()


@pytest_asyncio.fixture
async def redis_client() -> Redis:
    """Fresh, flushed Redis client — injectable via dependency override."""
    client = Redis.from_url("redis://localhost:6379/0", decode_responses=True)
    await client.flushdb()
    yield client
    await client.flushdb()
    await client.aclose()


@pytest_asyncio.fixture
async def client(migrated_test_db: str, redis_client: Redis):
    """httpx ASGI client against ``plot_test`` with rate limiting on fresh Redis."""
    from plot_backend.app.auth.rate_limit import get_redis
    from plot_backend.app.main import create_app

    app = create_app()
    app.dependency_overrides[get_redis] = lambda: redis_client
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as c:
        yield c
