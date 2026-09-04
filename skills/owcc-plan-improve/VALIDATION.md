# Validation rubric

Completion checks for `/owcc-plan-improve`. On failure, RETURN TO SKILL.md §5, resolve, THEN re-run this rubric.

## Scripted validation

None bundled in this package. Agent-run scripts live under `~/.cursor/skills/owcc-plan-validation-report/scripts/` (execute; do NOT write `.validation.json` from this skill).

### Mechanical commands (agent-run)

```bash
python3 ~/.cursor/skills/owcc-plan-validation-report/scripts/plan-chunk-report.py --json /absolute/path/to/plan.md
python3 ~/.cursor/skills/owcc-plan-validation-report/scripts/plan-qualitative-report.py --json /absolute/path/to/plan.md
python3 ~/.cursor/skills/owcc-plan-validation-report/scripts/plan-validate-structure.py --json /absolute/path/to/plan.md
```

- Parse `--json` only; fix until qualitative + structure pass (or document blockers). Qualitative = hygiene; structure = outline/gates — do not expect qualitative to repeat structure codes.
- Re-run chunk after material §0 / phase changes; apply [DECISIONS §8](DECISIONS.md#8-chunk-report-flag-response) without shortening for weight alone.
- Confirm no `.cursor/plans/reports/*.validation.json` write from this skill (that artifact is a separate operator gate, not part of the improve edit loop).

## Agent questions

- [ ] Target path unambiguous; edit scope and sizing mode stated?
- [ ] Plan body has Title H1 + §1–10 `##` headings in [OUTPUTS.md](OUTPUTS.md) order?
- [ ] `WORKFLOW.yaml` present; `skill: owcc-plan-improve`; step ids cover SKILL §5.3?
- [ ] Plan class chosen; section profile filled ([DECISIONS §9](DECISIONS.md#9-plan-class)–[§10](DECISIONS.md#10-section-profile-by-class))?
- [ ] Substance inventory ⊆ plan (fidelity gate) or blockers / user-approved drops documented?
- [ ] Lean: no verify-twin todos added solely for `missing_verify`?
- [ ] YAML vs Stages: verify/acceptance wording consistent; YAML wins on conflict?
- [ ] Operator chrome stripped ([OUTPUTS.md](OUTPUTS.md) Section Contract strip list)?
- [ ] Aims OKR table present (Todo | Objective | Result | Key signals) for implement todos?
- [ ] Rules First/Final ids exist in frontmatter?
- [ ] Coherence read done after scripts pass?
- [ ] Chat output ready per [RESPONSE.md](RESPONSE.md)?

## Interrogation agent

None by default.

## Authoring norms (plan package)

| Norm ID | Check | Severity default |
|---------|-------|-----------------|
| `PI-WORKFLOW-SYNC` | `WORKFLOW.yaml` present; mirrors SKILL §5.3 step ids; `skill` matches `name` | Critical |
| `PI-NAME-TITLE` | Frontmatter `name` matches body Title H1 | Critical |
| `PI-HEADING-ORDER` | Body `##` sections match OUTPUTS fixed order | Critical |
| `PI-FIDELITY` | Inventory items present or user-approved removed / blocked | Critical |
| `PI-LEAN-NO-FAKE-VERIFY` | Lean mode does not add verify twins only for `missing_verify` | Critical |
| `PI-NO-WEIGHT-SHORTEN` | No shorten-only edits for chunk weight | Critical |
| `PI-NO-REPORT-WRITE` | This skill does not write validation report files | Critical |
| `PI-YAML-WINS-VERIFY` | On conflict, YAML `content` owns verify/acceptance text | Suggestion |
| `PI-STRIP-CHROME` | Operator chrome absent after improve | Suggestion |
| `PI-CLASS-PROFILE` | Sections match class profile | Suggestion |

### Reporting rules

- Severity: Critical, Suggestion, or Nice to have.
- Mark unconfirmed findings speculative.
- Cap detailed findings; list remaining norm IDs IF many.
