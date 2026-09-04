# Validation rubric

Completion checks for `/owcc-plan-review-execution`. On failure, RETURN TO SKILL.md §5, resolve, THEN re-run this rubric.

## Judgment basis

Trust order (mandatory):

1. **Disk** — files exist; contents match Aim Result / Target shape / todo Key actions
2. **Git** — `git diff` / `git status` since baseline ([DECISIONS §3](DECISIONS.md#3-git-baseline))
3. **Plan YAML** — `status:` on each todo (claim only, not proof of success)
4. **Chat memory** — lowest; never sole basis for pass

### Judgment types

| Type | Source | Pass signal |
|------|--------|-------------|
| Aim Result | `## Aims` OKR **Result** + disk/diff | In-scope Result met |
| Target shape | `## Target shape` vs layout/files | End-state matches (or n/a) |
| Scope | `## Scope` + unplanned paths | In-scope covered; drift flagged |
| Stop-if | Rules Stop-if + chat/diff | No ignore/workaround |
| Rules / §9 | Plan Rules + bounded workspace rules | Honored by work |
| Better-than-start | Diff vs git baseline ([DECISIONS §3](DECISIONS.md#3-git-baseline), [§11](DECISIONS.md#11-better-than-start)) | Usable baseline; no clear in-scope regression; forward change when files claimed |
| A/M/R path | Inventory `claimed` / `unplanned` | Agent confirms Content/Change/Reason after disk read — inventory IS NOT verdict |
| Todo correctness | Aim Result + Stages Key actions / DoD | Correctly done, not YAML alone ([DECISIONS §15](DECISIONS.md#15-specified-but-undone)) |
| Subagent | Bugbot / Security Review | Defects folded into Failures with F-ids |

### Command re-run rules

Optional and light — not the review basis. Re-run backtick commands from todo `content` only when needed to judge correctness (e.g. named Final validation). Skip mutating/external/secret-gated commands → note **blocked** and use diff instead. Do NOT mandate per-todo verify theater.

## Success checklist

Mark each dimension **pass** / **warn** / **fail** / **n/a** for the review scope ([DECISIONS §5](DECISIONS.md#5-success-dimensions)).

### Plan success

- [ ] Aims: in-scope Aim Results met on disk/diff (not YAML alone).
- [ ] Target shape: matches §4 OR marked n/a.
- [ ] Scope: in-scope covered; material unplanned drift flagged.
- [ ] Stop-if: no met-and-ignored / worked-around halt.
- [ ] Rules / §9: plan Rules + §9 + bounded workspace rules honored ([DECISIONS §7](DECISIONS.md#7-workspace-rules)).
- [ ] Per-todo: correctly done vs Aim Result / Stages ([DECISIONS §15](DECISIONS.md#15-specified-but-undone)).
- [ ] Better-than-start: baseline usable; no clear in-scope regression vs baseline; forward change when file work claimed ([DECISIONS §11](DECISIONS.md#11-better-than-start)) — not a re-score of Aims.
- [ ] Every fail/warn has F-id, why + action needed ([DECISIONS §10](DECISIONS.md#10-failure-why-and-action)).
- [ ] Judgment cells follow criterion → workspace outcome → why (not lone path/snippet).

### Inventory assist

- [ ] A/M/R inventory script RUN; `claimed` / `unplanned` / `code_loc` / `bugbot_default` parsed.
- [ ] Agent still checked Content/Change/Reason for material A/M/R rows on disk (script IS NOT verdict).

### Subagents

- [ ] Bugbot gate applied ([DECISIONS §8](DECISIONS.md#8-bugbot-gate)); skip = n/a not fail.
- [ ] Security Review run or skipped with reason ([DECISIONS §9](DECISIONS.md#9-security-review)).
- [ ] Gated-on spawn failure → incomplete_review/warn, not Bugs/Security pass.

### Integrity (secondary)

- [ ] Plan file edits: only expected `status:` changes ([DECISIONS §14](DECISIONS.md#14-plan-edit-severity)).
- [ ] No premature close — `**Plan build:** complete` while success dims have **fail**.
- [ ] Authoring-class closeout (IF run) did NOT alone force Overall fail.

**Out of checklist (do not fail here):** plan body Title H1 / `##` section order / plan-authoring OUTPUTS shape — authoring concerns, not execution success.

### Severity guide

| Severity | Examples |
|----------|----------|
| **fail** | Specified-but-undone ([DECISIONS §15](DECISIONS.md#15-specified-but-undone)); Aim Result unmet; Target shape mismatch; Stop-if workaround; Rules/§9 violated; fail-severity Bugbot/Security when run |
| **warn** | Ambiguous outcome; blocked check; minor Scope drift; inventory_incomplete; Bugbot warns only |
| **pass** | Judgment shows criteria met on disk/diff |
| **n/a** | Dimension absent; Bugbot skipped; Security not relevant |

## Scripted validation

### Mechanical commands (agent-run)

Primary inventory assist (required):

```bash
python3 ~/.cursor/skills/owcc-plan-review-execution/scripts/plan-amr-inventory.py --json /absolute/path/to/plan.md
```

Optional: `--todo`, `--phase`, `--workspace`, `--base`.

Expect JSON keys: `claimed`, `unplanned`, `code_loc`, `bugbot_default` (plus light todos). Inventory assist only — not pass/fail verdicts.

Optional closeout appendix (operator ask OR `**Plan build:** complete` present) — classify per [DECISIONS §4](DECISIONS.md#4-closeout-finding-class):

```bash
python3 ~/.cursor/skills/owcc-plan-build/scripts/plan-validate-close.py --json /absolute/path/to/plan.md
# IF cursor-native under .cursor/plans/:
python3 ~/.cursor/skills/owcc-plan-verification-cursor/scripts/plan-verify-close-cursor.py --json /absolute/path/to/plan.plan.md
python3 ~/.cursor/skills/owcc-plan-verification-cursor/scripts/plan-registry-show.py --json /absolute/path/to/plan.plan.md
```

- Confirm RESPONSE order: Header → Success judgments → Failures (F-ids) → todo matrix → subagent findings → A/M/R inventory → Residual risks.
- Confirm plan file was NOT edited by this skill.

## Agent questions

- [ ] Target plan AND scope unambiguous ([DECISIONS §1](DECISIONS.md#1-target-plan)–[§2](DECISIONS.md#2-review-scope))?
- [ ] Review judged **plan success**, not YAML-theater / closeout authoring as the product?
- [ ] Report leads with Success judgments (not Objective checks)?
- [ ] Judgment cells state criterion → outcome → why (not lone paths)?
- [ ] Every fail/warn has F-id, why + action needed?
- [ ] Specified-but-undone items marked **fail** per [DECISIONS §15](DECISIONS.md#15-specified-but-undone)?
- [ ] No Aim or todo marked **pass** on YAML alone?
- [ ] Bugbot gate honored; skipped Bugbot recorded as n/a?
- [ ] Bounded workspace rules only (not full profile)?
- [ ] Chat OUTPUT matches [RESPONSE.md](RESPONSE.md)?
- [ ] Plan file untouched; no implementation fixes applied?

## Interrogation agent

None by default. IF operator requests a subagent audit, THEN scope it to: success dims vs disk/git, Bugbot gate, F-id coverage, AND no plan mutation.

## Package norms (this skill)

| Norm ID | Check | Severity default |
|---------|-------|-----------------|
| `PRE-OBJECT` | Object of review = plan success; inventory script is assist only | Critical |
| `PRE-NO-YAML-PASS` | Aims/todos require disk/diff judgment | Critical |
| `PRE-JUDGMENT-SHAPE` | Judgment cells: criterion → outcome → why | Critical |
| `PRE-FAILURE-IDS` | Every fail/warn has F-id | Critical |
| `PRE-SPECIFIED-UNDONE` | Plan-named unmet work → fail per DECISIONS §15 | Critical |
| `PRE-RESPONSE-ORDER` | RESPONSE leads with Success judgments | Critical |
| `PRE-BUGBOT-GATE` | Bugbot spawn follows DECISIONS §8; skip = n/a | Critical |
| `PRE-NO-MUTATE` | This skill does not edit the plan or implement work | Critical |
| `PRE-WORKFLOW-SYNC` | `WORKFLOW.yaml` mirrors SKILL §5.3; `skill` matches `name` | Critical |
| `PRE-CLOSEOUT-OPTIONAL` | Closeout scripts optional appendix; authoring alone ≠ Overall fail | Suggestion |
| `PRE-RESPONSE-SHAPE` | Final chat follows RESPONSE.md | Suggestion |

### Reporting rules

- Severity: Critical, Suggestion, or Nice to have.
- Mark unconfirmed findings speculative.
- Cap detailed findings; list remaining norm IDs IF many.
