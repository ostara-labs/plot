"""FastAPI application entrypoint."""

from fastapi import FastAPI, HTTPException
from sqlalchemy import text

from plot_backend import __version__
from plot_backend.app.auth.router import (
    get_auth_router,
    get_register_router,
    get_reset_router,
    get_users_router,
    get_verify_router,
)
from plot_backend.app.config import DEV_SECRET_KEY, get_settings
from plot_backend.app.db.session import engine


def create_app() -> FastAPI:
    """Build the FastAPI application.

    Raises ``RuntimeError`` at startup if a non-debug deployment still uses
    the source-controlled development signing secret (fail-fast, ZDD).
    """
    settings = get_settings()
    if not settings.debug and settings.secret_key == DEV_SECRET_KEY:
        raise RuntimeError(
            "PLOT_SECRET_KEY must be set to a deployment-specific secret when PLOT_DEBUG is false"
        )
    app = FastAPI(title="Plot API", version=__version__)

    app.include_router(get_register_router(), prefix="/auth", tags=["auth"])
    app.include_router(get_verify_router(), prefix="/auth", tags=["auth"])
    app.include_router(get_auth_router(), prefix="/auth/jwt", tags=["auth"])
    app.include_router(get_reset_router(), prefix="/auth", tags=["auth"])
    app.include_router(get_users_router(), prefix="/users", tags=["users"])

    @app.get("/health")
    async def health() -> dict[str, str]:
        return {"status": "ok", "version": __version__}

    @app.get("/health/db")
    async def health_db() -> dict[str, str]:
        try:
            async with engine.connect() as conn:
                await conn.execute(text("SELECT 1"))
        except Exception as exc:
            raise HTTPException(status_code=503, detail="database unavailable") from exc
        return {"status": "ok"}

    return app


app = create_app()
