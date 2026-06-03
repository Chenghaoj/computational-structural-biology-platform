# Privacy And Anonymization Policy

English (current)

This repository follows a Zero Personal Identity Policy for public documentation, examples, scripts, templates, and knowledge records.

## Policy

Public repository content must not include:

- Personal names or researcher identifiers.
- Usernames or account names.
- Server names, hostnames, machine names, or internal infrastructure details.
- Laboratory names or organization-specific identifiers.
- Unpublished project identifiers.
- Internal project names.
- Machine-specific paths.
- Credentials, private environment values, or access details.

## Required Generic Placeholders

Use generic placeholders instead of real identifiers:

| Sensitive content type | Public placeholder |
|---|---|
| Person name | `user` or `researcher` |
| Username | `user` |
| Server or host | `server` or `compute_server` |
| Internal project | `project` or `example_project` |
| Dataset | `dataset` or `example_dataset` |
| Protein name from unpublished work | `example_protein` or `example_protein_A` |
| Binding partner from unpublished work | `example_partner` or `example_protein_B` |
| Ligand name from unpublished work | `example_ligand` |
| Personal path | `/path/to/project` |

## Scientific Examples

Scientific examples may be preserved only when they are generic, public-safe, and not tied to unpublished research. When an example needs a protein, ligand, dataset, or project name, use:

- `example_protein_A`
- `example_protein_B`
- `example_ligand`
- `example_dataset`
- `example_project`

Do not use real unpublished project names in public examples.

## Contributor Requirements

Before opening a pull request, contributors must check for identity leaks:

```bash
python3 tests/check_identity_leaks.py
python3 tests/quick_validate_all.py
```

If the check fails, replace identity-specific content with generic placeholders before review.

## Release Requirements

Before a public release:

1. Run the identity leak check.
2. Run repository validation.
3. Review audit reports for unresolved identity-specific items.
4. Confirm examples use generic placeholders.
5. Confirm no private folders are staged for publication.

Do not publish if unresolved identity-specific content remains.
