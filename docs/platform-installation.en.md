# ZJSkills Multi-platform Installation and Usage

[简体中文](platform-installation.md)

This guide explains how to use ZJSkills with Codex, Claude Code, Tencent WorkBuddy, and Doubao. These products do not provide the same Agent Skills interface, so choose the integration level that the host actually supports.

## Compatibility matrix

| Platform | Integration level | Recommended approach | Invocation | Notes |
| --- | --- | --- | --- | --- |
| Codex | Native Skill | Install in a user or repository Skills directory | Name `ZJSkills` in the prompt; CLI/IDE users can also select it with `$` | Supports explicit and automatic selection |
| Claude Code | Native Skill | Install under `~/.claude/skills` or project `.claude/skills` | `/learning-architect` or natural-language triggering | Supports explicit and automatic selection |
| Tencent WorkBuddy | Native/compatible Skill | Import the local Skill through the Skills UI; if import is unavailable, ask WorkBuddy to create and install it from the local directory | Select or name the Skill in a new task | Import UI varies by version; review the security scan and file permissions |
| Doubao | prompt-based conversational integration | Upload `SKILL.md`, add referenced files as needed, and send the bootstrap prompt | Explicitly request the ZJSkills workflow in that conversation | This is not a local Native Skill installation; automatic triggering, cross-session state, and complete resource loading are not guaranteed |

“Native Skill” means the host discovers `SKILL.md` and loads it when needed. Prompt-based integration treats the Skill as instructions and reference material for the current conversation, subject to upload, context-window, and session-state limits.

The UI display name is `ZJSkills`. `learning-architect` remains the compatible technical directory and explicit invocation identifier, so installation paths and `/learning-architect` do not change.

## Before installation

1. Get the repository and confirm that `learning-architect/SKILL.md` exists.
2. Review `SKILL.md` and any scripts the host may execute. ZJSkills's core planning workflow does not require writing to an external online service, but the host may still have file, shell, or network permissions.
3. Stop if the destination already exists. Back up and inspect local changes instead of overwriting or merging two versions in place.

```bash
git clone https://github.com/zhijianZJ/ZJSklls.git
cd ZJSklls
test -f learning-architect/SKILL.md
```

## Codex

Codex currently recommends `$HOME/.agents/skills` for user Skills and `.agents/skills` inside a repository for project Skills. The following installs ZJSkills for the current user across projects.

### macOS / Linux

Run from the repository root:

```bash
(
  set -e
  source_dir="$PWD/learning-architect"
  destination="$HOME/.agents/skills/learning-architect"
  test -f "$source_dir/SKILL.md"
  if [ -e "$destination" ]; then
    echo "Installation stopped: $destination already exists; back it up or upgrade first." >&2
    exit 1
  fi
  mkdir -p "$HOME/.agents/skills"
  cp -R "$source_dir" "$destination"
  test -f "$destination/SKILL.md"
)
```

### Windows PowerShell

Run from the repository root:

```powershell
$Source = Join-Path (Get-Location) "learning-architect"
$Destination = Join-Path $HOME ".agents\skills\learning-architect"
if (-not (Test-Path (Join-Path $Source "SKILL.md"))) { throw "learning-architect/SKILL.md was not found" }
if (Test-Path $Destination) { throw "Installation stopped: $Destination already exists; back it up or upgrade first." }
New-Item -ItemType Directory -Force (Split-Path $Destination) | Out-Null
Copy-Item -Recurse $Source $Destination
if (-not (Test-Path (Join-Path $Destination "SKILL.md"))) { throw "Installation verification failed" }
```

Open a new task and enter:

```text
Use ZJSkills. First understand my target, baseline, available time, and constraints, then decide which decision-critical questions remain. Do not jump to course recommendations.
```

In Codex CLI or the IDE, you can also type `$` and select `learning-architect`. Codex normally discovers newly installed Skills automatically. If it does not appear, open a new task or restart the client and check again.

For repository-only use, change the destination to `.agents/skills/learning-architect` in the repository root and commit that directory with the project.

## Claude Code

Claude Code uses `$HOME/.claude/skills` for personal Skills and `.claude/skills` for project Skills.

### macOS / Linux

```bash
(
  set -e
  source_dir="$PWD/learning-architect"
  destination="$HOME/.claude/skills/learning-architect"
  test -f "$source_dir/SKILL.md"
  if [ -e "$destination" ]; then
    echo "Installation stopped: $destination already exists; back it up or upgrade first." >&2
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
if (-not (Test-Path (Join-Path $Source "SKILL.md"))) { throw "learning-architect/SKILL.md was not found" }
if (Test-Path $Destination) { throw "Installation stopped: $Destination already exists; back it up or upgrade first." }
New-Item -ItemType Directory -Force (Split-Path $Destination) | Out-Null
Copy-Item -Recurse $Source $Destination
if (-not (Test-Path (Join-Path $Destination "SKILL.md"))) { throw "Installation verification failed" }
```

Run an explicit test in Claude Code:

```text
/learning-architect
```

Then provide your goal and constraints. You can also say, “Use ZJSkills to plan my AI career learning path.” Claude Code watches an existing Skills directory for changes. If this installation created the top-level directory for the first time, restart Claude Code once.

For project-only use, copy the Skill to `.claude/skills/learning-architect` in the project root.

## Tencent WorkBuddy

Tencent WorkBuddy provides a Skill marketplace, custom Skills, and documented compatibility with OpenClaw community Skill imports. ZJSkills is a directory containing `SKILL.md` and supporting resources. Prefer the WorkBuddy Skills UI over guessing an internal storage path.

1. Download this repository and confirm that `learning-architect/SKILL.md` exists.
2. Open WorkBuddy's Skills or Skill Marketplace UI and look for Import Skill, Community Skill, or the corresponding entry in your version.
3. Select the local `learning-architect` directory. If your version accepts repository URLs, you may instead provide this GitHub repository URL.
4. Review WorkBuddy's security scan, file list, and requested permissions before installing and enabling it.
5. Create a new task, select ZJSkills in the Skill picker, or use the verification prompt below.

If your version has no manual import entry, create a task with this repository as its working directory and enter:

```text
Inspect the local learning-architect directory and install its SKILL.md and supporting resources as a custom Skill. Before installation, list the destination, files to be copied, and required permissions. Do not overwrite an existing Skill with the same name. After installation, tell me how to verify it in the Skills UI.
```

This fallback depends on the custom-Skill features in your current WorkBuddy version. Review the proposed changes before authorizing them, especially any request to replace an existing directory.

## Doubao

The public consumer-product documentation used for this guide does not publish a local `SKILL.md` installation convention for Doubao. This section therefore uses prompt-based conversational integration and does not describe it as a Native Skill installation.

1. Start a dedicated conversation.
2. Upload `learning-architect/SKILL.md`.
3. Send the bootstrap prompt below.
4. When Doubao asks for a referenced file, upload the exact file from `learning-architect/references/` or `learning-architect/assets/`. Do not let it assume the contents of unread files.
5. Save the final learner profile, roadmap, and weekly plan as files. Re-upload them in a new conversation instead of relying on implicit cross-session memory.

```text
Treat the SKILL.md I uploaded as the ZJSkills operating contract for this conversation.
Follow its stages, entry conditions, and gates: begin with discovery and goal analysis, then continue to gap, competency, project, roadmap, and weekly planning.
If the contract references a file you have not read, tell me the exact filename and wait for me to upload it. Do not guess its contents.
Ask first for information that could materially change the route. Do not jump to course recommendations or promise an offer, income, or another externally controlled outcome.
```

Doubao's conversational integration is suitable for initial analysis and lightweight planning. Prefer Codex, Claude Code, or a WorkBuddy version that can import Skills when you need reliable automatic triggering, complete on-demand resource loading, script validation, or long-term versioned state.

## Verify the integration

Use the same acceptance prompt on every platform:

```text
Use ZJSkills to design a six-month AI Agent Engineer learning path. I have told you only that I know a little Python and have ten hours per week. Do not generate the route yet. Tell me which missing facts could materially change the plan.
```

A correct first step fills decision-critical gaps or labels assumptions instead of immediately returning a course list. Continue the test by checking for competency dependencies, project evidence, phase gates, and next-week actions.

## Upgrade and uninstall

- Upgrade: move the installed directory to a backup location you control, then copy or import the new version. Keep the backup until verification succeeds.
- Uninstall: use the platform's Skills UI or move its `learning-architect` directory out of the Skills location. Preserve your learning state and local modifications first.
- Share one source across hosts: experienced users may point multiple native Skill locations at one trusted source directory with symbolic links. Stop when a same-name real directory exists; never overwrite it.

## Official capability references

- [Codex: Build skills](https://learn.chatgpt.com/docs/build-skills)
- [Claude Code: Extend Claude with skills](https://code.claude.com/docs/en/skills)
- [Tencent WorkBuddy: Skill selection and community Skill import](https://www.workbuddy.ai/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Task-Bar)
- [Tencent WorkBuddy: Create custom Skills](https://www.workbuddy.ai/docs/workbuddy/From-Beginner-to-Expert-Guide/Practice-Cases/Create-Skills)
- [Doubao](https://www.doubao.com/)
