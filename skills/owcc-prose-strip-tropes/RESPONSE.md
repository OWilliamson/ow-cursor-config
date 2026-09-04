# Completion response

Chat/session OUTPUT when `/owcc-prose-strip-tropes` finishes. Cited from SKILL.md §7.

## Template

```markdown
## Prose strip tropes — complete

**Target:** <absolute path | paste | chat-turn: …>
**Mode:** rewrite | audit

### Findings

| Severity | Category | Locus | Action |
|----------|----------|-------|--------|
| must-fix\|should-fix\|note\|keep\|ask-user | C# name | quote or path#section | fixed \| left \| n/a |

### Changes

- <what changed> (or `none` for audit / clean target)

### Rewritten text

<IF paste or chat-turn target AND mode IS rewrite: full cleaned prose here>
<IF file target OR audit: omit this section or write `n/a — file updated` / `n/a — audit only`>
```

## Sections

### Findings

#### Use

Always — one row per finding, or a single row `none` IF no hits.

#### Empty Allowance

No for the section; use explicit `none`.

### Changes

#### Use

Always.

#### Empty Allowance

No — write `none` when audit-only or when no edits were needed.

### Rewritten text

#### Use

When mode IS rewrite AND target IS paste or chat-turn.

#### Empty Allowance

Yes — omit or `n/a` for file rewrites and audits.

## Section Contract

### Content

- Absolute path or clear non-file target label.
- Mode.
- Findings with category ids from DECISIONS §4 (C1–C15) and severities from §5.
- What was changed (or `none`).
- Full cleaned prose only for non-file rewrite targets.

### Authoring

- Operator-facing; concise.
- Do NOT suggest other skills.
- Do NOT claim authorship (“written by an LLM”).
- Do NOT paste the entire large file body when the file was MODIFYed on disk — summarize changes and point at the path.
