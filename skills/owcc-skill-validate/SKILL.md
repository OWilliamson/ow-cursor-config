---
name: owcc-skill-validate
description: >-
  Read-only audit of a Cursor skill package against owcc-skill-improve
  VALIDATION.md (CS-* + new package shape). Use when checking a skill directory
  before shipping without rewriting it.
disable-model-invocation: true
---

# 1. Validate Cursor skills

The aim of invoking owcc-skill-validate is to audit a target skill package read-only against the improve-skill validation rubric and report findings in chat — without modifying the target.

Explicit-only. Invoke with `/owcc-skill-validate`.

## 2. When to use

- Operator wants a skill package checked for authoring quality before shipping.
- Operator wants read-only findings (norm IDs, severity) — NOT an improve rewrite.
- Goal IS verify full-package structure, wording, links, token budget, and hygiene against the canonical CS-* shape.

## 3. Inputs

| Signal | How to act |
|--------|------------|
| Absolute path to skill directory | Target ([DECISIONS §1](DECISIONS.md#1-target-skill-directory)) |
| `@` on `SKILL.md` or skill folder | Resolve package root as target |
| Pasted full skill package | Treat as target contents; ask for path IF reporting needs one |
| `full` (default) | Full package audit |
| No path / ambiguous | Ask once; do NOT guess |

## 4. Scope

**In scope:** READ target package; inventory files; RUN improve VALIDATION mechanical checks, CS-* norms, and filtered agent questions; OUTPUT chat report per [RESPONSE.md](RESPONSE.md).

**Out of scope:** MODIFY, DELETE, CREATE, WRITE, REWRITE, or archive anything IN the **target** package; invoking full `/owcc-skill-improve` §5 mutation; fixing findings; duplicating the CS-* table into this package; hyperlinking META from SKILL.

## 5. Workflow

### 5.1. Workflow Operators

These operator words mark specific operations in the workflow. When used as operators, they must be capitalised. When used for ordinary meaning (not as an operator), they must be lower case.

| Operator | Meaning | Example |
|----------|---------|---------|
| IF | Conditional test | IF path missing, THEN ask |
| THEN | Consequence of IF | IF Critical finding, THEN report |
| ELSE | Alternate branch | ELSE skip question |
| AND | Conjoin requirements | READ inventory AND RUN checks |
| NOT | Negation / forbid | do NOT MODIFY target |
| IS | Equality / state check | IF overall IS fail |
| IN | Location / membership | findings IN report |
| CREATE | Make a new file | (forbidden on target) |
| MODIFY | Change existing content | (forbidden on target) |
| DELETE | Remove | (forbidden on target) |
| RUN | Execute a check | RUN mechanical commands |
| READ | Load a document | READ improve VALIDATION.md |
| WRITE | Produce content at a path | (forbidden on target) |
| REWRITE | Replace content | (forbidden on target) |
| SKIP TO | Jump forward | SKIP TO 5.3.5 |
| RETURN TO | Go back | RETURN TO 5.3.1 IF path wrong |
| WHILE | Repeat | WHILE files remain, classify |
| DECIDE | Choose via matrix | DECIDE target per DECISIONS §1 |
| OUTPUT | Emit completion response | OUTPUT §7 |

### 5.2. Workflow Rules

- Carry out steps top to bottom; meet each **Outcome** before continuing.
- Stay within §4; when a step links a doc, READ that section for the step.
- Apply §5.1 operator capitalisation in step bodies; do not shout ordinary prose.
- Never MODIFY/DELETE/CREATE/WRITE/REWRITE/ARCHIVE the audit **target**.
- Never invoke `/owcc-skill-improve` full workflow; only RUN its VALIDATION rubric via this skill’s §6.
- On validation failure: report AND stop — do NOT RETURN TO improve §5 to fix.
- Shape norms (`CS-PKG-SHAPE`, `CS-PKG-SKILL-SPINE`, `CS-PKG-WORKFLOW-SYNC`, no live `reference-*`) are always Critical ([DECISIONS §2](DECISIONS.md#2-shape-policy)).

### 5.3. Workflow Steps

#### 5.3.1. Resolve target

1. DECIDE target per [DECISIONS §1](DECISIONS.md#1-target-skill-directory).
2. Confirm absolute path (or note pasted-only).

**Outcome:** Unambiguous target path or pasted package handle.

#### 5.3.2. Inventory package

1. List all files IN the target directory (including `scripts/` IF any).
2. Classify each file (role, legacy `reference-*`, orphan, script).

**Outcome:** Inventory table ready for the report.

#### 5.3.3. RUN improve validation rubric

1. READ [../owcc-skill-improve/VALIDATION.md](../owcc-skill-improve/VALIDATION.md).
2. READ local overrides IN [VALIDATION.md](VALIDATION.md).
3. RUN mechanical commands from improve VALIDATION against the **target**.
4. Apply every CS-* norm; treat shape norms as Critical always ([DECISIONS §2](DECISIONS.md#2-shape-policy)).
5. Answer filtered agent questions per [DECISIONS §3](DECISIONS.md#3-agent-question-filter) AND local VALIDATION.md.

**Outcome:** Findings draft with severities; passes noted.

#### 5.3.4. Label AND cap findings

1. Label each finding Critical, Suggestion, or Nice to have.
2. Mark mechanically unconfirmed items speculative.
3. Cap detailed findings at seven; list remaining norm IDs only.
4. Final sanity: only flag items worth fixing.

**Outcome:** Report-ready findings set.

#### 5.3.5. Complete

1. OUTPUT chat per [RESPONSE.md](RESPONSE.md).
2. Do NOT claim the target was changed.

**Outcome:** Operator has pass/fail report; target unchanged.

## 6. Validation

On failure of **this skill’s** process (wrong target, incomplete report), re-READ §5, resolve, re-check. Do **not** mutate the audit target to clear CS-* findings.

### 6.1. Scripted validation

None bundled. RUN mechanical commands from [../owcc-skill-improve/VALIDATION.md](../owcc-skill-improve/VALIDATION.md) against the target (see local [VALIDATION.md](VALIDATION.md)).

### 6.2. Agent questions

Answer filtered questions per local [VALIDATION.md](VALIDATION.md) AND [DECISIONS §3](DECISIONS.md#3-agent-question-filter). Skip improve-only fidelity / improve-RESPONSE / self-improve dual-target items.

### 6.3. Interrogation agent

None by default. IF operator requests, THEN read-only subagent scoped to inventory + Critical CS-* only — still no target mutation.

**Pass when:** Report delivered per RESPONSE.md; Critical findings listed or clear; target untouched.

## 7. Completion

OUTPUT chat per [RESPONSE.md](RESPONSE.md). Do NOT claim a pressure test unless done. Do NOT claim fixes were applied.
