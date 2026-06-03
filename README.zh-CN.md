<p align="center">
  🇺🇸 [English](README.md) | 🇨🇳 简体中文
</p>

# Computational Structural Biology Platform

Computational Structural Biology Platform 是一个公开的 Codex skill，用于计算结构生物学工作流，包括结构准备、对接、分子动力学自动化、轨迹分析，以及可复用的 human-in-the-loop research memory。

本仓库是经过清理的开源发布版本，不包含私人项目数据、原始研究输出、轨迹文件、对接结果或未发表的科学结论。

## 项目简介

Computational Structural Biology Platform 帮助研究者以更安全、更可复现的方式运行结构生物学工作流，并在关键科学决策处保留明确的检查点。项目强调有来源依据的规则、谨慎的 PDB/mmCIF 准备流程、经过验证的 MD 与 docking 命令序列、模块化软件支持，以及不会静默改变科学输入的案例积累机制。

## 功能特性

- 通过 `SKILL.md` 提供 Codex skill 入口
- PDB 与 AlphaFold3/mmCIF 准备辅助工具
- 显式水 GROMACS pipeline 自动化
- AutoDock Vina receptor 与 ligand 准备辅助工具
- 通用 MD contact-occupancy 分析
- 位于 `modules/` 与 `references/` 的 modular software registry
- human-in-the-loop case registry 与 exception memory
- public-safe release checks、identity leak validation 与双语文档

## 当前模块

- `af3_cif_preparation`
- `pdb_standardization`
- `gromacs_stability_md`
- `vina_screening`
- `trajectory_analysis`

这些模块对应当前公开工作流，包括 AlphaFold3 preparation、mmCIF processing、PDB standardization、AutoDock Vina workflows、molecular dynamics setup、GROMACS workflow automation、trajectory analysis 和 reusable research memory。

## 计划模块

- `haddock3`
- `smd`
- `membrane_md`
- `remd`
- `ligand_protein_md`
- `ion_analysis`
- `mmpbsa`

Planned modules 在完成文档、dependency rules、examples、tests 和 review 之前不会启用。

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

## 使用方式

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

## 仓库结构

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

## 模块开发

新模块应遵循 `modules/<module_name>/` 中的标准结构，并且必须完成注册后才能变为 active。请从以下开发文档开始：

- [参与贡献](CONTRIBUTING.zh-CN.md)
- [Developer Guide](docs/DEVELOPER_GUIDE.zh-CN.md)
- [Module Development Policy](docs/MODULE_DEVELOPMENT_POLICY.zh-CN.md)

发布前应验证模块结构、templates、scripts、identity safety 和公开文档：

```bash
python3 tests/check_identity_leaks.py
python3 tests/quick_validate_all.py
```

## 研究经验积累系统

Research memory system 用于记录可复用的 workflow lessons、exceptions、manual decisions 和 validated fixes，同时不发布私人研究数据。公开条目应使用 `example_protein_A`、`example_protein_B`、`example_ligand`、`example_dataset` 和 `example_project` 等通用示例。

相关文件包括：

- `knowledge/global_case_registry.csv`
- `knowledge/exceptions/`
- `knowledge/pending_review/`
- `docs/KNOWLEDGE_SYSTEM_POLICY.zh-CN.md`
- `docs/PRIVACY_AND_ANONYMIZATION_POLICY.md`

## 参与贡献

欢迎提交模块化、经过验证、文档充分且 public-safe 的贡献。提交 pull request 前请阅读 [CONTRIBUTING.zh-CN.md](CONTRIBUTING.zh-CN.md)。

所有公开 examples 和 reports 都必须避免个人姓名、服务器名称、内部项目名、未发表标识、凭据和机器特异性路径。

## 许可证

仓库许可证信息见 [LICENSE](LICENSE)。

## 免责声明

本项目提供工作流自动化与文档支持，但不会替研究者判断某个 force field、ligand protonation state、membrane composition、docking box 或 simulation length 是否适合特定体系。研究者需要自行审核所有科学假设，并遵守相关软件许可与数据共享限制。
