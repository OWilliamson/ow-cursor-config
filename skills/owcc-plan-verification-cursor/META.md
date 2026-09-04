# Meta

- **Version:** 2.1.0
- **Updated:** 2026-08-04T13:45:00Z
- **Maintainer:** <github-user>

## Directory tree

```
owcc-plan-verification-cursor/
  SKILL.md       # Master spine §1–7; procedural workflow
  DECISIONS.md   # Target, placement, frontmatter, closeout-gap check vs verify
  RESPONSE.md    # Chat completion template (§7)
  OUTPUTS.md     # Closeout inject templates
  VALIDATION.md  # Completion rubric (§6)
  META.md        # This file — maintainer only; never linked from SKILL
  WORKFLOW.yaml  # Machine mirror of SKILL §5.3 (required)
  scripts/       # Closeout-gap check, frontmatter, build-time closeout helpers
```

## Update rules

- Do **not** link or cite META.md from SKILL.md.
- Keep semantic role names stable (`DECISIONS`, `RESPONSE`, `OUTPUTS`, `VALIDATION`, `META`, `WORKFLOW.yaml`).
- Keep `WORKFLOW.yaml` IN sync with SKILL §5.3 step ids whenever the workflow changes.
- Do NOT reintroduce live `reference-*.md` — substance lives IN DECISIONS / OUTPUTS / VALIDATION.
- Keep invoke-time vs build-time script separation explicit IN META Scripts table.
- Archive superseded files to a timestamped copy outside this package before delete.
- Visibility changes: `/change-config-visibility` (operator). Do not hand-move between `private/` and `public/`. Package edits do not require reconcile, kit install, or publish.

## Scripts

| Script | Workflow stage | Input type | Expected inputs | Output shape |
|--------|----------------|------------|-----------------|--------------|
| `scripts/plan-audit-cursor-verification.py` | 5.3.2 / 5.3.5 | Agent-execute (invoke) | `--json` + `.plan.md` path | JSON gaps / ok |
| `scripts/plan-validate-frontmatter.py` | 5.3.4 | Agent-execute (invoke) | `.plan.md` path | Exit 0/1 |
| `scripts/plan-verify-close-cursor.py` | build closeout | Build-agent-execute (named IN todos) | `--json` + path | JSON stdout |
| `scripts/plan-registry-show.py` | build closeout | Build-agent-execute (named IN todos) | `--json` + path | JSON stdout |
| `scripts/plan_registry_lib.py` | (library) | Agent-read / import | — | Registry helpers |

## References

Operator chain docs live outside this package. This package does not prescribe sibling skill invokes.

### Reference To

| Path | Relationship |
|------|----------------|
| `~/.cursor/skills/owcc-plan-validation-report/scripts/plan_lib.py` | Shared parse helpers via script imports where used |
