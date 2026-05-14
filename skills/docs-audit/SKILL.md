---
name: docs-audit
description: Audits documentation directories for structure, metadata, freshness, agentic legibility, language quality, completeness, links, and cross-document consistency. Use when the user explicitly invokes docs-audit or asks to run this named documentation audit workflow.
disable-model-invocation: true
# Version format: MAJOR.MINOR.PATCH
version: 1.0.0
---

# Documentation Audit

## When to use

- Use when the user explicitly invokes `docs-audit`.
- Use when the user asks to run this named documentation audit workflow against a docs directory.
- Audit a documentation directory and all subdirectories for AI-agent-oriented documentation quality.

## Required inputs

- `target docs path`
- Optional current product version evidence
- Optional canonical glossary, style guide, or canonical index path

## Definition of done

- Produce an audit report at `docs/docs-report-YYYY-MM-DD.md`, or return the report in chat when file creation is not appropriate.
- Use YAML front matter for report metadata, including `created`, `updated`, and `skill_version`.
- Score all 16 checks as `Red`, `Amber`, `Green`, or `Not Assessed`.
- Base every finding on concrete evidence; mark unavailable evidence as `Not Assessed` unless the rubric defines missing evidence itself as an issue.
- Include file path, evidence, severity, impact, and suggested resolution for each finding.
- Complete the post-report verification in `WORKFLOW.md`.

## Non-goals

- Do not modify audited documentation.
- Do not invent current versions, release timing, glossary expectations, external link status, or canonical sources.
- Do not treat helper script output as final scoring or report-facing evidence; scripts extract internal mechanical inventory for judgment-heavy review.
- Do not include internal post-report checks in the delivered report.
- Do not suppress findings because the suggested resolution would change how the docs are structured or maintained. The audit is read-only, so it should freely recommend what the docs should become.

## Workflow

1. Confirm the target docs path, source type, output mode, and available version/glossary evidence.
2. Read `WORKFLOW.md`, then `CHECKLIST.md`, then `REPORT_TEMPLATE.md`. Read `EXAMPLES.md` only when shaping finding style.
3. Use cheap inventory and targeted reads first. Prefer helper scripts when available. Run them with **this skill’s directory** as the working directory (the folder containing `SKILL.md` and `scripts/`; when installed under `~/.cursor/skills/docs-audit/`, use that path), for example:
   - `python3 scripts/scan_docs.py <target docs path>`
   - `python3 scripts/check_links.py <target docs path>`
   - `python3 scripts/summarize_corpus.py <target docs path>`
4. Perform the phased review in `WORKFLOW.md`, using helper output only as internal inventory and using direct documentation evidence for judgments and report citations.
5. Fill `REPORT_TEMPLATE.md` or return the same report structure in chat.
6. Run the post-report verification from `WORKFLOW.md` before final delivery. Use the verification to improve the report; do not include the checklist itself in the delivered report.

