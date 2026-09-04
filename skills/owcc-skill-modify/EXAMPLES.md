# Examples

Sparse references for `/owcc-skill-modify`. Use when a step needs a concrete pattern.

## Example 1: META.md absent — hard stop

### Before (operator)

```text
/owcc-skill-modify
@legacy-skill/SKILL.md
Add a new validation question about hooks.
```

Target has `SKILL.md` but no `META.md`.

### After (agent)

- READ for `META.md` first → missing (do not open other files).
- Zero file edits.
- OUTPUT hard-stop template; recommend `/owcc-skill-improve` then re-invoke modify.

---

## Example 1b: WORKFLOW.yaml absent — hard stop

META.md present; `WORKFLOW.yaml` missing.

### After (agent)

- READ META.md → pass; READ WORKFLOW.yaml → missing.
- Zero file edits; recommend `/owcc-skill-improve`.

---

## Example 2: Plan loci before edit

### Before (bad)

Agent opens SKILL.md and rewrites §5 immediately from a vague “make it clearer” ask.

### After (good)

Change plan first:

| Locus | Intended change |
|-------|-----------------|
| SKILL.md §5.2 | Split compound rule into two bullets |
| DECISIONS.md §3 | Add option for optional dry-run |

THEN MODIFY only those rows; RUN fit-to-aim alignment; THEN maintainer sync (WORKFLOW + META).

---

## Example 3: Aims change → aim-to-package sweep

### Before

Operator: “This skill should also cover hooks, not only rules.”

Agent updates §1 and §4 only.

### After

- Change class: **aims / scope**.
- MODIFY §1/§4, THEN sweep §2, §5, DECISIONS, RESPONSE, VALIDATION, description for hook coverage gaps.
- Fix drifted siblings IN the same run or RETURN TO the plan with new loci.
- RUN maintainer sync: WORKFLOW mirrors any §5.3 changes; META **Updated** (+ tree/References IF membership changed).

---

## Example 4: Stale META/WORKFLOW after body edit — forbidden

### Before (bad)

Agent changes SKILL §5.3 steps and ships without touching `WORKFLOW.yaml` or META.

### After (good)

5.3.7 always RUNs: sync WORKFLOW step ids to §5.3; refresh META **Updated** (and tree IF files added/removed).
