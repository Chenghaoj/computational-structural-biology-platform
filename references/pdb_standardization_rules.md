# PDB Standardization Rules

Before `pdb2gmx`, inspect and classify. Do not blindly delete records.

Required checks:

- Multiple MODEL records
- Chain IDs and residue numbering
- Internal deletions and chain breaks
- Missing atoms/residues
- Altlocs
- Non-standard residues
- HETATM classes: water, ion, ligand, cofactor, metal, glycan, unknown
- Existing hydrogens and protonation state assumptions

For proteins with internal deletions, prevent artificial bonds across missing segments by splitting chains or applying a documented topology strategy.
