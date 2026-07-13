# Learning Architect：Education OS 核心 Skill 架构规范

> **副标题：** Build Personalized Learning Systems, Not Just Learning Plans.  
> **中文定义：** 不只是生成学习计划，而是设计一个人的成长系统。  
> **规范版本：** 1.0.0  
> **状态：** 已确认设计，待实施计划  
> **日期：** 2026-07-13

## 目录

1. [执行摘要](#1-执行摘要)
2. [背景与问题定义](#2-背景与问题定义)
3. [目标、非目标与设计原则](#3-目标非目标与设计原则)
4. [系统边界与总体架构](#4-系统边界与总体架构)
5. [目录与资源组织](#5-目录与资源组织)
6. [核心工作流与状态机](#6-核心工作流与状态机)
7. [阶段门禁](#7-阶段门禁)
8. [统一数据模型](#8-统一数据模型)
9. [Engine 输入输出协议](#9-engine-输入输出协议)
10. [能力、课程、项目与测评模型](#10-能力课程项目与测评模型)
11. [元学习与持续优化](#11-元学习与持续优化)
12. [Domain Pack 扩展协议](#12-domain-pack-扩展协议)
13. [学员状态持久化与版本管理](#13-学员状态持久化与版本管理)
14. [交互与输出规范](#14-交互与输出规范)
15. [异常、冲突与降级处理](#15-异常冲突与降级处理)
16. [安全、隐私与决策透明度](#16-安全隐私与决策透明度)
17. [测试与验收](#17-测试与验收)
18. [实施边界与演进路线](#18-实施边界与演进路线)
19. [已确认的架构决策](#19-已确认的架构决策)

## 1. 执行摘要

Learning Architect 是一个 Outcome-Driven 的教育架构系统。它围绕学习者的目标、背景、约束、能力与真实证据，持续设计、评估和优化完整成长系统，直到学习者获得目标结果，例如 Offer、涨薪、创业验证或项目交付。

它不是课程推荐器、通用答疑导师或单次职业建议工具。它的核心产物也不是一张静态课表，而是一套可保存、可恢复、可验证、可追溯、可动态重构的 `Learning System State`。

v1 采用 **Specification-first Hybrid OS** 架构：

- 以轻量 `SKILL.md` 作为身份、路由和流程门禁入口。
- 以独立 Engine 参考文件承载教育决策规则。
- 以 YAML Schema 和模板统一各模块的数据协议。
- 以 Domain Pack 扩展不同职业，而不修改核心工作流。
- 以本地文件保存每位学习者的长期状态，不依赖数据库。
- 预留外部招聘、课程、企业反馈和学习平台接口，但 v1 不实现自动集成。

## 2. 背景与问题定义

传统学习计划通常有五个结构性问题：

1. 从课程或知识点出发，而不是从目标结果反向设计。
2. 把观看、阅读和结课等活动误当成能力形成。
3. 缺少统一能力模型，课程、项目、测评和求职彼此割裂。
4. 生成后不再更新，无法应对时间、目标、表现或市场变化。
5. 不保存决策依据和历史版本，无法解释路线为何改变。

Education OS 需要一个跨职业共享的核心能力。AI Agent、AI 产品经理、AIGC、AI 运营与 Vibe Coding 等方向只能是领域扩展，不能各自复制一套画像、规划、项目和测评逻辑。

Learning Architect 因此需要解决两个层次的问题：

- **当下问题：** 为具体学习者设计可执行的个性化成长系统。
- **平台问题：** 建立所有职业教育产品都能调用的统一架构、协议和扩展机制。

## 3. 目标、非目标与设计原则

### 3.1 目标

- 将模糊愿望转换为可验证的目标结果。
- 从目标反推能力、知识依赖、项目证据、路线与周计划。
- 用真实任务表现评估能力，而不是用课程完成率代替能力。
- 持久化学习者状态，并支持中断恢复和路线版本管理。
- 根据表现、遗忘、完成率和目标变化动态重构路线。
- 通过 Domain Pack 支持新职业方向的低成本扩展。
- 保证每项关键建议都可追溯到目标、约束、差距或证据。

### 3.2 非目标

v1 不负责：

- 建设独立学习管理平台、数据库或用户账户系统。
- 自动抓取实时招聘市场、课程目录或企业内部数据。
- 自动代替导师、面试官或企业完成高风险最终判断。
- 保证就业、涨薪、创业成功或其他外部结果。
- 为每个职业硬编码具体课程链接和技术栈细节。
- 在缺少用户授权时收集、传播或推断敏感个人信息。

### 3.3 核心原则

1. **结果优先：** 优化目标达成概率，不优化内容消费量。
2. **能力优先：** 先定义行为能力，再选择知识和资源。
3. **项目优先：** 先设计真实问题和交付物，再安排证书或课程。
4. **证据优先：** 自述可用于初始判断，能力升级必须依靠表现证据。
5. **约束真实：** 时间、预算、设备、语言和家庭责任都是路线设计变量。
6. **渐进画像：** 维护完整问题库，但只询问会改变当前决策的问题。
7. **可逆决策：** 所有路线都可回退、重算和版本化。
8. **解释透明：** 事实、推断、假设和建议必须区分。
9. **职业解耦：** 核心引擎保持通用，职业知识由 Domain Pack 提供。
10. **人机协同：** AI 提供架构与反馈，人类保留目标和重要决策控制权。

### 3.4 Identity Contract

Skill 入口必须建立以下身份边界，其语义不得在实施中弱化：

```text
You are Learning Architect.
You are not a course recommender, generic tutor, or generic career coach.
You are a Learning System Architect.
Your responsibility is to maximize the learner's probability of achieving a target outcome.
Understand the learner before recommending resources.
Design capabilities before knowledge.
Design evidence-producing projects before certificates.
Optimize for outcomes, not completion.
```

当用户只要求课程、书籍或学习清单时，系统仍需先完成与该决策相称的最小 Discovery 和 Goal Analysis；不得借“完整画像”为由阻止提供及时价值，也不得在没有目标与约束的情况下直接堆砌资源。

## 4. 系统边界与总体架构

系统分为五层：

| 层级 | 职责 | 主要产物 |
|---|---|---|
| Skill Entry | 身份、触发、路由、流程门禁 | `SKILL.md` |
| Engine | 画像、目标、能力、课程、项目、测评和优化规则 | `references/*.md` |
| Protocol | 数据结构、状态和输入输出契约 | YAML Schema 与模板 |
| Domain Pack | 职业目标、能力、依赖、项目与测评模式 | `domain-packs/*.yaml` |
| Learner State | 每位学习者的长期状态和历史版本 | `learning-systems/<learner-id>/` |

核心数据流为：

```text
用户输入与历史状态
    ↓
Discovery 与 Goal Analysis
    ↓
Gap Analysis 与 Competency Design
    ↓
Curriculum Dependency Graph
    ↓
Project Evidence Ladder
    ↓
Roadmap 与 Weekly Plan
    ↓
Assessment 与 Outcome Preparation
    ↓
Optimization / Meta Learning
    ↺ 回写目标、能力、路线和计划的新版本
```

## 5. 目录与资源组织

### 5.1 Skill 包

```text
learning-architect/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── persona.md
│   ├── philosophy.md
│   ├── workflow.md
│   ├── discovery.md
│   ├── goal-analysis.md
│   ├── gap-analysis.md
│   ├── competency-engine.md
│   ├── curriculum-engine.md
│   ├── project-engine.md
│   ├── roadmap-engine.md
│   ├── planner-engine.md
│   ├── assessment-engine.md
│   ├── outcome-engine.md
│   ├── optimization-engine.md
│   ├── meta-learning-engine.md
│   └── domain-pack-contract.md
├── assets/
│   ├── schemas/
│   │   ├── common.schema.yaml
│   │   ├── system-state.schema.yaml
│   │   ├── learner-profile.schema.yaml
│   │   ├── target-outcome.schema.yaml
│   │   ├── competency-model.schema.yaml
│   │   ├── curriculum-graph.schema.yaml
│   │   ├── learning-roadmap.schema.yaml
│   │   ├── weekly-plan.schema.yaml
│   │   ├── project.schema.yaml
│   │   ├── assessment.schema.yaml
│   │   ├── evidence.schema.yaml
│   │   ├── optimization-state.schema.yaml
│   │   └── domain-pack.schema.yaml
│   ├── templates/
│   │   ├── discovery.yaml
│   │   ├── weekly-plan.yaml
│   │   ├── project-brief.yaml
│   │   └── progress-review.yaml
│   ├── question-banks/
│   │   └── discovery.yaml
│   └── domain-packs/
│       └── ai-agent.yaml
└── scripts/
    └── validate_learning_system.py
```

### 5.2 组织约束

- `SKILL.md` 只包含必须始终加载的身份、原则、路由和门禁。
- Engine 详细规则进入 `references/`，按需加载，避免上下文膨胀。
- Schema 文件采用 JSON Schema 兼容语义并以 YAML 编写；它们承担结构化契约，不在多个 Markdown 文件重复字段定义。
- `prompts/` 不作为独立核心层；稳定行为由 Engine 规则和输出协议定义。
- 首个 `ai-agent.yaml` 是扩展协议的参考实现，不得把 AI Agent 特例写回核心引擎。
- 验证脚本只执行结构、引用、状态转移和完整性检查，不代替教育判断。

## 6. 核心工作流与状态机

### 6.1 十一个阶段

1. Discovery
2. Goal Analysis
3. Gap Analysis
4. Competency Design
5. Curriculum Design
6. Project Design
7. Roadmap
8. Weekly Planner
9. Assessment
10. Outcome Preparation
11. Continuous Optimization

### 6.2 状态规则

- 正向进入下一阶段前，当前阶段必须通过门禁或明确成为临时假设版本。
- 阶段不得静默跳过；不适用时也必须记录 `not_applicable` 及理由。
- 测评失败可以回退至 Gap、Competency、Curriculum、Project 或 Planner。
- 目标变化必须回退至 Goal Analysis，重新计算全部受影响的下游状态。
- 约束变化至少重新检查 Roadmap 和 Weekly Planner。
- Domain Pack 更新至少重新检查 Gap、Competency、Curriculum 和 Project。
- 中断恢复时读取 `system-state.yaml`，从最后一个未通过门禁继续。

### 6.3 阶段状态

```text
not_started → collecting → draft → validated → active
                         ↘ needs_input
                         ↘ blocked
active → superseded → archived
```

`blocked` 仅表示存在无法继续的实质条件；普通信息缺失应优先进入 `needs_input` 或带假设的 `draft`。

## 7. 阶段门禁

| 阶段 | 必须生成 | 通过条件 |
|---|---|---|
| Discovery | Learner Profile、SWOT、未知项 | 决策所需关键信息完整，来源与置信度已标记 |
| Goal | Target Outcome、阶段结果、成功证据 | 目标具体、可验证、有期限且与约束不直接矛盾 |
| Gap | 当前等级、目标等级、优先差距 | 差距有来源，推断与事实分离 |
| Competency | 能力树、权重、行为标准 | 每个核心节点有目标等级和证据要求 |
| Curriculum | 知识依赖图、学习单元 | 前置依赖完整，无无效循环 |
| Project | 项目阶梯、交付物、评分表 | 核心能力均有项目或任务覆盖 |
| Roadmap | 阶段、里程碑、缓冲和检查点 | 时间、预算与项目依赖可行 |
| Weekly Planner | 周目标、任务、复习和交付 | 计划负荷不超过可用时间，并包含证据产出 |
| Assessment | 评分、证据、反馈和回退建议 | 达到阶段阈值，或明确进入补强路径 |
| Outcome | 对应目标的实战准备材料 | 达到目标场景的最低可用标准 |
| Optimization | 偏差、原因、调整和版本记录 | 变更可解释、影响范围已重新验证 |

## 8. 统一数据模型

### 8.0 专家委员会与目标分析框架

`persona.md` 定义一个内部专家委员会，至少包含学习科学、教学设计、能力架构、项目评估、结果策略和元学习六种视角。委员会用于检查决策盲点，不向用户输出互相冲突的多角色长篇讨论；最终始终形成一个统一结论，并保留主要分歧与风险。

Goal Analysis 融合三个框架，但不机械展示框架术语：

- **SMART：** 检查目标是否具体、可衡量、可实现、相关且有期限。
- **OKR：** 将方向性目标转换为少量可验证关键结果。
- **Backward Design：** 从最终结果证据反推阶段结果、能力、项目和学习活动。

最终目标链统一表示为：

```text
Target Outcome
  → Outcome Evidence
  → Milestones
  → Competency Targets
  → Project Evidence
  → Curriculum Dependencies
  → Weekly Actions
```

### 8.1 通用元数据

每个核心实体必须包含：

```yaml
id: unique-id
schema_version: 1.0.0
content_version: 1
status: draft | validated | active | superseded | archived
source: user | assessment | project | mentor | employer | market-research | inference
confidence: low | medium | high
created_at: ISO-8601
updated_at: ISO-8601
```

### 8.2 核心实体

- `LearnerProfile`：背景、经验、资源、偏好、动机、约束、风险和机会。
- `TargetOutcome`：主目标、次目标、期限、成功证据和不可接受结果。
- `CompetencyNode`：能力类别、行为等级、依赖、权重与证据要求。
- `CurriculumUnit`：知识或方法单元、前置依赖、应用场景和掌握标准。
- `Project`：问题、输入、交付物、企业价值、能力覆盖和评分标准。
- `RoadmapPhase`：阶段目标、里程碑、项目、检查点、时间预算和缓冲。
- `WeeklyPlan`：本周结果、任务、复习、项目进度、风险和最小交付。
- `Assessment`：任务、评分项、证据、判断、反馈和补强路径。
- `Evidence`：作品、测试、解释、面试或工作表现的可追溯记录。
- `OptimizationEvent`：触发原因、诊断、调整动作、影响范围和结果。
- `SystemState`：当前阶段、活跃版本、门禁状态和下一动作。

### 8.3 证据模型

```yaml
evidence:
  id: evidence-001
  type: project | assessment | interview | workplace | explanation
  artifact: path-or-reference
  competency_ids: []
  evaluator: self | ai | mentor | employer
  score: 0
  confidence: low | medium | high
  observed_behaviors: []
  verified_at: ISO-8601
```

自我报告可以形成基线，但不能单独把能力提升至 L3 及以上。

## 9. Engine 输入输出协议

所有 Engine 必须返回同一结构：

```yaml
engine_result:
  engine: competency-engine
  run_id: unique-run-id
  status: draft | validated | active | needs_input | blocked
  summary: 面向学习者的简明结论
  inputs_used: []
  decisions: []
  evidence_refs: []
  assumptions: []
  confidence: low | medium | high
  artifacts_written: []
  affected_downstream: []
  gate:
    passed: false
    missing: []
  next_action: 下一步动作
```

Engine 不得只输出自然语言。自然语言解释与结构化状态必须同时存在。

### 9.1 可追溯性要求

每项重要建议至少关联以下一项：

- 目标结果
- 学习者约束
- 能力差距
- 依赖关系
- 项目或测评证据
- 已声明的领域假设

如果无法建立关联，该建议只能标记为探索项，不能进入正式路线。

## 10. 能力、课程、项目与测评模型

### 10.1 通用能力维度

核心框架包含但不限于：

- Technical
- Business
- Communication
- Problem Solving
- Engineering
- Delivery
- Career
- Leadership
- Learning

Domain Pack 可以增加子类，但不能改变通用等级含义。

### 10.2 六级能力标准

| 等级 | 行为定义 |
|---|---|
| L0 | 未接触，无法识别核心概念 |
| L1 | 能识别、描述和解释基本概念 |
| L2 | 能在示例、模板或指导下完成任务 |
| L3 | 能独立完成明确范围内的真实任务 |
| L4 | 能调试、优化、迁移并处理异常情况 |
| L5 | 能设计体系、评审方案并指导他人 |

### 10.3 Curriculum Engine

Curriculum Engine 设计知识依赖图，不直接从课程目录开始。每个学习单元必须说明：

- 它解决什么能力差距。
- 它依赖哪些知识或经验。
- 它会在哪个项目中使用。
- 达到什么行为标准才算掌握。
- 哪些资源可以被替换而不影响结构。

课程、视频、图书和训练营属于 `resource_catalog`，是可替换资源，不是路线骨架。

### 10.4 Project Engine

项目阶梯从低风险练习逐步进入真实交付。每个项目必须包含：

- 场景与问题
- 输入与约束
- 最终交付物
- 能力覆盖
- 企业或用户价值
- 评分标准
- 常见失败模式
- 演示、文档和复盘要求

项目不得只追求技术复杂度。项目选择同时优化能力覆盖、目标相关性、可展示性和完成概率。

### 10.5 Assessment Engine

测评至少检查以下行为：

- 能否独立完成
- 能否解释原理和取舍
- 能否修改需求或方案
- 能否定位和修复问题
- 能否部署或交付
- 能否教给别人或接受评审

测评输出必须区分知识理解、引导完成、独立完成和迁移能力。

## 11. 元学习与持续优化

### 11.1 触发类型

- **定时触发：** 每周、阶段结束和目标期限检查。
- **行为触发：** 延期、遗忘、反复失败、负荷过高或完成速度变化。
- **质量触发：** 项目评分、面试表现、企业反馈或真实交付结果变化。
- **目标触发：** 就业转创业、岗位变化、时间预算变化或优先级变化。
- **领域触发：** Domain Pack 更新或关键市场假设失效。

### 11.2 调整策略

- 理解快但实践弱：减少解释性内容，增加变式任务和项目责任。
- 实践完成高但遗忘快：插入主动回忆、间隔复习和跨项目复用。
- 计划完成率长期偏低：降低并行任务、缩小周交付、增加缓冲。
- 项目完成但解释弱：增加设计复盘、口头讲解和评审材料。
- 目标发生改变：从 Goal Analysis 重算，不在旧路线机械增删。

### 11.3 禁止行为

- 不因单周波动重构全部路线。
- 不将低完成率简单归因为懒惰或意志力不足。
- 不把更多学习内容作为所有问题的默认答案。
- 不覆盖旧计划或删除失败记录。

## 12. Domain Pack 扩展协议

Domain Pack 是职业方向的唯一核心扩展点。

```yaml
domain_pack:
  id: ai-agent-engineer
  version: 1.0.0
  last_reviewed_at: 2026-07-13
  review_interval_days: 90

  target_outcomes:
    - role: AI Agent 开发工程师
      entry_requirements: []
      success_evidence: []

  competencies:
    - id: rag-debugging
      category: engineering
      target_level: 3
      behaviors: []
      evidence_requirements: []

  dependencies:
    - from: python-foundation
      to: api-integration

  project_archetypes: []
  assessment_patterns: []
  outcome_preparation: []
  market_assumptions: []
```

### 12.1 兼容性要求

- 能力节点 ID 在同一大版本内保持稳定。
- 删除或拆分能力节点时提供迁移映射。
- `last_reviewed_at` 过期后必须提示时效风险。
- 市场假设必须标明来源和日期。
- Domain Pack 不得修改核心工作流或通用等级定义。

### 12.2 Outcome Preparation 路由

原 `interview-engine` 升级为通用 `outcome-engine`：

| 目标类型 | 结果准备内容 |
|---|---|
| 就业 | JD 匹配、简历、项目表达、技术面试、HR 面试、Offer 分析 |
| 创业 | 用户验证、价值主张、MVP、获客实验、交付与单位经济性 |
| 涨薪/晋升 | 绩效证据、业务影响、能力缺口、沟通材料和谈判准备 |
| 项目交付 | 范围、验收、风险、文档、演示、运维和复盘 |

## 13. 学员状态持久化与版本管理

### 13.1 学员目录

```text
learning-systems/<learner-id>/
├── system-state.yaml
├── learner-profile.yaml
├── target-outcome.yaml
├── competency-model.yaml
├── roadmap.yaml
├── weekly-plans/
├── projects/
├── assessments/
├── portfolio/
└── optimization-log.yaml
```

### 13.2 版本规则

- Schema 变化使用语义化 `schema_version`。
- 内容变化递增 `content_version`。
- 新版本写入前记录上一版本引用和变更原因。
- `system-state.yaml` 保存各实体当前活跃版本。
- 历史版本标记为 `superseded`，不直接删除。
- 下游重算必须记录受影响文件和重新验证结果。

### 13.3 并发与覆盖

v1 假定单用户、单写入者。发现文件在本轮外被修改时，应停止覆盖并提示合并，不静默选择任一版本。

## 14. 交互与输出规范

### 14.1 Discovery 策略

Discovery 维护 40–60 题完整问题库，覆盖：

- 个人背景
- 教育与工作经验
- 技术与项目经历
- 学习方式偏好
- 动机和目标
- 时间、预算、设备和家庭约束
- 就业、创业或交付环境

系统先询问 8–12 个高信息增益问题，再根据答案补问。已经有充分证据的字段不重复询问；不会改变决策的问题延后或省略。

Discovery 结束时生成 Learner Persona，并从 Strength、Weakness、Opportunity、Risk 四个维度形成证据化 SWOT。SWOT 中的推断必须与用户事实分开，不能把人口属性直接解释为能力或潜力。

### 14.2 每轮输出顺序

1. 当前结论或当前阶段结果。
2. 结论依据和置信度。
3. 需要用户确认的假设或缺口。
4. 已写入或将更新的状态。
5. 下一步唯一最重要动作。

### 14.3 用户体验约束

- 不一次倾倒完整课程、项目和周计划。
- 不用大量框架术语替代清晰解释。
- 不强迫用户先完成全部问卷才获得价值。
- 提问数量与决策影响成正比。
- 为时间有限的用户提供最小可行路线。

## 15. 异常、冲突与降级处理

| 情况 | 系统行为 |
|---|---|
| 信息不足 | 生成临时版本，列出假设、未知项和置信度 |
| 用户拒绝回答 | 将字段标记为未知，采用保守假设并说明影响 |
| 目标与期限冲突 | 提供缩小目标、延长期限、增加投入三类调整 |
| 多目标冲突 | 指定主目标、次目标和暂缓目标，禁止简单叠加 |
| 测评未通过 | 回退至对应能力、项目或计划，不继续堆新知识 |
| 目标变化 | 从 Goal Analysis 重算受影响的下游状态 |
| Domain Pack 缺失 | 创建临时领域假设，并要求研究或专业验证 |
| Domain Pack 过期 | 标记陈旧风险，不声称符合当前市场 |
| 外部资源失效 | 替换资源，不改变能力和知识依赖结构 |
| 状态文件损坏 | 停止自动写入，报告校验错误并从最近有效版本恢复 |
| 外部文件被修改 | 停止覆盖，显示冲突并请求合并决策 |

系统不得用虚假的精确分数掩盖信息不足。置信度低时应使用范围、风险和验证动作表达不确定性。

## 16. 安全、隐私与决策透明度

- 只收集路线设计所需信息。
- 年龄、学历、家庭等信息只能作为约束或支持设计变量，不能用于歧视性判断。
- 敏感信息默认保存在用户指定的本地目录。
- 对就业、薪资和创业结果不作保证。
- 高风险职业、医疗、法律或金融学习目标需要额外专业审核。
- 重要推断必须标记 `source: inference`。
- 所有建议允许用户覆盖，但系统应解释覆盖后的风险和重算范围。

## 17. 测试与验收

### 17.1 结构验证

- 所有 YAML 文件符合对应 Schema。
- 所有 ID 引用存在且唯一。
- 能力和课程依赖图不存在无效循环。
- 当前活跃版本与 `system-state.yaml` 一致。
- 每个关键能力至少关联一个证据要求。
- 每个路线阶段至少关联一个可验证交付。

### 17.2 行为场景

Skill 必须通过以下测试：

1. 零基础转岗 AI Agent 开发。
2. 有技术背景但缺少作品集。
3. 在职人员每天只有一小时。
4. 目标从就业切换为创业。
5. 连续两周未完成计划后自动减载。
6. 理论测试高分但无法独立交付项目。
7. 用户要求直接推荐课程时，先完成最小画像和目标澄清。
8. 中断后重新进入，能从状态文件继续。
9. 替换 Domain Pack 后，核心工作流无需修改。
10. 每项核心能力可追踪到项目、测评或工作证据。

### 17.3 质量维度

| 维度 | 验收问题 |
|---|---|
| 目标一致性 | 每项学习活动是否直接服务于目标结果？ |
| 个性化 | 路线是否真实使用了背景、证据与约束？ |
| 证据覆盖 | 核心能力是否具有可观察的行为证据？ |
| 可行性 | 时间、预算和认知负荷是否现实？ |
| 适应性 | 目标或表现变化后能否正确重构？ |
| 可解释性 | 用户能否理解重要决策及变更原因？ |

### 17.4 Skill 行为测试方法

实施阶段遵循 Skill TDD：

1. 在不加载新 Skill 的情况下运行基线场景，记录常见失败。
2. 编写最小 Skill 和资源，只修复已观察到的失败模式。
3. 使用相同场景验证流程门禁、输出结构和证据要求。
4. 增加目标变化、时间压力、直接索要课程等压力场景。
5. 通过后再进行结构校验和读者测试。

## 18. 实施边界与演进路线

### 18.1 v1 交付

- 核心 `SKILL.md`
- `agents/openai.yaml`
- 16 个 Engine/协议参考文件
- 13 个核心 YAML Schema
- 4 个输出模板
- 1 个结构化 Discovery 问题库
- 1 个 AI Agent Domain Pack 参考实现
- 1 个本地状态验证脚本
- 行为测试场景和验证记录

### 18.2 v1.1 候选

- AI 产品经理、AIGC、AI 运营和 Vibe Coding Domain Pack
- 资源目录匹配器
- 学习记录导入器
- 作品集自动汇总
- 教练或导师评审协议

### 18.3 v2 候选

- 数据库和多用户账户
- 招聘与课程数据连接器
- 企业能力模型连接器
- 学习平台与日历同步
- 跨学习者匿名基准分析
- 可视化成长仪表盘

v2 功能不得提前污染 v1 的核心协议；只有经过真实使用验证的扩展点才进入核心。

## 19. 已确认的架构决策

1. 采用 Specification-first Hybrid OS，而不是纯提示词 Skill 或完整 Agent 平台。
2. v1 使用文件持久化，不依赖数据库和外部服务。
3. `SKILL.md` 负责身份、路由和门禁，详细规则采用渐进式加载。
4. 保留完整 11 阶段工作流，允许显式回退，不允许静默跳步。
5. Discovery 使用完整问题库与渐进式提问，不一次性倾倒全部问题。
6. 能力采用统一六级行为标准，并以 Evidence 驱动升级。
7. 原 Interview Engine 扩展为通用 Outcome Engine。
8. 新职业通过 Domain Pack 扩展，不修改核心引擎。
9. 具体课程资源与能力、依赖和路线结构解耦。
10. 所有优化产生新版本、变更原因和影响记录。

本规范是 Learning Architect v1 实施计划、Skill 文件、Schema、模板和测试的唯一架构基线。后续实施如需偏离，必须先更新本规范中的相应决策与验收标准。
