# Versioning Policy

This repository uses versioning to protect reproducibility across Codex skill behavior, workflow modules, scripts, templates, and public releases.

## Versioning Goals

- Keep public releases reproducible.
- Make workflow changes traceable.
- Prevent silent changes to verified templates.
- Help users understand when a workflow change may affect scientific outputs.

## Release Versioning

Use semantic versioning for public releases when practical:

- `MAJOR`: breaking architecture, workflow defaults, or output contract changes.
- `MINOR`: new modules, new workflows, or backward-compatible capabilities.
- `PATCH`: bug fixes, documentation updates, safety checks, and compatibility improvements.

Pre-release labels may be used for early work, such as `v0.2.0-alpha.1`.

## Module Versioning

Each active module should document major behavior changes in its `README.md` or `known_issues.md`. If a module changes inputs, outputs, defaults, or scientific assumptions, update its documentation and record the change in `CHANGELOG.md`.

## Template Versioning

Verified templates are immutable. To update a verified template:

1. Create a new versioned template path, such as `templates/gromacs/v2/` or `modules/<module>/templates/v2/`.
2. Document what changed and why.
3. Add validation evidence.
4. Update references only after review.
5. Keep the prior version available unless it contains a public-safety problem.

Never overwrite a verified template directly.

## Script Versioning

Scripts should expose behavior through documented variables or command-line options. Avoid changing defaults in ways that silently alter scientific results. If defaults change, document the migration path and release note.

## Registry Versioning

Changes to `references/module_registry.md`, `references/software_registry.md`, and `references/software_dependency_matrix.md` should happen in the same pull request as the module or dependency change.

## Changelog Policy

Update `CHANGELOG.md` for:

- New modules.
- Module status changes.
- Workflow default changes.
- Dependency policy changes.
- Verified template updates.
- Public-safety or sanitization changes.
- Breaking changes.

## Release Tags

Recommended release flow:

```bash
git checkout main
git pull
git status
python3 tests/quick_validate_all.py
git tag -a vX.Y.Z -m "Release vX.Y.Z"
git push origin main
git push origin vX.Y.Z
```

Only tag after validation and final public-safety review.
