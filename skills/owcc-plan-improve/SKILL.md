---
name: owcc-plan-improve
description: >-
  Use when improving a plan file's structure, sizing, section contracts, or
  execution rules via /owcc-plan-improve (optional lean|full|auto).
disable-model-invocation: true
---

# 1. Plan improve

The aim of invoking owcc-plan-improve is to rewrite a plan file toward OUTPUTS-ordered sections, lean/full sizing, and executable Rules — without dropping inventoried requirements.

Explicit-only. Invoke with `/owcc-plan-improve`. Optional same-line sizing: `lean`, `full`, or `auto` (default).

## 2. When to use

- Plan needs structure, sizing, section contracts, or execution rules improved.
- Plan is ambiguous, oversized, duplicated, hard to resume, or missing Aims/Stages alignment.
- Operator wants a new plan skeleton at an agreed path.

## 3. Inputs

| Signal | How to act |
|--------|------------|
| Plan path (absolute or workspace-relative) | Target ([DECISIONS §1](DECISIONS.md#1-target-plan)) |
| `@` on a plan file | Resolve that path as target |
| Cursor native plan this session | Prefer `.cursor/plans/*.plan.md` once saved |
| Intent to write a new plan | CREATE skeleton ([OUTPUTS.md](OUTPUTS.md)); agree path first |
| `lean` / `full` / `auto` on invoke line | Sizing ([DECISIONS §3](DECISIONS.md#3-sizing-mode-from-invoke)); default **auto** |
| `todos-only` / `body-only` / full | Edit scope ([DECISIONS §2](DECISIONS.md#2-edit-scope)); default **full** |
| No path / ambiguous | Ask once; do NOT guess |

## 4. Scope

**In scope:** mutate plan frontmatter (§0) and body (Title H1 + §1–10); run chunk/qualitative/structure scripts with `--json`; Relocate/Compress inventory; strip operator chrome; OUTPUT chat delta.

**Out of scope:** substance interrogation (session-intent lag, contradictions, loose-end/scope patching, executor info-gap fixes); writing `.validation.json` report files; user-unapproved removal of requirements/acceptance/gates/verify checks ([DECISIONS §18](DECISIONS.md#18-fidelity-gate)); shortening todo/body text solely to clear chunk weight ([DECISIONS §8](DECISIONS.md#8-chunk-report-flag-response)); adding verify-twin todos under **lean** only to clear `missing_verify`.

## 5. Workflow

### 5.1. Workflow Operators

These operator words mark specific operations in the workflow. When used as operators, they must be capitalised. When used for ordinary meaning (not as an operator), they must be lower case.

| Operator | Meaning | Example |
|----------|---------|---------|
| IF | Conditional test | IF new plan, THEN CREATE skeleton |
| THEN | Consequence of IF | IF scripts fail, THEN RETURN TO |
| ELSE | Alternate branch | ELSE use existing plan |
| AND | Conjoin requirements | DECIDE target AND edit scope |
| NOT | Negation / forbid | do NOT invent requirements |
| IS | Equality / state check | IF sizing IS auto |
| IN | Location / membership | item IN inventory |
| CREATE | Make a new artifact | CREATE skeleton from OUTPUTS |
| MODIFY | Change existing content | MODIFY plan sections |
| DELETE | Remove with approval | DELETE only with user approval |
| RUN | Execute a command or check | RUN chunk report |
| READ | Load and use a document | READ [OUTPUTS.md](OUTPUTS.md) |
| WRITE | Produce new content at a path | WRITE plan body |
| REWRITE | Replace section content | REWRITE Rules block |
| SKIP TO | Jump forward | SKIP TO 5.3.4 |
| RETURN TO | Go back | RETURN TO script step |
| WHILE | Repeat while condition holds | WHILE scripts fail |
| DECIDE | Choose via a decision matrix | DECIDE sizing |
| OUTPUT | Emit the completion response | OUTPUT §7 |

### 5.2. Workflow Rules

- Carry out steps top to bottom; meet each **Outcome** before continuing.
- Stay within §4; when a step links a doc, READ that section for the step.
- Apply §5.1 operator capitalisation in step bodies; do not shout ordinary prose.
- Do NOT drop requirements — Relocate or Compress ([DECISIONS §18](DECISIONS.md#18-fidelity-gate)).
- One canonical home per policy; YAML `content` wins verify/acceptance wording over Stages ([OUTPUTS.md](OUTPUTS.md)).
- Prefer verifiable script checks ([VALIDATION.md](VALIDATION.md)); SKILL links one hop (DECISIONS may point to OUTPUTS/VALIDATION).

| Excuse | Reality |
|--------|---------|
| “Chunk weight high — shorten the todo text.” | Relocate detail; never shorten solely for weight ([DECISIONS §8](DECISIONS.md#8-chunk-report-flag-response)). |
| “Lean failed `missing_verify` — add verify twins.” | Keep `Verify: terminal` + `completion-audit`; do NOT add twins for the flag alone. |
| “This requirement is awkward in OUTPUTS order — drop it.” | Relocate or Block; DELETE only with explicit user approval ([DECISIONS §18](DECISIONS.md#18-fidelity-gate)). |
| “Scripts passed — skip coherence read.” | Always READ top-to-bottom after scripts pass (§5.3.5). |

### 5.3. Workflow Steps

#### 5.3.1. Resolve target and scope

1. DECIDE target per [DECISIONS §1](DECISIONS.md#1-target-plan).
2. IF **new plan**, THEN CREATE file from [OUTPUTS.md](OUTPUTS.md) Template skeleton; SKIP TO 5.3.4 (no chunk report until substantive content exists).
3. DECIDE edit scope per [DECISIONS §2](DECISIONS.md#2-edit-scope).

**Outcome:** Plan path (or new file), edit scope, new vs existing.

#### 5.3.2. Chunk report and sizing (existing plan)

1. IF step 5.3.1 created an empty skeleton, THEN SKIP TO 5.3.4 until content exists.
2. RUN chunk report:

```bash
python3 ~/.cursor/skills/owcc-plan-validation-report/scripts/plan-chunk-report.py --json /absolute/path/to/plan.md
```

3. DECIDE sizing: [DECISIONS §3](DECISIONS.md#3-sizing-mode-from-invoke) → [§4](DECISIONS.md#4-auto-pick-lean-or-full) when `auto` → [§5](DECISIONS.md#5-lean-vs-full-plan-shape).
4. IF delivery spans multiple files, THEN DECIDE [DECISIONS §6](DECISIONS.md#6-multi-plan-strategy).
5. Note flat vs phased intent ([DECISIONS §7](DECISIONS.md#7-flat-vs-phased-frontmatter)).
6. Note chunk flags for 5.3.4 ([DECISIONS §8](DECISIONS.md#8-chunk-report-flag-response)).

**Outcome:** Chunk JSON reviewed; lean or full chosen; multi-file and phase shape decided.

#### 5.3.3. Classify and inventory

1. DECIDE plan class ([DECISIONS §9](DECISIONS.md#9-plan-class)).
2. Confirm sections to fill ([DECISIONS §10](DECISIONS.md#10-section-profile-by-class); [OUTPUTS.md](OUTPUTS.md)).
3. READ [OUTPUTS.md](OUTPUTS.md) for Title H1, heading order, and Stages sub-structure.
4. Build substance inventory: classify ([DECISIONS §11](DECISIONS.md#11-inventory-substance-class)); map ([DECISIONS §12](DECISIONS.md#12-map-substance-to-plan-section)). Do NOT invent requirements.

**Outcome:** Plan class, section checklist, substance inventory (item → class → section).

#### 5.3.4. Restructure and migrate

Work in order. Sub-steps map to [DECISIONS §14](DECISIONS.md#14-restructure-situation-response).

1. **Skeleton** — Normalize Title H1 + §1–10 ([OUTPUTS.md](OUTPUTS.md) Template).
2. **Migrate inventory** — Place items; legacy headings per [DECISIONS §17](DECISIONS.md#17-legacy-heading-migration).
3. **Contracts** — Fill per [DECISIONS §10](DECISIONS.md#10-section-profile-by-class) and [OUTPUTS.md](OUTPUTS.md).
4. **Frontmatter** — Rescale §0; before removing todos apply [DECISIONS §15](DECISIONS.md#15-relocate-before-removing-todos).
5. **Chunk-driven reshape** — Apply [DECISIONS §8](DECISIONS.md#8-chunk-report-flag-response).
6. **Align cross-references** — `name`, Title H1, `overview`, Stages ids, Rules First/Final ids.
7. **Deduplicate** — [DECISIONS §16](DECISIONS.md#16-body-vs-yaml-deduplication).
8. **Strip** — [DECISIONS §13](DECISIONS.md#13-protect-strip-or-migrate-content).
9. **Fidelity gate** — [DECISIONS §18](DECISIONS.md#18-fidelity-gate).

**Outcome:** OUTPUTS contracts satisfied; inventory complete; operator chrome stripped.

#### 5.3.5. Validate

Scripts enforce todos, Rules edit contract, qualitative hygiene, Title H1 / §1–§10 structure, and coherence. Coherence reading catches substance mismatches scripts cannot judge.

This is the **edit-loop** gate (`--json` only). Do **not** WRITE `.validation.json` here. A later operator-run validation-report (non-cursor-native build gate) re-runs the same scripts to write the artifact — do not skip this loop “because VR will run,” and do not invoke the write script from improve.

1. IF 5.3.2 was skipped or 5.3.4 changed todos/phases materially, THEN re-RUN chunk report (same command as 5.3.2) AND apply [DECISIONS §8](DECISIONS.md#8-chunk-report-flag-response) only when flags warrant reshape.
2. RUN AND parse `--json` (qualitative = hygiene; structure = outline/gates — each once):

```bash
python3 ~/.cursor/skills/owcc-plan-validation-report/scripts/plan-qualitative-report.py --json /absolute/path/to/plan.md
python3 ~/.cursor/skills/owcc-plan-validation-report/scripts/plan-validate-structure.py --json /absolute/path/to/plan.md
```

3. Fix errors reported by the scripts.
4. IF either script still fails, THEN RETURN TO step 2 of this section.
5. When scripts pass, continue.
6. READ the plan top to bottom for coherence (Title matches `name`, Aims match work, Stages match todos, Scope and Target shape align with file tables, Rules ids exist in frontmatter, no section contradictions).
7. IF problems found, THEN check [OUTPUTS.md](OUTPUTS.md) and plan context; MODIFY; RETURN TO step 2 of this section.

**Outcome:** Scripts pass, plan reads coherently, or blockers documented.

#### 5.3.6. Report

1. OUTPUT short chat delta per [RESPONSE.md](RESPONSE.md): edits, relocations, sizing mode and class, script findings, remaining blockers ([DECISIONS §18](DECISIONS.md#18-fidelity-gate)).

**Outcome:** Operator can build or re-invoke improve.

## 6. Validation

On failure, re-read §5, resolve, re-check.

### 6.1. Scripted validation

None bundled in this package. RUN external scripts documented in [VALIDATION.md](VALIDATION.md) (chunk, qualitative, structure — `--json` only; do NOT write report files). Confirm [WORKFLOW.yaml](WORKFLOW.yaml) still mirrors §5.3 when workflow steps changed.

### 6.2. Agent questions

Answer every [VALIDATION.md](VALIDATION.md) Agent question against the improved plan.

### 6.3. Interrogation agent

None by default.

**Pass when:** structure + qualitative scripts clear (or blockers reported); agent questions answered; fidelity gate passed.

## 7. Completion

OUTPUT chat per [RESPONSE.md](RESPONSE.md). Do NOT claim a pressure test unless done.
