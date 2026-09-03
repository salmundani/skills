# skills

Personal collection of [Agent Skills](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) —
instructions I use daily, codified so Claude loads them automatically when they're relevant.

## Layout

```
skills/<skill-name>/SKILL.md   # one directory per skill; SKILL.md is required
scripts/                       # repo tooling (validate, scaffold)
templates/                     # starting point for a new skill
evals/<skill-name>.jsonl       # evaluation scenarios, one JSON object per line
```

A skill directory may also contain:

```
skills/<skill-name>/
├── SKILL.md          # entry point, loaded when the skill triggers
├── reference/*.md    # detail files, linked one level deep from SKILL.md
└── scripts/*         # utility scripts Claude executes (not loaded into context)
```

## Install

Symlink every skill in this repo into `~/.claude/skills/`:

```bash
./scripts/install.sh          # symlink all skills
./scripts/install.sh --dry-run
./scripts/install.sh --force  # replace existing entries of the same name
```

Skills are picked up by Claude Code on the next session. Because these are symlinks,
editing a skill here takes effect immediately.

## Add a skill

```bash
./scripts/new-skill.sh reviewing-migrations
$EDITOR skills/reviewing-migrations/SKILL.md
./scripts/validate.py
```

See [CLAUDE.md](CLAUDE.md) for the authoring conventions this repo follows.

## Validate

```bash
./scripts/validate.py           # all skills
./scripts/validate.py skills/reviewing-migrations
```

Checks frontmatter (`name`, `description`), naming rules, body length, link targets,
and Windows-style paths. CI runs the same script on every push.

## Skills

<!-- BEGIN SKILLS TABLE -->
| Skill | Description |
| --- | --- |
| [`clean-comments`](skills/clean-comments/SKILL.md) | Removes or rewrites code comments so that every remaining comment follows the comment conventions from Robert C. Martin's Clean Code. Use when code is over-c... |
| [`codex-review`](skills/codex-review/SKILL.md) | Reviews the current branch against its parent with codex exec review, then triages and fixes the findings, looping until the review is clean. Use when finish... |
<!-- END SKILLS TABLE -->

Regenerate this table with `./scripts/validate.py --update-readme`.
