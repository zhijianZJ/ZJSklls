# ZJSkills 多平台安装与使用

[English](platform-installation.en.md)

本文适用于 ZJSkills 3.0.0。技术目录和 Skill 名称是 `zjskills`，公开名称是 `ZJSkills`。不同产品的接入能力不相同：原生 Skill 由宿主发现并按需加载 `SKILL.md` 及引用文件；手动文件/上下文接入只在当前会话中把这些文件作为指令和参考，不能假设自动触发、完整加载或跨会话持续。

## 兼容性矩阵

| 平台类别 | 接入级别 | 推荐方式 | 调用与验收 |
| --- | --- | --- | --- |
| Codex | 原生 Skill | 用户级 `$HOME/.agents/skills/zjskills` 或项目级 `.agents/skills/zjskills` | `$zjskills` 或自然语言；返回职业诊断 |
| Claude Code | 原生 Skill | 用户级 `$HOME/.claude/skills/zjskills` 或项目级 `.claude/skills/zjskills` | `/zjskills` 或自然语言；返回职业诊断 |
| Tencent WorkBuddy | 手动文件/上下文 | 在任务中提供 `SKILL.md` 和当前所需引用 | 明确要求按 ZJSkills 工作；返回职业诊断 |
| 豆包 | 手动文件/上下文 | 在专用对话上传运行文件 | 明确要求按 ZJSkills 工作；不描述为本地原生安装 |
| 通用文件与上下文宿主 | 手动文件/上下文 | 提供 `SKILL.md` 和本次所需引用 | 能读取文件并遵守条件加载；不保证自动触发 |

## 安装前检查

获取仓库并确认 3.0 运行目录只有 `SKILL.md`、一个界面文件和四个引用文件：

```bash
git clone https://github.com/zhijianZJ/ZJSkills.git
cd ZJSkills
test -f zjskills/SKILL.md
test -f zjskills/agents/openai.yaml
test -f zjskills/references/career-diagnosis.md
test -f zjskills/references/learning-route.md
test -f zjskills/references/learning-help.md
test -f zjskills/references/ai-career-map.md
test "$(find zjskills/references -maxdepth 1 -type f -name '*.md' | wc -l | tr -d ' ')" = "4"
```

验收标准不是文件越多越好，而是：安装目录含 `SKILL.md`；四个引用文件都存在；显式调用会返回职业诊断；方向清楚时能生成最多三阶段路线；“我卡住了”会得到一个行动、成功信号和备用检查。

## Codex

在仓库根目录执行用户级安装。命令遇到同名目录会停止，不会覆盖：

```bash
(
  set -e
  source_dir="$PWD/zjskills"
  destination="$HOME/.agents/skills/zjskills"
  test -f "$source_dir/SKILL.md"
  if [ -e "$destination" ]; then
    echo "安装已停止：$destination 已存在，请先备份或按升级流程处理。" >&2
    exit 1
  fi
  mkdir -p "$HOME/.agents/skills"
  cp -R "$source_dir" "$destination"
  test -f "$destination/SKILL.md"
  test "$(find "$destination/references" -maxdepth 1 -type f -name '*.md' | wc -l | tr -d ' ')" = "4"
)
```

新建任务后输入：

```text
$zjskills
我想进入 AI 行业，但方向不确定。我做过的真实工作是[内容]，每周可投入[时间]。请先返回职业诊断，不要直接生成长期课表。
```

项目级使用时，把目标改为仓库中的 `.agents/skills/zjskills`。Windows 可把本地 `zjskills` 目录复制到 `$HOME\.agents\skills\zjskills`；复制前确认目标不存在，复制后检查 `SKILL.md` 和 `references` 下四个 Markdown 文件。

## Claude Code

Claude Code 的个人 Skill 目录是 `$HOME/.claude/skills/zjskills`，项目目录是 `.claude/skills/zjskills`。安装逻辑与 Codex 相同，只替换目标根目录：

```bash
(
  set -e
  source_dir="$PWD/zjskills"
  destination="$HOME/.claude/skills/zjskills"
  test -f "$source_dir/SKILL.md"
  if [ -e "$destination" ]; then
    echo "安装已停止：$destination 已存在。" >&2
    exit 1
  fi
  mkdir -p "$HOME/.claude/skills"
  cp -R "$source_dir" "$destination"
  test -f "$destination/SKILL.md"
  test "$(find "$destination/references" -maxdepth 1 -type f -name '*.md' | wc -l | tr -d ' ')" = "4"
)
```

新会话输入 `/zjskills`，再描述真实处境。正确响应会选择职业诊断，而不是显示旧工作流或要求先创建状态文件。若新安装后尚未出现，重新打开会话或客户端，并检查目录层级是否正好是 `.../zjskills/SKILL.md`。

## Tencent WorkBuddy

WorkBuddy 官方文档中的自定义 Skill 通常包含 `skill.yml`、实现文件和 README。当前 ZJSkills 包采用 Agent Skill 的 `SKILL.md` 结构，不含 `skill.yml`，也尚未创建并完成测试 WorkBuddy 专用改造，因此不把它宣称为 WorkBuddy 原生 Skill，也不指示用户导入这个六文件目录。

当前请按手动文件/上下文使用：

1. 把仓库设为任务工作目录，或在任务中提供 `zjskills/SKILL.md`；
2. 按 `SKILL.md` 的条件路由，只提供当前任务需要的引用文件；
3. 要求 WorkBuddy 说明它实际读取了哪些文件，然后发送与 Codex 相同的职业诊断提示词；
4. 在新任务中重新提供必要文件和上一轮结果，不假设自动触发或跨任务持续。

以后若创建了含 `skill.yml`、实现文件和 README 的 WorkBuddy 专用改造，应按官方自定义 Skill 流程安装并在新对话中完成测试后，再单独说明原生支持。

## 豆包

这里不把豆包消费端描述为本地原生 Skill。使用专用对话进行手动文件/上下文接入：

1. 上传 `zjskills/SKILL.md`；
2. 上传 `zjskills/references/career-diagnosis.md`；
3. 如果需要比较方向，再上传 `ai-career-map.md`；方向明确需要路线时上传 `learning-route.md`；学习卡住时上传 `learning-help.md`；
4. 发送启动提示词，并要求它不要猜测未上传文件的内容。

```text
把我上传的 SKILL.md 作为本次对话的 ZJSkills 工作协议。
先读取已有对话并只选择职业诊断、学习路线、学习解题中的一种模式。
如果所需引用文件尚未上传，请告诉我准确文件名并等待；不要猜测内容。
默认在对话中回答，只给一个当前行动，不承诺外部结果。
```

新对话应重新提供必要文件和上一轮可读结果。手动上下文接入受上传、上下文窗口和会话状态限制，不能承诺自动按需加载。

## 通用文件与上下文宿主

任何能够读取 Markdown 文件的 AI 宿主都可以尝试手动使用，但这不等于原生 Skill 支持：

1. 先提供 `SKILL.md`；
2. 根据当前请求只提供表格中对应的引用文件；
3. 要求宿主先说明它实际读取了哪些文件；
4. 用同一条职业诊断提示词验收；
5. 新会话重新提供必要上下文，不依赖隐含记忆。

宿主若无法可靠读取引用文件，就把相关内容直接粘贴到上下文中。不要声称 `$zjskills` 或 `/zjskills` 在没有原生调用机制的平台上一定有效。

## 统一验收

安装或上传后检查：

```bash
test -f zjskills/SKILL.md
test "$(find zjskills/references -maxdepth 1 -type f -name '*.md' | wc -l | tr -d ' ')" = "4"
```

然后用 `$zjskills` 或 `/zjskills`（手动宿主则直接发送正文）测试：

```text
我想转入 AI，但不知道选 Agent 还是 Vibe Coding。我会一点 Python，只复制过教程项目，每周 6 小时。请先诊断，并给一个最小验证行动。
```

正确结果应返回职业诊断，区分已知事实、推断与不确定性，并只给一个验证行动。再分别测试“方向已明确，请生成最多三阶段路线”和“我卡住了：[现象]”，确认三种模式都能工作。

## 从 2.x 迁移到 3.0.0

2.x 与 3.0 使用相同技术目录 `zjskills`，不能把新文件直接合并进旧安装目录。先备份已安装 Skill，再完整替换：

```bash
(
  set -e
  skills_root="$HOME/.agents/skills"
  installed="$skills_root/zjskills"
  backup="$skills_root/zjskills.backup-2.x"
  replacement="$PWD/zjskills"
  test -f "$installed/SKILL.md"
  test -f "$replacement/SKILL.md"
  if [ -e "$backup" ]; then
    echo "迁移已停止：$backup 已存在，请先核对。" >&2
    exit 1
  fi
  mv "$installed" "$backup"
  cp -R "$replacement" "$installed"
  test -f "$backup/SKILL.md"
  test -f "$installed/SKILL.md"
  test "$(find "$installed/references" -maxdepth 1 -type f -name '*.md' | wc -l | tr -d ' ')" = "4"
)
```

Claude Code 只需把根目录改为 `$HOME/.claude/skills`。Windows PowerShell 中，先确认 `$HOME\.agents\skills\zjskills.backup-2.x` 不存在，再把已安装目录移动为该备份名，复制仓库中的 `zjskills`，最后检查 `SKILL.md` 与四个引用文件。

始终**保留用户自己创建的学习文件**；它们不属于安装目录升级范围。3.0 不默认维护旧 YAML 工作区。用户主动提供时，把它当作来源材料读取，并可选择把仍然有效的诊断、目标、路线、当前行动和更新记录汇总为一份 Markdown 文件；不要删除或覆盖原文件。

迁移验收通过前保留备份。需要回滚时，先移走 3.0 安装目录，再把 `zjskills.backup-2.x` 恢复为 `zjskills`，不要用复制覆盖可能存在的本地修改。

## 公开支持说明

使用 ZJSkills 时如遇到使用问题、规划疑问或其他未解决问题，可联系智建进入答疑群交流。

## 官方能力参考

- [Codex：Build skills](https://learn.chatgpt.com/docs/build-skills)
- [Claude Code：使用 Skills 扩展 Claude](https://code.claude.com/docs/zh-CN/skills)
- [Tencent WorkBuddy：创建自定义 Skills](https://www.workbuddy.ai/docs/workbuddy/From-Beginner-to-Expert-Guide/Practice-Cases/Create-Skills)
- [Tencent WorkBuddy：Skill Marketplace](https://www.workbuddy.ai/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Skills-Market)
- [豆包官网](https://www.doubao.com/)
