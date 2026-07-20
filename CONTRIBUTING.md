# Contributing to ZJSkills

## 中文贡献指南

### 可以贡献什么

- 修正文档歧义、失效链接、双语不一致或缺失示例；
- 提交可复现的交互问题，包含输入、上下文、预期输出、实际输出与安全脱敏后的证据；
- 改进 `SKILL.md` 或四个精简引用文件，但每个文件必须保持单一职责和按需加载；
- 增加能证明真实用户需求的前向交互测试或边界回归测试。

### 3.0 贡献边界

- **精简引用文件：**不要重复共享规则，不要为了“以后可能有用”新增大而全的知识库。
- **交互测试：**优先测试真实输入下的模式选择、上下文复用、零个或一个决定性问题、单一下一步、证据边界与非 AI 边界。
- **运行时不得推广：**不得加入联系人、答疑群、课程、社群、购买、转化或线索分发逻辑；公开支持说明只能留在指定公开文档中。
- **双语文档：**任何用户可见行为变化必须同时更新中文与英文配对页面，并保持语义一致、链接可用。
- **前向测试证据：**没有一个真实前向测试证明现有六个运行时文件无法满足需求，就不得新增运行时文件、脚本、模板、状态 Schema 或引用文件。
- 继续保持自学、免费资源、付费课程和结构化支持的商业中立；不得承诺外部结果或伪造专业权威。

### 提交前验证

从仓库根目录运行：

```bash
python3 -m unittest tests.zjskills.test_open_source_package -q
python3 -m unittest discover -s tests/zjskills -p 'test_*.py' -q
```

Pull Request 应聚焦一个目标，说明动机、文件范围、RED/GREEN 证据、完整测试结果、迁移影响和剩余风险。示例与日志必须移除个人信息、密钥、客户机密及未授权材料。

## English Contribution Guide

### What you can contribute

- Fix ambiguity, broken links, bilingual drift, or missing examples in public documentation.
- Report a reproducible interaction problem with the input, context, expected output, actual output, and safely redacted evidence.
- Improve `SKILL.md` or the four concise reference files while preserving one responsibility per file and conditional loading.
- Add a forward interaction test or boundary regression that demonstrates a real user need.

### 3.0 contribution boundaries

- **Keep concise reference files:** do not duplicate shared rules or add a broad knowledge base for hypothetical future use.
- **Use interaction tests:** prioritize mode selection, context reuse, zero-or-one decisive questions, one next action, evidence boundaries, and non-AI boundaries under realistic inputs.
- **No runtime promotion:** do not add contacts, Q&A groups, courses, communities, purchasing, conversion, or lead-routing logic. The public support note belongs only in its designated public documents.
- **Maintain bilingual documentation:** every user-visible behavior change must update the paired Chinese and English pages with equivalent meaning and working links.
- **Require forward-test evidence:** do not add a runtime file, script, template, state schema, or reference unless a real forward test proves that the existing six runtime files cannot meet the need.
- Preserve commercial neutrality among self-study, free resources, paid courses, and structured support. Never promise external outcomes or fabricate domain authority.

### Validation before submission

Run from the repository root:

```bash
python3 -m unittest tests.zjskills.test_open_source_package -q
python3 -m unittest discover -s tests/zjskills -p 'test_*.py' -q
```

Keep each Pull Request focused on one goal. Report motivation, file scope, RED/GREEN evidence, complete test results, migration impact, and remaining risks. Remove personal information, secrets, client-confidential content, and unauthorized material from examples and logs.
