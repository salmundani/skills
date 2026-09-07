---
name: remove-signs-of-ai-writing
description: >
  Rewrites user-facing copy — UI labels, error messages, empty states, docs and
  marketing prose — to remove the stylistic tells of LLM writing catalogued in
  Wikipedia's "Signs of AI writing". Use when the user asks to make strings sound
  less AI-generated, less like ChatGPT, or more human, or mentions AI slop, AI
  tells, LLM voice, or slop phrasing such as "not just X, but Y".
disable-model-invocation: true
metadata:
  author: salmundani
  version: "0.1.0"
---

# Remove Signs of AI Writing

The tells are a closed, specific set of words and constructions, not "writing that
sounds formal". Rewriting works by finding a listed tell and removing it, not by
making prose shorter, blunter, or more casual. A string with no tell in it is
already finished.

Full catalogue, with product-copy before/after pairs:
[reference/tells.md](reference/tells.md). Upstream source:
[Wikipedia:Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing).

## Scope

Rewrite strings a user reads: UI labels and buttons, headings, empty states,
tooltips, error and toast messages, onboarding and settings copy, CLI output,
release notes, README and docs prose, marketing pages.

Leave alone unless asked: identifiers, code comments, log lines, exception
messages that only reach a log, error codes, analytics event names, test names,
commit messages, and any string another program parses.

## Workflow

1. **Scope the pass.** Use the files or directory named in the request; with none
   given, use the current diff (`git diff`, plus staged and untracked files).
2. **Collect the strings.** Read each one where it renders — a 12-character button
   and a docs paragraph fail different ways and get different fixes.
3. **Flag, then rewrite.** For each string, name the tell before touching it. No
   tell, no edit. Rewrite one string at a time; keep every constraint in
   [Preserve](#preserve).
4. **Chase the copy.** `grep` the old literal across the repo. Update tests,
   snapshots, and fixtures that assert on it. Locale files are covered in
   [Preserve](#preserve).
5. **Report.** List `file:line`, the tell, and the before/after. Say which strings
   you deliberately left alone, and which translations went stale.

## The tells

The highest-signal ones for product copy. Each links to its section in
[reference/tells.md](reference/tells.md), which has the full list.

| Tell | Looks like | Fix |
| --- | --- | --- |
| [AI vocabulary](reference/tells.md#ai-vocabulary) | seamless, robust, vibrant, leverage, crucial, enhance, streamline, unlock, elevate, delve, tapestry, testament | Use the plain word, or cut the sentence |
| [Puffery](reference/tells.md#puffery-and-significance) | "powerful and intuitive", "our commitment to", "a testament to how much your team has grown" | State the fact, drop the praise |
| [Negative parallelism](reference/tells.md#negative-parallelism) | "Projects aren't just folders — they're the foundation of your workflow" | Say what it is, once |
| [Rule of three](reference/tells.md#rule-of-three) | "fine-grained, flexible, and secure" | Keep the item that carries information |
| [Copula avoidance](reference/tells.md#copula-avoidance) | serves as, functions as, boasts, features, represents | `is`, `has` |
| [Participle tails](reference/tells.md#participle-tails) | "…, ensuring your changes are never lost", "…, allowing you to focus on what matters" | Delete the tail, or make it its own claim |
| [Vague attribution](reference/tells.md#vague-attribution) | "industry-leading", "trusted by teams everywhere", "experts recommend" | Name the source or drop the claim |
| [Canned openers](reference/tells.md#canned-openers-and-closers) | sentence-initial "Additionally,", "Whether you're a solo dev or a large team…" | Cut |
| [Formatting tells](reference/tells.md#formatting-tells) | Title Case Headings, bolded key phrases, emoji bullets, `**Label**: description` lists, spaced em dashes, curly quotes | Sentence case, plain bullets, house punctuation |
| [Assistant register](reference/tells.md#assistant-register) | "Great question!", "Let's dive in", "I hope this helps", "Please try again later" | Address the user's task, not the chat |

Newer models produce fewer of the 2023-era tells (`delve`, `tapestry`) and more of
the quieter ones: participle tails, copula avoidance, puffery. Weight accordingly.

## Preserve

- **Placeholders and markup.** `%s`, `{count}`, `{{name}}`, `$1`, ICU plural and
  select blocks, HTML and JSX interpolations: same set, same order, same spelling.
- **Length budget.** Never lengthen a label, button, heading, or table cell. Body
  copy may shrink; it should not grow.
- **The claim.** Say the same thing about the same subject. Do not add a fact to
  fill the space a cut phrase left, and do not drop a caveat, limit, or
  consequence the user needs.
- **Escaping.** Rewriting `it's` into a single-quoted string, or a straight quote
  into a curly one, is how this pass breaks a build. Match the file's convention.
- **Other locales.** Change the source-language string only. Editing translated
  files is a separate task: report which locale files now hold stale text and let
  the user route it to translation.
- **Contract strings.** Leave anything with a stable-text contract — a string a
  test matches on by design, a CLI output another script greps, an accessibility
  label a test suite queries by text — or update every call site in the same pass.

## Do not overcorrect

The upstream page is explicit that these do **not** indicate AI writing, and
"fixing" them makes copy worse:

- **Correct em dashes.** Unspaced, one per sentence, doing real work: leave it.
  The tell is the spaced, pat, sales-pitch dash, not the character.
- **Formal or long words.** The list is specific words. Their synonyms are not on
  it, and `utilize`-hunting is a different job.
- **Genuine threes.** Three setup steps are three setup steps. The tell is three
  adjectives padding one idea.
- **Correct grammar, contractions, hedges, superlatives.** All normal human
  writing. Do not strip `very`, `we think`, or `the first` for tidiness.
- **Terseness for its own sake.** The target is copy a person on this team would
  write, not clipped fragments. Plain sentences with `is` and `has` are the goal.

When a string's only problem is that it is bad copy — vague, wrong register, buries
the action — say so and fix it, but call it what it is rather than an AI tell.
