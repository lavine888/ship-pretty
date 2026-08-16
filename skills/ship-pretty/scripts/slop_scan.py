#!/usr/bin/env python3
"""Static heuristic scan for common AI-UI implementation patterns.

Supporting evidence for Ship Pretty, not a visual judge.
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

TEXT_EXTENSIONS = {
    ".html", ".css", ".scss", ".sass", ".less", ".js", ".jsx",
    ".ts", ".tsx", ".vue", ".svelte",
}
SKIP_DIRS = {
    "node_modules", ".git", "dist", "build", ".next", ".nuxt",
    "coverage", "vendor",
}


@dataclass(frozen=True)
class Signal:
    name: str
    pattern: re.Pattern[str]
    threshold: int
    note: str


SIGNALS = [
    Signal(
        "rounded-everything",
        re.compile(r"\brounded(?:-(?:sm|md|lg|xl|2xl|3xl|full|\[[^\]]+\]))?\b|border-radius\s*:", re.I),
        5,
        "Many rounded surfaces; inspect whether shape hierarchy collapsed into one default radius.",
    ),
    Signal(
        "shadow-everything",
        re.compile(r"\bshadow(?:-(?:sm|md|lg|xl|2xl|inner))?\b|box-shadow\s*:", re.I),
        4,
        "Many shadows; inspect whether elevation is semantic or just polish chrome.",
    ),
    Signal(
        "gradient-overload",
        re.compile(r"(?:bg-gradient|linear-gradient|radial-gradient|conic-gradient|from-[\w\[]|to-[\w\[])", re.I),
        4,
        "Several gradient signals; inspect whether accents are scarce enough to preserve hierarchy.",
    ),
    Signal(
        "blur-glass-overload",
        re.compile(r"(?:backdrop-blur|filter\s*:\s*blur|backdrop-filter|blur-[\w\[])", re.I),
        3,
        "Repeated blur/glass effects; inspect whether they add structure or merely imply premium styling.",
    ),
    Signal(
        "pill-overload",
        re.compile(r"(?:rounded-full|border-radius\s*:\s*9999|border-radius\s*:\s*50px)", re.I),
        4,
        "Many pill shapes; inspect badges/buttons/tags for undifferentiated shape language.",
    ),
    Signal(
        "centered-stack",
        re.compile(r"(?:text-center|items-center|justify-center|text-align\s*:\s*center)", re.I),
        6,
        "Heavy centering signals; inspect whether the page defaults to a centered-stack composition.",
    ),
]

GENERIC_COPY = [
    re.compile(p, re.I)
    for p in [
        r"transform your (?:workflow|business|experience)",
        r"unlock the power of",
        r"supercharge your",
        r"built for the future",
        r"everything you need to",
        r"smarter\.?\s+faster\.?\s+better\.?,?",
        r"next[- ]generation",
        r"reimagine the way you",
    ]
]


def iter_files(root: Path) -> Iterable[Path]:
    if root.is_file():
        if root.suffix.lower() in TEXT_EXTENSIONS:
            yield root
        return

    for path in root.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in TEXT_EXTENSIONS:
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        yield path


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Heuristic static scan for AI-UI slop signals."
    )
    parser.add_argument(
        "path", nargs="?", default=".", help="Frontend file or directory to scan"
    )
    args = parser.parse_args()

    root = Path(args.path).resolve()
    files = list(iter_files(root))
    if not files:
        print("No supported frontend text files found.")
        return 0

    corpus_parts: list[str] = []
    total_bytes = 0
    for file in files:
        text = read_text(file)
        corpus_parts.append(text)
        total_bytes += len(text.encode("utf-8", errors="ignore"))
    corpus = "\n".join(corpus_parts)

    print(f"Ship Pretty static scan: {len(files)} files, {total_bytes:,} bytes")
    print("Reminder: these are inspection prompts, not automatic design failures.\n")

    findings = 0
    for signal in SIGNALS:
        count = len(signal.pattern.findall(corpus))
        if count >= signal.threshold:
            findings += 1
            print(f"[{signal.name}] {count} hits (threshold {signal.threshold})")
            print(f"  {signal.note}\n")

    generic_hits: list[str] = []
    for pattern in GENERIC_COPY:
        generic_hits.extend(match.group(0) for match in pattern.finditer(corpus))

    if generic_hits:
        findings += 1
        sample = ", ".join(repr(x[:60]) for x in generic_hits[:5])
        print(f"[generic-marketing-copy] {len(generic_hits)} hits")
        print("  Generic marketing language can make a polished UI feel interchangeable.")
        print(f"  Samples: {sample}\n")

    if findings == 0:
        print("No threshold-level static signals found. The render still needs visual review.")
    else:
        print(f"{findings} signal group(s) worth inspecting in the rendered UI.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
