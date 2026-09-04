---
name: owcc-skill-improve
description: >-
  Refactors full Cursor skill packages into the semantic-sibling authoring
  shape (numbered SKILL §1–7, RESPONSE, VALIDATION, META, WORKFLOW.yaml, plus
  optional DECISIONS/OUTPUTS/EXAMPLES). Use when improving a skill directory
  under ~/.cursor/skills or .cursor/skills before or after shipping.
disable-model-invocation: true
---

# 1. Improve Cursor skills

The aim of invoking owcc-skill-improve is to rewrite a target skill package into a leaner, clearer authoring shape with semantic siblings and a numbered SKILL.md spine.

Explicit-only. Invoke with `/owcc-skill-improve`.

## 2. When to use

- Operator wants a skill sharper, shorter, or less misfire-prone before or after shipping.
- Skill IS long, duplicated, vague, or inconsistent with its description.
- Operator wants a package refactor to the semantic-sibling standard — NOT review-only.

## 3. Inputs

| Signal | How to act |
|--------|------------|
| Absolute path to skill directory | Target ([DECISIONS §1](DECISIONS.md#1-target-skill-directory)) |
| `@` on `SKILL.md` or skill folder | Resolve package root as target |
| `full` / `siblings-only` / `SKILL-only` | Scope ([DECISIONS §2](DECISIONS.md#2-edit-scope)); default **full** |
| Explicit rename request | Rename only IF clearly requested; ELSE forbid |
| Domain-behaviour change ask | Allowed only IF asked; ELSE structure/authoring only |
| No path / ambiguous | Ask once; do NOT guess |

## 4. Scope

**In scope:** entire target directory; force [OUTPUTS.md](OUTPUTS.md) roles + SKILL §1–7; Relocate/Compress/CREATE/MODIFY/archive; apply [VALIDATION.md](VALIDATION.md); OUTPUT chat per [RESPONSE.md](RESPONSE.md).

**Out of scope:** domain behaviour change unless asked; rename unless asked; links to other `ow-cursor-config/skills/*` except intentional peer wrappers listed IN META References; duplicating CS-* norms into `owcc-skill-validate`; hyperlinking META from SKILL; claiming behavioural proof without a fresh-session pressure test.

## 5. Workflow

### 5.1. Workflow Operators

These operator words mark specific operations in the workflow. When used as operators, they must be capitalised. When used for ordinary meaning (not as an operator), they must be lower case.

| Operator | Meaning | Example |
|----------|---------|---------|
| IF | Conditional test | IF path missing, THEN ask |
| THEN | Consequence of IF | IF rename requested, THEN allow |
| ELSE | Alternate branch | ELSE forbid rename |
| AND | Conjoin requirements | DECIDE target AND scope |
| NOT | Negation / forbid | do NOT invent requirements |
| IS | Equality / state check | IF scope IS full |
| IN | Location / membership | READ the section IN context |
| CREATE | Make a new file or artifact | CREATE RESPONSE.md |
| MODIFY | Change existing content | MODIFY SKILL.md §4 |
| DELETE | Remove from the package | DELETE live `reference-*.md` |
| RUN | Execute a command or check | RUN mechanical commands |
| READ | Load and use a document | READ [OUTPUTS.md](OUTPUTS.md) |
| WRITE | Produce new content at a path | WRITE META.md |
| REWRITE | Replace content to a new shape | REWRITE SKILL.md to §1–7 |
| WEB SEARCH | Look up external information | WEB SEARCH only if policy unclear |
| SKIP TO | Jump forward to a later step | SKIP TO 5.3.9 |
| RETURN TO | Go back to an earlier step | RETURN TO the failing step |
| WHILE | Repeat while condition holds | WHILE scripts remain, document each |
| DECIDE | Choose via a decision matrix | DECIDE scope per [DECISIONS §2](DECISIONS.md#2-edit-scope) |
| OUTPUT | Emit the completion response | OUTPUT §7 |

### 5.2. Workflow Rules

- Carry out steps top to bottom; meet each **Outcome** before continuing.
- Stay within §4; when a step links a doc, READ that section for the step.
- Apply §5.1 operator capitalisation in step bodies; do not shout ordinary prose.
- Do NOT drop requirements — relocate or compress ([DECISIONS §8](DECISIONS.md#8-fidelity-disposition)).
- One canonical home per policy (skill, rule, or AGENTS.md); preserve user-supplied canonical wording.
- Prefer verifiable checks ([VALIDATION.md](VALIDATION.md)); SKILL links one hop (DECISIONS may point to OUTPUTS/VALIDATION).

### 5.3. Workflow Steps

#### 5.3.1. Resolve target AND scope

1. DECIDE target per [DECISIONS §1](DECISIONS.md#1-target-skill-directory).
2. DECIDE scope per [DECISIONS §2](DECISIONS.md#2-edit-scope).
3. Confirm no rename before writing; list all package files including `scripts/`.

**Outcome:** Absolute path, scope, file list.

#### 5.3.2. Inventory against OUTPUTS roles

1. READ [OUTPUTS.md](OUTPUTS.md); classify each file as allowed role, `scripts/`, legacy (`reference-*` / old spine), or orphan.
2. Build substance inventory (do NOT invent).

**Outcome:** Classification + inventory (item → destination).

#### 5.3.3. Workspace overlap

1. IF workspace root exists, THEN READ AGENTS.md, `.cursor/rules`, nearby skills ([DECISIONS §3](DECISIONS.md#3-workspace-overlap-read)).
2. ELSE ask once to skip or name a root.
3. Note external policy so improve does NOT duplicate it.

**Outcome:** Overlap notes or skip.

#### 5.3.4. DECIDE optional siblings

1. DECIDE optional siblings per [DECISIONS §4](DECISIONS.md#4-optional-siblings-for-target).
2. Always require SKILL, RESPONSE, VALIDATION, META, WORKFLOW.yaml; force §1–7; no live `reference-*` after migrate.

**Outcome:** Sibling checklist (CREATE / KEEP / OMIT).

#### 5.3.5. Plan fidelity map

1. Map inventory to SKILL §1–7 or sibling roles; mark legacy for relocate ([DECISIONS §5](DECISIONS.md#5-sibling-disposition)).

**Outcome:** Destination map with no silent drops.

#### 5.3.6. REWRITE target SKILL.md

1. REWRITE to §1–7 per OUTPUTS SKILL contract.
2. DECIDE description per [DECISIONS §6](DECISIONS.md#6-description-rewrite).
3. Move old Principles / Definition of done / Non-goals into §5.2, §6, §4.
4. WRITE §5.3 with multilevel ids, **Outcome:** lines, §5.1 operators, DECIDE links.
5. IF discipline-enforcing, THEN DECIDE [DECISIONS §7](DECISIONS.md#7-discipline-excusereality).
6. IF scope IS siblings-only, THEN SKIP TO 5.3.7 after link-only SKILL fixes.

**Outcome:** §1–7 SKILL; trigger-only description.

#### 5.3.7. WRITE OR REWRITE semantic siblings

1. CREATE/REWRITE each required AND chosen role per OUTPUTS (including WORKFLOW.yaml mirroring §5.3).
2. DECIDE disposition ([DECISIONS §5](DECISIONS.md#5-sibling-disposition)).
3. Migrate `reference-*` substance into roles; WRITE META (do NOT link from SKILL).
4. IF EXAMPLES kept, THEN prune stale ones ([EXAMPLES.md](EXAMPLES.md) sparingly).

**Outcome:** Sibling set filled; WORKFLOW.yaml present; legacy relocated.

#### 5.3.8. Scripts hygiene

1. IF no `scripts/`, THEN SKIP TO 5.3.9.
2. Trim dead code; top comment = purpose, deps, execute-vs-read; cite from §5.3 or §6.
3. Apply `CS-SCRIPT-SAFETY` AND `CS-PKG-SCRIPTS-DOCUMENTED`.

**Outcome:** Scripts documented or N/A.

#### 5.3.9. Strip legacy members

1. Archive THEN DELETE live `reference-*.md` and non-role orphans.
2. Confirm no SKILL links to removed files.

**Outcome:** Only allowed roles (+ scripts if any).

#### 5.3.10. Fidelity gate

1. Re-scan: inventory ⊆ package; DECIDE gaps per [DECISIONS §8](DECISIONS.md#8-fidelity-disposition).
2. IF Block, THEN stop; do NOT claim done.

**Outcome:** Inventory complete or blockers documented.

#### 5.3.11. Validate AND complete

1. RUN §6. IF fail, THEN RETURN TO the failing step, fix, re-validate.
2. IF pass, THEN OUTPUT §7.

**Outcome:** Validation pass (or blockers) AND completion chat.

## 6. Validation

On failure, re-READ §5, resolve, re-check.

### 6.1. Scripted validation

None bundled. RUN mechanical commands IN [VALIDATION.md](VALIDATION.md).

### 6.2. Agent questions

Answer every [VALIDATION.md](VALIDATION.md) Agent question against the **target** (AND this package when self-improving).

### 6.3. Interrogation agent

None by default. IF operator requests, THEN read-only subagent per VALIDATION.md.

**Pass when:** Critical CS-* plus `CS-PKG-SHAPE` / `CS-PKG-SKILL-SPINE` clear (or blockers reported); agent questions answered; fidelity gate passed.

## 7. Completion

OUTPUT chat per [RESPONSE.md](RESPONSE.md). Do NOT claim a pressure test unless done.
