---
name: owcc-plan-triage
description: >-
  Interrogates draft plans for substance gaps and patches clear fixes in the
  same run. Use when the user invokes /owcc-plan-triage on a saved plan before build.
disable-model-invocation: true
---

# 1. Plan triage

The aim of invoking owcc-plan-triage is to interrogate a draft plan for substance gaps (session intent, contradictions, loose ends, executor info gaps) and **patch** clear fixes in the same run — without resizing or restructuring for form.

Explicit-only. Invoke with `/owcc-plan-triage` in an **Agent** chat. Prefer **@**-attach the plan file in the same message.

**Shape B:** interrogate, then patch (substance only). No per-finding approval gate.

## 2. When to use

- Draft plan saved before build — substance needs interrogation.
- Session asks may not be fully reflected in the plan.
- Plan may have internal contradictions, loose scope boundaries, or executor info gaps.
- Re-run after plan content changes or new user requirements in the same session.

## 3. Inputs

| Signal | How to act |
|--------|------------|
| Plan path (absolute or workspace-relative) | Target ([DECISIONS §1](DECISIONS.md#1-target-plan)) |
| `@` on a plan file | Resolve that path as target |
| Pasted plan content | Prefer a saved path; IF paste-only, ask to save first when edits needed |
| No path / ambiguous | Ask once; do NOT guess |

## 4. Scope

**In scope:** Harvest user-only session asks; READ plan; bounded workspace spot-checks; four-axis interrogation with severity; MODIFY plan substance when locus is clear; OUTPUT chat delta.

**Out of scope:** Lean/full reshape, rephase, or rescale todos; strip/merge Rules execution-contract chrome; add verify-twin todos for form; WRITE `.validation.json`; inject cursor-native closeout; decide “do not build”; suggest other skills IN output; invent session asks the user never endorsed.

## 5. Workflow

### 5.1. Workflow Operators

These operator words mark specific operations in the workflow. When used as operators, they must be capitalised. When used for ordinary meaning (not as an operator), they must be lower case.

| Operator | Meaning | Example |
|----------|---------|---------|
| IF | Conditional test | IF ambiguous, THEN ask-user |
| THEN | Consequence of IF | IF clear locus, THEN patch |
| ELSE | Alternate branch | ELSE report only |
| AND | Conjoin requirements | DECIDE severity AND patch |
| NOT | Negation / forbid | do NOT invent asks |
| IS | Equality / state check | IF severity IS blocker |
| IN | Location / membership | ask IN this chat session |
| CREATE | Make a new artifact | CREATE todo when absent ask |
| MODIFY | Change existing content | MODIFY plan substance |
| READ | Load and use a document | READ [DECISIONS.md](DECISIONS.md) |
| DECIDE | Choose via a decision matrix | DECIDE severity per [DECISIONS §3](DECISIONS.md#3-severity) |
| OUTPUT | Emit the completion response | OUTPUT §7 |

### 5.2. Workflow Rules

- Carry out steps top to bottom; meet each **Outcome** before continuing.
- Stay within §4; when a step links a doc, READ that section for the step.
- Apply §5.1 operator capitalisation in step bodies; do not shout ordinary prose.
- **Shape B** — patch clear findings in the same run; leave ambiguous items as `ask-user`.
- Do NOT drop requirements without user approval.
- Do NOT suggest other skills IN the report.

| Excuse | Reality |
|--------|---------|
| “Missing verify twin — add one.” | Form-only; out of scope. |
| “Chunk heavy — lean the plan.” | Resizing / lean-full reshape IS out of scope for triage. |
| “Invent a reasonable requirement.” | Only user-endorsed session asks ([DECISIONS §2](DECISIONS.md#2-session-intent-harvest)). |
| “Fail the build gate.” | Triage does NOT gate build — surface severities only. |

### 5.3. Workflow Steps

#### 5.3.1. Resolve target

1. DECIDE target per [DECISIONS §1](DECISIONS.md#1-target-plan).

**Outcome:** Absolute plan path.

#### 5.3.2. Harvest session asks

1. Collect **user-only** requirements from this chat per [DECISIONS §2](DECISIONS.md#2-session-intent-harvest).
2. Apply supersession rules.
3. Map each surviving ask: **present** | **partial** | **absent**.

**Outcome:** Session-ask inventory with status and expected locus.

#### 5.3.3. Read plan and spot-check workspace

1. READ frontmatter and body (all sections).
2. For axes 3–4 ([DECISIONS §4](DECISIONS.md#4-four-axes)): targeted spot-checks only — user-named paths, plan-adjacent siblings, referenced files. No full-repo crawl.

**Outcome:** Plan context loaded; bounded workspace notes ready.

#### 5.3.4. Interrogate four axes

1. RUN axes 1–4 per [DECISIONS §4](DECISIONS.md#4-four-axes).
2. DECIDE severity per finding ([DECISIONS §3](DECISIONS.md#3-severity)).

**Outcome:** Findings list with axis, severity, locus.

#### 5.3.5. Patch (Shape B)

1. For each finding with a clear plan locus, MODIFY per [DECISIONS §5](DECISIONS.md#5-patch-matrix).
2. Honor patch limits ([DECISIONS §6](DECISIONS.md#6-patch-limits)).
3. IF ambiguous, THEN leave as `ask-user` — do NOT invent.

**Outcome:** Clear findings patched; ambiguous items reported only.

#### 5.3.6. Report

1. OUTPUT chat delta per [RESPONSE.md](RESPONSE.md).

**Outcome:** Operator sees findings, patches, remaining ask-user/blockers.

## 6. Validation

On failure, re-read §5, resolve, re-check.

### 6.1. Scripted validation

None bundled. Confirm [WORKFLOW.yaml](WORKFLOW.yaml) mirrors §5.3 when workflow steps changed.

### 6.2. Agent questions

Answer every [VALIDATION.md](VALIDATION.md) Agent question against this run.

### 6.3. Interrogation agent

This skill **is** the interrogation agent for plan substance. Do NOT nest another interrogator.

**Pass when:** Four axes run; clear findings patched (substance only); ambiguous left as `ask-user`; chat matches [RESPONSE.md](RESPONSE.md).

## 7. Completion

OUTPUT chat per [RESPONSE.md](RESPONSE.md). Do NOT claim a pressure test unless done.
