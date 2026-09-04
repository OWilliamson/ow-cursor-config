# Meta

- **Version:** 3.2.0
- **Updated:** 2026-08-07T12:50:46Z
- **Maintainer:** <github-user>

## Directory tree

```
owcc-plan-review-execution/
  SKILL.md       # Master spine §1–7; success-first workflow
  DECISIONS.md   # Target, scope, baseline, success dims, F-ids, specified-but-undone
  RESPONSE.md    # Chat completion template (§7) — Judgment + F-ids
  VALIDATION.md  # Success checklist + A/M/R inventory script contract (§6)
  META.md        # This file — maintainer only; never linked from SKILL
  EXAMPLES.md    # Success / inventory / F-id / Bugbot gate examples
  WORKFLOW.yaml  # Machine mirror of SKILL §5.3 (required)
  scripts/       # A/M/R + code_loc inventory assist (agent-execute)
```

## Update rules

- Do **not** link or cite META.md from SKILL.md.
- Keep semantic role names stable (`DECISIONS`, `RESPONSE`, `VALIDATION`, `META`, `EXAMPLES`, `WORKFLOW.yaml`).
- Keep `WORKFLOW.yaml` IN sync with SKILL §5.3 step ids whenever the workflow changes.
- Do NOT reintroduce live `reference-*.md` — substance lives IN DECISIONS / VALIDATION / RESPONSE.
- Do NOT add OUTPUTS.md unless this skill starts writing a structured file artifact (chat report stays IN RESPONSE).
- **Object of review:** plan success (Aims, Target shape, Scope, Stop-if, Rules, todos) plus baseline non-regression (Better-than-start). Inventory script IS assist only — not the review product.
- Judgment cells: criterion → workspace outcome → why verdict. Every fail/warn gets F-id ([DECISIONS §10](DECISIONS.md#10-failure-why-and-action)).
- Specified-but-undone → **fail** ([DECISIONS §15](DECISIONS.md#15-specified-but-undone)).
- A/M/R inventory gaps feed Scope and todo correctness as hints; each dim owns one primary verdict ([DECISIONS §13](DECISIONS.md#13-amr-inventory-severity)) — do not double-fail the same path.
- Better-than-start IS baseline delta / non-regression only — never a re-score of Aims or Bugbot/Security.
- Preserve: authoring-class closeout codes classified, not mistaken for success failure; skipped Bugbot = n/a.
- Archive superseded files to a timestamped copy outside this package before delete.
- Visibility changes: `/change-config-visibility` (operator). Do not hand-move between `private/` and `public/`. Package edits do not require reconcile, kit install, or publish.

## Scripts

| Script | Workflow stage | Input type | Expected inputs | Output shape |
|--------|----------------|------------|-----------------|--------------|
| `scripts/plan-amr-inventory.py` | 5.3.2 / §6 | Agent-execute | `--json` + absolute plan path; optional `--todo` / `--phase` / `--workspace` / `--base` | JSON stdout: `claimed`, `unplanned`, `code_loc`, `bugbot_default`, light todos (inventory assist) |
| `scripts/plan_lib_import.py` | (library) | Agent-read / import | Used by inventory script | Imports `plan_lib` from validation-report scripts path |
| `~/.cursor/skills/owcc-plan-build/scripts/plan-validate-close.py` | 5.3.10 optional appendix | Agent-execute (peer) | `--json` + plan path | JSON stdout — classify findings |
| `~/.cursor/skills/owcc-plan-verification-cursor/scripts/plan-verify-close-cursor.py` | 5.3.10 optional appendix | Agent-execute (peer) | `--json` + cursor `.plan.md` | JSON stdout — classify findings |
| `~/.cursor/skills/owcc-plan-verification-cursor/scripts/plan-registry-show.py` | 5.3.10 optional appendix | Agent-execute (peer) | `--json` + cursor `.plan.md` | JSON stdout — informational |

## References

Operator chain docs live outside this package. This package does not prescribe sibling skill invokes.

### Reference To

| Path | Relationship |
|------|----------------|
| Plan OUTPUTS shape (§1–§8) | Consumed as plan success criteria (do not mutate OUTPUTS from this skill) |
| `~/.cursor/skills/owcc-plan-build/scripts/plan-validate-close.py` | Optional peer bookkeeping closeout |
| `~/.cursor/skills/owcc-plan-verification-cursor/scripts/plan-verify-close-cursor.py` | Optional peer cursor closeout |
| `~/.cursor/skills/owcc-plan-verification-cursor/scripts/plan-registry-show.py` | Optional peer registry detail |
| `~/.cursor/skills/owcc-plan-validation-report/scripts/plan_lib.py` | Shared plan parse library via `plan_lib_import.py` |
| Profile `review-bugbot` / `review-security` | Task spawn shapes for gated subagents |
