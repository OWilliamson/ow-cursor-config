# Meta

- **Version:** 1.1.0
- **Updated:** 2026-07-29T10:48:00Z
- **Maintainer:** <github-user>

## Directory tree

```
owcc-skill-modify/
  SKILL.md       # Master spine §1–7; procedural modify workflow
  DECISIONS.md   # Target, META+WORKFLOW gate, change class, alignment, reshape, maintainer sync
  RESPONSE.md    # Chat completion + hard-stop templates (§7)
  VALIDATION.md  # Modify-run rubric + Critical MOD-* checks (§6)
  META.md        # This file — maintainer only; never linked from SKILL
  EXAMPLES.md    # Sparse invoke / gate / alignment / sync examples
  WORKFLOW.yaml  # Machine mirror of SKILL §5.3 (required)
```

## Update rules

- Do **not** link or cite META.md from SKILL.md.
- Keep semantic role names stable (`DECISIONS`, `RESPONSE`, `VALIDATION`, `META`, `EXAMPLES`, `WORKFLOW.yaml`).
- Keep `WORKFLOW.yaml` IN sync with SKILL §5.3 step ids whenever the workflow changes.
- After any modify-run edit to other package files, refresh this META (tree/References/Updated as needed) AND verify WORKFLOW sync — see SKILL 5.3.7 / DECISIONS §7.
- Do **not** copy the full CS-* table from `owcc-skill-improve`; point operators at `/owcc-skill-validate` for deep audits.
- Keep META References IN sync when peer consumers or peer citations change.
- Archive superseded files to a timestamped copy outside this package before delete.
- Visibility changes: `/change-config-visibility` (operator). Do not hand-move between `private/` and `public/`. Package edits do not require reconcile, kit install, or publish.

## Scripts

| Script | Workflow stage | Input type | Expected inputs | Output shape |
|--------|----------------|------------|-----------------|--------------|
| — | — | — | — | — |

No `scripts/` directory IN this package. Mechanical checks are agent-run commands documented IN VALIDATION.md.

## References

### Referenced From

| Skill | Relationship |
|-------|----------------|
| — | — |

### Reference To

| Skill / path | Relationship |
|--------------|----------------|
| `../owcc-skill-improve/` | Prerequisite reshape tool; recommended when META/WORKFLOW/shape missing |
| `../owcc-skill-validate/` | Optional deep CS-* audit after modify |
