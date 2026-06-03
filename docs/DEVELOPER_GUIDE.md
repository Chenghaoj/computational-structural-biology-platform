# Developer Guide

English (current) | [简体中文](DEVELOPER_GUIDE.zh-CN.md)

This guide explains how to develop the Computational Structural Biology Platform as a public, multi-developer Codex skill. It is written for new lab members, external contributors, and maintainers who need a reliable path from idea to validated module.

## Repository Baseline

The current architecture is organized around modular, reviewable workflows:

- `SKILL.md` is the entry point for Codex skill behavior.
- `core/` contains development, validation, versioning, and template policies.
- `modules/` contains workflow modules such as GROMACS MD, Vina screening, PDB standardization, AF3 preparation, and trajectory analysis.
- `references/` contains registries, dependency matrices, workflow rules, and software policies.
- `scripts/` contains shared automation scripts.
- `templates/` contains reusable workflow templates.
- `knowledge/` contains anonymized cases, known workflow lessons, and review queues.
- `docs/` contains public-facing and developer documentation.
- `tests/` contains repository validation utilities.

## Current Active Modules

- `af3_cif_preparation`
- `pdb_standardization`
- `gromacs_stability_md`
- `vina_screening`
- `trajectory_analysis`

## Reserved Future Modules

- `haddock3`
- `smd`
- `membrane_md`
- `remd`
- `ligand_protein_md`
- `ion_analysis`
- `mmpbsa`

Future modules should start as `planned` or `experimental` and become `active` only after validation, documentation, and review.

## Development Lifecycle

1. Define the scientific or workflow problem.
2. Decide whether it belongs in an existing module or a new module.
3. Create a branch using the branch naming rules in `CONTRIBUTING.md`.
4. Implement the smallest coherent change.
5. Update registries and documentation.
6. Add or update examples and tests.
7. Run validation.
8. Open a pull request with review notes.
9. Merge after review and successful validation.

## Branch Strategy

`main` is the public release branch. Keep it valid, portable, and free of private data.

Use short, descriptive branches:

- `feature/gromacs-background-pipeline`
- `fix/vina-dependency-check`
- `docs/module-policy`
- `registry/add-haddock3`
- `experiment/membrane-md-prototype`

Experimental branches may contain incomplete work, but experimental code merged into `main` must be clearly marked and must not affect active workflows by default.

## Pull Request Workflow

A good pull request includes:

- A short summary of what changed.
- The module or policy area affected.
- Scientific assumptions or workflow assumptions.
- Validation commands and results.
- Any public-safety checks performed.
- Known limitations or follow-up work.

Reviewers should focus on reproducibility, public safety, scientific correctness, portability, and maintainability.

## Adding a New Module

Create `modules/<module_name>/` with the required module skeleton:

```text
modules/<module_name>/
  README.md
  workflow_rules.md
  install.md
  dependencies.md
  input_schema.md
  output_schema.md
  known_issues.md
  scripts/
  templates/
  examples/
  tests/
```

Then update:

- `references/module_registry.md`
- `references/software_registry.md`
- `references/software_dependency_matrix.md`
- `SKILL.md` if Codex routing or workflow behavior changes
- `tests/quick_validate_all.py` if validation rules need to expand

A module should remain `planned` if only installation notes exist, `experimental` if workflows exist but are not validated, and `active` only after validation and review.

## Updating an Existing Module

Before modifying a module:

1. Read its `README.md`, `workflow_rules.md`, `dependencies.md`, and `known_issues.md`.
2. Check whether related cases exist in `knowledge/`.
3. Preserve existing public interfaces unless a breaking change is documented.
4. Add migration notes when paths, inputs, outputs, or defaults change.

## Dependency Policy

Workflows must check required third-party software before execution. A workflow should detect:

- Software availability.
- Executable path.
- Version.
- Required Python package imports where relevant.
- Environment notes or limitations.

If software is missing, explain what is missing, link official installation documentation when available, and ask the user before installing anything. Never silently install software.

## Template Policy

Verified templates are reproducibility anchors. Do not overwrite them directly. Create a new versioned template path, document the reason, and update references only after validation.

## Knowledge and Case Management

The knowledge system records reusable lessons, common failures, manual decisions, and workflow improvements. It must not contain unpublished research findings or private outputs. Put unresolved or project-specific notes in a private local location, not the public repository.

Use cases when:

- A workflow required a manual scientific decision.
- A failure mode may recur.
- A dependency or environment issue was solved.
- A template or workflow policy changed because of experience.

## Validation

Run the quick validator before opening a pull request:

```bash
python3 tests/quick_validate_all.py
```

Also run syntax checks for changed shell and Python scripts where applicable:

```bash
bash -n path/to/script.sh
python3 -m py_compile path/to/script.py
```

For workflow scripts that execute external tools, validate syntax and dependency detection even when the external software is not available locally.

## Release Process

A release is ready when:

- Validation passes.
- Public-safety scans are clean.
- `CHANGELOG.md` is updated.
- New modules and dependencies are registered.
- Documentation reflects current behavior.
- No private data or raw computational outputs are staged.

Do not push or publish if audit reports contain unresolved private items.
