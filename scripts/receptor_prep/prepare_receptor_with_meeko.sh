#!/usr/bin/env bash
set -euo pipefail
if [[ $# -lt 9 ]]; then
  cat >&2 <<'USAGE'
Usage:
  prepare_receptor_with_meeko.sh receptor.pdb output_base center_x center_y center_z size_x size_y size_z log.txt

Writes output_base.pdbqt via mk_prepare_receptor.py. Review receptor protonation,
waters/ions/ligands, and box source before running.
USAGE
  exit 2
fi
receptor=$1; out_base=$2; cx=$3; cy=$4; cz=$5; sx=$6; sy=$7; sz=$8; log=${9:-prepare_receptor.log}
mkdir -p "$(dirname "$out_base")" "$(dirname "$log")"
mk_prepare_receptor.py --read_pdb "$receptor" -o "$out_base" -p -a \
  --box_center "$cx" "$cy" "$cz" \
  --box_size "$sx" "$sy" "$sz" \
  -v > "$log" 2>&1
