# Plot (carto)

Find the best terrain/parcel to build or invest in France. Two modes:
**Primary residence** (buried house lot, standard lot,
house, apartment) and **Rental investment** (house, apartment,
lot) — each with its own criteria, scoring weights, and data sources.

Multi-language monorepo: TypeScript frontend + Python backend behind one GNU
Make entrypoint, built from the [ostara-labs repo-template](https://github.com/ostara-labs/repo-template).

[![CI](https://github.com/ostara-labs/plot/actions/workflows/ci.yml/badge.svg)](https://github.com/ostara-labs/plot/actions/workflows/ci.yml)
[![Security](https://github.com/ostara-labs/plot/actions/workflows/security.yml/badge.svg)](https://github.com/ostara-labs/plot/actions/workflows/security.yml)
[![Release](https://img.shields.io/github/v/release/ostara-labs/plot)](https://github.com/ostara-labs/plot/releases)

## Stacks

| Stack | Directory | Marker | Package |
|---|---|---|---|
| Frontend | `typescript/` | package.json | `@ostara-labs/plot` |
| Backend | `python/` | pyproject.toml | `plot-backend` / `plot_backend` |

Frontend: SvelteKit + Skeleton Svelte + MapLibre GL JS.
Backend: FastAPI + geopandas/shapely + PostGIS.

## Quickstart

1. Install pre-commit + the toolchains for both stacks (see CONTRIBUTING.md).
2. Clone with submodules (or `git submodule update --init`).
3. `make deps && make hooks`
4. `make ci`

## Commands

| Target | What it does |
|---|---|
| `make help` | List all targets |
| `make hooks` | Install pre-commit hooks |
| `make deps` | Install dependencies in all present stacks |
| `make format` | Format all present stacks |
| `make lint` | Lint all present stacks |
| `make test` | Test all present stacks |
| `make build` | Build all present stacks |
| `make ci` | `lint` + `test` — the full local gate |
| `make clean` | Remove build artifacts |
| `make lint-typescript` | One stack only (`-typescript`, `-python` also available) |
| `make db-up` | Start the local dev stack (PostGIS + Redis) |
| `make db-down` | Stop the local dev stack (keeps volumes) |
| `make migrate` | Apply database migrations (Alembic) |
| `make migrate-down` | Roll back one migration (`steps=N` for more) |
| `make migration m="..."` | Autogenerate a migration from the models |
| `make api` | Run the FastAPI dev server (auto-reload) |

Absent stacks print `[target] skipped (no <marker>)` and are ignored.

## Documentation

Suggested reading order for humans: MANIFEST → CONTRIBUTING → the docs
tree below (guidelines first).

- SPEC.md + specs/ — product specification (wave tree)
- MANIFEST.md — file inventory and bootstrap checklist
- CONTRIBUTING.md — setup, conventions, PR process
- SECURITY.md — supported versions and vulnerability reporting
- docs/architecture/ARCHITECTURE.md — layout rationale and CI/CD flow
- docs/architecture/decisions/ — architecture decision records
- docs/guidelines/ — repo rules (engineering principles: coding-patterns.md)
- docs/processes/ — process and code-walkthrough docs (code wins over prose)
- docs/domain/ — business-domain concepts and glossary (fill after bootstrap)
- docs/how-to/ — task-oriented recipes for humans
- docs/SOURCES.md — open data sources used by the product

## License

MIT — see LICENSE.
