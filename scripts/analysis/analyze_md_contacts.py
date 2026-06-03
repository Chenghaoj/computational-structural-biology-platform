#!/usr/bin/env python3
"""Generic contact-occupancy analysis between two MDAnalysis atom selections.

This public script intentionally avoids project-specific chain names, residue ranges,
or unpublished systems. Provide explicit selections for your system.
"""
from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from pathlib import Path

import numpy as np

try:
    import MDAnalysis as mda
    from MDAnalysis.lib.distances import capped_distance
except ImportError as exc:
    raise SystemExit("Install MDAnalysis and numpy before running this script") from exc


def residue_label(residue):
    segid = getattr(residue, "segid", "") or "SEG"
    return f"{segid}:{residue.resid}:{residue.resname}"


def main():
    parser = argparse.ArgumentParser(description="Contact occupancy between two atom selections.")
    parser.add_argument("--topology", required=True, help="Topology/reference file, e.g. npt.gro or system.pdb")
    parser.add_argument("--trajectory", required=True, help="Trajectory file, e.g. md_centered_nopbc.xtc")
    parser.add_argument("--selection-a", required=True, help="MDAnalysis selection for group A")
    parser.add_argument("--selection-b", required=True, help="MDAnalysis selection for group B")
    parser.add_argument("--cutoff", type=float, default=4.5, help="Heavy-atom cutoff in Angstrom")
    parser.add_argument("--occupancy-threshold", type=float, default=0.5, help="Report pairs at or above this occupancy")
    parser.add_argument("--stride", type=int, default=1)
    parser.add_argument("--out-csv", default="contact_occupancy.csv")
    args = parser.parse_args()

    u = mda.Universe(args.topology, args.trajectory)
    group_a = u.select_atoms(args.selection_a)
    group_b = u.select_atoms(args.selection_b)
    if len(group_a) == 0 or len(group_b) == 0:
        raise SystemExit("One or both selections are empty")

    a_heavy = group_a.select_atoms("not name H* and not type H")
    b_heavy = group_b.select_atoms("not name H* and not type H")
    if len(a_heavy) == 0 or len(b_heavy) == 0:
        raise SystemExit("One or both heavy-atom selections are empty")

    a_atom_to_res = {atom.index: atom.residue for atom in a_heavy}
    b_atom_to_res = {atom.index: atom.residue for atom in b_heavy}
    counts = defaultdict(int)
    min_dist = defaultdict(lambda: np.inf)
    frames = 0

    for ts in u.trajectory[:: args.stride]:
        pairs, distances = capped_distance(a_heavy.positions, b_heavy.positions, max_cutoff=args.cutoff, box=ts.dimensions, return_distances=True)
        seen = {}
        for (ia, ib), dist in zip(pairs, distances):
            ra = residue_label(a_atom_to_res[a_heavy[int(ia)].index])
            rb = residue_label(b_atom_to_res[b_heavy[int(ib)].index])
            key = (ra, rb)
            if dist < seen.get(key, np.inf):
                seen[key] = float(dist)
        for key, dist in seen.items():
            counts[key] += 1
            min_dist[key] = min(min_dist[key], dist)
        frames += 1

    rows = []
    for (ra, rb), count in counts.items():
        occ = count / frames if frames else 0.0
        if occ >= args.occupancy_threshold:
            rows.append({"residue_a": ra, "residue_b": rb, "occupancy": occ, "frames_present": count, "frames_total": frames, "min_distance_A": min_dist[(ra, rb)]})
    rows.sort(key=lambda r: (-r["occupancy"], r["residue_a"], r["residue_b"]))

    out = Path(args.out_csv)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["residue_a", "residue_b", "occupancy", "frames_present", "frames_total", "min_distance_A"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"wrote {out} rows={len(rows)} frames={frames}")


if __name__ == "__main__":
    main()
