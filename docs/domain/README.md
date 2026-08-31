# Domain

This directory documents the **business domain** of the project generated
from this template: the concepts of the problem space, independent of any
implementation.

The template ships this directory empty on purpose — a template has no
domain. Fill it as soon as your project has one; it is most valuable in
the first weeks, before implicit knowledge fossilizes in people's heads.

## What belongs here

- `glossary.md` — ubiquitous language: one entry per term, definition,
  and what it is NOT (the fastest way to kill ambiguity)
- `<concept>.md` — one file per core concept: rules, invariants, examples,
  edge cases. Written for a reader who knows nothing about the code

## Why it matters (even for small projects)

- Onboarding: a new contributor (human or AI agent) reads the domain docs
  before the code and asks 10x better questions
- Naming: arguments about names are really arguments about concepts;
  writing them down settles them once
- Boundary detection: concepts that keep appearing together hint at
  module boundaries

## Relationship to code

Domain docs describe the problem; the code implements a solution. They can
legitimately diverge — but if the *vocabulary* diverges (same word means
different things in docs and code), treat it as a bug and fix it.
