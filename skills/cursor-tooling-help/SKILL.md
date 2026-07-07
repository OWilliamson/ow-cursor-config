---
name: cursor-tooling-help
description: >-
  One-shot reference card for picking Cursor hub skills, rules, hooks, and related
  workflows. Use when the user asks what tool to use, cursor help, which skill,
  tooling map, or invokes /cursor-tooling-help.
disable-model-invocation: true
---

# Cursor tooling help

**One-shot display.** Do not change modes, write files, or persist state unless the user asks in the same turn.

## When to use

- User asks which skill, rule, hook, or workflow fits their goal.
- User says "cursor help", "what tool should I use", or `/cursor-tooling-help`.

## Definition of done

- User sees the **tool picker** table from [reference-tool-picker.md](reference-tool-picker.md) (or a filtered subset matching their question).
- One concrete **next invoke** (`@skill-name` or path) is recommended when intent is clear.

## Boundaries

- Display and recommend only — does not run validate/improve, reconcile, publish, or delegate.

## Workflow

1. Match user intent to a row in [reference-tool-picker.md](reference-tool-picker.md).
2. Output the relevant table section(s) and one recommended `@` invocation.
3. If intent spans profile install vs repo-local `.cursor/` tooling, say which path applies.

## Additional resources

- [reference-tool-picker.md](reference-tool-picker.md) — full decision tables
