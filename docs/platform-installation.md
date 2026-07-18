# ZJSkills 多平台安装与使用

[English](platform-installation.en.md)

本文说明如何在 Codex、Claude Code、Tencent WorkBuddy 和豆包中使用 ZJSkills。不同产品对 Agent Skills 的支持并不相同，因此先确认接入级别，再选择安装方式。

## 兼容性矩阵

| 平台 | 接入级别 | 推荐方式 | 调用方式 | 说明 |
| --- | --- | --- | --- | --- |
| Codex | 原生 Skill | 安装到用户级或项目级 Skills 目录 | 在提示词中点名 `ZJSkills`，CLI/IDE 也可用 `$` 选择 | 支持自动匹配与显式调用 |
| Claude Code | 原生 Skill | 安装到 `~/.claude/skills` 或项目 `.claude/skills` | `/learning-architect` 或自然语言触发 | 支持自动匹配与显式调用 |
| Tencent WorkBuddy | 原生/兼容 Skill | 从技能界面导入本地 Skill；没有导入入口时让 WorkBuddy 从本地目录创建并安装 | 在新任务中选择或点名 Skill | 产品版本的导入入口可能不同，安装前查看安全扫描与文件权限 |
| 豆包 | 对话接入 | 上传 `SKILL.md`，按需补充引用文件，并使用启动提示词 | 在当前对话中明确要求按 ZJSkills 工作流执行 | 不是本地原生 Skill 安装；自动触发、跨会话状态与完整资源加载不作保证 |

“原生 Skill”表示宿主能发现 `SKILL.md` 并按需加载它；“对话接入”表示把 Skill 当作当前对话的指令与参考资料，能力会受文件上传、上下文窗口和会话状态限制。

界面显示名称统一为 `ZJSkills`。`learning-architect` 是保留的技术目录和显式调用标识，因此安装命令、目录路径和 `/learning-architect` 不需要改名。

## 安装前检查

1. 从本仓库获取代码，并确认 `learning-architect/SKILL.md` 存在。
2. 阅读 `SKILL.md` 以及会被执行的脚本。ZJSkills 的核心规划流程不需要联网写入外部服务，但宿主本身仍可能拥有文件、命令或网络权限。
3. 如果目标位置已经存在同名目录，先停止安装。备份并核对本地修改，不要直接覆盖或混合两个版本。

```bash
git clone https://github.com/zhijianZJ/ZJSklls.git
cd ZJSklls
test -f learning-architect/SKILL.md
```

## Codex

Codex 当前推荐的用户级目录是 `$HOME/.agents/skills`，项目级目录是仓库中的 `.agents/skills`。下面安装为用户级 Skill，适用于你打开的所有项目。

### macOS / Linux

在仓库根目录执行：

```bash
(
  set -e
  source_dir="$PWD/learning-architect"
  destination="$HOME/.agents/skills/learning-architect"
  test -f "$source_dir/SKILL.md"
  if [ -e "$destination" ]; then
    echo "安装已停止：$destination 已存在，请先备份或升级。" >&2
    exit 1
  fi
  mkdir -p "$HOME/.agents/skills"
  cp -R "$source_dir" "$destination"
  test -f "$destination/SKILL.md"
)
```

### Windows PowerShell

在仓库根目录执行：

```powershell
$Source = Join-Path (Get-Location) "learning-architect"
$Destination = Join-Path $HOME ".agents\skills\learning-architect"
if (-not (Test-Path (Join-Path $Source "SKILL.md"))) { throw "未找到 learning-architect/SKILL.md" }
if (Test-Path $Destination) { throw "安装已停止：$Destination 已存在，请先备份或升级。" }
New-Item -ItemType Directory -Force (Split-Path $Destination) | Out-Null
Copy-Item -Recurse $Source $Destination
if (-not (Test-Path (Join-Path $Destination "SKILL.md"))) { throw "安装验证失败" }
```

安装后新建任务并输入：

```text
请使用 ZJSkills。先了解我的目标、基础、时间与约束，再决定还需要问哪些关键问题；不要直接推荐课程。
```

在 Codex CLI 或 IDE 中，也可以先输入 `$` 并选择 `learning-architect`。Codex 通常会自动发现新 Skill；若未出现，重新打开任务或重启客户端后再检查。

如果只希望当前项目使用，把目标目录改成项目根目录下的 `.agents/skills/learning-architect`，并把该目录纳入项目版本管理。

## Claude Code

Claude Code 的用户级目录是 `$HOME/.claude/skills`，项目级目录是 `.claude/skills`。

### macOS / Linux

```bash
(
  set -e
  source_dir="$PWD/learning-architect"
  destination="$HOME/.claude/skills/learning-architect"
  test -f "$source_dir/SKILL.md"
  if [ -e "$destination" ]; then
    echo "安装已停止：$destination 已存在，请先备份或升级。" >&2
    exit 1
  fi
  mkdir -p "$HOME/.claude/skills"
  cp -R "$source_dir" "$destination"
  test -f "$destination/SKILL.md"
)
```

### Windows PowerShell

```powershell
$Source = Join-Path (Get-Location) "learning-architect"
$Destination = Join-Path $HOME ".claude\skills\learning-architect"
if (-not (Test-Path (Join-Path $Source "SKILL.md"))) { throw "未找到 learning-architect/SKILL.md" }
if (Test-Path $Destination) { throw "安装已停止：$Destination 已存在，请先备份或升级。" }
New-Item -ItemType Directory -Force (Split-Path $Destination) | Out-Null
Copy-Item -Recurse $Source $Destination
if (-not (Test-Path (Join-Path $Destination "SKILL.md"))) { throw "安装验证失败" }
```

在 Claude Code 中执行显式测试：

```text
/learning-architect
```

然后输入你的目标和约束。也可以直接说“请使用 ZJSkills 帮我规划 AI 职业学习路线”。Claude Code 会监控已经存在的 Skills 目录；如果本次安装才创建顶层目录，重启一次 Claude Code。

项目级安装时，把 Skill 复制到项目根目录的 `.claude/skills/learning-architect`。

## Tencent WorkBuddy

Tencent WorkBuddy 提供技能市场、自定义 Skill，并公开说明兼容 OpenClaw 社区 Skill 导入。ZJSkills 是一个包含 `SKILL.md` 和配套资源的目录，推荐从 WorkBuddy 的技能界面导入，而不是猜测内部存储路径。

1. 下载本仓库，确认 `learning-architect/SKILL.md` 存在。
2. 打开 WorkBuddy 的“技能”或“技能市场”界面，查找“导入 Skill”“社区 Skill”或同类入口。
3. 选择本地 `learning-architect` 目录；如果当前版本支持仓库地址导入，也可填写本仓库 GitHub 地址。
4. 查看 WorkBuddy 的安全扫描、文件清单与权限请求，确认后安装并启用。
5. 新建任务，在技能选择器中选择 ZJSkills，或输入下面的测试提示词。

如果当前版本没有手动导入入口，创建一个以本仓库为工作目录的新任务，并输入：

```text
请检查本地 learning-architect 目录，把其中的 SKILL.md 及配套资源作为一个自定义 Skill 安装。安装前先列出目标位置、将复制的文件和所需权限；不要覆盖已有同名 Skill。安装后告诉我如何在技能栏验证它。
```

这个回退方式依赖 WorkBuddy 当前版本的自定义 Skill 能力。执行前检查它给出的变更，不要授权覆盖已有目录。

## 豆包

截至本文所依据的公开产品资料，豆包消费端没有公开本地 `SKILL.md` 目录安装规范。因此这里提供对话接入，而不把它描述为原生安装。

1. 新建一个专用对话。
2. 上传 `learning-architect/SKILL.md`。
3. 发送下面的启动提示词。
4. 当豆包需要某个引用文件时，从 `learning-architect/references/` 或 `learning-architect/assets/` 上传对应文件。不要让它在未读取文件时假设文件内容。
5. 把最终学习者画像、路线图和周计划另存为文件；开启新对话时重新上传，避免依赖隐含的跨会话记忆。

```text
请把我上传的 SKILL.md 作为本次对话的 ZJSkills 工作协议。
严格按照其中的阶段、进入条件和关卡执行：先发现与目标分析，再做差距、能力、项目、路线和周计划。
如果协议引用了你尚未读取的文件，请先告诉我准确文件名并等待上传，不要猜测其内容。
先询问真正会改变路线的关键信息，不要直接推荐课程，也不要承诺 Offer、收入或其他外部结果。
```

豆包的对话接入适合首次分析和轻量规划。需要稳定的自动触发、完整资源按需加载、脚本验证或长期版本化状态时，优先使用 Codex、Claude Code 或支持导入 Skill 的 WorkBuddy。

## 验证是否生效

无论使用哪个平台，都用同一条验收提示词测试：

```text
请使用 ZJSkills 帮我制定 6 个月 AI Agent 工程师学习路线。我只告诉你：会一点 Python，每周 10 小时。现在先不要生成路线，请告诉我还缺哪些会实质改变规划的信息。
```

正确的第一步应是补齐决策关键事实或标记假设，而不是立即给出课程清单。接着再测试它是否能输出能力依赖、项目证据、阶段关卡和下一周行动。

## 升级与卸载

- 升级：先把已安装目录移动到你指定的备份位置，再复制或导入新版本；验证成功前保留备份。
- 卸载：从对应平台的 Skills 界面卸载，或移走该平台的 `learning-architect` 目录。先保存你自己的学习状态和本地修改。
- 多平台共用：熟悉符号链接的用户可以让多个原生 Skill 目录指向同一份可信源目录，以减少版本分叉；遇到同名真实目录时必须停止，不能覆盖。

## 官方能力参考

- [Codex：Build skills](https://learn.chatgpt.com/docs/build-skills)
- [Claude Code：使用 Skills 扩展 Claude](https://code.claude.com/docs/zh-CN/skills)
- [Tencent WorkBuddy：选择技能与社区 Skill 导入](https://www.workbuddy.ai/docs/zh/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Task-Bar)
- [Tencent WorkBuddy：创建自定义 Skills](https://www.workbuddy.ai/docs/zh/workbuddy/From-Beginner-to-Expert-Guide/Practice-Cases/Create-Skills)
- [豆包官网](https://www.doubao.com/)
