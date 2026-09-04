# Improve-run decisions

Enumerated decisions for `/owcc-rule-improve`, IN **[SKILL.md](SKILL.md)** workflow order. Target shape: [OUTPUTS.md](OUTPUTS.md). Rubric: [VALIDATION.md](VALIDATION.md).

## Index

| # | Decision | Workflow step |
|---|----------|---------------|
| 1 | [Target rule file](#1-target-rule-file) | 5.3.1 |
| 2 | [Edit scope](#2-edit-scope) | 5.3.1 |
| 3 | [Workspace overlap read](#3-workspace-overlap-read) | 5.3.2 |
| 4 | [Activation mode](#4-activation-mode) | 5.3.4 |
| 5 | [Split strategy](#5-split-strategy) | 5.3.5 |
| 6 | [Description rewrite](#6-description-rewrite) | 5.3.5 |
| 7 | [Discipline Excuse-Reality](#7-discipline-excuse-reality) | 5.3.5 |
| 8 | [Fidelity disposition](#8-fidelity-disposition) | 5.3.6 |

---

## 1. Target rule file

**Workflow:** 5.3.1

| Option | Description | Choose when | Apply to |
|--------|-------------|-------------|----------|
| **Use given path** | Edit the `.mdc` at the absolute path | User gives absolute path to a rule file | That file |
| **Resolve from @** | Use the @-attached `.mdc` path | User @-tags a rule file | That path |
| **Ask operator** | One-line ask for absolute path | Path missing, not `.mdc`, or two+ candidates | Do not guess |

**Not valid:** inventing a new rule path; rename of the `.mdc` unless user explicitly requested rename.

---

## 2. Edit scope

**Workflow:** 5.3.1

| Option | Description | Choose when | Apply to |
|--------|-------------|-------------|----------|
| **Full pass** | Frontmatter + body + linked siblings | Default; user did not narrow | Entire target (+ paired refs) |
| **Frontmatter only** | Activation / description / globs only | User asked frontmatter-only | YAML frontmatter |
| **Body only** | Keep activation; rewrite body | User asked body-only | Body below frontmatter |

IF unclear, THEN use **Full pass**.

---

## 3. Workspace overlap read

**Workflow:** 5.3.2

| Option | Description | Choose when | Apply to |
|--------|-------------|-------------|----------|
| **READ workspace** | READ AGENTS.md, `.cursor/rules/`, nearby skills; check `~/.cursor/rules/` for same topic | Workspace root IS known | Deduplicate policy into canonical home |
| **Ask once** | Ask whether to skip overlap or which root to use | No workspace root | One question; THEN proceed |
| **Skip overlap** | Do not scan repo policy | User said skip OR ask answered skip | Target-only improve |

---

## 4. Activation mode

**Workflow:** 5.3.4

| Option | Description | Choose when | Apply to |
|--------|-------------|-------------|----------|
| **Always-on** | `alwaysApply: true` | Short universal constraint; contributes to always-on budget | Frontmatter |
| **Glob-scoped** | `alwaysApply: false` + `globs` | Guidance applies only to matching paths | Frontmatter |
| **Intelligent apply** | `alwaysApply: false`, no `globs`, one-line `description` | Agent should apply from description trigger | Frontmatter |
| **Dead — fix** | Was `alwaysApply: false` with no globs and no meaningful description | Never fires automatically (`CR-DEAD-RULE`) | Pick one of the three live modes above |

Avoid `alwaysApply: true` plus body text that says “only when editing X” without bridging (`CR-SCOPE-EXCLUSIVE`).

---

## 5. Split strategy

**Workflow:** 5.3.5

| Option | Description | Choose when | Apply to |
|--------|-------------|-------------|----------|
| **Keep one rule** | Compress body; stay under ~50-line concern budget | Single concern; over length only | Same `.mdc` |
| **Sibling reference** | MOVE detail to one-hop `reference-*.md` linked from the rule | Detail needed; same activation | Paired file + link |
| **True rule split** | Two `.mdc` files, separate activations | Unrelated concerns with distinct scopes | New `.mdc` + narrower globs each |

Prefer sibling reference before true split. True split needs user-visible second file and distinct globs/descriptions.

---

## 6. Description rewrite

**Workflow:** 5.3.5

| Option | Description | Choose when | Apply to |
|--------|-------------|-------------|----------|
| **Trigger-only** | Keep/rewrite as when-to-apply one-liner | Default; description leaks workflow steps | Frontmatter `description` |
| **Align body** | Fix description claims that mismatch body | `CR-DESC-BODY-ALIGN` failure | description AND/OR body |

IF description summarises workflow steps, THEN REWRITE to trigger-only AND MOVE detail into the body. Keep **one physical line** — never `>-` / `|` (`CR-DESC-SINGLE-LINE`).

---

## 7. Discipline Excuse-Reality

**Workflow:** 5.3.5

| Option | Description | Choose when | Apply to |
|--------|-------------|-------------|----------|
| **Add table** | Add Excuse → Reality loophole table | Target IS discipline-enforcing | Rule body |
| **Skip** | No table | Target IS not discipline-enforcing | — |

---

## 8. Fidelity disposition

**Workflow:** 5.3.6

| Option | Description | Choose when | Apply to |
|--------|-------------|-------------|----------|
| **Relocate** | MOVE requirement to correct section/sibling | Substance still needed | Inventory item |
| **Compress** | Shorten without losing meaning | Duplicated OR verbose | Same location |
| **User-approved drop** | DELETE inventoried requirement | User explicitly approved IN chat | Remove from inventory; note IN RESPONSE |
| **Block** | Stop improve as incomplete | Cannot restore without inventing | Report blocker; do NOT claim done |
