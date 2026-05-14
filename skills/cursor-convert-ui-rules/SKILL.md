---
name: cursor-convert-ui-rules
description: >-
  Splits pasted Cursor Settings "User Rules" text (blocks separated by horizontal bar
  lines) into separate `.mdc` rule files with YAML frontmatter aligned to the
  ow-cursor-config migration template. Use when the user manually invokes
  cursor-convert-ui-rules after pasting UI rules, multiple rules in one paste, or when
  migrating Settings-only prose into file-backed rules.
disable-model-invocation: true
---

# Convert UI rules to rule files

## Invocation

**Manual only:** load this skill by **name** (`cursor-convert-ui-rules`) or **`@cursor-convert-ui-rules`**. Do **not** infer this workflow from ambient chat alone.

Hub-relative paths, migration template, where to write files, naming, post-steps, block separators, and checklist: **[reference-hub.md](reference-hub.md)**.

## Required inputs

1. **Pasted text** (typically from **Cursor → Settings → Rules → User Rules**) to split into files.
2. **Optional:** destination directory.
3. **Optional:** `YYYY-MM-DD` for migration wording in `description` (default: today's date from context).
4. **Optional:** explicit `.mdc` base names, one per block in order; use when auto-naming would be wrong.

## Definition of done

- One `.mdc` file emitted per block, each with correct frontmatter per the migration template.
- User reminded to clear the Settings UI field (if applicable) and to sync hub ↔ profile.

## Non-goals

- Do not invent rule content; convert only what the user pasted.
- Do not guess destination if ambiguous; ask once.
- Do not treat `---` (three chars) as a block separator.

## Workflow

1. Read [reference-hub.md](reference-hub.md) (migration template path, hub table, block separators, emit rules).
2. Split the paste per block separator rules in `reference-hub.md`.
3. Emit one `.mdc` per block per `reference-hub.md`.
4. Confirm destination with the user if ambiguous; finish with the post-write reminders in `reference-hub.md`.
