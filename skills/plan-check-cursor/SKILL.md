---
name: plan-check-cursor
description: >-
  Refines Cursor implementation plans into Build-ready execution contracts with
  clear scope, dependency-ordered todos, and checkable validation gates. Use
  when tightening plan files or Plan mode output before running Build or
  continuing execution with @plan.
disable-model-invocation: true
---

# Check and improve Cursor plans

This skill is explicit-only. Invoke it with `/plan-check-cursor` or `@plan-check-cursor`.

## When to use

- The user has a plan file or Plan mode output that needs to be made Build-ready.
- Execution will run through Cursor Build or a follow-up agent run from `@plan`.
- The current plan is ambiguous, oversized, duplicated, or hard to resume.

## Required inputs

- **Target**: absolute path to the plan file, or full pasted plan content.
- **Scope** (if unclear): todos only, body only, or full pass.
- **Execution route** (if known): Cursor Build, Agent from `@plan`, or human-led.

## Definition of done

- Plan is Build-sized (or split into phases) with a complete execution contract: frozen decisions, definition of done, non-goals, first action, final validation, continuation rule, and a sequential-execution directive in the plan body.
- Each non-trivial todo is paired with a verification step; the final todo is a completion audit.
- Todos are dependency-ordered, verb-led or binary checks, with no body duplication.
- Ambiguous todos include a short example; self-explanatory items do not.
- Resumable work names an authoritative workspace file (not only internal todos).
- Report includes Summary, Concrete edits, and Residual risks.

## Non-goals

- Do not remove requirements unless the user explicitly approves removal; relocate, compress, or point instead.
- Do not silently expand scope into implementation unless the user asked to build.
- Do not invent product or org facts; flag unknowns when they block execution.
- Do not promise Cursor runtime behavior; encode resilient handoff instead.

## Workflow

1. Confirm target, scope, and execution route.
2. Read frontmatter and body; capture frozen decisions and missing gates.
3. Size for Build: one scope or split into phases with per-phase scope, first action, validation, and handoff.
4. Add or tighten the execution contract: frozen decisions, checkable definition of done, non-goals, first action, final validation, continuation rule.
5. Add a sequential-execution directive in the plan body: execute one todo at a time, mark complete before advancing.
6. Rewrite todos: dependency order, verb-led actions or binary checks, stable IDs, one source of truth for fuzzy parity items.
7. Pair each non-trivial implementation todo with a verification step (command, diff check, or artifact check). Make the final todo a completion audit: "confirm all N todos marked done; do not report success until all are ticked."
8. Add a short example where a todo, gate, or verification step is likely to be misread; omit for self-explanatory items.
9. Deduplicate body vs todos: keep detail in one place, shorten the duplicate side, group references once.
10. Add stop-if gates for unknown licensing, destructive changes, schema relaxations, external writes, or unknown secrets.
11. Run [reference-checklist.md](reference-checklist.md) and report only the minimal edits needed to pass.
12. Keep user-operator guidance outside mandatory plan content; use [agent-build-plan-notes.md](agent-build-plan-notes.md) for those notes.

## Output format

1. **Summary**: what changed and why.
2. **Concrete edits**: section/todo replacements or patch list.
3. **Residual risks**: unresolved ambiguities or decisions still needed.

## Additional resources

- [reference-checklist.md](reference-checklist.md): pass/fail review gates for plan quality.
- [reference-patterns.md](reference-patterns.md): copyable plan patterns for sequential-execution directives, implement+verify pairs, completion audits, stop-if gates, and example annotations.
- [agent-build-plan-notes.md](agent-build-plan-notes.md): operator-side Build guidance that should not be embedded as mandatory plan tasks.
