# Public documentation links

Class **C** sources only. Used by `@customer-explanation` during workflow step 2 and self-check.

## Allowed hosts

- `https://docs.itrsgroup.com/docs/...`

## Forbidden link targets

- Confluence, Jira, Slack, GitHub (any visibility)
- `knowledge.opsview.com`, `opsview.com` doc mirrors
- Internal wikis, ticket trackers, repo browsers

## When to link

- Link where public documentation supports the answer (procedure, configuration, supported behaviour).
- Prefer linking over paraphrasing long steps the docs already cover well.
- If no suitable public page exists, omit links — do not invent URLs.

## Version URLs

- **Default:** use `/current/` in the doc path.
- **Pinned version** (e.g. `6.2.0`, `2.11.0`) only when the user or thread names a specific product or doc version.
- Rewrite pinned URLs to `current` before output unless a version was specified.

Examples:

| Before | After (no version in thread) |
|--------|------------------------------|
| `.../opentelemetry/6.2.0/...` | `.../opentelemetry/current/...` |
| `.../infrastructure-agent/2.11.0/...` | `.../infrastructure-agent/current/...` |
| `.../docs/opsview/current/...` | unchanged |

## Section anchors

- Link to the **most specific section**, not the page top alone.
- Append `#fragment` when the section has a stable anchor.

Good:

`https://docs.itrsgroup.com/docs/geneos/collection/opentelemetry/current/user-guide/opentelemetry/index.html#mappings`

Avoid when a section exists:

`.../opentelemetry/index.html` (no fragment)

**Discover anchors:**

1. Open the public page (fetch or browser).
2. Use the heading fragment — typically lowercase, hyphenated (`#mappings`, `#installation`, `#supported-versions`).
3. Verify the URL resolves to the correct section.

If the exact anchor is uncertain, link the page without a fragment rather than guess.

## Deduplication

- Track pages by **path without fragment** (e.g. `.../opentelemetry/index.html`).
- Each distinct page is linked **at most once** in the customer text.
- **First mention** carries the link (use the best section anchor at that point).
- Later mentions: plain text only — no repeat link, no "see above".
- Multiple relevant sections on one page: one link to the **most relevant** section.

## Link formatting (mandatory)

- Use markdown links: `[OpenTelemetry mappings](https://docs.itrsgroup.com/...)`
- **Never** wrap URLs in backticks.
- **Never** put links inside fenced code blocks or inline code.
- Full `https://` URLs are acceptable when not using link text.

## Placement by mode

| Mode | Pattern |
|------|---------|
| Answer | One inline link at first mention, or one reference at the end |
| Capability | Link feature overview or main section once |
| How-to | Link procedure section once (step 1 or after steps) — not every step |

## Product entry points

Search from these roots; paths vary by topic.

| Product | Base URL |
|---------|----------|
| Opsview | `https://docs.itrsgroup.com/docs/opsview/current/` |
| Geneos | `https://docs.itrsgroup.com/docs/geneos/` (use `current` mid-path for versioned collections) |
| Infrastructure Agent | `https://docs.itrsgroup.com/docs/infrastructure-agent/current/` |
| OP5 Monitor | `https://docs.itrsgroup.com/docs/op5-monitor/` |

## Doc drift

If internal facts and public docs disagree on **supported customer behaviour**, the customer text follows **verified public docs**. Flag the mismatch to the user separately — not in the customer draft.

## Self-check (documentation)

- [ ] Links are `docs.itrsgroup.com` only
- [ ] `/current/` unless a version was specified in the thread
- [ ] Section anchors where possible and verified
- [ ] No duplicate page links (path without fragment)
- [ ] Markdown links only — not backticks or code blocks
