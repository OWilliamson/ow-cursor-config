# Plan file

Contract for the plan file `/owcc-plan-improve` mutates or creates. Branching: [DECISIONS.md](DECISIONS.md). Workflow: [SKILL.md](SKILL.md).

**YAML vs Stages:** todo `id` + `status` drive Build. Stages holds expanded actions and Definition of done. On conflict, YAML `content` wins for verify commands and acceptance checks; align Stages to match.

## Template

```markdown
---
name: ""
overview: ""
todos:
  - id: first-implement-todo
    content: ""
    status: pending
  - id: completion-audit
    content: ""
    status: pending
isProject: false
---

# <!-- Plan title — must match frontmatter `name` -->

## Rules

<!-- Buildable: Plan file edit rule, Verify, Execution rule, First action, Final validation.
     Orchestrator: Authoritative Build file + Stop-if only. See Section Contract §1. -->

## Aims

<!-- Brief: 4–5 sentences — what and why. Then one OKR table (implement todos only). -->

| Todo | Objective | Result | Key signals |
|------|-----------|--------|-------------|
| `todo-id` | What this todo achieves | Checkable done-state | Depends / readiness / acceptance cues |

## Scope

<!-- In scope / Out of scope (with reasons). -->

## Target shape

<!-- Architecture, directories, schemas, “done looks like”. -->

## Stages

### Phase 1 — <name>   <!-- omit for lean flat -->

**Definition of done:** …

#### Todo `todo-id`

**Key actions:** …

## Additions

| Path | Content (1–2 sentences) | Reason (1–2 sentences) |
|------|-------------------------|------------------------|
| … | … | … |

## Modifications

| Path | Change (1–2 sentences) | Reason (1–2 sentences) |
|------|------------------------|------------------------|
| … | … | … |

## Removals

| Path | What goes away | Reason (1–2 sentences) |
|------|----------------|------------------------|
| … | … | … |

## Decisions

<!-- Cross-cutting only — or `None.` -->

## Reference

<!-- Read-only paths — or `None.` -->
```

### Buildable Rules block

Merge into `## Rules`. Adapt; do not paste blindly. Orchestrator plans use the Orchestrator block instead.

```markdown
**Plan file edit rule:** You may edit the plan file **only** to change frontmatter
todo `status` (`pending` → `in_progress` → `completed` | `cancelled`). Edit **only**
the `status:` line for the current todo; preserve order, ids, and `content`. Do **not**
edit plan body, overview, todo wording, or add/remove todos. Status-only exception.

**Verify:** terminal

**Execution rule:** Execute one todo at a time. Mark it complete before starting
the next. Do not batch, skip, or reorder unless the plan explicitly marks steps
as parallel-safe. If interrupted, resume from the first incomplete todo.

**Phase rule:** (only if isProject) Complete all todos in Phase 1 before Phase 2.

**First action:** `todo-id` — short description

**Final validation:** `completion-audit` — short description
```

`Verify` values: `terminal` (lean), `batched`, `per-todo` (full).

### Orchestrator Rules block

```markdown
**Authoritative Build file:** /absolute/path/to/active-implementation.plan.md

**Stop-if:** Plan UI Build is invoked on this file. Stop. Open Authoritative Build file
and Build there. Do not implement from index todos.
```

### Lean frontmatter example

```yaml
---
name: Hub docs pass
overview: Write three docs; validate at completion-audit.
todos:
  - id: glossary-doc
    content: Write docs/profile-and-sync-glossary.md
    status: pending
  - id: archival-policy
    content: Write docs/archival-policy.md
    status: pending
  - id: project-config-doc
    content: Write docs/project-config.md
    status: pending
  - id: completion-audit
    content: Confirm deliverables exist; run checks from Rules. Do not report success until done.
    status: pending
isProject: false
---
```

### Full-mode todo snippets

```yaml
- id: add-config
  content: >
    Write config/settings.yaml with fields host, port, and tls.enabled per §9 Decisions.
    Do not invent extra keys.
- id: verify-config
  content: Run `python -c "import config; config.load()"` and confirm no errors
- id: validate-phase-1
  content: >
    Phase 1 gate: all todos in this phase completed. Re-run phase validation
    commands. Do not start Phase 2 until this passes.
- id: completion-audit
  content: >
    Confirm all deliverables exist. Run validation commands from Rules.
    Do not report success until every todo is completed and checks pass.
```

```markdown
**Stop-if:** If the licence is not MIT or Apache-2.0, stop and ask before proceeding.
Do not infer or assume a licence.
```

## Sections

### Frontmatter (YAML §0)

#### Use

Always — all classes.

#### Empty Allowance

No.

### Title (body H1)

#### Use

Always — all classes.

#### Empty Allowance

No.

### `## Rules`

#### Use

Required for buildable-lean, buildable-full, orchestrator. Minimal for doc-only IF Build-run (edit rule + execution order).

#### Empty Allowance

No for buildable/orchestrator.

### `## Aims`

#### Use

Always — all classes. Short brief for orchestrator (program coordination).

#### Empty Allowance

No.

### `## Scope`

#### Use

Required for buildable-lean, buildable-full, doc-only. Orchestrator: program scope only.

#### Empty Allowance

No when required for class.

### `## Target shape`

#### Use

Required for buildable-full and code/feature plans. Optional for buildable-lean / doc-only / orchestrator.

#### Empty Allowance

Yes when optional — short N/A or “see §6”.

### `## Stages`

#### Use

Required for all buildable classes. Orchestrator: verify steps and child handoffs only.

#### Empty Allowance

No for buildable.

### `## Additions`

#### Use

When new files will be created.

#### Empty Allowance

Yes — write `None.` (literal). Do not omit the section or leave placeholder theater.

#### Table contract

- Header row must use exact columns: **Path** | **Content (1–2 sentences)** | **Reason (1–2 sentences)** (Content / Reason semantics).
- Each data row: one concrete path (backticks OK); Content = what the file will hold; Reason = why it is added.
- Prefer explicit rows when the path set is small. Abbreviated inventories (“and N similar”, ellipsis-only tables) leave execution-success preflight with `inventory_incomplete` — use only when listing every path would be noise (≥5 similar paths).

### `## Modifications`

#### Use

When existing files will change.

#### Empty Allowance

Yes — write `None.` (literal). Do not omit the section or leave placeholder theater.

#### Table contract

- Header row must use exact columns: **Path** | **Change (1–2 sentences)** | **Reason (1–2 sentences)**.
- Each data row: one concrete path; Change = what differs; Reason = why.
- Same abbreviate rule as Additions (`inventory_incomplete` when “and N similar”).

### `## Removals`

#### Use

When files or dirs will be deleted.

#### Empty Allowance

Yes — write `None.` (literal). Do not omit the section or leave placeholder theater.

#### Table contract

- Header row must use exact columns: **Path** | **What goes away** | **Reason (1–2 sentences)**.
- Each data row: one concrete path; What goes away = deleted artifact; Reason = why.
- Same abbreviate rule as Additions.

### `## Decisions`

#### Use

When cross-cutting agreements exist that cannot live in §1, §3, §4, or §5.

#### Empty Allowance

Yes — `None.` preferred.

### `## Reference`

#### Use

When non-obvious read-only context outside the plan exists.

#### Empty Allowance

Yes — `None.` when repo defaults suffice.

## Section Contract

### Content

- **Order:** YAML §0, then body Title H1, then `## Rules` … `## Reference` exactly as in Template. No other `#` H1.
- **Title:** First non-empty body line; text matches frontmatter `name` after trim (case-sensitive).
- **§0 Frontmatter:** `name`, `overview` (1–2 sentences from Aims), `todos` or `phases[].todos`, `isProject`. Each todo: kebab-case `id`, non-empty `content`, `status` in `pending` | `in_progress` | `completed` | `cancelled`. Lean: 3–8 implement todos, `completion-audit` last, flat or ≤2 phases, no verify-twin ids ([DECISIONS §5](DECISIONS.md#5-lean-vs-full-plan-shape), [§7](DECISIONS.md#7-flat-vs-phased-frontmatter)). Full: implement + `verify-*` pairs; `validate-phase-*` last in each non-final phase; `completion-audit` last. Phased: root `todos: []`; work under `phases[]`. Orchestrator: verify-only todos; overview states orchestrator-only. Class profile: [DECISIONS §9](DECISIONS.md#9-plan-class)–[§10](DECISIONS.md#10-section-profile-by-class).
- **§1 Rules (buildable):** Plan file edit rule (status-only); **Verify** `terminal` | `batched` | `per-todo`; execution rule; phase rule when `isProject: true`; **First action** / **Final validation** ids that exist in frontmatter; **Stop-if** when a wrong guess is costly. Optional process rules only if plan-wide. Not file inventories, architecture, or Aims rows.
- **§1 Rules (orchestrator):** Authoritative Build file + Stop-if only (Orchestrator Rules block).
- **§2 Aims:** Brief (4–5 sentences). Then one table with columns **Todo** | **Objective** | **Result** | **Key signals**. Rows = implement todos only (exclude `completion-audit`, `verify-*`, `validate-phase-*`, `cursor-native-close-verify`). **Objective** = what the todo achieves. **Result** = checkable done-state. **Key signals** = depends-on todo ids (or `none`) plus readiness/acceptance cues. `overview` stays a shorter distillation of the brief.
- **§3 Scope:** In scope (paths/systems/languages/envs); Out of scope with **reason**. May cross-link Rules Stop-if.
- **§4 Target shape:** End-state narrative, diagrams, directory layout, schema/config snippets (not full implementations).
- **§5 Stages:** Per phase (or single flat stage): Definition of done; per implement todo Key actions (omit only IF fully in YAML `content`). Full+phased: last todo in each non-final phase is `validate-phase-*`. Last plan todo is `completion-audit`. Lean collapse: relocate before dropping todos ([DECISIONS §15](DECISIONS.md#15-relocate-before-removing-todos)).
- **§6–§8:** Path tables as in Template with exact headers (Additions: Path | Content | Reason; Modifications: Path | Change | Reason; Removals: Path | What goes away | Reason). Empty → literal `None.` (not omitted). ≥5 similar paths may use example rows + “and N similar” — that marks execution preflight `inventory_incomplete`; prefer full rows when few paths.
- **§9 Decisions:** Overflow only — not a dump for scope, architecture, or stage detail ([DECISIONS §12](DECISIONS.md#12-map-substance-to-plan-section)).
- **§10 Reference:** Read-only paths for the build agent.
- **Strip (not protected):** Quoted “Do NOT edit the plan file itself”; `## How to run` / **Operator — how to run** / Plan UI click-paths; `### Progress tracking`; labels `**Execution route:**`, `**Plan shape:**`, `**Native chunks:**`, `**Plan-change-composer role:**`, `**Plan-build role:**`, `**Plan-registry role:**` ([DECISIONS §13](DECISIONS.md#13-protect-strip-or-migrate-content)).

### Authoring

- Prefer localized detail under Stages todos over §9 dumps.
- Adapt Template Rules/frontmatter examples; do not ship placeholder comments as plan content.
- Keep one-hop links to DECISIONS for branching; do not restate decision matrices here.
- Phased plans: work under `phases[].todos` — see §0 Content above.
