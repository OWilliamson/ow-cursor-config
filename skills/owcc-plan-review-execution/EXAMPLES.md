# Examples

Sparse references for `/owcc-plan-review-execution`. Use when a workflow step needs a concrete pattern.

## Example 1: A/M/R claimed path missing

Inventory marks `public/skills/foo/SKILL.md` as **missing** under Additions. Aim Result for the todo requires that file. Disk has no path; git shows no add.

### Verdict

**fail** on Aims (and that todo) — specified-but-undone ([DECISIONS §15](DECISIONS.md#15-specified-but-undone)). Failure **F1**: Source Aims + todo; Why: Result required file absent.

---

## Example 2: Aim Result unmet despite files present

Todo `reaim-skill-spine` IS `completed`. Files IN Modifications exist and differ from baseline, but Aim **Result** required "description not false-completion-led" and frontmatter still leads with false completions.

### Verdict

**fail** on Aims / todo correctness — presence of edits IS NOT success. Judge Result text, not path existence alone. Failure **F1**: criterion "description not false-completion-led" → frontmatter still false-completion-led → fail.

---

## Example 3: Stop-if workaround

Rules Stop-if: "Profile install mid-build — stop." Diff shows `~/.cursor` skill install while hub build continued. Chat has no operator override.

### Verdict

**fail** on Stop-if — halt ignored or worked around. Failure **F1** with action needed (revert install / re-run review after cleanup).

---

## Example 4: Bugbot LOC skip (default off)

Inventory `code_loc` = 6200. Operator gave no `bugbot=on`. Gate → skip; Bugs **n/a** with reason "LOC > 5000".

### Report fragment

```markdown
### Subagent findings

- Bugbot: n/a — code_loc 6200 > 5000 (default off)
- Security Review: n/a — no auth/secrets/network/external writes
```

Do **NOT** mark Bugs **fail** for the skip.

---

## Example 5: Operator skip-bugbot

User: `/owcc-plan-review-execution skip-bugbot`. `code_loc` = 200 (would default on).

### Verdict

Bugs **n/a** — operator skip. Overall may still **pass** IF success dims pass.

---

## Example 6: Bugbot spawn failure when gated on

`code_loc` = 400; gate on. Task `bugbot` fails twice before findings.

### Verdict

Overall **incomplete_review** (or warn on Bugs) — NOT Bugs **pass**. Failure **F1**: spawn failure under Failures table.

---

## Example 7: Closeout authoring ≠ success fail (appendix only)

Operator asked for closeout appendix. `plan-validate-close.py` reports `missing_final_validation`. Aims Results met; Target shape matches; no Bugbot fails.

### Correct report

```markdown
**Overall:** pass_with_warnings

### Success judgments
| Aims | pass | Result rows met on disk — … |

### Residual risks
- Closeout appendix: missing_final_validation — class: authoring (bookkeeping only)
```

Do **NOT** headline Objective checks as the product or force Overall **fail** on authoring alone.

---

## Example 8: Better-than-start is baseline delta — not Aims again

Aims **pass**. Bugbot **n/a**. Merge-base baseline resolved. Diff since baseline shows the claimed Modifications; no in-scope path that existed at baseline is missing or broken.

### Verdict

Better-than-start **pass** — usable baseline, forward change on claimed paths, no regression. Do **NOT** set Better from Aims verdict.

Alternate: same Aims **pass**, but baseline is HEAD+WT only (no main) → Better **warn** (ambiguous baseline), Aims stays **pass**.

---

## Example 9: Operator replies by F-id

Report lists **F2**: todo `wire-auth` — Key action "middleware enforces session" unmet.

Operator: "F2 fixed — re-review todo wire-auth."

### Next run

Scope to todo `wire-auth`; re-check F2 criterion only; close F2 IF judgment passes or open new F-id IF still unmet.

---

## Example 10: Inventory JSON without disk judgment

Agent RUN inventory assist; all `claimed` paths show **present**; agent marks Aims **pass** citing only inventory JSON.

### Verdict

**Wrong** — inventory IS NOT the review. Agent must READ files and judge Aim Result / Content columns. Unmet Result despite present paths → **fail** per Example 2 and [DECISIONS §15](DECISIONS.md#15-specified-but-undone).
