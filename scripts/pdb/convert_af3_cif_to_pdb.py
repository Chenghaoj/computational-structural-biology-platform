#!/usr/bin/env python3
"""Convert AlphaFold3/mmCIF atom_site coordinates to PDB with validation report.

Default behavior preserves chain IDs and residue numbering where possible. It does
not delete atoms and does not renumber unless --renumber is explicitly requested.
"""
from __future__ import annotations

import argparse
import shlex
from collections import Counter, defaultdict
from pathlib import Path

STANDARD_AA = {
    "ALA","ARG","ASN","ASP","CYS","GLN","GLU","GLY","HIS","ILE",
    "LEU","LYS","MET","PHE","PRO","SER","THR","TRP","TYR","VAL",
    "MSE","SEC","PYL",
}
WATER = {"HOH", "WAT", "SOL", "H2O"}
IONS = {"NA", "CL", "K", "CA", "MG", "ZN", "FE", "MN", "CU", "CO", "NI"}
TWO_LETTER = {"CL", "BR", "NA", "MG", "ZN", "FE", "MN", "CU", "CO", "NI", "LI", "AL", "SI", "SE"}


def parse_mmcif_loop(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    lines = path.read_text(errors="replace").splitlines()
    rows: list[dict[str, str]] = []
    columns: list[str] = []
    i = 0
    while i < len(lines):
        if lines[i].strip() != "loop_":
            i += 1
            continue
        i += 1
        cols = []
        while i < len(lines) and lines[i].strip().startswith("_"):
            cols.append(lines[i].strip())
            i += 1
        if not cols or not all(c.startswith("_atom_site.") for c in cols):
            continue
        columns = cols
        n = len(cols)
        while i < len(lines):
            stripped = lines[i].strip()
            if not stripped or stripped == "#":
                i += 1
                break
            if stripped == "loop_" or stripped.startswith("_"):
                break
            try:
                tokens = shlex.split(lines[i], posix=True)
            except ValueError:
                tokens = lines[i].split()
            i += 1
            while len(tokens) < n and i < len(lines):
                more = lines[i].strip()
                if not more or more == "#" or more == "loop_" or more.startswith("_"):
                    break
                try:
                    tokens.extend(shlex.split(lines[i], posix=True))
                except ValueError:
                    tokens.extend(lines[i].split())
                i += 1
            if len(tokens) >= n:
                rows.append({cols[j].split(".", 1)[1]: tokens[j] for j in range(n)})
        if rows:
            return columns, rows
    raise SystemExit(f"No _atom_site loop found in {path}")


def pick(row: dict[str, str], *keys: str, default: str = "") -> str:
    for key in keys:
        val = row.get(key, "")
        if val not in {"", ".", "?"}:
            return val
    return default


def infer_element(atom_name: str, resname: str, explicit: str = "") -> str:
    if explicit and explicit not in {".", "?"}:
        return explicit.strip().title()[:2]
    letters = "".join(ch for ch in atom_name.strip() if ch.isalpha()).upper()
    if not letters:
        return ""
    rn = resname.strip().upper()
    if len(letters) >= 2 and letters[:2] in TWO_LETTER and rn in TWO_LETTER:
        return letters[:2].title()
    if len(letters) >= 2 and letters[:2] in {"CL", "BR"}:
        return letters[:2].title()
    return letters[0]


def fmt_atom_name(name: str, element: str) -> str:
    name = name[:4]
    if len(name) == 4:
        return name
    if len(element.strip()) == 1:
        return f" {name:<3}"[:4]
    return f"{name:<4}"[:4]


def safe_int(text: str) -> int | None:
    try:
        return int(float(text))
    except Exception:
        return None


def classify_residue(resname: str, group: str) -> str:
    rn = resname.upper()
    if group.upper() == "ATOM" and rn in STANDARD_AA:
        return "protein"
    if rn in WATER:
        return "water"
    if rn in IONS:
        return "ion_or_metal"
    if rn in STANDARD_AA:
        return "protein_like"
    return "nonstandard_or_ligand"


def convert(args: argparse.Namespace) -> None:
    _, rows = parse_mmcif_loop(args.input)
    atom_rows = [r for r in rows if pick(r, "Cartn_x")]
    if not atom_rows:
        raise SystemExit("No coordinate atom rows found")

    chain_map: dict[str, str] = {}
    chain_counts = Counter()
    residue_seen = defaultdict(list)
    components = Counter()
    warnings: list[str] = []
    pdb_lines: list[str] = []
    serial = 1
    renum_counter: dict[str, int] = defaultdict(int)
    renum_map: dict[tuple[str, str, str], int] = {}

    for row in atom_rows:
        group = pick(row, "group_PDB", default="ATOM")
        atom_name = pick(row, "auth_atom_id", "label_atom_id", default="X")
        resname = pick(row, "auth_comp_id", "label_comp_id", default="UNK").upper()
        chain_raw = pick(row, "auth_asym_id", "label_asym_id", default="A")
        seq_raw = pick(row, "auth_seq_id", "label_seq_id", default="1")
        ins = pick(row, "pdbx_PDB_ins_code", default=" ")
        if ins in {".", "?"}:
            ins = " "
        alt = pick(row, "label_alt_id", default=" ")
        if alt in {".", "?"}:
            alt = " "
        if chain_raw not in chain_map:
            chain_map[chain_raw] = chain_raw[0] if chain_raw else "A"
            if len(chain_raw) != 1:
                warnings.append(f"Chain ID '{chain_raw}' mapped to one-character PDB chain '{chain_map[chain_raw]}'.")
        chain = chain_map[chain_raw]
        if args.renumber:
            key = (chain, seq_raw, resname)
            if key not in renum_map:
                renum_counter[chain] += 1
                renum_map[key] = renum_counter[chain]
            resid = renum_map[key]
        else:
            parsed = safe_int(seq_raw)
            if parsed is None:
                warnings.append(f"Non-integer residue id '{seq_raw}' in chain {chain_raw}; sequential numbering used for that residue.")
                key = (chain, seq_raw, resname)
                if key not in renum_map:
                    renum_counter[chain] += 1
                    renum_map[key] = renum_counter[chain]
                resid = renum_map[key]
            else:
                resid = parsed
        try:
            x = float(pick(row, "Cartn_x")); y = float(pick(row, "Cartn_y")); z = float(pick(row, "Cartn_z"))
        except ValueError as exc:
            warnings.append(f"Skipped atom with invalid coordinates: {row}")
            continue
        occ = float(pick(row, "occupancy", default="1.00") or 1.0)
        bfac = float(pick(row, "B_iso_or_equiv", default="0.00") or 0.0)
        elem = infer_element(atom_name, resname, pick(row, "type_symbol"))
        rec = "HETATM" if group.upper() == "HETATM" else "ATOM"
        atom_field = fmt_atom_name(atom_name, elem)
        pdb_lines.append(f"{rec:<6}{serial:5d} {atom_field}{alt[:1]}{resname:>3} {chain[:1]}{resid:4d}{ins[:1]}   {x:8.3f}{y:8.3f}{z:8.3f}{occ:6.2f}{bfac:6.2f}          {elem:>2}")
        serial += 1
        chain_counts[chain] += 1
        residue_key = (chain, resid, resname)
        if not residue_seen[chain] or residue_seen[chain][-1] != residue_key:
            residue_seen[chain].append(residue_key)
        components[(group.upper(), resname, classify_residue(resname, group))] += 1

    args.output.write_text("\n".join(pdb_lines) + "\nEND\n")

    report = [f"# CIF to PDB Conversion Report", "", f"Input: `{args.input}`", f"Output: `{args.output}`", f"Atoms written: `{len(pdb_lines)}`", f"Renumber requested: `{args.renumber}`", ""]
    report += ["## Chain mapping", ""]
    for original, mapped in chain_map.items():
        report.append(f"- CIF chain `{original}` -> PDB chain `{mapped}`; atoms `{chain_counts[mapped]}`")
    report += ["", "## Residue ranges and gaps", ""]
    large_gap_threshold = args.large_gap
    for chain in sorted(residue_seen):
        residues = residue_seen[chain]
        by_num = []
        for _, resid, resname in residues:
            if not by_num or by_num[-1][0] != resid:
                by_num.append((resid, resname))
        nums = [r for r, _ in by_num]
        report.append(f"### Chain {chain}")
        report.append(f"- residues observed: `{len(by_num)}`")
        if nums:
            report.append(f"- min/max residue id: `{min(nums)}`-`{max(nums)}`")
        gaps = []
        for (a, _), (b, _) in zip(by_num, by_num[1:]):
            if b > a + 1:
                gaps.append((a, b, b-a-1))
        if gaps:
            for a, b, missing in gaps:
                label = "LARGE" if missing >= large_gap_threshold else "gap"
                report.append(f"- {label}: `{a}` -> `{b}` missing `{missing}` residue numbers")
        else:
            report.append("- no internal residue-number gaps detected")
        report.append("")
    report += ["## Components", ""]
    for (group, resname, cls), count in sorted(components.items()):
        report.append(f"- `{group}` `{resname}` classified as `{cls}`: atoms `{count}`")
    report += ["", "## Warnings", ""]
    if args.renumber:
        warnings.append("Residues were renumbered because --renumber was requested; document mapping before pdb2gmx.")
    if any(cls != "protein" for (_, _, cls), _ in components.items()):
        warnings.append("Non-protein or non-standard components are present or suspected; classify before GROMACS preparation.")
    warnings.append("PDB conversion may lose AF3 confidence annotations and mmCIF metadata. Keep the original CIF.")
    for warning in warnings:
        report.append(f"- WARNING: {warning}")
    args.report.write_text("\n".join(report) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path, help="Input .cif/.mmcif")
    parser.add_argument("--output", required=True, type=Path, help="Output .pdb")
    parser.add_argument("--report", required=True, type=Path, help="Markdown conversion report")
    parser.add_argument("--renumber", action="store_true", help="Renumber residues sequentially per PDB chain; off by default")
    parser.add_argument("--large-gap", type=int, default=10, help="Gap size threshold for LARGE gap warnings")
    args = parser.parse_args()
    if args.input.suffix.lower() not in {".cif", ".mmcif"}:
        raise SystemExit("Input must end with .cif or .mmcif")
    convert(args)

if __name__ == "__main__":
    main()
