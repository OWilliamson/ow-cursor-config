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

- **How it works (in depth):** Architecture, data/control flow, equations, version quirks, edge cases.
- **Implementation notes:** Practical steps (envs, commands, repo paths, notebooks, pipelines) and how to validate.
- **Research Backing:** Papers, benchmarks, official research posts, stated limitations, or explicit “no strong backing found” after search.
- **Public Sentiment:** Thread/issue tone with selection-bias caveats; cite `SRC-###` per specific claim.

## Sentiment guardrails

- Attribute sentiment to **sources** (e.g. “maintainers on GitHub emphasize X — SRC-012”) rather than universal claims.
- Call out **uncertainty**: vocal minorities, release timing, version skew.

## When searches fail

Document dead ends briefly in `reference.md` (e.g. “No arXiv hits; tried: …”) so the next review does not repeat the same queries blindly.
