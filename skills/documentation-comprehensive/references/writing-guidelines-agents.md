Concise rules for writing clear, agent-readable docs. Use MUST/SHOULD/NEVER to guide decisions.

## Planning

- MUST: Plan before writing (overview, goal, audiences, documentation plan, open questions)
- MUST: Declare `meta.contentType` (`Tutorial`, `How-to`, `Reference`, `Conceptual`, `Troubleshooting`, `Landing`)
- MUST: Title is user-shaped (the user's question), not feature-shaped
- MUST: Define every term on first use; link to its conceptual page
- SHOULD: Goal uses a Bloom's taxonomy verb (`configure`, `explain`, `debug`)
- MUST: One page does one job (tutorial OR how-to OR reference, not all three)

## Voice & tone

- MUST: Active voice. Test: append "by monkeys". If the sentence parses, rewrite
- MUST: Direct address: `you`. Never `the user` or `one can`
- MUST: Imperative for steps ("Click **Add Project**", not "You will need to click...")
- SHOULD: Sentences under 20 words
- SHOULD: Contractions (`you'll`, `it's`)
- MUST: Present tense unless describing future behavior
- NEVER: `we` as a stand-in for `you` (only for deliberate Vercel actions)
- NEVER: `easy`, `simple`, `quick`
- NEVER: Filler words: `very`, `just`, `really`, `simply`
- NEVER: Rhetorical questions
- MUST: Second-read test: each sentence parses on one read at speech pace; name the subject, action, and consequence (kill metaphor verbs and far-reaching pronouns)

## Concision

- MUST: Earn every detail; cut a number, name, or implementation detail that wouldn't change the reader's understanding or action
- NEVER: Weasel words (`significantly`, `many`, `often`, `typically`, `generally`); give a specific number or claim
- NEVER: Vague quantifiers (`near-zero`, `sub-second`, `most requests`); give the figure and cite it
- NEVER: Filler/metaphor verbs (`moves through`, `lands`, `carries`, `hits`); name the literal step

## AI-generated tells

- NEVER: Summary-style transitions recapping the previous paragraph (`With this setup complete…`); pivot to the next point
- NEVER: Stop-start fragments splitting one dependent idea into choppy sentences
- NEVER: Spec-sheet voice reading like a datasheet (`provides`, `is configurable`, `is explicitly labeled`)
- NEVER: Cold-open body paragraphs with no antecedent; carry the prior subject forward
- NEVER: Personified artifacts performing human-physical actions (`hand the browser a URL` → `the browser fetches the URL`)
- NEVER: Reused/template framing not specific to the page (`The question most teams face is whether…`)

## Tone, by content type

- Tutorial: warm, encouraging, predictable structure
- How-to: terse, direct (reader is mid-task)
- Reference: neutral, exhaustive, quotable
- Conceptual: explain like the reader will teach it back
- Troubleshooting: empathetic but not apologetic

## Headings & structure

- MUST: Sentence case for page headings (`H1` through `H6`)
- MUST: Title case for nav labels
- MUST: Subheadings descriptive (`Caveats when self-hosting on Cloudflare`, not `Caveats`)
- MUST: Every page opens with a TL;DR paragraph
- MUST: Every major section opens with a summary sentence
- MUST: Acronyms spelled out on first use (`Content Security Policy (CSP)`)
- MUST: Keep paragraphs to 2 to 4 sentences; split anything longer or covering two ideas

## Lists

- MUST: Three or more list-shaped items convert to a list
- MUST: Always introduce a list with a colon
- MUST: Bold/description format: `- **Term**: description`
- NEVER: Periods on list items unless they're full sentences

## Code

- MUST: Language tag on every code block
- SHOULD: TypeScript first for new code
- MUST: Wrap multi-step flows in `<Steps/>`
- SHOULD: ≤80 columns per line; ≤25 lines per snippet (split with prose)
- SHOULD: Highlight load-bearing lines (` ```ts {8-12} `)
- MUST: Explain what each code block does in prose
- NEVER: Reference "see the full example file" at the end of a guide

## Placeholders, units, & numbers

- MUST: Text placeholders are `snake_case`, descriptive (`your_access_token_here`)
- MUST: Number placeholders count up (`1234567890123`)
- NEVER: `<TOKEN>`, `xxx`, `your-token`, `ABC123`
- MUST: Data sizes have a space and uppercase unit (`64 KB`, `200 ms`)
- MUST: Seconds bare (`30s`)
- MUST: Numerals for counts (`8 deployments`, not `eight`)

## Typography

- NEVER: Em dashes (`—`) or dashes (`-`) as punctuation. Use colons, commas, periods, or rephrase
- MUST: Curly quotes (`"` `"` `'` `'`), not straight
- MUST: Ellipsis character (`…`), not three dots (`...`)
- MUST: Loading states end with `…` (`Loading…`, `Saving…`)
- MUST: Non-breaking spaces for glued terms (`10&nbsp;MB`, `⌘&nbsp;K`, brand names)
- SHOULD: `&` over `and` only where space-constrained

## Source formatting

- NEVER: Hard-wrap paragraphs (each paragraph is one line in source)
- MUST: One blank line before headings; before and after code blocks
- NEVER: `---` horizontal rules between sections

## Emphasis

- MUST: Bold for UI elements or critical facts only, never for emphasis
- MUST: Inline code for paths, file extensions, identifiers, short snippets (`/api`, `.tsx`, `body`)

## Links

- MUST: Define every term on first appearance; link to its conceptual page
- MUST: Anchor text names the destination
- NEVER: Bare URLs or `here`/`link` as anchor text

## Pricing & money pages

- MUST: Use tables for pricing
- MUST: Document the pricing model explicitly
- NEVER: Assume the reader knows what counts as one invocation

## AI workflow

- MUST: You are accountable for AI-generated content
- MUST: Hold technical accuracy to a high standard (LLMs consume the docs)
- MUST: Use only enterprise models that do not train on your data
- MUST: Disclose AI use in the PR
- MUST: Plan first by hand; the plan is the spec
- MUST: Final human review

## Review

- MUST: PR description links the plan, lists what to review, links the preview URL
- MUST: Author is accountable; reviewers liberal with approvals
- SHOULD: Suggestion comments for small fixes; preview comments for bigger feedback
