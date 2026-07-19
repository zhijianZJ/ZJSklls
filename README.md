# ZJSkills

[English](README.en.md)

**版本 [2.0.0](VERSION) · 87 tests 核心回归 / 105 tests 总计 · MIT**

把模糊的学习目标转化为可验证、可调整的个性化学习系统。

## 它解决什么问题

课程清单通常不会回答三个关键问题：目标究竟需要哪些能力、当前差距有什么证据、条件变化后应该从哪里重算。ZJSkills 从目标、基础、时间和约束出发，设计能力模型、项目阶梯、阶段路线、周度行动与评估关卡，并把事实、自述、证据、推断和假设分开记录。

开始学习后，它还能处理“看不懂、不会做、遇到报错、不知道第一步、没有完成计划”等真实问题：先进行问题拆解，给出一个最小行动和完成标志，再判断是否需要调整任务、本周计划、整体路线或目标系统。

它帮助你提高学习决策、能力证据和持续调整的质量，但不保证 Offer、转岗、晋升、收入或其他由外部主体决定的结果。

## 快速开始

在支持 Skills 的 AI 工具中启用 `ZJSkills`。2.0.0 起，底层目录和显式调用标识统一为 `zjskills`：Codex 使用 `$zjskills`，Claude Code 使用 `/zjskills`。如果你还不知道要问什么，直接发送“使用 ZJSkills”，它会显示下面的入口。

### ZJSkills 学习导航

1. 了解 AI 行业，判断适合的方向
2. 制定 AI 学习或转行路线
3. 安排今天或本周学习任务
4. 解决学习中遇到的问题
5. 时间、目标或情况变了，调整原计划
6. 继续上次的学习进度

回复数字，或直接用自己的话描述需求。默认采用**新手模式**：一次只呈现一个主要行动、完成标志和备用办法；你也可以随时要求“切换到标准模式”或“切换到专业模式并显示证据和结构化状态”。已经明确描述问题时，Skill 会直接处理，不会强制先走菜单。

也可以直接说明目标与约束：

```text
请使用 ZJSkills 帮我设计个性化学习系统。
我的目标是：在六个月内具备 AI Agent 工程师岗位所需的可验证能力。
我的基础是：会使用 Python 完成基础脚本。
我每周可投入：12 小时。
我的主要约束是：预算有限，希望项目优先。
请先询问会改变路线的关键信息，不要直接推荐课程。
```

第一次使用、继续规划和重新规划的提示词见[新手入门](docs/getting-started.md)。

## 学习中遇到问题

不需要重新描述整套背景，也不用懂任何技术术语。直接告诉它：

```text
请使用 ZJSkills 继续陪我学习。我卡住了：[用自己的话描述问题]。
请先判断我最早卡在哪一步。简单问题直接给我现在只做的一步、完成标志和备用办法；复杂问题每次只问我一个关键问题。最后说明是否需要调整原计划。
```

如果不知道怎么描述，只说“我卡住了，不知道问题在哪里”也可以。Skill 会提供少量通俗选项或一个很小的验证任务，而不是一次抛出长教程和完整问卷。

## 安装

ZJSkills 支持 Codex、Claude Code 和 Tencent WorkBuddy 的原生或兼容 Skill 接入；豆包使用明确标注的对话接入模式。各平台能力、macOS/Linux 与 Windows 安装命令、升级、卸载和验收步骤见[多平台安装与使用指南](docs/platform-installation.md)。

Codex 用户可先获取仓库，并在仓库根目录执行用户级安装：

```bash
git clone https://github.com/zhijianZJ/ZJSkills.git
cd ZJSkills
(
  set -e
  skills_dir="$HOME/.agents/skills"
  destination="$skills_dir/zjskills"
  if [ -e "$destination" ]; then
    echo "安装已停止：$destination 已存在，请先备份或选择升级流程。" >&2
    exit 1
  fi
  mkdir -p "$skills_dir"
  cp -R ./zjskills "$skills_dir/"
  test -f "$destination/SKILL.md"
)
```

整个括号命令没有报错且退出状态为 0，表示目标原本不存在且 `SKILL.md` 已复制成功；如果目标已存在，它会停止而不会复制。安装后请新建任务，并使用 `$zjskills` 或直接要求使用 `ZJSkills`。Claude Code 请安装到 `~/.claude/skills/zjskills` 并使用 `/zjskills`；Tencent WorkBuddy 请优先从技能界面导入本地目录；豆包不应按本地原生 Skill 描述，具体操作见多平台指南。

升级时不要把新目录直接合并进旧目录。先把已安装目录移到你指定的备份位置，再复制新版本；验证无误前保留备份，避免覆盖本地修改。卸载只需在确认不再需要本地修改后移走已安装目录。

维护者与贡献者可在仓库根目录验证完整项目：

```bash
python3 "${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-creator/scripts/quick_validate.py" zjskills
python3 -m unittest discover -s tests/zjskills -p "test_*.py" -q
python3 zjskills/scripts/validate_learning_system.py --skill-root zjskills --learner-dir tests/zjskills/fixtures/valid-learner
```

验证器需要 Python 3.9+，以及 `PyYAML`、`jsonschema` 和 `referencing`。第一条命令依赖 Codex 内置的 `skill-creator`；没有该路径时可运行后两条仓库验证命令。

## 你会得到什么

- 一份包含目标、基础证据、容量、约束与风险的学习者画像；
- 从目标结果反推的能力树与前置依赖；
- 以真实产物和评分标准为核心的项目阶梯；
- 分阶段路线、下一周计划与明确的通过关卡；
- 学习中问题的一步步拆解、最小行动、完成标志与后续追踪；
- 可追溯的结构化状态，以及在目标、约束或证据变化后的版本化更新；
- 可复用的 Domain Pack 契约，仓库内置 AI Agent 工程师领域包。

## 工作方式

```text
发现 → 目标分析 → 差距分析 → 能力设计 → 课程设计
→ 项目设计 → 路线图 → 周度计划 → 阶段测评 → 结果准备 → 持续优化
```

每个阶段都有进入条件、产物与关卡。证据不足时，系统会标记假设或请求补充信息；项目或测评未通过时，它会定位最早的因果缺口，只重算受影响的下游部分。

学习陪跑是贯穿执行过程的横向循环：`遇到问题 → 找到最早卡点 → 只做一步 → 验证结果 → 必要时最小化调整计划`，不会为了处理一次卡顿强制重走全部阶段。

## 完整文档

- [新手入门](docs/getting-started.md)：第一次使用、遇到问题、继续与重新规划；
- [完整使用手册](docs/usage-guide.md)：工作流、问题拆解、动态调整、结构化状态与安全边界；
- [使用场景与提示词](docs/examples.md)：四类目标与学习中卡住的完整示例；
- [多平台安装与使用](docs/platform-installation.md)：Codex、Claude Code、Tencent WorkBuddy 与豆包；
- [Domain Pack 扩展指南](docs/domain-pack-guide.md)：数据契约、能力依赖、项目原型与验证要求；
- [English documentation](README.en.md)：英文项目入口。

## 项目结构

| 位置 | 用途 |
| --- | --- |
| [`zjskills/SKILL.md`](zjskills/SKILL.md) | 核心运行契约与工作流路由 |
| [`zjskills/references/`](zjskills/references/) | 发现、能力、课程、项目、测评与优化引擎 |
| [`zjskills/assets/`](zjskills/assets/) | Schema、模板与 Domain Pack |
| [`zjskills/scripts/`](zjskills/scripts/) | 离线学习系统验证器 |
| [`tests/zjskills/`](tests/zjskills/) | 87 项核心回归测试、18 项开源封装测试及有效、无效样例 |
| [`docs/`](docs/) | 中英文使用与扩展文档 |

## 贡献

欢迎修正文档、报告可复现问题或提交符合数据契约的新 Domain Pack。提交前请阅读[贡献指南](CONTRIBUTING.md)，并遵守证据、隐私、品牌中立和禁止隐藏推广的边界。

## 发起与维护

由 ZJSkills（智建）发起并维护。

## 许可证

本项目采用 [MIT 许可证](LICENSE)。
