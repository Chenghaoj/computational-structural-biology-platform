# GROMACS Workflow Rules

## Warning Policy

Never default to `-maxwarn`. For every `grompp` warning:

1. Capture the exact warning text.
2. Explain the cause.
3. Classify severity: informational, acceptable-with-rationale, fix-required, or blocker.
4. Suggest a fix.
5. Ask before using `-maxwarn`.

## Workflow Execution Modes

- `full_background_pipeline_mode`: generate a complete runnable script for the standard explicit-water workflow, then launch it with `nohup` in the background. This is the default for real MD runs unless stepwise execution is explicitly requested.
- `stepwise_interactive_mode`: run each stage in the foreground. Use this for debugging, teaching, or close inspection.

Recommended launch command:

```bash
nohup bash run_explicit_water_pipeline.sh > pipeline_console.log 2>&1 & echo $! > pipeline.pid
tail -f pipeline_console.log
cat pipeline.pid
ps -fp $(cat pipeline.pid)
```

## Required Run Records

Record machine, working directory, GROMACS version, force field, water model, ion choices, salt concentration, MDP source, exact commands, warnings, output files, GPU/CPU settings, and final status.
