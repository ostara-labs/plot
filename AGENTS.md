# AGENTS.md

## Project overview

**Plot** — find the best terrain/parcel to build or invest in France (carto is
the repo name). Multi-language monorepo: two stacks (TypeScript, Python)
behind one GNU Make entrypoint. Stacks are auto-detected via marker files
(typescript/package.json, python/pyproject.toml); adding a stack means adding
its dir plus its CI, Dependabot, and release-please entries — zero Makefile
edits. Built from the ostara-labs repo-template; shared tooling lives in the
devtools submodule.

- Frontend (typescript/) — SvelteKit + Skeleton + MapLibre GL JS; package
  `@ostara-labs/plot`.
- Backend (python/) — FastAPI + geopandas/shapely + PostGIS; package
  `plot-backend`/`plot_backend`.
- Product spec: `SPEC.md` + `specs/` (wave tree). Data sources:
  `docs/SOURCES.md`.

## Commands

- `make ci` — full local gate (lint + test). Run before declaring work done.
- `make deps` — install dependencies for all present stacks (run after clone).
- `make lint`, `make test`, `make format`, `make build`, `make clean`
- Per-stack: `make lint-typescript`, `make test-python`, ... (suffixes:
  -typescript, -python). Absent stacks print
  `[target] skipped (no <marker>)`.
- Single tests:
  - TypeScript: `cd typescript && pnpm exec vitest run <path>`
  - Python: `uv run pytest <path>::<test_name>` from python/

## Structure

- typescript/ — frontend, package `@ostara-labs/plot`; marker package.json
- python/ — backend, package `plot-backend` / `plot_backend`;
  marker pyproject.toml
- specs/ — wave specification tree (entry point: specs/README.md)
- .github/ — workflows, dependabot, issue/PR templates
- .devtools/ — submodule (ostara-labs/devtools): shared makefiles + stack
  CI workflows. Update deliberately via `make devtools-update`, then commit
  the submodule pointer bump.
- docs/ — architecture/ (ARCHITECTURE.md + decisions/ ADRs),
  guidelines/ (coding-patterns.md), processes/, domain/, how-to/, SOURCES.md

## Documentation policy

### Mandatory context — read before ANY task

- `MANIFEST.md` — the map: what every notable file is for. Never work
  blind on file locations.
- `docs/guidelines/coding-patterns.md` — YAGNI, KISS, clean code, clean
  architecture, continuous refactoring, zero-defect. Every line written
  must comply.

`AGENTS.md` itself is always in context by definition. Nothing else is
mandatory: loading more dilutes attention.

### On demand — consult when the task touches it

| Task involves | Read |
|---|---|
| Structure, CI topology, new stack | `docs/architecture/ARCHITECTURE.md` |
| A significant architectural choice | `docs/architecture/decisions/` (write an ADR) |
| Runtime behavior, "how does X work" | `docs/processes/` |
| Domain vocabulary or business rules | `docs/domain/` |
| Opening the PR (format, checklist) | `CONTRIBUTING.md` |

### Maintenance — keep docs honest in the same PR

- Adding/removing/moving a notable file → update its MANIFEST.md row.
- Changing behavior → update the affected process/architecture doc.
- Finding doc drift while working → fix it in the same PR (the code is
  always the source of truth; stale prose is a bug).

## Code style

- TypeScript: Biome 2.x; 2-space indent
- Python: ruff (check + format); 4-space indent
- Naming (27.27): every technical identifier is English, spelled out,
  intent-revealing; vague names are banned and lint/test-enforced. Specs
  stay French; all other docs are English. See
  `docs/guidelines/coding-patterns.md` (§ Naming).
- Commits: Conventional Commits — types: feat, fix, docs, style, refactor,
  perf, test, build, ci, chore, revert. Breaking changes: `!` after the type
  (e.g. `feat!: ...`). Scope optional (e.g. `feat(typescript): ...`).

## Security and secrets

- Never commit real secrets or `.env` files. `.env.example` is the only
  committed template.
- gitleaks runs in pre-commit and CI (security.yml); a leak blocks the PR.
- Report vulnerabilities via SECURITY.md.

## PR maturity loop

Every PR starts as a **draft** and leaves draft state only when mature:

1. `gh pr create --draft` - never open a finished-looking PR on day one.
2. Ask for a review round: comment `@coderabbitai review` on the PR.
3. Process EVERY finding:
   - fix the code, or
   - dismiss the thread with a written justification when it is wrong.
   Silence is not resolution. Resolve threads you addressed.
4. Push, then go back to step 2. Repeat until a full round produces zero
   findings and zero open threads.
5. The PR is **mature** only when ALL of these hold:
   - no unresolved CodeRabbit comments,
   - every required check is green,
   - size label is `size/L` or smaller (`size/XL` means split the PR).
6. `gh pr ready` - only now does the PR leave draft state and become
   reviewable by humans. Humans read mature PRs, not drafts.

AI review informs; it never replaces human approval on trust-boundary
paths (see CODEOWNERS).

## Boundaries

### Always

- Run `make ci` before declaring work done.
- Update docs and MANIFEST.md when behavior changes.

### Ask first

- Add dependencies.
- Edit `.github/workflows/**`.
- Change the Makefile contract or `.pre-commit-config.yaml`.
- Touch LICENSE. (MANIFEST.md maintenance is routine work — see
  Documentation policy above.)

### Never

- Commit real secrets or `.env`.
- Force-push main.
- Bypass or disable hooks or CI gates.
- Weaken lint configs to pass.
- Commit directly to main.
- Act as a code owner: code ownership of trust-boundary files belongs to
  humans only, never to automation (a bot approving its own changes
  defeats the gate).

## Definition of done

- `make ci` is green locally.
- PR is mature per the PR maturity loop (no open CodeRabbit comments).
- Docs updated (README, MANIFEST, ADRs as applicable).
- No unrelated changes in the PR.

Nested AGENTS.md files are allowed per stack dir and override this file within
that subtree.
