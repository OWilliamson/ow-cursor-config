# Validation rubric

Completion checks for `/owcc-plan-triage`. On failure, RETURN TO SKILL.md §5, resolve, THEN re-run this rubric.

## Scripted validation

None bundled in this package. Confirm [WORKFLOW.yaml](WORKFLOW.yaml) mirrors SKILL §5.3 when steps change.

## Agent questions

- [ ] Target path unambiguous ([DECISIONS §1](DECISIONS.md#1-target-plan))?
- [ ] Session asks harvested with supersession; no invented asks ([DECISIONS §2](DECISIONS.md#2-session-intent-harvest))?
- [ ] All four axes interrogated ([DECISIONS §4](DECISIONS.md#4-four-axes))?
- [ ] Each finding has severity ([DECISIONS §3](DECISIONS.md#3-severity))?
- [ ] Clear findings patched; ambiguous left as `ask-user` ([DECISIONS §5](DECISIONS.md#5-patch-matrix))?
- [ ] Patch limits honored — no lean/full reshape, no verify twins for form, no validation JSON ([DECISIONS §6](DECISIONS.md#6-patch-limits))?
- [ ] Chat matches [RESPONSE.md](RESPONSE.md)?
- [ ] `WORKFLOW.yaml` present; `skill: owcc-plan-triage`; step ids cover SKILL §5.3?

## Interrogation agent

This skill is the substance interrogator. Nested interrogators: none.

## Authoring norms (this package)

| Norm ID | Check | Severity default |
|---------|-------|-----------------|
| `PT-WORKFLOW-SYNC` | `WORKFLOW.yaml` present; mirrors SKILL §5.3; `skill` matches `name` | Critical |
| `PT-SHAPE-B` | Clear findings patched in-run; no approval gate required | Critical |
| `PT-NO-RESIZE` | No lean/full reshape or verify-twin form edits | Critical |
| `PT-NO-INVENT` | No invented session asks | Critical |
| `PT-FOUR-AXES` | All four axes covered in RESPONSE | Critical |
| `PT-NO-SKILL-ROUTE` | Chat does not name other skills | Suggestion |

### Reporting rules

- Severity: Critical, Suggestion, or Nice to have.
- Mark unconfirmed findings speculative.
