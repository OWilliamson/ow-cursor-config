---
name: owcc-plan-verification-cursor
description: >-
  Injects or repairs cursor-native closeout verification in .plan.md files.
  Use when the user invokes /owcc-plan-verification-cursor.
disable-model-invocation: true
---

# 1. Plan verification (cursor-native)

The aim of invoking owcc-plan-verification-cursor is to mutate a cursor-native `.plan.md` so build agents run file, registry, and **Plan build:** complete checks at closeout.

Explicit-only. Invoke with `/owcc-plan-verification-cursor` and **@** the `.plan.md` file.

## 2. When to use

- Cursor-native `.plan.md` needs closeout verification injected or repaired.
- Plan lacks per-phase closeout todos, verify script paths, registry language, or **Plan build:** complete requirements.

## 3. Inputs

| Signal | How to act |
|--------|------------|
| Absolute path to `.plan.md` under `.cursor/plans/` | Target ([DECISIONS §1](DECISIONS.md#1-target-plan)) |
| `@` on a `.plan.md` | Resolve that path |
| Non-`.plan.md` or non-cursor-native plan | Refuse; out of scope ([DECISIONS §1](DECISIONS.md#1-target-plan)) |
| No path / ambiguous | Ask once; do NOT guess |

## 4. Scope

**In scope:** Audit plan text for closeout gaps; MODIFY frontmatter todos and body closeout language per [OUTPUTS.md](OUTPUTS.md); RUN frontmatter validator after every write; re-audit until clean; OUTPUT mutation delta.

**Out of scope:** Generic plan content/sizing/execution-contract reshape; WRITE `.validation.json`; execute build closeout scripts at invoke (`plan-verify-close-cursor.py` / `plan-registry-show.py` are for build agents); registry writes (`sync` retired); name or route to other plan skills.

## 5. Workflow

### 5.1. Workflow Operators

These operator words mark specific operations in the workflow. When used as operators, they must be capitalised. When used for ordinary meaning (not as an operator), they must be lower case.

| Operator | Meaning | Example |
|----------|---------|---------|
| IF | Conditional test | IF gaps remain, THEN edit |
| THEN | Consequence of IF | IF isProject, THEN per-phase todos |
| ELSE | Alternate branch | ELSE flat final todo |
| AND | Conjoin requirements | Audit AND frontmatter validate |
| NOT | Negation / forbid | do NOT run closeout at invoke |
| IS | Equality / state check | IF ok IS true |
| IN | Location / membership | todos IN each phase |
| CREATE | Make a new artifact | CREATE closeout verify todo |
| MODIFY | Change existing content | MODIFY plan YAML |
| RUN | Execute a command or check | RUN audit script |
| READ | Load and use a document | READ [OUTPUTS.md](OUTPUTS.md) |
| WRITE | Produce new content at a path | WRITE plan edits |
| WHILE | Repeat while condition holds | WHILE gaps remain, edit |
| DECIDE | Choose via a decision matrix | DECIDE placement per [DECISIONS §2](DECISIONS.md#2-closeout-placement) |
| OUTPUT | Emit the completion response | OUTPUT §7 |
| RETURN TO | Go back to an earlier step | RETURN TO audit |

### 5.2. Workflow Rules

- Carry out steps top to bottom; meet each **Outcome** before continuing.
- Stay within §4; when a step links a doc, READ that section for the step.
- Apply §5.1 operator capitalisation in step bodies; do not shout ordinary prose.
- **Invoke-time** scripts: audit + frontmatter validate. **Build-time** scripts: verify-close + registry-show (named IN todo content only).
- After every WRITE to the plan, RUN frontmatter validate; exit 0 required.

| Excuse | Reality |
|--------|---------|
| “Run verify-close now to see if it passes.” | That script IS for build agents; invoke uses audit only. |
| “Skip frontmatter validate — small edit.” | RUN after every write ([DECISIONS §3](DECISIONS.md#3-frontmatter-rules)). |
| “Also fix lean/full sizing.” | Out of scope — generic mutation skills. |

### 5.3. Workflow Steps

#### 5.3.1. Resolve target

1. DECIDE target per [DECISIONS §1](DECISIONS.md#1-target-plan).

**Outcome:** Absolute `.plan.md` path confirmed cursor-native.

#### 5.3.2. Audit plan text

1. RUN:

```bash
python3 ~/.cursor/skills/owcc-plan-verification-cursor/scripts/plan-audit-cursor-verification.py --json /absolute/path/to/plan.plan.md
```

2. Parse `gaps[]`. Exit **1** with gaps IS expected before injection.

**Outcome:** Gap list ready (or already `ok: true`).

#### 5.3.3. Edit plan

1. DECIDE placement per [DECISIONS §2](DECISIONS.md#2-closeout-placement).
2. CREATE or MODIFY closeout todos and optional body addendum per [OUTPUTS.md](OUTPUTS.md).
3. Inject script paths IN todo `content` for build agents (verify-close + registry-show).

**Outcome:** Closeout language present per shape.

#### 5.3.4. Validate frontmatter after every write

1. RUN:

```bash
python3 ~/.cursor/skills/owcc-plan-verification-cursor/scripts/plan-validate-frontmatter.py /absolute/path/to/plan.plan.md
```

2. Exit **0** required. IF fail, THEN fix per [DECISIONS §3](DECISIONS.md#3-frontmatter-rules) AND RETURN TO this step.

**Outcome:** Frontmatter validator exit 0.

#### 5.3.5. Re-audit until gaps clear

1. WHILE audit reports gaps: RETURN TO 5.3.3 → 5.3.4 → re-RUN audit.
2. Stop when `ok: true`.

**Outcome:** Audit `ok: true`.

#### 5.3.6. Report

1. OUTPUT mutation delta per [RESPONSE.md](RESPONSE.md) — not runtime verify results.

**Outcome:** Operator sees what was added or repaired.

## 6. Validation

On failure, re-read §5, resolve, re-check.

### 6.1. Scripted validation

RUN audit + frontmatter scripts documented IN [VALIDATION.md](VALIDATION.md). Confirm [WORKFLOW.yaml](WORKFLOW.yaml) mirrors §5.3 when steps change.

### 6.2. Agent questions

Answer every [VALIDATION.md](VALIDATION.md) Agent question against this run.

### 6.3. Interrogation agent

None.

**Pass when:** Audit `ok: true`; last frontmatter validate exit 0; chat matches [RESPONSE.md](RESPONSE.md).

## 7. Completion

OUTPUT chat per [RESPONSE.md](RESPONSE.md). Do NOT claim a pressure test unless done.
