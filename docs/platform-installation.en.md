# ZJSkills Multi-platform Installation and Usage

[简体中文](platform-installation.md)

This guide applies to ZJSkills 3.0.0. The technical directory and Skill name are `zjskills`; the public display name is `ZJSkills`. Hosts have different integration capabilities. A Native Skill is discovered by the host, which loads `SKILL.md` and references when needed. Manual file/context use treats the files as instructions and reference material in the current conversation; it does not imply automatic triggering, complete loading, or cross-session continuity.

## Compatibility matrix

| Host category | Integration level | Recommended approach | Invocation and acceptance |
| --- | --- | --- | --- |
| Codex | Native Skill | User `$HOME/.agents/skills/zjskills` or project `.agents/skills/zjskills` | `$zjskills` or natural language; returns a career diagnosis |
| Claude Code | Native Skill | User `$HOME/.claude/skills/zjskills` or project `.claude/skills/zjskills` | `/zjskills` or natural language; returns a career diagnosis |
| Tencent WorkBuddy | Manual file/context | Provide `SKILL.md` and the references needed for the current task | Explicitly request the ZJSkills workflow; returns a career diagnosis |
| Doubao | Manual file/context | Upload runtime files in a dedicated conversation | Explicitly request the ZJSkills workflow; do not describe this as local native installation |
| Generic file and context hosts | Manual file/context | Provide `SKILL.md` and only the references needed now | Confirm actual file access; do not assume automatic triggering |

## Before installation

Get the repository and confirm that the 3.0 runtime contains `SKILL.md`, one interface file, and four reference files:

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

Acceptance is not about having more files. The installed directory must contain `SKILL.md`; all four reference files must exist; an explicit invocation must return a career diagnosis; a clear direction must produce a route of at most three stages; and “I'm stuck” must produce one action, success signal, and fallback check.

## Codex

Run the user-level installation from the repository root. It stops instead of overwriting a same-name directory:

```bash
(
  set -e
  source_dir="$PWD/zjskills"
  destination="$HOME/.agents/skills/zjskills"
  test -f "$source_dir/SKILL.md"
  if [ -e "$destination" ]; then
    echo "Installation stopped: $destination exists; back it up or use the upgrade flow." >&2
    exit 1
  fi
  mkdir -p "$HOME/.agents/skills"
  cp -R "$source_dir" "$destination"
  test -f "$destination/SKILL.md"
  test "$(find "$destination/references" -maxdepth 1 -type f -name '*.md' | wc -l | tr -d ' ')" = "4"
)
```

Open a new task and enter:

```text
$zjskills
I want to move into AI, but my direction is uncertain. My real work experience is [content], and I have [time] per week. Return a career diagnosis first; do not jump to a long curriculum.
```

For project-only use, change the destination to `.agents/skills/zjskills`. On Windows, copy the local `zjskills` directory to `$HOME\.agents\skills\zjskills` only after confirming the destination does not exist; then check `SKILL.md` and the four Markdown files under `references`.

## Claude Code

Claude Code uses `$HOME/.claude/skills/zjskills` for a personal Skill and `.claude/skills/zjskills` for a project Skill. The flow matches Codex with a different destination root:

```bash
(
  set -e
  source_dir="$PWD/zjskills"
  destination="$HOME/.claude/skills/zjskills"
  test -f "$source_dir/SKILL.md"
  if [ -e "$destination" ]; then
    echo "Installation stopped: $destination exists." >&2
    exit 1
  fi
  mkdir -p "$HOME/.claude/skills"
  cp -R "$source_dir" "$destination"
  test -f "$destination/SKILL.md"
  test "$(find "$destination/references" -maxdepth 1 -type f -name '*.md' | wc -l | tr -d ' ')" = "4"
)
```

Enter `/zjskills` in a new session, then describe the real situation. A correct response selects career diagnosis instead of exposing an old workflow or requiring a state file. If the Skill does not appear after installation, reopen the session or client and check that the path is exactly `.../zjskills/SKILL.md`.

## Tencent WorkBuddy

WorkBuddy's official documentation says that a custom Skill typically includes `skill.yml`, implementation files, and a README. The current ZJSkills package uses the Agent Skill `SKILL.md` structure, does not include `skill.yml`, and has no WorkBuddy-specific adaptation that has been created and tested. Therefore, this guide does not claim it is a native WorkBuddy Skill or instruct users to import the six-file directory.

For now, use manual file/context:

1. Set the repository as the task working directory, or provide `zjskills/SKILL.md` in the task.
2. Follow the conditional routing in `SKILL.md` and provide only the reference needed for the current task.
3. Ask WorkBuddy to name the files it actually read, then send the same career-diagnosis prompt used for Codex.
4. Provide the necessary files and prior result again in a new task; do not assume automatic triggering or cross-task continuity.

If a future WorkBuddy-specific adaptation is created with `skill.yml`, implementation files, and a README, install it through the documented custom-Skill flow and test it in a new conversation before describing that adaptation as native support.

## Doubao

This guide does not describe the Doubao consumer product as a local Native Skill host. Use manual file/context in a dedicated conversation:

1. Upload `zjskills/SKILL.md`.
2. Upload `zjskills/references/career-diagnosis.md`.
3. Add `ai-career-map.md` for direction comparison, `learning-route.md` for a clear route request, or `learning-help.md` for a current blocker.
4. Send the bootstrap prompt and require it not to guess the contents of files that were not uploaded.

```text
Treat the uploaded SKILL.md as the ZJSkills operating contract for this conversation.
Read existing context and select exactly one of career diagnosis, learning route, or learning help.
If a required reference is missing, name the exact file and wait for it. Do not guess its contents.
Answer in chat by default, give one current action, and do not promise external outcomes.
```

Provide the needed files and prior readable result again in a new conversation. Manual context is limited by uploads, the context window, and session state; it cannot guarantee automatic conditional loading.

## Generic file and context hosts

Any AI host that can read Markdown may attempt manual use, but this is not equivalent to Native Skill support:

1. Provide `SKILL.md` first.
2. Provide only the reference selected by its routing table for the current request.
3. Ask the host to name the files it actually read.
4. Use the same career-diagnosis acceptance prompt.
5. Restore necessary files and context in a new session instead of relying on implicit memory.

If the host cannot read references reliably, paste the relevant content into the context. Do not claim that `$zjskills` or `/zjskills` must work on a host with no native invocation mechanism.

## Unified acceptance check

After installation or upload, check:

```bash
test -f zjskills/SKILL.md
test "$(find zjskills/references -maxdepth 1 -type f -name '*.md' | wc -l | tr -d ' ')" = "4"
```

Then use `$zjskills` or `/zjskills`—or send the body directly on a manual host:

```text
I want to move into AI but cannot choose between Agent and Vibe Coding. I know a little Python, have only copied tutorial projects, and have six hours per week. Diagnose first and give one minimum validation action.
```

A correct result returns a career diagnosis, separates known facts, inference, and uncertainty, and gives one validation action. Then test “The direction is clear; generate a route of at most three stages” and “I'm stuck: [observed result]” to confirm all three modes.

## Migrate from 2.x to 3.0.0

Both versions use the technical directory `zjskills`, so do not merge the new files into an old installation. Back up the installed Skill, then replace it completely:

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
    echo "Migration stopped: $backup exists; inspect it first." >&2
    exit 1
  fi
  mv "$installed" "$backup"
  cp -R "$replacement" "$installed"
  test -f "$backup/SKILL.md"
  test -f "$installed/SKILL.md"
  test "$(find "$installed/references" -maxdepth 1 -type f -name '*.md' | wc -l | tr -d ' ')" = "4"
)
```

For Claude Code, change the root to `$HOME/.claude/skills`. In Windows PowerShell, first confirm that `$HOME\.agents\skills\zjskills.backup-2.x` does not exist, move the installed directory to that backup name, copy the repository `zjskills` directory, and check `SKILL.md` plus the four reference files.

Always **keep user-created learning files**; they are outside the installed Skill upgrade. Version 3.0 does not maintain an old YAML workspace by default. When a user supplies one, read it as source material and optionally summarize still-valid diagnosis, target, route, current action, and update history into one Markdown file. Never delete or overwrite the source.

Keep the backup until acceptance passes. To roll back, move the 3.0 installation away, then restore `zjskills.backup-2.x` as `zjskills`. Do not copy over local modifications.

## Public support note

If you encounter usage issues, planning questions, or other unresolved problems while using ZJSkills, contact Zhijian to join the Q&A group.

## Official capability references

- [Codex: Build skills](https://learn.chatgpt.com/docs/build-skills)
- [Claude Code: Extend Claude with Skills](https://code.claude.com/docs/en/skills)
- [Tencent WorkBuddy: create custom Skills](https://www.workbuddy.ai/docs/workbuddy/From-Beginner-to-Expert-Guide/Practice-Cases/Create-Skills)
- [Tencent WorkBuddy: Skill Marketplace](https://www.workbuddy.ai/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Skills-Market)
- [Doubao](https://www.doubao.com/)
