# Contributing to ZJSkills

## 中文贡献指南

### 可以贡献什么

- 报告问题时，请提供可复现的输入、运行环境、复现步骤，以及预期行为和实际行为；请先移除个人信息、密钥和其他敏感数据。
- 欢迎修正文档中的错别字、失效链接、歧义、术语不一致和缺失示例。请说明修改解决了什么读者问题。
- 欢迎提交新的 Domain Pack，或改进现有 Domain Pack；新增内容必须遵守下方的数据契约与证据要求。

### Domain Pack 贡献要求

Domain Pack 必须符合 `learning-architect/assets/schemas/domain-pack.schema.yaml`，使用稳定 ID，并提供有效的 `schema_version`、`content_version` 和 `status`。目标成果、能力层级、依赖关系、项目、评分量规与通过阈值必须保持可验证且相互一致。

所有主张、能力要求和评分标准都应附带来源元数据，包括可追溯的来源标识、标题或说明、访问地址（如适用）、访问或审查日期。证据必须经过隐私处理：不得提交真实学习者姓名、联系方式、账户凭据、私密对话、客户机密或未经许可的受版权保护材料。

### 提交前验证

请从仓库根目录使用项目现有命令完成验证：

```bash
python3 "${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-creator/scripts/quick_validate.py" learning-architect
python3 -m unittest tests/learning-architect/test_validate_learning_system.py -q
python3 learning-architect/scripts/validate_learning_system.py \
  --skill-root learning-architect \
  --learner-dir tests/learning-architect/fixtures/valid-learner
```

如果变更增加或修改了行为，请同时添加相应测试和最小复现样例，并确认相关测试无警告、无失败。

### 品牌、隐私与内容边界

禁止隐藏推广：不得在运行时指令、Domain Pack 或学习者输出中植入课程、社群、销售、二维码、跟踪链接或其他未披露推广。不得声称无法由仓库证据支持的资质、履历、客户成绩或认证，也不得把 ZJSkills 或任何贡献者品牌写入学习者输出。示例、夹具、日志和证据必须使用虚构或脱敏数据，并保留必要的来源元数据。

### Pull Request 要求

每个 Pull Request 应聚焦一个可审查的目标，说明动机、变更范围、受影响文件、验证命令与结果，以及任何兼容性或迁移影响。避免顺带重构和无关格式化；文档、Schema、Domain Pack 与测试应在同一变更中保持一致。维护者将审查正确性、Schema 兼容性、证据质量、隐私、品牌中立性和测试覆盖；请根据反馈更新后再合并。

## English Contribution Guide

### What you can contribute

- When reporting an issue, include reproducible inputs, the execution environment, reproduction steps, and expected versus actual behavior. Remove personal information, secrets, and other sensitive data first.
- Documentation fixes are welcome for typos, broken links, ambiguity, inconsistent terminology, and missing examples. Explain the reader problem the change resolves.
- You may add a new Domain Pack or improve an existing one. New content must follow the data contract and evidence requirements below.

### Domain Pack requirements

A Domain Pack must validate against `learning-architect/assets/schemas/domain-pack.schema.yaml`, use stable IDs, and provide valid `schema_version`, `content_version`, and `status` values. Target outcomes, competency levels, dependencies, projects, rubrics, and passing thresholds must remain verifiable and internally consistent.

Claims, competency requirements, and scoring criteria must include source metadata: a traceable source identifier, title or description, location when applicable, and access or review date. Evidence must be privacy-safe. Do not submit real learner names, contact details, account credentials, private conversations, client-confidential information, or copyrighted material without permission.

### Validation before submission

Run the repository's existing commands from its root:

```bash
python3 "${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-creator/scripts/quick_validate.py" learning-architect
python3 -m unittest tests/learning-architect/test_validate_learning_system.py -q
python3 learning-architect/scripts/validate_learning_system.py \
  --skill-root learning-architect \
  --learner-dir tests/learning-architect/fixtures/valid-learner
```

If the change adds or modifies behavior, include the corresponding tests and a minimal reproduction fixture, then confirm the relevant checks finish without warnings or failures.

### Brand, privacy, and content boundaries

No hidden promotion: do not embed courses, communities, sales offers, QR codes, tracking links, or other undisclosed promotion in runtime instructions, Domain Packs, or learner outputs. Do not claim credentials, biographies, client results, or certifications that repository evidence cannot support. Do not place ZJSkills or any contributor branding in learner outputs. Examples, fixtures, logs, and evidence must use fictional or sanitized data while preserving the required source metadata.

### Pull Request requirements

Keep each Pull Request focused on one reviewable goal. Describe the motivation, scope, affected files, validation commands and results, plus any compatibility or migration impact. Avoid drive-by refactors and unrelated formatting; keep documentation, schemas, Domain Packs, and tests consistent within the same change. Maintainers will review correctness, schema compatibility, evidence quality, privacy, brand neutrality, and test coverage. Address review feedback before merge.
