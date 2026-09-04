# Prose strip tropes decisions

Enumerated decisions for `/owcc-prose-strip-tropes`, in **[SKILL.md](SKILL.md)** workflow order. Rubric: [VALIDATION.md](VALIDATION.md).

## Index

| # | Decision | Workflow step |
|---|----------|---------------|
| 1 | [Target](#1-target) | 5.3.1 |
| 2 | [Mode](#2-mode) | 5.3.2 |
| 3 | [Preserve](#3-preserve) | 5.3.3, 5.3.5, 5.3.6 |
| 4 | [Check categories](#4-check-categories) | 5.3.4, 5.3.6 |
| 5 | [Severity](#5-severity) | 5.3.4, 5.3.6 |
| 6 | [Rewrite limits](#6-rewrite-limits) | 5.3.5, 5.3.6 |

---

## 1. Target

**Workflow:** 5.3.1

| Option | Description | Choose when | Apply to |
|--------|-------------|-------------|----------|
| **File path** | Edit or audit on disk | User gives path or `@` attaches a file | That file |
| **Paste** | Prose IN the invoke message | User pastes a block to clean | Chat return (unless they name a write path) |
| **Named chat turn** | Prior assistant (or user) message | “Last reply”, “de-AI that”, “strip tropes from that”, message id/quote | That turn’s text IN this chat |
| **Open editor file** | File focused IN IDE | “This file” and one open candidate | That path IF unambiguous |
| **Ambiguous / none** | Ask once | Two+ candidates or none | Do NOT guess |

**Do not use:** Arbitrary “latest markdown in the repo” without chat linkage.

---

## 2. Mode

**Workflow:** 5.3.2

| Mode | Meaning | Choose when |
|------|---------|-------------|
| **rewrite** | Check, then apply fixes | Default when target is clear and user did not say audit/findings-only |
| **audit** | Check only; no prose changes | User says audit, findings-only, report-only, or “don’t edit” |

IF both signals conflict, THEN prefer the later user message.

---

## 3. Preserve

**Workflow:** 5.3.3, 5.3.5, 5.3.6

Leave these unchanged unless the user explicitly asks to alter them:

| Region | Examples |
|--------|----------|
| Code | Fenced blocks, indented code, inline code |
| Identifiers | Paths, URLs, commands, API/library names, issue keys, norm IDs |
| Structure | YAML/JSON keys and values that are machine-read; frontmatter enums; table column headers when semantic |
| Templates | Skill RESPONSE / OUTPUT contracts, required headings, checklist item ids |
| Domain vocabulary | Intentional house terms (product names, reconcile vocabulary, org jargon used on purpose) |
| Facts | Numbers, quoted evidence, citations, must/must-not requirements |

Prose *around* preserved regions may change; the preserved tokens themselves must stay intact.

Heading `#` / `##` IN a markdown file is not a trope by itself. Flag markdown-as-default only when the sink is not markdown (wikitext, plain email body, YAML string).

---

## 4. Check categories

**Workflow:** 5.3.4, 5.3.6

RUN every category. A hit is optional wording or layout that signals instruction-tuned house style more than content. Skip when the same pattern is required by a template or is accurate technical phrasing.

**Overlay:** IF the workspace contains `topics/llm-output-tropes/deepdive.md`, THEN READ it and prefer its dated inventory when it disagrees with the snapshot below on era or seeds. Do NOT copy that catalogue into always-on rules. Do NOT treat it as a word-ban.

**Ineffective alone:** one watch-list token; isolated sentence-initial *Additionally* / *Consequently*; “fancy academic” register; a single em dash; curly quotes.

### Discourse and rhetoric (C1–C12)

| ID | Category | What to look for |
|----|----------|------------------|
| C1 | **Stock framing** | Generic openers/closers and throat-clearing (“I'd be happy to”, “Great question”, “In conclusion”, “It's worth noting”, “As an AI…”); chat residue (*I hope this helps*, *Of course!*, *Certainly!*, *You're absolutely right!*, *Would you like…*, *is there anything else*, *let me know*, *here is a more detailed breakdown*); knowledge-cutoff cans (*as of my last knowledge update*, *based on available information*, *not widely documented*); didactic *it’s important/crucial to note/remember* |
| C2 | **Performative helpfulness** | Sentences whose only job is to signal diligence; participle tack-ons (*highlighting*, *underscoring*, *illustrating*) that add no mechanism |
| C3 | **Empty intensifiers** | Abstract praise without a referent; generic significance (*testament*, *pivotal*, *crucial role*, *evolving landscape*, *indelible mark*); copula avoidance (*serves as*, *stands as*, *marks*, *functions as*, *boasts*, *features*, *offers* in place of *is/are/has*) |
| C4 | **Rhetorical templates** | Negative parallelism: *not only X but Y*; *it’s not just X, it’s Y*; *not X but Y*; ornamental *X rather than Y*; rule of three (adj, adj, adj or three canned noun phrases); *simple yet powerful* / chiasmus |
| C5 | **Sycophancy** | Unearned praise of the user, the codebase, or the plan |
| C6 | **Restatement loops** | Same claim again in softer words; outline futures (Challenges / Future prospects / In conclusion restating the body); canned notability (*has garnered attention*, *widely recognized*) without named coverage |
| C7 | **Uniform rhythm** | Long runs of same-length sentences or parallel bullets that read as generated pattern rather than distinct points |
| C8 | **Decorative chrome** | Emoji-as-heading-prefix; badge-like bold stacks; flourish punctuation; formulaic *clause — punch — clause* em dashes (often with spaces around the dash) — **supporting** evidence only |
| C9 | **Hedge theatre** | Softeners that add no real uncertainty (*might possibly*, *it could be argued*) when evidence state is known; inverse: unearned *clearly* / *simply* / *just* / *easily* / *obviously*; vague attribution (*studies show*, *experts say*) with no named source |
| C10 | **False collaboration** | “We” / “let's” / “together” filler when no joint action is happening |
| C11 | **Generic abstraction** | Noun piles that could apply to any topic (*holistic approach*, *key insights*, *moving forward*, *in the realm of*) where a specific referent exists |
| C12 | **Signpost spam** | Meta narration of reply structure (“First, I will…”, “In this section we discuss…”) when order is already visible |

### Lexicon, layout, residue (C13–C15)

| ID | Category | What to look for |
|----|----------|------------------|
| C13 | **Stock lexicon** | Watch-list / overrepresented seeds IN the [dated snapshot](#dated-lexicon-snapshot-2026-09-04); near-synonyms with the same job. Allow listed house terms. One token is weak. |
| C14 | **Layout defaults** | Inline-header lists (`- **Label:** rest` or `1. **Thing:**`); mechanical bold on every keyword or “key takeaways”; Title Case headings that are not titles; empty parent heading wrapping children; thematic `---` between sections; H1 spam / skipped heading levels; stats stuffed into a tiny table that should be a sentence; placeholders (`PASTE_URL_HERE`, `TODO: add image`) |
| C15 | **Rewrite residue** | After a rewrite: synonym cycling (*delve* → *explore* with the same empty job); article-stripped fragments; slang or first-person “soul” the source lacked |

Record locus with a short quote. IF unsure whether a phrase is intentional house style, THEN severity `note` and leave it IN audit; IN rewrite, change only when clearly trope-led.

### Dated lexicon snapshot (2026-09-04)

Snapshot for C13. Re-date when model fashion moves. Inflected forms count.

**Watch-list seeds (co-occurrence):** Additionally (esp. sentence-initial, weak alone), align with, boasts, bolstered, crucial, deep dive, delve, emphasizing, enduring, enhance, fostering, garner, highlight (verb), interplay, intricate / intricacies, key (adj.), landscape (abstract), meticulous / meticulously, pivotal, robust, showcase / showcasing, tapestry (abstract), testament, underscore (verb), valuable, vibrant.

**Measured focals (scientific English spike, 2020–2024 extract):** delve / delves / delving / delved, showcasing / showcases, underscores / underscoring / underscore, comprehending, intricacies / intricate, surpassing / surpasses, boasts, garnered, emphasizing, realm, groundbreaking, advancements, aligns.

**Era sketch (not hard cutoffs):** 2023–mid-2024 packs *delve, tapestry, testament, meticulous*; later text often thins to *emphasizing, enhance, highlighting, showcasing* plus notability cans. Some models still overuse *underscore*, *empirical*, *causal*. Em dash over-emission may be **historical** on families that suppress it — treat as supporting.

**Allow:** Literal *underscore* (underline); *landscape* / *deepdive* as coined topic or path tokens; *robust* IN statistics; *key* as in “primary key”; required template words.

---

## 5. Severity

**Workflow:** 5.3.4, 5.3.6

| Severity | Meaning | Rewrite |
|----------|---------|---------|
| `must-fix` | High-precision trope, **or** two-plus categories co-occurring IN the artefact with an obvious meaning-preserving fix | Always when mode IS rewrite |
| `should-fix` | Likely trope cluster; fix improves voice | Prefer fix when confident |
| `note` | Isolated lexical/punctuation hit, borderline, or intentional-looking | Report; change only IF user asked to be aggressive |
| `keep` | Required template or accurate tech phrasing | Do NOT change |
| `ask-user` | Empty promotional span; no in-artefact fact to recast with | Leave the span; do NOT invent |

**High-precision** (may `must-fix` without a second category): chat residue and knowledge-cutoff cans (C1); negative parallelism used as ornament (C4); inline-header list used as default cadence (C14); C15 telegram or invented soul.

**Not high-precision:** a single C13 seed; one em dash; one bold phrase; Title Case on a real title.

Findings are style/trope labels — do **not** claim the text was authored by a model.

---

## 6. Rewrite limits

**Workflow:** 5.3.5, 5.3.6

| Rule | Apply |
|------|--------|
| Meaning stable | Same claims, constraints, and outcomes after edit |
| Complete sentences | Do NOT drop articles/connectives to “sound human” |
| Minimal diff | Change flagged spans; do not restyle the whole file for taste |
| In-artefact facts | Recast empty significance using names, numbers, citations, or constraints already IN the target |
| No new content | Do NOT add examples, caveats, features, opinions, or slang the source lacked |
| Lists | Keep enumerated structure when it helps; each item a readable sentence when the sink is chat or other continuous prose; flatten C14 inline-header lists to ordinary sentences or label-free bullets when the bold+colon is cadence not a schema |
| No backup by default | CREATE a backup file only IF the user asked |
| File vs chat | File targets: MODIFY in place after the residue pass. Paste/chat targets: full cleaned text IN RESPONSE |

IF a must-fix cannot be fixed without guessing meaning, THEN leave the span, mark `ask-user` IN findings, AND do NOT invent.
