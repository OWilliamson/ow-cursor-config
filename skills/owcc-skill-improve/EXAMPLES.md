# Examples

Sparse references for `/owcc-skill-improve`. Use only when a workflow step needs a concrete pattern.

## Example 1: CS-DESC-WORKFLOW-SUMMARY — description summarises workflow

The agent may follow the description instead of reading the body. Strip internal steps; leave trigger-only wording.

### Before

```yaml
description: >-
  Reviews SKILL.md for quality. Runs wc -l, checks frontmatter fields,
  resolves all links, and produces a severity-labelled findings report.
```

### After

```yaml
description: >-
  Validates a Cursor skill package against authoring norms. Use when
  checking a skill for quality issues before shipping.
```

---

## Example 2: Migrate old Principles dump into §5.2 + VALIDATION

### Before (unnumbered SKILL.md)

```markdown
## Principles

- Always check frontmatter before touching the body.
- Verify every link resolves. A broken link is a critical finding.
- Descriptions must be in third person and answer "when should this skill be used?"
- Keep body under 500 lines. Split if over.
- Use binary pass/fail checks over advisory prose.
```

(Norms duplicated IN `reference-cursor-authoring-norms.md`.)

### After

- SKILL §5.1 holds the operator table; §5.2 holds only non-obvious execution rules (order, Outcome, scope, READ linked docs).
- Generic CS-* checks live IN VALIDATION.md — not restated IN SKILL.
- Package uses RESPONSE / OUTPUTS / VALIDATION / META roles instead of `reference-*`.

---

## Example 3: Target forced to §1–7 spine

### Before (excerpt)

```markdown
# My skill
## When to use
## Required inputs
## Definition of done
## Non-goals
## Workflow
```

### After (excerpt)

```markdown
# 1. My skill
## 2. When to use
## 3. Inputs
## 4. Scope
## 5. Workflow
### 5.1. Workflow Operators
### 5.2. Workflow Rules
### 5.3. Workflow Steps
## 6. Validation
## 7. Completion
```
