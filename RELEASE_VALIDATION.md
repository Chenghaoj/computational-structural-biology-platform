# Release Validation

## Checks Run

- `python3 tests/quick_validate_all.py`
- `bash -n scripts/gromacs/run_explicit_water_pipeline.sh`
- `bash -n scripts/gromacs/check_pipeline_status.sh`
- `bash -n scripts/receptor_prep/prepare_receptor_with_meeko.sh`
- `PYTHONPYCACHEPREFIX=/private/tmp/csb_release_pycache python3 -m compileall -q scripts tests`
- private path / credential / server-name scan excluding `_private_excluded_from_release/`
- disallowed output extension scan excluding `_private_excluded_from_release/`
- large file scan excluding `.git/` and `_private_excluded_from_release/`
- `git status`

## Results

| Check | Result | Notes |
|---|---|---|
| Skill validation | PASS | `quick_validate_all: OK` |
| Shell syntax | PASS | GROMACS and receptor-prep shell scripts passed `bash -n`. |
| Python syntax | PASS | `scripts/` and `tests/` compiled with pycache redirected to `/private/tmp`. |
| Private paths / credentials | PASS | No unresolved publishable hits. Validator pattern definitions are intentionally excluded. |
| Raw MD / docking outputs | PASS | No `.xtc`, `.trr`, `.tpr`, `.edr`, `.cpt`, `.gro`, `.pdbqt`, `.log`, `.out`, `.err`, archives, or `.env` files found in publishable tree. |
| Large files | PASS | No files larger than 1 MB in publishable tree. |
| Private excluded folder | PASS | `_private_excluded_from_release/` is ignored by `.gitignore` and not staged for release. |
| Final release audit | PASS | `FINAL_RELEASE_AUDIT.md` has no unresolved PRIVATE_REMOVE_BEFORE_UPLOAD items. |

## Remote

Configured remote:

```text
origin https://github.com/Chenghaoj/computational-structural-biology-platform.git
```

The remote appears to match the requested repository name.
