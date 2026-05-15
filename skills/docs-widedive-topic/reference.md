# docs-widedive-topic — reference

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

## Identifying channel gaps

Before searching, audit the existing `reference.md` against the channel table above:

1. For each channel kind, check whether any `SRC-###` rows in `reference.md` already cover it.
2. Mark channels as **covered**, **thin** (one source), or **absent**.
3. Prioritise **absent** channels first, then **thin** ones.
4. Record your gap map at the top of the research session so you don't search covered ground again.

A channel is not "covered" just because the domain appears — a GitHub README is not the same channel as a GitHub issue thread, and a news article is not the same as an official changelog.

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

## Appending to existing docs

When adding new bullets to `info.md` or `deepdive.md`:

- **Append only** — add bullets or short paragraphs after existing content under the matching heading. Never remove, move, or rewrite existing text.
- **Match heading intent** — check the section rubric in the deepdive skill's `reference.md` (at `../.cursor/skills/docs-deepdive-topic/reference.md`) if you are unsure where a finding belongs.
- **Cite inline** — every new claim that originates from a source should end with `SRC-###` on the same line as the claim.
- **Skip missing headings** — if a heading the finding belongs to does not exist, note the gap in a comment in your session; do not create the heading (that is deepdive's job).

## Sentiment guardrails

- Attribute sentiment to **sources** (e.g. "maintainers on GitHub emphasize X — SRC-012") rather than universal claims.
- Call out **uncertainty**: vocal minorities, release timing, version skew.
- Widen the sentiment sample across new threads/issues rather than deepening the same source.

## When searches fail

Document dead ends in `reference.md` using the documented-null format required by the hub's **Writing quality standards**: include the exact query or channel tried and the date — e.g. "Searched `site:reddit.com <topic> performance` on YYYY-MM-DD; no threads with substantive discussion found." A channel listed as absent without a search record is not a valid null result — it is indistinguishable from not having searched. Do not leave a blank entry or a placeholder.
