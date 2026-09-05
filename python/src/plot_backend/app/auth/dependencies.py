"""FastAPI dependencies: user database adapter, manager, JWT backend.

The installed fastapi-users-db-sqlalchemy 7.x names the adapter
``SQLAlchemyUserDatabase`` (the older ``SQLAlchemyUserAdapter`` alias was
removed upstream).
"""

from collections.abc import AsyncGenerator
from typing import Annotated
from uuid import UUID

from fastapi import Depends
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from plot_backend.app.auth.user_manager import UserManager
from plot_backend.app.config import get_settings
from plot_backend.app.db.models.identity import User
from plot_backend.app.db.session import get_session


async def get_user_db(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> AsyncGenerator[SQLAlchemyUserDatabase[User, UUID], None]:
    """Yield the SQLAlchemy user database adapter bound to the request session."""
    yield SQLAlchemyUserDatabase(session, User)


async def get_user_manager(
    user_db: Annotated[SQLAlchemyUserDatabase[User, UUID], Depends(get_user_db)],
) -> AsyncGenerator[UserManager, None]:
    """Yield a UserManager instance for the request."""
    yield UserManager(user_db)


def get_jwt_strategy() -> JWTStrategy[User, UUID]:
    """Build the stateless JWT strategy from settings."""
    settings = get_settings()
    return JWTStrategy(
        secret=settings.secret_key,
        lifetime_seconds=settings.access_token_expire_minutes * 60,
    )


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=BearerTransport(tokenUrl="auth/jwt/login"),
    get_strategy=get_jwt_strategy,
)
