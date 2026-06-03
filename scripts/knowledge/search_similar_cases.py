#!/usr/bin/env python3
"""Search the skill knowledge registry and exception CSVs for similar cases."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


def rows_from_csv(path: Path):
    if not path.exists():
        return []
    with path.open(newline="", errors="ignore") as handle:
        return list(csv.DictReader(handle))


def score_row(row: dict, terms: list[str]) -> int:
    text = " ".join(str(v) for v in row.values()).lower()
    return sum(1 for term in terms if term in text)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query", nargs="+", help="Search terms, e.g. RDKit valence Vina")
    parser.add_argument("--skill-root", default=Path(__file__).resolve().parents[2])
    parser.add_argument("--limit", type=int, default=10)
    args = parser.parse_args()

    root = Path(args.skill_root)
    terms = [q.lower() for q in args.query]
    sources = [root / "knowledge" / "global_case_registry.csv"]
    sources.extend(sorted((root / "knowledge" / "exceptions").glob("*.csv")))

    hits = []
    for source in sources:
        for row in rows_from_csv(source):
            score = score_row(row, terms)
            if score:
                hits.append((score, source.relative_to(root), row))

    hits.sort(key=lambda item: item[0], reverse=True)
    for score, source, row in hits[: args.limit]:
        case_id = row.get("case_id") or row.get("exception_id") or ""
        module = row.get("module", "")
        symptom = row.get("symptom", "")
        root_cause = row.get("root_cause", "")
        print(f"[score={score}] {source} {case_id} {module}")
        print(f"  symptom: {symptom}")
        print(f"  root_cause: {root_cause}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
