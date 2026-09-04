# Completion response

Chat/session OUTPUT when `/owcc-rule-improve` finishes. Cited from SKILL.md §7.

## Template

```markdown
## Rule improve — complete

**Target:** <absolute path to .mdc>
**Scope:** full | frontmatter-only | body-only

### Capabilities and usage

- What the rewritten rule does now:
- When it applies (activation / globs / alwaysApply):
- Required inputs:
- Out of scope:

### Activation

- `alwaysApply`:
- `globs`:
- Sample path that SHOULD match:
- Sample path that should NOT match:
- Verification method:

### Inventory

| File | Type | Action taken | Rationale |
|------|------|--------------|-----------|
| example.mdc | Rule entry | rewritten | |

### Inter-rule and scope conflicts

| Other rule | Relationship | Resolution |
|------------|--------------|------------|
| | | |

### Edit summary

- File:
- What changed:
- Why:

### Before/after pair(s)

#### Before

```markdown
<old excerpt>
```

#### After

```markdown
<new excerpt>
```

### Residual risks

- `<risk>`
```

## Sections

### Capabilities and usage

#### Use

Always.

#### Empty Allowance

No.

### Activation

#### Use

Always.

#### Empty Allowance

No — state N/A for samples only when `alwaysApply: true` with no globs (note always-on instead).

### Inventory

#### Use

Always.

#### Empty Allowance

No.

### Inter-rule and scope conflicts

#### Use

Always when overlap scan ran.

#### Empty Allowance

Yes — write a single “none” row IF no conflicts.

### Edit summary

#### Use

Always when files changed.

#### Empty Allowance

No IF any edit occurred.

### Before/after pair(s)

#### Use

When substance relocated or spine reshaped; at least one pair preferred on full pass.

#### Empty Allowance

Yes IF only trivial frontmatter fixes — state “none”.

### Residual risks

#### Use

Always (may be a single “none”).

#### Empty Allowance

No — write `none` explicitly IF empty.

## Section Contract

### Content

- Absolute target path and edit scope.
- Post-rewrite capabilities aligned with frontmatter + body.
- Activation samples for glob precision (or always-on note).
- Inventory of target and paired siblings with action/rationale.
- Inter-rule / scope-layer resolutions.
- Residual risks (e.g. validate-rule still vendors a norms copy; pressure test not run).

### Authoring

- Concise operator chat; do NOT paste full CR-* dump unless blockers remain.
- Do NOT claim behavioural effectiveness without a fresh-session pressure test.
