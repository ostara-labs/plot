# MANIFEST

Every file and directory in this repository, what it does, and where it
lives. Maintained continuously — adding/removing/moving a notable file means
updating its row here in the same PR.

## Inventory

### Shared core

| Path | Purpose |
|---|---|
| Makefile | Entrypoint; canonical targets (help, hooks, format, lint, test, build, ci, clean) |
| .pre-commit-config.yaml | Local hooks: hygiene, gitleaks, conventional commits, no-commit-to-main |
| .editorconfig | Editor defaults (LF, indentation) |
| .gitattributes | Line endings, linguist hints |
| .gitignore | Root ignores (stack ignores live in stack dirs) |
| .env.example | Environment template |
| .gitleaks.toml | Secret scanning config |
| README.md | Pitch and quickstart |
| MANIFEST.md | This file |
| AGENTS.md | Agent rules |
| CLAUDE.md | Claude import of AGENTS.md |
| CONTRIBUTING.md | Contribution guide |
| SECURITY.md | Security policy |
| CODE_OF_CONDUCT.md | Contributor Covenant 2.1 |
| CHANGELOG.md | Keep a Changelog |
| LICENSE | MIT |
| SPEC.md | Product spec (entry point; details span specs/) |
| docs/architecture/ARCHITECTURE.md | Layout and flow |
| docs/architecture/decisions/ | ADRs |
| docs/guidelines/, docs/processes/, docs/domain/, docs/how-to/ | Documentation tree (see each README) |
| docs/SOURCES.md | Open data sources used by the product |

### CI, security, release

| Path | Purpose |
|---|---|
| .github/CODEOWNERS | Review ownership |
| .github/dependabot.yml | Dependency updates (npm + pip) |
| .github/pull_request_template.md | PR template |
| .github/ISSUE_TEMPLATE/ | Issue templates |
| .github/workflows/ci.yml | Main CI; thin callers to devtools + workflow-lint gate |
| .devtools/ (submodule) | Shared makefiles, workflows, hooks — ostara-labs/devtools @ v1.0.0 |
| .github/workflows/security.yml | gitleaks + scorecard scan |
| .github/workflows/release.yml | release-please |
| .github/workflows/pr-classify.yml | Trust-boundary PR labeling |
| .github/workflows/pr-meta.yml | PR title lint + size/risk labels |
| .coderabbit.yaml | AI review config (free on public repos) |
| release-please-config.json | Release config; one entry per stack |
| .release-please-manifest.json | Release manifest; one entry per stack |
| .github/trust-boundary.yml | Trust-boundary path patterns |
| scripts/setup-rulesets.sh | Branch-protection ruleset provisioning |

### TypeScript (frontend)

| Path | Purpose |
|---|---|
| typescript/ | Package `@ostara-labs/plot`; marker package.json |
| typescript/.gitignore | Stack ignores |

### Python (backend)

| Path | Purpose |
|---|---|
| python/ | Package `plot-backend` / `plot_backend`; marker pyproject.toml |
| python/.gitignore | Stack ignores |

### Specification tree

| Path | Purpose |
|---|---|
| specs/README.md | Wave tree entry point |
| specs/wave-XX-*/ | Per-wave specification files |

## Post-bootstrap hardening

After the first push:

- [ ] Replace `@Oloompa` in `.github/CODEOWNERS` with your maintainer
      identity or team. These entries are the trust boundary: PRs touching
      CI workflows, dependency policy, release automation, hook config, or
      governance files require a code-owner approval to merge. Normal PRs
      (code, docs, dependency bumps) need no approval.
- [ ] Branch protection on `main`: run
      `bash scripts/setup-rulesets.sh <owner>/<repo>` — creates the
      "main-protection" ruleset (PRs required, force-push/deletion blocked,
      status checks required, code-owner review for trust-boundary paths)
      and the `requires-human-review` label.
- [ ] Secret scanning with push protection: ON.
- [ ] Dependabot alerts: ON.
- [ ] Auto-merge: ON (Settings → General → Pull Requests → *Allow
      auto-merge*, squash only, commit title = PR title, delete branches).
      With the main-protection ruleset this means: normal PRs squash-merge
      as soon as CI is green; trust-boundary PRs merge automatically once
      a code owner approves.
- [ ] Allow GitHub Actions to create pull requests (org admins:
      Organization → Settings → Actions → Workflow permissions → check
      *Allow GitHub Actions to create and approve pull requests*).
      release-please needs this to open its Release PRs; without it the
      Release workflow stays red.
- [ ] Default branch is `main`.
