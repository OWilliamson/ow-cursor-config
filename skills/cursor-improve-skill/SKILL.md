---
name: cursor-improve-skill
description: >-
  Refactors full Cursor skill packages into a leaner, clearer, less drift-prone
  shape before shipping. Use when improving SKILL.md plus sibling references,
  templates, and scripts under ~/.cursor/skills or .cursor/skills.
disable-model-invocation: true
---

# Improve Cursor skills

This skill is explicit-only. Invoke it with `/cursor-improve-skill` or `@cursor-improve-skill`.

## When to use

- The user wants a skill sharper, shorter, or less misfire-prone before or after shipping it.
- The skill has grown long, duplicated, vague, or inconsistent with its description.
- The user wants the package refactored, not just reviewed.

## Required inputs

- **Target**: absolute path to the skill directory whose package should change.
- **Scope** (if unclear): default to full pass.

## Definition of done

- The target package has been rewritten toward the shared spine in this file.
- `reference-cursor-authoring-norms.md` has been applied and checked.
- A post-change report is prepared using `reference-report-skeleton.md`.
- Mechanical improvement is complete. Behavioural effectiveness is not guaranteed without a pressure test in a fresh session.

## Non-goals

- Do not change the target skill’s domain behaviour unless the user asked.
- Do not rename `name:` or the folder unless the user explicitly requested a rename.
- Do not keep duplicate long prose that already belongs in a sibling file or a repo rule.
- Do not link to other `ow-cursor-config/skills/*` skills.

## Principles

0. Treat the package as the unit, not `SKILL.md` alone. Every file in the directory is in scope.
1. Do not drop requirements. Relocate or compress them instead.
2. Keep one canonical home per policy: skill, rule, or AGENTS.md.
3. Keep `SKILL.md` procedural; deep reference lives in sibling files only one hop away.
4. Use verifiable checks over advice.
5. Preserve user-supplied canonical wording verbatim when it exists.

## Package member types

Classify every file in the package before deciding what to do with it.

| Type | Examples | Improvement intent |
|------|----------|-------------------|
| Entry point | `SKILL.md` | Procedural spine; lean and readable in one pass |
| Reference doc | `reference-*.md`, `reference.md` | Dense; trim unused content; verify all sections are cited |
| Template | `*-skeleton.md`, `REPORT_TEMPLATE.md` | Align output shape with current workflow; remove stale placeholders |
| Workflow doc | `WORKFLOW.md`, `agent-build-plan-notes.md` | Must not contradict `SKILL.md`; merge if short enough |
| Checklist | `CHECKLIST.md`, `reference-checklist.md` | Verify items are actionable checks, not essays |
| Examples | `EXAMPLES.md` | Verify examples match current norms; prune outdated ones |
| Script | `scripts/*.py`, `scripts/*.sh` | Read and verify: runnable? deps documented? still referenced? |
| README | `README.md` | Human-only; check for drift from `SKILL.md` |

## Workflow

0. Confirm the target directory and list sibling support files.
1. If a workspace root exists, read `AGENTS.md`, `.cursor/rules`, and nearby skills for overlap. If no workspace exists, ask once whether to skip overlap or which repo to treat as root.
2. Confirm target path is unambiguous and no rename is requested before writing anything.
3. Audit every package member by type (see Package member types table).
   - List all files including any `scripts/` subdirectory.
   - Classify each by type, then apply the improvement intent for that type.
   - **Reference docs:** read each; flag sections not cited or exercised by the workflow.
   - **Templates:** verify the output shape matches what the current workflow produces; remove stale placeholders.
   - **Scripts:** read every script file; confirm it is referenced in `SKILL.md`, note its dependencies, and note whether it is agent-executed or human-executed. Apply `CS-PKG-SCRIPTS-DOCUMENTED`.
   - **Workflow/checklist docs:** verify items don't contradict `SKILL.md` and are not stale duplicates.
   - **Examples:** check that examples reflect current norms, not superseded patterns.
   - Apply `CS-PKG-NO-ORPHANS`, `CS-PKG-REFS-EXIST`, `CS-PKG-SIBLINGS-LEAN` across all members.
4. Rewrite the target `SKILL.md` toward the common spine: when to use, required inputs, definition of done, non-goals, then workflow.
5. When the description summarises workflow steps, rewrite it to trigger-only wording and move workflow summary into the body.
6. For each sibling file, either keep as-is, tighten, relocate, or mark for removal with explicit rationale. Do not silently drop requirements.
7. If the target skill is discipline-enforcing, suggest an `Excuse → Reality` table for loopholes the agent might rationalize.
8. For each script in `scripts/`: (a) trim dead code and unused imports; (b) ensure a comment block at the top states purpose, dependencies, and whether the agent should execute or only read it; (c) ensure `SKILL.md` cites it by name with the same execute-vs-read guidance.
9. Deliver the post-change report using `reference-report-skeleton.md`.

## Editing rules

- Use verb-led edits and concrete replacements.
- Match specificity to fragility: text for contextual choices, exact commands or scripts for fragile steps.
- If removing content, relocate or compress it instead of deleting silently.
- Preserve one-level file references.
- Keep the target package lean enough to read in one pass.

## Output format

Use `reference-report-skeleton.md` for the report structure.

## Additional resources

- [reference-cursor-authoring-norms.md](reference-cursor-authoring-norms.md)
- [reference-report-skeleton.md](reference-report-skeleton.md)
- [reference-examples.md](reference-examples.md)
