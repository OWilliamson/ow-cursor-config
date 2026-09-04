# Examples

Sparse references for `/owcc-rule-improve`. Use only when a workflow step needs a concrete pattern.

## Example 1: CR-DEAD-RULE — alwaysApply false with no globs

### Before

```yaml
---
description: Always use UTC for date handling; never use local time in stored data.
alwaysApply: false
---

Never store local time in the database. Always convert to UTC before persisting.
```

`alwaysApply: false` with no `globs` and a description that does not drive intelligent apply as intended often never fires. Prefer an explicit live mode.

### After (option A — always-on for a short universal constraint)

```yaml
---
description: Enforce UTC-only date storage; never persist local time.
alwaysApply: true
---

Never store local time in the database. Always convert to UTC before persisting.
```

### After (option B — glob-scoped)

```yaml
---
description: Enforce UTC-only date storage when writing models or migrations.
globs:
  - "**/models/**"
  - "**/migrations/**"
alwaysApply: false
---

Never store local time in the database. Always convert to UTC before persisting.
```

---

## Example 2: CR-DESC-WORKFLOW-SUMMARY — description substitutes for body

### Before

```yaml
description: When editing TypeScript files: check for any type, verify strict null checks are handled, ensure no implicit returns, and confirm exports are typed.
```

### After

```yaml
description: TypeScript strict-mode conventions for this project. Applies when editing .ts and .tsx files.
```

Detail moves into the rule body.

---

## Example 3: CR-DESC-SINGLE-LINE — folded YAML description breaks Cursor UI

### Before

```yaml
---
description: >-
  Apply when the user reports an issue, bug, regression, or failure, or asks to
  investigate, diagnose, debug, or find root cause of broken behaviour.
alwaysApply: false
---
```

### After

```yaml
---
description: Apply when the user reports an issue, bug, regression, or failure, or asks to investigate, diagnose, debug, or find root cause.
alwaysApply: false
---
```

One physical line. Quote IF colons could confuse a naive parser: `description: "Apply when editing API routes: validate input and status codes."`

---

## Example 4: CR-SCOPE-EXCLUSIVE — body contradicts alwaysApply true

### Before

```yaml
---
description: Naming conventions for React components.
alwaysApply: true
---

When editing React component files, use PascalCase for component names...
```

### After

```yaml
---
description: Naming conventions for React components.
globs:
  - "**/*.tsx"
  - "**/components/**/*.ts"
alwaysApply: false
---

Use PascalCase for component names...
```
