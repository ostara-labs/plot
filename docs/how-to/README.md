# How-to guides

Task-oriented recipes for humans working in a repository created from
this template. Each guide is a short path to a done thing; the *why*
lives in `../guidelines/` and `../architecture/`.

## Bootstrap

- **Create your project from this template** → [MANIFEST.md](../../MANIFEST.md)
  (the guided selection pass: keep stacks, delete the rest, rename
  placeholders, run `scripts/setup-rulesets.sh`)
- **Set up a dev machine** → CONTRIBUTING.md § Setup (`make deps && make hooks`)

## Daily work

- **Add a feature** → branch from `main`, code, `make ci`, PR (Conventional
  Commits title); CI + review do the rest
- **Run everything locally** → `make help` lists all targets;
  `make ci` = lint + test across kept stacks
- **Test one thing** → per-stack single-test commands in AGENTS.md

## Maintenance

- **Handle a Dependabot PR** → checks must be green; if it touches
  trust-boundary paths (workflows, dependency policy...) it needs a
  code-owner approval — see `../processes/`
- **Cut a release** → merge the release-please PR when it appears;
  versions, tags, changelogs are generated
- **Remove a stack** → delete the directory, then its entries in
  `.github/workflows/ci.yml`, `dependabot.yml`,
  `release-please-config.json` (checklist in MANIFEST.md)
- **Change CI or protected files** → expect the `requires-human-review`
  label; a code-owner approval unlocks merge

## Troubleshooting

- **Pre-commit hook fails on files I did not touch** → hooks run repo-wide
  gates (`make lint` / `make test`); investigate and fix the repo-wide
  failure, or follow the approved exception process — never bypass hooks
  with `--no-verify` (see AGENTS.md)
- **pnpm version mismatch** → run pnpm from inside `typescript/`, not from
  the repo root (corepack resolves the pinned version per directory)
