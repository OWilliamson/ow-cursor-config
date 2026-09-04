---
name: owcc-plan-build
description: >-
  Governs plan execution on disk (four intents, YAML status, closeout).
  Use when the user invokes /owcc-plan-build with a plan file attached.
disable-model-invocation: true
---

# 1. Plan build

The aim of invoking owcc-plan-build is to govern plan execution on disk and in chat — reconcile YAML `status`, run scoped implementation when asked, validate, and close. Non-cursor-native plans require a passing `.validation.json` preflight; cursor-native `.plan.md` skips that gate.

Explicit-only. Invoke with `/owcc-plan-build` in an **Agent** chat, and **@**-attach the plan file in the same message.

Do **not** use mode keywords (`audit`, `resume`, `close`). **Infer** intent from what the user names and plan state ([DECISIONS §2](DECISIONS.md#2-four-intents)).

## 2. When to use

- Sync YAML after a native Build chunk.
- Continue one named phase or named todo.
- Advance an incomplete plan (first pending).
- Sign off a complete plan (all todos done).

Native Build remains the default implementer for greenfield chunks; then `/owcc-plan-build` reconciles layer A ([DECISIONS §3](DECISIONS.md#3-two-layers); [EXAMPLES.md](EXAMPLES.md)).

## 3. Inputs

| Signal | How to act |
|--------|------------|
| `@` plan path | Target ([DECISIONS §1](DECISIONS.md#1-target-and-preflight)) |
| Path ends with `.plan.md` | Cursor-native — skip `.validation.json` preflight |
| Passing `.validation.json` on disk | Required only for non-`.plan.md` targets ([DECISIONS §1](DECISIONS.md#1-target-and-preflight)) |
| Todo **id** named | Intent = named todo |
| Phase **name** named (case-insensitive) | Intent = named phase (`isProject` only) |
| Neither; any pending/in_progress | Intent = incomplete plan |
| Neither; all completed/cancelled | Intent = complete plan |
| Ambiguous / missing validation (non-`.plan.md`) | Stop; ask or report preflight failure |

## 4. Scope

**In scope:** Preflight (`.validation.json` for non-`.plan.md` only); DECIDE intent; update layer A `status:` IN scope; mirror layer B session todos; implement+verify per todo `content` when this agent executes; RUN `plan-validate-close.py` on complete intent; stamp `**Plan build:** complete — YYYY-MM-DD`; OUTPUT chat per [RESPONSE.md](RESPONSE.md).

**Out of scope:** Rewrite plan body, todo `content`, order, or frozen decisions without user approval; RUN `plan-validate-frontmatter.py` / UUID recovery / cursor-native rewrites at close; invent mode flags; name other skills on preflight fail.

## 5. Workflow

### 5.1. Workflow Operators

These operator words mark specific operations in the workflow. When used as operators, they must be capitalised. When used for ordinary meaning (not as an operator), they must be lower case.

| Operator | Meaning | Example |
|----------|---------|---------|
| IF | Conditional test | IF preflight fails, THEN stop |
| THEN | Consequence of IF | IF complete, THEN RUN validate-close |
| ELSE | Alternate branch | ELSE incomplete intent |
| AND | Conjoin requirements | Update layer A AND layer B |
| NOT | Negation / forbid | do NOT rewrite body |
| IS | Equality / state check | IF status IS pending |
| IN | Location / membership | todo IN scope |
| MODIFY | Change existing content | MODIFY status only |
| RUN | Execute a command or check | RUN plan-validate-close.py |
| READ | Load and use a document | READ validation JSON |
| WHILE | Repeat while condition holds | WHILE todos pending IN scope |
| DECIDE | Choose via a decision matrix | DECIDE intent per [DECISIONS §2](DECISIONS.md#2-four-intents) |
| OUTPUT | Emit the completion response | OUTPUT §7 |
| SKIP TO | Jump forward | SKIP TO 5.3.5 on complete-only |

### 5.2. Workflow Rules

- Carry out steps top to bottom; meet each **Outcome** before continuing.
- Stay within §4; when a step links a doc, READ that section for the step.
- Apply §5.1 operator capitalisation in step bodies; do not shout ordinary prose.
- **One todo at a time** within scope ([DECISIONS §4](DECISIONS.md#4-execution-rule)).
- Layer A = plan YAML `status:`; layer B = session todos — do not conflate ([DECISIONS §3](DECISIONS.md#3-two-layers)).
- Trust order: plan file + git diff > chat memory.

| Excuse | Reality |
|--------|---------|
| “YAML says completed — skip verify.” | Re-run verify from todo `content` when executing. |
| “Skip preflight — we validated yesterday.” | For non-`.plan.md`, always READ fresh passing JSON ([DECISIONS §1](DECISIONS.md#1-target-and-preflight)). Cursor-native `.plan.md` skips JSON. |
| “Rewrite the body to fix closeout.” | Status-only (+ Plan build line on complete); body needs approval. |
| “User said audit mode.” | No mode flags — infer four intents only. |

### 5.3. Workflow Steps

#### 5.3.1. Preflight and orient

1. DECIDE preflight per [DECISIONS §1](DECISIONS.md#1-target-and-preflight): IF path ends with `.plan.md`, THEN skip `.validation.json`; ELSE READ validation report — IF fail, THEN stop with path + `failures[]` — do NOT name other skills.
2. READ frontmatter, Rules / Execution contract, frozen decisions, stop-if.
3. DECIDE intent per [DECISIONS §2](DECISIONS.md#2-four-intents).
4. IF frozen decisions / First action / Final validation missing when required, THEN stop.
5. Resolve phase name case-insensitively IF named.

**Outcome:** Preflight satisfied (JSON skipped or pass); intent chosen; scope known.

#### 5.3.2. Confirm scope

1. State plan path, intent, first pending todo id IN scope (one short block).
2. Proceed unless user blocked scope.

**Outcome:** Scope confirmed.

#### 5.3.3. Per-todo loop

1. WHILE todos remain IN scope: apply [DECISIONS §4](DECISIONS.md#4-execution-rule).
2. Respect stop-if before writes.
3. Layer A discipline: only `status:` (and Plan build line on complete) without approval ([DECISIONS §5](DECISIONS.md#5-plan-file-discipline)).

**Outcome:** Scoped todos advanced or blockers noted.

#### 5.3.4. Complete intent closeout

1. IF intent IS NOT complete plan, THEN SKIP TO 5.3.5.
2. RUN:

```bash
python3 ~/.cursor/skills/owcc-plan-build/scripts/plan-validate-close.py /absolute/path/to/plan.md
```

3. RUN plan Final validation commands.
4. Complete **completion-audit** / **final-validation** todo IN YAML.
5. Confirm every todo `completed` or `cancelled`.
6. Set `**Plan build:** complete — YYYY-MM-DD`.
7. Do NOT RUN cursor-native frontmatter hygiene at close.

**Outcome:** Closeout done or blockers reported.

#### 5.3.5. Report

1. OUTPUT chat per [RESPONSE.md](RESPONSE.md).

**Outcome:** Operator sees intent, todos, validation, notes.

## 6. Validation

On failure, re-read §5, resolve, re-check.

### 6.1. Scripted validation

RUN closeout script on complete intent per [VALIDATION.md](VALIDATION.md). Confirm [WORKFLOW.yaml](WORKFLOW.yaml) mirrors §5.3 when steps change.

### 6.2. Agent questions

Answer every [VALIDATION.md](VALIDATION.md) Agent question against this run.

### 6.3. Interrogation agent

None.

**Pass when:** Preflight held; intent correct; layer A updates status-only; complete intent closed or blockers explicit.

## 7. Completion

OUTPUT chat per [RESPONSE.md](RESPONSE.md). Do NOT claim a pressure test unless done.
