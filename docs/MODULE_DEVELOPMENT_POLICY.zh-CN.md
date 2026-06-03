# Module Development Policy

[English](MODULE_DEVELOPMENT_POLICY.md) | 简体中文（当前）

本政策定义 workflow modules 的创建、review、验证和维护方式。

## Module Status Labels

在 `references/module_registry.md` 中一致使用以下标签：

- `active`: implemented, documented, validated, and safe for standard use.
- `experimental`: implemented or partially implemented, but still under testing or limited review.
- `planned`: reserved for future development or installation guidance only.
- `deprecated`: retained for compatibility but no longer recommended.

在 required files、registries、dependencies、examples 和 validation checks 完成前，模块不得标记为 `active`。

## Required Module Structure

每个模块必须包含：

```text
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

Planned modules 的文件可以简洁，但必须清楚说明当前状态和限制。

## Module README

`README.md` 应说明：

- Purpose and scope.
- Supported workflows.
- Required software.
- Typical inputs and outputs.
- Current status.
- Known limitations.
- Links to related references.

## Workflow Rules

`workflow_rules.md` 定义 Codex 应如何操作该模块。它应包含：

- Preflight checks.
- Required dependencies.
- User approval points.
- Non-interactive behavior where appropriate.
- Failure handling.
- Logging expectations.
- When to stop and ask a human researcher.

## Install Documentation

`install.md` 必须优先引用官方软件文档。如果包含建议命令，应明确标注为 recommended examples，不能替代官方来源。

## Dependency Documentation

`dependencies.md` 必须列出 required and optional software、version expectations、verification commands 和 known environment issues。

## Input and Output Schemas

`input_schema.md` 和 `output_schema.md` 必须定义 expected files、formats、naming conventions、required metadata 和 validation checks。不要在未记录假设的情况下接受含糊输入。

## Scripts

Scripts 应可移植、明确、防御性强：

- Use strict shell behavior when appropriate, such as `set -euo pipefail`.
- Validate inputs before execution.
- Check expected outputs after each major step.
- Do not use local usernames, server hostnames, or absolute private paths.
- Do not silently continue after scientific or tool failures.
- Do not use unsafe overrides such as GROMACS `-maxwarn` by default.

## Examples

Examples 必须 public-safe 且体积较小。不要包含 raw trajectories、unpublished structures、docking result files、production outputs 或 project-specific data。

## Tests

Module tests 应检查 structure、script syntax、input validation、registry consistency 和 public-safety constraints。除非明确标记为 optional integration tests，否则 tests 不应要求大型 third-party workloads。

## Future Module Expansion Workflow

添加 software 或 workflow module 时：

1. Create `modules/<module_name>/`.
2. Add installation instructions.
3. Add dependency definitions.
4. Add workflow rules.
5. Add input and output schemas.
6. Add known issues.
7. Add examples and tests.
8. Register the module in `references/module_registry.md`.
9. Register software in `references/software_registry.md`.
10. Register dependencies in `references/software_dependency_matrix.md`.
11. Run validation.
12. Request review before marking the module `active`.

## Backward Compatibility

重构已有功能时不要删除旧的公开路径。可行时应保留旧路径、添加 migration notes，或提供 compatibility wrappers。
