---
name: repo-convention-change
description: >-
  Guides defining, restating, or redefining repository-wide conventions (naming, layout, policy)
  with explicit triage so drift fixes are not mistaken for new rules. Use when the user sets or
  corrects team standards, says a convention was already decided, asks to align docs or tooling to a policy,
  introduces a single source of truth, or wants migration from an old pattern—any project with
  AGENTS.md, CONTRIBUTING, or docs hubs.
disable-model-invocation: true
---

# Repository convention and policy change

Human install and copy notes: [README.md](README.md).

Use this skill **before** editing scattered files when the task touches **how the repo should behave or read**, not only feature code.

## When to read

- User **defines**, **restates**, **standardizes**, or **redefines** a repo-wide rule (naming, paths, dates, branches, review bars, generated artifact shape).
- User implies **“we already agreed on this”** or **“fix drift”** vs **“introduce something new”**—ambiguity is high.
- User asks for a **canonical doc**, **policy table**, or **alignment** across handbook, rules, scripts, and tests.

**Defer instead of duplicating:** for CLI flags, packagers, and generated artifacts, apply the **`repo-tooling-invariants`** rule after policy is clear. For auditing `AGENTS.md` / `.cursor/rules` / hubs holistically, use **`cursor-workflow-review`**.

## Phase 0 — Classify (mandatory, answer in prose before large edits)

Pick **one** primary mode; if mixed, split into two passes.

| Mode | Meaning | Typical outcome |
| ---- | ------- | ---------------- |
| **A — New** | First written policy for this topic, or intentional new rule. | Add canonical doc; link once from handbook; optional checks. |
| **B — Restatement** | Rule already stated; implementation or docs are wrong or incomplete. | **One** canonical file already exists or is obvious—**close the gap**; do not invent a parallel “nicer” convention. |
| **C — Redefinition** | Old rule is **explicitly** superseded (breaking change). | Update canonical doc first; list migrations (renames, CI, callers); avoid silent half-migration. |

If the user did not say **A/B/C**, infer from their words and **state your inference** in one sentence before proceeding.

## Phase 1 — Discover (read-only)

1. Identify the **handbook**: `AGENTS.md`, `CONTRIBUTING.md`, `CLAUDE.md`, or root `README.md`—whichever the team treats as contract.
2. Find **existing** mentions: search handbook, `.cursor/rules`, `docs/` hub, and tooling readmes for the topic (naming, branches, dates, etc.).
3. Decide **single canonical file** for this convention (prefer one markdown path; avoid duplicating full policy in three places).

Output a **three-line summary**: current state, canonical path (or “none—create”), and contradictions found.

## Phase 2 — Author or update the canonical policy

1. Edit **only** the canonical file (or create it under `docs/` if the repo uses a doc hub—adjust to repo layout).
2. Policy text must include: **scope** (what paths or artifacts), **allowed character set or pattern** if naming, **examples** (correct vs wrong), **non-goals** (what this policy does *not* cover), and **relationship to tools** (e.g. “packager enforces X”).
3. Elsewhere: **replace** duplicated prose with **one link** to the canonical section (hub-first; avoid drift).

Templates, longer checklist, expanded phases 3–4, and anti-patterns: [reference.md](reference.md).

## Phase 3 — Align implementation

Update callers, tooling, tests, and other docs to match the canonical policy (rename, re-link, remove duplicated prose). Full checklist and examples: [reference.md — Phase 3](reference.md#phase-3-align).

## Phase 4 — Verify

Confirm no stale references remain: search for the old pattern, run affected tests, verify CI passes. Full checklist: [reference.md — Phase 4](reference.md#phase-4-verify).

## Summary

**Classify → discover → one canonical doc → align code/docs/tests → verify.** Restatement means **enforce what was already decided**, not reinterpret.
