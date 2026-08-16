#!/usr/bin/env python3
"""Validate the repository's Agent Skill shape and internal references."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.S)
REQUIRED_FRONTMATTER = {"name", "description"}
REQUIRED_AGENT_CONFIG = {"display_name", "short_description", "default_prompt"}


def frontmatter_keys(text: str) -> set[str]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return set()
    keys: set[str] = set()
    for line in match.group(1).splitlines():
        if ":" in line and not line.lstrip().startswith("#"):
            keys.add(line.split(":", 1)[0].strip())
    return keys


def yaml_keys(text: str) -> set[str]:
    return {
        line.split(":", 1)[0].strip()
        for line in text.splitlines()
        if ":" in line and not line.lstrip().startswith("#")
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repo", nargs="?", default=".", type=Path)
    args = parser.parse_args()
    root = args.repo.resolve()
    skill = root / "skills" / "ship-pretty"
    skill_md = skill / "SKILL.md"
    agent_yaml = skill / "agents" / "openai.yaml"
    errors: list[str] = []

    if not skill_md.is_file():
        errors.append(f"missing {skill_md.relative_to(root)}")
    else:
        missing = REQUIRED_FRONTMATTER - frontmatter_keys(skill_md.read_text(encoding="utf-8"))
        errors.extend(f"SKILL.md missing frontmatter key: {key}" for key in sorted(missing))

    if not agent_yaml.is_file():
        errors.append(f"missing {agent_yaml.relative_to(root)}")
    else:
        missing = REQUIRED_AGENT_CONFIG - yaml_keys(agent_yaml.read_text(encoding="utf-8"))
        errors.extend(f"openai.yaml missing key: {key}" for key in sorted(missing))

    if skill_md.is_file():
        skill_text = skill_md.read_text(encoding="utf-8")
        for reference in re.findall(r"`?(references/[A-Za-z0-9._/-]+\.md)`?", skill_text):
            if not (skill / reference).is_file():
                errors.append(f"broken SKILL.md reference: {reference}")
        for script in re.findall(r"`?(?:<skill-dir>/)?scripts/([A-Za-z0-9._/-]+)`?", skill_text):
            if not (skill / "scripts" / script).is_file():
                errors.append(f"broken SKILL.md script reference: scripts/{script}")

    if errors:
        print("Ship Pretty skill validation: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Ship Pretty skill validation: PASS")
    print(f"- root: {root}")
    print("- SKILL.md frontmatter: name, description")
    print("- agents/openai.yaml: display_name, short_description, default_prompt")
    print("- internal references: resolved")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
