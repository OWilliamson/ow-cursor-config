# Validate skill — examples

## Example: Completed findings report

### Input package

`~/.cursor/skills/git-commit/` — two files: `SKILL.md`, `reference.md`.

### Filled-in report

---

**Target:** `~/.cursor/skills/git-commit/`

**Inventory:**

| File | Type | Status |
|------|------|--------|
| SKILL.md | Entry point | Cited |
| reference.md | Reference doc | Cited from Additional resources |

**Executive pass/fail:** Conditional pass — one Critical finding must be resolved before shipping.

**Findings table:**

| Norm ID | Severity | Evidence | Minimal fix |
|---------|----------|----------|-------------|
| `CS-DESC-WORKFLOW-SUMMARY` | Critical | description says "runs git log, formats message, stages files" — these are internal steps | Rewrite to trigger form: "Use when writing a commit message or reviewing staged changes." |
| `CS-LINES-500` | Suggestion | `wc -l SKILL.md` → 312. Under budget. | — |
| `CS-WORDS-GENERAL` | Suggestion | Body word count → 487. Under 500 (single-task skill). | — |

**Passing checks:** CS-NAME-FOLDER ✓, CS-FRONTMATTER ✓, CS-DESC-LEN ✓, CS-DESC-BODY-ALIGN ✓, CS-DISABLE-INTENT ✓, CS-LINKS-ONE-HOP ✓, CS-PKG-REFS-EXIST ✓, CS-PKG-NO-ORPHANS ✓, CS-ANTI-WIN-PATHS ✓, CS-TERMINOLOGY ✓, CS-NO-TIME-BOMBS ✓.

**Speculative items:**

| Item | What would confirm it |
|------|----------------------|
| `CS-PORTABLE-PATHS`: body references `~/.gitconfig` | Confirm this is operational guidance rather than an install path |

**Follow-up question:** None.

---

## Notes on filling in the findings table

- **Evidence**: quote or cite the exact text that triggers the finding; do not paraphrase.
- **Minimal fix**: state the smallest change that clears the norm; do not over-prescribe.
- **Speculative**: mark anything you cannot confirm mechanically (file content not read, path not resolved, etc.) as speculative and state what would confirm it.
