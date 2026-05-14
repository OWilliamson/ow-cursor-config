# Documentation Audit Workflow

This is the canonical lifecycle workflow for the `docs-audit` skill.

## Phase 0: Intake And Constraints

- Confirm target documentation path.
- Determine whether source docs are local files, repository docs, generated docs, or mixed.
- Ask for or infer current product version evidence only when needed. If reliable current-version evidence is unavailable, treat that as an audit finding for Timeliness rather than silently skipping the check.
- Ask for a glossary, style guide, or canonical index if available.
- Identify output mode: write report file in Agent mode, or return report in chat in read-only modes.
- Record unavailable evidence as `Not Assessed` instead of guessing.
- Evaluate against the desired documentation standard, not only the current way the docs are organized. Read-only means do not edit the docs; it does not restrict suggested resolutions.

## Phase 1: Inventory And Structure Scan

Prefer `scripts/scan_docs.py` for mechanical evidence. If helper scripts are unavailable, use available read/search tools.

Validate:

- Recursively list files and directories.
- Identify Markdown files and other documentation assets.
- Review the full document inventory: relative path, directory, filename, stem, extension, detected naming style, naming signals, filename tokens, generic-word signals, and ambiguous-name signals.
- Detect dominant file naming convention, but do not rely on the dominant-style label alone. Judge whether the document names are predictable from the full inventory.
- Inspect the words in filenames. Green requires that filenames are not only syntactically consistent but also meaningful, specific, and distinguishable from nearby documents.
- Flag spaces, unusual characters, capitalization mismatches, inconsistent date stamps, and illogical sort order.
- Review per-directory sort-order hints for cases such as `version-2.md` sorting after `version-10.md`.
- Identify directories containing Markdown files.
- Check each such directory for `README.md`.
- Inspect README index tables for index number, document name, and short description.
- Cross-reference Markdown files against index entries.
- Detect stale index entries pointing to missing files.

This phase supports checks 1 and 2.

## Phase 2: Metadata And Freshness Review

Prefer `scripts/scan_docs.py` for front matter and freshness evidence. If helper scripts are unavailable, inspect front matter manually or with available read/search tools.

Validate:

- Parse YAML front matter when present.
- Check required fields: `title`, `description`, `version`, `audience`, `tags`, `created`, `last_updated`.
- Validate data types: version as quoted string, tags as array, dates as ISO 8601.
- Compare metadata title to first H1.
- Compute age from `last_updated`.
- Compare documented versions to current version only if reliable current-version evidence exists.
- If reliable current-version evidence cannot be found or provided, record a Timeliness issue because the audit cannot verify freshness against the current release.
- Flag unclear version semantics, such as minimum required versus last verified.

This phase supports checks 3 and 4.

## Phase 3: Markdown Structure And Agentic Legibility

Use `scripts/scan_docs.py` to identify hotspots before targeted reading. If helper scripts are unavailable, inspect representative and suspicious files directly.

Validate:

- Build style profile: admonition syntax, list markers, code fence language tags, heading casing, code block spacing.
- Compare style evidence across files: heading level sequences, H1 counts, list marker styles, admonition styles, code fence language tags, heading casing, section shape, and blank-line issues.
- Treat broad structural inconsistency across documents as a potential Document Style issue even if each individual file is parseable.
- Detect heading hierarchy skips, missing H1s, and headings used as styling.
- Identify multi-step instructions written as plain paragraphs.
- Detect hidden or interactive content: `details`, `summary`, tabs, collapsibles, JavaScript-dependent sections.
- Search for critical keywords inside hidden blocks: `required`, `warning`, `prerequisite`, `API key`, `breaking change`, `must`, `mandatory`.
- Measure whether critical information or first executable example appears only in the last 20 percent of a file.
- Detect image-only guidance, missing alt text, or screenshots without textual equivalents.
- Identify cross-reference phrases: "see section", "as mentioned above", "refer to", "as described earlier".
- Check whether cross-references include enough local context to be understood when chunked.
- Detect absolute internal URLs that should be relative.

This phase supports checks 5 through 8.

## Phase 4: Language And Information Quality Review

Use focused reading, not blind repeated full-corpus reading.

Validate:

- Compare terminology across files and against any glossary.
- Detect inconsistent aliases for core concepts.
- Check acronym expansion on first use.
- Compare code-level identifiers, endpoints, commands, and class names to textual references.
- Detect spelling variants and tone shifts.
- Review tense consistency in procedural sections.
- Identify long sentences, long paragraphs, unclear antecedents, ambiguity, jargon, and wall-of-text instructions.
- Identify redundant explanations, mixed unrelated topics, weak front-loading, and token-inefficient organization.

This phase supports checks 9 through 12.

## Phase 5: Content Completeness, Examples, And Links

Prefer `scripts/check_links.py` for internal links and `scripts/summarize_corpus.py` for compact extraction. If helper scripts are unavailable, inspect local links and examples with available tools.

Validate:

- Extract documented API endpoints, CLI commands, workflows, parameters, flags, and configuration fields.
- Review section-shape and workflow evidence for missing prerequisites, examples, troubleshooting, numbered steps, or executable guidance.
- Check whether each key workflow has numbered steps or executable examples.
- Check whether examples include necessary imports, configuration, syntax, placeholder labeling, OS assumptions, and deprecation warnings.
- Check parameter format and business-rule constraints near examples.
- Resolve internal links, anchors, and relative paths using local evidence.
- Do not run external network checks from helper scripts. If external link status is unavailable, report it as unavailable evidence or an issue according to the Referencing and Completeness criteria.
- Detect missing pages, placeholder pages, TODO-only content, circular references, and prerequisite gaps.

This phase supports checks 13 through 15.

## Phase 6: Global Consistency And Unified Truth

Prefer `scripts/summarize_corpus.py` to create compact review input. If helper scripts are unavailable, extract key facts through targeted reading.

Validate:

- Extract key facts: version numbers, default values, endpoint URLs, auth methods, config keys, environment variables, command names, feature names, and limits.
- Group facts by semantic key.
- Compare assertions across files.
- Flag conflicting details without canonical source.
- Check whether intentional duplication points to a canonical document.
- Verify canonical links still work.

This phase supports check 16.

## Phase 7: Report Generation

- Fill `REPORT_TEMPLATE.md` and write it to `docs/docs-report-YYYY-MM-DD.md`, or return the same structure in chat when writing is not appropriate.
- Use `YYYY-MM-DD` in the report title and filename.
- Use YAML front matter for metadata. Set `created` and `updated` to UTC timestamps in `YYYY-MM-DDTHH:MM:SSZ` format.
- Set `skill_version` to the version in `SKILL.md`.
- Include summary under 200 words.
- Frame the methodology around answering the 16 audit questions across the six rubric sections. Do not describe internal helper scripts, internal skill files, or implementation mechanics in the generated report.
- Include an Overview table for all 16 checks.
- Keep the Overview table compact: number, section, check, and state only.
- Include a `Summary:` line in every detailed finding section, including Green checks. A Green summary must cite what was inspected, not merely state that no issues were found.
- For every finding, include file path, evidence, severity, impact, and suggested resolution.
- Include further issues only if found.
- Include exactly three priority actions when at least three meaningful actions exist; otherwise include all meaningful actions and state that fewer than three were found.
- Keep suggestions practical and tied to the evidence.
- Do not mention internal skill implementation files or helper scripts such as `WORKFLOW.md`, `CHECKLIST.md`, `REPORT_TEMPLATE.md`, `EXAMPLES.md`, `scan_docs.py`, `check_links.py`, or `summarize_corpus.py` in the generated report.

## Phase 8: Post-Report Verification

- Re-read the scoring definitions.
- Check every Red, Amber, Green, and Not Assessed classification against the evidence.
- Green is not the easy path. Every Green state requires extra verification because the audit is asserting the check fully passes. The more Green states in the report, the more direct inspection and cross-checking must happen before delivery.
- For each Green state, do a second-pass review of the relevant question using direct document evidence. For corpus-wide checks, inspect more than one representative file and any suspicious outliers.
- If the report is mostly Green, perform a deeper verification pass across all six sections before finalizing. A highly Green report should take longer than a mixed or obviously problematic report because it must prove absence of issues, not just find visible ones.
- Check scoring distribution for suspicious patterns:
  - If most checks are Green, re-open representative files and verify that major expectations were not skipped or softened.
  - If most checks are Red, re-check severity thresholds and confirm the report is not double-counting the same issue across unrelated checks.
  - If several checks are Not Assessed, confirm each one has a specific missing-evidence reason and that the evidence could not reasonably be found locally.
- Treat every Green state as requiring verification before delivery. Re-check the question, inspect direct evidence, and ensure the summary explains why the check passes.
- Treat every Major issue as requiring verification before delivery. Re-check that the severity is justified, evidence is specific, and the suggested resolution addresses the root issue.
- Confirm all 16 checks were actually evaluated. Pay special attention to checks that helper scripts cannot fully judge: Terminology, Linguistic Consistency, Clarity And Concision, Information Density And Prioritization, Examples And Practical Guidance, and Unified Truth.
- Confirm the report is not over-relying on helper script output. There must be direct file reads or targeted content inspection for judgment-heavy findings and for every Green conclusion that depends on prose quality, examples, or cross-document consistency.
- Spot-check at least one file or evidence point for each Red check and each Green section. If the score depends on corpus-wide consistency, spot-check more than one file.
- Confirm examples in `EXAMPLES.md` shaped the finding style only; they must not limit the kinds of issues reported.
- Confirm the report does not cite helper scripts, internal skill files, or script-derived filenames as the source of truth. Evidence should be documentation paths, observed document content, or explicitly missing evidence.
- Confirm every cited file or link exists in the scanned corpus unless the finding is a missing file or broken link.
- Confirm no facts were invented, especially current version, glossary expectations, release timing, or external link status.
- Confirm the report distinguishes issues from forward-looking improvements.
- Confirm the report does not recommend changes that contradict the documented audience or repo conventions.
- Confirm the report did not include this post-report verification checklist.
- If this verification finds report problems, fix the report before delivery instead of documenting the verification failure in the report.
