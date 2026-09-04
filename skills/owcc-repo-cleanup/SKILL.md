---
name: owcc-repo-cleanup
description: >-
  Audits a Cursor-oriented git repository for cleanup opportunities—deletion candidates,
  doc/script mergers, directory consolidation, rehoming rules or Agent Skills to user scope,
  and a .gitignore sanity pass. Use when the user asks to clean up a repo, remove cruft,
  consolidate documentation, audit skills vs project scope, or review .gitignore coverage.
disable-model-invocation: true
---

# Repository cleanup (audit-first)

Explicit-only. Invoke with `/owcc-repo-cleanup`.

## Non-negotiable workflow

1. **Read-only discovery** in the target repository: search, list, read docs. Do **not** delete, merge, rehome, or commit until the user responds to the report.
2. **Emit one structured report** using the template in [reference.md — Report output](reference.md#report-output-template). Index every object (path or rule id); assign each to **one** bucket: **Delete** | **Merge / refactor** | **Rehome (user scope)** | **Review / uncertain**.
3. **Stop and wait.** After the report, ask what subset to execute (or none). Only then apply changes—typically on a **feature branch**, never `main`/`master` unless the user explicitly overrides team policy.

If the user only wanted the audit, end after the report. **Definition of done (audit):** structured report delivered with every object assigned to a bucket and stable IDs. **Definition of done (execution):** approved items applied on a feature branch (never `main`/`master` unless user overrides); user notified of each change.

## Non-goals

- Do not delete, merge, rehome, or commit during the audit phase.
- Do not write to `main`/`master` during execution unless the user explicitly overrides team policy.
- Do not run without user approval after the report.

## What to look for

Buckets, heuristics, and examples: [reference.md — What to look for](reference.md#what-to-look-for).

## Report output

Use stable ids (`D1`, `M2`, …) so the user can reply “execute D1, M2 only”. Full markdown skeleton: [reference.md — Report template](reference.md#report-output-template).

## Execution phase (only after approval)

Follow [reference.md — Execution phase](reference.md#execution-phase-after-approval).

## Further patterns

Optional expanded grep ideas and examples: [reference.md](reference.md).
