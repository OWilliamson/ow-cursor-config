# Validation rubric

Completion checks for `/owcc-plan-build`. On failure, RETURN TO SKILL.md §5, resolve, THEN re-run this rubric.

## Scripted validation

### Complete intent (agent-execute)

```bash
python3 ~/.cursor/skills/owcc-plan-build/scripts/plan-validate-close.py /absolute/path/to/plan.md
```

Optional `--json` when parsing programmatically.

### Peer scripts (when named IN todo content)

```bash
python3 ~/.cursor/skills/owcc-plan-verification-cursor/scripts/plan-verify-close-cursor.py --json /absolute/path/to/plan.plan.md
python3 ~/.cursor/skills/owcc-plan-verification-cursor/scripts/plan-registry-show.py --json /absolute/path/to/plan.plan.md
```

### Preflight artifact (read-only; non-`.plan.md` only)

`<workspace>/.cursor/plans/reports/<plan-name>.validation.json` — required when the target plan path does **not** end with `.plan.md`. Do NOT write it from this skill. Cursor-native `.plan.md` skips this artifact.

Confirm [WORKFLOW.yaml](WORKFLOW.yaml) mirrors SKILL §5.3 when steps change.

## Agent questions

- [ ] Preflight satisfied — `.plan.md` skip OR non-native JSON pass ([DECISIONS §1](DECISIONS.md#1-target-and-preflight))?
- [ ] Intent inferred correctly — no mode keywords ([DECISIONS §2](DECISIONS.md#2-four-intents))?
- [ ] One todo at a time; layer A+B mirrored ([DECISIONS §4](DECISIONS.md#4-execution-rule))?
- [ ] Plan file edits status-only (plus Plan build line on complete) ([DECISIONS §5](DECISIONS.md#5-plan-file-discipline))?
- [ ] Complete intent: validate-close RUN; Final validation; Plan build line set?
- [ ] No frontmatter hygiene at close?
- [ ] Chat matches [RESPONSE.md](RESPONSE.md)?
- [ ] `WORKFLOW.yaml` present; `skill: owcc-plan-build`; step ids cover SKILL §5.3?

## Interrogation agent

None.

## Authoring norms (this package)

| Norm ID | Check | Severity default |
|---------|-------|-----------------|
| `PB-WORKFLOW-SYNC` | `WORKFLOW.yaml` mirrors SKILL §5.3; `skill` matches `name` | Critical |
| `PB-PREFLIGHT` | Non-`.plan.md` requires passing validation JSON; `.plan.md` skips | Critical |
| `PB-FOUR-INTENTS` | No mode vocabulary; four intents only | Critical |
| `PB-STATUS-ONLY` | Body/content edits forbidden without approval | Critical |
| `PB-CLOSE-SCRIPT` | Complete intent cites `plan-validate-close.py` execute | Critical |
| `PB-NO-SKILL-ROUTE` | Preflight fail does not name other skills | Suggestion |

### Reporting rules

- Severity: Critical, Suggestion, or Nice to have.
