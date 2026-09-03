# Repo: Agent Skills

This repo holds Agent Skills. One skill per directory under `skills/`, entry point
`skills/<name>/SKILL.md`.

When creating or editing a skill here:

1. Read `CONTRIBUTING.md` first — it is the authoring standard for this repo.
2. Scaffold with `./scripts/new-skill.sh <gerund-name>`; don't hand-create directories.
3. Write or update `evals/<name>.jsonl` (three scenarios minimum) *before* expanding prose.
4. Run `./scripts/validate.py` before finishing. Fix everything it reports.
5. Run `./scripts/validate.py --update-readme` when a skill's name or description changes.

Do not install skills into `~/.claude/skills` directly — `./scripts/install.sh` symlinks
them, so the repo stays the single source of truth.
