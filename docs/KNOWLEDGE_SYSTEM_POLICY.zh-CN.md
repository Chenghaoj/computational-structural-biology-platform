# Knowledge System Policy

[English](KNOWLEDGE_SYSTEM_POLICY.md) | 简体中文（当前）

Knowledge system 让 skill 能够记住可复用的 workflow lessons，同时保护未发表研究和课题组私人信息。

## 目的

Knowledge system 记录：

- Common failure modes.
- Verified fixes.
- Manual researcher decisions.
- Environment-specific issues that may recur.
- Workflow improvement cases.
- Known limitations and pending review items.

它应帮助改进未来工作流，同时不能暴露私人科学结果。

## 只记录 Public-Safe Knowledge

公开仓库中的 knowledge 必须匿名化且可复用。不要发布：

- Unpublished protein-specific results.
- Raw docking scores tied to private projects.
- Raw MD trajectories or analysis outputs.
- Private project names or internal hypotheses.
- Server names, usernames, absolute personal paths, or SSH details.
- Credentials or private environment configuration.

如果经验来自私人项目，加入前必须泛化。例如，记录 "GROMACS grompp failed because ion topology was not included"，而不是写入私人项目名称和输出文件。

## Case Management System

使用 cases 记录可复用决策和经验。一个 case 应包含：

- Case ID.
- Date.
- Module.
- Status.
- Problem.
- Decision.
- Reusable lesson.
- Validation evidence.
- Reviewer or researcher annotation when relevant.

推荐状态：

- `open`
- `pending_review`
- `verified`
- `superseded`
- `rejected`

需要人工科学判断的 cases 应保持 `pending_review`，直到 researcher 批准。

## Researcher Annotation Policy

当人类专业判断决定正确 workflow choice 时，应使用 researcher annotations。例如：

- Selecting a biologically relevant chain or assembly.
- Choosing protonation, ligand, cofactor, membrane, or ion treatment.
- Deciding whether a structure cleanup operation is scientifically acceptable.
- Interpreting whether a simulation or docking run is meaningful.

Annotations 应区分事实与解释，并标注该决策是 project-specific 还是 reusable。

## Knowledge Database Locations

常见位置包括：

- `knowledge/global_case_registry.csv`
- `knowledge/exceptions/`
- `knowledge/pending_review/`
- module-specific `known_issues.md`
- module-specific tests or examples when a case becomes a reusable validation fixture

不要向这些位置加入私人原始数据。

## Installation and Environment Knowledge

Skill 可以记住常见 installation issues 和 environment-specific fixes，但 installation instructions 在可用时必须引用官方文档。不要把私人机器假设编码成通用要求。

## From Case to Policy

当 case 显示出通用 workflow improvement 时：

1. Add or update the case entry.
2. Generalize the lesson.
3. Update module `known_issues.md` or `workflow_rules.md`.
4. Update shared references if the lesson affects multiple modules.
5. Add validation if possible.
6. Mark the case `verified` after review.

## Review and Cleanup

应定期 review knowledge entries，清理过期 workaround、私人细节和已被替代的建议。Superseded cases 应保持可追溯，并指向新的 policy 或 fix。
