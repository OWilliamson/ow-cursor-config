# Completion response

Chat/session OUTPUT when `/owcc-skill-improve` finishes. Cited from SKILL.md §7.

## Template

```markdown
## Skill improve — complete

**Target:** <absolute path to skill directory>
**Scope:** full | siblings-only | SKILL-only

### Capabilities and usage

- What the rewritten skill does now:
- When to use it:
- Required inputs (signals):
- Out of scope:

### Package inventory

| File | Role | Action taken | Rationale |
|------|------|--------------|-----------|
| SKILL.md | Entry | rewritten | §1–7 spine |
| DECISIONS.md | Decisions | created \| tightened \| n/a | |
| RESPONSE.md | Response | … | |
| OUTPUTS.md | Outputs | … \| omitted | |
| VALIDATION.md | Validation | … | |
| META.md | Meta | … | |
| EXAMPLES.md | Examples | … \| omitted | |
| WORKFLOW.yaml | Workflow | created \| tightened | §5.3 mirror |

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

- `<risk>` (e.g. WORKFLOW.yaml out of sync with §5.3)
```

## Sections

### Capabilities and usage

#### Use

Always.

#### Empty Allowance

No.

### Package inventory

#### Use

Always.

#### Empty Allowance

No.

### Edit summary

#### Use

Always when files changed.

#### Empty Allowance

No IF any edit occurred.

### Before/after pair(s)

#### Use

When substance relocated or spine reshaped; at least one pair preferred on full pass.

#### Empty Allowance

Yes IF only trivial link fixes — state “none”.

### Residual risks

#### Use

Always (may be a single “none”).

#### Empty Allowance

No — write `none` explicitly IF empty.

## Section Contract

### Content

- Absolute target path and edit scope.
- Post-rewrite capabilities aligned with target §1–2 and §4.
- Inventory of every package member with role and action (keep / tighten / relocate / archive / create / omit).
- Why for each material edit.
- Residual risks (e.g. peer META References stale; WORKFLOW sync).

### Authoring

- Concise operator chat; do NOT paste full VALIDATION dump unless blockers remain.
- Do NOT claim behavioural effectiveness without a fresh-session pressure test.
