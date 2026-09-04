# Meta

- **Version:** 1.1.0
- **Updated:** 2026-09-04T11:20:00Z
- **Maintainer:** <github-user>

## Directory tree

```
owcc-prose-strip-tropes/
  SKILL.md       # Master spine §1–7; check → rewrite → residue rescan
  DECISIONS.md   # Target, mode, preserve, C1–C15, cluster severity, rewrite limits
  RESPONSE.md    # Chat completion template (§7)
  VALIDATION.md  # Completion rubric (§6)
  META.md        # This file — maintainer only; never linked from SKILL
  WORKFLOW.yaml  # Machine mirror of SKILL §5.3 (required)
```

## Update rules

- Do **not** link or cite META.md from SKILL.md.
- Keep semantic role names stable (`DECISIONS`, `RESPONSE`, `VALIDATION`, `META`, `WORKFLOW.yaml`).
- Keep `WORKFLOW.yaml` IN sync with SKILL §5.3 step ids whenever the workflow changes.
- Do NOT reintroduce live `reference-*.md` — substance lives IN DECISIONS / VALIDATION / RESPONSE.
- Do NOT add OUTPUTS.md unless this skill starts writing a separate structured artifact file (rewrites stay IN the target file or chat RESPONSE).
- Dated lexicon snapshot lives IN DECISIONS §4; re-date when model fashion moves. Do NOT promote seeds into always-on hub rules or identity files.
- Archive superseded files to a timestamped copy outside this package before delete.
- Visibility changes: `/change-config-visibility` only — do not hand-move between `private/` and `public/`.
- Package edits do not require kit install. Refresh the installed profile copy when the operator wants it updated.

## Scripts

| Script | Workflow stage | Input type | Expected inputs | Output shape |
|--------|----------------|------------|-----------------|--------------|
| — | — | — | — | — |

No `scripts/` directory IN this package.

## References

Identity stance may prefer plain peer prose; this skill is the thorough pass. Do not require identity to link here.

### Referenced From

| Skill | Relationship |
|-------|----------------|
| — | — |

### Reference To

| Skill / path | Relationship |
|--------------|----------------|
| `topics/llm-output-tropes/deepdive.md` | Optional workspace overlay for dated inventory (DECISIONS §4); not required at install |
