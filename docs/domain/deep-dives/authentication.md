# Authentication deep dive

How Plot handles accounts and sessions: who can exist, how identity is
established, and the rules the system enforces — independent of the code
that implements them. The implementation lives in
`python/src/plot_backend/app/auth/` on top of FastAPI Users.

## Concepts

- **Account (User)** — an identity with a unique email (the login key),
  a password hash, and lifecycle flags: active, verified. IDs are UUIDs.
- **Verification** — a freshly registered account exists but cannot log
  in until its email address is confirmed.
- **Session tokens** — two stateless JWTs issued at login: an
  **access token** (15 minutes) and a **refresh token** (7 days, dedicated
  audience `fastapi-users:refresh`, rotated on every refresh).
- **Login attempt** — one credential submission, counted per identity and
  per source for the rate limit.

## Rules

1. **Verified-only login.** A correct password on an unverified account
   is rejected with 403 — deliberately distinct from a wrong-password 400.
2. **Distinct credential errors (27.7).** Unknown email and wrong
   password produce different public messages, both 400; an inactive
   account answers the generic bad-credentials message.
3. **Login rate limit (27.8).** At most 5 attempts per 15 minutes,
   counted independently per email and per client IP; over the cap on
   either → 429. The email is stored only as a SHA-256 hash: no PII in
   the rate-limit store.
4. **Fail-open availability (27.14).** If the rate-limit store (Redis)
   is unreachable, attempts are allowed and a warning is logged — an
   outage must never become a site-wide lockout.
5. **Atomic counters.** Each rate-limit counter and its TTL are set in
   one atomic operation, so an interrupted write can never leave a
   permanent block (a key without expiry).
6. **Stateless logout.** Logout discards tokens client-side; the server
   keeps no revocable session state (204).
7. **Hash rotation on login.** When the configured hashing scheme
   strengthened since the stored hash, a successful login transparently
   rewrites it.
8. **Token delivery boundary.** Verification and reset tokens are
   generated server-side; until the mail provider is configured
   (wave-07, Postmark) they go to a dev log sink and are never emailed.

## Deferred, by design

- Profile fields (names, account type, siret) belong to registration
  step 3 (spec wave-01 §20); the auth schemas stay minimal meanwhile.
- Roles (particulier / agence / notaire) and the reliability score are
  data-model fields whose workflows ship in later waves.
- SMS (SMSemode) is not part of this wave.
