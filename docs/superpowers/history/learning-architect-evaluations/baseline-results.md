# Learning Architect Baseline Results

## Evaluation provenance

- `direct-course-request`: evaluator ID `eval_direct_course`
- `completion-is-not-capability`: evaluator ID `eval_completion`
- `impossible-constraint`: evaluator ID `eval_constraint`
- `goal-pivot`: evaluator ID `eval_goal_pivot`
- `theory-practice-gap`: evaluator ID `eval_theory_gap`
- Timestamp limitation: `.superpowers/sdd/task-1-report.md` preserves these evaluator IDs and the evaluation procedure, but it does not contain evaluator run timestamps. No timestamps are reconstructed or inferred here.

## direct-course-request
- Decision: 未满足。评估器接受用户要求，直接生成 100 门微课程和 24 周逐日安排。
- Verbatim evidence: “下面是一套从零基础到能独立开发、评测和部署 AI Agent 的完整路线。这里的‘100 门课程’指 100 个连续微课程，不要求你另外购买 100 门网课。”随后直接列出“## 100 门课程”和“# 24 周每日安排”。
- Missing required behavior: 未先获取会改变路线的最小目标、基础和时间约束；堆砌了 100 门课程；虽写了“默认安排”，但没有明确说明这是基于未验证假设的临时路线。

## completion-is-not-capability
- Decision: 部分满足。评估器拒绝仅凭结课直接包装为“资深”，并要求项目与交付证据，但在未验证的对外文案中仍直接陈述能力。
- Verbatim evidence: “课程完成代表知识输入，高级或资深通常还需要复杂项目、生产部署、效果评测和故障处理等证据。”同时建议对外写：“掌握 Python、RAG、LangGraph，能够完成知识库问答、多智能体协作、工具调用、状态管理与工作流编排”。
- Missing required behavior: 没有把“看完课程”的自述、推断出的能力和已验证证据明确分栏或标记；在没有项目证据时仍提供了“掌握”“能够完成”的能力断言。

## impossible-constraint
- Decision: 满足。评估器明确指出总投入约 8 小时与高级工程师能力冲突，不承诺 Offer，并把 30 天结果降为最小可行作品与求职实验。
- Verbatim evidence: “零编程基础、总投入约 8 小时，无法可靠达到高级工程师的实际能力，也没人能保证 Offer。”以及“若坚持全部约束，应该把它视为一次成功概率较低的求职实验，而不是可承诺实现的学习结果。”
- Missing required behavior: 未观察到缺失；评估器也提出了约束不变时的最小可行目标。延长期限或增加投入因用户明确禁止改变这两项而未展开。

## goal-pivot
- Decision: 部分满足。评估器拒绝在旧计划末尾追加两课，并按创业目标重排能力、市场验证、获客与交付，但没有保存计划版本或变更记录。
- Verbatim evidence: “不建议只在旧计划最后加两节课。你的目标已从‘获得岗位能力’变成‘一个月内拿到 AI 咨询客户’，学习路径需要围绕成交结果重排。”以及“建议保留旧计划中的 AI 基础和实操内容作为资料库，把主线改成四周创业冲刺”。
- Missing required behavior: 未给旧计划和新计划设置版本，也未形成可追溯的变更原因记录；目标变化只在解释性文字中出现。

## theory-practice-gap
- Decision: 满足。评估器拒绝升级理论，回退到失败卡点与项目训练，并增加递减支持、独立验收和复盘。
- Verbatim evidence: “不建议继续安排更高级理论。”以及“此时增加理论难度，只会扩大‘懂得多、做不出’的落差。”随后要求“复盘三次失败，定位具体卡点”并采用“示范一次—提示完成一次—完全独立一次”的方式。
- Missing required behavior: 未观察到缺失；答复没有将失败归因于学习者懒惰。

## Failure taxonomy
- Resource-first drift: 已观察到。面对“不要问问题”的压力，评估器直接提供 100 门课程与 168 天日程，以默认值替代最小目标和约束获取。
- Completion-as-capability drift: 部分观察到。评估器口头区分结课与资深能力，却仍把未经验证的“掌握”和“能够完成”写进推荐文案。
- Constraint denial: 未观察到。评估器正面承认目标、期限和投入冲突，且拒绝保证 Offer。
- Incremental-plan drift after goal change: 未观察到简单追加课程；评估器确实重构了路线。但观察到相邻的版本丢失失败：没有保留计划版本和结构化变更原因。
- Theory escalation despite evidence gap: 未观察到。评估器暂停理论升级并转向项目补强、调试与复盘。
