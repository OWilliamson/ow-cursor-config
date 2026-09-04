# Subagents (`subagents/`)

**What this is:** In Cursor, **subagents** (Task runs: `explore`, `shell`, `generalPurpose`, `bugbot`, `security-review`, etc.) are **child agent sessions** with their own context and tool budget. This directory is the place to version prompts or manifests next to commands, rules, and skills.

## Canonical delegation skill

Routing, output contracts, chaining, and anti-patterns live in **`/owcc-agent-delegate`**:

- Skill: [../skills/owcc-agent-delegate/SKILL.md](../skills/owcc-agent-delegate/SKILL.md)
- Reference: [../skills/owcc-agent-delegate/reference-delegation.md](../skills/owcc-agent-delegate/reference-delegation.md)

Use that skill before spawning Task subagents when the return payload would otherwise be long prose.

## Quick routing

| Task | Prefer | Return shape |
|------|--------|--------------|
| Locate symbol / callers / usages | `explore` (readonly) | `path:line — symbol — note` |
| Run build, test, git read-only | `shell` | command + exit + decisive stdout/stderr |
| ≤2-file edit, path known | Main thread | — |
| Diff / branch bug scan | `bugbot` | findings list |
| Security on local changes | `security-review` | full detail for high-severity items |
| 3+ files or cross-cutting feature | Main thread (+ plan if needed) | — |

## Contents

| Item | What it does |
|------|----------------|
| *(no definition files yet)* | Reserved for **subagent prompts, manifests, or references** you want versioned here. |

When you add files, add one table row per file and note when to use it.

## Related

| Need | Where |
|------|-------|
| Which skill or hook fits | `/owcc-tooling-help` |
| Session retro after heavy runs | `/owcc-session-retro` + `agent-retro-meter` hook |
