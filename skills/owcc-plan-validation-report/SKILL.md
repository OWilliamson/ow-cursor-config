---
name: owcc-plan-validation-report
description: >-
  Read-only plan validation that writes a build-gate .validation.json.
  Use when the user invokes /owcc-plan-validation-report.
disable-model-invocation: true
---

# 1. Plan validation report

The aim of invoking owcc-plan-validation-report is to run structural and qualitative checks on a plan file and WRITE a workspace `.validation.json` artifact for the **non-cursor-native** build gate — without editing the plan.

Explicit-only. Invoke with `/owcc-plan-validation-report`.

## 2. When to use

- Produce a `.validation.json` build-gate artifact for **non-cursor-native** plans (paths that do not end with `.plan.md`) before execution under that gate.
- Check plan quality and structure without mutating the plan.

## 3. Inputs

| Signal | How to act |
|--------|------------|
| Plan path (absolute or workspace-relative) | Target ([DECISIONS §1](DECISIONS.md#1-target-plan)) |
| `@` on a plan file | Resolve that path as target |
| Pasted plan content | Write to a temp path only IF needed for the script; prefer a saved path |
| `--sizing lean\|full\|auto` or same-line sizing | Pass to write script ([DECISIONS §2](DECISIONS.md#2-sizing-flag)); default **lean** |
| No path / ambiguous | Ask once; do NOT guess |

## 4. Scope

**In scope:** Resolve target; RUN `plan-write-validation-report.py`; OUTPUT one chat status line per [RESPONSE.md](RESPONSE.md).

**Out of scope:** Edit the plan file; RUN cursor-native frontmatter validator; WRITE anything except the report JSON under `.cursor/plans/reports/`; suggest other skills IN chat; interpret/fix findings beyond pass/fail (operator uses the report JSON).

## 5. Workflow

### 5.1. Workflow Operators

These operator words mark specific operations in the workflow. When used as operators, they must be capitalised. When used for ordinary meaning (not as an operator), they must be lower case.

| Operator | Meaning | Example |
|----------|---------|---------|
| IF | Conditional test | IF path missing, THEN ask |
| THEN | Consequence of IF | IF ambiguous, THEN ask once |
| ELSE | Alternate branch | ELSE use chat default |
| AND | Conjoin requirements | DECIDE target AND sizing |
| NOT | Negation / forbid | do NOT edit the plan |
| IS | Equality / state check | IF result IS pass |
| IN | Location / membership | report IN `.cursor/plans/reports/` |
| RUN | Execute a command or check | RUN write script |
| READ | Load and use a document | READ [OUTPUTS.md](OUTPUTS.md) |
| WRITE | Produce new content at a path | WRITE validation JSON (via script) |
| DECIDE | Choose via a decision matrix | DECIDE target per [DECISIONS §1](DECISIONS.md#1-target-plan) |
| OUTPUT | Emit the completion response | OUTPUT §7 |

### 5.2. Workflow Rules

- Carry out steps top to bottom; meet each **Outcome** before continuing.
- Stay within §4; when a step links a doc, READ that section for the step.
- Apply §5.1 operator capitalisation in step bodies; do not shout ordinary prose.
- **Read-only on the plan** — the write script may only CREATE/UPDATE the report JSON.
- Do NOT suggest other skills IN the status line.

| Excuse | Reality |
|--------|---------|
| “Report failed — fix the plan now.” | This skill does NOT edit the plan; OUTPUT fail line only. |
| “Chat should explain every failure.” | One status line; details live IN the JSON ([OUTPUTS.md](OUTPUTS.md)). |
| “Also run frontmatter validator.” | Out of scope — cursor-native frontmatter hygiene IS not this skill. |

### 5.3. Workflow Steps

#### 5.3.1. Resolve target and sizing

1. DECIDE target per [DECISIONS §1](DECISIONS.md#1-target-plan).
2. DECIDE sizing flag per [DECISIONS §2](DECISIONS.md#2-sizing-flag).

**Outcome:** Absolute plan path; sizing `lean` | `full` | `auto`.

#### 5.3.2. Write validation report

1. RUN:

```bash
python3 ~/.cursor/skills/owcc-plan-validation-report/scripts/plan-write-validation-report.py /absolute/path/to/plan.md
```

Optional: append `--sizing lean|full|auto` (default `lean`).

2. Script orchestrates qualitative + structure + chunk **once each** (qualitative does not re-run structure); WRITEs report per [OUTPUTS.md](OUTPUTS.md).
3. Note exit code: `0` = pass, `1` = fail, `2` = runtime error ([DECISIONS §3](DECISIONS.md#3-pass-fail-semantics)).

**Outcome:** Report file on disk (or runtime error surfaced).

#### 5.3.3. Report

1. OUTPUT one chat line per [RESPONSE.md](RESPONSE.md).

**Outcome:** Operator sees path + pass|fail (or error).

## 6. Validation

On failure, re-read §5, resolve, re-check.

### 6.1. Scripted validation

RUN the write script documented IN [VALIDATION.md](VALIDATION.md). Confirm [WORKFLOW.yaml](WORKFLOW.yaml) still mirrors §5.3 when workflow steps changed.

### 6.2. Agent questions

Answer every [VALIDATION.md](VALIDATION.md) Agent question against this run.

### 6.3. Interrogation agent

None.

**Pass when:** Report JSON exists at the contracted path (or runtime error reported); chat IS one status line; plan file untouched.

## 7. Completion

OUTPUT chat per [RESPONSE.md](RESPONSE.md). Do NOT claim a pressure test unless done.
