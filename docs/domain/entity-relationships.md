# Entity relationships

The wave-1 data model: 15 tables in five bounded areas, 17 native
PostgreSQL enum types. Source of truth:
`python/src/plot_backend/app/db/models/`. Conventions referenced below:
ADR-0002 (dual coordinates), business rules (JSONB policy).

## Identity (`identity.py`)

- **users** — accounts. Lifecycle flags `is_active` / `is_superuser` /
  `email_verified` (FastAPI Users), moderation flag `is_blocked`
  (independent), `account_type` (individual/agency/notary, optional),
  `role` (user/moderator/admin), `reliability_score` (nullable),
  `locale` (default `fr`).

## Projects (`projects.py`)

- **projects** — saved searches owned by a user (nullable: anonymous
  drafts allowed), with criteria (JSONB), an optional zone as polygon or
  center+radius, `max_budget_in_euros`, cached `latest_results` (JSONB)
  and `new_offers_count`.
- **priority_zones** — polygons attached to a project, with a priority
  level.
- **weighting_profiles** — named scoring weights (JSONB) per project
  category, reusable across projects.

## Geodata (`geodata.py`) — open-data, ETL-fed

- **terrains** — cadastral parcels: `parcel_id`, `commune`, buildability,
  tax, slope, exposure; open-data extras in `metadata` (JSONB).
- **properties** — houses/apartments from open data: DPE and GES
  classes, potential rent, tax.
- **scores** — computed scores with a polymorphic target
  (`target_type` + `target_id` → terrain or property), per category,
  with a JSON breakdown.

## Listings (`listings.py`) — user-published

- **listings** — offers owned by a user: type (terrain/house/apartment),
  lifecycle status, price/surface/DPE/bedrooms, `source` (manual, import,
  claim), `claim_status`, denormalized `report_count`.
- **reports** — unavailability signals on a listing; user is nullable
  (anonymous reports carry a `device_fingerprint`).
- **claims** — ownership requests on a listing, with proof document URL
  and admin note.

## Engagement (`engagement.py`)

- **feedback** — in-app feedback, user nullable, token-tracked.
- **contacts** — buyer-to-seller messages on a listing.
- **favorites** — bookmarks with polymorphic target
  (`favorite_target_type` + `target_id`), optional project link.
- **shares** — public links by unique token, expirable and revocable.
- **notifications** — per-user in-app notifications, read flag.

## Relationships

- users 1—N: projects, listings, weighting_profiles, favorites, shares,
  contacts (as sender), notifications, feedback (optional).
- projects 1—N: priority_zones; projects N—1 users (optional).
- listings 1—N: reports, claims, contacts; listings N—1 users (owner).
- Polymorphic (no FK): favorites and scores point at terrains or
  properties through `target_type` + `target_id`.
- No FK between listings and terrains/properties: open-data objects and
  user listings merge at read time (ADR-0003).

## Column conventions

- Every geometry column exists twice: `geometry` (EPSG:4326, WGS84) and
  `geometry_lambert_93` (EPSG:2154), each with a GiST spatial index
  (ADR-0002).
- Query, sort and scoring fields are dedicated indexed columns
  (`price_in_euros`, `surface_in_square_meters`, `commune`,
  `report_count`, …); JSONB holds display-only data only.
- All enums are native PostgreSQL types with explicit names; stored
  values are the member values, all English (27.27).
- IDs are UUID v4 (server-side `gen_random_uuid()`); timestamps are
  timezone-aware, with `created_at` / `updated_at` maintenance.
