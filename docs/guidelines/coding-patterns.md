# Coding patterns

The engineering principles governing every line written in this
repository — stated once, applied everywhere, by humans and AI agents
alike. Each principle ends with **what it looks like here**, because a
principle without enforcement is a wish.

## YAGNI — You Aren't Gonna Need It

Build what the current requirement needs. Nothing speculative: no config
option with one caller, no abstraction with one implementation, no "we'll
need this later".

**Here:** a PR introducing unused parameters, dead exports, or
genericity without a second use case gets sent back. Deleting speculative
code later is cheaper than maintaining it now.

## KISS — Keep It Simple

The simplest solution that satisfies the requirement wins. Complexity is
paid by every future reader, so it must justify itself.

**Here:** prefer flat over clever — boring functions over frameworks,
explicit over implicit, stdlib/first-party over a dependency when the
dependency saves < 50 lines. If a diff needs a paragraph to explain why
it is convoluted, it is wrong.

## Clean Code

Names carry meaning; functions do one thing; side effects are visible;
errors are handled, never swallowed.

**Here:** linters enforce the mechanical part (`biome check`,
`ruff check`) — treat their warnings as errors, never suppress them
inline. The non-mechanical part (naming, decomposition) is review
territory.

## Naming (decision 27.27)

Every technical identifier is English, spelled out, and reveals intent.
French appears only in product documentation (`specs/`, `SPEC.md`) and in
official French administrative designations (`siret`, `commune`, `insee`)
— proper names, not abbreviations.

- **Names reveal intent**: `reliability_score`, not `score` or
  `score_fiabilite`. Length proportional to scope; no invented
  abbreviations.
- **Units spelled out** with the `_in_` pattern in DB columns:
  `price_in_euros`, `surface_in_square_meters`, `slope_in_percent`.
  Official French administrative designations stay as-is (`siret`,
  `commune`, `insee`).
- **Booleans read as predicates**: `is_blocked`, `is_read`, `buildable`.
- **Enums**: English class, member and stored value
  (`ListingStatus.RENTED`); UI labels are Paraglide's job, not the data
  model's.
- **Enforcement**: casing via `ruff` (pep8-naming) and Biome
  `useNamingConvention`; vague names via `python/tests/test_naming.py`;
  intent via CodeRabbit `path_instructions` ("flag names that do not reveal
  intent"). Never suppress — extend the ban list instead.

## Clean Architecture

Dependencies point inward: domain logic knows nothing about frameworks,
databases, or transports. Side-effecting shells adapt the core.

**Here:** keep business rules testable without I/O — unit tests should
not need a network, a database, or a filesystem. When a framework type
leaks into domain logic, wrap it behind a narrow interface owned by the
core.

## Continuous refactoring

Refactoring is part of feature work, not a separate activity. Leave the
code better than you found it (Boy Scout Rule) — but refactor *because*
you must touch the code, not for its own sake.

**Here:** behavior-preserving refactors ship inside the same PR when
small, or as a dedicated PR flagged `refactor:` before the feature.
Never mix behavior changes and restructuring in the same commit.

## ZDD — Zero-Defect Development

Prevent defects instead of hunting them after the fact: make invalid
states unrepresentable, push failures to the earliest possible moment
(compile time > startup > runtime).

**Here:** strict types and exhaustive matches over defensive null-checks;
validation at boundaries (parse, don't validate); every bug fix ships
with the regression test that would have caught it; CI gates are red
until green — "temporarily skipped" tests are deleted tests.

## The meta-rule

When two principles conflict in a specific situation, pick the one that
reduces total complexity over the system's lifetime — and record the
trade-off in an ADR if it will recur.
