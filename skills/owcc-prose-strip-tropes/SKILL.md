---
name: owcc-prose-strip-tropes
description: >-
  Use when the user invokes /owcc-prose-strip-tropes on a path, paste, or prior
  reply, or asks for a de-AI, humanize-prose, or writing-trope pass. Strips LLM
  stylistic defaults from chat or documents without changing meaning, facts,
  links, code, or required structure.
disable-model-invocation: true
---

# 1. Prose strip tropes

The aim of invoking owcc-prose-strip-tropes is a check-then-rewrite pass that strips LLM stylistic defaults from chat text or documents without changing meaning, facts, or required structure.

Explicit-only. Invoke with `/owcc-prose-strip-tropes`. Prefer **@**-attach the target file in the same message when rewriting on disk.

## 2. When to use

- A draft, rule, skill, README, plan, report, or chat reply reads as generic LLM prose.
- Operator wants findings only, or an in-place / returned rewrite.
- After drafting, before publish or handoff, when voice quality matters.

## 3. Inputs

| Signal | How to act |
|--------|------------|
| Path (absolute or workspace-relative) | Target file ([DECISIONS §1](DECISIONS.md#1-target)) |
| `@` on a file | Resolve that path as target |
| Pasted prose | Treat as chat target; return rewrite IN chat unless user asks to write a path |
| “Last reply” / “this message” | Target the named assistant turn IN this chat |
| `audit` / `rewrite` | Mode ([DECISIONS §2](DECISIONS.md#2-mode)); default **rewrite** when target clear |
| No target / ambiguous | Ask once; do NOT guess |

## 4. Scope

**In scope:** Natural-language prose IN chat or text-like files (`.md`, `.mdc`, `.txt`, mixed-markdown prose); categories IN [DECISIONS.md](DECISIONS.md); cluster-scored findings; meaning-stable rewrite using facts already IN the artefact.

**Out of scope:** Changing technical claims; inventing facts, examples, or “soul”; telegram cuts; one-token “proof”; authorship accusations; restyling code or config; YAML/JSON or RESPONSE templates beyond prose cells; durable word-bans; commit, push, or profile install unless asked; naming other skills IN the report.

## 5. Workflow

### 5.1. Workflow Operators

These operator words mark specific operations in the workflow. When used as operators, they must be capitalised. When used for ordinary meaning (not as an operator), they must be lower case.

| Operator | Meaning | Example |
|----------|---------|---------|
| IF / THEN / ELSE | Conditional | IF mode IS audit THEN SKIP TO 5.3.7 |
| AND / NOT / IS / IN | Logic / membership | finding IN category |
| CREATE / MODIFY / READ / WRITE / REWRITE | Artifact ops | REWRITE flagged passages |
| DECIDE | Decision matrix | DECIDE mode per [DECISIONS §2](DECISIONS.md#2-mode) |
| OUTPUT / RUN / SKIP TO | Emit, checklist, jump | RUN categories IN DECISIONS §4 |

### 5.2. Workflow Rules

- Carry out steps top to bottom; meet each **Outcome** before continuing.
- Stay within §4; READ linked sections; capitalise §5.1 operators only as operators.
- Preserve [DECISIONS §3](DECISIONS.md#3-preserve) unless the user asks to change those regions.
- Score **clusters**, not isolated tokens ([DECISIONS §5](DECISIONS.md#5-severity)). Keep complete sentences. Do NOT invent facts or drop requirements.

| Excuse | Reality |
|--------|---------|
| “Shorter / edgier is more human.” | Cut tropes; keep complete sentences; do NOT invent soul. |
| “House jargon or one watch-list word is the tell.” | Keep intentional vocabulary ([DECISIONS §3](DECISIONS.md#3-preserve)). Isolated seeds are `note` ([DECISIONS §5](DECISIONS.md#5-severity)). |
| “Every em dash must go.” | Supporting evidence only, not a standalone `must-fix`. |
| “Audit is enough; skip the rewrite.” | Only IF mode IS audit or user said findings-only. |

### 5.3. Workflow Steps

#### 5.3.1. Resolve target

1. DECIDE target per [DECISIONS §1](DECISIONS.md#1-target).

**Outcome:** One target (path, paste buffer, or named chat turn).

#### 5.3.2. DECIDE mode

1. DECIDE mode per [DECISIONS §2](DECISIONS.md#2-mode).

**Outcome:** `audit` or `rewrite`.

#### 5.3.3. Load AND map preserve regions

1. READ the target.
2. Mark preserve regions per [DECISIONS §3](DECISIONS.md#3-preserve).

**Outcome:** Working text loaded; preserve map ready.

#### 5.3.4. RUN trope checks

1. RUN every category IN [DECISIONS §4](DECISIONS.md#4-check-categories) (overlay IF that section says to READ it).
2. Record findings: category, locus, severity ([DECISIONS §5](DECISIONS.md#5-severity)).

**Outcome:** Findings list (may be empty). Isolated weak hits marked `note`.

#### 5.3.5. Rewrite OR stop at audit

1. IF mode IS audit, THEN SKIP TO 5.3.7.
2. REWRITE flagged prose per [DECISIONS §6](DECISIONS.md#6-rewrite-limits).

**Outcome:** Working copy rewritten, or audit-only skip.

#### 5.3.6. Rescan residue AND persist

1. RUN categories again on the working copy, including C15.
2. IF residue hits, THEN REWRITE those spans per [DECISIONS §6](DECISIONS.md#6-rewrite-limits).
3. IF target IS a file, THEN MODIFY it (CREATE backup only IF asked).
4. IF target IS paste or chat turn, THEN return the full rewritten text IN the completion.

**Outcome:** Residue pass done; artifact persisted or held for chat.

#### 5.3.7. Report

1. OUTPUT chat per [RESPONSE.md](RESPONSE.md).

**Outcome:** Operator sees mode, findings, and what changed (or that nothing needed change).

## 6. Validation

On failure, re-READ §5, resolve, re-check.

### 6.1. Scripted validation

None bundled. Confirm [WORKFLOW.yaml](WORKFLOW.yaml) mirrors §5.3 when workflow steps changed.

### 6.2. Agent questions

Answer every [VALIDATION.md](VALIDATION.md) Agent question against this run.

### 6.3. Interrogation agent

None by default. IF operator requests, THEN read-only subagent for a second pass on the rewritten text only.

**Pass when:** C1–C15 considered; cluster scoring and preserve map honored; mode respected; rewrite rescanned; chat matches [RESPONSE.md](RESPONSE.md).

## 7. Completion

OUTPUT chat per [RESPONSE.md](RESPONSE.md). Do NOT claim a pressure test unless done.
