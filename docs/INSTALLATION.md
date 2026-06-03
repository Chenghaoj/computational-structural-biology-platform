# Installation

Clone this repository and link it into your Codex skills directory:

```bash
git clone https://github.com/<your-org>/computational-structural-biology-platform.git
cd computational-structural-biology-platform
mkdir -p ~/.codex/skills
ln -s "$PWD" ~/.codex/skills/computational-structural-biology-platform
```

Install domain tools separately:

- GROMACS for MD
- Python 3.10+
- MDAnalysis and NumPy for trajectory analysis
- RDKit, Meeko, and Vina Python bindings for docking
