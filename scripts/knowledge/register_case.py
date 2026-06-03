#!/usr/bin/env python3
"""Append a case to global_case_registry.csv and optionally pending_cases.csv."""

from __future__ import annotations

import argparse
import csv
from datetime import date
from pathlib import Path


REGISTRY_COLUMNS = [
    "case_id", "date_added", "module", "submodule", "project",
    "input_file_or_system", "symptom", "error_message", "root_cause",
    "auto_fix_attempted", "auto_fix_allowed", "fix_method", "fix_status",
    "researcher_review_required", "researcher_decision", "researcher_notes",
    "reusable_rule_created", "reusable_script_created", "linked_reference_file",
    "linked_script", "future_action", "confidence", "last_updated",
]

PENDING_COLUMNS = [
    "case_id", "date_added", "module", "submodule", "project",
    "input_file_or_system", "symptom", "error_message", "why_pending",
    "researcher_decision_needed", "linked_case_report", "status", "last_updated",
]


def append_row(path: Path, columns: list[str], row: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    exists = path.exists()
    with path.open("a", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        if not exists or path.stat().st_size == 0:
            writer.writeheader()
        writer.writerow({col: row.get(col, "") for col in columns})


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skill-root", default=Path(__file__).resolve().parents[2])
    parser.add_argument("--case-id", required=True)
    parser.add_argument("--module", required=True)
    parser.add_argument("--submodule", default="")
    parser.add_argument("--project", default="")
    parser.add_argument("--input", default="")
    parser.add_argument("--symptom", required=True)
    parser.add_argument("--error-message", default="")
    parser.add_argument("--root-cause", default="")
    parser.add_argument("--confidence", default="Low")
    parser.add_argument("--pending", action="store_true")
    parser.add_argument("--decision-needed", default="")
    parser.add_argument("--case-report", default="")
    args = parser.parse_args()

    today = date.today().isoformat()
    root = Path(args.skill_root)
    registry_row = {
        "case_id": args.case_id,
        "date_added": today,
        "module": args.module,
        "submodule": args.submodule,
        "project": args.project,
        "input_file_or_system": args.input,
        "symptom": args.symptom,
        "error_message": args.error_message,
        "root_cause": args.root_cause,
        "auto_fix_attempted": "No",
        "auto_fix_allowed": "Unknown",
        "fix_status": "pending_review" if args.pending else "documented",
        "researcher_review_required": "Yes" if args.pending else "",
        "future_action": args.decision_needed,
        "confidence": args.confidence,
        "last_updated": today,
    }
    append_row(root / "knowledge" / "global_case_registry.csv", REGISTRY_COLUMNS, registry_row)

    if args.pending:
        pending_row = {
            "case_id": args.case_id,
            "date_added": today,
            "module": args.module,
            "submodule": args.submodule,
            "project": args.project,
            "input_file_or_system": args.input,
            "symptom": args.symptom,
            "error_message": args.error_message,
            "why_pending": "unsafe_auto_fix_or_insufficient_evidence",
            "researcher_decision_needed": args.decision_needed,
            "linked_case_report": args.case_report,
            "status": "pending",
            "last_updated": today,
        }
        append_row(root / "knowledge" / "pending_review" / "pending_cases.csv", PENDING_COLUMNS, pending_row)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
