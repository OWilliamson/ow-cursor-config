# Documentation Audit Rubric

This is the canonical 16-check rubric for the `docs-audit` skill.

## Scoring Model

Red: one or more major issues, or three or more minor issues.

Amber: one or two minor issues and no major issues.

Green: no issues.

Not Assessed: the check cannot be completed from available local evidence. State what evidence was missing and do not infer the result.

## Applicability Rules

- Apply the rubric to documentation whose primary audience is AI agents or humans assisted by AI agents.
- README files, changelogs, generated docs, archive directories, templates, and short index-only files may have different expectations. State any applicability decision in the report.
- If a project intentionally does not use metadata, index tables, or front matter, report the impact rather than inventing a toolchain requirement.
- Evaluate against what the documentation should provide for an AI-agent-oriented audience. Do not suppress an issue because the resolution would require changing the docs' structure, metadata policy, indexing, or maintenance workflow.
- Do not assume current software version, release history, external link status, or canonical glossary content unless evidence is available.
- For Timeliness, missing reliable current-version evidence is itself a major issue because the audit cannot verify whether the documentation is fresh against the current release.
- Examples in this rubric are illustrative. Do not require an exact match to an example before flagging an issue.

## Section A: Directory And File Structure

### Check 1: Document Naming

Question: Is there a consistent, predictable naming convention for documents and files, and do the words in each filename clearly indicate the document's purpose?

Minor issue: A single file deviates slightly from the convention, or one filename is slightly generic but still understandable from nearby context.

Example: `UserGuide.md` when all other files are `lowercase-with-hyphens.md`.

Major issue: No discernible naming convention exists; multiple files have names that collide or are misleading; names are ambiguous to the point an AI cannot guess the content; filenames use generic words that do not distinguish purpose, such as `overview.md`, `guide.md`, or `notes.md` across multiple directories without clarifying context.

Example: Some files are `Topic_Name.md`, others are `topicname.md`, others are `topic-name.md` with no pattern.

Other things to look out for: inconsistent use of date stamps in file names; spaces, special characters, or capitalization that breaks cross-platform compatibility; naming that does not sort logically, such as `version-2.md` then `version-10.md`; filenames whose tokens are too broad to predict content; near-duplicate stems that differ only by vague words.

### Check 2: Directory-Level Indexing

Question: Does every directory contain an up-to-date `README.md` that includes a table indexing the documents in that directory, with at minimum an index number, document name, and short description?

Minor issue: The index table exists but is missing one or two recently added files, or has an incorrect description that does not hinder understanding.

Example: `migration-guide.md` was added recently but is not listed in the table.

Major issue: No `README.md` present; the index table is entirely absent; the table lists files that no longer exist.

Example: The index still lists `old-api.md`, which was deleted.

Other things to look out for: README only contains an index and nothing else useful; descriptions so terse they are useless, such as "Various docs"; table format is not machine-parseable.

## Section B: Metadata And Freshness

### Check 3: Metadata

Question: Does every document carry structured metadata, such as YAML front matter, that identifies its purpose, audience, software version, and tags?

Minor issue: Metadata exists but is missing non-critical fields like description or tags where helpful; a `last_updated` date is off by a few days.

Example: Front matter contains title and version but lacks tags and description.

Major issue: No metadata block at all when the toolchain supports it; version field is completely wrong; audience field missing or misleading.

Example: Front matter says `version: 8.0.0` but the content only describes features available up to `7.2.0`.

Other things to look out for: metadata is valid YAML or JSON but not machine-readable due to incorrect data types, such as `version: 7` instead of `version: "7.0.0"`; tags are too broad to be useful; metadata title and first heading disagree.

### Check 4: Timeliness

Question: Does each document carry a creation date, a last-updated date, and a clear indication of which software versions it covers?

Minor issue: Dates exist but are in a non-standard format, such as "yesterday" instead of `YYYY-MM-DD`; a document covers a point release older than current but no flag is raised.

Major issue: Missing creation or update date entirely; last updated more than one year ago; last updated before the last major release; last updated before the last minor release when current version evidence is available.

Example: A document with `last_updated: 2025-03-01` when today is `2026-05-01` triggers a major freshness warning.

Major issue: No reliable current software version evidence can be found or provided for a docs set where version freshness is required.

Other things to look out for: a version field does not specify whether it means minimum required version or last verified version; a recently updated document omits relevant latest-release breaking changes.

## Section C: Structure And Agentic Legibility

### Check 5: Document Style

Question: Is the formatting and visual style uniform?

Minor issue: A single code block uses a different language tag than peers, such as `sh` instead of `bash`; one list uses `-` while another uses `*` but the rendered result is identical.

Major issue: Warning, note, and tip blocks are formatted completely differently across documents, making an AI's pattern matcher fail to recognize them; critical structural elements are indicated inconsistently; documents use substantially different section shapes, heading casing, list styles, or code block conventions without a clear reason.

Example: Some docs use `!!! warning "Important"` while others use `> **Warning**` for the same severity.

Other things to look out for: inconsistent monospace for UI elements or commands; missing blank lines around lists or code blocks; heading casing varies wildly; some documents use highly structured task sections while others use free-form prose for equivalent material.

### Check 6: Agentic Legibility: Heading And Structure

Question: Is the document organized with a strict, predictable heading hierarchy that an AI agent can reliably parse?

Minor issue: A minor heading skip that does not obscure overall structure, such as a short section moving from H2 to H4.

Example: `## Installation` followed directly by `#### Prerequisites`, but the section is only two paragraphs.

Major issue: No headings at all; significant heading skip, especially H1 to H3; multi-step instructions written as plain paragraphs with no numbered list to signal sequence.

Example: A document with an H1 title then immediately H3 subsections.

Other things to look out for: headings used for styling rather than structure; bold text used instead of real headings; inconsistent heading casing makes equivalent levels harder to recognize.

### Check 7: Agentic Legibility: Critical Information Visibility

Question: Are warnings, prerequisites, and mandatory steps presented in a way that an AI agent will reliably find them, without relying on interactive or hidden elements?

Minor issue: A non-critical tip is collapsible, but no essential information is trapped inside.

Example: A "Did you know?" box that expands but contains only supplementary trivia.

Major issue: Critical prerequisites, required API keys, or breaking-change warnings are buried inside a collapsible, tab, or visual-only element that an AI agent cannot parse.

Example: A mandatory config flag is only mentioned inside a `details` HTML element.

Major issue: Essential information, such as commands, prerequisites, or warnings, appears only at the end of the document after extended background, risking context-limit loss.

Other things to look out for: content relies on client-side JavaScript; diagrams lack alt text or textual equivalents; information is conveyed only through screenshots.

### Check 8: Agentic Legibility: Self-Contained Content

Question: Can each section be understood independently, or are cross-references accompanied by enough inline context to remain useful when chunked?

Minor issue: A cross-reference lacks a brief inline summary, making the chunk slightly ambiguous if extracted alone.

Example: "See the authentication setup for details" with no one-sentence recap.

Major issue: The document relies so heavily on cross-references that no single chunk is understandable in isolation; essential instructions are split across files with only phrases like "as described earlier."

Example: A setup guide says "Run the command described in step 2 of the installation manual" with no recap.

Other things to look out for: absolute internal URLs break across forks or branches; ambiguous language like "as mentioned above" lacks a direct link or anchor.

## Section D: Language Quality

### Check 9: Terminology

Question: Is terminology used consistently throughout the documentation?

Minor issue: A less-significant term is used with a synonym once or twice, but context makes the meaning clear.

Example: "Dashboard" and "home screen" used interchangeably, but still understandable.

Major issue: A key term is referred to by different names in different places, causing an AI to believe they are separate entities; a term has different meanings in different docs without explanation.

Example: "workspace" is also called "project", "sandbox", and "environment" with no mapping table.

Other things to look out for: acronyms not expanded on first use; glossary contradicts actual usage; code identifiers, endpoints, or class names use incorrect casing or variation.

### Check 10: Linguistic Consistency

Question: Are language, tone, and spelling conventions, such as US versus UK English and formality level, uniform across all documents?

Minor issue: A single document uses a different spelling variant or sporadically switches between "you" and "the user".

Major issue: Whole sections or documents switch between drastically different tones, causing an AI to misjudge audience or authority level.

Example: Formal academic tone switches to casual chatty guidance without a clear reason.

Other things to look out for: inconsistent tense for system behavior; mixed instruction and description styles without clear demarcation.

### Check 11: Clarity And Concision

Question: Is the prose clear, direct, and free from unnecessary jargon, ambiguity, or verbosity?

Minor issue: Occasional wordiness or a sentence that requires rereading; a minor ambiguity that does not lead to a wrong action.

Example: "It is important to note that the system, in its current implementation, may occasionally exhibit behavior that is not entirely predictable" could be "The system may sometimes behave unpredictably."

Major issue: A paragraph can be interpreted in two fundamentally different ways; essential required steps are buried in wall-of-text; jargon makes the doc incomprehensible to the target audience.

Example: A 500-word deployment paragraph where the crucial command appears once in the middle without formatting or callout.

Other things to look out for: over-abbreviated language; confusing sentence fragments; inconsistent detail level.

### Check 12: Information Density And Prioritization

Question: Is the document structured to front-load critical information, avoid internal redundancy, and keep topics focused for token-efficient processing?

Minor issue: Slight internal redundancy; preamble is longer than necessary but still useful.

Example: The same version compatibility note appears in both introduction and final summary.

Major issue: The file covers multiple unrelated concepts, forcing an agent to load a large document for a small question; critical information appears last after extensive exposition.

Example: One Markdown file documents the whole API surface, deployment, and troubleshooting.

Other things to look out for: file length so great that one topic is split across many agent chunks without self-contained summaries; gotchas buried mid-section; ordering does not follow a logical need-to-know progression.

## Section E: Content Completeness And Practical Guidance

### Check 13: Examples And Practical Guidance

Question: Are key concepts, APIs, and workflows accompanied by minimal executable examples or step-by-step walkthroughs, including non-obvious constraints?

Minor issue: An example exists but uses a non-ideal scenario; example code would fail in a real environment due to a missing import or configuration line that the text mentions.

Example: A Python snippet calls `requests.get()` without showing `import requests`.

Minor issue: A parameter is described as required but the expected format or type restriction is not stated nearby.

Example: A command accepts `--date` but does not state the format must be `YYYY-MM-DD`.

Major issue: A core endpoint or workflow is described purely in prose with no code sample or numbered steps; the only example is too abstract to adapt.

Example: The `/users` endpoint reference has no request or response example.

Major issue: A code example omits non-obvious constraints or business rules essential for execution.

Example: A POST endpoint says "Provide `body.url`" but omits that exactly one of `body.url` and `body.file` is required.

Other things to look out for: placeholders not clearly flagged; examples work only on one OS without disclaimer; examples use deprecated syntax.

### Check 14: Referencing

Question: Are external sources cited where needed, and are internal cross-references provided for context?

Minor issue: A statement would benefit from a source but is well-known or easily verifiable; an internal link uses an absolute URL that will break on fork or branch change.

Example: `https://github.com/owner/repo/blob/main/docs/setup.md` instead of relative `setup.md`.

Major issue: A critical claim lacks a source; a see-also link vital to understanding is dead.

Example: A deprecation note has no link to the official deprecation notice or changelog.

Other things to look out for: over-citation clutter; references point to non-permanent resources; missing cross-references prevent completion of a multi-step task.

### Check 15: Documentation Completeness

Question: Are there dead ends, broken links, placeholder pages, or obvious gaps in the documentation?

Minor issue: A non-critical "to be written" placeholder; broken link to optional external resource.

Example: "Advanced Customization" contains only "Coming soon."

Major issue: A broken link prevents a core task; placeholder page exists where actual documentation should be; an entire feature or endpoint is referenced but never documented.

Example: Setup guide links to missing `system-requirements.md`.

Other things to look out for: circular references; links redirect to a generic home page; docs assume prior knowledge from a missing prerequisite guide.

## Section F: Global Consistency

### Check 16: Unified Truth

Question: Does every piece of information have one canonical location that serves as the single source of truth?

Minor issue: A fact appears in two places, but duplication is intentional and one doc points to the canonical location.

Example: Getting Started and FAQ both describe installation, but FAQ links to Getting Started for details.

Major issue: Same fact exists in multiple documents with conflicting or diverging details, or no canonical source is identified.

Example: One document states the default timeout is 30 seconds, another says 5 seconds.

Other things to look out for: partial duplication where a summary diverges over time; links to canonical locations are broken or point to wrong versions.
