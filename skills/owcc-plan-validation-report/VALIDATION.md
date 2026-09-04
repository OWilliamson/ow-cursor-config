# Validation rubric

Completion checks for `/owcc-plan-validation-report`. On failure, RETURN TO SKILL.md §5, resolve, THEN re-run this rubric.

## Scripted validation

### Mechanical commands (agent-run)

**This skill — execute:**

```bash
python3 ~/.cursor/skills/owcc-plan-validation-report/scripts/plan-write-validation-report.py /absolute/path/to/plan.md
```

Optional: `--sizing lean|full|auto` (default `lean`).

**Peer-executed (edit-loop consumers with `--json` only — not this skill's write path):**

```bash
python3 ~/.cursor/skills/owcc-plan-validation-report/scripts/plan-chunk-report.py --json /absolute/path/to/plan.md
python3 ~/.cursor/skills/owcc-plan-validation-report/scripts/plan-qualitative-report.py --json /absolute/path/to/plan.md
python3 ~/.cursor/skills/owcc-plan-validation-report/scripts/plan-validate-structure.py --json /absolute/path/to/plan.md
```

The write script shells to qualitative + structure + chunk **once each**. Qualitative is hygiene-only (does not embed `validate_structure`). Confirm [WORKFLOW.yaml](WORKFLOW.yaml) mirrors SKILL §5.3 when steps change.

### Libraries (agent-read / import)

| File | Role |
|------|------|
| `scripts/plan_lib.py` | Shared plan parse / report path helpers |
| `scripts/plan_lib_import.py` | Import shim for peer packages |

## Agent questions

- [ ] Target path absolute and unambiguous ([DECISIONS §1](DECISIONS.md#1-target-plan))?
- [ ] Sizing flag decided ([DECISIONS §2](DECISIONS.md#2-sizing-flag))?
- [ ] Write script RUN; report path matches [OUTPUTS.md](OUTPUTS.md)?
- [ ] JSON has `schema: 1`, `result`, `issued_at`, matching `plan`?
- [ ] Plan file not modified by this skill?
- [ ] Chat IS one status line per [RESPONSE.md](RESPONSE.md)?
- [ ] `WORKFLOW.yaml` present; `skill: owcc-plan-validation-report`; step ids cover SKILL §5.3?

## Interrogation agent

None.

## Authoring norms (this package)

| Norm ID | Check | Severity default |
|---------|-------|-----------------|
| `PVR-WORKFLOW-SYNC` | `WORKFLOW.yaml` present; mirrors SKILL §5.3; `skill` matches `name` | Critical |
| `PVR-NO-PLAN-EDIT` | Skill does not instruct plan body/YAML edits | Critical |
| `PVR-ONE-LINE` | RESPONSE contract IS one status line | Critical |
| `PVR-WRITE-SCRIPT` | SKILL cites `plan-write-validation-report.py` as agent-execute | Critical |
| `PVR-PEER-SCRIPTS-DOC` | META documents chunk/qual/structure as peer-execute | Critical |
| `PVR-NO-SKILL-ROUTE` | Chat does not name other skills | Suggestion |

### Reporting rules

- Severity: Critical, Suggestion, or Nice to have.
- Mark unconfirmed findings speculative.
