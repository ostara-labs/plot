# ADR-0002: Dual coordinate storage (WGS84 + Lambert-93)

## Status

Accepted

## Date

2026-09-02 (decision from spec wave-01, §27.19)

## Context

Plot's data is inherently geographic and French. Source geodata (IGN,
cadastre) is natively projected in Lambert-93 (EPSG:2154), the legal
planar CRS for metropolitan France — the only one where PostGIS
computations (distances, areas, buffers) return correct meters.
Conversely, the rendering stack (MapLibre GL JS, vector tiles via
Martin) consumes WGS84 (EPSG:4326). Transforming coordinates at query
time would put `ST_Transform` on every hot path, defeating the spatial
indexes and adding per-request cost.

## Decision

Every geometry column is stored twice, at write time:

- `geometry` — EPSG:4326 (WGS84), for rendering and tiles;
- `geometry_lambert_93` — EPSG:2154, for PostGIS spatial calculations.

Both carry a GiST spatial index. The transform happens once, on write
(ETL or API), via `ST_Transform`; readers never transform.

## Consequences

- Spatial queries (`ST_DWithin`, area, intersection) run planar and
  indexed in Lambert-93 — correct meters, no per-request transform.
- Storage roughly doubles for geometry, and every write writes two
  columns; acceptable at the expected volumes (millions of parcels).
- The two columns can drift if one write path forgets the transform —
  mitigated by a single shared write layer; a consistency check can be
  added to the ETL if drift is ever observed.
- Overseas collectivities (UTM zones, Lambert-93 not valid) are out of
  scope for wave 1 and will need their own ADR.
