#!/usr/bin/env python3
"""Validate the Taste Library schema and retrieval-critical fields."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


DEFAULT_LIBRARY = Path(__file__).resolve().parents[1] / "references" / "taste-library" / "patterns.json"
DIMENSIONS = {"layout", "hierarchy", "components", "interaction", "motion", "responsive", "microcopy"}
REQUIRED = {"id", "dimension", "problem", "decision", "why_it_works", "use_when", "avoid_when", "failure_modes", "signals", "qa", "provenance"}


def validate(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        entries = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"cannot read JSON: {exc}"]
    if not isinstance(entries, list) or not entries:
        return ["library must be a non-empty JSON array"]
    ids: set[str] = set()
    for index, entry in enumerate(entries):
        label = f"entry {index + 1}"
        if not isinstance(entry, dict):
            errors.append(f"{label} must be an object")
            continue
        missing = REQUIRED - entry.keys()
        errors.extend(f"{label} missing {field}" for field in sorted(missing))
        identifier = entry.get("id")
        if not isinstance(identifier, str) or not identifier.strip():
            errors.append(f"{label} has invalid id")
        elif identifier in ids:
            errors.append(f"duplicate id: {identifier}")
        else:
            ids.add(identifier)
        if entry.get("dimension") not in DIMENSIONS:
            errors.append(f"{label} has invalid dimension: {entry.get('dimension')}")
        for field in ("use_when", "avoid_when", "failure_modes", "signals", "qa"):
            value = entry.get(field)
            if not isinstance(value, list) or not all(isinstance(item, str) and item.strip() for item in value):
                errors.append(f"{label}.{field} must be a non-empty string list")
        if isinstance(entry.get("qa"), list) and len(entry["qa"]) < 2:
            errors.append(f"{label}.qa needs at least two observable checks")
        for field in ("problem", "decision", "why_it_works", "provenance"):
            if not isinstance(entry.get(field), str) or not entry[field].strip():
                errors.append(f"{label}.{field} must be a non-empty string")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("library", nargs="?", type=Path, default=DEFAULT_LIBRARY)
    args = parser.parse_args()
    errors = validate(args.library)
    if errors:
        print("Taste Library validation: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"Taste Library validation: PASS ({len(json.loads(args.library.read_text(encoding='utf-8')))} patterns)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
