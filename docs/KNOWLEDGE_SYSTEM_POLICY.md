# Knowledge System Policy

English (current) | [简体中文](KNOWLEDGE_SYSTEM_POLICY.zh-CN.md)

The knowledge system lets the skill remember reusable workflow lessons while protecting unpublished research and private lab information.

## Purpose

The knowledge system records:

- Common failure modes.
- Verified fixes.
- Manual researcher decisions.
- Environment-specific issues that may recur.
- Workflow improvement cases.
- Known limitations and pending review items.

It should improve future workflows without exposing private scientific results.

## Public-Safe Knowledge Only

Public repository knowledge must be anonymized and reusable. Do not publish:

- Unpublished protein-specific results.
- Raw docking scores tied to private projects.
- Raw MD trajectories or analysis outputs.
- Private project names or internal hypotheses.
- Server names, usernames, absolute personal paths, or SSH details.
- Credentials or private environment configuration.

If a lesson comes from a private project, generalize it before adding it. For example, record "GROMACS grompp failed because ion topology was not included" instead of naming the private project and output files.

## Case Management System

Use cases to record reusable decisions and lessons. A case should include:

- Case ID.
- Date.
- Module.
- Status.
- Problem.
- Decision.
- Reusable lesson.
- Validation evidence.
- Reviewer or researcher annotation when relevant.

Recommended statuses:

- `open`
- `pending_review`
- `verified`
- `superseded`
- `rejected`

Cases that need human scientific judgment should remain `pending_review` until a researcher approves them.

## Researcher Annotation Policy

Researcher annotations are used when human expertise determines the correct workflow choice. Examples include:

- Selecting a biologically relevant chain or assembly.
- Choosing protonation, ligand, cofactor, membrane, or ion treatment.
- Deciding whether a structure cleanup operation is scientifically acceptable.
- Interpreting whether a simulation or docking run is meaningful.

Annotations should separate facts from interpretation. They should also mark whether the decision is project-specific or reusable.

## Knowledge Database Locations

Common locations include:

- `knowledge/global_case_registry.csv`
- `knowledge/exceptions/`
- `knowledge/pending_review/`
- module-specific `known_issues.md`
- module-specific tests or examples when a case becomes a reusable validation fixture

Do not add private raw data to these locations.

## Installation and Environment Knowledge

The skill may remember common installation issues and environment-specific fixes, but installation instructions must reference official documentation when available. Do not encode private machine assumptions as universal requirements.

## From Case to Policy

When a case reveals a general workflow improvement:

1. Add or update the case entry.
2. Generalize the lesson.
3. Update module `known_issues.md` or `workflow_rules.md`.
4. Update shared references if the lesson affects multiple modules.
5. Add validation if possible.
6. Mark the case `verified` after review.

## Review and Cleanup

Periodically review knowledge entries for stale workarounds, private details, and superseded recommendations. Superseded cases should remain traceable but should point to the newer policy or fix.
