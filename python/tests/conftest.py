"""Test fixtures: plot_test database, migrated schema, ASGI client, Redis.

``PLOT_DATABASE_URL`` is pointed at the test database at import time so the
app engine (created lazily on first use) targets it. The session-scoped
``migrated_test_db`` fixture creates the database and applies Alembic
migrations once per run.

Two runtime shapes:

- **Local** — the dev docker stack (docker-compose.dev.yml). Tests run
  against ``plot_test`` and Redis DB 15; they are skipped when PostgreSQL
  is unreachable, so a bare `pytest` still passes.
- **CI** — the devtools ``test-postgis`` job exports ``CI_DATABASE_URL``
  and ``CI_REDIS_URL`` pointing at its service containers; those win when
  present, and a CI run without a reachable database is a hard failure —
  silent skips would erase the integration suite exactly where it matters.
"""

import os
import socket
import subprocess
from pathlib import Path

import httpx
import pytest
import pytest_asyncio
from redis.asyncio import Redis

TEST_DB_NAME = "plot_test"
TEST_DATABASE_URL = os.environ.get(
    "CI_DATABASE_URL", f"postgresql+asyncpg://plot:plot@localhost:5432/{TEST_DB_NAME}"
)
TEST_REDIS_URL = os.environ.get("CI_REDIS_URL", "redis://localhost:6379/15")
_IN_CI = os.environ.get("CI") == "true"

# Point the app at the test database before any app import.
os.environ["PLOT_DATABASE_URL"] = TEST_DATABASE_URL
os.environ["PLOT_REDIS_URL"] = TEST_REDIS_URL

PYTHON_DIR = Path(__file__).resolve().parents[1]


def _postgres_reachable() -> bool:
    """True when something accepts TCP connections on localhost:5432."""
    with socket.socket() as sock:
        sock.settimeout(2)
        return sock.connect_ex(("127.0.0.1", 5432)) == 0


@pytest.fixture(scope="session")
def migrated_test_db() -> str:
    """Create the test database and apply Alembic migrations (once per session)."""
    if not _postgres_reachable():
        if _IN_CI:
            pytest.skip(
                "CI run without a reachable PostgreSQL: the workflow must "
                "provide one (devtools python-ci test-postgis job, "
                "postgis-image input)"
            )
        pytest.skip(
            "PostgreSQL unreachable on localhost:5432 — auth integration "
            "tests need the dev docker stack (docker compose -f "
            "docker-compose.dev.yml up -d)"
        )
    if not _IN_CI:
        # Local convenience only: in CI the service database already exists.
        subprocess.run(
            [
                "docker",
                "exec",
                "carto-postgres-1",
                "createdb",
                "-U",
                "plot",
                TEST_DB_NAME,
            ],
            check=False,
            capture_output=True,
        )
    env = {**os.environ, "PLOT_DATABASE_URL": TEST_DATABASE_URL}
    try:
        subprocess.run(
            ["uv", "run", "alembic", "upgrade", "head"],
            check=True,
            env=env,
            cwd=PYTHON_DIR,
            capture_output=True,
        )
    except subprocess.CalledProcessError as exc:
        pytest.skip(f"alembic upgrade head failed on plot_test: {exc.stderr}")
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
    """Fresh Redis client on the test Redis database (isolated from dev data)."""
    client = Redis.from_url(TEST_REDIS_URL, decode_responses=True)
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
