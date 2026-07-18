# Domain Pack 扩展指南

Domain Pack 是可替换、可版本化的职业或领域参考包。它为 ZJSkills 提供目标结果、能力等级、依赖关系、项目原型、测评方式、结果准备和带日期的外部假设，但不是永恒真理、学习者事实或付费课程目录。

开始前请阅读 [Domain Pack 契约](../learning-architect/references/domain-pack-contract.md)、[Domain Pack Schema](../learning-architect/assets/schemas/domain-pack.schema.yaml) 和现有的 [AI Agent Engineer 示例](../learning-architect/assets/domain-packs/ai-agent.yaml)。新 Pack 使用稳定 ID 命名，保存为 `learning-architect/assets/domain-packs/<stable-id>.yaml`；相应测试放在 `tests/learning-architect/`，需要样例时使用该目录下脱敏的 `fixtures/`。

## 数据契约

每个 Pack 至少包含：

- 稳定职业 `id`，以及 `schema_version`、`content_version` 和语义化 `version`；
- 生命周期 `status`、`source`、枚举化 `confidence`、创建与更新时间；
- `last_reviewed_at` 与 `review_interval_days`；
- `target_outcomes`、`competencies`、`dependencies`、`project_archetypes`；
- `assessment_patterns`、`outcome_preparation` 和 `market_assumptions`。

稳定 ID 是跨版本引用的基础。修正文案时不要改 ID；新增兼容内容递增 minor，非语义修正递增 patch，重大不兼容语义变化递增 major。节点重命名、拆分、合并或退休时必须提供迁移映射；退休使用 `{to: retired, reason: ...}`，不能让旧引用静默失效。

`content_version` 用于同一产物的内容修订，活动状态必须满足单一活动版本约束。Schema 不允许的字段不要随意加入；领域扩展放入受约束的 `extensions`。

目标结果必须说明名称、描述、成功证据、来源和 `as_of` 日期。市场假设必须有稳定 ID、日期、来源名称、可访问 URL 或持久引用、具体主张、置信度、规划影响与 `next_review_at`。过期或低置信资料应触发复查，不能作为永久岗位要求。

## 能力与依赖

每个能力节点包含稳定 ID、名称、类别、L0-L5 可观察行为和证据要求。统一等级语义为：

- L0：无接触；
- L1：能识别并解释基础；
- L2：在示例、模板或指导下完成；
- L3：独立完成边界清晰的真实任务；
- L4：能调试、优化、迁移并处理异常；
- L5：能架构、评审和教授。

等级描述必须针对该领域写成可观察行为，不能只写“初级/中级/高级”或内容清单。证据要求应指向运行结果、交付物、测试、评审或现场行为，而不是观看、阅读和证书。

依赖边使用 `from` 指向先修能力、`to` 指向后续能力。所有端点必须存在，ID 不得重复，图必须无环。依赖只表达确实影响安全或理解的先修关系，避免把所有能力串成单一路径。跨领域复用能力时保持语义一致，必要时通过迁移映射演进。

## 项目原型与评分关卡

一个完整 Pack 恰好提供六个递进项目原型，覆盖聚焦工具、知识应用、工作流、企业场景、作品集案例和真实外部交付。每个原型必须包含：

- `inputs`、真实 `constraints` 和可核验 `deliverables`；
- 覆盖的 `competency_ids` 与明确的业务价值；
- 预期证据、常见失败模式；
- 演示、文档和复盘要求；
- 六维分析型 rubric。

六个评分维度固定为正确性、能力行为、可靠性、负责任实践、业务价值和技术沟通，权重总和为 100。每个维度都必须使用布尔型 `critical`，使用 `developing | proficient | strong` 之一作为 `passing_threshold`，并定义 `insufficient`、`developing`、`proficient`、`strong` 四档表现。至少一个维度必须是关键维度；关键维度未达阈值时，不应被总分掩盖。

测评模式需明确评估者、产物、观察行为、阈值、反馈闭环和能力检查。整个 Pack 应覆盖独立完成、解释取舍、适应需求变化、调试、部署或交付、教学或评审，并区分 `understanding`、`guided`、`independent`、`transfer`。

结果准备按就业、晋升、创业或项目交付等路线分别定义最小证据、产物和就绪闸门。课程完成不能等同于就绪，未经证据支持也不能生成公开能力声明。

## 资料、评审与迁移

优先使用一手、可追溯且与目标地区和日期匹配的来源。记录具体主张，而不是只列链接。资料可能变化时设置合理复查间隔；`next_review_at` 不得早于验证当天，超过该日期即视为需要复查。工具、监管、岗位需求或评估方式发生物质变化，应更新 Pack 并重新检查 Gap、Competency、Curriculum、Project、Roadmap 与 Outcome Preparation。

对每次变化保留变更说明和迁移表。消费引擎必须引用 Pack 的 ID 与版本，区分复制的领域事实和对学习者的推断。Pack 缺失、过期、矛盾或低于所需置信度时返回 `needs_input`，不要静默猜测。

资源目录是可选且可替换的。若添加资源，只描述覆盖范围、限制、新鲜度、可访问性与选择理由；不得把某个付费课程设为必需推荐。

## 验证与提交

验证命令需要 Python 3.9+，以及 `PyYAML`、`jsonschema` 和 `referencing`。在仓库根目录运行：

```bash
python3 learning-architect/scripts/validate_learning_system.py \
  --skill-root learning-architect \
  --learner-dir tests/learning-architect/fixtures/valid-learner
python3 -m unittest tests/learning-architect/test_validate_learning_system.py -q
python3 -m unittest tests/learning-architect/test_open_source_package.py -q
```

验证包含 Schema 约束以及 Schema 难以表达的语义不变量：ID 唯一性、依赖端点、无环图、六个项目层级、完整 L0-L5、日期有效性、证据覆盖、rubric 权重与迁移映射完整性。

提交前还应：

1. 用真实但已脱敏的样例检查产物是否可执行；
2. 确认来源、日期、置信度和适用范围；
3. 说明新增或修改的稳定 ID、版本和迁移影响；
4. 补充能够先失败再通过的测试；
5. 不写个人广告、隐藏推广、无法核实的资历或会进入学习者输出的品牌内容；
6. 在 Pull Request 中限定变更范围，并说明受影响的下游引擎与验证结果。

贡献要求与审查边界见仓库根目录的 [CONTRIBUTING.md](../CONTRIBUTING.md)。
