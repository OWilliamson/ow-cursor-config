# Triage decisions

Enumerated decisions for `/owcc-plan-triage`, in **[SKILL.md](SKILL.md)** workflow order. Rubric: [VALIDATION.md](VALIDATION.md).

## Index

| # | Decision | Workflow step |
|---|----------|---------------|
| 1 | [Target plan](#1-target-plan) | 5.3.1 |
| 2 | [Session intent harvest](#2-session-intent-harvest) | 5.3.2 |
| 3 | [Severity](#3-severity) | 5.3.4 |
| 4 | [Four axes](#4-four-axes) | 5.3.3–5.3.4 |
| 5 | [Patch matrix](#5-patch-matrix) | 5.3.5 |
| 6 | [Patch limits](#6-patch-limits) | 5.3.5 |

---

## 1. Target plan

**Workflow:** 5.3.1

| Option | Description | Choose when | Apply to |
|--------|-------------|-------------|----------|
| **Use given path or paste** | Triage that plan | User `@` tags a file, gives path, or pastes content | That file (prefer saved path for edits) |
| **Session native plan** | Triage `.plan.md` saved this session | Cursor native plan created in chat | Path once saved |
| **Open file in IDE** | Use the file the user means | “Triage this plan”, file open, chat subject matches | That path IF unambiguous |
| **Chat default** | Most recently discussed plan in this chat | `/owcc-plan-triage` only, no path | Paths, `@`, or edits cited in this thread |
| **Ambiguous / none** | Ask once | Two+ candidates or none | Do NOT guess |

**Do not use:** IDE Recently viewed unrelated to this chat; arbitrary latest plan file without chat linkage.

---

## 2. Session intent harvest

**Workflow:** 5.3.2

### What counts as a session ask

| Counts | Does not count |
|--------|----------------|
| Explicit user requests to include something in the plan | Assistant suggestions the user never endorsed |
| User corrections or refinements to plan content | Hypothetical options the user did not choose |
| User-stated constraints, non-goals, or scope boundaries | Prior-session asks unless re-stated in this chat |
| User answers to clarifying questions that commit to content | Implied requirements with no user statement |

### Supersession rules

1. **Later user message wins** when it contradicts or narrows an earlier ask.
2. **Explicit drop** ("don't include", "remove", "out of scope", "skip") supersedes an earlier "add".
3. **Refinement** ("actually use X instead of Y") replaces the earlier ask — do not report both.
4. **Approval of assistant draft** counts only when the user explicitly adopts it ("yes", "use that", "looks good, save it").

### Mapping to plan

| Status | Meaning |
|--------|---------|
| **present** | Fully reflected in overview, Aims, Scope, Decisions, Rules, Stages, todos, or A/M/R tables |
| **partial** | Mentioned but missing acceptance criteria, todo, stop-if, or concrete path |
| **absent** | Not in the plan at all |

Record expected plan locus when absent or partial. Do not invent asks to fill gaps.

---

## 3. Severity

**Workflow:** 5.3.4

| Severity | Meaning | Patch |
|----------|---------|-------|
| `blocker` | Build likely fails or violates explicit user intent | Patch IF clear; ELSE `ask-user` |
| `should-fix` | Gap or risk that will confuse the build agent | Patch when locus clear |
| `ask-user` | Relevance or resolution ambiguous | Report only; do NOT invent |
| `note` | Observation; no change required | Optional minor clarification |

Triage does **not** gate build — operator decides whether to proceed.

---

## 4. Four axes

**Workflow:** 5.3.3–5.3.4

### Axis 1 — Session intent lag

**Question:** Did user asks from this session (not superseded) make it into the plan?

**Check:** Harvest per §2; compare against overview, Aims, Scope, Decisions, Rules, Stages, todos, A/M/R.

**Patch:** Absent ask with clear deliverable → add todo or Additions/Modifications row; absent constraint → **Stop-if** or out-of-scope; partial → strengthen section or acceptance line.

### Axis 2 — Internal contradictions

**Question:** Do steps, workflow, logic, or facts conflict within the plan?

**Check:** Todo order vs Stages; Scope vs path tables vs todos; Rules Verify mode vs todo verify pattern; Decisions vs todos/non-goals; duplicate conflicting approaches; First/Final validation ids missing from frontmatter.

**Patch:** Resolve toward later Decisions or explicit session intent; clarify order or remove duplicate approach (do NOT delete requirements without approval); IF ambiguous → `ask-user`.

### Axis 3 — Loose ends / boundary (conservative)

**Question:** Are relevant paths, systems, or scope items undefined?

**Check (bounded):** User-named paths/systems never scheduled; plan-referenced paths never in A/M/R or todos; plan-adjacent siblings that must ship together; contested items neither in-scope nor out-of-scope.

**Do not:** Speculative full-repo expansion; flag distant systems with no chat or plan linkage.

**Patch:** High confidence → add row/todo or explicit out-of-scope; speculative → `ask-user` only.

### Axis 4 — Executor information gaps

**Question:** Does the build agent have enough information to execute?

**Check:** Todos without checkable done criteria; commands without success criteria; vague paths; secrets/MCP/external writes without Stop-if or Scope boundary; Stages missing key actions; later phase assumes earlier artifact without naming path.

**Patch:** Add concrete path, command, or acceptance line; add **Stop-if** when wrong guess is costly; substance only — no lean/full reshape.

---

## 5. Patch matrix

**Workflow:** 5.3.5

| Finding type | Patch action |
|--------------|--------------|
| Absent session ask | Add todo, **Stop-if**, non-goal, or body note in the right section |
| Contradiction | Resolve toward later frozen decision or clearer todo order; IF ambiguous → `ask-user` |
| Loose end (high confidence) | Add in-scope todo or explicit out-of-scope/non-goal; IF speculative → `ask-user` |
| Executor gap | Add paths, commands, acceptance criteria, or definitions to body/todos |

---

## 6. Patch limits

**Workflow:** 5.3.5

Do **not** during triage:

- Rescale todos for lean/full sizing
- Inject execution-contract boilerplate (owcc-plan-improve owns Rules shape)
- Add verify-twin todos for form
- RUN validation scripts or WRITE `.validation.json`
- Remove requirements without user approval
- Invent session asks from assistant brainstorming
