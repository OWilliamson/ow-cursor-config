---
name: cursor-validate-skill
description: >-
  Validates a full Cursor skill package with read-only checks, norm-ID findings,
  and a chat report. Use when checking SKILL.md plus sibling references, templates,
  and scripts for authoring-norm issues before shipping a skill.
disable-model-invocation: true
---

# Validate Cursor skills

This skill is explicit-only. Invoke it with `/cursor-validate-skill` or `@cursor-validate-skill`.

## When to use

- The user wants a skill package checked for authoring quality before shipping.
- The skill should be read-only and report findings in chat.
- The goal is to verify full-package structure, wording, links, token budget, and hygiene.

## Required inputs

- **Target**: absolute path to the skill directory, or a full pasted skill package.
- **Scope** (if unclear): full pass is default.

## Definition of done

- The target package has been checked against `reference-cursor-authoring-norms.md`.
- Findings are reported with norm IDs and severity labels.
- Passing checks are acknowledged.
- Any speculative items are explicitly marked.
- The output follows `reference-report-skeleton.md`.

## Non-goals

- Do not modify the target package.
- Do not rewrite the target skill for style or clarity.
- Do not run improve-style refactors.

## Principles

0. Treat the package as the unit, not `SKILL.md` alone. Every file in the directory is in scope.
1. Use verifiable checks (binary pass/fail) over advisory notes.
2. Acknowledge passing checks explicitly; do not omit them silently.
3. Mark mechanically unconfirmed findings as speculative.

## Package member types

Classify every file in the package before evaluating it.

| Type | Examples | What to check |
|------|----------|---------------|
| Entry point | `SKILL.md` | Procedural spine; lean; all norm checks apply |
| Reference doc | `reference-*.md`, `reference.md` | All sections cited from `SKILL.md`; no unused bulk |
| Template | `*-skeleton.md`, `REPORT_TEMPLATE.md` | Output shape matches current workflow; no stale placeholders |
| Workflow doc | `WORKFLOW.md`, `agent-build-plan-notes.md` | Does not contradict `SKILL.md` |
| Checklist | `CHECKLIST.md`, `reference-checklist.md` | Items are actionable checks, not essays |
| Examples | `EXAMPLES.md` | Examples match current norms |
| Script | `scripts/*.py`, `scripts/*.sh` | Cited in `SKILL.md`; deps documented; execute-vs-read stated |
| README | `README.md` | Human-only; check for drift from `SKILL.md` |

## Workflow

1. Confirm the target path and list the package contents.
2. Inventory all files in the target directory and classify each as cited, generated, or orphaned.
3. Read every package member by type (see Package member types table).
   - **Reference docs:** verify all sections are cited from `SKILL.md`; flag unused bulk.
   - **Templates:** verify output shape matches current workflow; flag stale placeholders.
   - **Scripts:** read every script file; confirm it is cited in `SKILL.md`, check for dependency notes, and verify execute-vs-read guidance is stated. Apply `CS-PKG-SCRIPTS-DOCUMENTED`.
   - **Workflow/checklist docs:** check items don't contradict `SKILL.md`.
   - Apply `CS-PKG-NO-ORPHANS`, `CS-PKG-REFS-EXIST`, `CS-PKG-SIBLINGS-LEAN` across all members.
4. Run the norm checks from `reference-cursor-authoring-norms.md` across the whole package, not only `SKILL.md`.
5. Label findings Critical, Suggestion, or Nice to have.
6. Mark unconfirmed findings as speculative.
7. End with a final sanity pass before reporting.

## Check handling

- Use `wc -l`, `python3 -c`, `basename`, and link resolution checks as needed. For `CS-WORDS-*`, use the frontmatter-excluding command from `reference-cursor-authoring-norms.md`.
- Keep link checks scoped to paths cited directly from `SKILL.md`.
- Flag orphaned sibling files with `CS-PKG-NO-ORPHANS`.
- Flag missing referenced files with `CS-PKG-REFS-EXIST`.
- For scripts, enforce `CS-PKG-SCRIPTS-DOCUMENTED`.
- For sibling references/templates, enforce `CS-PKG-SIBLINGS-LEAN`.
- Acknowledge passes explicitly.
- Cap detailed findings at seven; list remaining norm IDs only.

## Output format

Use `reference-report-skeleton.md` for the report structure.

## Additional resources

- [reference-cursor-authoring-norms.md](reference-cursor-authoring-norms.md)
- [reference-report-skeleton.md](reference-report-skeleton.md)
- [reference-examples.md](reference-examples.md)
