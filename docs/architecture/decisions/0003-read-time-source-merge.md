# ADR-0003: Merge open-data and user listings at read time

## Status

Accepted

## Date

2026-09-02 (decision from spec wave-01, §27.16)

## Context

Plot consumes two families of real-estate objects: open-data records
(terrains, properties — DVF, IGN, fiscal data) loaded by the ETL chain
(Airflow + dbt, full replication), and user-published listings (manual
entry, imports, later claims). The same physical good can exist in both
worlds. Copying open-data facts into listings at write time — or the
reverse — would create dual-write inconsistency: two stores claiming
authority over the same fact, drifting on every update cycle.

## Decision

Open data and listings stay in their own tables and merge at READ time:

- `terrains` / `properties` are authoritative for open-data facts; they
  are written only by the ETL.
- `listings` are authoritative for offers; they never copy open-data
  facts and hold no foreign key to terrains/properties.
- API queries join/project the two at request time (matching by
  geometry/commune) — enrichment happens in the read layer, not in the
  stores.

## Consequences

- No dual-write path: each store is written by exactly one pipeline, so
  ETL re-runs and user edits can never fight.
- Read queries carry the merge logic — the cost lives in one shared
  read layer, testable once.
- Claims (wave-03+) let a user take ownership of a listing without
  importing open data into it; the listing's `claim_status` records the
  state.
- Freshness is the union of both pipelines; an object that disappears
  from open data does not disappear from user listings.
