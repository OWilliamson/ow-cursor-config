# Plan review pass/fail checklist

Use after reading the **target plan** (file path or pasted content). Mark **Pass** / **Fail** / **N/A**; for each **Fail**, note the minimal fix.

## Target and scope

- [ ] **Target plan** path or full text was identified before edits (no wrong file).
- [ ] **Scope** (todos-only / body-only / full) matches what the user asked for.
- [ ] **Execution route** is known or assumed explicitly: Cursor Build, Agent from `@plan`, or human-led.

## Build sizing

- [ ] Plan is small enough for **one Build run** or split into **Build-sized phases**.
- [ ] Each phase has its own scope, first action, validation gate, and handoff.
- [ ] Plan says what to do if execution stops early: resume from first pending todo, do not rerun completed work blindly.

## Execution contract

- [ ] Frozen decisions are explicit (names, paths, versions, branch, legal/shipping).
- [ ] Definition of done is checkable (not "make it good").
- [ ] Non-goals listed where the team historically over-scopes.
- [ ] First action after approval is explicit (command, file, or workflow step).
- [ ] Final validation commands or review gates are explicit.
- [ ] Stop-if gates exist for decisions the Build agent must not guess (license, destructive changes, schema relaxation, parity changes, external writes).

## Todos (YAML or equivalent)

- [ ] Each todo is a **verb-led action** or a **binary verification** (no vague "ensure quality").
- [ ] No two todos repeat the same work unless one is **verify** after **implement**.
- [ ] Order matches **dependency** (cannot start B before A without noting parallel OK).
- [ ] Plan contains an explicit **sequential-execution directive** in the plan body, not only in operator notes (template: [reference-patterns.md](reference-patterns.md)).
- [ ] Each non-trivial implementation todo is paired with a **verification step** (exact command, diff check, or artifact check) (example: [reference-patterns.md](reference-patterns.md)).
- [ ] The final todo is a **completion audit**: confirm all N todos are marked done; do not report success until all are ticked (template: [reference-patterns.md](reference-patterns.md)).
- [ ] Overloaded todos are **split** OR **merged with sub-bullets in body** - pick one pattern consistently.
- [ ] Fuzzy items ("preserve behaviour", "parity") point to a **named checklist or diff target**.
- [ ] Ambiguous todos or gates include a short **example** where misreading is likely; self-explanatory items do not.
- [ ] Todo IDs, if present, are stable and kebab-case; wording-only edits do not churn IDs.

## Body (markdown)

- [ ] No long paragraph duplicates a todo `content` line-for-line.
- [ ] Reference paths appear in **one** grouped list where possible.
- [ ] Counts/lists (N services, N modes) have a **single canonical reference**.
- [ ] Deep technical notes appear **once** (MIB, OID, parity, perfdata).

## Context cost (when this plan is attached to Agent)

- [ ] `overview` / intro could stand alone for a quick orientation (optional but high leverage).
- [ ] Obvious boilerplate the repo already encodes in AGENTS.md/rules is **not** repeated unless this plan is used **outside** that repo.
- [ ] Long snippets are replaced with file paths, commands, or source-of-truth references where possible.
- [ ] Operator-only advice (model picking, restart habits, manual review habits) is kept outside mandatory plan tasks and moved to operator notes when needed.

## Resumability and state

- [ ] If work spans more than one Build run, the plan names an authoritative workspace file for progress/handoff (not only transient internal todos).
- [ ] Cursor internal todos are treated as a mirror unless the user explicitly makes them authoritative.
- [ ] Completed work is tracked outside the plan only if that avoids confusing the next Build pass.

## Handoff

- [ ] Next owner knows the **first concrete action** after approval (e.g. first shell command, first file to open, or first workflow step in the plan).
