# Meta

- **Version:** 2.0.0
- **Updated:** 2026-07-25T01:30:00Z
- **Maintainer:** <github-user>

## Directory tree

```
owcc-skill-validate/
  SKILL.md       # Master spine §1–7; read-only wrapper workflow
  DECISIONS.md   # Target, shape policy, question filter
  RESPONSE.md    # Chat report template (§7)
  VALIDATION.md  # Thin overrides; points at improve VALIDATION
  META.md        # This file — maintainer only; never linked from SKILL
  WORKFLOW.yaml  # Machine mirror of SKILL §5.3 (required)
```

## Update rules

- Do **not** link or cite META.md from SKILL.md.
- Keep semantic role names stable (`DECISIONS`, `RESPONSE`, `VALIDATION`, `META`, `WORKFLOW.yaml`).
- Keep `WORKFLOW.yaml` IN sync with SKILL §5.3 step ids whenever the workflow changes.
- Do **not** copy CS-* tables into this package; consume `../owcc-skill-improve/VALIDATION.md`.
- Keep META References IN sync when peer consumers or peer citations change.
- Archive superseded files to a timestamped copy outside this package before delete.
- Visibility changes: `/change-config-visibility` (operator). Do not hand-move between `private/` and `public/`. Package edits do not require reconcile, kit install, or publish.

## Scripts

| Script | Workflow stage | Input type | Expected inputs | Output shape |
|--------|----------------|------------|-----------------|--------------|
| — | — | — | — | — |

No `scripts/` directory IN this package. Mechanical checks are agent-run commands from improve VALIDATION.md.

## References

### Referenced From

| Skill | Relationship |
|-------|----------------|
| `owcc-context-compress` | Suggests `/owcc-skill-validate` after compression |
| `owcc-skill-modify` | May recommend deep CS-* audit after surgical edits |
| `owcc-tooling-help` | Tool picker routes read-only skill audit here |

### Reference To

| Skill / path | Relationship |
|--------------|----------------|
| `../owcc-skill-improve/VALIDATION.md` | Sole CS-* / shape norms source (read-only RUN) |
| `../owcc-skill-improve/` | Peer package; wrapper consumer relationship |
