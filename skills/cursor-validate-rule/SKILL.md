---
name: cursor-validate-rule
description: >-
  Validates a Cursor rule file (.mdc) with read-only checks, CR-norm findings,
  and a chat report. Use when checking a rule for authoring-norm issues, dead
  activation, glob precision, inter-rule conflicts, or scope-layer overlap
  before shipping or after drift is suspected.
disable-model-invocation: true
---

# Validate Cursor rules

This skill is explicit-only. Invoke it with `/cursor-validate-rule` or `@cursor-validate-rule`.

## When to use

- The user wants a rule checked for authoring quality before shipping.
- The check should be read-only — no edits, only a findings report.
- The goal is to verify frontmatter, activation mechanics, body structure, and overlap.

## Required inputs

- **Target**: absolute path to the `.mdc` file to validate.
- **Scope** (if unclear): full pass is default.

## Definition of done

- The target `.mdc` has been checked against `reference-cursor-rule-authoring-norms.md`.
- Findings are reported with norm IDs and severity labels.
- Activation is covered: dead rule check, glob precision test, always-on budget, inter-rule conflicts, scope-layer overlap.
- Passing checks are acknowledged.
- Any speculative items are explicitly marked.
- The output follows `reference-report-skeleton.md`.

## Non-goals

- Do not modify the target rule.
- Do not rewrite the rule for style or clarity.
- Do not run improve-style refactors.

## Principles

0. Treat the `.mdc` as the unit. If it links to a paired sibling (e.g. `reference-*.md`), include that in scope.
1. Use verifiable checks (binary pass/fail) over advisory notes.
2. Acknowledge passing checks explicitly; do not omit them silently.
3. Mark mechanically unconfirmed findings as speculative.

## Rule artifact types

Classify everything in scope before evaluating.

| Type | Examples | What to check |
|------|----------|---------------|
| Rule entry | `*.mdc` | All CR-norm checks; frontmatter + activation + body |
| Paired reference | `reference-*.md` linked from the rule | Sections cited; no unused bulk |
| Index / human doc | `README.md` in rules folder | Human-only; check for drift from the live rule |

## Workflow

1. Confirm the target path is a `.mdc` file and list any linked siblings.
2. If a workspace root exists, read `AGENTS.md` and sibling files under `.cursor/rules/` for overlap context; also check `~/.cursor/rules/` for user-scope rules on the same topic (`CR-SCOPE-LAYER`). If no workspace, ask once.
3. Read the target and any linked sibling in scope.
4. Run all CR-norm checks from `reference-cursor-rule-authoring-norms.md`:
   - **Frontmatter and activation:**
     - Dead rule: `alwaysApply: false` + no `globs` and no meaningful `description` (`CR-DEAD-RULE`). `alwaysApply: false` with one-line `description` and no `globs` = apply intelligently.
     - Folded `description`: no `>-`, `|`, or multiline block values (`CR-DESC-SINGLE-LINE`).
     - Glob precision: state one path that should match and one that should not (`CR-GLOB-PRECISION`).
     - Picker label: `description` reads as a clear one-liner (`CR-DESC-PICKER`).
     - Scope contradictions: `alwaysApply: true` + "only when editing X" body text (`CR-SCOPE-EXCLUSIVE`).
   - **Always-on budget:** list all `alwaysApply: true` rules in the directory; sum line counts or run `npx cursor-doctor budget`; flag if disproportionate (`CR-ALWAYS-ON-BUDGET`).
   - **Inter-rule conflicts:** list simultaneously active rules; check for overlap or contradiction (`CR-INTER-RULE-CONFLICT`).
   - **Body:** one concern per rule (`CR-ONE-CONCERN`); line budget (`CR-LINES-BUDGET`).
   - **Siblings:** `CR-RULE-NO-ORPHANS`, `CR-RULE-REFS-EXIST`, `CR-RULE-SIBLINGS-LEAN`.
5. Label findings Critical, Suggestion, or Nice to have.
6. Mark unconfirmed findings as speculative.
7. End with a final sanity pass before reporting.

## Check handling

- Use `wc -l`, `python3 -c`, and link resolution checks as needed.
- For activation, state sample paths explicitly (see report skeleton).
- Cap detailed findings at seven; list remaining norm IDs only.
- Acknowledge passes explicitly.

## Output format

Use `reference-report-skeleton.md` for the report structure.

## Additional resources

- [reference-cursor-rule-authoring-norms.md](reference-cursor-rule-authoring-norms.md)
- [reference-report-skeleton.md](reference-report-skeleton.md)
- [reference-examples.md](reference-examples.md)
