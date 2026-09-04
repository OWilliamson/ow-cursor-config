# Completion response

Chat/session OUTPUT when `/owcc-skill-modify` finishes. Cited from SKILL.md §7.

## Template — completed modify

```markdown
## Skill modify — complete

**Target:** <absolute path to skill directory>
**Change class:** behaviour | sibling-docs | aims-scope | description | mixed
**META gate:** passed (META.md + WORKFLOW.yaml)
**Maintainer sync:** both updated | WORKFLOW only | META only | verified no-op

### Change plan (pre-edit)

| Locus (file §/role) | Intended change | Done? |
|---------------------|-----------------|-------|
| … | … | yes \| no |

### Alignment sweep

- Mode: fit-to-aim | aim-to-package | both
- Result: pass | fixes applied | blockers
- Notes: …

### Maintainer sync

- WORKFLOW.yaml: mirrored §5.3 | no-op | n/a
- META.md: tree/References/Updated | no-op | n/a

### Edit summary

- File:
- What changed:
- Why:

### Residual risks

- `<risk>` or `none`
```

## Template — hard stop (no edits)

```markdown
## Skill modify — stopped (no edits)

**Target:** <absolute path or unresolved>
**Reason:** META.md absent | META unreadable | WORKFLOW.yaml absent | WORKFLOW unreadable | reshape required | ambiguous (awaiting answer)

### Recommended next step

- Run `/owcc-skill-improve` on this package first (when META, WORKFLOW, or shape missing), THEN re-invoke `/owcc-skill-modify`.
- OR clarify the change request, THEN re-invoke.

### Confirmation

- Package files modified: **none**
```

## Sections

### Change plan (pre-edit)

#### Use

Always on completed modify runs.

#### Empty Allowance

No — at least one planned locus row.

### Alignment sweep

#### Use

Always when any edit occurred.

#### Empty Allowance

No IF edits occurred; use hard-stop template when zero edits.

### Maintainer sync

#### Use

Always when any edit occurred.

#### Empty Allowance

No IF edits occurred; omit on hard-stop.

### Edit summary

#### Use

When files changed.

#### Empty Allowance

No IF any edit occurred.

### Residual risks

#### Use

Always on completed modify (may be `none`).

#### Empty Allowance

No — write `none` explicitly IF empty.

### Hard stop block

#### Use

When META gate or reshape defer aborts before edits.

#### Empty Allowance

N/A — use hard-stop template instead of complete template.

## Section Contract

### Content

- Absolute target path; change class; META+WORKFLOW gate status; maintainer sync result.
- Pre-edit plan table matching what was actually attempted.
- Alignment mode and result.
- Concise edit why; residual risks.
- Hard stop: explicit zero-edits confirmation AND improve recommendation when META/WORKFLOW/shape missing.

### Authoring

- Operator-facing; concise.
- Do NOT claim behavioural effectiveness without a fresh-session pressure test.
- Do NOT paste full VALIDATION dumps unless blockers remain.
