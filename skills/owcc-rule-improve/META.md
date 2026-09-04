# Meta

- **Version:** 2.0.0
- **Updated:** 2026-07-25T02:30:00Z
- **Maintainer:** <github-user>

## Directory tree

```
owcc-rule-improve/
  SKILL.md       # Master spine §1–7; procedural workflow
  DECISIONS.md   # Branching matrices for improve runs
  RESPONSE.md    # Chat completion template (§7)
  OUTPUTS.md     # Target .mdc spine + section contracts
  VALIDATION.md  # Completion rubric + CR-* norms (§6)
  META.md        # This file — maintainer only; never linked from SKILL
  EXAMPLES.md    # Sparse before/after activation examples
  WORKFLOW.yaml  # Machine mirror of SKILL §5.3 (required)
```

## Update rules

- Do **not** link or cite META.md from SKILL.md (workflow, Additional resources, or otherwise).
- Keep semantic role names stable (`DECISIONS`, `RESPONSE`, `OUTPUTS`, `VALIDATION`, `META`, `EXAMPLES`, `WORKFLOW.yaml`).
- Keep `WORKFLOW.yaml` IN sync with SKILL §5.3 step ids whenever the workflow changes.
- This package owns the canonical CR-* table IN `VALIDATION.md`. Prefer rewriting `owcc-rule-validate` as a read-only wrapper that RUNs this VALIDATION.md (same pattern as skill validate→improve). Until then, keep any vendored norms copy IN sync manually.
- Do NOT reintroduce live `reference-*.md` — substance lives IN OUTPUTS / RESPONSE / VALIDATION / EXAMPLES.
- Archive superseded files to a timestamped copy outside this package before delete.
- Visibility changes: `/change-config-visibility` (operator). Do not hand-move between `private/` and `public/`. Package edits do not require reconcile, kit install, or publish.

## Scripts

| Script | Workflow stage | Input type | Expected inputs | Output shape |
|--------|----------------|------------|-----------------|--------------|
| — | — | — | — | — |

No `scripts/` directory IN this package. Mechanical checks are agent-run shell one-liners documented IN VALIDATION.md. Optional external: `npx cursor-doctor budget` for always-on token precision.

## References

### Referenced From

| Skill | Relationship |
|-------|----------------|
| `owcc-rule-validate` | Should become read-only wrapper over this VALIDATION.md (currently vendors a norms copy) |
| `owcc-context-compress` | Suggests `/owcc-rule-validate` after compression; pairs with this improve path |
| `owcc-tooling-help` | Tool picker routes rule refactor here |

### Reference To

| Skill / path | Relationship |
|--------------|----------------|
| — | — |
