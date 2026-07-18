# ZJSkills

[简体中文](README.md)

**Version [1.0.0](VERSION) · 84 core regression tests / 94 total tests · MIT**

Turn an ambiguous learning goal into a verifiable, adaptable, personalized learning system.

## What it helps you solve

Course lists rarely answer three critical questions: which capabilities the target actually requires, what evidence supports the current gap, and where to recompute when circumstances change. ZJSkills starts from the target, baseline, capacity, and constraints, then designs a competency model, project ladder, phased roadmap, weekly actions, and assessment gates while keeping facts, self-reports, evidence, inferences, and assumptions distinct.

It can improve the quality of learning decisions, capability evidence, and adaptation, but it does not guarantee an offer, career transition, promotion, income, or any result controlled by external parties.

## Quick start

Enable the Skill displayed as `ZJSkills` in a Skill-capable AI tool. For installed-user compatibility, its directory and explicit invocation identifier remain `learning-architect`. Then state your target and constraints directly:

```text
Use ZJSkills to design my personalized learning system.
My target: build verifiable capabilities for an AI Agent Engineer role within six months.
My baseline: I can write basic Python scripts.
My weekly capacity: 12 hours.
My main constraint: limited budget, with a preference for project-first learning.
First ask for the decision-critical information that could change the route. Do not jump to course recommendations.
```

See [Getting Started](docs/getting-started.en.md) for prompts covering first use, continuation, and replanning.

## Install

ZJSkills supports native or compatible Skill integration with Codex, Claude Code, and Tencent WorkBuddy. Doubao uses an explicitly labeled prompt-based conversational mode. See the [multi-platform installation and usage guide](docs/platform-installation.en.md) for platform capabilities, macOS/Linux and Windows commands, upgrades, uninstallation, and acceptance tests.

Codex users can get the repository and run this user-level installation from its root:

```bash
git clone https://github.com/zhijianZJ/ZJSklls.git
cd ZJSklls
(
  set -e
  skills_dir="$HOME/.agents/skills"
  destination="$skills_dir/learning-architect"
  if [ -e "$destination" ]; then
    echo "Installation stopped: $destination already exists; back it up or use the upgrade flow first." >&2
    exit 1
  fi
  mkdir -p "$skills_dir"
  cp -R ./learning-architect "$skills_dir/"
  test -f "$destination/SKILL.md"
)
```

The parenthesized command exits successfully only when the destination was absent and `SKILL.md` was copied; an existing destination stops the copy with an error. After installation, open a new task and explicitly ask for `ZJSkills`. For Claude Code, install to `~/.claude/skills/learning-architect`. For Tencent WorkBuddy, prefer importing the local directory through the Skills UI. Do not describe Doubao as a native local Skill host; follow the guide's conversational workflow.

For an upgrade, do not merge the new directory into the old one. Move the installed directory to a backup location you control, copy the new version, and keep the backup until verification succeeds so local modifications are not silently overwritten. To uninstall, move the installed directory away only after preserving any changes you need.

Maintainers and contributors can validate the complete repository from its root:

```bash
python3 "${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-creator/scripts/quick_validate.py" learning-architect
python3 -m unittest discover -s tests/learning-architect -p "test_*.py" -q
python3 learning-architect/scripts/validate_learning_system.py --skill-root learning-architect --learner-dir tests/learning-architect/fixtures/valid-learner
```

The validator requires Python 3.9+ with `PyYAML`, `jsonschema`, and `referencing`. The first command uses Codex's bundled `skill-creator`; if that path is unavailable, run the latter two repository checks.

## What you get

- A learner profile covering the target, baseline evidence, capacity, constraints, and risks.
- A competency tree and prerequisite dependencies derived backward from the target outcome.
- A project ladder centered on authentic artifacts and explicit rubrics.
- A phased roadmap, next weekly plan, and clear passing gates.
- Traceable structured state and versioned updates when the target, constraints, or evidence change.
- A reusable Domain Pack contract, with an AI Agent Engineer pack included in the repository.

## How it works

```text
Discovery → Goal Analysis → Gap Analysis → Competency Design → Curriculum Design
→ Project Design → Roadmap → Weekly Planner → Assessment → Outcome Preparation
→ Continuous Optimization
```

Each stage has entry conditions, artifacts, and a gate. When evidence is insufficient, the system labels assumptions or requests more information. When a project or assessment fails, it locates the earliest causal gap and recomputes only the affected downstream parts.

## Full documentation

- [Getting Started](docs/getting-started.en.md): first use, continuation, and replanning.
- [Full Usage Guide](docs/usage-guide.en.md): workflow, structured state, evidence judgment, and safety boundaries.
- [Scenarios and Prompts](docs/examples.en.md): complete examples for four typical targets.
- [Multi-platform Installation and Usage](docs/platform-installation.en.md): Codex, Claude Code, Tencent WorkBuddy, and Doubao.
- [Domain Pack Extension Guide](docs/domain-pack-guide.en.md): data contract, competency dependencies, project archetypes, and validation requirements.
- [中文文档](README.md): Chinese project entry.

## Project structure

| Location | Purpose |
| --- | --- |
| [`learning-architect/SKILL.md`](learning-architect/SKILL.md) | Core operating contract and workflow router |
| [`learning-architect/references/`](learning-architect/references/) | Discovery, competency, curriculum, project, assessment, and optimization engines |
| [`learning-architect/assets/`](learning-architect/assets/) | Schemas, templates, and Domain Packs |
| [`learning-architect/scripts/`](learning-architect/scripts/) | Offline learning-system validator |
| [`tests/learning-architect/`](tests/learning-architect/) | 84 core regression tests, 10 open-source package tests, and valid/invalid fixtures |
| [`docs/`](docs/) | Chinese and English usage and extension guides |

## Contributing

Documentation fixes, reproducible issue reports, and new Domain Packs that follow the data contract are welcome. Read the [contribution guide](CONTRIBUTING.md) before submitting, and follow its evidence, privacy, brand-neutrality, and no-hidden-promotion boundaries.

## Initiator and maintainer

Initiated and maintained by ZJSkills.

## License

This project is available under the [MIT License](LICENSE).
