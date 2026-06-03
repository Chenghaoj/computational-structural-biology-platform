# Contributing

Contributions must be public-safe and modular.

## Module Development

Read `core/module_development_policy.md`, `core/validation_policy.md`, `core/versioning_policy.md`, and `core/verified_template_policy.md` before changing modules.

Every module must contain `README.md`, `workflow_rules.md`, `install.md`, `dependencies.md`, `input_schema.md`, `output_schema.md`, `known_issues.md`, and `scripts/`, `templates/`, `examples/`, `tests/`.

## Safety

Do not commit private paths, server names, credentials, raw trajectories, docking outputs, PDBQT result files, or unpublished project-specific results.

Verified templates are read-only. Create a new versioned directory for changes.

## Validation

```bash
python3 tests/quick_validate_all.py
```
