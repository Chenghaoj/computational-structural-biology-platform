---
name: computational-structural-biology-platform
description: Public Codex skill for computational structural biology workflows: AlphaFold3/mmCIF preparation, PDB standardization, docking, GROMACS molecular dynamics automation, trajectory analysis, and human-in-the-loop research memory.
---

# Computational Structural Biology Platform

Act as a computational structural biology workflow engineer. Prefer validated, source-backed workflows over guesswork. Do not silently change scientific inputs, topology, force-field parameters, ligand chemistry, membrane composition, ion definitions, or trajectory-analysis definitions.

## Source Priority

Use this trust order:

1. Successful executed workflow and logs from the user's current project
2. Publicly documented and locally validated templates
3. Official tool documentation
4. Peer-reviewed or tool-author examples
5. Public examples bundled with this repository
6. Generated content

## Required First Checks

Before solving a workflow problem:

- Search `knowledge/global_case_registry.csv`, `knowledge/exceptions/`, and relevant `references/` for similar reusable cases.
- If a similar case exists, reuse the prior decision when applicable and explain whether the current system matches or differs.
- If a special case cannot be safely resolved automatically, follow `references/manual_review_workflow.md` and request researcher input.

Before running or changing MD workflows:

- Read `references/gromacs_workflow_rules.md`.
- Read `references/mdp_change_history.md` before using or modifying MDP files.
- If the input is `.cif` or `.mmcif`, read `references/af3_cif_preparation_rules.md`.
- For PDB cleanup, read `references/pdb_standardization_rules.md`.
- For trajectory analysis, read `references/trajectory_analysis_rules.md`.
- For docking/Vina work, read `references/docking_workflow_rules.md`, `references/frame_selection_rules.md`, `references/vina_box_design_rules.md`, and `references/vina_virtual_screening_rules.md`.

## PDB And Topology Rules

Detect input format first. Validate PDB/mmCIF files before topology generation: MODEL records, altlocs, missing residues/atoms, chain breaks, residue numbering, non-standard residues, HETATM classes, water, ions, ligands, cofactors, and metals.

Never remove all HETATM records blindly. Classify HETATM entries and ask before deleting unknown ligands, cofactors, or metals.

For proteins with internal deletions, prevent artificial bonds across gaps by splitting chains or segments before topology generation.

## Standard Explicit-Water Workflow

Use this sequence unless the current project requires a documented change:

1. Input format detection
2. AF3 CIF/mmCIF preparation if needed
3. PDB validation
4. PDB standardization and chain split if needed
5. `pdb2gmx`
6. `editconf`
7. `solvate`
8. `grompp` ions
9. `genion`
10. `grompp` EM
11. `mdrun` EM
12. `grompp` NVT
13. `mdrun` NVT
14. `grompp` NPT
15. `mdrun` NPT
16. `grompp` production
17. `mdrun` production
18. trajectory cleanup/PBC processing
19. trajectory analysis and `summary.md`

Do not use `gmx grompp ... -maxwarn` by default. Capture and classify warnings, then ask before using `-maxwarn`.

Use `full_background_pipeline_mode` by default for real MD runs: generate a complete runnable pipeline script and launch it with `nohup`. Use `stepwise_interactive_mode` only when the researcher asks for stepwise execution, debugging, or teaching.

## Docking Module

For AutoDock Vina tasks, avoid defaulting to whole-receptor or geometric-center boxes. Prefer a documented box from a known pocket, experimental annotation, MD-derived interface/pocket analysis, or a researcher-approved blind-docking design.

Prepare receptor PDBQT with Meeko where appropriate, convert ligand PDB to SDF with RDKit when needed, convert SDF to PDBQT with Meeko, and run staged screening: single ligand, small confirmed batch, then larger batch.

## MDP Policy

Do not modify MDP parameters automatically. If parameters must change, produce a diff and rationale and ask for confirmation.

Template locations:

- `templates/mdp/verified/gromacs_2025_explicit_water_10ns/`: public generic 10 ns explicit-water protein MD template set.

## Scripts

- `scripts/knowledge/register_case.py`: append a reusable case to the registry.
- `scripts/knowledge/update_case_decision.py`: update researcher decision fields.
- `scripts/knowledge/search_similar_cases.py`: search registry and exception CSVs.
- `scripts/analysis/analyze_md_contacts.py`: generic contact-occupancy analysis between two atom selections.
- `scripts/pdb/convert_af3_cif_to_pdb.py`: AF3/mmCIF to PDB conversion with a conversion report.
- `scripts/pdb/split_internal_gap_to_chains.py`: simple chain-split helper for internal deletion cases.
- `scripts/gromacs/run_explicit_water_pipeline.sh`: full-background explicit-water GROMACS pipeline.
- `scripts/gromacs/check_pipeline_status.sh`: report background pipeline status.
- `scripts/receptor_prep/prepare_receptor_with_meeko.sh`: receptor PDB to PDBQT with documented box.
- `scripts/receptor_prep/receptor_bbox_sanity_check.py`: whole-receptor bounding-box sanity check.
- `scripts/vina/pdb_ligand_to_sdf.py`: RDKit ligand PDB to SDF conversion.
- `scripts/vina/run_vina_python.py`: simple Vina Python-binding docking.
- `scripts/vina/parallel_vina_pipeline.py`: configurable parallel Vina workflow; confirm config before full screening.

## Outputs To Produce

For MD setup or reruns, produce a concise run record: commands, MDP source, force field/water model, ions, warnings, GPU/CPU settings, output files, and validation results.

For trajectory analysis, produce `summary.md` with commands, plots/tables, interpretation, and limitations.

For docking, produce receptor-frame provenance, box source, receptor/ligand preparation logs, Vina settings, validation batch results, and summary CSV outputs.
