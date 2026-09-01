"""Auth routers: register, verify, login/logout/refresh, forgot/reset, users.

The login endpoint is custom (not ``fastapi_users.get_auth_router``) because
the spec requires distinct error messages for unknown email vs wrong password
(27.7) and a 403 for unverified logins. Refresh tokens are not native to
fastapi-users: a minimal stateless refresh JWT (7 days, rotated on each
refresh) is issued alongside the access token — see the PR report for the
trade-off.
"""

from typing import Annotated
from uuid import UUID

import jwt
from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_users import FastAPIUsers, exceptions
from fastapi_users.authentication.strategy import JWTStrategy
from fastapi_users.jwt import decode_jwt, generate_jwt
from fastapi_users.manager import BaseUserManager
from pydantic import BaseModel

from plot_backend.app.auth.dependencies import auth_backend, get_user_manager
from plot_backend.app.auth.rate_limit import login_rate_limit
from plot_backend.app.auth.schemas import UserCreate, UserRead, UserUpdate
from plot_backend.app.config import get_settings
from plot_backend.app.db.models.identity import User

REFRESH_TOKEN_AUDIENCE = "fastapi-users:refresh"

fastapi_users = FastAPIUsers[User, UUID](get_user_manager, [auth_backend])


class RefreshRequest(BaseModel):
    """Payload for ``POST /auth/jwt/refresh``."""

    refresh_token: str


def _issue_refresh_token(user: User) -> str:
    """Issue a stateless refresh JWT (lifetime from settings)."""
    settings = get_settings()
    return generate_jwt(
        {"sub": str(user.id), "aud": REFRESH_TOKEN_AUDIENCE},
        settings.secret_key,
        settings.refresh_token_expire_days * 24 * 3600,
    )


def get_auth_router() -> APIRouter:
    """Build the ``/auth/jwt`` router (login, refresh, logout)."""
    router = APIRouter()

    @router.post(
        "/login",
        name="auth:jwt.login",
        dependencies=[Depends(login_rate_limit)],
    )
    async def login(
        request: Request,
        credentials: Annotated[OAuth2PasswordRequestForm, Depends()],
        user_manager: Annotated[BaseUserManager[User, UUID], Depends(get_user_manager)],
        strategy: Annotated[JWTStrategy[User, UUID], Depends(auth_backend.get_strategy)],
    ) -> dict[str, str]:
        # Distinct messages per 27.7: unknown email vs wrong password.
        try:
            user = await user_manager.get_by_email(credentials.username)
        except exceptions.UserNotExists:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="EMAIL_NOT_FOUND")

        verified, updated_hash = user_manager.password_helper.verify_and_update(
            credentials.password, user.hashed_password
        )
        if not verified:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="INVALID_PASSWORD")
        if updated_hash is not None:
            await user_manager.user_db.update(user, {"hashed_password": updated_hash})

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="LOGIN_BAD_CREDENTIALS"
            )
        if not user.is_verified:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="LOGIN_USER_NOT_VERIFIED"
            )

        access_token = await strategy.write_token(user)
        await user_manager.on_after_login(user, request)
        return {
            "access_token": access_token,
            "refresh_token": _issue_refresh_token(user),
            "token_type": "bearer",
        }

    @router.post("/refresh", name="auth:jwt.refresh")
    async def refresh(
        body: RefreshRequest,
        user_manager: Annotated[BaseUserManager[User, UUID], Depends(get_user_manager)],
        strategy: Annotated[JWTStrategy[User, UUID], Depends(auth_backend.get_strategy)],
    ) -> dict[str, str]:
        settings = get_settings()
        try:
            data = decode_jwt(body.refresh_token, settings.secret_key, [REFRESH_TOKEN_AUDIENCE])
            user = await user_manager.get(user_manager.parse_id(data["sub"]))
        except (jwt.PyJWTError, KeyError, exceptions.UserNotExists, exceptions.InvalidID):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="INVALID_REFRESH_TOKEN"
            )
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="INVALID_REFRESH_TOKEN"
            )
        access_token = await strategy.write_token(user)
        return {
            "access_token": access_token,
            "refresh_token": _issue_refresh_token(user),
            "token_type": "bearer",
        }

    @router.post(
        "/logout",
        name="auth:jwt.logout",
        status_code=status.HTTP_204_NO_CONTENT,
    )
    async def logout(
        user_token: Annotated[
            tuple[User, str],
            Depends(fastapi_users.authenticator.current_user_token(active=True)),
        ],
    ) -> Response:
        # JWT is stateless: logout is a client-side token discard (204).
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    return router


def get_register_router() -> APIRouter:
    """Build the ``/auth/register`` router."""
    return fastapi_users.get_register_router(UserRead, UserCreate)


def get_verify_router() -> APIRouter:
    """Build the ``/auth`` verify router (request-verify-token, verify)."""
    return fastapi_users.get_verify_router(UserRead)


def get_reset_router() -> APIRouter:
    """Build the ``/auth`` reset-password router (forgot-password, reset-password)."""
    return fastapi_users.get_reset_password_router()


def get_users_router() -> APIRouter:
    """Build the ``/users`` router (me, patch-me, superuser admin routes)."""
    return fastapi_users.get_users_router(UserRead, UserUpdate)
