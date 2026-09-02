"""Settings parsing tests (env prefix PLOT_)."""

from plot_backend.app.config import Settings


def test_settings_defaults():
    settings = Settings(_env_file=None)
    assert settings.database_url == "postgresql+asyncpg://plot:plot@localhost:5432/plot"
    assert settings.access_token_expire_minutes == 15
    assert settings.refresh_token_expire_days == 7


def test_settings_reads_plot_prefixed_env(monkeypatch):
    monkeypatch.setenv("PLOT_DATABASE_URL", "postgresql+asyncpg://test:test@db:5432/test")
    monkeypatch.setenv("PLOT_SECRET_KEY", "test-secret")
    monkeypatch.setenv("PLOT_ACCESS_TOKEN_EXPIRE_MINUTES", "30")

    settings = Settings(_env_file=None)

    assert settings.database_url == "postgresql+asyncpg://test:test@db:5432/test"
    assert settings.secret_key == "test-secret"
    assert settings.access_token_expire_minutes == 30
    assert settings.refresh_token_expire_days == 7
