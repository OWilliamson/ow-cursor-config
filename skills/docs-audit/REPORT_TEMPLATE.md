# Documentation Audit Report Template

Use this template for reports produced by the `docs-audit` skill.

```markdown
---
title: "Documentation Audit Report YYYY-MM-DD"
description: "Audit of documentation structure, metadata, freshness, agentic legibility, language quality, completeness, and global consistency."
target_path: "[path]"
created: "YYYY-MM-DDTHH:MM:SSZ"
updated: "YYYY-MM-DDTHH:MM:SSZ"
skill: "docs-audit"
skill_version: "1.0.0"
agent_model: "[model]"
current_product_version_evidence: "[source or Not provided]"
---

# Documentation Audit Report YYYY-MM-DD

## Summary

[Under 200 words. Describe the overall purpose of the documentation, what works well, and what needs attention.]

## Methodology

I reviewed the documentation directory and its subdirectories to answer 16 audit questions across six sections: Directory And File Structure, Metadata And Freshness, Structure And Agentic Legibility, Language Quality, Content Completeness And Practical Guidance, and Global Consistency.

For each question, I inspected the available documentation evidence and classified findings as Major, Minor, Other Issue, or Further Improvement. Red means one or more major issues, or three or more minor issues. Amber means one or two minor issues and no major issues. Green means no issues. Not Assessed means there was insufficient evidence to complete the check without guessing, except where missing required evidence is itself defined as an issue.

## Overview

| Number | Section | Check | State |
|--------|---------|-------|-------|
| 1 | A. Directory And File Structure | Document Naming | [Red/Amber/Green/Not Assessed] |
| 2 | A. Directory And File Structure | Directory-Level Indexing | [Red/Amber/Green/Not Assessed] |
| 3 | B. Metadata And Freshness | Metadata | [Red/Amber/Green/Not Assessed] |
| 4 | B. Metadata And Freshness | Timeliness | [Red/Amber/Green/Not Assessed] |
| 5 | C. Structure And Agentic Legibility | Document Style | [Red/Amber/Green/Not Assessed] |
| 6 | C. Structure And Agentic Legibility | Heading And Structure | [Red/Amber/Green/Not Assessed] |
| 7 | C. Structure And Agentic Legibility | Critical Information Visibility | [Red/Amber/Green/Not Assessed] |
| 8 | C. Structure And Agentic Legibility | Self-Contained Content | [Red/Amber/Green/Not Assessed] |
| 9 | D. Language Quality | Terminology | [Red/Amber/Green/Not Assessed] |
| 10 | D. Language Quality | Linguistic Consistency | [Red/Amber/Green/Not Assessed] |
| 11 | D. Language Quality | Clarity And Concision | [Red/Amber/Green/Not Assessed] |
| 12 | D. Language Quality | Information Density And Prioritization | [Red/Amber/Green/Not Assessed] |
| 13 | E. Content Completeness And Practical Guidance | Examples And Practical Guidance | [Red/Amber/Green/Not Assessed] |
| 14 | E. Content Completeness And Practical Guidance | Referencing | [Red/Amber/Green/Not Assessed] |
| 15 | E. Content Completeness And Practical Guidance | Documentation Completeness | [Red/Amber/Green/Not Assessed] |
| 16 | F. Global Consistency | Unified Truth | [Red/Amber/Green/Not Assessed] |

## Detailed Findings

### 1. Document Naming

State: [Red/Amber/Green/Not Assessed]

Question: Is there a consistent, predictable naming convention for documents and files?

Summary: [Short evidence-backed conclusion for this check, including Green states.]

Major issues:

- [File/path] Evidence: [specific evidence]. Impact: [why it matters]. Suggested resolution: [concrete fix].

Minor issues:

- [File/path] Evidence: [specific evidence]. Impact: [why it matters]. Suggested resolution: [concrete fix].

Other issues:

- [File/path] Evidence: [specific evidence]. Suggested resolution: [concrete fix].

Further improvements:

- [Suggestion]

[Repeat the same detailed section for checks 2 through 16.]

## Further Issues

[Any further issues or considerations that do not fit the 16 checks. If none, write: None found.]

## Priority Actions

1. [High impact, practical action]
2. [High impact, practical action]
3. [High impact, practical action]

## Conclusion

[Under 100 words.]
```
