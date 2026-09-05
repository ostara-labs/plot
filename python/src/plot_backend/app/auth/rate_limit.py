"""Login rate limiting (spec 27.8) with fail-open on Redis errors (27.14).

Two sliding counters per attempt — one keyed by the SHA-256 of the email
(PII-safe), one by the client IP — each capped at 5 attempts per 15 minutes.
If Redis is unreachable the request is allowed through with a warning log:
a Redis outage must never turn into a 500.
"""

import hashlib
import logging
from typing import Annotated

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from redis.asyncio import Redis
from redis.exceptions import RedisError

from plot_backend.app.config import get_settings

logger = logging.getLogger(__name__)

RATE_LIMIT_WINDOW_SECONDS = 15 * 60
RATE_LIMIT_MAX_ATTEMPTS = 5

_redis: Redis | None = None


def get_redis() -> Redis:
    """Return the shared async Redis client (dependency-overridable in tests)."""
    global _redis
    if _redis is None:
        _redis = Redis.from_url(get_settings().redis_url, decode_responses=True)
    return _redis


def _email_key(email: str) -> str:
    """Hash the email so raw PII never lands in Redis keys (27.8)."""
    digest = hashlib.sha256(email.encode("utf-8")).hexdigest()
    return f"rl:login:{digest}"


def _ip_key(ip: str) -> str:
    return f"rl:login:{ip}"


async def _attempt_allowed(redis: Redis, key: str) -> bool:
    """Atomic INCR + EXPIRE(NX); True while the counter is within the cap.

    The pipeline makes the counter and its TTL one atomic operation: with a
    separate ``expire`` a failure between the two would leave a key without
    TTL that no later attempt re-expires — a permanent block.
    """
    async with redis.pipeline(transaction=True) as pipe:
        pipe.incr(key)
        pipe.expire(key, RATE_LIMIT_WINDOW_SECONDS, nx=True)
        count, _ = await pipe.execute()
    return int(count) <= RATE_LIMIT_MAX_ATTEMPTS


async def login_rate_limit(
    request: Request,
    credentials: Annotated[OAuth2PasswordRequestForm, Depends()],
    redis: Annotated[Redis, Depends(get_redis)],
) -> None:
    """Reject login attempts beyond 5/15min per email and per IP (429).

    NOTE (deployment): behind a reverse proxy, run uvicorn with
    ``--proxy-headers --forwarded-allow-ips="<proxy>"`` so
    ``request.client.host`` is the real client IP — otherwise every user
    behind the proxy shares one IP counter. Never trust forwarded headers
    from untrusted clients.
    """
    ip = request.client.host if request.client is not None else "unknown"
    for key in (_email_key(credentials.username), _ip_key(ip)):
        try:
            allowed = await _attempt_allowed(redis, key)
        except (RedisError, OSError, TimeoutError):
            logger.warning("Redis unavailable for login rate limiting; allowing attempt")
            return
        if not allowed:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="TOO_MANY_ATTEMPTS",
            )
