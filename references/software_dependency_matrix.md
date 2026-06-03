# Software Dependency Matrix

## af3_cif_preparation
requires: gemmi, biopython

## pdb_standardization
requires: python3
optional: gemmi, biopython

## gromacs_stability_md
requires: gromacs

## vina_screening
requires: vina, rdkit, meeko, autogrid4, gemmi, prody

## trajectory_analysis
requires: MDAnalysis, numpy

## planned modules
haddock3, smd, membrane_md, remd, ligand_protein_md, ion_analysis, mmpbsa require module-specific dependency registration before workflow support.
