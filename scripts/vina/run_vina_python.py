#!/usr/bin/env python
import argparse
import csv
import math
from pathlib import Path

from vina import Vina


def parse_xyz(text):
    vals = [float(x) for x in text.replace(",", " ").split()]
    if len(vals) != 3:
        raise argparse.ArgumentTypeError("expected three numbers, for example: '10 20 30'")
    return vals


def best_affinity_from_pdbqt(path):
    for line in Path(path).read_text(errors="ignore").splitlines():
        if line.startswith("REMARK VINA RESULT:"):
            parts = line.split()
            return float(parts[3])
    return math.nan


def main():
    parser = argparse.ArgumentParser(description="Batch docking with AutoDock Vina Python API.")
    parser.add_argument("--receptor", default="examples/vina_project/receptors/receptor.pdbqt")
    parser.add_argument("--ligand-dir", default="examples/vina_project/ligands_pdbqt")
    parser.add_argument("--out-dir", default="examples/vina_project/results")
    parser.add_argument("--center", type=parse_xyz, required=True, help="Docking box center: 'x y z'")
    parser.add_argument("--size", type=parse_xyz, default=[24.0, 24.0, 24.0], help="Docking box size: 'x y z'")
    parser.add_argument("--exhaustiveness", type=int, default=8)
    parser.add_argument("--num-modes", type=int, default=9)
    parser.add_argument("--cpu", type=int, default=0)
    parser.add_argument("--seed", type=int, default=20260529)
    parser.add_argument("--limit", type=int, default=0, help="For testing, dock only first N ligands")
    args = parser.parse_args()

    receptor = Path(args.receptor).expanduser()
    ligand_dir = Path(args.ligand_dir).expanduser()
    out_dir = Path(args.out_dir).expanduser()
    out_dir.mkdir(parents=True, exist_ok=True)
    log_dir = out_dir.parent / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)

    ligands = sorted(ligand_dir.glob("*.pdbqt"))
    if args.limit > 0:
        ligands = ligands[: args.limit]
    if not receptor.is_file():
        raise SystemExit(f"Missing receptor pdbqt: {receptor}")
    if not ligands:
        raise SystemExit(f"No ligand pdbqt files found in: {ligand_dir}")

    summary_path = out_dir / "vina_summary.csv"
    with summary_path.open("w", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["ligand", "affinity_kcal_mol", "output_pdbqt", "status", "message"],
        )
        writer.writeheader()

        v = Vina(sf_name="vina", cpu=args.cpu, seed=args.seed)
        v.set_receptor(str(receptor))
        v.compute_vina_maps(center=args.center, box_size=args.size)

        for ligand in ligands:
            out_pdbqt = out_dir / f"{ligand.stem}_out.pdbqt"
            try:
                v.set_ligand_from_file(str(ligand))
                v.dock(exhaustiveness=args.exhaustiveness, n_poses=args.num_modes)
                v.write_poses(str(out_pdbqt), n_poses=args.num_modes, overwrite=True)
                affinity = best_affinity_from_pdbqt(out_pdbqt)
                writer.writerow(
                    {
                        "ligand": ligand.name,
                        "affinity_kcal_mol": affinity,
                        "output_pdbqt": str(out_pdbqt),
                        "status": "OK",
                        "message": "",
                    }
                )
                print(f"OK {ligand.name} {affinity}", flush=True)
            except Exception as exc:
                writer.writerow(
                    {
                        "ligand": ligand.name,
                        "affinity_kcal_mol": "",
                        "output_pdbqt": str(out_pdbqt),
                        "status": "ERROR",
                        "message": repr(exc),
                    }
                )
                print(f"ERROR {ligand.name}: {exc!r}", flush=True)

    print(f"Summary: {summary_path}")


if __name__ == "__main__":
    main()
