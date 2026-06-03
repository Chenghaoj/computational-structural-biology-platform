#!/usr/bin/env python
import argparse
import csv
import json
import math
import os
import subprocess
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path


def run(cmd, log_path=None):
    if log_path is None:
        subprocess.run(cmd, check=True)
    else:
        with open(log_path, "w") as handle:
            subprocess.run(cmd, stdout=handle, stderr=subprocess.STDOUT, check=True)


def parse_affinity(path):
    path = Path(path)
    if not path.is_file():
        return math.nan
    for line in path.read_text(errors="ignore").splitlines():
        if line.startswith("REMARK VINA RESULT:"):
            return float(line.split()[3])
    return math.nan


def ligand_name_from_pdb(path):
    return Path(path).stem


def prepare_one_ligand(args):
    pdb_path, sdf_dir, pdbqt_dir, log_dir = args
    pdb_path = Path(pdb_path)
    name = ligand_name_from_pdb(pdb_path)
    sdf_path = Path(sdf_dir) / f"{name}.sdf"
    pdbqt_path = Path(pdbqt_dir) / f"{name}.pdbqt"
    log_path = Path(log_dir) / f"prepare_ligand_{name}.log"
    if pdbqt_path.is_file() and pdbqt_path.stat().st_size > 0:
        return {"ligand": name, "status": "SKIP", "message": "pdbqt exists", "pdbqt": str(pdbqt_path)}

    try:
        from rdkit import Chem

        sdf_path.parent.mkdir(parents=True, exist_ok=True)
        pdbqt_path.parent.mkdir(parents=True, exist_ok=True)
        mol = Chem.MolFromPDBFile(str(pdb_path), removeHs=False, sanitize=True)
        if mol is None:
            raise RuntimeError(f"RDKit could not read {pdb_path}")
        Chem.AssignStereochemistryFrom3D(mol)
        writer = Chem.SDWriter(str(sdf_path))
        writer.write(mol)
        writer.close()
        run(["mk_prepare_ligand.py", "-i", str(sdf_path), "-o", str(pdbqt_path)], log_path=log_path)
        return {"ligand": name, "status": "OK", "message": "", "pdbqt": str(pdbqt_path)}
    except Exception as exc:
        return {"ligand": name, "status": "ERROR", "message": repr(exc), "pdbqt": str(pdbqt_path)}


def dock_one_ligand(args):
    receptor_pdbqt, ligand_pdbqt, out_dir, box_center, box_size, exhaustiveness, num_modes, cpu, seed = args
    from vina import Vina

    ligand_pdbqt = Path(ligand_pdbqt)
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_pdbqt = out_dir / f"{ligand_pdbqt.stem}_out.pdbqt"
    if out_pdbqt.is_file() and out_pdbqt.stat().st_size > 0:
        affinity = parse_affinity(out_pdbqt)
        if not math.isnan(affinity):
            return {
                "ligand": ligand_pdbqt.name,
                "affinity_kcal_mol": affinity,
                "output_pdbqt": str(out_pdbqt),
                "status": "SKIP",
                "message": "output exists",
            }

    try:
        v = Vina(sf_name="vina", cpu=cpu, seed=seed)
        v.set_receptor(str(receptor_pdbqt))
        v.compute_vina_maps(center=box_center, box_size=box_size)
        v.set_ligand_from_file(str(ligand_pdbqt))
        v.dock(exhaustiveness=exhaustiveness, n_poses=num_modes)
        v.write_poses(str(out_pdbqt), n_poses=num_modes, overwrite=True)
        affinity = parse_affinity(out_pdbqt)
        return {
            "ligand": ligand_pdbqt.name,
            "affinity_kcal_mol": affinity,
            "output_pdbqt": str(out_pdbqt),
            "status": "OK",
            "message": "",
        }
    except Exception as exc:
        return {
            "ligand": ligand_pdbqt.name,
            "affinity_kcal_mol": "",
            "output_pdbqt": str(out_pdbqt),
            "status": "ERROR",
            "message": repr(exc),
        }


def load_config(project):
    config_path = Path(project) / "vina_config.json"
    return json.loads(config_path.read_text())


def select_ligands(paths, limit):
    paths = sorted(paths)
    if limit and limit > 0:
        return paths[:limit]
    return paths


def write_rows(path, rows, fieldnames):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def cmd_prepare_receptors(config):
    project = Path(config["project_dir"])
    logs = project / "logs"
    logs.mkdir(parents=True, exist_ok=True)
    for receptor in config["receptors"]:
        out_base = Path(receptor["prepared_pdbqt"]).with_suffix("")
        out_base.parent.mkdir(parents=True, exist_ok=True)
        box = receptor["box"]
        log_path = logs / f"prepare_receptor_{receptor['name']}.log"
        if Path(receptor["prepared_pdbqt"]).is_file():
            print(f"SKIP receptor exists: {receptor['prepared_pdbqt']}", flush=True)
            continue
        cmd = [
            "mk_prepare_receptor.py",
            "--read_pdb",
            receptor["source_pdb"],
            "-o",
            str(out_base),
            "-p",
            "-a",
            "--box_center",
            *(str(x) for x in box["center"]),
            "--box_size",
            *(str(x) for x in box["size"]),
            "-v",
        ]
        print(f"Preparing receptor {receptor['name']}", flush=True)
        run(cmd, log_path=log_path)
        print(f"Prepared receptor: {receptor['prepared_pdbqt']}", flush=True)


def cmd_prepare_ligands(config, limit, workers):
    project = Path(config["project_dir"])
    ligand_cfg = config["ligands"]
    pdb_paths = select_ligands(Path(ligand_cfg["source_pdb_dir"]).glob("*.pdb"), limit)
    logs = project / "logs" / "ligand_prepare"
    logs.mkdir(parents=True, exist_ok=True)
    tasks = [(str(p), ligand_cfg["sdf_dir"], ligand_cfg["pdbqt_dir"], str(logs)) for p in pdb_paths]
    rows = []
    print(f"Preparing {len(tasks)} ligands with {workers} workers", flush=True)
    with ProcessPoolExecutor(max_workers=workers) as pool:
        futures = [pool.submit(prepare_one_ligand, task) for task in tasks]
        for i, future in enumerate(as_completed(futures), start=1):
            row = future.result()
            rows.append(row)
            print(f"[ligand {i}/{len(tasks)}] {row['status']} {row['ligand']} {row['message']}", flush=True)
    write_rows(project / "logs" / f"prepare_ligands_limit{limit or 'all'}.csv", rows, ["ligand", "status", "message", "pdbqt"])
    errors = [r for r in rows if r["status"] == "ERROR"]
    if errors:
        raise SystemExit(f"Ligand preparation had {len(errors)} errors")


def cmd_dock(config, receptor_name, limit, workers, cpu_per_worker):
    receptor = next((r for r in config["receptors"] if r["name"].startswith(receptor_name) or r["name"] == receptor_name), None)
    if receptor is None:
        raise SystemExit(f"Unknown receptor: {receptor_name}")
    ligand_dir = Path(config["ligands"]["pdbqt_dir"])
    ligands = select_ligands(ligand_dir.glob("*.pdbqt"), limit)
    if not ligands:
        raise SystemExit(f"No ligand pdbqt files found in {ligand_dir}")

    vina_cfg = config["vina"]
    out_dir = Path(receptor["results_dir"])
    summary = out_dir / "vina_summary.csv"
    tasks = [
        (
            receptor["prepared_pdbqt"],
            str(lig),
            str(out_dir),
            receptor["box"]["center"],
            receptor["box"]["size"],
            int(vina_cfg["exhaustiveness"]),
            int(vina_cfg["num_modes"]),
            int(cpu_per_worker),
            int(vina_cfg["seed"]),
        )
        for lig in ligands
    ]
    rows = []
    print(f"Docking {len(tasks)} ligands against {receptor['name']} with {workers} workers, cpu_per_worker={cpu_per_worker}", flush=True)
    with ProcessPoolExecutor(max_workers=workers) as pool:
        futures = [pool.submit(dock_one_ligand, task) for task in tasks]
        for i, future in enumerate(as_completed(futures), start=1):
            row = future.result()
            rows.append(row)
            print(f"[dock {receptor['name']} {i}/{len(tasks)}] {row['status']} {row['ligand']} {row['affinity_kcal_mol']} {row['message']}", flush=True)
    rows.sort(key=lambda r: (r["status"] == "ERROR", float(r["affinity_kcal_mol"]) if r["affinity_kcal_mol"] != "" else 9999, r["ligand"]))
    write_rows(summary, rows, ["ligand", "affinity_kcal_mol", "output_pdbqt", "status", "message"])
    errors = [r for r in rows if r["status"] == "ERROR"]
    if errors:
        raise SystemExit(f"Docking had {len(errors)} errors for {receptor['name']}")
    print(f"Summary: {summary}", flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", default="examples/vina_project")
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("prepare-receptors")
    p_lig = sub.add_parser("prepare-ligands")
    p_lig.add_argument("--limit", type=int, default=0)
    p_lig.add_argument("--workers", type=int, default=8)
    p_dock = sub.add_parser("dock")
    p_dock.add_argument("--receptor", required=True, help="Receptor name from vina_config.json")
    p_dock.add_argument("--limit", type=int, default=0)
    p_dock.add_argument("--workers", type=int, default=8)
    p_dock.add_argument("--cpu-per-worker", type=int, default=1)
    args = parser.parse_args()

    config = load_config(args.project)
    os.makedirs(Path(args.project) / "logs", exist_ok=True)

    if args.cmd == "prepare-receptors":
        cmd_prepare_receptors(config)
    elif args.cmd == "prepare-ligands":
        cmd_prepare_ligands(config, args.limit, args.workers)
    elif args.cmd == "dock":
        cmd_dock(config, args.receptor, args.limit, args.workers, args.cpu_per_worker)


if __name__ == "__main__":
    main()
