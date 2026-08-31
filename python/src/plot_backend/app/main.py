"""FastAPI application entrypoint."""

from fastapi import FastAPI, HTTPException
from sqlalchemy import text

from plot_backend import __version__
from plot_backend.app.db.session import engine


def create_app() -> FastAPI:
    """Build the FastAPI application."""
    app = FastAPI(title="Plot API", version=__version__)

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
