# Completion response

Chat/session OUTPUT when `/owcc-skill-validate` finishes. Cited from SKILL.md §7.

## Template

```markdown
## Skill validate — complete

### Target

- `<absolute path or pasted package>`

### Package inventory

| File | Type | Status |
|------|------|--------|
| SKILL.md | Entry point | |

### Executive pass/fail

- Overall verdict:
- Why:

### Findings table

| Norm ID | Severity | Evidence | Minimal fix |
|---------|----------|----------|-------------|

### Passing checks

- Pass:

### Speculative items

- Item:
- What would confirm it:

### Follow-up question

- `<single question if needed, or none>`
```

## Sections

### Target

#### Use

Always.

#### Empty Allowance

No.

### Package inventory

#### Use

Always.

#### Empty Allowance

No — list every package member.

### Executive pass/fail

#### Use

Always.

#### Empty Allowance

No.

### Findings table

#### Use

Always when any finding exists; IF none, state “none” under the table heading.

#### Empty Allowance

Yes IF zero findings — write `none`.

### Passing checks

#### Use

Always — acknowledge passes explicitly.

#### Empty Allowance

No — list key passes or “none recorded”.

### Speculative items

#### Use

When mechanically unconfirmed.

#### Empty Allowance

Yes — write `none`.

### Follow-up question

#### Use

When one clarifying question would unblock the operator.

#### Empty Allowance

Yes — write `none`.

## Section Contract

### Content

- Absolute target path (or pasted note).
- Full inventory with type/status.
- Overall verdict and why.
- Findings keyed to norm IDs with severity, evidence, minimal fix.
- Explicit passing checks and speculative items.

### Authoring

- Read-only report only; do NOT imply the target was edited.
- Cap detailed findings at seven; list remaining norm IDs only.
- Prefer Critical findings first.
