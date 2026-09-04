# Agent session retro — reference templates

Use only when the user wants a **full** write-up or copy-paste scaffolds. Default retro stays in the main `SKILL.md` format (capped, evidence-backed).

## Full retro report template

```markdown
# Session retro: <short title>

## Executive summary

- 
- 
- 
- 
- 

## Session facts

- **Repo / path:**
- **Branch:**
- **Mode:** Plan | Agent | Ask | unknown
- **Goal:**
- **Outcome:**
- **Constraints:**

## Timeline (optional)

| Step | What happened | Notes |
|------|----------------|-------|
| | | |

## Ranked root causes

### 1. <Cause title> (P0/P1/P2)

- **Evidence:**
- **Why it mattered:**
- **Remediation type:** prompt | doc | script | rule | skill | template
- **Proposed artifact / path:**

### 2. ...

## Prioritized backlog

| ID | Pri | Type | Location | Owner | Definition of done |
|----|-----|------|----------|-------|---------------------|
| R1 | P0 | | | user | |
| R2 | P1 | | | agent | |

## Before / after prompts

**Before:**

> 

**After:**

> 

## Next-time verification

1. 
2. 
3. 

## Redaction note

Confirm no secrets were included in pasted logs for this retro.
```

## New Cursor rule stub (`.cursor/rules/*.mdc`)

```markdown
---
description: <one line>
globs: <pattern or omit for alwaysApply>
alwaysApply: false
---

# <Title>

- Bullet conventions
- Link to doc or script if longer explanation needed
```

## New skill stub (`SKILL.md`)

```markdown
---
name: <lowercase-hyphen-name>
description: <third person WHAT + WHEN, trigger terms>
---

# <Title>

## When to use

## Steps

1. 
2. 

## Output format

## Optional

- See [reference.md](reference.md) if split content is needed.
```

## Helper script placeholder (README snippet)

```markdown
## <Task name>

Run:

`./scripts/<name>.sh` (or `python scripts/<name>.py`)

**Inputs:** ...
**Outputs:** ...
**Failure modes:** ...
```

## Exhaustive mode (user-requested)

If the user says **exhaustive mode**:

- Raise cap (agree a number, e.g. 10–15 actions) up front.
- Include optional “secondary issues” section.
- Still require evidence for each primary cause; mark low-confidence items clearly.

<a id="diagnosis-taxonomy"></a>

## Diagnosis taxonomy (examples)

Use as a checklist during step 2 of the main workflow; pick only what the evidence supports:

- Ambiguous success criteria or shifting requirements
- Missing orientation (`AGENTS.md`, architecture map, key entrypoints)
- Wrong tool or wrong command for the environment
- Environment mismatch (paths, shell, sandbox, network, permissions)
- Incorrect API/framework assumptions
- Over-broad search or wrong codebase area
- Plan vs Agent vs Ask confusion (e.g. could not execute vs chose wrong approach)
- Missing verification (no test/lint/run step before claiming done)
- Context loss / truncation / too much irrelevant history
- Conflicting rules or hidden constraints
- Repeated trial-and-error without a hypothesis

<a id="remediation-map"></a>

## Remediation map (hypothesis → artifact)

| Pattern | Prefer |
|--------|--------|
| Ambiguous asks, missing acceptance checks | Reusable **prompt template** + “definition of done” checklist |
| Repo layout unknown | **Short doc** (`AGENTS.md`, `docs/`, README section) with entrypoints and commands |
| Fragile/repeated commands | **Helper script** + one-line doc on how to run |
| Stable coding convention | Focused **Cursor rule** (`.cursor/rules/*.mdc`) with tight `globs` |
| Multi-step domain workflow | **Skill** (`SKILL.md`) with progressive disclosure |
| Repeated boilerplate outputs | **Template** (PR/issue/checklist markdown) |
