# Completion response

Chat/session OUTPUT when `/owcc-plan-build` finishes. Cited from SKILL.md §7.

## Template

```markdown
## Plan build — <intent>

**Plan:** <path>
**Intent:** named todo | named phase | incomplete plan | complete plan
**Validation report:** <path> (pass)

### Todos in scope
- <id>: <status> — <one line>

### Validation
<commands / plan-validate-close.py> → <pass/fail brief>

### Plan closed (complete intent only)
- **Plan build:** complete — <date>

### Notes
<stop-if, blockers, follow-up>
```

### Orient (first message after reading the plan)

Optional short confirm before the loop:

```markdown
**Plan build** — intent: <named todo | named phase | incomplete | complete>
**Plan:** `<path>`
**Validation report:** pass
**Scope:** <todo id | phase name | whole plan>
**First in scope:** `<id>` — <short content>
**Stop-if:** <none | gates>
Proceeding unless you change scope.
```

## Sections

### Header (Plan / Intent / Validation report)

#### Use

Always.

#### Empty Allowance

No.

### Todos in scope

#### Use

Always.

#### Empty Allowance

No IF any todo IN scope — one line per id.

### Validation

#### Use

Always after any verify or closeout script (or note n/a for sync-only status updates).

#### Empty Allowance

No — state pass/fail/skip.

### Plan closed

#### Use

Complete intent only.

#### Empty Allowance

Yes — omit section IF not complete intent.

### Notes

#### Use

Always.

#### Empty Allowance

No — write `none` explicitly IF empty.

## Section Contract

### Content

- Absolute plan path, inferred intent, validation report path (pass).
- Per-todo status IN scope.
- Closeout / verify results when run.
- Stop-if, blockers, follow-up.

### Authoring

- Concise; do NOT dump full script JSON unless debugging.
- Do NOT name other skills on preflight fail.
- Do NOT claim complete unless Plan build line set (complete intent).
