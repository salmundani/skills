#!/usr/bin/env bash
# Symlink this repo's skills into ~/.claude/skills so Claude Code picks them up.
#
# Usage:
#   ./scripts/install.sh [--dry-run] [--force] [--target DIR] [skill-name ...]
#
# Symlinks (not copies) keep the repo as the single source of truth: editing a
# skill here takes effect immediately.
set -euo pipefail

repo="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
target="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}"
dry_run=0
force=0
names=()

while [ $# -gt 0 ]; do
  case "$1" in
    --dry-run) dry_run=1 ;;
    --force) force=1 ;;
    --target) shift; target="$1" ;;
    -h|--help) sed -n '2,9p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    -*) echo "error: unknown option $1" >&2; exit 2 ;;
    *) names+=("$1") ;;
  esac
  shift
done

if [ ${#names[@]} -eq 0 ]; then
  for dir in "$repo"/skills/*/; do
    [ -f "$dir/SKILL.md" ] || continue
    names+=("$(basename "$dir")")
  done
fi

if [ ${#names[@]} -eq 0 ]; then
  echo "no skills found in $repo/skills" >&2
  exit 0
fi

[ "$dry_run" -eq 1 ] || mkdir -p "$target"
installed=0
skipped=0

for name in "${names[@]}"; do
  src="$repo/skills/$name"
  dest="$target/$name"

  if [ ! -f "$src/SKILL.md" ]; then
    echo "skip     $name (no skills/$name/SKILL.md)" >&2
    skipped=$((skipped + 1))
    continue
  fi

  if [ -L "$dest" ] && [ "$(readlink "$dest")" = "$src" ]; then
    echo "ok       $name (already linked)"
    continue
  fi

  if [ -e "$dest" ] || [ -L "$dest" ]; then
    if [ "$force" -eq 0 ]; then
      echo "skip     $name ($dest exists; use --force to replace)" >&2
      skipped=$((skipped + 1))
      continue
    fi
    if [ "$dry_run" -eq 1 ]; then
      echo "would remove $dest"
    else
      rm -rf "$dest"
    fi
  fi

  if [ "$dry_run" -eq 1 ]; then
    echo "would link $dest -> $src"
  else
    ln -s "$src" "$dest"
    echo "linked   $name -> $dest"
  fi
  installed=$((installed + 1))
done

echo
echo "$installed linked, $skipped skipped, target $target"
[ "$dry_run" -eq 1 ] && echo "(dry run: nothing changed)"
exit 0
