# Improve-run decisions

Enumerated decisions for `/owcc-skill-improve`, IN **[SKILL.md](SKILL.md)** workflow order. Package shape: [OUTPUTS.md](OUTPUTS.md). Rubric: [VALIDATION.md](VALIDATION.md).

## Index

| # | Decision | Workflow step |
|---|----------|---------------|
| 1 | [Target skill directory](#1-target-skill-directory) | 5.3.1 |
| 2 | [Edit scope](#2-edit-scope) | 5.3.1 |
| 3 | [Workspace overlap read](#3-workspace-overlap-read) | 5.3.3 |
| 4 | [Optional siblings for target](#4-optional-siblings-for-target) | 5.3.4 |
| 5 | [Sibling disposition](#5-sibling-disposition) | 5.3.7 |
| 6 | [Description rewrite](#6-description-rewrite) | 5.3.6 |
| 7 | [Discipline Excuse→Reality](#7-discipline-excusereality) | 5.3.6 |
| 8 | [Fidelity disposition](#8-fidelity-disposition) | 5.3.10 |

---

## 1. Target skill directory

**Workflow:** 5.3.1

| Option | Description | Choose when | Apply to |
|--------|-------------|-------------|----------|
| **Use given path** | Edit the skill directory at the absolute path | User gives absolute path to a skill folder | That directory |
| **Resolve from @** | Use directory of the @-attached SKILL.md or folder | User @-tags a skill file or folder | Parent skill package root |
| **Ask operator** | One-line ask for absolute path | Path missing or two+ candidates | Do not guess |

**Not valid:** arbitrary newest skill under `~/.cursor/skills` without chat linkage; rename of `name:` or folder unless user explicitly requested rename.

---

## 2. Edit scope

**Workflow:** 5.3.1

| Option | Description | Choose when | Apply to |
|--------|-------------|-------------|----------|
| **Full pass** | SKILL.md + all semantic siblings + scripts | Default; user did not narrow | Entire package |
| **Siblings only** | Rewrite/migrate siblings; minimal SKILL touch for links | User asked siblings-only | Roles except keep §5 stable unless link fix required |
| **SKILL only** | Rewrite SKILL.md spine; leave siblings unless broken links | User asked SKILL-only | SKILL.md; fix CS-PKG-REFS-EXIST only |

IF unclear, THEN use **Full pass**.

---

## 3. Workspace overlap read

**Workflow:** 5.3.3

| Option | Description | Choose when | Apply to |
|--------|-------------|-------------|----------|
| **READ workspace** | READ AGENTS.md, `.cursor/rules`, nearby skills for overlap | Workspace root IS known | Deduplicate policy into canonical home |
| **Ask once** | Ask whether to skip overlap or which root to use | No workspace root | One question; THEN proceed |
| **Skip overlap** | Do not scan repo policy | User said skip OR ask answered skip | Package-only improve |

---

## 4. Optional siblings for target

**Workflow:** 5.3.4

Always CREATE/KEEP required roles: `SKILL.md`, `RESPONSE.md`, `VALIDATION.md`, `META.md`, `WORKFLOW.yaml`.

| Option | Description | Choose when | Apply to |
|--------|-------------|-------------|----------|
| **Include DECISIONS.md** | WRITE decision matrices | Target workflow branches OR needs judgment tables | DECISIONS.md |
| **Omit DECISIONS.md** | No decision file | Linear workflow; no meaningful matrices | Do not CREATE |
| **Include OUTPUTS.md** | WRITE file/package output contracts | Target produces files, configs, or a structured package | OUTPUTS.md |
| **Omit OUTPUTS.md** | Chat-only skill | No structured file/package output | Do not CREATE |
| **Include EXAMPLES.md** | Sparse before/after examples | Concrete examples reduce misfires | EXAMPLES.md |
| **Omit EXAMPLES.md** | No examples | Examples would stale or bloat | Do not CREATE |

This improve skill forces the **new package shape** on targets: §1–7 SKILL + required siblings (including `WORKFLOW.yaml`); optional rows above still apply.

---

## 5. Sibling disposition

**Workflow:** 5.3.7

| Option | Description | Choose when | Apply to |
|--------|-------------|-------------|----------|
| **Keep** | Leave content as-is | Already matches role contract | That file |
| **Tighten** | Compress unused bulk; keep requirements | Role correct; prose bloated | That file |
| **Relocate** | MOVE substance into correct role | Wrong file OR legacy `reference-*` | Destination role per OUTPUTS |
| **Archive** | Archive THEN remove from package | Legacy/orphan after relocate complete | `reference-*`, dead templates |

Do NOT silently DELETE requirements — Relocate or Tighten first.

---

## 6. Description rewrite

**Workflow:** 5.3.6

| Option | Description | Choose when | Apply to |
|--------|-------------|-------------|----------|
| **Trigger-only** | Keep/rewrite description as when-to-use only | Default; description leaks workflow steps | Frontmatter `description` |
| **Align body** | Fix description claims that mismatch body | CS-DESC-BODY-ALIGN failure | description AND/OR body |

IF description summarises workflow steps, THEN REWRITE to trigger-only AND MOVE detail into §5.

---

## 7. Discipline Excuse→Reality

**Workflow:** 5.3.6

| Option | Description | Choose when | Apply to |
|--------|-------------|-------------|----------|
| **Add table** | Suggest Excuse → Reality loophole table | Target IS discipline-enforcing (forbids agent rationalizations) | SKILL §5.2 or VALIDATION |
| **Skip** | No table | Target IS not discipline-enforcing | — |

---

## 8. Fidelity disposition

**Workflow:** 5.3.10

| Option | Description | Choose when | Apply to |
|--------|-------------|-------------|----------|
| **Relocate** | MOVE requirement to correct section/role | Substance still needed | Inventory item |
| **Compress** | Shorten without losing meaning | Duplicated OR verbose | Same location |
| **User-approved drop** | DELETE inventoried requirement | User explicitly approved IN chat | Remove from inventory; note IN RESPONSE |
| **Block** | Stop improve as incomplete | Cannot restore without inventing | Report blocker; do NOT claim done |
