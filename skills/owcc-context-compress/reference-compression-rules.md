# Context compression rules

Apply to prose **outside** preserved regions. When unsure, leave unchanged.

## Preserve exactly (never modify)

- Fenced code blocks (``` … ```) and indented code blocks
- Inline code (`backtick content`)
- URLs and markdown links (full href and link text if technical)
- File paths (`src/...`, `./config.yaml`, `.cursor/...`)
- Shell commands (`git commit`, `npm install`, `./scripts/deploy.sh`)
- API names, library names, norm IDs (`CS-*`, `CR-*`), issue keys
- YAML frontmatter **keys** and enum-like values (`alwaysApply`, `globs`, skill `name`)
- Tables: compress cell prose only if meaning stays unambiguous; keep column headers

## Remove from prose

- Articles where safe (`a`, `an`, `the`)
- Filler: just, really, basically, actually, simply, essentially
- Pleasantries: sure, certainly, of course, happy to, I'd recommend
- Hedging: it might be worth, you could consider, it would be good to
- Redundant phrasing: "in order to" → "to"; "make sure to" → imperative
- Connective fluff when list order carries meaning: however, furthermore, additionally

## Compress

- Short synonyms: "fix" not "implement a solution for"; "use" not "utilize"
- Imperatives: drop "you should", "remember to" — state the action
- Merge duplicate bullets that repeat the same constraint
- One example where several show the same pattern

## Do not use fake abbreviations

Do not invent `cfg`, `impl`, `req`, `auth` in prose expecting token savings — tokenizers often split them like full words. Compress **structure** (fewer bullets, shorter sentences) instead.

## File-type notes

### `AGENTS.md`

- Keep table of doc links intact (paths are preserved regions).
- Tighten narrative paragraphs; do not remove policy constraints.

### `.mdc` rules

- Never fold or multiline the frontmatter `description` (see `CR-DESC-SINGLE-LINE`).
- Keep must / must-not lists; shorten wording per bullet.
- After compression, run `/owcc-rule-validate`.

### `SKILL.md`

- Do not move workflow steps into `description` (see `CS-DESC-WORKFLOW-SUMMARY`).
- After compression, run `/owcc-skill-validate`.

## Backup convention

Original: `AGENTS.md` → backup `AGENTS.original.md`

Rule: `foo.mdc` → `foo.original.mdc`

Skip creating backup if `<name>.original<ext>` already exists — ask user before overwrite.
