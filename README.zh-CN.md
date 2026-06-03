# Computational Structural Biology Platform

[English](README.md) | 简体中文（当前）

Computational Structural Biology Platform 是一个公开的 Codex skill，用于计算结构生物学工作流，包括结构准备、对接、分子动力学自动化、轨迹分析，以及可复用的 human-in-the-loop 研究记忆系统。

本仓库是经过清理的开源发布版本，不包含私人项目数据、原始研究输出、轨迹文件、对接结果或未发表的科学结论。

## 项目简介

Computational Structural Biology Platform 帮助研究者以更安全、更可复现的方式运行结构生物学工作流，并在关键科学决策处保留人工审核节点。项目强调有来源依据的规则、谨慎的 PDB/mmCIF 准备流程、经过验证的 MD 与 docking 命令序列，以及不会静默改变科学输入的案例积累机制。

## 功能特性

- 通过 `SKILL.md` 提供 Codex skill 入口
- PDB 与 AlphaFold3/mmCIF 准备辅助工具
- 显式水 GROMACS pipeline 自动化
- AutoDock Vina receptor 与 ligand 准备辅助工具
- 通用 MD contact-occupancy 分析
- human-in-the-loop case registry 与 exception memory
- public-safe 文档与 release 报告
- 双语文档支持，English 作为 canonical source

## 当前模块

- AlphaFold3 preparation
- mmCIF processing
- PDB standardization
- Protein docking
- AutoDock Vina workflows
- Molecular dynamics
- GROMACS workflow automation
- Trajectory analysis
- Research memory system
- Human-in-the-loop case management

## 计划模块

- Membrane protein MD
- Ligand-protein MD
- Ion-specific analysis
- HADDOCK integration
- ClusPro integration
- MM/PBSA
- DFMD benchmarking

## 安装方式

克隆仓库：

```bash
git clone https://github.com/<your-org>/computational-structural-biology-platform.git
cd computational-structural-biology-platform
```

通过复制或符号链接的方式安装为 Codex skill：

```bash
mkdir -p ~/.codex/skills
ln -s "$PWD" ~/.codex/skills/computational-structural-biology-platform
```

根据需要单独安装运行环境：

- GROMACS for MD workflows
- Python 3.10+
- MDAnalysis and NumPy for trajectory analysis
- RDKit, Meeko, and AutoDock Vina Python bindings for docking workflows

## Codex Skill 使用方式

在 Codex 中使用该 skill：

```text
Use $computational-structural-biology-platform to prepare this PDB for explicit-water GROMACS MD.
```

配置变量后，可在项目目录中手动运行 GROMACS pipeline：

```bash
cp scripts/gromacs/run_explicit_water_pipeline.sh ./
cp -r templates/mdp/verified/gromacs_2025_explicit_water_10ns ./mdp
INPUT_PDB=protein.pdb GMX_BIN=gmx MDP_DIR=mdp nohup bash run_explicit_water_pipeline.sh > pipeline_console.log 2>&1 & echo $! > pipeline.pid
```

检查运行状态：

```bash
bash scripts/gromacs/check_pipeline_status.sh
```

## 目录结构

```text
SKILL.md                       Codex skill instructions
core/                          Shared development and validation policies
modules/                       Modular workflow implementations
scripts/                       Workflow helper scripts
references/                    Public workflow rules and registries
templates/mdp/                 Generic public GROMACS MDP templates
knowledge/                     Public seed case registry and exception schemas
docs/                          User and developer documentation
examples/                      Generic example configs
tests/                         Repository validation scripts
```

## 示例用法

- `examples/gromacs_pipeline.env`: configurable environment variables for an explicit-water MD run
- `examples/vina_config.example.json`: Vina project configuration template

## 文档

- [Developer Guide](docs/DEVELOPER_GUIDE.zh-CN.md)
- [Module Development Policy](docs/MODULE_DEVELOPMENT_POLICY.zh-CN.md)
- [Knowledge System Policy](docs/KNOWLEDGE_SYSTEM_POLICY.zh-CN.md)
- [Translation Policy](docs/TRANSLATION_POLICY.md)
- [Translation Status](docs/translation_status.md)

## 贡献指南

请阅读 [CONTRIBUTING.zh-CN.md](CONTRIBUTING.zh-CN.md)。贡献内容应当保持通用、文档充分，并且不包含私人数据或未发表结果。

## 免责声明

本项目提供工作流自动化与文档支持，但不会替研究者判断某个 force field、ligand protonation state、membrane composition、docking box 或 simulation length 是否适合特定体系。研究者需要自行审核所有科学假设，并遵守相关软件许可与数据共享限制。
