# Improve-run decisions

Enumerated decisions for `/owcc-plan-improve`, in **[SKILL.md](SKILL.md)** workflow order. Contracts and templates: [OUTPUTS.md](OUTPUTS.md). Rubric: [VALIDATION.md](VALIDATION.md).

## Index

| # | Decision | Workflow step |
|---|----------|---------------|
| 1 | [Target plan](#1-target-plan) | 5.3.1 |
| 2 | [Edit scope](#2-edit-scope) | 5.3.1 |
| 3 | [Sizing mode from invoke](#3-sizing-mode-from-invoke) | 5.3.2 |
| 4 | [Auto-pick lean or full](#4-auto-pick-lean-or-full) | 5.3.2 |
| 5 | [Lean vs full plan shape](#5-lean-vs-full-plan-shape) | 5.3.2; 5.3.4 |
| 6 | [Multi-plan strategy](#6-multi-plan-strategy) | 5.3.2 |
| 7 | [Flat vs phased frontmatter](#7-flat-vs-phased-frontmatter) | 5.3.2; 5.3.4 |
| 8 | [Chunk report flag response](#8-chunk-report-flag-response) | 5.3.2; 5.3.4 |
| 9 | [Plan class](#9-plan-class) | 5.3.3 |
| 10 | [Section profile by class](#10-section-profile-by-class) | 5.3.3; 5.3.4 |
| 11 | [Inventory substance class](#11-inventory-substance-class) | 5.3.3 |
| 12 | [Map substance to plan section](#12-map-substance-to-plan-section) | 5.3.3; 5.3.4 |
| 13 | [Protect strip or migrate content](#13-protect-strip-or-migrate-content) | 5.3.4 |
| 14 | [Restructure situation response](#14-restructure-situation-response) | 5.3.4 |
| 15 | [Relocate before removing todos](#15-relocate-before-removing-todos) | 5.3.4 |
| 16 | [Body vs YAML deduplication](#16-body-vs-yaml-deduplication) | 5.3.4 |
| 17 | [Legacy heading migration](#17-legacy-heading-migration) | 5.3.4 |
| 18 | [Fidelity gate](#18-fidelity-gate) | 5.3.4 |

---

## 1. Target plan

**Workflow:** 5.3.1

| Option | Description | Choose when | Apply to |
|--------|-------------|-------------|----------|
| **Use given path or paste** | Edit the plan at the path or pasted body | User `@` tags a file, gives absolute/relative path, or pastes plan content | That file or new file from paste |
| **Session native plan** | Edit the `.plan.md` saved this session | Cursor native plan created in chat (e.g. `.cursor/plans/`) | Path once saved |
| **New plan file** | Create plan from skeleton | User wants a new plan at an agreed path | CREATE file; [OUTPUTS.md](OUTPUTS.md) Template; SKIP TO 5.3.4 until content exists |
| **Open file in IDE** | Use the file the user means | “Improve this plan”, file open, and chat shows it as the subject | That path IF unambiguous |
| **Chat default** | Most recently discussed plan in this chat | `/owcc-plan-improve` only, no path | Paths, `@`, or edits cited in this thread |
| **Ask operator** | One-line ask for path or paste | Two+ plans in play; or none identified | Do NOT guess |

**Not valid targets:** IDE Recently viewed unrelated to chat; newest plan in workspace without chat link; older topic’s plan unless still active.

---

## 2. Edit scope

**Workflow:** 5.3.1

| Option | Description | Choose when | Apply to |
|--------|-------------|-------------|----------|
| **Full pass** | Frontmatter §0 + body §1–10 + todos/phases | Default; user did NOT narrow scope | Entire plan |
| **Todos only** | Rescale §0; minimal body edits for id alignment | User asked todos-only | §0; touch §1/§5 only IF Rules/Stages ids must match |
| **Body only** | Reshape Title H1 + §1–10 | User asked body-only | Body; §0 ids unchanged unless structure scripts require fix |

IF unclear, THEN use **full pass**.

---

## 3. Sizing mode from invoke

**Workflow:** 5.3.2; also 5.3.4 Frontmatter for new plans after content exists.

| Option | Description | Choose when | Apply to |
|--------|-------------|-------------|----------|
| **Lean** | Homogeneous, low-risk sizing path | User message includes `lean` | [5 Lean vs full plan shape](#5-lean-vs-full-plan-shape) lean row; reconcile [9 Plan class](#9-plan-class) |
| **Full** | Mixed, risky, multi-milestone sizing path | User message includes `full` | [5](#5-lean-vs-full-plan-shape) full row; reconcile [9](#9-plan-class) |
| **Auto** | Agent picks lean or full | User says `auto` or omits mode (default) | [4 Auto-pick lean or full](#4-auto-pick-lean-or-full) then [5](#5-lean-vs-full-plan-shape) |

State chosen mode in chat when using **auto**.

---

## 4. Auto-pick lean or full

**Workflow:** 5.3.2 — when [3](#3-sizing-mode-from-invoke) IS **Auto**.

| Option | Description | Choose when | Apply to |
|--------|-------------|-------------|----------|
| **Pick lean** | Use lean shape and `buildable-lean` unless orchestrator | **Most** of: homogeneous output; no external/destructive/licence stop-if; chunk suggests `homogeneous_work` or `merge_phases`; single workspace; not multi-file program | [5](#5-lean-vs-full-plan-shape); [9](#9-plan-class) |
| **Pick full** | Use full shape and `buildable-full` unless orchestrator/doc-only | Any auto-pick criterion for lean is not met | [5](#5-lean-vs-full-plan-shape); [9](#9-plan-class) |

---

## 5. Lean vs full plan shape

**Workflow:** 5.3.2 after sizing mode set; 5.3.4 rescale §0.

| Option | Description | Choose when | Apply to |
|--------|-------------|-------------|----------|
| **Lean** | Flat or ≤2 phases; 3–8 implement todos; no verify-twin ids; `Verify: terminal` in §1 Rules | [3](#3-sizing-mode-from-invoke) or [4](#4-auto-pick-lean-or-full) → lean | §0 todos; `completion-audit` holds terminal checks; [OUTPUTS.md](OUTPUTS.md) Lean frontmatter example |
| **Full** | Phases when warranted; implement + `verify-*` pairs; `Verify: per-todo` or `batched` | [3](#3-sizing-mode-from-invoke) or [4](#4-auto-pick-lean-or-full) → full; multi-file default | §0 / phases; [OUTPUTS.md](OUTPUTS.md) Full-mode todo snippets |

Invoke examples: `/owcc-plan-improve lean @plan.md`, `/owcc-plan-improve full @plan.md`.

---

## 6. Multi-plan strategy

**Workflow:** 5.3.2 — multiple files or chunk suggests split.

| Option | Description | Choose when | Apply to |
|--------|-------------|-------------|----------|
| **A — Implementation children** | Separate buildable child plans | Child plans exist or mid-flight handoff | Build **child only**; each child full OUTPUTS shape + buildable class |
| **B — Single phased plan** | One `isProject: true` file | One Plan UI tree; one workspace program | One file; phase per Build |
| **C — Verify-only index** | Orchestrator index + children | Must keep a third index file | Index class **orchestrator**; [OUTPUTS.md](OUTPUTS.md) Orchestrator Rules block |

Default sizing for multi-file programs: **full** ([5](#5-lean-vs-full-plan-shape)). Do NOT create three full implementation plans by default. Fail improve IF strategy unclear or index has implement todos without **Authoritative Build file**.

---

## 7. Flat vs phased frontmatter

**Workflow:** 5.3.2 note intent; 5.3.4 set `isProject` and phases.

| Option | Description | Choose when | Apply to |
|--------|-------------|-------------|----------|
| **Flat** | `isProject: false`; todos at root | Lean or auto→lean; [8](#8-chunk-report-flag-response) `merge_phases`; homogeneous work; no phase human gate | §0 root `todos` |
| **≤2 coarse phases** | Minimal phasing | Lean needs light separation only | `isProject: true`; 1–2 phases |
| **Phased** | `isProject: true`; `todos: []` at root | Full mode; milestones; human gates between phases; Plan UI one phase per chunk | `phases[].todos`; phase-validation todos |

Do NOT add phases on small plans only to clear chunk weight. Prefer flat when plan has 3+ phases with &lt;3 todos per phase on average.

---

## 8. Chunk report flag response

**Workflow:** 5.3.2 note flags; 5.3.4 chunk-driven reshape. Advisory unless structure/qualitative scripts fail.

| Option | Description | Choose when | Apply to |
|--------|-------------|-------------|----------|
| **Dismiss `missing_verify` (lean)** | Do NOT add verify-twin todos | Lean mode; flag only | Keep `Verify: terminal` + `completion-audit` |
| **Merge `redundant_grep_verify`** | Drop or merge verify twin after relocating checks | Lean; verify todo duplicates grep | [15 Relocate before removing todos](#15-relocate-before-removing-todos) first |
| **Prefer flat / merge phases** | Flatten or ≤2 phases | `merge_phases` or [7](#7-flat-vs-phased-frontmatter) flat signals | §0 shape |
| **Split or relocate todo** | Split todos or move detail to Stages / Target shape | `split_todo`, high weight, overloaded | [14](#14-restructure-situation-response); [15](#15-relocate-before-removing-todos) |
| **Dismiss `add_phases`** | Do NOT add phases for weight | Small homogeneous plan | [7](#7-flat-vs-phased-frontmatter) flat |
| **Propose multi-plan** | A, B, or C | Chunk suggests multiple files | [6](#6-multi-plan-strategy) |

Never shorten text solely to clear weight flags.

---

## 9. Plan class

**Workflow:** 5.3.3

| Option | Description | Choose when | Apply to |
|--------|-------------|-------------|----------|
| **orchestrator** | Index; do NOT Build this file | **Authoritative Build file** in Rules; verify-only work; [6C](#6-multi-plan-strategy) | [10](#10-section-profile-by-class) orchestrator column; [OUTPUTS.md](OUTPUTS.md) Orchestrator Rules block |
| **doc-only** | Docs/config deliverables only | No application code changes | [10](#10-section-profile-by-class) doc-only; relaxed §4 / A/M/R |
| **buildable-lean** | Single-file lean build | Sizing → lean; not orchestrator | [10](#10-section-profile-by-class) buildable-lean |
| **buildable-full** | Buildable with full sizing | Sizing → full; phased/risky/mixed; not orchestrator | [10](#10-section-profile-by-class) buildable-full |

State class in chat when not obvious. **doc-only** still uses buildable Rules when the plan is Build-run.

---

## 10. Section profile by class

**Workflow:** 5.3.3 checklist; 5.3.4 Contracts.

| Class | Description | Choose when | Apply to |
|--------|-------------|-------------|----------|
| **buildable-lean** | Lean sections + scaled §0 | [9](#9-plan-class) buildable-lean | Title; §0 lean; §1 Buildable Rules block; §2–3, §5 required; §4 short optional; §6–8 IF files change; §9–10 IF needed |
| **buildable-full** | Full sections + verify pairing | [9](#9-plan-class) buildable-full | Title; §0 full/phased; §1 Buildable Rules block; §2–5 + phase DoD; §6–8 when applicable |
| **orchestrator** | Index profile | [9](#9-plan-class) orchestrator | Title; §0 verify todos; §1 Orchestrator Rules block; §2 program Aims; §5 verify/handoffs; §10 child paths |
| **doc-only** | Doc-focused profile | [9](#9-plan-class) doc-only | Title; same as lean buildable with optional §4; A/M/R when paths change |

Detail per section: [OUTPUTS.md](OUTPUTS.md) §0–§10. Empty §6–§8 → `None.` when allowed.

---

## 11. Inventory substance class

**Workflow:** 5.3.3 — build substance inventory (do NOT invent items).

| Option | Description | Choose when | Apply to |
|--------|-------------|-------------|----------|
| **Definitions** | Requirements, acceptance, specs, naming, deliverable paths | Item describes *what* must exist or contain | [12](#12-map-substance-to-plan-section) → Aims, Target shape, Stages, §6–8 |
| **Workflow** | Order, gates, dependencies, resume, parallel-safe marks | Item describes *order* or *when to stop/advance* | [12](#12-map-substance-to-plan-section) → Rules, Stages |
| **Contracts** | Verify mode, concrete checks, non-goals, Authoritative Build | Item binds execution or cross-cutting agreement | [12](#12-map-substance-to-plan-section) → Rules, Scope, §9 |

Operator chrome is not inventory — [13](#13-protect-strip-or-migrate-content).

---

## 12. Map substance to plan section

**Workflow:** 5.3.3 map each inventory item; 5.3.4 Migrate inventory.

| Option | Description | Choose when | Apply to |
|--------|-------------|-------------|----------|
| **§2 Aims** | Brief + OKR table (Todo \| Objective \| Result \| Key signals) | Intent or per-todo objective/result/signals | `## Aims` |
| **Title H1** | Display title matching `name` | Plan title line in body | `#` heading before `## Rules` |
| **§3 Scope** | In/out boundaries with reasons | Workspace, systems, or explicit non-goals | `## Scope` |
| **§4 Target shape** | End-state architecture, dirs, schemas | “Done looks like”; structure at completion | `## Target shape` |
| **§5 Stages** | Key actions, Definition of done per phase/todo | Step-by-step work under a todo id | `## Stages` |
| **§1 Rules** | Edit rule, Verify, execution order, stop-if, First/Final ids | Plan-wide *how* to run the plan | `## Rules` |
| **§6–§8 A/M/R** | File create / change / remove rows | Deliverable is a specific path | Additions / Modifications / Removals tables |
| **§9 Decisions** | Cross-cutting agreement only | Cannot fit §3, §4, §5, or §1 without breaking context | `## Decisions` — not a dump ([OUTPUTS.md](OUTPUTS.md) §9) |
| **§10 Reference** | Read-only context paths | Specs, skills, docs agent must read | `## Reference` |
| **§0 todo `content`** | Build handoff line for a todo | Checkable acceptance or verify command for Build | YAML — wins over Stages for verify/acceptance text |

Every inventory item must land in one primary row; cross-reference duplicates in [16](#16-body-vs-yaml-deduplication).

---

## 13. Protect strip or migrate content

**Workflow:** 5.3.4 Strip.

| Option | Description | Choose when | Apply to |
|--------|-------------|-------------|----------|
| **Protect** | Keep; relocate IF section changes | Requirements, acceptance, verify commands, stop-if, gates, specs | [12](#12-map-substance-to-plan-section); never DELETE unless [18](#18-fidelity-gate) user-approved removal |
| **Strip** | Remove from plan body | Plan UI how-to-run; quoted “Do NOT edit the plan file itself”; `### Progress tracking`; forbidden labels | [OUTPUTS.md](OUTPUTS.md) Section Contract strip list |
| **Migrate** | Move into §1–10; remove legacy block | Legacy `## Frozen decisions` / `## Execution contract` | [17](#17-legacy-heading-migration) |

---

## 14. Restructure situation response

**Workflow:** 5.3.4 — when this situation arises during restructure.

| Option | Description | Choose when | Apply to |
|--------|-------------|-------------|----------|
| **Normalize skeleton** | Add Title H1 + §1–10 in OUTPUTS order; move prose into sections | Headings missing or out of order | 5.3.4 skeleton |
| **Migrate inventory** | Place each inventoried item per [12](#12-map-substance-to-plan-section) | After skeleton exists | 5.3.4 migrate; no net loss |
| **Fill contracts** | Complete sections for [10](#10-section-profile-by-class) | Class known | 5.3.4 contracts; [OUTPUTS.md](OUTPUTS.md) |
| **Rescale §0** | Lean/full todos and phases | After substance placed | 5.3.4 frontmatter; [5](#5-lean-vs-full-plan-shape), [7](#7-flat-vs-phased-frontmatter) |
| **Chunk reshape** | Act on flags from 5.3.2 | 5.3.4 chunk reshape | [8](#8-chunk-report-flag-response) |
| **Align cross-refs** | `name`, Title H1, `overview`, Stages ids, Rules First/Final ids | After §0 and body drafted | 5.3.4 align |
| **User-approved cut** | Remove only user-dropped requirements | User explicitly approved scope reduction | Inventory minus approved items only |
| **Body-only id touch** | Change todo ids only for script fix | [2](#2-edit-scope) body only + structure script error | §0 minimal fix |

Default when unsure: preserve substance; split or relocate — do NOT shorten for chunk weight.

---

## 15. Relocate before removing todos

**Workflow:** 5.3.4 — before merging or deleting any todo.

| Option | Description | Choose when | Apply to |
|--------|-------------|-------------|----------|
| **Stages** | Move steps and acceptance into Stages under todo id | Lean collapse; todo merge | `## Stages` |
| **Surviving todo `content`** | Move checks into another todo’s YAML | Collapse to fewer todos | §0 |
| **`completion-audit`** | Terminal verify commands | Lean; checks were on dropped verify twins | Last todo `content` + §5 |
| **§4 Target shape** | Spec/detail for end state | Detail is architectural not step-level | Target shape |
| **Do not drop yet** | Keep todo until relocate done | Any relocate row not completed | Inventory item would be lost |

Order of preference: Stages → surviving `content` → `completion-audit` → Target shape.

---

## 16. Body vs YAML deduplication

**Workflow:** 5.3.4 Deduplicate.

| Option | Description | Choose when | Apply to |
|--------|-------------|-------------|----------|
| **Keep richer Stages; shorten YAML** | Detail in Stages; one-line `content` | Stages has full steps; YAML repeats | §5 + §0 |
| **Keep richer YAML; point Stages** | Verify/acceptance in `content` | Commands and checks in YAML | §0 wins verify/acceptance wording |
| **Single location only** | DELETE duplicate prose | Same text in two places | Keep richer per row above; cross-reference the other |

[OUTPUTS.md](OUTPUTS.md) canonical split: YAML **wins** on verify commands and acceptance checks; Stages must match.

---

## 17. Legacy heading migration

**Workflow:** 5.3.4 Migrate inventory.

| Option | Description | Choose when | Apply to |
|--------|-------------|-------------|----------|
| **→ §1 Rules** | Execution contract, edit rule, Verify, sequential rule | `## Execution contract` or equivalent | `## Rules` |
| **→ §9 or localized Stages** | Frozen bullet decisions | `## Frozen decisions` | §9 IF cross-cutting; else under todo in §5 |
| **→ §3 Scope** | Non-goals and boundaries | Legacy “out of scope” blocks | `## Scope` |
| **Remove legacy heading** | DELETE empty legacy section after migrate | Content fully moved | Body |

Do NOT leave duplicate legacy blocks after migrate.

---

## 18. Fidelity gate

**Workflow:** 5.3.4 — after strip; gate before §5.3.5 Validate.

| Option | Description | Choose when | Apply to |
|--------|-------------|-------------|----------|
| **Pass** | Inventory ⊆ plan | Every item from 5.3.3 appears in Title, §0, or §1–10 | Proceed to 5.3.5 Validate |
| **Restore missing** | Put item back in mapped section | Re-scan finds gap | [12](#12-map-substance-to-plan-section) |
| **Record relocation** | Note in 5.3.6 report | Item moved section | Chat delta |
| **User-approved removal** | Drop inventoried item | User explicitly approved in chat | Remove from inventory; document in report |
| **Block** | Cannot restore without inventing requirements | Missing substance and no user approval | Report blocker; do NOT mark improve done |

Do NOT invent requirements to fill gaps.
