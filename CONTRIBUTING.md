# Contributing

English (current) | [简体中文](CONTRIBUTING.zh-CN.md)

Thank you for helping develop the Computational Structural Biology Platform. This repository is intended for long-term collaboration between lab members, external contributors, and Codex-assisted workflows. Contributions should improve reproducibility, protect unpublished research, and keep workflow behavior transparent.

## Privacy And Anonymization

All contributors must follow [docs/PRIVACY_AND_ANONYMIZATION_POLICY.md](docs/PRIVACY_AND_ANONYMIZATION_POLICY.md). Public documentation, examples, scripts, templates, and knowledge records must not contain personal names, usernames, server names, internal project names, unpublished project identifiers, or machine-specific paths. Use generic placeholders such as `user`, `researcher`, `server`, `compute_server`, `example_project`, `example_dataset`, `example_protein`, and `example_ligand`.

## Contribution Principles

- Keep the public repository free of private paths, server names, credentials, unpublished project results, raw trajectories, docking outputs, and large binary data.
- Prefer modular changes under `modules/<module_name>/` instead of broad edits across unrelated workflows.
- Update documentation, registries, schemas, and tests in the same pull request as workflow changes.
- Treat verified templates as protected release artifacts. Do not overwrite them directly.
- Record reusable lessons in the knowledge system, but anonymize all project-specific scientific details.

## Branch Strategy

Use `main` as the release-ready branch. It should always pass validation and remain safe for public GitHub distribution.

Recommended branch names:

- `feature/<module>-<short-topic>` for new capabilities.
- `fix/<module>-<short-topic>` for bug fixes.
- `docs/<short-topic>` for documentation-only changes.
- `registry/<short-topic>` for registry updates.
- `experiment/<module>-<short-topic>` for exploratory work that is not yet active.

Avoid direct commits to `main` unless a maintainer is preparing a small release-only update. Experimental workflows should remain marked `experimental` or `planned` until validated.

## Pull Request Workflow

1. Create or identify an issue, case, or development need.
2. Create a branch from the latest `main`.
3. Make scoped changes using the existing architecture.
4. Update module documentation and registries when behavior changes.
5. Run validation:

```bash
python3 tests/quick_validate_all.py
```

6. Check for private content before opening a PR:

```bash
rg -n "PERSONAL_PATH_PATTERN|PRIVATE_HOST_PATTERN|PRIVATE_PROJECT_PATTERN|CREDENTIAL_PATTERN" .
find . -type f -size +20M -print
```

7. Open a pull request with a concise summary, validation output, and risk notes.
8. Request review from at least one maintainer or module owner.
9. Address review comments with follow-up commits.
10. Merge only after validation passes and public-safety checks are clean.

## PR Checklist

Include this checklist in substantial PRs:

```markdown
- [ ] Scope is limited to one module, policy area, or release task.
- [ ] `python3 tests/quick_validate_all.py` passes.
- [ ] New or changed scripts have syntax checks.
- [ ] Module registry was updated if module status changed.
- [ ] Software registry and dependency matrix were updated if dependencies changed.
- [ ] Verified templates were not overwritten directly.
- [ ] No raw trajectories, docking outputs, PDBQT results, credentials, or private project data were added.
- [ ] Documentation was updated for users and developers.
```

## Module Development

Each module lives in `modules/<module_name>/` and must include:

- `README.md`
- `workflow_rules.md`
- `install.md`
- `dependencies.md`
- `input_schema.md`
- `output_schema.md`
- `known_issues.md`
- `scripts/`
- `templates/`
- `examples/`
- `tests/`

Active modules must be registered in `references/module_registry.md`, mapped to dependencies in `references/software_dependency_matrix.md`, and covered by validation.

## Verified Template Protection

Verified templates are read-only. If a workflow template needs to change, create a new versioned directory or file, document why the change was made, update references, and validate the new template before marking it active. Never silently replace a verified template because that breaks reproducibility.

## Knowledge System

Reusable workflow lessons belong in `knowledge/`. Project-specific observations, unpublished scientific interpretations, private protein names, and raw output-derived conclusions must not be published. Use anonymized cases and generalizable lessons only.

## Release Workflow

Before a release:

1. Run repository validation.
2. Run public-safety scans.
3. Update `CHANGELOG.md`.
4. Confirm `.gitignore` excludes raw outputs and private folders.
5. Confirm no unresolved `PRIVATE_REMOVE_BEFORE_UPLOAD` items remain in release audit reports.
6. Commit with a release-oriented message.
7. Push only to the correct GitHub remote.
8. Create a GitHub release or tag after review.

See [docs/DEVELOPER_GUIDE.md](docs/DEVELOPER_GUIDE.md) for the full development process.
