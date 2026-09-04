# Validation rubric

Completion checks for `/owcc-rule-improve`. On failure, RETURN TO SKILL.md §5, resolve, THEN re-run this rubric against the **target** `.mdc`.

Canonical CR-* norms for rule authoring live here. `owcc-rule-validate` should consume this file as a read-only wrapper (same pattern as skill validate→improve). Until that rewrite, keep any vendored copy IN sync manually.

## Scripted validation

None. (This package has no `scripts/`. Mechanical checks below are agent-run commands.)

### Mechanical commands (agent-run)

- `wc -l` on the target `.mdc` — eyeball frontmatter vs body; flag `CR-LINES-BUDGET` IF body (excluding frontmatter) IS far over ~50 lines for one concern.
- Parse frontmatter (YAML); confirm `description` IS one physical line (no `>-`, `|`, or indented continuations) — `CR-DESC-SINGLE-LINE`.
- Confirm `description` non-empty — `CR-DESC-NONEMPTY`.
- Dead rule: `alwaysApply: false` with no `globs` and no meaningful one-line `description` — `CR-DEAD-RULE`.
- Glob precision: state one matching path AND one non-matching path; confirm — `CR-GLOB-PRECISION`.
- List all `alwaysApply: true` rules IN the same `.cursor/rules/` directory; sum line counts; optional `npx cursor-doctor budget` — `CR-ALWAYS-ON-BUDGET`.
- List simultaneously active peers; check overlap/contradiction — `CR-INTER-RULE-CONFLICT`.
- IF accessible, check `~/.cursor/rules/` for same-topic user-scope rule — `CR-SCOPE-LAYER`.
- Resolve every markdown link path from the rule — `CR-RULE-REFS-EXIST`.
- Confirm file suffix IS `.mdc` — `CR-FILE-SUFFIX`.

## Agent questions

- [ ] Target path unambiguous; no unauthorized rename of the `.mdc`?
- [ ] Frontmatter parseable; `description` one physical line; activation mode live (not dead)?
- [ ] Body matches [OUTPUTS.md](OUTPUTS.md) spine (when / must / must-not / checks as applicable)?
- [ ] Glob samples stated (or always-on / intelligent-apply noted)?
- [ ] Always-on budget and inter-rule conflicts reviewed?
- [ ] Linked siblings exist, cited, and lean (or explicitly deprecated)?
- [ ] No substance dropped without user-approved drop ([DECISIONS §8](DECISIONS.md#8-fidelity-disposition))?
- [ ] Description IS trigger-only (no workflow summary) AND aligns with body?
- [ ] Chat OUTPUT ready per [RESPONSE.md](RESPONSE.md)?
- [ ] CR-* norms below applied; Critical findings cleared or blocked explicitly?

## Interrogation agent

None by default. IF operator requests a subagent audit, THEN scope it to: frontmatter/activation, Critical CR-*, AND fidelity gate only — still mutation stays IN the main improve workflow.

## Authoring norms (CR-*)

Principles:

- Verifiable checks (binary pass/fail) preferred over advisory notes.
- Mechanical checks confirm structure; behavioural effectiveness requires a pressure test with representative files open AND a fresh session.
- Keep the `.mdc` body scannable; deeper reference IN a sibling file only one hop away when necessary.
- One term per concept; avoid synonym drift.
- Frontmatter `description` says when the rule applies — NOT a substitute for the body.

| Norm ID | Check | Severity default |
|---------|-------|------------------|
| `CR-FILE-SUFFIX` | file extension IS `.mdc` | Critical |
| `CR-FRONTMATTER` | YAML frontmatter present and parseable | Critical |
| `CR-DESC-NONEMPTY` | `description` IS non-empty | Critical |
| `CR-DESC-WHEN` | `description` states what the rule enforces and when it applies; not first-person | Suggestion |
| `CR-DESC-WORKFLOW-SUMMARY` | `description` does not substitute for the full procedural body | Critical |
| `CR-DESC-BODY-ALIGN` | `description` claims match what the body actually instructs | Critical |
| `CR-SCOPE-EXCLUSIVE` | `alwaysApply: true` IS not combined with contradictory “only when editing X” body text without explicit bridging | Suggestion |
| `CR-GLOBS-WHEN-NEEDED` | when `alwaysApply` IS false, `globs` (or equivalent scoping) IS set for file-specific rules | Suggestion |
| `CR-LINES-BUDGET` | body (excluding frontmatter) roughly within the “under ~50 lines” budget for a single concern; split IF not | Suggestion |
| `CR-ONE-CONCERN` | one primary concern per `.mdc`; multiple unrelated concerns → split | Suggestion |
| `CR-LINKS-ONE-HOP` | links from the rule resolve within repo; no file→file→file chains | Suggestion |
| `CR-RULE-NO-ORPHANS` | non-generated siblings IN the rules area are linked from the rule or explicitly marked deprecated | Suggestion |
| `CR-RULE-REFS-EXIST` | every path the rule links to exists | Critical |
| `CR-RULE-SIBLINGS-LEAN` | paired reference files are single-purpose and avoid unused bulk | Suggestion |
| `CR-ANTI-WIN-PATHS` | no Windows-style backslash paths IN docs | Suggestion |
| `CR-TERMINOLOGY` | one term per concept throughout | Suggestion |
| `CR-NO-TIME-BOMBS` | no time-sensitive phrases unless IN a dated legacy section | Suggestion |
| `CR-NO-DUP-AGENTS` | no large copy-paste overlap with `AGENTS.md` or other rules without a single canonical home | Suggestion |
| `CR-DEAD-RULE` | rule IS not `alwaysApply: false` with no `globs` and no meaningful one-line `description` | Critical |
| `CR-GLOB-PRECISION` | glob matches intended paths and a stated non-matching sample path confirms it does not over-fire | Suggestion |
| `CR-DESC-PICKER` | `description` IS readable as a human-facing rule-picker label | Suggestion |
| `CR-DESC-SINGLE-LINE` | `description` IS one physical line (no YAML block scalars `>-`, `|`, or folded/multiline values) | Critical |
| `CR-ALWAYS-ON-BUDGET` | cumulative line count of all `alwaysApply: true` rules IN the same `.cursor/rules/` directory IS not disproportionately large | Suggestion |
| `CR-INTER-RULE-CONFLICT` | no semantic contradiction or unintended duplication with simultaneously active rules | Suggestion |
| `CR-SCOPE-LAYER` | user-scope and project-scope rules on the same topic do not contradict; canonical home IS explicit | Suggestion |
| `CR-BOUNDARIES-EXPLICIT` | rule states what it does **not** override or require when scope could be misread | Suggestion |
| `CR-AUTO-CLARITY` | terse/format rules include when to break out (security, irreversible ops, ambiguity) | Suggestion |
| `CR-NO-FAKE-ABBREV` | prose does not invent shorthands expecting token savings; compress structure instead | Nice to have |

### Frontmatter guidance

- `description`: third person; what the rule enforces and when; **one physical line only**; quote IF punctuation requires it.
- `alwaysApply: true`: sparingly for universal short constraints.
- `alwaysApply: false` + `globs`: file-scoped.
- `alwaysApply: false` + no `globs` + one-line `description`: intelligent apply.
- `alwaysApply: false` + no `globs` + empty/missing `description`: dead rule.

### Structure guidance

- Open with scope; add Boundaries / Auto-Clarity when needed.
- Must / must-not, THEN ordered checks.
- Prefer correct-pattern examples over anti-patterns only.

### Reporting rules

- Severity: Critical, Suggestion, or Nice to have.
- Mark unconfirmed findings speculative.
- Acknowledge passes; do not omit checks silently.
- Cap detailed findings; list remaining norm IDs IF many.
- Final sanity: only flag items worth fixing.
