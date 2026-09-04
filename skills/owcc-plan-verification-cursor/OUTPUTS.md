# Closeout injection templates

Templates this skill WRITEs into `.plan.md`. Build agents execute the scripts named IN todo `content` — this skill does not RUN them at invoke time.

## What closeout must confirm (build agent)

| Layer | Check |
|-------|--------|
| **Plan file** | Every todo `status` IS `completed` or `cancelled` |
| **Plan body** | `**Plan build:** complete — YYYY-MM-DD` IN execution contract |
| **Registry** | Row IN `composer.planRegistry`; `builtBy` lists all plan todo ids |

## Per-phase closeout todo (`isProject: true`)

Last todo IN **each** phase:

```yaml
- id: phase-1-close-verify
  content: >
    Cursor-native closeout: run
    python3 ~/.cursor/skills/owcc-plan-verification-cursor/scripts/plan-verify-close-cursor.py --json
    /absolute/path/to/plan.plan.md — exit 0 required. Inspect registry with
    python3 ~/.cursor/skills/owcc-plan-verification-cursor/scripts/plan-registry-show.py --json
    same plan path; confirm builtBy lists every todo id in this phase and plan.
    Confirm **Plan build:** complete — YYYY-MM-DD exists in execution contract when
    this is the final phase and all plan todos are done. On any failure: investigate
    file YAML vs registry before marking this todo complete; re-run verify until exit 0.
  status: pending
```

Use stable ids: `phase-N-close-verify` or `cursor-native-close-verify` when one phase only.

## Flat plan final todo

```yaml
- id: cursor-native-close-verify
  content: >
    Cursor-native closeout: run
    python3 ~/.cursor/skills/owcc-plan-verification-cursor/scripts/plan-verify-close-cursor.py --json
    /absolute/path/to/plan.plan.md — exit 0 required. Run
    python3 ~/.cursor/skills/owcc-plan-verification-cursor/scripts/plan-registry-show.py --json
    on the same path; confirm builtBy covers all plan todo ids. Confirm
    **Plan build:** complete — YYYY-MM-DD in execution contract. On failure:
    investigate incomplete YAML todos, missing Plan build line, or registry gaps;
    fix completion evidence; re-run verify; do not mark this todo complete until exit 0.
  status: pending
```

Or strengthen existing `completion-audit` with the same script paths and pass criteria.

## Body addendum (optional but recommended)

```markdown
## Cursor-native closeout

At phase closeout (or plan closeout for flat plans), the build agent runs
`plan-verify-close-cursor.py` and `plan-registry-show.py` as named in the final
verify todo. Do not mark the verify todo complete until verify script exits 0.
On failure: reconcile file `status:` with registry `builtBy` before retrying.
```

Alternatively embed closeout language under **Execution contract** / Rules IN the plan body.

## Build-agent behaviour on script fail

1. Print which checks failed (from `--json` `failures[]` or stderr).
2. Fix layer A when file todos or **Plan build:** complete line are wrong.
3. For registry gaps: RUN `plan-registry-show.py --json`, compare plan todo ids vs `builtBy`.
4. Re-run `plan-verify-close-cursor.py` until exit **0**.
5. Do **not** mark the closeout verify todo `completed` until verify passes.
