# Learning Architect

[English](README.md)

**构建个性化学习系统，而不只是生成学习计划。**

Learning Architect 是一个结果导向（Outcome-Driven）的教育操作系统（Education OS）技能包（Skill），用于围绕真实结果——就业、晋升、创业或项目交付——设计、验证并持续优化学习者的成长路径。

它将学习视为能力建设。课程与资源只是可替换的输入；可观察的行为、真实项目、测评证据与可执行的练习，才是系统要交付的结果。

## 能做什么

- 采集可用于决策的学习者画像，包括约束、能力基线证据、动机与风险。
- 将目标结果拆解为能力模型、满足前置依赖的课程图谱、真实项目、里程碑、周度承诺与测评关卡。
- 保持路线可适应：目标、约束、测评和领域变化都会形成版本化更新，并重新验证受影响的下游产物。
- 区分自述、证据、推断与假设；不把课程完成、证书或出勤误认为能力证明。
- 内置首个 AI Agent 工程师领域包，并提供可复用的职业领域扩展契约。

## 工作流

```text
发现（Discovery）→ 目标分析 → 差距分析 → 能力设计
→ 课程设计 → 项目设计 → 路线图 → 周度计划
→ 阶段测评 → 结果准备 → 持续优化
```

每个阶段都有明确关卡。当证据缺失，或学习者尚不能独立完成目标行为时，系统会回到最早的因果缺口，而不是简单堆叠更多内容。

## 目录说明

| 位置 | 用途 |
| --- | --- |
| `learning-architect/SKILL.md` | 核心运行契约与工作流路由器 |
| `learning-architect/references/` | 发现、能力、课程、项目、测评、结果与优化等详细引擎 |
| `learning-architect/assets/schemas/` | 机器可读的学习系统数据契约 |
| `learning-architect/assets/templates/` | 学习者产物的起始模板 |
| `learning-architect/assets/domain-packs/ai-agent.yaml` | 初始 AI Agent 工程师领域包 |
| `learning-architect/scripts/validate_learning_system.py` | 离线学习系统产物验证器 |
| `tests/learning-architect/` | 回归测试与有效/无效样例 |

## 如何使用

安装到 Codex 后，直接用自然语言提出需求。例如：

> 我想在六个月内获得 AI Agent 工程师岗位。我每周可学习 12 小时，有基础 Python，希望采用项目优先的路径。请使用 Learning Architect。

Skill 会先提出仅会影响当前决策的必要问题，然后同时返回简明说明与可追溯的 `engine_result` 结构化状态。

## 验证方法

如需运行仓库回归验证，请在仓库根目录执行：

```bash
python3 "${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-creator/scripts/quick_validate.py" learning-architect
python3 -m unittest tests/learning-architect/test_validate_learning_system.py -q
python3 learning-architect/scripts/validate_learning_system.py \
  --skill-root learning-architect \
  --learner-dir tests/learning-architect/fixtures/valid-learner
```

当前测试集共 84 项，覆盖 Schema 验证、依赖环检测、证据引用、激活版本治理、项目契约与领域包评分关卡。

如需在没有仓库测试样例的情况下检查已安装副本的 Skill 结构（这不是完整回归测试），可运行：

```bash
SKILL_ROOT="${CODEX_HOME:-$HOME/.codex}/skills/learning-architect"
python3 "${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-creator/scripts/quick_validate.py" "$SKILL_ROOT"
```

## 扩展新的职业领域

新增职业时无需重写核心 Skill。只需添加版本化领域包，定义目标结果、能力种子、依赖关系、项目原型、证据要求与来源元数据；现有工作流与验证契约即可复用于新的职业路径。
