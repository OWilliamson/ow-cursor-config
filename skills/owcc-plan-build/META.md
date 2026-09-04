# Meta

- **Version:** 2.1.0
- **Updated:** 2026-08-04T13:45:00Z
- **Maintainer:** <github-user>

## Directory tree

```
owcc-plan-build/
  SKILL.md       # Master spine §1–7; procedural workflow
  DECISIONS.md   # Preflight, intents, layers, execution, native pairing
  RESPONSE.md    # Chat completion template (§7)
  VALIDATION.md  # Completion rubric (§6)
  META.md        # This file — maintainer only; never linked from SKILL
  EXAMPLES.md    # Sparse invoke samples
  WORKFLOW.yaml  # Machine mirror of SKILL §5.3 (required)
  scripts/       # plan-validate-close.py (complete intent)
```

## Update rules

- Do **not** link or cite META.md from SKILL.md.
- Keep semantic role names stable (`DECISIONS`, `RESPONSE`, `VALIDATION`, `META`, `EXAMPLES`, `WORKFLOW.yaml`).
- Keep `WORKFLOW.yaml` IN sync with SKILL §5.3 step ids whenever the workflow changes.
- Do NOT reintroduce live `reference-*.md` — substance lives IN DECISIONS / EXAMPLES / VALIDATION.
- Do NOT add OUTPUTS.md unless this skill starts writing a structured file artifact beyond plan YAML status / Plan build line.
- Archive superseded files to a timestamped copy outside this package before delete.
- Visibility changes: `/change-config-visibility` (operator). Do not hand-move between `private/` and `public/`. Package edits do not require reconcile, kit install, or publish.

## Scripts

| Script | Workflow stage | Input type | Expected inputs | Output shape |
|--------|----------------|------------|-----------------|--------------|
| `scripts/plan-validate-close.py` | 5.3.4 / §6 | Agent-execute | plan path; optional `--json` | Exit 0/1; optional JSON |
| `~/.cursor/skills/owcc-plan-verification-cursor/scripts/plan-verify-close-cursor.py` | when named IN todo | Peer-execute | `--json` + `.plan.md` | JSON stdout |
| `~/.cursor/skills/owcc-plan-verification-cursor/scripts/plan-registry-show.py` | when named IN todo | Peer-execute | `--json` + `.plan.md` | JSON stdout |

## References

Operator chain docs live outside this package. This package does not prescribe sibling skill invokes.

### Reference To

| Path | Relationship |
|------|----------------|
| Workspace `.cursor/plans/reports/<plan-name>.validation.json` | Non-`.plan.md` preflight artifact contract |
| `~/.cursor/skills/owcc-plan-verification-cursor/scripts/plan-verify-close-cursor.py` | Peer closeout when named IN todos |
| `~/.cursor/skills/owcc-plan-verification-cursor/scripts/plan-registry-show.py` | Peer registry when named IN todos |
