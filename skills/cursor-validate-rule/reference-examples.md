# Validate rule — examples

## Example: Completed findings report

### Input rule

`~/.cursor/rules/date-handling.mdc` — single file, no siblings.

```yaml
---
description: >-
  When editing TypeScript or Python files: check for any type, verify strict null
  checks are handled, ensure no implicit returns, and confirm all exports are typed.
alwaysApply: false
---

Never use `any` type in TypeScript. Always use strict null checks...
```

### Filled-in report

---

**Target:** `~/.cursor/rules/date-handling.mdc`

**Inventory:**

| File | Type | Status |
|------|------|--------|
| date-handling.mdc | Rule entry | Target |

**Activation summary:**
- `alwaysApply`: false
- `globs`: not set
- Dead rule check (`CR-DEAD-RULE`): **FAIL** — `alwaysApply: false` with no `globs`; rule never fires automatically.
- Sample path that SHOULD match: N/A (no globs defined)
- Glob precision verdict: N/A — fix dead rule first.

**Executive pass/fail:** Fail — one Critical finding (dead rule) blocks shipping.

**Findings table:**

| Norm ID | Severity | Evidence | Minimal fix |
|---------|----------|----------|-------------|
| `CR-DEAD-RULE` | Critical | `alwaysApply: false`, no `globs` field | Add `globs: ["**/*.ts", "**/*.tsx"]` or set `alwaysApply: true` |
| `CR-DESC-WORKFLOW-SUMMARY` | Critical | description lists four internal checks ("check for any type, verify strict null checks...") | Rewrite to trigger: "TypeScript strict-mode conventions. Applies when editing .ts/.tsx files." |
| `CR-SCOPE-EXCLUSIVE` | Suggestion | description mentions Python files but body only covers TypeScript | Remove Python from scope or add Python-specific guidance |

**Passing checks:** `CR-FILE-SUFFIX` ✓, `CR-FRONTMATTER` ✓, `CR-DESC-NONEMPTY` ✓, `CR-ONE-CONCERN` ✓, `CR-RULE-REFS-EXIST` ✓, `CR-ANTI-WIN-PATHS` ✓, `CR-NO-TIME-BOMBS` ✓.

**Speculative items:**

| Item | What would confirm it |
|------|----------------------|
| `CR-ALWAYS-ON-BUDGET`: cannot assess without listing all other rules in `.cursor/rules/` | List all `alwaysApply: true` rules and sum line counts |

**Follow-up question:** None — Critical findings are clear.

---

## Notes

- Quote evidence verbatim; do not paraphrase.
- Always complete the activation summary before the findings table — a dead rule invalidates glob precision checks.
- Never skip the passing checks list; omitting them makes the report look like all-fail.
