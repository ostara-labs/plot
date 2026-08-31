"""Application settings, loaded from environment variables (prefix PLOT_)."""

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# ``.env`` lives at the repository root (next to ``.env.example``). Resolve it
# from this file's location so the path is stable regardless of the process
# working directory (uvicorn may be started from the repo root or python/).
_REPO_ROOT = Path(__file__).resolve().parents[4]


class Settings(BaseSettings):
    """Runtime configuration for the Plot backend.

    Values come from environment variables prefixed with ``PLOT_`` (e.g.
    ``PLOT_DATABASE_URL``) or from a ``.env`` file at the repository root.
    """

    model_config = SettingsConfigDict(
        env_prefix="PLOT_",
        env_file=_REPO_ROOT / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    database_url: str = "postgresql+asyncpg://plot:plot@localhost:5432/plot"
    secret_key: str = "dev-secret-key-change-me"
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 7


@lru_cache
def get_settings() -> Settings:
    """Return the cached application settings instance."""
    return Settings()
