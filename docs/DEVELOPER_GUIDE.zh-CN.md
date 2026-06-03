# Developer Guide

[English](DEVELOPER_GUIDE.md) | 简体中文（当前）

本指南说明如何把 Computational Structural Biology Platform 作为一个公开、可多人协作的 Codex skill 进行开发。目标读者包括新加入课题组的成员、外部贡献者和维护者，帮助他们从想法稳定推进到经过验证的模块。

## 仓库基线

当前架构围绕模块化、可审核的工作流组织：

- `SKILL.md` is the entry point for Codex skill behavior.
- `core/` contains development, validation, versioning, and template policies.
- `modules/` contains workflow modules such as GROMACS MD, Vina screening, PDB standardization, AF3 preparation, and trajectory analysis.
- `references/` contains registries, dependency matrices, workflow rules, and software policies.
- `scripts/` contains shared automation scripts.
- `templates/` contains reusable workflow templates.
- `knowledge/` contains anonymized cases, known workflow lessons, and review queues.
- `docs/` contains public-facing and developer documentation.
- `tests/` contains repository validation utilities.

## 当前 Active Modules

- `af3_cif_preparation`
- `pdb_standardization`
- `gromacs_stability_md`
- `vina_screening`
- `trajectory_analysis`

## 预留 Future Modules

- `haddock3`
- `smd`
- `membrane_md`
- `remd`
- `ligand_protein_md`
- `ion_analysis`
- `mmpbsa`

Future modules 应先从 `planned` 或 `experimental` 开始，只有在完成验证、文档和 review 后才能变为 `active`。

## 开发生命周期

1. Define the scientific or workflow problem.
2. Decide whether it belongs in an existing module or a new module.
3. Create a branch using the branch naming rules in `CONTRIBUTING.md`.
4. Implement the smallest coherent change.
5. Update registries and documentation.
6. Add or update examples and tests.
7. Run validation.
8. Open a pull request with review notes.
9. Merge after review and successful validation.

## 分支策略

`main` 是公开 release 分支。它应保持可验证、可移植，并且不包含私人数据。

使用简短清晰的分支名：

- `feature/gromacs-background-pipeline`
- `fix/vina-dependency-check`
- `docs/module-policy`
- `registry/add-haddock3`
- `experiment/membrane-md-prototype`

Experimental branches 可以包含未完成工作，但合并到 `main` 的 experimental code 必须清楚标记，并且默认不能影响 active workflows。

## Pull Request 流程

一个好的 pull request 应包含：

- 变更内容的简短总结。
- 受影响的 module 或 policy area。
- 科学假设或 workflow assumptions。
- Validation commands and results。
- 已执行的 public-safety checks。
- 已知限制或后续工作。

Reviewers 应重点关注可复现性、公开发布安全、科学正确性、可移植性和可维护性。

## 添加新模块

创建 `modules/<module_name>/`，并包含所需 module skeleton：

```text
modules/<module_name>/
  README.md
  workflow_rules.md
  install.md
  dependencies.md
  input_schema.md
  output_schema.md
  known_issues.md
  scripts/
  templates/
  examples/
  tests/
```

随后更新：

- `references/module_registry.md`
- `references/software_registry.md`
- `references/software_dependency_matrix.md`
- `SKILL.md` if Codex routing or workflow behavior changes
- `tests/quick_validate_all.py` if validation rules need to expand

如果模块只有安装说明，应保持 `planned`；如果已有 workflow 但尚未验证，应保持 `experimental`；只有验证和 review 完成后才能标记为 `active`。

## 更新现有模块

修改模块前：

1. Read its `README.md`, `workflow_rules.md`, `dependencies.md`, and `known_issues.md`.
2. Check whether related cases exist in `knowledge/`.
3. Preserve existing public interfaces unless a breaking change is documented.
4. Add migration notes when paths, inputs, outputs, or defaults change.

## 依赖策略

Workflows 在执行前必须检查所需 third-party software。Workflow 应检测：

- Software availability.
- Executable path.
- Version.
- Required Python package imports where relevant.
- Environment notes or limitations.

如果软件缺失，应说明缺失项，尽可能链接官方安装文档，并在安装任何内容前询问用户。不要静默安装软件。

## Template Policy

Verified templates 是可复现性的锚点。不要直接覆盖它们。应创建新的 versioned template path，说明原因，并仅在验证通过后更新 references。

## Knowledge and Case Management

Knowledge system 记录可复用经验、常见失败、人工决策和 workflow improvements。它不得包含未发表研究发现或私人输出。未解决或项目特异性笔记应保存在私人本地位置，而不是公开仓库。

以下情况应创建 case：

- A workflow required a manual scientific decision.
- A failure mode may recur.
- A dependency or environment issue was solved.
- A template or workflow policy changed because of experience.

## 验证

打开 pull request 前运行 quick validator：

```bash
python3 tests/quick_validate_all.py
```

对发生变化的 shell 和 Python scripts 运行语法检查：

```bash
bash -n path/to/script.sh
python3 -m py_compile path/to/script.py
```

对于需要外部工具执行的 workflow scripts，即使本地没有安装外部软件，也应验证语法和 dependency detection。

## Release Process

满足以下条件后可准备 release：

- Validation passes.
- Public-safety scans are clean.
- `CHANGELOG.md` is updated.
- New modules and dependencies are registered.
- Documentation reflects current behavior.
- No private data or raw computational outputs are staged.

如果 audit reports 中仍有未解决的 private items，不要 push 或 publish。
