# Verification-cursor decisions

Enumerated decisions for `/owcc-plan-verification-cursor`, in **[SKILL.md](SKILL.md)** workflow order. Templates: [OUTPUTS.md](OUTPUTS.md). Rubric: [VALIDATION.md](VALIDATION.md).

## Index

| # | Decision | Workflow step |
|---|----------|---------------|
| 1 | [Target plan](#1-target-plan) | 5.3.1 |
| 2 | [Closeout placement](#2-closeout-placement) | 5.3.3 |
| 3 | [Frontmatter rules](#3-frontmatter-rules) | 5.3.4 |
| 4 | [Audit vs runtime verify](#4-audit-vs-runtime-verify) | 5.3.2; build |

---

## 1. Target plan

**Workflow:** 5.3.1

| Option | Description | Choose when | Apply to |
|--------|-------------|-------------|----------|
| **Cursor-native `.plan.md`** | Mutate that file | Path ends IN `.plan.md`; typically under `.cursor/plans/` | That absolute path |
| **@ attachment** | Same | User `@` tags `.plan.md` | That path |
| **Non-cursor-native** | Refuse | Other suffix/path/shape | Stop; out of scope |
| **Ambiguous / none** | Ask once | Two+ candidates or none | Do NOT guess |

**Convention (no runtime profile detection):** `.plan.md` under workspace `.cursor/plans/`; uses Cursor Plan UI Build and composer `planRegistry`.

When path IS ambiguous among several `.plan.md` candidates, ask once — do NOT guess. Chat default: most recently discussed `.plan.md` IN this thread when invoke has no path.

---

## 2. Closeout placement

**Workflow:** 5.3.3

| Plan shape | Placement |
|------------|-----------|
| **`isProject: true`** | One closeout verify todo as the **last todo in each phase** |
| **Flat** (`isProject: false`) | One final `cursor-native-close-verify` or strengthened `completion-audit` |

Stable ids: `phase-N-close-verify` or `cursor-native-close-verify`. Templates: [OUTPUTS.md](OUTPUTS.md).

---

## 3. Frontmatter rules

**Workflow:** 5.3.4

RUN `plan-validate-frontmatter.py` after every WRITE.

### Hard rules (`isProject: true`)

| Rule | Why |
|------|-----|
| `todos: []` at root | Duplicate root + `phases[].todos` triggers Plan UI sync that can replace semantic ids with UUID shells and wipe `content` |
| Full objects under `phases[].todos` only | Each entry needs `id`, non-empty `content`, `status` |
| Stable **kebab-case** `id` values | UUID ids usually mean UI re-authored the plan; Build loses stable handoff |
| Body **First action** / **Final validation** ids exist in phase todos | Prevents prose pointing at removed ids |

### Flat plans (`isProject: false`)

- All todos under root `todos:` only — no `phases` array unless converting to project shape.
- Same non-empty `content` and kebab-case id rules.

### Recovery when Plan UI emptied todos

1. Restore frontmatter from git history, then validate again.
2. Or restore semantic todo content from chat/git IF history unavailable.

Do **not** hand-edit UUID shells in the Plan UI without restoring `content` text IN YAML.

### Body chrome (validator hard-fail)

Forbidden operator-only labels IN markdown body: `**Execution route:**`, `**Plan shape:**`, `**Native chunks:**`, `**Plan-change-composer role:**`, `**Plan-build role:**`, `**Plan-registry role:**`.

Keep **Phase rule**, **Plan file edit rule** (status-only exception — never quote Cursor's injected prohibition), **Verify** one-liner, and execution rule IN the body.

---

## 4. Audit vs runtime verify

| Script | When | Reads |
|--------|------|-------|
| `plan-audit-cursor-verification.py` | During **this skill** (mutation) | Plan file text only — gaps to fix |
| `plan-validate-frontmatter.py` | After every WRITE IN this skill | Frontmatter + body chrome rules |
| `plan-verify-close-cursor.py` | During **build** (todo content) | Live file + registry state |
| `plan-registry-show.py` | During **build** (todo content) | Registry detail |

Do NOT RUN verify-close / registry-show as the primary invoke workflow.
