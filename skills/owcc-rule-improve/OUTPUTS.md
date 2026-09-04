# Rule (.mdc)

Contract for the Cursor rule file `/owcc-rule-improve` mutates. Branching: [DECISIONS.md](DECISIONS.md). Workflow: [SKILL.md](SKILL.md). Rubric: [VALIDATION.md](VALIDATION.md).

## Template

```markdown
---
description: "Enforce <effect> when <trigger>."
globs:
  - "**/*.ts"
alwaysApply: false
---

# <Rule title>

## When this rule applies

- …

## Must

- …

## Must not

- …

## Checks

1. …
```

Omit `globs` when using always-on or intelligent-apply activation ([DECISIONS §4](DECISIONS.md#4-activation-mode)). Add **Boundaries** / **Auto-Clarity** / Excuse→Reality tables when CR-* require them.

## Sections

### Frontmatter

#### Use

Always.

#### Empty Allowance

No — at least `description` plus an activation strategy (`alwaysApply` and/or `globs`).

### Body title (H1)

#### Use

Always preferred for scannability.

#### Empty Allowance

Yes IF the rule IS a short always-on constraint under ~15 body lines.

### When this rule applies

#### Use

Always when activation IS not obvious from frontmatter alone.

#### Empty Allowance

Yes IF `globs` + `description` fully define scope AND body has no contradictory “only when” language.

### Must / Must not

#### Use

Always for behavioural rules.

#### Empty Allowance

No for policy rules; yes for pure checklist rules that use **Checks** only.

### Checks / Steps

#### Use

When the agent must run ordered verifications.

#### Empty Allowance

Yes IF Must/Must-not alone suffice.

### Boundaries / Auto-Clarity / Excuse→Reality

#### Use

When `CR-BOUNDARIES-EXPLICIT`, `CR-AUTO-CLARITY`, or discipline loopholes apply ([DECISIONS §7](DECISIONS.md#7-discipline-excuse-reality)).

#### Empty Allowance

Yes when not applicable.

## Section Contract

### Content

- `description`: one physical line; third person; trigger + enforcement effect; picker-readable (`CR-DESC-SINGLE-LINE`, `CR-DESC-PICKER`).
- Activation: exactly one live mode from [DECISIONS §4](DECISIONS.md#4-activation-mode); not a dead rule (`CR-DEAD-RULE`).
- Body: one primary concern (`CR-ONE-CONCERN`); roughly under ~50 lines or split ([DECISIONS §5](DECISIONS.md#5-split-strategy)).
- Links: one hop only; every linked path exists (`CR-LINKS-ONE-HOP`, `CR-RULE-REFS-EXIST`).
- No large copy-paste from AGENTS.md or sibling rules without a single canonical home (`CR-NO-DUP-AGENTS`).

### Authoring

- Prefer verifiable checks over advice.
- Verb-led edits; match specificity to fragility.
- Do NOT put workflow summaries IN `description`.
- Paired reference files stay single-purpose (`CR-RULE-SIBLINGS-LEAN`).
