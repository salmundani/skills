# Tells, with rewrites

Each tell below is drawn from [Wikipedia:Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)
and restated for product copy. The "before" lines are the shape to look for; the
"after" lines show the fix, not a target style.

## Contents

- [AI vocabulary](#ai-vocabulary)
- [Puffery and significance](#puffery-and-significance)
- [Negative parallelism](#negative-parallelism)
- [Rule of three](#rule-of-three)
- [Copula avoidance](#copula-avoidance)
- [Participle tails](#participle-tails)
- [Vague attribution](#vague-attribution)
- [Canned openers and closers](#canned-openers-and-closers)
- [Formatting tells](#formatting-tells)
- [Assistant register](#assistant-register)
- [Error and empty states](#error-and-empty-states)
- [Not tells](#not-tells)

## AI vocabulary

A specific list, corroborated by frequency studies rather than taste. One instance
means nothing; three in a paragraph is the strongest single tell there is.

From the upstream list: `additionally` (sentence-initial), `align with`, `boasts`,
`bolstered`, `crucial`, `deep dive`, `delve`, `emphasizing`, `enduring`, `enhance`,
`fostering`, `garner`, `highlight` (verb), `interplay`, `intricate`, `key`
(adjective), `landscape` (abstract), `meticulous`, `pivotal`, `robust`, `showcase`,
`tapestry`, `testament`, `underscore` (verb), `valuable`, `vibrant`.

Product-copy additions that behave the same way: `seamless`, `seamlessly`,
`effortless`, `streamline`, `leverage` (verb), `empower`, `unlock`, `elevate`,
`supercharge`, `comprehensive`, `powerful`, `cutting-edge`, `game-changing`,
`ensure` (in a benefit clause), `journey`, `experience` (as the object of a verb).

> **Before:** Our robust sync engine leverages a distributed queue to ensure a
> seamless experience.
> **After:** Sync retries in the background, so your changes upload when you
> reconnect.

Read it as literally as the source does: a word being on this list says nothing
about its synonyms. `robust` is a tell; `sturdy`, `reliable`, and `durable` are not.

## Puffery and significance

Copy that tells the reader how important something is instead of what it does.
Watch for `stands as`, `is a testament to`, `plays a crucial role in`, `underscores
its importance`, `reflects our broader commitment to`, `marks a shift`, `at the
heart of`, `industry-leading`, `best-in-class`, `renowned`, `groundbreaking`.

> **Before:** You've used {used} of {limit} seats — a testament to how much your
> team has grown.
> **After:** You've used {used} of {limit} seats.

The upstream page notes newer models puff more quietly: not "the best" but
"designed to help teams do their best work". Same tell.

## Negative parallelism

The single most recognisable construction. Three shapes, all of them setting up a
misconception the reader never had:

- `Not just X, but Y` / `Not only X, but also Y`
- `It's not X, it's Y` / `no X, no Y, just Z`
- `X rather than Y`

> **Before:** Projects aren't just folders — they're the foundation of your
> workflow.
> **After:** A project holds the tasks and files for one piece of work.

> **Before:** This isn't a settings page. It's your control center.
> **After:** Settings for this workspace.

## Rule of three

Three adjectives or three short phrases padding one idea, usually to make a thin
claim sound thorough.

> **Before:** Fine-grained, flexible, and secure permissions.
> **After:** Set permissions per project.

Three items that each carry distinct information are not a tell. "Connect a repo,
pick a branch, run the first build" is three steps, not a flourish.

## Copula avoidance

LLM output routes around `is` and `has`. Watch for `serves as`, `stands as`,
`functions as`, `operates as`, `acts as`, `represents`, `marks`, `refers to`, and
the marketing verbs `boasts`, `features`, `offers`, `provides`, `maintains`,
`delivers`, `enables`.

> **Before:** The dashboard serves as your central hub and features four panels.
> **After:** The dashboard has four panels.

`refers to` in a definition is the same tell: "A webhook refers to an HTTP callback"
should be "A webhook is an HTTP callback".

## Participle tails

An `-ing` clause bolted onto the end of a sentence to editorialise about what was
just said: `ensuring`, `allowing`, `enabling`, `helping you`, `making it easy to`,
`highlighting`, `reflecting`, `contributing to`, `fostering`, `so you can focus on
what matters`.

> **Before:** Changes save automatically, ensuring you never lose work and allowing
> you to focus on what matters.
> **After:** Changes save automatically.

If the tail carries real information the user needs, promote it to its own sentence
in the active voice. If it only reassures, cut it.

## Vague attribution

Praise or evidence sourced to nobody: `industry reports`, `experts recommend`,
`observers have noted`, `trusted by teams everywhere`, `many users find`, `studies
show`, `widely regarded as`. Also the exaggerated plural — "several publications
have covered" next to one link.

> **Before:** Trusted by teams everywhere to keep their data safe.
> **After:** Data is encrypted at rest and in transit.

## Canned openers and closers

- Sentence-initial `Additionally,` `Moreover,` `Furthermore,` `Notably,` `In
  today's fast-paced world,` `In the ever-evolving landscape of`.
- The uplift closer: `Whether you're a solo developer or a large enterprise, X has
  you covered.`
- The challenges-and-outlook formula: a `Challenges` or `Looking ahead` section
  that opens "Despite its strengths, X faces several challenges" and ends on a
  vague positive. In docs and release notes this is the same shape as the
  Wikipedia article ending nobody asked for.

All three are cuts, not rewrites. Delete and reread the paragraph; it will hold.

## Formatting tells

- **Title Case Headings.** Sentence case unless the project's style guide says
  otherwise. Check neighbouring headings before changing anything.
- **Boldface as emphasis spray.** Every key phrase bolded, "key takeaways" style.
  Keep bold for UI element names and real warnings.
- **Inline-header bullets.** `**Unlimited projects**: Scale without limits.`
  repeated down a list. Either the header or the gloss is redundant: keep one.
  Often the whole list is better as a sentence.
- **Emoji as structure.** Emoji leading bullets, headings, or callouts. Remove,
  unless the file already uses them consistently and deliberately.
- **Spaced em dashes.** ` — ` used where a comma, colon, or parentheses belongs,
  often two per paragraph. A correctly used dash stays.
- **Curly quotes and apostrophes.** Only a tell when the file otherwise uses
  straight ones. Never introduce them into code strings; match the file.
- **Horizontal rules between every section**, and heading levels that skip (`#`
  straight to `###`) or that contain nothing but more headings.

## Assistant register

Chat-assistant voice leaking into shipped copy: `Great question!`, `Let's dive
in!`, `I hope this helps!`, `Feel free to`, `Simply click`, `Don't hesitate to`,
`Please note that`, `It's important to note that`, `Happy building!`.

> **Before:** Simply click the button below and you'll be all set!
> **After:** Select **Connect** to finish setup.

`Please try again later` belongs here too: it is the shape of an apology with no
information in it. Say what failed and what the user can do now.

## Error and empty states

These two surfaces attract every tell at once, so check them first.

An error message says what happened, what it means for the user's work, and what to
do next — in that order, in one or two sentences, with no reassurance in the middle.

> **Before:** We encountered an issue while syncing your workspace. Our robust sync
> engine leverages a distributed queue, ensuring your changes are never lost.
> Please try again in a few moments.
> **After:** Sync failed. Your changes are saved on this device and will upload
> when the connection returns.

An empty state says what the thing is and what to do to fill it. It is not the
place to explain why the feature matters.

> **Before:** No Projects Yet. Projects aren't just folders — they're the
> foundation of your workflow. Create your first project to unlock seamless
> collaboration.
> **After:** No projects yet. Create one to start tracking tasks and files.

## Not tells

Listed upstream as ineffective indicators. Leave them:

- Correct grammar and clean prose.
- Formal or academic vocabulary that is not on the list above.
- Mixed registers — casual phrasing inside technical copy is how engineers write.
- Contractions, hedges (`we think`, `usually`), intensifiers (`very`), and
  superlatives (`the first`, `the only`).
- Wordy-but-normal constructions: `in order to`, `as a result of`, `the fact that`.
  Tighten them if you like, but that is copyediting, not this pass.
