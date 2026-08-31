# ADR-0001: Record architecture decisions

## Status

Accepted

## Date

2026-08-23

## Context

We need to record the architectural decisions made on this project, and to
communicate them to all interested parties, including future contributors and
agents. Without a record, decisions are lost, rediscovered, or re-litigated.

## Decision

We will use Architecture Decision Records (ADRs), as described by Michael
Nygard in "Documenting Architecture Decisions". Each ADR is a short text file
in docs/architecture/decisions/ named NNNN-title-with-dashes.md, following
the template in docs/architecture/decisions/adr-template.md. ADRs are
immutable once accepted; new decisions supersede old ones by reference.

## Consequences

- Decisions are documented and reviewable in the same repository as the code.
- ADRs are part of the PR review process: significant decisions require an ADR.
- Accepted ADRs are never edited; corrections are new ADRs that supersede them.
