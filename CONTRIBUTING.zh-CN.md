# Contributing

[English](CONTRIBUTING.md) | 简体中文（当前）

感谢你帮助开发 Computational Structural Biology Platform。本仓库面向课题组成员、外部贡献者和 Codex-assisted workflows 的长期协作。贡献应提升可复现性，保护未发表研究，并让工作流行为保持透明。

## 隐私与匿名化

所有贡献者必须遵守 [docs/PRIVACY_AND_ANONYMIZATION_POLICY.md](docs/PRIVACY_AND_ANONYMIZATION_POLICY.md)。公开文档、examples、scripts、templates 和 knowledge records 中不得包含个人姓名、用户名、服务器名、内部项目名、未发表项目标识或机器特异性路径。请使用 `user`、`researcher`、`server`、`compute_server`、`example_project`、`example_dataset`、`example_protein` 和 `example_ligand` 等通用占位符。

## 贡献原则

- 公开仓库中不得包含私人路径、服务器名称、访问凭据、未发表项目结果、原始轨迹、对接输出或大型二进制数据。
- 优先在 `modules/<module_name>/` 下进行模块化修改，避免跨越无关工作流的大范围改动。
- 工作流行为变化应在同一个 pull request 中同步更新文档、registries、schemas 和 tests。
- verified templates 是受保护的 release artifacts。不要直接覆盖它们。
- 可复用经验应记录到 knowledge system 中，但必须匿名化所有项目特异性科学细节。

## 分支策略

`main` 是 release-ready 分支，应始终通过验证，并保持适合公开 GitHub 发布。

推荐分支命名：

- `feature/<module>-<short-topic>` for new capabilities.
- `fix/<module>-<short-topic>` for bug fixes.
- `docs/<short-topic>` for documentation-only changes.
- `registry/<short-topic>` for registry updates.
- `experiment/<module>-<short-topic>` for exploratory work that is not yet active.

除非 maintainer 正在准备小型 release-only 更新，否则避免直接提交到 `main`。Experimental workflows 在通过验证前应保持 `experimental` 或 `planned` 状态。

## Pull Request 流程

1. Create or identify an issue, case, or development need.
2. Create a branch from the latest `main`.
3. Make scoped changes using the existing architecture.
4. Update module documentation and registries when behavior changes.
5. Run validation:

```bash
python3 tests/quick_validate_all.py
```

6. Check for private content before opening a PR:

```bash
rg -n "PERSONAL_PATH_PATTERN|PRIVATE_HOST_PATTERN|PRIVATE_PROJECT_PATTERN|CREDENTIAL_PATTERN" .
find . -type f -size +20M -print
```

7. Open a pull request with a concise summary, validation output, and risk notes.
8. Request review from at least one maintainer or module owner.
9. Address review comments with follow-up commits.
10. Merge only after validation passes and public-safety checks are clean.

## PR Checklist

在较大的 PR 中包含以下 checklist：

```markdown
- [ ] Scope is limited to one module, policy area, or release task.
- [ ] `python3 tests/quick_validate_all.py` passes.
- [ ] New or changed scripts have syntax checks.
- [ ] Module registry was updated if module status changed.
- [ ] Software registry and dependency matrix were updated if dependencies changed.
- [ ] Verified templates were not overwritten directly.
- [ ] No raw trajectories, docking outputs, PDBQT results, credentials, or private project data were added.
- [ ] Documentation was updated for users and developers.
```

## 模块开发

每个模块位于 `modules/<module_name>/`，并且必须包含：

- `README.md`
- `workflow_rules.md`
- `install.md`
- `dependencies.md`
- `input_schema.md`
- `output_schema.md`
- `known_issues.md`
- `scripts/`
- `templates/`
- `examples/`
- `tests/`

Active modules 必须登记在 `references/module_registry.md`，依赖关系必须映射到 `references/software_dependency_matrix.md`，并且需要验证覆盖。

## Verified Template 保护

Verified templates 是只读的。如果 workflow template 需要改变，请创建新的 versioned directory 或文件，说明修改原因，更新 references，并在验证通过后再标记为 active。不要静默替换 verified template，因为这会破坏可复现性。

## Knowledge System

可复用工作流经验应放在 `knowledge/` 中。项目特异性观察、未发表科学解释、私人 protein names，以及来自原始输出的结论不得发布。只记录匿名化的案例和可泛化经验。

## Release Workflow

发布前：

1. Run repository validation.
2. Run public-safety scans.
3. Update `CHANGELOG.md`.
4. Confirm `.gitignore` excludes raw outputs and private folders.
5. Confirm no unresolved `PRIVATE_REMOVE_BEFORE_UPLOAD` items remain in release audit reports.
6. Commit with a release-oriented message.
7. Push only to the correct GitHub remote.
8. Create a GitHub release or tag after review.

完整开发流程见 [docs/DEVELOPER_GUIDE.zh-CN.md](docs/DEVELOPER_GUIDE.zh-CN.md)。
