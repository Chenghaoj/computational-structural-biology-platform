#!/usr/bin/env python3
"""Update researcher decision fields for an existing case without editing annotations silently."""

from __future__ import annotations

import argparse
import csv
from datetime import date
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skill-root", default=Path(__file__).resolve().parents[2])
    parser.add_argument("--case-id", required=True)
    parser.add_argument("--decision", required=True)
    parser.add_argument("--notes", default="")
    parser.add_argument("--fix-status", default="")
    args = parser.parse_args()

    registry = Path(args.skill_root) / "knowledge" / "global_case_registry.csv"
    rows = list(csv.DictReader(registry.open()))
    fieldnames = rows[0].keys() if rows else []
    found = False
    for row in rows:
        if row.get("case_id") == args.case_id:
            found = True
            row["researcher_decision"] = args.decision
            if args.notes:
                previous = row.get("researcher_notes", "")
                row["researcher_notes"] = (previous + " | " if previous else "") + args.notes
            if args.fix_status:
                row["fix_status"] = args.fix_status
            row["last_updated"] = date.today().isoformat()
    if not found:
        raise SystemExit(f"Case not found: {args.case_id}")

    with registry.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
