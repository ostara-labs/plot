"""UserManager: fastapi-users business logic + email hooks.

Email delivery (Postmark) arrives in wave-07; the hooks below are logger
stubs that record the event and the token that would be emailed.
"""

import logging
from uuid import UUID

from fastapi import Request
from fastapi_users import BaseUserManager, UUIDIDMixin

from plot_backend.app.config import get_settings
from plot_backend.app.db.models.identity import User

logger = logging.getLogger(__name__)


class UserManager(UUIDIDMixin, BaseUserManager[User, UUID]):
    """Plot user manager: JWT secrets from settings, email hooks as stubs."""

    reset_password_token_secret = get_settings().secret_key
    verification_token_secret = get_settings().secret_key

    async def on_after_register(self, user: User, request: Request | None = None) -> None:
        logger.info("User %s registered (email=%s)", user.id, user.email)

    async def on_after_forgot_password(
        self, user: User, token: str, request: Request | None = None
    ) -> None:
        logger.info("User %s requested a password reset (token issued)", user.id)

    async def on_after_request_verify(
        self, user: User, token: str, request: Request | None = None
    ) -> None:
        logger.info("User %s requested email verification (token issued)", user.id)

    async def on_after_login(
        self, user: User, request: Request | None = None, response=None
    ) -> None:
        logger.info("User %s logged in", user.id)
