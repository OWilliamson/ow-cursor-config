# Validation rubric

Completion checks for `/owcc-plan-verification-cursor`. On failure, RETURN TO SKILL.md §5, resolve, THEN re-run this rubric.

## Scripted validation

### Invoke-time (agent-execute)

```bash
python3 ~/.cursor/skills/owcc-plan-verification-cursor/scripts/plan-audit-cursor-verification.py --json /absolute/path/to/plan.plan.md
python3 ~/.cursor/skills/owcc-plan-verification-cursor/scripts/plan-validate-frontmatter.py /absolute/path/to/plan.plan.md
```

- Audit: exit 1 with gaps expected before fix; final must be `ok: true`.
- Frontmatter: exit 0 required after every write.

### Build-time (named IN todo content — do not RUN as primary invoke workflow)

```bash
python3 ~/.cursor/skills/owcc-plan-verification-cursor/scripts/plan-verify-close-cursor.py --json /absolute/path/to/plan.plan.md
python3 ~/.cursor/skills/owcc-plan-verification-cursor/scripts/plan-registry-show.py --json /absolute/path/to/plan.plan.md
```

### Libraries

| File | Role |
|------|------|
| `scripts/plan_registry_lib.py` | Registry helpers for verify/show scripts |

Confirm [WORKFLOW.yaml](WORKFLOW.yaml) mirrors SKILL §5.3 when steps change.

## Agent questions

- [ ] Target IS cursor-native `.plan.md` ([DECISIONS §1](DECISIONS.md#1-target-plan))?
- [ ] Placement matches isProject vs flat ([DECISIONS §2](DECISIONS.md#2-closeout-placement))?
- [ ] Templates match [OUTPUTS.md](OUTPUTS.md)?
- [ ] Frontmatter validated after every write ([DECISIONS §3](DECISIONS.md#3-frontmatter-rules))?
- [ ] Final audit `ok: true`?
- [ ] Chat matches [RESPONSE.md](RESPONSE.md) (mutation delta, not runtime verify)?
- [ ] `WORKFLOW.yaml` present; `skill: owcc-plan-verification-cursor`; step ids cover SKILL §5.3?

## Interrogation agent

None.

## Authoring norms (this package)

| Norm ID | Check | Severity default |
|---------|-------|-----------------|
| `PVC-WORKFLOW-SYNC` | `WORKFLOW.yaml` mirrors SKILL §5.3; `skill` matches `name` | Critical |
| `PVC-INVOKE-VS-BUILD` | META/VALIDATION separate invoke-time vs build-time scripts | Critical |
| `PVC-FRONTMATTER-EVERY-WRITE` | SKILL requires frontmatter validate after every write | Critical |
| `PVC-NO-VALIDATION-JSON` | Skill does not write `.validation.json` | Critical |
| `PVC-NO-SKILL-ROUTE` | Chat does not name other skills | Suggestion |

### Reporting rules

- Severity: Critical, Suggestion, or Nice to have.
