#!/usr/bin/env python
from pathlib import Path
import sys

pdb = Path(sys.argv[1]).expanduser() if len(sys.argv) > 1 else Path("examples/receptor.pdb")
coords = []

for line in pdb.read_text(errors="ignore").splitlines():
    if line.startswith(("ATOM  ", "HETATM")):
        try:
            coords.append((float(line[30:38]), float(line[38:46]), float(line[46:54])))
        except ValueError:
            pass

if not coords:
    raise SystemExit(f"No atom coordinates parsed from {pdb}")

mins = [min(c[i] for c in coords) for i in range(3)]
maxs = [max(c[i] for c in coords) for i in range(3)]
center = [(mins[i] + maxs[i]) / 2 for i in range(3)]
size = [(maxs[i] - mins[i]) for i in range(3)]

print(f"PDB: {pdb}")
print(f"Atoms parsed: {len(coords)}")
print("Min:    " + " ".join(f"{x:.3f}" for x in mins))
print("Max:    " + " ".join(f"{x:.3f}" for x in maxs))
print("Center: " + " ".join(f"{x:.3f}" for x in center))
print("Size:   " + " ".join(f"{x:.3f}" for x in size))
print("Note: this is the whole receptor bounding box, not a binding pocket box.")
