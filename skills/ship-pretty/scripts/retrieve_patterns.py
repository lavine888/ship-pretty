#!/usr/bin/env python3
"""Retrieve transferable design decisions from Ship Pretty's Taste Library."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


DEFAULT_LIBRARY = Path(__file__).resolve().parents[1] / "references" / "taste-library" / "patterns.json"
STOP_WORDS = {"a", "an", "and", "are", "for", "has", "in", "is", "of", "on", "or", "the", "to", "with"}


def tokens(value: str) -> set[str]:
    return {token for token in re.findall(r"[a-z0-9]+", value.lower()) if token not in STOP_WORDS}


def split_terms(values: list[str]) -> list[str]:
    terms: list[str] = []
    for value in values:
        terms.extend(term.strip() for term in value.split(",") if term.strip())
    return terms


def score_pattern(pattern: dict[str, Any], query: str, contexts: list[str], dimension: str | None) -> tuple[float, list[str]]:
    query_lower = query.lower()
    query_tokens = tokens(query)
    matched: list[str] = []
    score = 0.0
    for signal in pattern["signals"]:
        signal_lower = signal.lower()
        signal_tokens = tokens(signal)
        overlap = query_tokens & signal_tokens
        if signal_lower in query_lower:
            score += 5.0
            matched.append(signal)
        elif overlap:
            score += min(3.0, 1.0 + len(overlap) * 0.75)
            matched.append(signal)
    signal_text = " ".join(pattern["signals"]).lower()
    for context in contexts:
        context_lower = context.lower()
        if context_lower in signal_text:
            score += 2.5
            matched.append(f"context:{context}")
        elif context_lower in pattern["dimension"].lower():
            score += 0.5
    if dimension and dimension == pattern["dimension"]:
        score += 2.0
    return score, matched


def retrieve(library: list[dict[str, Any]], issues: list[str], contexts: list[str], dimension: str | None, limit: int) -> list[dict[str, Any]]:
    query = " ".join(issues)
    ranked: list[dict[str, Any]] = []
    for pattern in library:
        score, matched = score_pattern(pattern, query, contexts, dimension)
        if score < 2.0:
            continue
        ranked.append({"score": round(score, 2), "matched_signals": matched, "pattern": pattern})
    ranked.sort(key=lambda item: (-item["score"], item["pattern"]["id"]))
    return ranked[:limit]


def render_text(matches: list[dict[str, Any]]) -> str:
    if not matches:
        return "No confident pattern match. Record pattern: none and continue with the quality-gate reasoning."
    lines = ["MATCHED PATTERNS"]
    for index, item in enumerate(matches, start=1):
        pattern = item["pattern"]
        lines.extend(
            [
                f"{index}. {pattern['id']}  score={item['score']}",
                f"   Problem: {pattern['problem']}",
                f"   Decision: {pattern['decision']}",
                f"   Matched signals: {', '.join(item['matched_signals'])}",
                f"   QA: {' | '.join(pattern['qa'])}",
            ]
        )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--issues", action="append", required=True, help="Observed issue or comma-separated issue signals; repeatable")
    parser.add_argument("--context", action="append", default=[], help="Product or task context; repeatable")
    parser.add_argument("--dimension", choices=["layout", "hierarchy", "components", "interaction", "motion", "responsive", "microcopy"])
    parser.add_argument("--limit", type=int, default=3)
    parser.add_argument("--library", type=Path, default=DEFAULT_LIBRARY)
    parser.add_argument("--format", choices=["text", "json"], default="text")
    args = parser.parse_args()
    if args.limit < 1:
        parser.error("--limit must be positive")
    library = json.loads(args.library.read_text(encoding="utf-8"))
    issues = split_terms(args.issues)
    contexts = split_terms(args.context)
    matches = retrieve(library, issues, contexts, args.dimension, args.limit)
    if args.format == "json":
        print(json.dumps({"query": issues, "context": contexts, "matches": matches}, indent=2, ensure_ascii=False))
    else:
        print(render_text(matches))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
