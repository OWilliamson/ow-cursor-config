# Completion response

Chat/session OUTPUT when `/owcc-plan-validation-report` finishes. Cited from SKILL.md §7.

## Template

One line only:

```markdown
Wrote <workspace-relative-or-absolute-report-path> — pass
```

or:

```markdown
Wrote <workspace-relative-or-absolute-report-path> — fail
```

On runtime error (script exit 2):

```markdown
owcc-plan-validation-report error: <brief>
```

## Sections

### Status line

#### Use

Always.

#### Empty Allowance

No.

## Section Contract

### Content

- Report path (prefer workspace-relative `.cursor/plans/reports/…` when clear).
- `pass` or `fail` matching JSON `result` (or error brief).

### Authoring

- Exactly one chat line on success path (path + pass/fail).
- Do NOT dump `failures[]` IN chat unless the operator asked for debug.
- Do NOT suggest other skills.
- Do NOT claim the plan was edited.
