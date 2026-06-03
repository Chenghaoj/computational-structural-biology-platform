# Module Registry

Allowed status labels: `active`, `experimental`, `planned`, `deprecated`.

| module_name | software_name | purpose | status | installation_supported | workflow_supported | verified | notes |
|---|---|---|---|---|---|---|---|
| af3_cif_preparation | AlphaFold3 / Gemmi / Biopython | AF3/mmCIF preparation and conversion | active | yes | yes | yes | Maps AF3/mmCIF preparation helpers. |
| pdb_standardization | Python PDB/mmCIF utilities | PDB validation and cleanup | active | yes | yes | yes | HETATM classification and chain/gap handling. |
| gromacs_stability_md | GROMACS | explicit-water protein stability MD | active | yes | yes | yes | Uses full-background pipeline mode. |
| vina_screening | AutoDock Vina / Meeko / RDKit | ligand docking and staged screening | active | yes | yes | yes | Requires strict dependency preflight. |
| trajectory_analysis | MDAnalysis / NumPy | trajectory metrics and contact analysis | active | yes | yes | yes | Configurable analysis workflows. |
| haddock3 | HADDOCK3 | protein docking | planned | yes | no | no | Installation guidance only. |
| smd | GROMACS / PLUMED or equivalent | steered MD | planned | no | no | no | Reserved. |
| membrane_md | GROMACS / membrane builders | membrane protein MD | planned | no | no | no | Reserved. |
| remd | REMD-capable MD engine | replica exchange MD | planned | no | no | no | Reserved. |
| ligand_protein_md | GROMACS / ligand parameterization tools | protein-ligand MD | planned | no | no | no | Reserved. |
| ion_analysis | MDAnalysis / ion analysis tooling | ion/cofactor analysis | planned | no | no | no | Reserved. |
| mmpbsa | gmx_MMPBSA / AmberTools or equivalent | MM/PBSA analysis | planned | no | no | no | Reserved. |
