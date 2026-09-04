# Meta

- **Version:** 2.1.1
- **Updated:** 2026-08-04T14:05:00Z
- **Maintainer:** <github-user>

## Directory tree

```
owcc-plan-improve/
  SKILL.md       # Master spine §1–7; procedural workflow
  DECISIONS.md   # Branching matrices for improve runs
  RESPONSE.md    # Chat completion template (§7)
  OUTPUTS.md     # Plan file template + section contracts
  VALIDATION.md  # Completion rubric (§6)
  META.md        # This file — maintainer only; never linked from SKILL
  WORKFLOW.yaml  # Machine mirror of SKILL §5.3 (required)
```

## Update rules

- Do **not** link or cite META.md from SKILL.md (workflow, Additional resources, or otherwise).
- Keep semantic role names stable (`DECISIONS`, `RESPONSE`, `OUTPUTS`, `VALIDATION`, `META`, `WORKFLOW.yaml`).
- Keep `WORKFLOW.yaml` IN sync with SKILL §5.3 step ids whenever the workflow changes.
- Do NOT reintroduce live `STRUCTURE.md`, `SECTIONS.md`, or `reference-*.md` — substance lives in OUTPUTS.md.
- External scripts stay under `~/.cursor/skills/owcc-plan-validation-report/scripts/`; document execute-vs-read in VALIDATION.md and here.
- Archive superseded files to a timestamped copy outside this package before delete.
- Visibility changes: `/change-config-visibility` (operator). Do not hand-move between `private/` and `public/`. Package edits do not require reconcile, kit install, or publish.

## Scripts

| Script | Workflow stage | Input type | Expected inputs | Output shape |
|--------|----------------|------------|-----------------|--------------|
| `~/.cursor/skills/owcc-plan-validation-report/scripts/plan-chunk-report.py` | 5.3.2 / 5.3.5 | Agent-execute | `--json` + absolute plan path | JSON stdout |
| `~/.cursor/skills/owcc-plan-validation-report/scripts/plan-qualitative-report.py` | 5.3.5 / §6 | Agent-execute | `--json` + absolute plan path | JSON stdout |
| `~/.cursor/skills/owcc-plan-validation-report/scripts/plan-validate-structure.py` | 5.3.5 / §6 | Agent-execute | `--json` + absolute plan path | JSON stdout |

No `scripts/` directory in this package. Do NOT invoke `plan-write-validation-report.py` from this skill.

## References

Operator chain docs live outside this package. This package does not prescribe sibling skill invokes.

### Reference To

| Path | Relationship |
|------|----------------|
| `~/.cursor/skills/owcc-plan-validation-report/scripts/plan-chunk-report.py` | Sizing / validate loop |
| `~/.cursor/skills/owcc-plan-validation-report/scripts/plan-qualitative-report.py` | Validate loop |
| `~/.cursor/skills/owcc-plan-validation-report/scripts/plan-validate-structure.py` | Validate loop |
