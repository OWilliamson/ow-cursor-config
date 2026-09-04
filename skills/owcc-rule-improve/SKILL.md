---
name: owcc-rule-improve
description: >-
  Refactors a Cursor project rule (.mdc) into a leaner, clearer, less
  drift-prone shape. Use when improving a rule under .cursor/rules before or
  after shipping.
disable-model-invocation: true
---

# 1. Improve Cursor rules

The aim of invoking owcc-rule-improve is to rewrite a target `.mdc` toward a lean frontmatter + body spine, apply CR-* norms, and report the change without dropping inventoried requirements.

Explicit-only. Invoke with `/owcc-rule-improve`.

## 2. When to use

- Operator wants a rule sharper, shorter, or less misfire-prone before or after shipping.
- Rule IS long, duplicated, vague, or inconsistent with its frontmatter `description`.
- Operator wants a rule refactor — NOT review-only (`/owcc-rule-validate`).

## 3. Inputs

| Signal | How to act |
|--------|------------|
| Absolute path to a `.mdc` file | Target ([DECISIONS §1](DECISIONS.md#1-target-rule-file)) |
| `@` on a `.mdc` file | Resolve that path as target |
| `full` / `frontmatter-only` / `body-only` | Scope ([DECISIONS §2](DECISIONS.md#2-edit-scope)); default **full** |
| Explicit rename request | Rename only IF clearly requested; ELSE forbid |
| Domain-policy change ask | Allowed only IF asked; ELSE structure/authoring only |
| No path / ambiguous | Ask once; do NOT guess |

## 4. Scope

**In scope:** mutate the target `.mdc` (and clearly paired same-directory linked siblings); RUN CR-* checks IN [VALIDATION.md](VALIDATION.md); Relocate/Compress inventory; verify activation samples; OUTPUT chat per [RESPONSE.md](RESPONSE.md).

**Out of scope:** domain policy change unless asked; rename unless asked; duplicating prose that belongs IN `AGENTS.md`, another rule, or a skill; links to other `ow-cursor-config/skills/*` except META Reference To peers; claiming behavioural proof without a fresh-session pressure test; hyperlinking META from SKILL.

## 5. Workflow

### 5.1. Workflow Operators

Capitalise these only when used as operators; lower case for ordinary meaning.

| Operator | Meaning | Example |
|----------|---------|---------|
| IF / THEN / ELSE | Conditional | IF path missing, THEN ask |
| AND / NOT / IS / IN | Logic / membership | IF scope IS full |
| CREATE / MODIFY / DELETE | File mutations | MODIFY frontmatter |
| RUN / READ / WRITE / REWRITE | Execute or edit | READ [OUTPUTS.md](OUTPUTS.md) |
| SKIP TO / RETURN TO / WHILE | Control flow | RETURN TO failing step |
| DECIDE / OUTPUT | Branch / complete | DECIDE [DECISIONS §4](DECISIONS.md#4-activation-mode); OUTPUT §7 |

### 5.2. Workflow Rules

- Steps top to bottom; meet each **Outcome** before continuing.
- Stay within §4; READ linked docs when a step cites them.
- Apply §5.1 operator capitalisation; do not shout ordinary prose.
- Do NOT drop requirements — Relocate or Compress ([DECISIONS §8](DECISIONS.md#8-fidelity-disposition)).
- One canonical home per policy; preserve user-supplied canonical wording.
- Prefer verifiable checks ([VALIDATION.md](VALIDATION.md)); SKILL links one hop.

| Excuse | Reality |
|--------|---------|
| “Description lists the steps — skip the body.” | Trigger-only `description`; detail IN body ([DECISIONS §6](DECISIONS.md#6-description-rewrite)). |
| “Always-on is easier than globs.” | Prefer scoped activation ([DECISIONS §4](DECISIONS.md#4-activation-mode)). |
| “Awkward requirement — drop it.” | Relocate/Block; DELETE only with user approval ([DECISIONS §8](DECISIONS.md#8-fidelity-disposition)). |
| “Over budget — two always-on rules.” | Prefer one-hop sibling first ([DECISIONS §5](DECISIONS.md#5-split-strategy)). |

### 5.3. Workflow Steps

#### 5.3.1. Resolve target AND scope

1. DECIDE target per [DECISIONS §1](DECISIONS.md#1-target-rule-file).
2. DECIDE scope per [DECISIONS §2](DECISIONS.md#2-edit-scope).
3. Confirm `.mdc` path AND no rename before writing; list linked same-directory siblings.

**Outcome:** Absolute `.mdc` path, scope, sibling list.

#### 5.3.2. Workspace overlap

1. IF workspace root exists, THEN READ AGENTS.md, `.cursor/rules/`, nearby skills ([DECISIONS §3](DECISIONS.md#3-workspace-overlap-read)); check `~/.cursor/rules/` for same-topic rules (`CR-SCOPE-LAYER`).
2. ELSE ask once to skip or name a root.
3. Note external policy so improve does NOT duplicate it.

**Outcome:** Overlap notes or skip.

#### 5.3.3. Inventory target AND siblings

1. READ [OUTPUTS.md](OUTPUTS.md); classify `.mdc` and linked siblings.
2. Build substance inventory (do NOT invent).
3. Apply `CR-RULE-NO-ORPHANS`, `CR-RULE-REFS-EXIST`, `CR-RULE-SIBLINGS-LEAN` when siblings exist.

**Outcome:** Classification + inventory (item → destination).

#### 5.3.4. Audit frontmatter AND activation

1. Parse frontmatter; enforce one-line picker-readable `description` (`CR-DESC-SINGLE-LINE`, `CR-DESC-PICKER`).
2. DECIDE activation ([DECISIONS §4](DECISIONS.md#4-activation-mode)); dead-rule check (`CR-DEAD-RULE`).
3. IF globs present, THEN state one matching AND one non-matching path (`CR-GLOB-PRECISION`).
4. Review always-on budget (`CR-ALWAYS-ON-BUDGET`; optional `npx cursor-doctor budget`) AND inter-rule conflicts (`CR-INTER-RULE-CONFLICT`).

**Outcome:** Activation plan + frontmatter findings ready to apply.

#### 5.3.5. REWRITE rule

1. REWRITE body toward [OUTPUTS.md](OUTPUTS.md) spine: when → must/must-not → checks.
2. DECIDE description ([DECISIONS §6](DECISIONS.md#6-description-rewrite)).
3. IF multi-concern or over budget, THEN DECIDE split ([DECISIONS §5](DECISIONS.md#5-split-strategy)).
4. IF discipline-enforcing, THEN DECIDE Excuse→Reality ([DECISIONS §7](DECISIONS.md#7-discipline-excuse-reality)).
5. Add Boundaries / Auto-Clarity when needed; handle siblings without silent drops. IF activation examples help, THEN READ [EXAMPLES.md](EXAMPLES.md).

**Outcome:** Lean `.mdc` matching OUTPUTS; siblings handled.

#### 5.3.6. Fidelity gate

1. Re-scan inventory ⊆ rewritten rule (+ siblings).
2. DECIDE gaps per [DECISIONS §8](DECISIONS.md#8-fidelity-disposition).
3. IF Block, THEN stop; do NOT claim done.

**Outcome:** Inventory complete or blockers documented.

#### 5.3.7. Validate AND complete

1. RUN §6. IF fail, THEN RETURN TO the failing step, fix, re-validate.
2. IF pass, THEN OUTPUT §7.

**Outcome:** Validation pass (or blockers) AND completion chat.

## 6. Validation

On failure, re-READ §5, resolve, re-check.

### 6.1. Scripted validation

None bundled. RUN mechanical commands IN [VALIDATION.md](VALIDATION.md).

### 6.2. Agent questions

Answer every [VALIDATION.md](VALIDATION.md) Agent question against the **target** `.mdc`.

### 6.3. Interrogation agent

None by default. IF operator requests, THEN read-only subagent scoped to Critical CR-* + activation samples.

**Pass when:** Critical CR-* clear (or blockers reported); activation samples stated; agent questions answered; fidelity gate passed.

## 7. Completion

OUTPUT chat per [RESPONSE.md](RESPONSE.md). Do NOT claim a pressure test unless done.
