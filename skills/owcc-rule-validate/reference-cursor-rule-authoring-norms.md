# Cursor rule authoring norms

Aligned with Cursor rule guidance (see project `create-rule` skill) and lean-rule practice; last synced 2026-07-07.

These norms are the canonical master for `owcc-rule-validate`, and copied byte-identically into `owcc-rule-improve`.

## Principles

- Verifiable checks (binary pass/fail) are preferred over advisory notes.
- Mechanical checks confirm structure; behavioural effectiveness requires a pressure test with representative files open and a fresh session.
- Keep the `.mdc` body scannable; deeper reference in a sibling file only one hop away when necessary.
- Maintain one term per concept throughout; avoid synonym drift.
- Do not let the frontmatter `description` replace reading the body for long workflows; descriptions should say when the rule applies.

## Norm IDs

| Norm ID | Check | Severity default |
|---------|-------|------------------|
| `CR-FILE-SUFFIX` | file extension is `.mdc` | Critical |
| `CR-FRONTMATTER` | YAML frontmatter present and parseable | Critical |
| `CR-DESC-NONEMPTY` | `description` is non-empty | Critical |
| `CR-DESC-WHEN` | `description` states what the rule enforces and when it applies; not first-person | Suggestion |
| `CR-DESC-WORKFLOW-SUMMARY` | `description` does not substitute for the full procedural body | Critical |
| `CR-DESC-BODY-ALIGN` | `description` claims match what the body actually instructs | Critical |
| `CR-SCOPE-EXCLUSIVE` | `alwaysApply: true` is not combined with contradictory “only when editing X” body text without explicit bridging | Suggestion |
| `CR-GLOBS-WHEN-NEEDED` | when `alwaysApply` is false, `globs` (or equivalent scoping) is set for file-specific rules | Suggestion |
| `CR-LINES-BUDGET` | body (excluding frontmatter) roughly within the “under ~50 lines” budget for a single concern; split if not | Suggestion |
| `CR-ONE-CONCERN` | one primary concern per `.mdc`; multiple unrelated concerns → split | Suggestion |
| `CR-LINKS-ONE-HOP` | links from the rule resolve within repo; no file→file→file chains | Suggestion |
| `CR-RULE-NO-ORPHANS` | non-generated siblings in the rules area are linked from the rule or explicitly marked deprecated | Suggestion |
| `CR-RULE-REFS-EXIST` | every path the rule links to exists | Critical |
| `CR-RULE-SIBLINGS-LEAN` | paired reference files are single-purpose and avoid unused bulk | Suggestion |
| `CR-ANTI-WIN-PATHS` | no Windows-style backslash paths in docs | Suggestion |
| `CR-TERMINOLOGY` | one term per concept throughout | Suggestion |
| `CR-NO-TIME-BOMBS` | no time-sensitive phrases unless in a dated legacy section | Suggestion |
| `CR-NO-DUP-AGENTS` | no large copy-paste overlap with `AGENTS.md` or other rules without a single canonical home | Suggestion |
| `CR-DEAD-RULE` | rule is not `alwaysApply: false` with no `globs` and no meaningful one-line `description` (would never fire automatically) | Critical |
| `CR-GLOB-PRECISION` | glob matches intended paths and a stated non-matching sample path confirms it does not over-fire | Suggestion |
| `CR-DESC-PICKER` | `description` is readable as a human-facing rule-picker label: states enforcement effect in one line, avoids internal jargon | Suggestion |
| `CR-DESC-SINGLE-LINE` | `description` is one physical line in the file (no YAML block scalars `>-`, `|`, or folded/multiline values); Cursor Settings and intelligent apply may misread them as the literal `>-` | Critical |
| `CR-ALWAYS-ON-BUDGET` | cumulative line count of all `alwaysApply: true` rules in the same `.cursor/rules/` directory is not disproportionately large; heaviest rules are flagged | Suggestion |
| `CR-INTER-RULE-CONFLICT` | no semantic contradiction or unintended duplication with simultaneously active rules (same always-on set or overlapping globs) | Suggestion |
| `CR-SCOPE-LAYER` | when both a user-scope (`~/.cursor/rules/`) and project-scope (`.cursor/rules/`) rule address the same topic, they do not contradict; canonical home is explicit | Suggestion |
| `CR-BOUNDARIES-EXPLICIT` | rule states what it does **not** override or require (no commit, no push, read-only external systems, etc.) when scope could be misread | Suggestion |
| `CR-AUTO-CLARITY` | rules that enforce terse communication or a fixed output format include when to break out (security, irreversible ops, ambiguity) | Suggestion |
| `CR-NO-FAKE-ABBREV` | prose does not invent shorthands expecting token savings; compress structure instead | Nice to have |

## Frontmatter guidance

- `description`: third person; what the rule enforces and when it applies (activation hint). Also a **human-facing label** in the Cursor rule picker — must communicate the enforcement effect clearly as a one-liner, without internal jargon. **One physical line only** — do not use YAML folded/block scalars (`>-`, `|`, multiline indentation). Quote the whole string on one line if punctuation requires it.
- `alwaysApply: true`: use sparingly for universal, short constraints; contributes to the cumulative always-on token budget every turn.
- `alwaysApply: false` with `globs`: file-scoped rules.
- `alwaysApply: false` with no `globs` but a one-line `description`: apply intelligently in Cursor (agent uses `description` as the trigger).
- `alwaysApply: false` with no `globs` and empty or missing `description`: dead rule — only fires on manual `@` mention. Either add `globs`, add a one-line `description`, or set `alwaysApply: true`.
- Avoid redundant fields that confuse activation (for example both “always” language in the body and narrow `globs` without explanation).

## Structure guidance

- Open with scope: when this rule is in play.
- **Boundaries:** when the rule could imply side effects, state what it does not authorize.
- **Auto-Clarity:** for style or format rules, state when normal prose or full detail overrides the rule briefly.
- Follow with must / must-not, then ordered checks or steps.
- Checklist rows should be actions or verifications, not essays.
- Prefer examples that show the correct pattern, not only anti-patterns.

## Validation checks

- Run `wc -l` on the `.mdc` and eyeball frontmatter vs body split.
- Parse frontmatter; confirm `description` length is reasonable for the rule picker (human-readable one-liner).
- Reject folded or block `description` values (`description: >-`, `description: |`, or continuation lines under `description:`) — flag `CR-DESC-SINGLE-LINE`.
- Check for dead rule: `alwaysApply: false` with no `globs` and no meaningful one-line `description` — flag `CR-DEAD-RULE`.
- Test glob precision: state one sample path that should match and one that should not; confirm both; flag `CR-GLOB-PRECISION` if over-broad.
- List all `alwaysApply: true` rules in the same `.cursor/rules/` directory; sum line counts; flag `CR-ALWAYS-ON-BUDGET` if combined total is disproportionate. For token-level precision, use `npx cursor-doctor budget` (reports actual token cost per rule rather than line count).
- List all rules simultaneously active with the target; check for semantic overlap or contradiction; flag `CR-INTER-RULE-CONFLICT`.
- Check `~/.cursor/rules/` if accessible for a user-scope rule on the same topic; flag `CR-SCOPE-LAYER` if both are active and contradict.
- Resolve every markdown link path from the rule.
- If siblings exist, inventory them and verify each is cited or explicitly deprecated.
- For style or format rules, verify **Auto-Clarity** and **Boundaries** (`CR-AUTO-CLARITY`, `CR-BOUNDARIES-EXPLICIT`).
- Scan prose for invented abbreviations (`CR-NO-FAKE-ABBREV`).

## Reporting rules

- Give every finding a severity label: Critical, Suggestion, or Nice to have.
- Mark mechanically unconfirmed findings as speculative and state the confirming evidence needed.
- Acknowledge passes explicitly; do not omit checks silently.
- Keep detailed findings capped; if there are more, list remaining norm IDs only.
- End with a final sanity pass: only flag items that are actually worth fixing.
