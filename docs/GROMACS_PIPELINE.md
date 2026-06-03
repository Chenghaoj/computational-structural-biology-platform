# GROMACS Pipeline

The public pipeline script supports full-background explicit-water MD:

```bash
INPUT_PDB=protein.pdb WORKDIR=$PWD GMX_BIN=gmx MDP_DIR=mdp nohup bash run_explicit_water_pipeline.sh > pipeline_console.log 2>&1 & echo $! > pipeline.pid
```

Do not use `-maxwarn` by default. If `grompp` fails, inspect the corresponding `logs/*grompp*.log` file and decide whether the issue is informational, acceptable with rationale, fix-required, or a blocker.
