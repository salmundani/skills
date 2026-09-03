# Repo: Agent Skills

One skill per directory under `skills/`, entry point `skills/<name>/SKILL.md`.
Evals live in `evals/<name>.jsonl`.

## Working here

1. Scaffold with `./scripts/new-skill.sh <gerund-name>`; don't hand-create directories.
2. Write or update `evals/<name>.jsonl` (three scenarios minimum) *before* expanding prose.
3. Run `./scripts/validate.py` before finishing. Fix everything it reports.
4. Run `./scripts/validate.py --update-readme` when a skill's name or description changes.
5. Don't install skills into `~/.claude/skills` directly — `./scripts/install.sh` symlinks
   them, so the repo stays the single source of truth.

## Authoring standard

Distilled from [Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices).
`scripts/validate.py` enforces the mechanical rules; the rest is judgment.

### Frontmatter

Two fields are required and validated:

```yaml
---
name: reviewing-migrations        # ≤64 chars, [a-z0-9-] only, no "claude"/"anthropic"
description: >
  Reviews database migrations for lock risk, backfills, and rollback safety.
  Use when a migration file changes, or the user mentions migrations, schema
  changes, or ALTER TABLE.                      # ≤1024 chars, third person
---
```

Optional keys: `metadata.author` / `metadata.version` for provenance, and `allowed-tools`
to pre-approve tools for the invoking turn.

Every skill directory is also a slash command: `skills/clean-comments/` gives
`/clean-comments`, and the directory name (not the `name` field) sets the command. Two
frontmatter fields decide who may invoke it:

- `disable-model-invocation: true` — explicit command only. Claude can't auto-load it, and
  the description stays out of context until invoked. Use for anything with side effects or
  where timing is yours to choose.
- `user-invocable: false` — the inverse: background knowledge Claude loads on its own,
  hidden from the `/` menu.

These are Claude Code-only fields. A skill using them still loads fine here, but packaging
it for claude.ai or the Skills API fails, since that path allows only `name`,
`description`, `license`, `compatibility`, `metadata`, and `allowed-tools`.

**The description is the whole discovery mechanism.** Only `name` and `description` are
preloaded; Claude picks the skill from these alone. Third person, what it does *and* the
concrete triggers, using the words that would actually get typed.

### Naming

Gerund form, kebab-case: `reviewing-migrations`, `writing-runbooks`, `processing-invoices`.
Noun phrases (`pdf-processing`) are acceptable. Never `helper`, `utils`, `tools`, `data`.
The directory name under `skills/` must equal the `name` field.

### Body

- Under 500 lines. Push detail into `reference/*.md` and link it from SKILL.md.
- References stay **one level deep** — every detail file links directly from SKILL.md,
  never from another detail file.
- Reference files over 100 lines start with a table of contents.
- Assume Claude is smart: only add context it doesn't already have. Cut any paragraph
  that explains a well-known concept.
- One term per concept, used consistently throughout.
- Forward slashes in every path. No dates or "as of version X" — put superseded guidance
  in a collapsed `<details>` "Old patterns" section instead.
- Give one default approach with an escape hatch, not a menu of options.

### Degrees of freedom

Match specificity to how fragile the task is:

| Task shape | Give Claude |
| --- | --- |
| Many valid approaches, context decides | Prose steps and heuristics |
| Preferred pattern, some variation fine | Pseudocode or a parameterized script |
| Fragile, exact sequence required | An exact command, and say not to deviate |

### Scripts

Scripts live in `skills/<name>/scripts/` and are **executed**, not read into context —
say which one you mean ("Run `scripts/check.py`" vs "See `scripts/check.py` for the
algorithm"). Handle errors inside the script rather than deferring to Claude, justify
every constant in a comment, and state required packages explicitly in SKILL.md.

For batch or destructive operations, use plan → validate → execute: have Claude write a
structured plan file, validate it with a script, then apply it.

### Evaluations

Write the evals before the prose. Three scenarios minimum, one JSON object per line:

```json
{"skills": ["reviewing-migrations"], "query": "Review this migration for safety", "files": ["evals/fixtures/add_index.sql"], "expected_behavior": ["Flags the non-concurrent index creation as a table-lock risk", "Suggests CREATE INDEX CONCURRENTLY", "Notes the migration is not reversible as written"]}
```

No built-in runner; these are the checklist to grade against by hand. Run them in a fresh
session with the skill installed, and test with Haiku as well as Opus — what Opus infers,
Haiku may need spelled out.

### Checklist before committing

- [ ] Description says what it does *and* when to use it, in third person
- [ ] Directory name matches `name`
- [ ] Body under 500 lines, detail split into `reference/`
- [ ] References one level deep, all link targets exist
- [ ] Examples are concrete, terminology consistent
- [ ] No time-sensitive statements outside an "Old patterns" section
- [ ] At least three evals in `evals/<name>.jsonl`
- [ ] `./scripts/validate.py` passes
