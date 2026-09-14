# Business rules

Rules currently in force (wave 1). Each rule states the invariant and
why; the code that enforces it is the source of truth — if this file
diverges from the code, fix this file.

## Data architecture

1. **Indexed columns for everything queried.** A field used in WHERE,
   ORDER BY or scoring is a dedicated, B-tree indexed column
   (`price_in_euros`, `surface_in_square_meters`, `commune`,
   `report_count`, …). JSONB is display-only; when a JSONB field must
   become queryable, it graduates to a real column (or a
   `GENERATED ALWAYS AS … STORED` virtual column).
2. **JSONB holds display-only payloads.** Photos, features, criteria,
   latest results, score breakdowns, open-data enrichment: read and
   render, never filter on.
3. **Binaries never enter the database.** Photos live in S3-compatible
   object storage; the database stores URLs/references only.
4. **Dual coordinates.** Every geometry is stored twice: WGS84
   (EPSG:4326) for MapLibre rendering and tiles, Lambert-93 (EPSG:2154)
   for PostGIS spatial math. See ADR-0002.
5. **Open data and listings merge at read time.** ETL-fed
   terrains/properties stay authoritative for their facts; user listings
   never copy them. See ADR-0003.

## Identity and moderation

6. **Blocked is not disabled.** `is_blocked` is the moderation flag
   (wave-08); it does not gate FastAPI Users login, which is driven by
   `is_active`. A blocked user keeps `is_active=True` until a moderator
   acts.
7. **Verification is column-level explicit.** The FastAPI Users
   attribute `is_verified` maps to the database column `email_verified`
   (27.27: the column names what it means, not the framework).
8. **Roles and account types are orthogonal.** What a user is
   (individual/agency/notary) never implies what a user may do
   (user/moderator/admin).

## Listings lifecycle

9. **Native enums, stored values.** Each enum is a native PostgreSQL
   type with an explicit name; the stored value is the member value
   (`sold`, not `SOLD`), all English.
10. **Listing lifecycle is enum-driven.** active → under_offer →
    sold/rented → archived/disabled/deleted; `reported` is set by
    moderation. `report_count` is denormalized on the listing for fast
    sorting.
11. **Claims are reviewed, never automatic.** A claim moves
    pending → approved/rejected; approval flips the listing's
    `claim_status` and grants ownership. Proof documents are URLs to
    object storage.

## Shared mechanics

12. **Polymorphic targets are two columns.** Favorites and scores point
    at a terrain or a property via `target_type` + `target_id` — no
    cross-table FK, integrity enforced at the application layer.
13. **Shares are tokens, not rows of content.** A share is a unique,
    expirable, revocable token; revocation is a boolean, expiry a
    timestamp.
