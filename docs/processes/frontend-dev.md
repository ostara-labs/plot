# Frontend development process

Daily-process notes for the TypeScript stack (`typescript/`, package
`@ostara-labs/plot`): what is generated, what is enforced, and the traps
that already bit once. Stack: SvelteKit 2 + Svelte 5, Skeleton, MapLibre
GL JS, Paraglide (inlang) for i18n, Vitest, Biome, pnpm.

## Generated directories — never edit, never commit

| Directory | Produced by | Regenerate with |
|---|---|---|
| `typescript/.svelte-kit/` | SvelteKit codegen | `pnpm dev` / `pnpm build` / `svelte-kit sync` |
| `typescript/src/lib/paraglide/` | Paraglide compiler | `pnpm pretypecheck` (runs on `pnpm typecheck` — pnpm executes `pre*` hooks by default) and the Paraglide Vite plugin (compiles on every `pnpm dev` / `pnpm build`) |
| `typescript/project.inlang/cache/` | inlang tooling | any paraglide command |

`src/lib/paraglide/` carries its own nested `.gitignore` (it ignores its
own output); `.svelte-kit/` is ignored by `typescript/.gitignore`. If
`make lint-typescript` fails on files under these directories on a machine
where a build has run, the local `biome.json` is missing their exclusions
— restore the exclusions, never hand-fix the generated files.

## i18n rule (decision 27.17)

- Every UI string comes from Paraglide messages (`messages/*.json`) —
  inline string literals in components are review findings.
- Adding a key means three files in the same commit: `messages/fr.json`,
  `messages/en.json`, and `messages/fr.meta.json`.
- `pnpm run check:i18n` is wired into both `build` and `test`: a FR key
  without an EN counterpart, or without a complete `fr.meta.json` entry,
  fails the build. There is no runtime fallback.

## Naming guardrails (decision 27.27)

- Biome `useNamingConvention`: camelCase identifiers; object literal
  properties may also be snake_case (Paraglide message keys).
- `src/naming.test.ts` adds a syntax-aware (AST) guard beyond the lint
  rules; its `$schema` key uses bracket notation on purpose (JSON-Schema
  convention, exempt from the naming rule).
- All technical names are English and spelled out, units use the
  `_in_` pattern (`price_in_euros`), booleans read as predicates
  (`is_blocked`). Official French administrative designations (siret,
  commune, insee) are proper names and stay as-is.

## Async map lifecycle

MapLibre is imported dynamically inside `onMount` (SSR safety). The
import is async, so the component may be destroyed before it resolves:
the established pattern (see `MapShell.svelte`) is a `disposed` flag set
by the cleanup callback and checked after the import, plus `map?.remove()`
in the cleanup. Never build a map for a detached container.

## Commands

- Full gate: `make ci` (lint + test across kept stacks).
- Frontend only: `make lint-typescript`, `pnpm exec vitest run <path>`.
- Dev server: `pnpm dev` (in `typescript/`).
