# AF3/mmCIF Preparation Rules

Use this reference when an MD or docking input starts as AlphaFold3 `.cif` or `.mmcif`.

- Preserve chain IDs, residue IDs, insertion codes, atom names, and model provenance when converting.
- Treat converted PDB files as candidates, not final MD inputs.
- Validate missing residues, missing atoms, pLDDT/confidence context, chain breaks, ligands, cofactors, metals, glycans, and waters before downstream topology generation.
- Generate a conversion report that records input file, output file, chain/residue counts, warnings, and unresolved issues.
