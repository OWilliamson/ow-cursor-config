# Meta

- **Version:** 2.1.1
- **Updated:** 2026-07-29T10:35:00Z
- **Maintainer:** <github-user>

## Directory tree

```
owcc-skill-improve/
  SKILL.md       # Master spine §1–7; procedural workflow
  DECISIONS.md   # Branching matrices for improve runs
  RESPONSE.md    # Chat completion template (§7)
  OUTPUTS.md     # Skill-package role contracts (target shape)
  VALIDATION.md  # Completion rubric + CS-* norms (§6)
  META.md        # This file — maintainer only; never linked from SKILL
  EXAMPLES.md    # Sparse before/after examples
  WORKFLOW.yaml  # Machine mirror of SKILL §5.3 (required)
```

## Update rules

- Do **not** link or cite META.md from SKILL.md (workflow, Additional resources, or otherwise).
- Keep semantic role names stable (`DECISIONS`, `RESPONSE`, `OUTPUTS`, `VALIDATION`, `META`, `EXAMPLES`, `WORKFLOW.yaml`).
- Keep `WORKFLOW.yaml` IN sync with SKILL §5.3 step ids whenever the workflow changes.
- `owcc-skill-validate` consumes this package’s `VALIDATION.md` as the sole CS-* source (read-only wrapper). Do **not** copy norms into validate. Keep META References IN sync when adding peer consumers or peer citations.
- Archive superseded files to a timestamped copy outside this package before delete.
- Visibility changes: `/change-config-visibility` (operator). Do not hand-move between `private/` and `public/`. Package edits do not require reconcile, kit install, or publish.

## Scripts

| Script | Workflow stage | Input type | Expected inputs | Output shape |
|--------|----------------|------------|-----------------|--------------|
| — | — | — | — | — |

No `scripts/` directory IN this package. Mechanical checks are agent-run shell one-liners documented IN VALIDATION.md.

## References

### Referenced From

| Skill | Relationship |
|-------|----------------|
| `owcc-skill-validate` | Read-only wrapper; RUNs this package’s VALIDATION.md |
| `owcc-skill-modify` | Recommends this skill when target META/shape missing |
| `owcc-context-compress` | Suggests `/owcc-skill-improve` after structural fixes |
| `owcc-tooling-help` | Tool picker routes refactor skill packages here |

### Reference To

| Skill / path | Relationship |
|--------------|----------------|
| — | — |
