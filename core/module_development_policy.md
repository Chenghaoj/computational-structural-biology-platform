# Module Development Policy

Every workflow module lives under `modules/<module_name>/` and contains `README.md`, `workflow_rules.md`, `install.md`, `dependencies.md`, `input_schema.md`, `output_schema.md`, `known_issues.md`, plus `scripts/`, `templates/`, `examples/`, and `tests/`.

New modules start as `planned` or `experimental`. They become `active` only after validation passes and the registries are updated. Existing working paths should be preserved or documented in migration notes.
