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
        self._dev_mail_sink("password reset", user, token)

    async def on_after_request_verify(
        self, user: User, token: str, request: Request | None = None
    ) -> None:
        self._dev_mail_sink("email verification", user, token)

    def _dev_mail_sink(self, action: str, user: User, token: str) -> None:
        """Log the token while no mail provider is configured (dev sink).

        Postmark delivery arrives in wave-07; once ``PLOT_POSTMARK_API_KEY``
        is set the token is no longer written to logs.
        """
        if get_settings().postmark_api_key is None:
            logger.warning("DEV MAIL SINK — %s token for %s: %s", action, user.email, token)
        else:
            logger.info("%s requested for %s (delivery: wave-07)", action, user.email)

    async def on_after_login(
        self, user: User, request: Request | None = None, response=None
    ) -> None:
        logger.info("User %s logged in", user.id)
