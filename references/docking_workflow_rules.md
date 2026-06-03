# Docking Workflow Rules

Use this module for receptor preparation and AutoDock Vina workflows.

Recommended staged workflow:

1. Choose receptor frame/protein state with documented provenance.
2. Export protein-only receptor PDB.
3. Design a box from a known pocket, interface, or researcher-approved blind-docking design.
4. Prepare receptor PDBQT with Meeko or an equivalent reviewed workflow.
5. Convert ligands to suitable formats with chemistry-aware tools.
6. Run a single-ligand test.
7. Run a small confirmed batch.
8. Run larger screens only after clean validation.
9. Write logs and summary CSV outputs.

Do not replace unsupported ligand atoms or alter chemistry automatically.
