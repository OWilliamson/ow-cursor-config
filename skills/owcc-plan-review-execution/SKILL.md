---
name: owcc-plan-review-execution
description: >-
  Read-only post-build success review of whether plan execution met Aims,
  Target shape, Scope, Stop-if, Rules, and todo correctness. Use when the user
  invokes /owcc-plan-review-execution with a plan attached after or during
  build. A/M/R inventory script assists git/path checks; Bugbot is delegated when gated.
disable-model-invocation: true
---

# 1. Plan success review

The aim of invoking owcc-plan-review-execution is to **judge** whether **plan execution succeeded** against the plan's success criteria (Aims, Target shape, Scope, Stop-if, Rules/§9, todos) by comparing plan criteria to workspace state — not to audit YAML completion theater or improve the unbuilt plan artifact.

The A/M/R inventory script assists path/git checks (`code_loc`, claimed vs unplanned). **Judgment** against Aims and related sections is the product. Stay read-only: do NOT edit the plan or auto-fix findings.

Explicit-only. Invoke with `/owcc-plan-review-execution` in an **Agent** chat, and **@**-attach the plan file in the same message.

## 2. When to use

- After a Build chunk or scoped plan execution — checkpoint before continuing.
- Before signing off — confirm the plan's Aims and Target shape were met.
- When work may have drifted from Scope, §9 Decisions, or Rules **Stop-if**.
- When A/M/R tables or the diff look incomplete or over-scoped relative to the plan.

## 3. Inputs

| Signal | How to act |
|--------|------------|
| `@` plan path, absolute path, or pasted body | That plan ([DECISIONS §1](DECISIONS.md#1-target-plan)) |
| Todo id | Scope to that todo ([DECISIONS §2](DECISIONS.md#2-review-scope)) |
| Phase name | That phase IF project plan; ELSE whole plan or named todo |
| Neither todo nor phase | Whole plan |
| `/owcc-plan-review-execution` only | Most recently discussed plan IN this chat ([DECISIONS §1](DECISIONS.md#1-target-plan)) |
| `bugbot=off` / `skip-bugbot` | Skip Bugbot ([DECISIONS §8](DECISIONS.md#8-bugbot-gate)) |
| `bugbot=on` / `run-bugbot` | Force Bugbot on (overrides LOC default) |
| `--base` / named git baseline | Use that baseline for inventory assist ([DECISIONS §3](DECISIONS.md#3-git-baseline)) |
| Ambiguous / none | Ask once; do NOT guess |

## 4. Scope

**In scope:** Resolve plan success criteria from Aims, Target shape, Scope, Stop-if, Rules/§9, and todos; RUN A/M/R inventory assist; judge success dimensions; assign F-ids to failures; spawn Bugbot when gated on (and Security Review when relevant); OUTPUT the success-first chat report.

**Out of scope:** Edit the plan (including `status:`); run remaining implementation todos; close the plan or set `**Plan build:** complete`; write `.validation.json`; validate or improve plan *authoring* (structure, substance interrogation, or pre-build report writing); inline duplicate of Bugbot's full review (delegate when gated); broad full-profile rule audits; profile install / reconcile / publish; suggest unrelated skills IN the report.

## 5. Workflow

### 5.1. Workflow Operators

These operator words mark specific operations in the workflow. When used as operators, they must be capitalised. When used for ordinary meaning (not as an operator), they must be lower case.

| Operator | Meaning | Example |
|----------|---------|---------|
| IF | Conditional test | IF path missing, THEN ask |
| THEN | Consequence of IF | IF project plan, THEN allow phase scope |
| ELSE | Alternate branch | ELSE use whole plan |
| AND | Conjoin requirements | DECIDE target AND scope |
| NOT | Negation / forbid | do NOT edit the plan |
| IS | Equality / state check | IF status IS completed |
| IN | Location / membership | READ the section IN context |
| RUN | Execute a command or check | RUN A/M/R inventory assist |
| READ | Load and use a document | READ [VALIDATION.md](VALIDATION.md) |
| SKIP TO | Jump forward | SKIP TO 5.3.11 |
| RETURN TO | Go back | RETURN TO 5.3.3 |
| WHILE | Repeat while condition holds | WHILE todos remain, judge correctness |
| DECIDE | Choose via a decision matrix | DECIDE Bugbot gate |
| OUTPUT | Emit the completion response | OUTPUT §7 |

### 5.2. Workflow Rules

- Carry out steps top to bottom; meet each **Outcome** before continuing.
- Stay within §4; when a step links a doc, READ that section for the step.
- Apply §5.1 operator capitalisation in step bodies; do not shout ordinary prose.
- **Object of review:** whether execution met plan success criteria. Inventory script IS assist only — NOT the review. YAML `status:` IS a claim, not proof of Aim Result.
- Trust order: **disk** > **git** > **YAML `status:`** > chat. Do NOT mark Aims or a todo **pass** on YAML alone.
- Partial scope: Aims / Target shape / Scope / Better are relative to the todo/phase/whole IN scope ([DECISIONS §2](DECISIONS.md#2-review-scope)).
- Apply [DECISIONS §15](DECISIONS.md#15-specified-but-undone): plan-named work unmet on disk/diff → **fail**, not soft **warn**.
- For every fail or warn, assign an **F-id** AND record **why** AND whether **action is needed now** ([DECISIONS §10](DECISIONS.md#10-failure-why-and-action)).
- Do NOT fix findings unless the user asks after the report.
- Closeout / validate-close scripts are optional appendix only — never headline Overall fail on authoring-class codes alone ([DECISIONS §4](DECISIONS.md#4-closeout-finding-class)).

| Excuse | Reality |
|--------|---------|
| "YAML says completed" | Not proof — judge Aim Result / Key actions / DoD on disk/diff |
| "Parsed inventory JSON → review done" | Inventory assist only; still judge each Aim/todo on disk ([DECISIONS §15](DECISIONS.md#15-specified-but-undone)) |
| "One path exists → Aims pass" | Path presence IS NOT success — judge Result text and content ([EXAMPLES.md](EXAMPLES.md) Example 2) |
| "Preflight paths present → success" | Inventory only; still judge Content/Change/Reason AND Aims |
| "Closeout script failed → execution fail" | Only IF finding IS execution-class ([DECISIONS §4](DECISIONS.md#4-closeout-finding-class)) |
| "Skipped Bugbot → Bugs fail" | Skipped Bugbot IS **n/a**, not fail ([DECISIONS §8](DECISIONS.md#8-bugbot-gate)) |
| "Chat memory says we finished" | Never sole basis for pass |

### 5.3. Workflow Steps

#### 5.3.1. Resolve plan, scope, AND baseline

1. DECIDE target plan per [DECISIONS §1](DECISIONS.md#1-target-plan).
2. DECIDE review scope per [DECISIONS §2](DECISIONS.md#2-review-scope).
3. Infer workspace root (git root from plan path, parent of `.cursor/plans/`, or CWD).
4. DECIDE git baseline per [DECISIONS §3](DECISIONS.md#3-git-baseline).
5. State plan path, scope, workspace root, AND baseline IN one line.

**Outcome:** Absolute plan path, scope, workspace root, baseline stated.

#### 5.3.2. RUN A/M/R inventory assist

1. RUN the inventory assist command IN [VALIDATION.md](VALIDATION.md) (Scripted validation), with optional `--todo` / `--phase` / `--workspace` / `--base`.
2. Parse JSON (`claimed`, `unplanned`, `code_loc`, `bugbot_default`, light todos) as inventory assist — NOT verdicts.
3. Note missing / wrong_change_type / unplanned paths AND `inventory_incomplete` IF present — use as hints only; agent still judges A/M/R Content/Change/Reason and Aims on disk/diff.

**Outcome:** Inventory JSON parsed; A/M/R gaps noted for later judgment.

#### 5.3.3. Judge Aims success

1. READ plan `## Aims` (brief + OKR table **Result** column for todos IN scope) **before** relying on inventory output.
2. Against disk + git diff since baseline, DECIDE whether execution lived up to each in-scope Aim Result ([DECISIONS §5](DECISIONS.md#5-success-dimensions), [§15](DECISIONS.md#15-specified-but-undone)).
3. Record pass/warn/fail/n/a + **Judgment** per Aim row (criterion → workspace outcome → why verdict). Do NOT use a lone path or inventory line as Judgment.

**Outcome:** Aims success judgment ready for the report.

#### 5.3.4. Match Target shape

1. READ plan `## Target shape`.
2. IF section IS `None.` or absent, THEN mark **n/a**.
3. ELSE compare end-state layout / schemas / narrative to disk + diff; DECIDE match per [DECISIONS §5](DECISIONS.md#5-success-dimensions).

**Outcome:** Target shape judgment (or n/a).

#### 5.3.5. Coverage vs Scope

1. READ plan `## Scope` (in / out).
2. Judge covered in-scope work AND flag out-of-scope drift (use inventory `unplanned` + diff).
3. DECIDE Scope dimension per [DECISIONS §5](DECISIONS.md#5-success-dimensions).

**Outcome:** Scope coverage judgment ready.

#### 5.3.6. Stop-if honesty

1. READ Rules **Stop-if** (and any localized halt gates).
2. Ask whether any stop-if was **met**, **ignored**, or **worked around** (chat + diff evidence).
3. DECIDE Stop-if dimension per [DECISIONS §5](DECISIONS.md#5-success-dimensions).

**Outcome:** Stop-if judgment ready.

#### 5.3.7. Rules, §9, AND bounded workspace rules

1. READ plan `## Rules` AND `## Decisions` (§9) when not `None.`.
2. Check bounded always-on / project rules that clearly apply to touched paths or Scope ([DECISIONS §7](DECISIONS.md#7-workspace-rules)).
3. DECIDE Rules dimension; do NOT audit the whole profile.

**Outcome:** Rules/§9 judgment ready.

#### 5.3.8. Per-todo correctness

1. WHILE each todo IN scope:
   1. Judge whether it was **correctly** done against Aim **Result** AND Stages Key actions / Definition of done — not YAML alone ([DECISIONS §6](DECISIONS.md#6-per-todo-verdict), [§15](DECISIONS.md#15-specified-but-undone)).
   2. Use disk, diff, and A/M/R Content/Change/Reason; optional light verify only when clearly needed for correctness (not mandatory per-todo backtick theater).
   3. Record **Judgment** (criterion → outcome → why) per todo; cite Failure ID when verdict IS fail/warn.
2. Fill the per-todo correctness matrix.

**Outcome:** Per-todo correctness matrix complete.

#### 5.3.9. Bugbot gate AND Security Review

1. DECIDE Bugbot gate per [DECISIONS §8](DECISIONS.md#8-bugbot-gate) using operator signal OR inventory `code_loc` / `bugbot_default`.
2. IF gated on, THEN spawn Task `bugbot` with `run_in_background: false` AND code-only Custom Instructions (prompt shape IN DECISIONS §8). Spawn failure → incomplete_review/warn — NOT Bugs pass.
3. IF gated off, THEN record Bugs as **n/a** with skip reason (operator / LOC / no code).
4. DECIDE Security Review per [DECISIONS §9](DECISIONS.md#9-security-review): run when diff touches auth, secrets, network, or external writes; ELSE skip with reason.

**Outcome:** Subagent findings recorded or skip reasons noted.

#### 5.3.10. Better-than-start, failures why/action, overall

1. DECIDE Better-than-start per [DECISIONS §11](DECISIONS.md#11-better-than-start) — baseline delta / non-regression only; do NOT re-score Aims or Bugbot/Security.
2. For each fail/warn across success dims, todos, AND subagents: assign sequential **F-id** (F1, F2, …); record **why** AND **action needed?** ([DECISIONS §10](DECISIONS.md#10-failure-why-and-action)).
3. DECIDE overall verdict per [DECISIONS §12](DECISIONS.md#12-overall-verdict).
4. Optionally RUN closeout scripts only IF operator asked OR `**Plan build:** complete` IS present — appendix only ([DECISIONS §4](DECISIONS.md#4-closeout-finding-class)).

**Outcome:** Better judgment (baseline/regression), failure actions, overall verdict set.

#### 5.3.11. OUTPUT report (do NOT fix)

1. OUTPUT chat per [RESPONSE.md](RESPONSE.md) — Success judgments first; enumerated Failures with F-ids; A/M/R inventory brief after subagents; no mandatory Objective-checks closeout list.
2. List remediation as recommendations only — do NOT execute fixes unless the user asks.

**Outcome:** Final message matches RESPONSE template.

## 6. Validation

On failure, re-READ §5, resolve, re-check.

### 6.1. Scripted validation

RUN mechanical checks IN [VALIDATION.md](VALIDATION.md).

### 6.2. Agent questions

Answer every [VALIDATION.md](VALIDATION.md) Agent question against this review run.

### 6.3. Interrogation agent

None by default.

**Pass when:** Object-of-review = plan success; report leads with Success judgments; Judgment cells follow criterion → outcome → why; F-ids assigned for every fail/warn; Bugbot gate honored; no pass-on-YAML-alone for Aims/todos; specified-but-undone → fail per DECISIONS §15; RESPONSE sections complete; agent questions answered.

## 7. Completion

OUTPUT chat per [RESPONSE.md](RESPONSE.md). Do NOT edit the plan or implement fixes IN this invocation.
