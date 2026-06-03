# Module Development Policy

English (current) | [简体中文](MODULE_DEVELOPMENT_POLICY.zh-CN.md)

This policy defines how workflow modules are created, reviewed, validated, and maintained.

## Module Status Labels

Use these labels consistently in `references/module_registry.md`:

- `active`: implemented, documented, validated, and safe for standard use.
- `experimental`: implemented or partially implemented, but still under testing or limited review.
- `planned`: reserved for future development or installation guidance only.
- `deprecated`: retained for compatibility but no longer recommended.

A module must not be marked `active` until required files, registries, dependencies, examples, and validation checks are complete.

## Required Module Structure

Every module must contain:

```text
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

The files may be concise for planned modules, but they must clearly state current status and limitations.

## Module README

`README.md` should explain:

- Purpose and scope.
- Supported workflows.
- Required software.
- Typical inputs and outputs.
- Current status.
- Known limitations.
- Links to related references.

## Workflow Rules

`workflow_rules.md` defines how Codex should operate the module. It should include:

- Preflight checks.
- Required dependencies.
- User approval points.
- Non-interactive behavior where appropriate.
- Failure handling.
- Logging expectations.
- When to stop and ask a human researcher.

## Install Documentation

`install.md` must prefer official software documentation. If suggested commands are included, they should be clearly labeled as recommended examples and should not replace official sources.

## Dependency Documentation

`dependencies.md` must list required and optional software, version expectations, verification commands, and known environment issues.

## Input and Output Schemas

`input_schema.md` and `output_schema.md` must define expected files, formats, naming conventions, required metadata, and validation checks. Avoid accepting ambiguous inputs without documenting assumptions.

## Scripts

Scripts should be portable, explicit, and defensive:

- Use strict shell behavior when appropriate, such as `set -euo pipefail`.
- Validate inputs before execution.
- Check expected outputs after each major step.
- Do not use local usernames, server hostnames, or absolute private paths.
- Do not silently continue after scientific or tool failures.
- Do not use unsafe overrides such as GROMACS `-maxwarn` by default.

## Examples

Examples must be public-safe and small. Do not include raw trajectories, unpublished structures, docking result files, production outputs, or project-specific data.

## Tests

Module tests should check structure, script syntax, input validation, registry consistency, and public-safety constraints. Tests should not require large third-party workloads unless clearly marked as optional integration tests.

## Future Module Expansion Workflow

When adding software or a workflow module:

1. Create `modules/<module_name>/`.
2. Add installation instructions.
3. Add dependency definitions.
4. Add workflow rules.
5. Add input and output schemas.
6. Add known issues.
7. Add examples and tests.
8. Register the module in `references/module_registry.md`.
9. Register software in `references/software_registry.md`.
10. Register dependencies in `references/software_dependency_matrix.md`.
11. Run validation.
12. Request review before marking the module `active`.

## Backward Compatibility

Do not delete old public paths when restructuring working features. Preserve old paths, add migration notes, or provide compatibility wrappers when feasible.
