# Meta

- **Version:** 2.1.1
- **Updated:** 2026-08-04T14:05:00Z
- **Maintainer:** <github-user>

## Directory tree

```
owcc-plan-validation-report/
  SKILL.md       # Master spine §1–7; procedural workflow
  DECISIONS.md   # Target, sizing, pass/fail
  RESPONSE.md    # One-line chat completion (§7)
  OUTPUTS.md     # .validation.json path + schema
  VALIDATION.md  # Completion rubric (§6)
  META.md        # This file — maintainer only; never linked from SKILL
  WORKFLOW.yaml  # Machine mirror of SKILL §5.3 (required)
  scripts/       # Write gate + shared plan_lib for peers
```

## Update rules

- Do **not** link or cite META.md from SKILL.md.
- Keep semantic role names stable (`DECISIONS`, `RESPONSE`, `OUTPUTS`, `VALIDATION`, `META`, `WORKFLOW.yaml`).
- Keep `WORKFLOW.yaml` IN sync with SKILL §5.3 step ids whenever the workflow changes.
- Do NOT reintroduce live `reference-*.md` — substance lives IN DECISIONS / OUTPUTS / VALIDATION.
- Shared scripts stay here; peers document execute-vs-read IN their VALIDATION/META and list filesystem paths under Reference To.
- Archive superseded files to a timestamped copy outside this package before delete.
- Visibility changes: `/change-config-visibility` (operator). Do not hand-move between `private/` and `public/`. Package edits do not require reconcile, kit install, or publish.

## Scripts

| Script | Workflow stage | Input type | Expected inputs | Output shape |
|--------|----------------|------------|-----------------|--------------|
| `scripts/plan-write-validation-report.py` | 5.3.2 / §6 | Agent-execute | plan path; optional `--sizing` | Writes JSON; prints path; exit 0/1/2 |
| `scripts/plan-chunk-report.py` | (peer consumers) | Peer-execute | `--json` + plan path | JSON stdout |
| `scripts/plan-qualitative-report.py` | (peer consumers; also internal to write) | Peer-execute / internal | `--json` + plan path | JSON stdout |
| `scripts/plan-validate-structure.py` | (peer consumers; also internal to write) | Peer-execute / internal | `--json` + plan path | JSON stdout |
| `scripts/plan_lib.py` | (library) | Agent-read / import | — | Shared helpers |
| `scripts/plan_lib_import.py` | (library) | Agent-read / import | — | Import shim for peers |

## References

Operator chain docs live outside this package. This package does not prescribe sibling skill invokes.

### Reference To

| Path | Relationship |
|------|----------------|
| `../owcc-plan-improve/OUTPUTS.md` | Body shape norms encoded IN structure/qualitative scripts |
| `../owcc-plan-improve/DECISIONS.md` §10 | Section profile (read-only contract pointer; do not expand) |
