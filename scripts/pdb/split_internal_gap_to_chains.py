#!/usr/bin/env python3
"""Split a PDB chain into A/B/C-style chain segments by residue ranges without changing coordinates."""
import argparse
from pathlib import Path

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('input', type=Path)
    ap.add_argument('output', type=Path)
    ap.add_argument('--c-start', type=int, required=True, help='Residues >= this value become chain C when currently in chain B')
    ap.add_argument('--c-end', type=int, required=True)
    args = ap.parse_args()
    out=[]
    for raw in args.input.read_text(errors='replace').splitlines(True):
        line=raw
        if line.startswith(('ATOM  ','HETATM','TER   ')) and len(line)>=26:
            try: resid=int(line[22:26])
            except ValueError: out.append(line); continue
            if line[21]=='B' and args.c_start <= resid <= args.c_end:
                line=line[:21]+'C'+line[22:]
        out.append(line)
    args.output.write_text(''.join(out))
if __name__ == '__main__': main()
