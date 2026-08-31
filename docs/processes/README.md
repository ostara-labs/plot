# Processes & code internals

This directory explains **how things happen** in this repository: the
recurring processes, and how the code actually works.

> ⚠️ **The code is the single source of truth.**
> Everything in this directory describes *intent*. When documentation and
> code disagree, the code wins — no discussion. In that case, fixing the
> doc is part of the change that updated the code.

## What belongs here

### Process documentation (`<process-name>.md`)

One file per recurring process, e.g.:

- `release.md` — how a version goes from merge to tagged release
- `dependency-update.md` — what happens when Dependabot opens a PR
- `trust-boundary-review.md` — what a reviewer checks on gated paths

Suggested structure per file: trigger → actors → step-by-step lifecycle →
failure modes → related files.

Diagrams are encouraged (Mermaid renders natively on GitHub).

### Code walkthroughs (`code/<area>.md`)

One file per meaningful area of the codebase (e.g. `code/ci-pipeline.md`,
`code/rust-stack.md`). A walkthrough answers: where do I start reading,
what calls what, where do the important types live, what are the gotchas.

Walkthroughs follow the same rule as everything else: they rot silently.
Prefer pointing at stable symbols (file + function name) over describing
logic in prose — describe the map, not the territory.

## What does NOT belong here

- Why the architecture is shaped this way (that is `../architecture/`
  decisions)
- Domain vocabulary (that is `../domain/`)
- Rules and conventions (that is `../guidelines/`)
