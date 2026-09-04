---
name: owcc-context-compress
description: >-
  Compresses natural-language always-on context files (AGENTS.md, alwaysApply rules,
  long skill descriptions) to reduce input tokens while preserving code blocks, paths,
  URLs, and commands exactly. Backs up originals before overwrite. Use when trimming
  profile token budget, compressing AGENTS.md, shrinking always-on rules, or when the
  user invokes /owcc-context-compress with a file path.
disable-model-invocation: true
---

# Compress always-on context

Explicit-only. Invoke with `/owcc-context-compress`.

## When to use

- An **always-loaded** file is verbose (root `AGENTS.md`, `alwaysApply: true` rules, long README the agent reads every turn).
- User wants **input token** reduction without breaking code, links, or activation semantics.
- After `/owcc-rule-improve` or `/owcc-skill-improve`, a file is structurally correct but still wordy.

## Required inputs

- **Target path(s)**: absolute or repo-relative paths to compress.
- **Approval** (implicit): user invoked the skill or named the file in the same turn.

## Definition of done

- Each target has a backup at `<path>.original` (same directory, basename + `.original` before extension).
- Prose is compressed per [reference-compression-rules.md](reference-compression-rules.md).
- Code fences, inline code, URLs, paths, commands, frontmatter keys, and norm IDs are **unchanged**.
- User is told backup paths and suggested follow-up: `/owcc-rule-validate` or `/owcc-skill-validate` as appropriate.

## Non-goals

- Do not compress `.py`, `.js`, `.ts`, `.json`, `.yaml`, `.sh`, or other executable/config sources.
- Do not change `description` trigger semantics in ways that fail validate norms.
- Do not delete requirements — relocate or tighten wording instead.

## Boundaries

- Local file edit only — no commit, push, reconcile, or publish unless the user asks separately.
- Does not run `npx cursor-doctor budget`; suggest it after edits for token verification.

## Workflow

1. Confirm each target is natural-language (`.md`, `.mdc`, `.txt`) or mixed prose+code markdown.
2. For each file: copy to `<name>.original<ext>` if backup does not already exist.
3. Compress prose only — rules in [reference-compression-rules.md](reference-compression-rules.md).
4. Re-read compressed file; verify preserved regions byte-match the original.
5. Report: paths changed, backup locations, approximate line reduction (`wc -l` before/after).
6. Recommend validate pass on rules/skills edited.

## Auto-Clarity

Do **not** compress these into fragments when it would change meaning:

- Security warnings and irreversible-action instructions.
- Ordered steps where dropping conjunctions changes execution order.
- `description` frontmatter — tighten wording but keep trigger clarity (`CS-DESC-WHEN`, `CR-DESC-WHEN`).

## Honest expectations

Output-token skills save per reply; **input** compression saves every turn the file loads. Net session savings depend on file size and session length — smaller wins on short chats.

## Additional resources

- [reference-compression-rules.md](reference-compression-rules.md) — preserve vs compress rules
