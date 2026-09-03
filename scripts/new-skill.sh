#!/usr/bin/env bash
# Scaffold a new skill from templates/skill.
#
# Usage: ./scripts/new-skill.sh <skill-name>
#
# <skill-name> must be lowercase letters, numbers and hyphens. Prefer gerund
# form: reviewing-migrations, writing-runbooks.
set -euo pipefail

repo="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if [ $# -ne 1 ]; then
  echo "usage: $0 <skill-name>" >&2
  exit 2
fi

name="$1"

if ! [[ "$name" =~ ^[a-z0-9-]+$ ]]; then
  echo "error: '$name' must contain only lowercase letters, numbers and hyphens" >&2
  exit 1
fi
if [ ${#name} -gt 64 ]; then
  echo "error: '$name' is ${#name} chars, max is 64" >&2
  exit 1
fi
case "$name" in
  *claude*|*anthropic*)
    echo "error: '$name' contains a reserved word (claude, anthropic)" >&2
    exit 1
    ;;
esac

dest="$repo/skills/$name"
if [ -e "$dest" ]; then
  echo "error: $dest already exists" >&2
  exit 1
fi

# Title-case the hyphenated name for the SKILL.md heading: foo-bar -> Foo Bar
title="$(echo "$name" | tr '-' ' ' | awk '{for (i=1; i<=NF; i++) $i = toupper(substr($i,1,1)) substr($i,2); print}')"

cp -R "$repo/templates/skill" "$dest"
find "$dest" -name .gitkeep -delete
rmdir "$dest/reference" "$dest/scripts" 2>/dev/null || true

sed -i.bak -e "s/SKILL_TITLE/$title/g" -e "s/SKILL_NAME/$name/g" "$dest/SKILL.md"
rm -f "$dest/SKILL.md.bak"

mkdir -p "$repo/evals"
sed "s/SKILL_NAME/$name/g" "$repo/templates/eval.jsonl" > "$repo/evals/$name.jsonl"

echo "created skills/$name/SKILL.md"
echo "created evals/$name.jsonl"
echo
echo "next: fill in the description and evals, then run ./scripts/validate.py"
