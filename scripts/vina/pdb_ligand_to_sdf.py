#!/usr/bin/env python
from pathlib import Path
import sys

from rdkit import Chem


def main():
    if len(sys.argv) != 3:
        raise SystemExit("Usage: 08_pdb_ligand_to_sdf.py input.pdb output.sdf")
    src = Path(sys.argv[1]).expanduser()
    dst = Path(sys.argv[2]).expanduser()
    dst.parent.mkdir(parents=True, exist_ok=True)

    mol = Chem.MolFromPDBFile(str(src), removeHs=False, sanitize=True)
    if mol is None:
        raise SystemExit(f"RDKit could not read ligand PDB: {src}")
    Chem.AssignStereochemistryFrom3D(mol)
    writer = Chem.SDWriter(str(dst))
    writer.write(mol)
    writer.close()
    print(f"wrote {dst}")
    print(f"atoms={mol.GetNumAtoms()} bonds={mol.GetNumBonds()}")


if __name__ == "__main__":
    main()
