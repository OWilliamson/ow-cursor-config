# Cursor skill authoring norms

Vendored from Cursor create-skill; last synced 2026-05-12.

These norms are the canonical master for `cursor-validate-skill`, and copied byte-identically into `cursor-improve-skill` and `cursor-test-skill`.

## Principles

- Verifiable checks (binary pass/fail) are preferred over advisory notes.
- Mechanical checks confirm structure; behavioural effectiveness requires a pressure test in a fresh session.
- Keep `SKILL.md` procedural, with deeper reference in sibling files only one hop away.
- Maintain one term per concept throughout; avoid synonym drift.
- Do not let descriptions summarize workflow steps; descriptions should describe when to use the skill.

## Norm IDs

| Norm ID | Check | Severity default |
|---------|-------|-----------------|
| `CS-NAME-FOLDER` | `name` field matches folder basename | Critical |
| `CS-DESC-LEN` | `description` char count under 1024 | Critical |
| `CS-DESC-WHEN` | description starts with "Use when" or equivalent trigger form; not first-person | Suggestion |
| `CS-DESC-WORKFLOW-SUMMARY` | description does not summarise skill's own workflow steps (agent may follow description instead of reading body) | Critical |
| `CS-DESC-BODY-ALIGN` | description claims match what the body actually instructs | Critical |
| `CS-LINES-500` | `wc -l SKILL.md` under 500 | Suggestion |
| `CS-WORDS-FREQ` | if `disable-model-invocation` omitted or false: body word count (frontmatter excluded) under 200 | Suggestion |
| `CS-WORDS-GENERAL` | if `disable-model-invocation: true`: body word count (frontmatter excluded) under 500 for single-task skills; under 900 for multi-step workflow skills (5+ ordered steps in the Workflow section) | Suggestion |
| `CS-DISABLE-INTENT` | `disable-model-invocation` value matches skill length and niche intent | Suggestion |
| `CS-LINKS-ONE-HOP` | all links in `SKILL.md` body resolve within package; no file→file→file chains | Suggestion |
| `CS-NO-FORCE-LOAD` | no `@path` links in body unless intentionally force-loaded | Suggestion |
| `CS-PATHS-SCOPE` | file-type-specific skills declare `paths` glob in frontmatter | Nice to have |
| `CS-PORTABLE-PATHS` | no absolute personal paths (`~/.cursor/...`) that break for other installers | Suggestion |
| `CS-SCRIPT-SAFETY` | `scripts/` (if present) has no network calls or raw shell with user-supplied input | Critical |
| `CS-PKG-NO-ORPHANS` | non-generated files in the package are cited from `SKILL.md` or explicitly marked archive/deprecated | Suggestion |
| `CS-PKG-REFS-EXIST` | every file referenced by `SKILL.md` exists within the package | Critical |
| `CS-PKG-SCRIPTS-DOCUMENTED` | each script has dependency notes and explicit execute-vs-read guidance | Suggestion |
| `CS-PKG-SIBLINGS-LEAN` | sibling reference/template files are single-purpose and avoid unused bulk content | Suggestion |
| `CS-ANTI-WIN-PATHS` | no Windows-style backslash paths in docs or scripts | Suggestion |
| `CS-TERMINOLOGY` | one term per concept throughout; no synonym drift | Suggestion |
| `CS-NO-TIME-BOMBS` | no time-sensitive phrases ("before August 2025...") unless in a dated legacy section | Suggestion |

## Frontmatter and description guidance

- `name` must stay lowercase with hyphens only, under 64 characters.
- `description` must be third person and answer "when should the agent use this skill?"
- For explicit-only skills, `disable-model-invocation: true` is appropriate when the skill is long, narrow, or purposefully invoked.
- For discoverable skills, omit the flag or set it false only when soft discovery is desired.
- If the skill is clearly file-type-specific, consider `paths` scope as a nice-to-have.

## Structure guidance

- Opening sections should state when to use, required inputs, definition of done, and non-goals.
- Workflows should be ordered by dependency.
- Checklists should be action or verify rows, not essays.
- Main files should stay lean; long detail belongs in sibling reference files or scripts.
- Avoid deep chains of linked files.

## Validation checks

- Run `wc -l SKILL.md`.
- For word-count norms, exclude frontmatter: `python3 -c "import re,sys; t=open('SKILL.md').read(); print(len(re.sub(r'^---\n.*?\n---\n','',t,1,re.DOTALL).split()))" `
- For `CS-WORDS-GENERAL` tier: count ordered steps in the `## Workflow` section; 5+ steps → 900-word budget, otherwise 500.
- Use `python3 -c "print(len(...))"` or similar for description length checks.
- Compare `name` to folder basename.
- Inventory all sibling files in the package and classify each as cited, generated, or orphaned.
- Verify every link cited from `SKILL.md` resolves inside the package.
- Flag any `@path` links in the body unless they are intentionally force-loaded.
- For scripts, verify dependency names are explicitly documented.

## Reporting rules for validate

- Give every finding a severity label: Critical, Suggestion, or Nice to have.
- Mark mechanically unconfirmed findings as speculative and state the confirming evidence needed.
- Acknowledge passes explicitly; do not omit checks silently.
- Keep detailed findings capped; if there are more, list remaining norm IDs only.
- End with a final sanity pass: only flag items that are actually worth fixing.
