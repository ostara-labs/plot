# Configuration

Runtime configuration for the Plot backend: `python/src/plot_backend/app/
config.py`, a pydantic-settings `Settings` class.

## Loading

- Environment variables are prefixed with **`PLOT_`**:
  `PLOT_DATABASE_URL`, `PLOT_SECRET_KEY`, …
- A `.env` file at the **repository root** (next to `.env.example`) is
  also read; its path is resolved from the config module's location, so
  the process working directory does not matter (uvicorn may start from
  the repo root or `python/`).
- Unknown environment variables are ignored (`extra="ignore"`).
- `get_settings()` returns a cached singleton (`lru_cache`): the first
  call fixes the values for the process lifetime.

## Settings (wave 1)

| Setting | Env var | Default | Role |
|---|---|---|---|
| `database_url` | `PLOT_DATABASE_URL` | `postgresql+asyncpg://plot:plot@localhost:5432/plot` | asyncpg connection string; matches `docker-compose.dev.yml` |
| `secret_key` | `PLOT_SECRET_KEY` | `dev-secret-key-change-me` | signs JWTs and verification/reset tokens — **must be changed in production** |
| `access_token_expire_minutes` | `PLOT_ACCESS_TOKEN_EXPIRE_MINUTES` | 15 | access token lifetime |
| `refresh_token_expire_days` | `PLOT_REFRESH_TOKEN_EXPIRE_DAYS` | 7 | refresh token lifetime |

Auth-adjacent knobs introduced by the authentication wave (Redis,
Postmark) are documented in `docs/processes/login-flow.md`; email/SMS
provider variables in `.env.example` activate with their features in
later waves.

## Adding a setting

1. Add the typed field to `Settings` with a safe default.
2. Add the variable to `.env.example` (the only committed template).
3. If it changes behavior, update the relevant doc in the same PR.
