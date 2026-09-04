# Completion response

Chat/session OUTPUT when `/owcc-plan-verification-cursor` finishes. Cited from SKILL.md §7.

## Template

```markdown
## Plan verification (cursor-native) — complete

**Target:** <absolute path to .plan.md>
**Shape:** isProject | flat

### Mutations
- …

### Script results
- audit: ok true|false (final)
- frontmatter: exit 0

### Remaining gaps
- none
```

## Sections

### Mutations

#### Use

Always.

#### Empty Allowance

No IF any edit occurred — list todos/sections added or repaired. IF already clean, write `none (already ok)`.

### Script results

#### Use

Always.

#### Empty Allowance

No — final audit + last frontmatter exit code.

### Remaining gaps

#### Use

Always.

#### Empty Allowance

No — write `none` when audit `ok: true`.

## Section Contract

### Content

- Absolute `.plan.md` path and shape.
- Mutation summary (not runtime closeout pass/fail).
- Final audit + frontmatter results.

### Authoring

- Concise; do NOT dump full gap JSON unless debugging.
- Do NOT suggest other skills.
- Do NOT report `plan-verify-close-cursor.py` runtime results as this skill's outcome.
