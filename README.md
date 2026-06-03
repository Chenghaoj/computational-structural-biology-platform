# Computational Structural Biology Platform

A public Codex skill for computational structural biology workflows: structure preparation, docking, molecular dynamics automation, trajectory analysis, and reusable human-in-the-loop research memory.

This repository is a sanitized open-source release. It does not include private project data, raw research outputs, trajectories, docking results, or unpublished scientific conclusions.

## Overview

The Computational Structural Biology Platform helps researchers run safer, more reproducible structural biology workflows with explicit checkpoints for scientific decisions. It emphasizes source-backed rules, careful PDB/mmCIF preparation, validated MD and docking command sequences, and reusable case capture without silently changing scientific inputs.

## Features

- Codex skill entrypoint via `SKILL.md`
- PDB and AlphaFold3/mmCIF preparation helpers
- Explicit-water GROMACS pipeline automation
- AutoDock Vina receptor and ligand preparation helpers
- Generic MD contact-occupancy analysis
- Human-in-the-loop case registry and exception memory
- Public-safe documentation and release reports

## Current Modules

- AlphaFold3 preparation
- mmCIF processing
- PDB standardization
- Protein docking
- AutoDock Vina workflows
- Molecular dynamics
- GROMACS workflow automation
- Trajectory analysis
- Research memory system
- Human-in-the-loop case management

## Future Modules

- Membrane protein MD
- Ligand-protein MD
- Ion-specific analysis
- HADDOCK integration
- ClusPro integration
- MM/PBSA
- DFMD benchmarking

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

## Skill Structure

```text
SKILL.md                       Codex skill instructions
agents/                        Optional skill metadata
scripts/                       Workflow helper scripts
references/                    Public workflow rules and policies
templates/mdp/                 Generic public GROMACS MDP templates
knowledge/                     Public seed case registry and exception schemas
docs/                          User and release documentation
examples/                      Generic example configs
```

## Examples

- `examples/gromacs_pipeline.env`: configurable environment variables for an explicit-water MD run
- `examples/vina_config.example.json`: Vina project configuration template

## Contribution Guide

See `CONTRIBUTING.md`. Contributions should be generic, documented, and free of private data or unpublished results.

## Disclaimer

This project provides workflow automation and documentation. It does not validate the scientific suitability of a force field, ligand protonation state, membrane composition, docking box, or simulation length for your specific system. Researchers are responsible for reviewing all scientific assumptions and complying with software licenses and data-sharing restrictions.

## Languages

- English: `README.md`
- 简体中文: `README.zh-CN.md`

## Multi-Developer Modular Architecture

Modules live under `modules/`, shared policies under `core/`, and quick validation under `tests/quick_validate_all.py`.
