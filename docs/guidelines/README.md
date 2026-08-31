# Guidelines

The rules of this repository — indexed here, defined in their own file.
One rule, one authoritative location: this page only points.

## Engineering principles

| Principle | Where |
|---|---|
| YAGNI, KISS, clean code, clean architecture, continuous refactoring, zero-defect | [coding-patterns.md](coding-patterns.md) |

## Contribution flow

| Rule | Where |
|---|---|
| How to contribute, commit format, PR checklist | [CONTRIBUTING.md](../../CONTRIBUTING.md) |
| Local quality gates (lint on commit, tests on push) | [.pre-commit-config.yaml](../../.pre-commit-config.yaml) |
| Make targets (`make deps`, `make ci`, ...) | root [Makefile](../../Makefile) |

## Branch & merge policy

| Rule | Where |
|---|---|
| PRs required, status checks required, force-push blocked | `main-protection` ruleset (repo Settings → Rules → Rulesets; provisioned by [scripts/setup-rulesets.sh](../../scripts/setup-rulesets.sh)) |
| Human approval for CI/dependency/release/governance files | [CODEOWNERS](../../.github/CODEOWNERS) + [trust-boundary.yml](../../.github/trust-boundary.yml) |
| Conventional Commits (`type(scope)!: subject`) | enforced by commit-msg hook; see CONTRIBUTING.md |

## Security

| Rule | Where |
|---|---|
| Reporting vulnerabilities (do NOT open an issue) | [SECURITY.md](../../SECURITY.md) |
| Secret scanning (CI + pre-commit) | gitleaks — config in [.gitleaks.toml](../../.gitleaks.toml) |

## Documentation rules

- Docs live under `docs/` with one concern per subdirectory (see the
  README of each)
- In `docs/processes/`, **the code is always authoritative** over prose
- Architecture decisions get an ADR before merge:
  `docs/architecture/decisions/`
