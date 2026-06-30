---
name: cursor-improve-rule
description: >-
  Refactors Cursor project rules (.mdc) into a leaner, clearer, less drift-prone
  shape before shipping. Use when improving a rule under .cursor/rules, tightening
  frontmatter and body, or aligning a rule with AGENTS.md and sibling rules without
  duplicating them.
disable-model-invocation: true
---

# Improve Cursor rules

This skill is explicit-only. Invoke it with `/cursor-improve-rule` or `@cursor-improve-rule`.

## When to use

- The user wants a rule sharper, shorter, or less misfire-prone before or after shipping it.
- The rule has grown long, duplicated, vague, or inconsistent with its frontmatter `description`.
- The user wants the rule refactored, not just reviewed.

## Required inputs

- **Target**: absolute path to the rule `.mdc` file whose content should change.
- **Scope** (if unclear): default to full pass on that file only.

## Definition of done

- The target `.mdc` has been rewritten toward the shared spine in this file.
- `reference-cursor-rule-authoring-norms.md` has been applied and checked.
- A post-change report is prepared using `reference-report-skeleton.md`.
- Activation verified: at least one sample path matches the declared glob and one does not.
- Mechanical improvement is complete. Behavioural effectiveness is not guaranteed without a pressure test in a fresh session with representative files open.

## Non-goals

- Do not change the rule’s domain policy unless the user asked.
- Do not rename the `.mdc` file unless the user explicitly requested a rename.
- Do not duplicate long prose that already belongs in `AGENTS.md`, another rule, or a skill.
- Do not link to other `ow-cursor-config/skills/*` skills.

## Principles

0. Treat the `.mdc` as the unit. If the same directory contains a clearly paired sibling (for example `reference-*.md` linked from the rule), include it in the audit; otherwise scope stays on the one file.
1. Do not drop requirements. Relocate or compress them instead.
2. Keep one canonical home per policy: rule, skill, or `AGENTS.md`.
3. Keep the rule body procedural and scannable; deep reference belongs in a sibling file only one hop away when the rule truly needs it.
4. Use verifiable checks over advice.
5. Preserve user-supplied canonical wording verbatim when it exists.

## Rule artifact types

Classify everything in scope before editing.

| Type | Examples | Improvement intent |
|------|----------|-------------------|
| Rule entry | `*.mdc` | Correct frontmatter; lean body; one concern |
| Paired reference | `reference-*.md` linked from the rule | Dense; trim unused content; verify cited sections are used |
| Index / human doc | `README.md` in rules folder | Human-only; must not contradict the live rules |

## Workflow

0. Confirm the target path is a `.mdc` file and note any same-directory siblings the rule links to.
1. If a workspace root exists, read `AGENTS.md`, files under `.cursor/rules/`, and nearby skills for overlap; also check `~/.cursor/rules/` for a user-scope rule on the same topic (`CR-SCOPE-LAYER`). If no workspace, ask once whether to skip overlap or which repo to treat as root.
2. Confirm the target path is unambiguous and no rename is requested before writing anything.
3. Audit the target and any linked sibling in scope.
   - **Frontmatter and activation:**
     - Verify `description`, `globs`, and `alwaysApply` match intent and each other.
     - `description` must be **one physical line** — no YAML `>-`, `|`, or indented continuations (`CR-DESC-SINGLE-LINE`). Cursor Settings may show `>-` as the rule name and break intelligent apply.
     - Dead rule check: `alwaysApply: false` + no `globs` and no meaningful `description` = never fires (`CR-DEAD-RULE`). `alwaysApply: false` with a one-line `description` and no `globs` = apply intelligently in Cursor.
     - Glob precision: state one path that should match and one that should not (`CR-GLOB-PRECISION`).
     - Picker label: `description` must read as a clear one-liner in the rule picker (`CR-DESC-PICKER`).
   - **Always-on budget:** list all `alwaysApply: true` rules in the same directory; sum line counts; flag if total is disproportionate (`CR-ALWAYS-ON-BUDGET`).
   - **Inter-rule conflicts:** list rules simultaneously active with the target; check for overlap or contradiction; confirm one canonical home per policy (`CR-INTER-RULE-CONFLICT`).
   - **Body:** split if multiple unrelated concerns; replace vague guidance with executable checks.
   - Apply `CR-RULE-NO-ORPHANS`, `CR-RULE-REFS-EXIST`, `CR-RULE-SIBLINGS-LEAN` when siblings exist.
4. Rewrite the target `.mdc` toward a common spine: when the rule applies, what the agent must do, what it must not do, then ordered checks or steps.
5. When the frontmatter `description` summarises long workflow steps, compress it to trigger-oriented wording and move detail into the body (or a one-hop sibling). Keep `description` on **one line** — never use YAML block/folded scalars (`CR-DESC-SINGLE-LINE`).
6. For each linked sibling, either keep as-is, tighten, relocate content back into the rule, or mark for removal with explicit rationale. Do not silently drop requirements.
7. If the rule is discipline-enforcing, add or refresh an `Excuse → Reality` table for loopholes the agent might rationalize.
8. Deliver the post-change report using `reference-report-skeleton.md`.

## Editing rules

- Use verb-led edits and concrete replacements.
- Match specificity to fragility: text for contextual choices, exact commands only when the step is fragile.
- If removing content, relocate or compress it instead of deleting silently.
- Preserve one-level links from the rule to any sibling reference files.
- When the body exceeds the line budget, choose split strategy: **sibling reference file** (one rule, one activation) for detail that can live one hop away; **true rule split** (two `.mdc` files, separate activations) only when fragments have genuinely distinct scopes — assign narrower globs per fragment accordingly.

## Output format

Use `reference-report-skeleton.md` for the report structure.

## Additional resources

- [reference-cursor-rule-authoring-norms.md](reference-cursor-rule-authoring-norms.md)
- [reference-report-skeleton.md](reference-report-skeleton.md)
- [reference-examples.md](reference-examples.md)
