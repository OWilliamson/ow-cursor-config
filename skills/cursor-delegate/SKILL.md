---
name: cursor-delegate
description: >-
  Decision guide for when to delegate work to Cursor Task subagents (explore, shell,
  generalPurpose, bugbot, security-review) versus the main thread, plus structured
  output contracts so parent context stays small. Use when spawning subagents, saving
  context, delegating search or review, choosing explore vs inline work, or when the
  user asks how to delegate agent tasks.
disable-model-invocation: true
---

# Cursor delegation guide

Explicit-only. Invoke with `/cursor-delegate` or `@cursor-delegate`.

## When to use

- You are about to spawn a **Task** subagent and need a routing decision.
- The main thread context is large and subagent output should be **structured and compact**.
- The user asks whether to use explore, shell, bugbot, security-review, or stay inline.

## Required inputs

- **Task type** (optional): locate, edit, review, shell command, or unknown.
- **Scope** (optional): file count, readonly vs write, security sensitivity.

## Definition of done

- A concrete recommendation: **main thread**, **explore**, **shell**, **generalPurpose**, **bugbot**, or **security-review**.
- If delegating: a **task prompt** that embeds the matching **output contract** from [reference-delegation.md](reference-delegation.md).
- Chaining pattern named when the work is multi-step (investigate → edit → verify).

## Non-goals

- Do not spawn subagents automatically just because this skill was invoked.
- Do not override repo policies (external-systems read-only, github-and-remotes, etc.).

## Boundaries

- Routing and prompt drafting only — does not run Task, commit, push, or mutate external systems.

## Workflow

1. Classify the request using the **When to delegate** table in [reference-delegation.md](reference-delegation.md).
2. If **main thread** wins, say why (known path, ≤2 files, needs prose or user-facing draft).
3. If a subagent wins, pick `subagent_type` and **thoroughness** (`quick` / `medium` / `very thorough` for explore).
4. Append the matching **output contract** block to the Task prompt verbatim.
5. For multi-step work, name the chain (e.g. explore → main edit → bugbot) and what each step returns.

## Auto-Clarity

Use full prose in the Task prompt (not compressed contracts) when:

- The subagent must explain a **security** or **compliance** finding with rationale.
- The user will read subagent output **directly** without paraphrase (customer email, PR description body).
- Scope is ambiguous — prefer one clarifying question over a vague delegation.

Resume structured contracts after the clear part.

## Additional resources

- [reference-delegation.md](reference-delegation.md) — routing tables, output contracts, chaining, anti-patterns
