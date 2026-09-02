# Authentication flow (runtime)

What happens on the wire for each auth request. Implementation:
`python/src/plot_backend/app/auth/` (router, rate_limit, dependencies,
user_manager) on FastAPI Users; configuration uses the `PLOT_` env prefix.

## Endpoints

| Route | Purpose |
|---|---|
| `POST /auth/register` | create an account (email + password) |
| `POST /auth/request-verify-token` | send an email-verification token |
| `POST /auth/verify` | confirm the email address |
| `POST /auth/jwt/login` | credentials → access + refresh tokens |
| `POST /auth/jwt/refresh` | refresh → new token pair (rotated) |
| `POST /auth/jwt/logout` | 204; client-side token discard |
| `POST /auth/forgot-password`, `POST /auth/reset-password` | password reset |
| `GET /users/me`, `PATCH /users/me` | current account read/update |

## Login sequence (`POST /auth/jwt/login`)

1. **Rate limit first.** Atomically `INCR` + `EXPIRE(NX)` on two Redis
   keys — `rl:login:<sha256(email)>` and `rl:login:<client-ip>` — sliding
   15-minute window, cap 5 each. Over the cap on either key → 429
   `TOO_MANY_ATTEMPTS`. Redis unreachable → allow through, log a warning
   (fail-open).
2. **User lookup** by email → unknown: 400 `EMAIL_NOT_FOUND`.
3. **Password verify** (hash rewritten if the scheme strengthened) →
   mismatch: 400 `INVALID_PASSWORD`.
4. **Active check** → inactive: 400 `LOGIN_BAD_CREDENTIALS`.
5. **Verified check** → unverified: 403 `LOGIN_USER_NOT_VERIFIED`.
6. **Token issue**: access JWT (15 min, Bearer) + refresh JWT
   (7 days, audience `fastapi-users:refresh`).
7. `on_after_login` hook (currently a log line).

## Refresh sequence

Decode the refresh JWT with its audience checked → load the user →
the account must still be active → issue a fresh token pair (rotation).
Any decode or lookup failure: 401 `INVALID_REFRESH_TOKEN`.

## Deployment note

Behind a reverse proxy, uvicorn must run with `--proxy-headers` and
`--forwarded-allow-ips` restricted to the proxy — otherwise every client
behind it shares one IP rate-limit counter. Never trust forwarded headers
from untrusted clients.

## Operational knobs (`PLOT_` env)

| Variable | Default | Role |
|---|---|---|
| `PLOT_SECRET_KEY` | — | signs access + refresh + verify/reset tokens |
| `PLOT_ACCESS_TOKEN_EXPIRE_MINUTES` | 15 | access token lifetime |
| `PLOT_REFRESH_TOKEN_EXPIRE_DAYS` | 7 | refresh token lifetime |
| `PLOT_REDIS_URL` | `redis://localhost:6379/0` | rate-limit store |
| `PLOT_POSTMARK_API_KEY` | unset | unset → dev log sink for tokens; set → real delivery (wave-07) |
