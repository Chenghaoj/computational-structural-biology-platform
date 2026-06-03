# Code Review Policy

Code review protects scientific reproducibility, public-release safety, and long-term maintainability.

## Review Priorities

Reviewers should prioritize:

1. Public-safety risks.
2. Scientific or workflow correctness.
3. Reproducibility and logging.
4. Dependency and environment handling.
5. Module architecture consistency.
6. Test coverage and validation.
7. Documentation quality.

Style issues matter, but they should not distract from correctness and safety.

## Required Review For

A maintainer or module owner should review:

- New modules.
- Active workflow behavior changes.
- Dependency installation logic.
- Verified template additions.
- Release preparation changes.
- Knowledge-system policy changes.
- Any change touching public-safety audit behavior.

## Public-Safety Review

Run the identity leak check before approval:

```bash
python3 tests/check_identity_leaks.py
```


PRs must not include:

- Personal paths such as `/Users/<name>` or `/home/<name>`.
- Server hostnames or SSH details.
- Access tokens, credentials, or private environment files.
- Raw MD trajectories or production outputs.
- Docking result outputs or PDBQT result files.
- Unpublished project-specific scientific results.
- Large binary files that are not required for documentation.

Use repository scans before approval:

```bash
rg -n "PERSONAL_PATH_PATTERN|PRIVATE_HOST_PATTERN|CREDENTIAL_PATTERN|SSH_PATTERN" .
find . -type f -size +20M -print
```

## Workflow Review

For workflow scripts, check that they:

- Validate inputs before execution.
- Detect required software before running.
- Record environment information where relevant.
- Use non-interactive execution when expected.
- Stop on failure.
- Preserve logs for failed steps.
- Avoid unsafe automatic retries.
- Avoid machine-specific assumptions.

## Scientific Review

Scientific assumptions should be explicit. Reviewers should ask for clarification when a workflow chooses force fields, solvent models, ion concentrations, docking parameters, structure cleanup rules, or trajectory analysis thresholds without documentation.

Human researcher decisions should be recorded when they affect interpretation or workflow choices.

## Review Outcomes

Use these outcomes:

- `approve`: ready to merge.
- `request changes`: must fix before merge.
- `comment`: non-blocking feedback or question.
- `needs researcher review`: scientific decision requires human confirmation.
- `needs release safety review`: possible private or unpublished content risk.

## Merge Policy

Merge only when:

- Required reviews are complete.
- Validation passes.
- Public-safety checks are clean.
- Documentation and registries are updated.
- Any unresolved limitations are documented.

Prefer squash or merge commits based on maintainer preference, but preserve enough history to understand why workflow behavior changed.
