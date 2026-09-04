# Modify-run decisions

Enumerated decisions for `/owcc-skill-modify`, IN **[SKILL.md](SKILL.md)** workflow order. Rubric: [VALIDATION.md](VALIDATION.md).

## Index

| # | Decision | Workflow step |
|---|----------|---------------|
| 1 | [Target skill directory](#1-target-skill-directory) | 5.3.1 |
| 2 | [META gate](#2-meta-gate) | 5.3.2 |
| 3 | [Change class](#3-change-class) | 5.3.4 |
| 4 | [Ambiguity](#4-ambiguity) | 5.3.4 |
| 5 | [Alignment sweep](#5-alignment-sweep) | 5.3.6 |
| 6 | [Reshape vs modify](#6-reshape-vs-modify) | 5.3.3 |
| 7 | [Maintainer sync](#7-maintainer-sync) | 5.3.7 |

---

## 1. Target skill directory

**Workflow:** 5.3.1

| Option | Description | Choose when | Apply to |
|--------|-------------|-------------|----------|
| **Use given path** | Edit the skill directory at the absolute path | User gives absolute path to a skill folder | That directory |
| **Resolve from @** | Use directory of the @-attached SKILL.md or folder | User @-tags a skill file or folder | Parent skill package root |
| **Ask operator** | One-line ask for absolute path | Path missing or two+ candidates | Do not guess |

**Not valid:** newest skill under `~/.cursor/skills` without chat linkage; rename of `name:` or folder unless explicitly requested.

---

## 2. META gate

**Workflow:** 5.3.2

| Option | Description | Choose when | Apply to |
|--------|-------------|-------------|----------|
| **Proceed** | META.md EXISTS AND IS readable; THEN READ WORKFLOW.yaml IN the same pass | META present | Continue orientation; load WORKFLOW next |
| **Hard stop (META)** | Make **zero** edits; recommend `/owcc-skill-improve` first | META.md absent, empty, or unreadable | Exit after 5.3.2 OUTPUT |
| **Hard stop (WORKFLOW)** | Make **zero** edits; recommend `/owcc-skill-improve` first | WORKFLOW.yaml absent, empty, or unreadable after META passed | Exit after 5.3.2 OUTPUT |

Do NOT invent META.md or WORKFLOW.yaml. Do NOT proceed on SKILL-only familiarity. WORKFLOW IS part of the orientation gate, not a later optional read.

---

## 3. Change class

**Workflow:** 5.3.4

| Option | Description | Choose when | Apply to |
|--------|-------------|-------------|----------|
| **Behaviour / workflow** | Steps, operators, rules, DECISIONS branches | Operator changes how the skill acts | SKILL §5 (+ DECISIONS / WORKFLOW as needed) |
| **Sibling / docs** | RESPONSE, VALIDATION, EXAMPLES, OUTPUTS, scripts docs | Operator changes contracts or examples only | Named siblings; keep §1/§4 unless asked |
| **Aims / scope** | §1 aim and/or §4 in/out of scope | Operator changes purpose or boundaries | SKILL §1/§4 THEN whole-package alignment |
| **Description / triggers** | Frontmatter description or §2 | Operator changes when-to-use signals | Frontmatter + §2; check body align |
| **Mixed** | Two or more rows above | Operator lists multiple kinds of change | Union of loci; RUN both alignment directions IF aims/scope involved |

Record the chosen class IN the change plan.

---

## 4. Ambiguity

**Workflow:** 5.3.4

| Option | Description | Choose when | Apply to |
|--------|-------------|-------------|----------|
| **Ask once** | One clarifying question; do NOT edit | Locus OR intent unclear | Chat; THEN RETURN TO 5.3.4 |
| **Assumptions IN plan** | State explicit assumptions; proceed | Operator said “use judgment” OR only one reasonable locus | Change plan assumptions section |
| **Defer to improve** | Stop without edits; recommend improve | Request IS a reshape / migrate / full spine rewrite | Exit with RESPONSE stop template |

---

## 5. Alignment sweep

**Workflow:** 5.3.6

| Option | Description | Choose when | Apply to |
|--------|-------------|-------------|----------|
| **Fit-to-aim** | Check edited content still matches current §1 AND §4 | Any non-aim/scope locus changed | Whole package vs existing aim/scope |
| **Aim-to-package** | Check package matches new §1 AND/OR §4 | §1 and/or §4 changed | Workflow, siblings, description, VALIDATION, RESPONSE |
| **Both** | RUN fit-to-aim AND aim-to-package | Mixed class including aims/scope, OR both kinds of edit occurred | Entire package |
| **Skip (no edits)** | No sweep | Hard stop or deferred; zero files changed | — |

On mismatch: MODIFY to restore alignment OR RETURN TO 5.3.4 with an updated plan. Do NOT leave silent drift.

---

## 6. Reshape vs modify

**Workflow:** 5.3.3

| Option | Description | Choose when | Apply to |
|--------|-------------|-------------|----------|
| **Modify here** | Package already has required siblings + §1–7 spine + WORKFLOW; request IS surgical | META AND WORKFLOW present; shape OK; change IS local | Continue 5.3.4 |
| **Recommend improve** | Need migrate, spine rewrite, or live `reference-*` removal | Missing required roles, old spine, or operator asked full improve | Zero edits; exit after 5.3.3 OUTPUT |

---

## 7. Maintainer sync

**Workflow:** 5.3.7

Run after alignment whenever any non-META/non-WORKFLOW-only primary edit occurred (including alignment fixes). IF the run made **zero** edits, THEN skip.

| Option | Description | Choose when | Apply to |
|--------|-------------|-------------|----------|
| **Sync both** | Update WORKFLOW.yaml to mirror §5.3 AND refresh META tree/References/timestamp | Default after any other package edit | WORKFLOW.yaml + META.md |
| **WORKFLOW only** | Mirror §5.3; META already accurate | Only §5.3 / step ids changed; tree and References unchanged | WORKFLOW.yaml |
| **META only** | Refresh tree, Scripts, References, Updated | Membership, scripts, or peer refs changed; §5.3 unchanged | META.md |
| **Verify no-op** | Confirm both already correct; no WRITE | Sync check finds no drift | Record “synced (no-op)” IN RESPONSE |

Always verify: `skill:` matches frontmatter `name`; every top-level §5.3 step has a WORKFLOW `id`; META directory tree lists current members; SKILL does NOT link META.

