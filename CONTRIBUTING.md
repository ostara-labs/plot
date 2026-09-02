# Contributing

## Environment setup

### Windows

- GNU Make >= 4: `choco install make`
- Git Bash in PATH — the Makefile recipes are POSIX
- Line endings are enforced as LF by `.gitattributes`

### Linux

- GNU Make >= 4: `sudo apt install make` (or your distro's package)

### macOS

- GNU Make >= 4: `brew install make` (or Xcode Command Line Tools)

## Toolchains

Install only the toolchains for the stacks you keep:

| Stack | Toolchain |
|---|---|
| TypeScript | Node 22 + pnpm (via corepack) |
| Python | uv |

## Getting started

1. Install pre-commit: `pipx install pre-commit` (or `pip install pre-commit`).
2. Clone with submodules (or run `git submodule update --init` in an
   existing clone) — the shared Makefiles live in `.devtools/`.
3. Install dependencies and hooks: `make deps && make hooks`.
4. For backend work, start the stack and apply migrations:
   `make db-up && make migrate`.
5. Run the full gate: `make ci`.
6. When you need the dev server, run `make api` in a separate terminal
   (it stays in the foreground until interrupted).

## Commit convention

Conventional Commits. The type is required; the scope is optional.

| Type | Purpose |
|---|---|
| feat | New feature |
| fix | Bug fix |
| docs | Documentation |
| style | Formatting; no behavior change |
| refactor | Code change; no behavior change |
| perf | Performance improvement |
| test | Tests |
| build | Build system |
| ci | CI configuration |
| chore | Maintenance |
| revert | Revert a commit |

Breaking changes: append `!` to the type, e.g. `feat!: drop Node 20`.
Scope: optional, e.g. `feat(typescript): add greet`.

## Pull requests

Keep PRs small and focused: one logical change per PR. Before opening a PR,
check the definition of done:

- `make ci` is green locally.
- Docs updated (README, MANIFEST, ADRs as applicable).
- No unrelated changes in the PR.

## Releases

Releases are automated by release-please, which derives versions and
changelogs from Conventional Commits on `main`. Never bump versions manually.
