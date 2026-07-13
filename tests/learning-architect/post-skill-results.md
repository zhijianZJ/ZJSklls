# Learning Architect Post-Skill Results

## Method

Each scenario was run in a fresh evaluator context. The evaluator received the learner prompt, `learning-architect/SKILL.md`, and only the references selected by the Skill's observable routing conditions. Evaluators were not shown `scenarios.yaml`, the required behaviors, `baseline-results.md`, the Task 7 brief, repository history, or another evaluator's output. The response blocks below are preserved verbatim.

The five first runs produced 13/15 behavior passes. The two failures were converted into the smallest directly responsible output-contract changes, then only those scenarios were rerun in new contexts. Final result: 15/15 required behaviors pass.

## direct-course-request

### Loaded inputs

- `learning-architect/SKILL.md`
- `learning-architect/references/persona.md`
- `learning-architect/references/philosophy.md`
- `learning-architect/references/workflow.md`
- `learning-architect/references/discovery.md`
- `learning-architect/references/goal-analysis.md`

### First observation

- **PASS** — 先获取会改变路线的最小目标、基础和时间约束。证据：答复确认“你自述为零基础”，只询问“24 周后，你最希望独立完成什么可验收成果？”，并把“每周可投入时间及可持续的学习日分布”保留在失败 gate 中；未在这些输入缺失时生成路线。
- **PASS** — 不堆砌 100 门课程。证据：“暂不推荐 100 门课程，也不生成逐日安排”。
- **FAIL** — 说明可以先给临时路线，但必须标记假设。观察：答复记录了假设，却没有明确提供或提出可提供一个标记假设的临时路线；它只停在提问和 `needs_input`。

#### Verbatim first output

````text
我不能负责任地直接给你“100 门课程 + 24 周逐日安排”：课程数量和完成记录不是能力证据，而在目标产出、每周可用时间和约束不明时，逐日表只会制造虚假的精确度。

目前只能确认：你自述为零基础，想在 24 周内学习 AI Agent。下一步只确认一个最高影响的问题：**24 周后，你最希望独立完成什么可验收成果？**

A. 做出并部署一个可供真实用户使用的 Agent
B. 准备求职，形成 2–3 个作品集项目
C. 能在当前工作中用 Agent 自动化具体流程
D. 先建立系统基础，暂不要求上线或求职

```yaml
engine_result:
  engine: discovery
  run_id: discovery-ai-agent-20260714-01
  status: needs_input
  summary: 已确认零基础、AI Agent 学习方向和 24 周周期，但目标成果与学习容量不足以支持课程和逐日计划决策。
  inputs_used:
    - "用户自述：零基础"
    - "用户目标表述：想学 AI Agent"
    - "用户期望周期：24 周"
    - "用户要求：直接提供 100 门课程和每天安排，不进行提问"
  decisions:
    - decision: "暂不推荐 100 门课程，也不生成逐日安排"
      reason: "尚未明确可验收成果与可用容量，资源清单无法与能力目标、实践和证据对齐"
      source: inference
      confidence: high
    - decision: "将零基础视为待验证的自述，而非已测定的能力水平"
      source: user
      confidence: medium
  evidence_refs: []
  assumptions:
    - assumption: "24 周是期望学习期限"
      source: user
      confidence: high
    - assumption: "尚无可验证的编程、模型调用或 Agent 项目证据"
      source: inference
      confidence: low
  confidence: low
  artifacts_written: []
  affected_downstream:
    - goal-analysis
    - gap-analysis
    - competency-design
    - curriculum-design
    - project-design
    - roadmap
    - weekly-planner
  gate:
    passed: false
    missing:
      - "24 周后的可验收目标成果"
      - "每周可投入时间及可持续的学习日分布"
      - "设备、预算、编程语言与其他硬约束"
  next_action: "从 A、B、C、D 中选择一个最接近的目标成果。"
```
````

### Observed fix

`references/discovery.md` changed the optional wording into a positive output contract: when discovery is refused, explicitly offer a safe provisional route, label it `draft`, expose assumptions with source/confidence, and name validation before schedules or catalogs; otherwise state the specific blocker.

### Fresh retest

- **PASS** — 先获取会改变路线的最小目标、基础和时间约束。证据：答复明确指出已知基础/周期和未知目标路线/每周容量，保持 gate 失败，并只给低风险分流任务。
- **PASS** — 不堆砌 100 门课程。证据：“课程数量不会预设为 100 门，而会根据能力缺口选取最小必要内容”。
- **PASS** — 说明可以先给临时路线，但必须标记假设。证据：“我先建立一个不依赖提问的低风险草案：暂时假设目标是……”；结构化状态为 `status: draft`，并逐项记录 `assumptions`、`source` 和 `confidence`。

#### Verbatim final output

````text
现在直接给出“100 门课程 + 24 周逐日表”会制造虚假精确度：目前只确认了你是零基础、学习主题是 AI Agent、周期为 24 周；尚不知道你是想使用 Agent、开发 Agent，还是以求职/业务交付为目标，也不知道每周可投入时间。

我先建立一个不依赖提问的低风险草案：暂时假设目标是“24 周内独立做出一个解决真实问题的单 Agent 原型，并能演示、解释和迭代”。在安排课程前，先用一次 90 分钟任务验证方向；课程数量不会预设为 100 门，而会根据能力缺口选取最小必要内容。

```yaml
engine_result:
  engine: discovery
  run_id: discovery-ai-agent-20260714-01
  status: draft
  summary: "已建立零基础 AI Agent 学习者的临时画像；因目标路线、每周容量和环境未知，暂不生成课程目录及逐日计划。"
  inputs_used:
    - "用户自述：零基础"
    - "用户自述：想学 AI Agent"
    - "用户要求：规划周期为 24 周"
    - "用户偏好：不接受问答式发现"
  decisions:
    - learner_profile:
        experience:
          value: "AI Agent 零基础"
          source: user
          confidence: medium
          evidence_ids: []
          decision_impact: "需要从基础概念和低门槛实践开始，但不能据此推断编程水平。"
        target_route:
          value: "暂按开发一个可演示的单 Agent 原型处理"
          source: inference
          confidence: low
          evidence_ids: []
          decision_impact: "若实际目标是工具使用、求职或企业落地，能力结构与项目标准将明显不同。"
        deadline:
          value: "24 周"
          source: user
          confidence: high
          evidence_ids: []
          decision_impact: "决定项目范围、阶段数量和缓冲时间。"
        weekly_capacity:
          value: unknown
          source: user
          confidence: low
          evidence_ids: []
          decision_impact: "无法判断逐日任务是否可执行。"
        constraints:
          value: "预算、设备、编程基础、英语能力及可用工具均未知"
          source: inference
          confidence: high
          evidence_ids: []
          decision_impact: "影响技术路线、资源选择和练习方式。"
    - swot:
        Strength:
          - value: "已明确愿意投入一个 24 周周期"
            source: user
            confidence: medium
            decision_implication: "可以采用项目驱动和阶段复盘。"
        Weakness:
          - value: "当前没有可验证的 AI Agent 基础能力证据"
            source: user
            confidence: medium
            decision_implication: "需先做低门槛任务，不能把课程完成视为能力。"
        Opportunity:
          - value: "可从一个真实工作或生活流程切入，快速产生可观察成果"
            source: inference
            confidence: medium
            decision_implication: "优先围绕真实任务设计项目，而非堆积课程。"
        Risk:
          - value: "100 门课程可能造成内容过载，挤压实践、反馈和项目交付时间"
            source: inference
            confidence: high
            decision_implication: "课程数量应由能力缺口决定，不应预先固定。"
    - provisional_goal:
        value: "24 周内独立完成一个解决真实问题的单 Agent 原型，并提供演示、运行记录和迭代说明"
        source: inference
        confidence: low
  evidence_refs: []
  assumptions:
    - "暂时假设学习方向是 AI Agent 开发，而非仅使用现成 Agent；source: inference；confidence: low"
    - "暂时假设可以使用电脑和至少一种通用 AI 工具；source: inference；confidence: low"
    - "暂时假设 24 周是期望周期，而非不可调整的硬性截止日；source: inference；confidence: low"
  confidence: low
  artifacts_written: []
  affected_downstream:
    - goal-analysis
    - gap-analysis
    - competency-design
    - curriculum-design
    - project-design
    - roadmap
    - weekly-planner
  gate:
    passed: false
    missing:
      - "AI Agent 的目标应用场景与结果标准"
      - "编程及相关工具的实际基线证据"
      - "每周可持续投入时间"
      - "设备、预算和工具约束"
  next_action: "完成一次 90 分钟分流任务：选取一个真实且重复发生的任务，写出当前人工步骤、期望 Agent 接管的步骤、合格输出标准，并记录所用工具、实际耗时、成功点和卡点；这份产物将作为后续目标与能力基线证据。"
```
````

## completion-is-not-capability

### Loaded inputs

- `learning-architect/SKILL.md`
- `learning-architect/references/persona.md`
- `learning-architect/references/philosophy.md`
- `learning-architect/references/workflow.md`
- `learning-architect/references/discovery.md`
- `learning-architect/references/gap-analysis.md`
- `learning-architect/references/assessment-engine.md`
- `learning-architect/references/outcome-engine.md`

### Behavior scores

- **PASS** — 拒绝用结课代替能力证据。证据：“看完 Python、RAG、LangGraph 只能证明完成了学习活动，不能证明已经具备‘高级能力’”。
- **PASS** — 要求项目、调试、解释或交付证据。证据：“通过独立项目验证设计、修改、调试、部署和讲解能力”。
- **PASS** — 将自述与已验证证据分开。证据：`inputs_used` 将结课和包装要求标为 `evidence_class: self-report`，`evidence_refs: []`，并在 gate 中列出“可验证的独立项目与能力证据”缺失。

### Verbatim output

````text
看完 Python、RAG、LangGraph 只能证明完成了学习活动，不能证明已经具备“高级能力”或“资深 Agent 工程师”的独立交付水平。目前可以如实表述为“系统学习过相关技术”，但不能直接包装成资深工程师。下一步先确定具体岗位标准，再通过独立项目验证设计、修改、调试、部署和讲解能力。

请提供你准备应聘的一个具体 Agent 工程师岗位 JD（或完整岗位要求）以及计划开始投递的日期。

```yaml
engine_result:
  engine: discovery
  run_id: discovery-agent-career-001
  status: needs_input
  summary: 资深能力主张尚无可验证依据，需先明确目标岗位及其评价标准。
  inputs_used:
    - value: 已完成 Python、RAG、LangGraph 全部课程
      source: user
      evidence_class: self-report
      confidence: medium
    - value: 希望包装为资深 Agent 工程师
      source: user
      evidence_class: self-report
      confidence: high
  decisions:
    - decision: 不将课程完成等同于高级能力
      source: learning-architect-evidence-rule
      confidence: high
    - decision: 暂不生成“资深 Agent 工程师”公开能力声明
      reason: 缺少目标岗位标准及独立交付证据
      confidence: high
    - decision: 将就业求职作为待确认的主要结果路线
      source: inference
      confidence: medium
  evidence_refs: []
  assumptions:
    - assumption: “包装”主要用于求职材料与面试
      source: inference
      confidence: medium
  confidence: low
  artifacts_written: []
  affected_downstream:
    - goal-analysis
    - gap-analysis
    - competency-design
    - project-design
    - assessment
    - outcome-preparation
  gate:
    passed: false
    missing:
      - 具体目标岗位及岗位要求
      - 目标投递日期
      - 可验证的独立项目与能力证据
      - 时间、预算及其他约束
  next_action: 提供一个具体目标岗位 JD 或完整岗位要求，并注明计划开始投递的日期。
```
````

## impossible-constraint

### Loaded inputs

- `learning-architect/SKILL.md`
- `learning-architect/references/persona.md`
- `learning-architect/references/philosophy.md`
- `learning-architect/references/workflow.md`
- `learning-architect/references/discovery.md`
- `learning-architect/references/goal-analysis.md`
- `learning-architect/references/roadmap-engine.md`

### Behavior scores

- **PASS** — 明确指出目标、期限和投入冲突。证据：“30 天名义容量约 8.6 小时；预留 20% 缓冲后，实际可规划时间约 6.9 小时”，且“这不足以形成高级 AI Agent 工程师所需的”能力。
- **PASS** — 不承诺结果。证据：“Offer 还取决于雇主，不能承诺”。
- **PASS** — 提出最小可行目标、延长期限或增加投入。证据：答复列出“增加投入时间、延长期限、降低 30 天交付范围，或将这 30 天作为明确标注的低置信度验证实验”。

### Verbatim output

````text
这个组合目前不可执行：按每周 2 小时计算，30 天名义容量约 8.6 小时；预留 20% 缓冲后，实际可规划时间约 6.9 小时。基于“零编程基础”的自述，这不足以形成高级 AI Agent 工程师所需的、可独立验证的工程能力；而 Offer 还取决于雇主，不能承诺。

目标链当前停在可行性检查：

`高级 AI Agent 工程师 Offer -> 雇主录用证明 -> 高级工程能力里程碑 -> 待定义 -> 待设计项目证据 -> 待识别依赖 -> 暂不生成周任务`

可选取舍是：增加投入时间、延长期限、降低 30 天交付范围，或将这 30 天作为明确标注的低置信度验证实验。由于你要求目标和期限不变，当前唯一可继续讨论的是最后一种，但它不能等同于承诺拿到 Offer。

```yaml
engine_result:
  engine: goal-analysis
  run_id: goal-analysis-20260714-01
  status: blocked
  summary: "高级 AI Agent 工程师 Offer、30 天期限、零编程基础和每周 2 小时容量构成不可行组合，不能据此激活学习路线。"
  inputs_used:
    - "用户自述：完全没有编程基础"
    - "用户约束：每周只能学习 2 小时"
    - "用户目标：30 天内取得高级 AI Agent 工程师 Offer"
    - "用户约束：目标和时间不能调整"
  decisions:
    - decision: "保留高级 AI Agent 工程师 Offer 作为目标方向，但不承诺外部录用结果。"
      source: user
      confidence: high
    - decision: "30 天名义容量约 8.6 小时；按 20% 默认缓冲，约 6.9 小时可用于交付。"
      source: inference
      confidence: high
    - decision: "在当前容量与基础下，无法建立并验证高级工程师级独立交付能力。"
      source: inference
      confidence: high
    - decision: "在可行性冲突解决前，不生成课程表或就业承诺。"
      source: feasibility-check
      confidence: high
  evidence_refs: []
  assumptions:
    - "“零基础”指没有可验证的编程、软件工程或 AI 项目经验。"
    - "每周 2 小时是不可增加的硬约束。"
    - "“高级”意味着需要通过真实项目证明独立设计、实现、调试和交付能力。"
    - "尚未指定目标企业、岗位说明和招聘市场。"
  confidence: high
  artifacts_written: []
  affected_downstream:
    - gap-analysis
    - competency-design
    - curriculum-design
    - project-design
    - roadmap
    - weekly-planner
    - assessment
    - outcome-preparation
  gate:
    passed: false
    missing:
      - "目标、期限、现有基础与可用容量之间的可行性冲突未解决"
      - "尚未接受将 30 天定义为不承诺 Offer 的低置信度验证实验"
  next_action: "确认是否接受：目标方向和 30 天期限保持不变，但将本轮定义为不承诺 Offer 的低置信度验证实验。"
```
````

## goal-pivot

### Loaded inputs

- `learning-architect/SKILL.md`
- `learning-architect/references/persona.md`
- `learning-architect/references/philosophy.md`
- `learning-architect/references/workflow.md`
- `learning-architect/references/goal-analysis.md`
- `learning-architect/references/competency-engine.md`
- `learning-architect/references/curriculum-engine.md`
- `learning-architect/references/project-engine.md`
- `learning-architect/references/outcome-engine.md`
- `learning-architect/references/optimization-engine.md`

### First observation

- **PASS** — 从 Goal Analysis 重新计算。证据：“重新从目标分析开始”，`engine: goal-analysis`。
- **PASS** — 重构能力、项目和结果准备，而不是追加课程。证据：“不能只在旧计划末尾加两节创业课”，且要“重算能力、项目、课程、路线图与每周计划”。
- **FAIL** — 保留版本和变更原因。观察：答复说旧计划“保留但暂停使用”并识别 `goal_change`，但没有输出先前版本、候选版本和变更原因构成的可追溯变更记录。

#### Verbatim first output

````text
不能只在旧计划末尾加两节创业课。你从“就业”转向“一个月内开展 AI 咨询创业”，属于目标与评价场景的实质变化，旧计划应保留但暂停使用，重新从目标分析开始，并重算能力、项目、课程、路线图与每周计划。

目标链暂定为：

`AI 咨询创业目标 -> 客户与商业验证证据 -> 月度里程碑 -> 咨询交付与获客能力 -> 演示方案/试点项目 -> 必要课程依赖 -> 每周行动`

目前唯一需要先确认的问题是：**一个月后，你把哪种可验证结果视为成功——A. 完成明确报价、可演示方案、客户访谈和一次获客实验；还是 B. 必须签下至少一个付费试点客户？**

```yaml
engine_result:
  engine: goal-analysis
  run_id: goal-pivot-ai-consulting-20260714
  status: needs_input
  summary: 就业路线已发生目标转向，不能通过追加两节课完成适配；需先确认一个月创业目标的成功标准，再重建下游学习系统。
  inputs_used:
    - "学习者自述：原计划面向就业；现改为一个月内开展 AI 咨询创业。source: learner_self_report; confidence: high"
    - "学习者请求：在旧计划末尾追加两节创业课。source: learner_self_report; confidence: high"
  decisions:
    - "将本次变化识别为 goal_change，而非局部课程增补。source: inference_from_route_change; confidence: high"
    - "返回 Goal Analysis；旧计划暂不覆盖或删除，待新目标确认后再建立新内容版本。source: change_control_rule; confidence: high"
    - "创业路线的最低证据应包含客户问题、报价假设、可工作演示、交付边界、获客实验、基础单位经济与可信客户验证。source: entrepreneurship_outcome_contract; confidence: high"
    - "一个月期限可以支持有边界的市场验证实验，但不能据现有信息承诺签约或收入。source: feasibility_inference; confidence: medium"
  evidence_refs: []
  assumptions:
    - "尚未确认当前 AI 能力、咨询经验、客户资源、每周可用时间与预算。source: unknown; confidence: low"
    - "尚未确认成功标准是完成商业验证，还是取得付费客户。source: unknown; confidence: low"
  confidence: high
  artifacts_written: []
  affected_downstream:
    - gap-analysis
    - competency-design
    - curriculum-design
    - project-design
    - roadmap
    - weekly-planner
    - assessment
    - outcome-preparation
    - continuous-optimization
  gate:
    passed: false
    missing:
      - "一个月后可验证的成功标准：完成商业验证，或签下至少一个付费试点客户"
  next_action: "回答 A 或 B；若都不符合，请用一句话写出你希望一个月后拿出的可验证结果。"
```
````

### Observed fix

`references/goal-analysis.md` now requires every goal-change response to emit a compact change record naming the prior version, candidate version, `trigger: goal_change`, reason, and `affected_downstream`; unavailable identifiers must be `unknown`, not invented.

### Fresh retest

- **PASS** — 从 Goal Analysis 重新计算。证据：答复“回到目标分析后重算”，且 `engine: goal-analysis`。
- **PASS** — 重构能力、项目和结果准备，而不是追加课程。证据：“这不是‘补两节课’”，新目标链重建 Outcome Evidence、Competency Targets、Project Evidence、Curriculum Dependencies 和 Weekly Actions。
- **PASS** — 保留版本和变更原因。证据：“旧计划应保留并标记为被替代”，并输出 `change_record`：`prior_version: unknown`、`candidate_version: pending`、`trigger: goal_change`、`reason: 目标评价场景由就业转为创业`以及完整 `affected_downstream`。

#### Verbatim final output

````text
这不是“补两节课”，而是从就业转向创业的目标变更：成功证据已从“岗位胜任”变成“客户问题、可售卖方案、交付演示与需求验证”。旧计划应保留并标记为被替代，回到目标分析后重算能力、项目、课程和行动计划。

暂定目标链：

`Target Outcome -> Outcome Evidence -> Milestones -> Competency Targets -> Project Evidence -> Curriculum Dependencies -> Weekly Actions`

`一个月内完成 AI 咨询创业验证 -> 明确客户问题、可演示方案、报价与真实客户验证记录 -> 定位/方案/演示/获客实验 -> 诊断、方案设计、交付、销售验证 -> 一次可复现演示和一次客户访谈或试单证据 -> 依据能力缺口重建最小课程 -> 每周产出可验证成果`

下一步只需回答：**你准备服务哪一类客户，解决他们哪个具体且愿意付费的问题？**

```yaml
engine_result:
  engine: goal-analysis
  run_id: goal-pivot-ai-consulting-20260714
  status: needs_input
  summary: 就业路线已变更为一个月内验证 AI 咨询创业，不能通过在旧计划末尾追加课程处理。
  inputs_used:
    - source: learner_self_report
      statement: 原按就业路线学习，现决定一个月内做 AI 咨询创业。
  decisions:
    - target_route: entrepreneurship
      source: learner_self_report
      confidence: high
    - change_record:
        prior_version: unknown
        candidate_version: pending
        trigger: goal_change
        reason: 目标评价场景由就业转为创业
        affected_downstream:
          - gap-analysis
          - competency-design
          - curriculum-design
          - project-design
          - roadmap
          - weekly-planner
          - assessment
          - outcome-preparation
    - provisional_goal_chain: "Target Outcome -> Outcome Evidence -> Milestones -> Competency Targets -> Project Evidence -> Curriculum Dependencies -> Weekly Actions"
  evidence_refs: []
  assumptions:
    - statement: “一个月内”暂按截至 2026-08-14 理解。
      source: inference_from_current_date
      confidence: medium
    - statement: 当前尚未确定目标客户、付费问题和创业成功阈值。
      source: absence_in_learner_input
      confidence: high
  confidence: medium
  artifacts_written: []
  affected_downstream:
    - gap-analysis
    - competency-design
    - curriculum-design
    - project-design
    - roadmap
    - weekly-planner
    - assessment
    - outcome-preparation
  gate:
    passed: false
    missing:
      - 目标客户
      - 待解决的具体付费问题
      - 一个月后的成功证据与阈值
      - 旧目标或旧计划的版本标识
      - 每周可投入时间及关键约束
  next_action: 明确目标客户及其具体付费问题。
```
````

## theory-practice-gap

### Loaded inputs

- `learning-architect/SKILL.md`
- `learning-architect/references/persona.md`
- `learning-architect/references/philosophy.md`
- `learning-architect/references/workflow.md`
- `learning-architect/references/gap-analysis.md`
- `learning-architect/references/competency-engine.md`
- `learning-architect/references/curriculum-engine.md`
- `learning-architect/references/project-engine.md`
- `learning-architect/references/assessment-engine.md`
- `learning-architect/references/meta-learning-engine.md`

### Behavior scores

- **PASS** — 回退到对应能力和项目训练。证据：`rollback_to_gap_analysis`，并要求“先做一次诊断型项目”。
- **PASS** — 减少新理论并增加变式实践、调试和复盘。证据：“暂不安排更高级理论”，并安排“支架渐退、变式练习、调试、复盘和独立复测”。
- **PASS** — 不把失败归因为学习者懒惰。证据：答复将原因作为待验证的“迁移、调试或支架依赖问题”，没有人格或努力程度归因。

### Verbatim output

````text
暂不安排更高级理论。95 分测验只支持“理解较好”的判断，不能证明能独立交付；连续三次项目失败更可能暴露了迁移、调试或支架依赖问题，但具体原因仍需证据确认。

先做一次诊断型项目：对照示例完成关键步骤，随后逐步撤掉提示；加入需求变体和受控故障；最后在无帮助条件下重新交付，并复盘“卡点—原因—修正”。只有确认失败来自知识缺口时，才补最小必要理论。

请提供最近一次项目的任务要求、你的产出、卡住的位置，以及过程中接受过的提示或帮助。

```yaml
engine_result:
  engine: assessment
  run_id: assessment-20260714-theory-practice-gap-01
  status: needs_input
  summary: 暂停高级理论升级，先鉴别独立完成、迁移和调试环节的最早因果缺口。
  inputs_used:
    - input: 测验均为95分
      source: learner_self_report
      confidence: medium
    - input: 连续三次无法独立完成项目
      source: learner_self_report
      confidence: medium
  decisions:
    - decision: 测验成绩仅暂时支持理解层面，不作为独立项目能力证据
      source: learner_self_report
      confidence: high
    - decision: assessment_gate_fail
      reason: independent行为暂记为fail；其余关键行为缺少可解析证据
      source: learner_self_report_and_inference
      confidence: medium
    - decision: rollback_to_gap_analysis
      reason: 需重新校准当前能力基线，并定位最早因果缺口
      source: inference
      confidence: medium
    - decision: 采用示例对照、支架渐退、变式练习、调试、复盘和独立复测
      source: assessment_diagnosis
      confidence: medium
  evidence_refs: []
  assumptions:
    - assumption: 目标仍是独立完成同类真实项目
      source: inference_from_learner_request
      confidence: medium
  confidence: medium
  artifacts_written: []
  affected_downstream:
    - gap-analysis
    - curriculum-design
    - project-design
    - weekly-planner
  gate:
    passed: false
    missing:
      - 最近一次项目的任务要求与验收标准
      - 可检查的项目产出及失败记录
      - 独立完成过程中所获提示或帮助
      - explain、modify、debug、deploy、teach行为证据
  next_action: 提交最近一次项目的任务要求、产出、卡点及所获帮助，以完成一次最小诊断评估。
```
````

## Baseline comparison

| Scenario | Baseline | First post-Skill | Final post-Skill | Failure-mode change |
|---|---:|---:|---:|---|
| `direct-course-request` | 0/3 | 2/3 | 3/3 | Resource-first drift removed. The first post-Skill response correctly blocked the catalog but omitted the provisional-draft offer; the direct discovery output contract closed that observed gap. |
| `completion-is-not-capability` | 2/3 | 3/3 | 3/3 | Completion-as-capability drift removed: public capability claims are withheld, self-report is labeled, and performance evidence is requested. |
| `impossible-constraint` | 3/3 | 3/3 | 3/3 | Constraint denial remains absent; the response quantifies capacity, rejects an Offer promise, and exposes trade-offs. |
| `goal-pivot` | 2/3 | 2/3 | 3/3 | Incremental-plan drift remains absent, and the previously adjacent version-loss failure is now closed with an explicit change record. |
| `theory-practice-gap` | 3/3 | 3/3 | 3/3 | Theory escalation remains absent; project failure triggers causal rollback and guided-to-independent practice. |

## Final decision

**PASS — 15/15 required behaviors.** The first failed post-Skill observations and final passing observations are both retained above. No hypothetical rule was added: both reference changes correspond directly to a recorded first-run failure.
