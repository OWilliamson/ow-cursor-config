# Improve rule — examples

## Example 1: CR-DEAD-RULE — alwaysApply: false with no globs

### Before

```yaml
---
description: Always use UTC for date handling; never use local time in stored data.
alwaysApply: false
---

Never store local time in the database. Always convert to UTC before persisting.
```

This rule never fires automatically. `alwaysApply: false` with no `globs` = dead rule.

### After (option A — make it always-on, it's a short universal constraint)

```yaml
---
description: Enforce UTC-only date storage; never persist local time.
alwaysApply: true
---

Never store local time in the database. Always convert to UTC before persisting.
```

### After (option B — scope it to files where date handling occurs)

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
description: >-
  When editing TypeScript files: check for any type, verify strict null checks
  are handled, ensure no implicit returns, and confirm exports are typed.
```

This description summarises four internal workflow steps. The agent may follow the description instead of reading the body.

### After

```yaml
description: TypeScript strict-mode conventions for this project. Applies when editing .ts and .tsx files.
```

Detail moves into the rule body where it belongs.

---

## Example 3: CR-SCOPE-EXCLUSIVE — body contradicts alwaysApply: true

### Before

```yaml
---
description: Naming conventions for React components.
alwaysApply: true
---

When editing React component files, use PascalCase for component names...
```

The body says "when editing React component files" but the rule loads everywhere (`alwaysApply: true`). When editing a migration file, this rule fires but its guidance doesn't apply.

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
