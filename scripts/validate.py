#!/usr/bin/env python3
"""Validate the skills in this repo against the authoring rules in CONTRIBUTING.md.

Usage:
    ./scripts/validate.py                    # all skills under skills/
    ./scripts/validate.py skills/foo         # one or more specific skills
    ./scripts/validate.py --update-readme    # also rewrite the README skills table

Exits non-zero if any error is found. Warnings do not fail the run.
"""

import argparse
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO / "skills"
EVALS_DIR = REPO / "evals"

# Limits come from the frontmatter validation rules in the Agent Skills docs.
NAME_MAX = 64
DESCRIPTION_MAX = 1024
NAME_RE = re.compile(r"^[a-z0-9-]+$")
RESERVED_WORDS = ("anthropic", "claude")

# The docs recommend keeping the SKILL.md body under 500 lines so it stays cheap
# to load; past that, content belongs in reference files.
BODY_MAX_LINES = 500
# Reference files longer than this should open with a table of contents, since
# Claude may preview them with a partial read.
TOC_THRESHOLD_LINES = 100
# Three scenarios is the minimum the authoring guide asks for.
MIN_EVALS = 3

MD_LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)
FRONTMATTER_RE = re.compile(r"\A---\r?\n(.*?)\r?\n---\r?\n?(.*)\Z", re.DOTALL)


def parse_frontmatter(text):
    """Return (metadata dict, body, error message or None)."""
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}, text, "missing YAML frontmatter delimited by '---' at the top of the file"
    raw, body = match.group(1), match.group(2)
    try:
        import yaml  # PyYAML is the reference parser; fall back if unavailable.
    except ImportError:
        return _parse_frontmatter_fallback(raw), body, None
    try:
        data = yaml.safe_load(raw)
    except Exception as exc:  # noqa: BLE001 - report any parse failure verbatim
        return {}, body, f"frontmatter is not valid YAML: {exc}"
    if not isinstance(data, dict):
        return {}, body, "frontmatter must be a YAML mapping"
    return data, body, None


def _parse_frontmatter_fallback(raw):
    """Minimal parser for `key: value` and folded `key: >` blocks, used when
    PyYAML is not installed. Handles the shapes this repo's template produces."""
    data = {}
    key = None
    buffer = []
    for line in raw.splitlines():
        if line.startswith((" ", "\t")) and key is not None:
            buffer.append(line.strip())
            continue
        if key is not None:
            data[key] = " ".join(buffer).strip()
            key, buffer = None, []
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            continue
        name, _, value = line.partition(":")
        value = value.strip()
        if value in (">", "|", ">-", "|-", ""):
            key, buffer = name.strip(), []
        else:
            data[name.strip()] = value.strip('"\'')
    if key is not None:
        data[key] = " ".join(buffer).strip()
    return data


class Report:
    def __init__(self):
        self.errors = []
        self.warnings = []

    def error(self, where, message):
        self.errors.append(f"{where}: {message}")

    def warn(self, where, message):
        self.warnings.append(f"{where}: {message}")


def check_skill(skill_dir, report):
    """Validate one skill directory. Returns (name, description) or None."""
    rel = skill_dir.relative_to(REPO)
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        report.error(rel, "no SKILL.md")
        return None

    text = skill_md.read_text(encoding="utf-8")
    meta, body, err = parse_frontmatter(text)
    where = rel / "SKILL.md"
    if err:
        report.error(where, err)
        return None

    name = str(meta.get("name", "")).strip()
    description = str(meta.get("description", "")).strip()

    if not name:
        report.error(where, "frontmatter is missing 'name'")
    else:
        if len(name) > NAME_MAX:
            report.error(where, f"name is {len(name)} chars, max is {NAME_MAX}")
        if not NAME_RE.match(name):
            report.error(where, f"name '{name}' must be lowercase letters, numbers and hyphens only")
        for word in RESERVED_WORDS:
            if word in name.lower():
                report.error(where, f"name contains the reserved word '{word}'")
        if name != skill_dir.name:
            report.error(where, f"name '{name}' does not match directory '{skill_dir.name}'")

    if not description:
        report.error(where, "frontmatter is missing 'description'")
    else:
        if len(description) > DESCRIPTION_MAX:
            report.error(where, f"description is {len(description)} chars, max is {DESCRIPTION_MAX}")
        if "<" in description and ">" in description:
            report.warn(where, "description looks like it contains XML tags, which are not allowed")
        first_person = re.search(r"\b(I|I'll|I can|you can use this)\b", description)
        if first_person:
            report.warn(where, "description should be third person ('Reviews X', not 'I review X')")
        if not re.search(r"\b(use when|use this|when the user|when a|when working)\b", description, re.I):
            report.warn(where, "description should state when to use the skill, not just what it does")
        if "TODO" in description:
            report.error(where, "description still contains TODO")

    body_lines = body.count("\n") + 1
    if body_lines > BODY_MAX_LINES:
        report.error(where, f"body is {body_lines} lines, max is {BODY_MAX_LINES}; split into reference files")

    check_links(skill_dir, skill_md, body, report, top_level=True)
    check_reference_files(skill_dir, report)
    check_evals(name or skill_dir.name, report)

    return (name or skill_dir.name, description)


def check_links(skill_dir, md_file, text, report, top_level):
    """Verify local link targets exist, and that detail files don't link on to
    further detail files (references must stay one level deep from SKILL.md)."""
    where = md_file.relative_to(REPO)
    # Links inside HTML comments are guidance for the author, not real references.
    for target in MD_LINK_RE.findall(HTML_COMMENT_RE.sub("", text)):
        target = target.split("#", 1)[0].strip()
        if not target or target.startswith(("http://", "https://", "mailto:")):
            continue
        if "\\" in target:
            report.error(where, f"link '{target}' uses backslashes; use forward slashes")
            continue
        resolved = (md_file.parent / target).resolve()
        if not resolved.exists():
            report.error(where, f"link target '{target}' does not exist")
            continue
        if not top_level and resolved.suffix == ".md":
            report.warn(
                where,
                f"links to '{target}'; keep references one level deep from SKILL.md",
            )


def check_reference_files(skill_dir, report):
    for md_file in sorted(skill_dir.rglob("*.md")):
        if md_file.name == "SKILL.md":
            continue
        text = md_file.read_text(encoding="utf-8")
        where = md_file.relative_to(REPO)
        lines = text.count("\n") + 1
        if lines > TOC_THRESHOLD_LINES and not re.search(r"^##\s*(contents|table of contents)", text, re.I | re.M):
            report.warn(where, f"{lines} lines without a '## Contents' table of contents")
        check_links(skill_dir, md_file, text, report, top_level=False)


def check_evals(name, report):
    path = EVALS_DIR / f"{name}.jsonl"
    where = path.relative_to(REPO)
    if not path.is_file():
        report.warn(where, f"no evaluations for skill '{name}'; add at least {MIN_EVALS}")
        return
    count = 0
    for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            case = json.loads(line)
        except json.JSONDecodeError as exc:
            report.error(f"{where}:{lineno}", f"invalid JSON: {exc.msg}")
            continue
        count += 1
        for field in ("skills", "query", "expected_behavior"):
            if field not in case:
                report.error(f"{where}:{lineno}", f"missing '{field}'")
        if name not in case.get("skills", []):
            report.warn(f"{where}:{lineno}", f"'skills' does not list '{name}'")
        if "TODO" in line:
            report.error(f"{where}:{lineno}", "still contains TODO")
    if count < MIN_EVALS:
        report.warn(where, f"{count} evaluations, expected at least {MIN_EVALS}")


def update_readme(skills):
    readme = REPO / "README.md"
    text = readme.read_text(encoding="utf-8")
    start, end = "<!-- BEGIN SKILLS TABLE -->", "<!-- END SKILLS TABLE -->"
    if start not in text or end not in text:
        print("README.md has no skills-table markers; skipping", file=sys.stderr)
        return
    rows = ["| Skill | Description |", "| --- | --- |"]
    if skills:
        for name, description in sorted(skills):
            summary = " ".join(description.split())
            if len(summary) > 160:
                summary = summary[:157].rstrip() + "..."
            rows.append(f"| [`{name}`](skills/{name}/SKILL.md) | {summary} |")
    else:
        rows.append("| _none yet_ | |")
    table = "\n".join(rows)
    head, _, rest = text.partition(start)
    _, _, tail = rest.partition(end)
    readme.write_text(f"{head}{start}\n{table}\n{end}{tail}", encoding="utf-8")
    print("README.md skills table updated")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("paths", nargs="*", help="skill directories to check (default: all)")
    parser.add_argument("--update-readme", action="store_true", help="rewrite the README skills table")
    parser.add_argument("--strict", action="store_true", help="treat warnings as errors")
    args = parser.parse_args()

    if args.paths:
        dirs = [Path(p).resolve() for p in args.paths]
    else:
        dirs = sorted(d for d in SKILLS_DIR.iterdir() if d.is_dir()) if SKILLS_DIR.is_dir() else []

    report = Report()
    skills = []
    for skill_dir in dirs:
        if not skill_dir.is_dir():
            report.error(skill_dir, "not a directory")
            continue
        result = check_skill(skill_dir, report)
        if result:
            skills.append(result)

    for warning in report.warnings:
        print(f"warning  {warning}")
    for error in report.errors:
        print(f"error    {error}")

    if args.update_readme:
        update_readme(skills)

    checked = len(dirs)
    print(f"\n{checked} skill(s) checked, {len(report.errors)} error(s), {len(report.warnings)} warning(s)")
    if report.errors or (args.strict and report.warnings):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
