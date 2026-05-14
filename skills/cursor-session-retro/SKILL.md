---
name: cursor-session-retro
description: >-
  Analyzes inefficient or failing Cursor agent sessions to produce evidence-backed root causes
  and a capped backlog of durable fixes (prompts, documentation, scripts, Cursor rules, skills, templates).
  Use after repeated failures, long detours, wasted tool loops, frustrating sessions, or when the user asks
  for a post-mortem, session retro, friction diagnosis, why something was slow, how to be faster next time,
  or how to prevent the same class of mistake.
disable-model-invocation: true
---

# Agent session efficiency retro

## When to use

Run this workflow in a **new chat** (or clean context) so the retro is not fighting the same truncated or noisy thread that caused the incident.

## Hook integration (optional automation)

Thresholds, logging, and optional nudges live in **Cursor hooks**, not in this file. Install paths, privacy (prompts may appear in JSONL), tuning keys, JSONL schema, rotation, and CLI dry run: **[reference-hooks.md](reference-hooks.md)**.

## Required inputs (ask if missing)

Collect from the user (or transcript), with **secrets redacted**:

1. **Goal:** what “done” meant for the session.
2. **Outcome:** success, partial, or failure—and the final state.
3. **Failures:** tool errors, test failures, wrong edits, or blocked steps (paste minimal excerpts).
4. **Wasted loops:** 1–3 concrete examples (e.g. wrong file, repeated search, long speculative refactor).
5. **Context:** repo/path, branch, OS/runtime if relevant.
6. **Mode:** Plan vs Agent vs Ask (if known)—fixes differ (permissions, tooling, vs reasoning-only).
7. **Constraints:** offline, no network, policy limits, “do not touch X”.

**Privacy:** never ask the user to paste raw tokens, cookies, passwords, or private keys. If logs may contain them, instruct scrubbing or describe errors generically.

## Hard constraints on your output

- **Evidence:** each root cause cites concrete material (errors, tool output, quotes, or step sequence); label **speculative** when thin and name confirming evidence.
- **Cap:** default **≤5** prioritized actions (P0/P1 toward cap; **exhaustive mode** only if the user asks).
- **Brevity:** executive summary **≤5 bullets**; no long narrative unless exhaustive mode.
- **No megapastes:** point to gaps; propose **small** targeted additions, not full rule dumps.
- **Verification:** end with **1–3** concrete next-time checks (commands, file reads)—not vague advice.

## Workflow

1. Restate goal and outcome in one short paragraph.
2. Build a **ranked** list of hypotheses using the taxonomy in [reference.md](reference.md#diagnosis-taxonomy); merge duplicates.
3. Map top hypotheses to remediation types using the [remediation map](reference.md#remediation-map) in `reference.md` (scripts vs docs vs rule vs skill vs prompt template).
4. Produce the **required output format** (below).
5. If the user wants implementation immediately: offer to draft the **smallest** artifact first (usually a prompt template + one doc paragraph, or one focused rule).

## Required output format

### Executive summary

- **≤5 bullets**

### Session facts

- Goal, outcome, mode (if known), key constraints

### Ranked root causes

For each cause: **severity**, **evidence** (quote or pointer), **fix type** (prompt/doc/script/rule/skill/template). Mark **speculative** when needed.

### Prioritized changes (cap: 5 unless exhaustive mode)

Table or list: **ID**, **Priority (P0/P1/P2)**, **Artifact type**, **Proposed location/path**, **Owner** (user vs agent), **Definition of done** (one sentence).

### Before / after prompts

At least **one** minimal pair showing how the user should ask next time.

### Next-time verification

1–3 concrete checks (commands or file reads).

### Optional: artifact drafts

Only if asked: draft the smallest useful snippet (rule stub, skill stub, script outline, doc paragraph)—keep short.

## Long-form templates

For a full retro write-up or draft scaffolds, use [reference.md](reference.md).

For hooks, env vars, and log rotation, use [reference-hooks.md](reference-hooks.md).
