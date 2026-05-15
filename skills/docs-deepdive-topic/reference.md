# docs-deepdive-topic — reference

## Search channels

Use web search (and fetches when helpful). Prefer primary docs and official repos over SEO aggregators.

| Kind | How to search |
|------|----------------|
| News | Topic + vendor/product name; add `news` or a recent year if noisy. |
| Blog posts | Topic + `blog`, author names, engineering blogs, release notes. |
| Reddit | `site:reddit.com` + topic keywords; read thread context, not only titles. |
| GitHub | `site:github.com` + topic; README, issues, discussions for limitations and tone. |
| GitLab | `site:gitlab.com` + topic; same pattern as GitHub. |
| Research papers | arXiv, ACM, IEEE, Google Scholar; prefer abstracts and stated limitations. |
| Product documentation | Official docs domains, changelogs, API reference, migration guides. |

### Minimum search coverage

Before writing any `deepdive.md` section you **must** attempt at least **three distinct channel types**. For technical ML/tooling topics the required minimum is:

1. **Primary technical source** — arXiv, official docs, or spec (paper, RFC, changelog).
2. **Implementation artifact** — GitHub/GitLab repo, model hub card (Hugging Face, Ollama registry), or official benchmark leaderboard.
3. **Practitioner forum** — Reddit (`r/MachineLearning`, `r/LocalLLaMA`, etc.), Hacker News, or a project Discord/issue tracker.

Document failed searches in `reference.md` (e.g. "Searched `site:reddit.com slm edge inference`; no threads with ≥10 comments found as of YYYY-MM-DD") so the next review does not repeat them blindly.

## Query building

Combine **canonical names** (product, paper title, repo org/name) with **intent words**: `documentation`, `changelog`, `limitations`, `reddit discussion`, `issue`, `RFC`, `arxiv`, `evaluation`, `benchmark`.

Examples (adapt tokens):

- News: `"<Product>" announcement <year>` or `"<Product>" news blog`
- Blogs: `"<Topic>" engineering blog` OR `"<Author>" <Topic>`
- Reddit: `site:reddit.com <Topic> <Product>`
- GitHub: `site:github.com "<Topic>" README` or `site:github.com <org>/<repo> issues`
- GitLab: `site:gitlab.com <Topic>`
- Papers: `site:arxiv.org <Topic>` or `"<Topic>" survey paper`
- Docs: `"<Product>" official documentation` (verify the domain is official)

## Topic synthesis files

Each topic under `<docs-dir>/topics/<slug>/` uses:

- **`info.md`** — short, scannable overview (index-friendly).
- **`deepdive.md`** — room for mechanics, implementation steps, research backing, and sourced sentiment.

**`###` subsection headings must match exactly** (order matters). Optional one-line blurb may sit directly under the topic title `##` before the first `###` (keep short).

## `info.md` skeleton

```markdown
## <Topic title>

### Summary

### How it works

### Use cases for us

### Other use cases

### Strengths

### Weaknesses

### Future Outlook
```

## `deepdive.md` skeleton

```markdown
## <Topic title> — deep dive

### How it works (in depth)

### Implementation notes

### Research Backing

### Public Sentiment
```

## Section rubric

### `info.md`

- **Summary:** What it is, why it matters here, and the headline takeaway.
- **How it works:** High-level mechanics and boundaries only; point readers to `deepdive.md` for depth.
- **Use cases for us:** When this hub should use, pilot, teach, or operationalize (including ML workflows, not only editor config).
- **Other use cases:** Legitimate uses outside this hub.
- **Strengths / Weaknesses:** Balanced, evidence-backed bullets; cite `SRC-###` when the audit trail matters.
- **Future Outlook:** Trajectory, what would change the recommendation, open questions, and gaps vs other areas of the docs directory when relevant.

### `deepdive.md`

- **How it works (in depth):** Named architectural components, data/control flow, key design decisions, equations or pseudocode where they clarify (not merely decorate), version quirks and edge cases. **This section must explain the mechanism itself — not summarise what a source covers.** A phrase like "the paper analyses architecture, datasets, and algorithms" is not a deep dive; name the actual components (e.g. tokeniser type, attention variant, positional encoding scheme, training objective). Cite ≥2 independent sources; a single survey is a starting point, not backing.

- **Implementation notes:** Runnable commands, config snippets, model-hub identifiers, environment requirements, hardware numbers (VRAM, latency, context length), and a concrete "how to validate" step. **Do not defer wholesale to a paper** ("see the paper for implementation detail"). Extract the relevant step, quote the key config line, or state explicitly why a practical artifact cannot be provided. If a vendor CLI or tool is involved, name it and its relevant flags.

- **Research Backing:** ≥2 distinct source types (e.g. a paper + a benchmark leaderboard, two independent papers, or a paper + a model card with published eval numbers). State specific results or stated limitations — not just that a paper exists. If no strong backing is found after genuine search across the required channels, write "No peer-reviewed backing found; searched [channels] as of YYYY-MM-DD."

- **Public Sentiment:** Named-thread or issue tone tied to `SRC-###`, with selection-bias caveats. If genuine multi-channel search found nothing, write "Queried [channels] on [date]; no substantial practitioner discussion found" — do not leave this section blank, as a placeholder, or silently skipped.

## Sentiment guardrails

- Attribute sentiment to **sources** (e.g. "maintainers on GitHub emphasize X — SRC-012") rather than universal claims.
- Call out **uncertainty**: vocal minorities, release timing, version skew.

## When searches fail

Document dead ends briefly in `reference.md` (e.g. "No arXiv hits; tried: …") so the next review does not repeat the same queries blindly.
