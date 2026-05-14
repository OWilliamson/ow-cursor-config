# Documentation Audit Examples

Use these examples to shape finding style in the `docs-audit` skill. They are illustrative, not exhaustive; flag evidence-backed issues even when they do not exactly match an example.

## Example Major Finding

Check: Agentic Legibility: Critical Information Visibility

State contribution: Major

File: `docs/setup.md`

Evidence: The required API token is documented only inside a `<details>` block.

Impact: An AI agent chunking raw Markdown may skip or underweight the mandatory prerequisite.

Suggested resolution: Move the token requirement into a visible `Prerequisites` section near the start of the document, and leave the collapsible block only for optional explanation.

## Example Minor Finding

Check: Metadata

State contribution: Minor

File: `docs/api/users.md`

Evidence: Front matter includes `title`, `version`, and `last_updated`, but no `tags`.

Impact: Search and automated routing are less precise, but the document remains understandable.

Suggested resolution: Add targeted tags such as `api`, `users`, and `authentication`.

## Example Other Issue

Check: Referencing

File: `docs/setup.md`

Evidence: The page links to an absolute GitHub URL for another file in the same docs tree.

Impact: The link may break on forks, branches, or local clones.

Suggested resolution: Replace it with a relative link.
