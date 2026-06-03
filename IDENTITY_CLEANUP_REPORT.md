# Identity Cleanup Report

English (current)

## Summary

Zero Personal Identity Policy support was added across the repository. Public-facing documentation now requires generic placeholders for people, servers, projects, datasets, proteins, ligands, and paths.

## Items Found

| category | result |
|---|---|
| Personal names | no unresolved public findings |
| Usernames | no unresolved public findings |
| Server names and hostnames | no unresolved public findings |
| Machine-specific paths | no unresolved public findings |
| Unpublished project identifiers | no unresolved public findings |
| Credential markers | no unresolved public findings |
| Laboratory-specific wording | generalized in contributor-facing documentation |

## Replacements Made

| original category | public replacement policy |
|---|---|
| real person name | `user` or `researcher` |
| researcher name | `researcher` |
| server or machine name | `server` or `compute_server` |
| unpublished project protein | `example_protein` or `example_protein_A` |
| unpublished project partner | `example_partner` or `example_protein_B` |
| specific project | `example_project` |
| specific dataset | `example_dataset` |
| ligand from unpublished work | `example_ligand` |
| machine-specific path | `/path/to/project` |

## Files Updated

- `docs/PRIVACY_AND_ANONYMIZATION_POLICY.md`
- `tests/check_identity_leaks.py`
- `tests/quick_validate_all.py`
- `CONTRIBUTING.md`
- `CONTRIBUTING.zh-CN.md`
- `docs/CODE_REVIEW_POLICY.md`
- `IDENTITY_AUDIT_REPORT.md`
- `IDENTITY_CLEANUP_REPORT.md`

## Remaining Review Items

No unresolved identity-specific items remain in the scanned public repository areas.

Future releases should run:

```bash
python3 tests/check_identity_leaks.py
python3 tests/quick_validate_all.py
```
