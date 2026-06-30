# Convert UI rules — hub paths and emit rules

Authoritative docs and templates live in the **ow-cursor-config** repository that contains `skills/cursor-convert-ui-rules/` (adjust if the hub moves).

## Hub paths (from repository root)

| What | Path |
|------|------|
| Migration template | `templates/user-rules-migration.md` |
| Tooling map | `docs/user-tooling-map.md` |
| User sync | `docs/user-cursor-sync.md` |
| Global rules in hub (when present) | `ow-cursor-config/rules/` |
| Packaged rules bundle | `ow-cursor-config/rules/` |

Read the migration template when generating frontmatter and post-steps.

## Frontmatter and body (per block)

For **each** block, emit one `.mdc` file that matches the migration template.

1. Opening YAML frontmatter between `---` lines.
2. Fields:
   - **`description`:** Short, accurate summary of that block’s intent. When the source was Settings UI, include wording like `Migrated from Settings → User Rules (YYYY-MM-DD)`.
   - **`alwaysApply: true`** unless the user asked for path-scoped rules; then `alwaysApply: false` and **`globs:`** as appropriate (see Cursor rule docs or existing `.mdc` under the live rules directory for that machine).
3. **Body:** the block’s markdown **after** the closing frontmatter `---` (no duplicate frontmatter inside the body).

## Where to write files

Prefer, in order, unless the user specifies otherwise:

1. **`ow-cursor-config/rules/`** under the hub clone above, if that directory exists or the user is adding new hub globals.
2. **`ow-cursor-config/rules/`** under the same clone for the packaged bundle.
3. **Live profile rules directory** when the user only wants the live profile updated (still remind them to keep git canonical if they use the hub).

If both hub targets are plausible and the user did not say which, **ask once** before writing.

## Filenames

Derive **kebab-case** `.mdc` names from each block:

1. Prefer the first markdown heading (`# …`) or obvious title line; lowercase; replace runs of non-alphanumeric characters with `-`; collapse repeated `-`; trim length sensibly (about 60 chars max before `.mdc`).
2. If there is no title: `migrated-ui-rule-01.mdc`, `migrated-ui-rule-02.mdc`, … in **paste order**.
3. On collision with an existing file, append `-2`, `-3`, … or stop and ask.

## After writing (tell the user)

1. Smoke-check behavior in a fresh chat if needed.
2. When the text came from **Settings → User Rules**, they must **clear that Settings field** after the `.mdc` files are in place so instructions are not duplicated. Follow the migration template and tooling map paths in the table above.
3. Install or sync into the live rules directory per the user-cursor-sync doc path above when hub and profile should stay aligned.

## Block separators

Split the paste into blocks on **delimiter lines** that contain **only** one repeated bar character, **length 5 or more**:

| Character | Example delimiter line |
|-----------|------------------------|
| `-` | `----------` |
| `=` | `==========` |
| `_` | `__________` |

- **One block:** if there is no matching delimiter line, the entire paste is one rule file.
- **Trim** leading and trailing blank lines on each block after splitting.
- **Do not** use a bare `---` line (three characters) as a block delimiter: it clashes with YAML frontmatter and Markdown horizontal rules. If the user used only `---`, ask them to re-paste with `-----` or longer separators, or split manually with explicit filenames.

## Agent checklist

- [ ] Split only on full-line bar delimiters (`-----`, `=====`, `_____`, or longer).
- [ ] One `.mdc` per block; frontmatter + body per hub migration template.
- [ ] Names derived or taken from the user; collisions handled.
- [ ] User reminded to clear Settings when applicable and to sync hub ↔ profile as usual.
