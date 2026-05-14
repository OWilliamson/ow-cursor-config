# Improve skill — examples

## Example 1: CS-DESC-WORKFLOW-SUMMARY — description summarises workflow steps

The agent may follow the description instead of reading the body. Strip internal steps; leave only when-to-use trigger.

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

## Example 2: Long SKILL.md body with principles duplicated in reference doc

### Before (SKILL.md, ~30-line Principles section)

```markdown
## Principles

- Always check frontmatter before touching the body.
- Verify every link resolves. A broken link is a critical finding.
- Descriptions must be in third person and answer "when should this skill be used?"
- Keep body under 500 lines. Split if over.
- Use binary pass/fail checks over advisory prose.
- Preserve user-supplied wording verbatim when it exists.
- One canonical home per policy; do not duplicate across skill, rule, and AGENTS.md.
```

(All seven items are restated word-for-word in `reference-cursor-authoring-norms.md`.)

### After (SKILL.md — compressed to non-obvious constraints only)

```markdown
## Principles

0. Treat the package as the unit; every file in scope.
1. Do not drop requirements. Relocate or compress instead.
2. One canonical home per policy: skill, rule, or AGENTS.md.
3. Keep SKILL.md procedural; deep reference one hop away.
4. Preserve user-supplied canonical wording verbatim.
```

(Generic checks like "descriptions must be third person" belong in the reference doc, not here.)
