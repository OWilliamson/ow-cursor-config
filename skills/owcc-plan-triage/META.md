# Meta

- **Version:** 2.1.0
- **Updated:** 2026-08-04T13:45:00Z
- **Maintainer:** <github-user>

## Directory tree

```
owcc-plan-triage/
  SKILL.md       # Master spine §1–7; procedural workflow
  DECISIONS.md   # Target, harvest, severity, axes, patch
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
- Do NOT add OUTPUTS.md unless this skill starts writing a structured file artifact (plan patches stay IN the plan file; chat stays IN RESPONSE).
- Archive superseded files to a timestamped copy outside this package before delete.
- Visibility changes: `/change-config-visibility` (operator). Do not hand-move between `private/` and `public/`. Package edits do not require reconcile, kit install, or publish.

## Scripts

None in this package.

## References

Operator chain docs live outside this package. This package does not prescribe sibling skill invokes.

### Reference To

None (target-plan matrix lives IN this package’s DECISIONS).
