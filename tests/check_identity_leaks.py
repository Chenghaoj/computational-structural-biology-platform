#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SCAN_TARGETS = [
    "README.md",
    "README.zh-CN.md",
    "CONTRIBUTING.md",
    "CONTRIBUTING.zh-CN.md",
    "docs",
    "references",
    "knowledge",
    "scripts",
    "templates",
    "examples",
    "SKILL.md",
]


def term(*parts: str) -> str:
    return "".join(parts)


KNOWN_USERS = [term("h", "c"), term("c", "h", "j")]
KNOWN_PERSONS = [term("Hao", "jie")]
KNOWN_SERVERS = [term("de", "ll"), term("go", "oxi")]
KNOWN_PROJECTS = [term("CK", "AP4"), term("DR", "P1")]
KNOWN_PATHS = [term("/Users/", "h", "c"), term("/home/", "c", "h", "j")]

PATTERNS = {
    "hardcoded_personal_home": [
        re.compile(r"/Users/[A-Za-z0-9._-]+"),
        re.compile(r"/home/[A-Za-z0-9._-]+"),
        *(re.compile(re.escape(value)) for value in KNOWN_PATHS),
    ],
    "known_user_identifier": [
        *(re.compile(r"\b" + re.escape(value) + r"\b", re.IGNORECASE) for value in KNOWN_USERS),
    ],
    "known_person_identifier": [
        *(re.compile(r"\b" + re.escape(value) + r"\b", re.IGNORECASE) for value in KNOWN_PERSONS),
    ],
    "known_server_identifier": [
        *(re.compile(r"\b" + re.escape(value) + r"\b", re.IGNORECASE) for value in KNOWN_SERVERS),
    ],
    "known_project_identifier": [
        *(re.compile(r"\b" + re.escape(value) + r"\b", re.IGNORECASE) for value in KNOWN_PROJECTS),
    ],
    "credential_marker": [
        re.compile(re.escape(term("BEGIN ", "OPEN", "SSH"))),
        re.compile(re.escape(term("PRIVATE", " KEY"))),
        re.compile(term("api", "[_-]?", "key"), re.IGNORECASE),
        re.compile(term("pass", "word"), re.IGNORECASE),
        re.compile(term("sec", "ret"), re.IGNORECASE),
    ],
}

EXCLUDED_DIRS = {
    ".git",
    "_private_excluded_from_release",
    "__pycache__",
}

EXCLUDED_FILES = {
    "IDENTITY_AUDIT_REPORT.md",
    "IDENTITY_CLEANUP_REPORT.md",
}


def iter_files() -> list[Path]:
    files: list[Path] = []
    for target in SCAN_TARGETS:
        path = ROOT / target
        if not path.exists():
            continue
        if path.is_file():
            files.append(path)
            continue
        for item in path.rglob("*"):
            if not item.is_file():
                continue
            rel_parts = set(item.relative_to(ROOT).parts)
            if rel_parts & EXCLUDED_DIRS:
                continue
            files.append(item)
    return sorted(set(files))


def main() -> int:
    findings: list[str] = []
    for path in iter_files():
        rel = path.relative_to(ROOT).as_posix()
        if rel in EXCLUDED_FILES:
            continue
        text = path.read_text(errors="ignore")
        for category, patterns in PATTERNS.items():
            for pattern in patterns:
                for match in pattern.finditer(text):
                    line = text.count("\n", 0, match.start()) + 1
                    findings.append(f"{rel}:{line}: {category}")
    if findings:
        print("Identity leak check failed:")
        print("\n".join(findings))
        return 1
    print("identity leak check: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
