<p align="center">
  🇺🇸 English | 🇨🇳 [简体中文](README.zh-CN.md)
</p>

# Computational Structural Biology Platform

A public Codex skill for computational structural biology workflows: structure preparation, docking, molecular dynamics automation, trajectory analysis, and reusable human-in-the-loop research memory.

This repository is a sanitized open-source release. It does not include private project data, raw research outputs, trajectories, docking results, or unpublished scientific conclusions.

## Overview

Computational Structural Biology Platform helps researchers run safer and more reproducible structural biology workflows with explicit checkpoints for scientific decisions. The project emphasizes source-backed rules, careful PDB/mmCIF preparation, validated MD and docking command sequences, modular software support, and reusable case capture without silently changing scientific inputs.

## Features

- Codex skill entrypoint via `SKILL.md`
- PDB and AlphaFold3/mmCIF preparation helpers
- Explicit-water GROMACS pipeline automation
- AutoDock Vina receptor and ligand preparation helpers
- Generic MD contact-occupancy analysis
- Modular software registry under `modules/` and `references/`
- Human-in-the-loop case registry and exception memory
- Public-safe release checks, identity leak validation, and bilingual documentation

## Current Modules

- `af3_cif_preparation`
- `pdb_standardization`
- `gromacs_stability_md`
- `vina_screening`
- `trajectory_analysis`

These modules map to current public workflows for AlphaFold3 preparation, mmCIF processing, PDB standardization, AutoDock Vina workflows, molecular dynamics setup, GROMACS workflow automation, trajectory analysis, and reusable research memory.

## Planned Modules

- `haddock3`
- `smd`
- `membrane_md`
- `remd`
- `ligand_protein_md`
- `ion_analysis`
- `mmpbsa`

Planned modules remain inactive until they have documentation, dependency rules, examples, tests, and review.

## Installation

Clone the repository:

```bash
git clone https://github.com/<your-org>/computational-structural-biology-platform.git
cd computational-structural-biology-platform
```

Install as a Codex skill by copying or symlinking the repository into your Codex skills directory:

```bash
mkdir -p ~/.codex/skills
ln -s "$PWD" ~/.codex/skills/computational-structural-biology-platform
```

Install runtime tools separately as needed:

- GROMACS for MD workflows
- Python 3.10+
- MDAnalysis and NumPy for trajectory analysis
- RDKit, Meeko, and AutoDock Vina Python bindings for docking workflows

## Usage

Use the skill in Codex:

```text
Use $computational-structural-biology-platform to prepare this PDB for explicit-water GROMACS MD.
```

Run the GROMACS pipeline manually from a project directory after configuring variables:

```bash
cp scripts/gromacs/run_explicit_water_pipeline.sh ./
cp -r templates/mdp/verified/gromacs_2025_explicit_water_10ns ./mdp
INPUT_PDB=protein.pdb GMX_BIN=gmx MDP_DIR=mdp nohup bash run_explicit_water_pipeline.sh > pipeline_console.log 2>&1 & echo $! > pipeline.pid
```

Check status:

```bash
bash scripts/gromacs/check_pipeline_status.sh
```

## Repository Structure

```text
SKILL.md                       Codex skill instructions
core/                          Shared development and validation policies
modules/                       Modular workflow implementations
scripts/                       Workflow helper scripts
references/                    Public workflow rules and registries
templates/mdp/                 Generic public GROMACS MDP templates
knowledge/                     Public seed case registry and exception schemas
docs/                          User and developer documentation
examples/                      Generic example configs
tests/                         Repository validation scripts
```

## Module Development

New modules should follow the standardized structure in `modules/<module_name>/` and must be registered before they become active. Start with the developer documentation:

- [Contributing](CONTRIBUTING.md)
- [Developer Guide](docs/DEVELOPER_GUIDE.md)
- [Module Development Policy](docs/MODULE_DEVELOPMENT_POLICY.md)

Before release, validate module structure, templates, scripts, identity safety, and public documentation:

```bash
python3 tests/check_identity_leaks.py
python3 tests/quick_validate_all.py
```

## Research Memory System

The research memory system records reusable workflow lessons, exceptions, manual decisions, and validated fixes without publishing private research data. Public entries should use generic examples such as `example_protein_A`, `example_protein_B`, `example_ligand`, `example_dataset`, and `example_project`.

Relevant files include:

- `knowledge/global_case_registry.csv`
- `knowledge/exceptions/`
- `knowledge/pending_review/`
- `docs/KNOWLEDGE_SYSTEM_POLICY.md`
- `docs/PRIVACY_AND_ANONYMIZATION_POLICY.md`

## Contributing

Contributions are welcome when they are modular, validated, documented, and public-safe. Please read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request.

All public examples and reports must avoid personal names, server names, internal project names, unpublished identifiers, credentials, and machine-specific paths.

## License

See [LICENSE](LICENSE) for repository license information.

## Disclaimer

This project provides workflow automation and documentation. It does not validate the scientific suitability of a force field, ligand protonation state, membrane composition, docking box, or simulation length for a specific system. Researchers are responsible for reviewing all scientific assumptions and complying with software licenses and data-sharing restrictions.
