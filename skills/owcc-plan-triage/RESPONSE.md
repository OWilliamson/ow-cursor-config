# Completion response

Chat/session OUTPUT when `/owcc-plan-triage` finishes. Cited from SKILL.md §7.

## Template

```markdown
## Plan triage — complete

**Target:** <absolute path>

### Findings by axis

| Axis | Severity | Finding | Locus |
|------|----------|---------|-------|
| session-intent | blocker\|should-fix\|ask-user\|note | … | … |
| contradictions | … | … | … |
| loose-ends | … | … | … |
| executor-gaps | … | … | … |

### Patches applied

- <section or todo id>: <what changed>

### Remaining ask-user / blockers

- … (or `none`)
```

## Sections

### Findings by axis

#### Use

Always — cover all four axes (write `none` per axis IF empty).

#### Empty Allowance

No for the section; individual axes may say `none`.

### Patches applied

#### Use

Always when Shape B ran.

#### Empty Allowance

Yes — write `none` IF no safe patches.

### Remaining ask-user / blockers

#### Use

Always.

#### Empty Allowance

No — write `none` explicitly IF empty.

## Section Contract

### Content

- Absolute plan path.
- Findings with severity and locus.
- Patches applied (section/todo touched).
- Remaining ambiguous or unfixed blockers.

### Authoring

- Concise operator chat; no six-section essay; no How-to-run block.
- Do NOT suggest other skills.
- Do NOT claim build gate pass/fail.
