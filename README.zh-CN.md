# Computational Structural Biology Platform

## 项目简介

Computational Structural Biology Platform 是一个面向 Codex 的计算结构生物学技能，用于结构准备、分子对接、分子动力学自动化、轨迹分析以及人工审核驱动的经验积累。

## 适用场景

- AlphaFold3/mmCIF 输出整理
- PDB 标准化和拓扑前检查
- GROMACS 显式水稳定性模拟
- AutoDock Vina 分子对接和小规模筛选
- MD 轨迹分析和接触占有率分析
- 记录可复用的工作流经验和异常案例

## 当前模块

- `af3_cif_preparation`
- `pdb_standardization`
- `gromacs_stability_md`
- `vina_screening`
- `trajectory_analysis`

## 计划模块

- `haddock3`
- `smd`
- `membrane_md`
- `remd`
- `ligand_protein_md`
- `ion_analysis`
- `mmpbsa`

## 安装方式

```bash
git clone https://github.com/Chenghaoj/computational-structural-biology-platform.git
cd computational-structural-biology-platform
mkdir -p ~/.codex/skills
ln -s "$PWD" ~/.codex/skills/computational-structural-biology-platform
```

第三方软件需要按模块单独安装，例如 GROMACS、MDAnalysis、RDKit、Meeko、AutoDock Vina 等。安装说明见 `references/software_registry.md`。

## Codex Skill 使用方式

在 Codex 中调用：

```text
Use $computational-structural-biology-platform to prepare this PDB for explicit-water GROMACS MD.
```

## 目录结构

```text
core/          多开发者协作、验证、版本和模板策略
modules/       标准化工作流模块
references/    全局规则、软件注册表和依赖矩阵
scripts/       可执行辅助脚本
templates/     模板文件
knowledge/     经验记忆和异常登记
tests/         快速验证脚本
```

## 示例用法

运行 GROMACS 后台流水线前，先检查依赖：

```bash
python3 scripts/environment/check_dependencies.py --module gromacs --strict --output environment_report.md
```

启动流水线：

```bash
INPUT_PDB=protein.pdb MDP_DIR=mdp nohup bash scripts/gromacs/run_explicit_water_pipeline.sh > pipeline_console.log 2>&1 & echo $! > pipeline.pid
```

## 软件依赖

不同模块依赖不同软件。请查看：

- `references/software_registry.md`
- `references/software_dependency_matrix.md`
- `references/software_dependency_rules.md`

缺少依赖时，技能应停止执行，提供官方安装资源，并且不得静默安装软件。

## 如何添加新模块

新模块必须包含：

- `README.md`
- `workflow_rules.md`
- `install.md`
- `dependencies.md`
- `input_schema.md`
- `output_schema.md`
- `known_issues.md`
- `scripts/`、`templates/`、`examples/`、`tests/`

添加后更新 `references/module_registry.md`、`references/software_registry.md` 和 `references/software_dependency_matrix.md`，并运行：

```bash
python3 tests/quick_validate_all.py
```

## 人工审核与经验积累机制

本项目强调 human-in-the-loop：涉及配体化学、金属/辅因子、膜组成、力场参数、离子定义、轨迹分析定义等科学判断时，不能自动修改，必须请求研究者确认。可复用经验记录在 `knowledge/`。

## 注意事项

- 不要提交轨迹、对接结果、PDBQT 输出或未发表科研结果。
- verified templates 是只读的；修改模板必须新建版本目录。
- `-maxwarn` 不能默认使用。
- 计划模块不能执行未验证工作流。

## 免责声明

本项目提供工作流自动化和工程化规范，不替代科学判断。用户需要自行确认体系、参数、力场、模拟长度、对接盒子和分析定义是否适合具体研究问题。
