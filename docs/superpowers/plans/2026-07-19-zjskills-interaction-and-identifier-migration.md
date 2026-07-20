# ZJSkills Interaction and Identifier Migration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a state-aware, beginner-friendly conversational navigation layer and migrate the runtime Skill identifier from `learning-architect` to `zjskills` across the package.

**Architecture:** Keep learning decisions in the existing engines and add `interaction-orchestrator.md` as a presentation/router layer that derives views from current learner state. Perform one Git-preserving directory migration, then update current runtime, tests, public docs, version metadata, installation paths, and UI metadata without shipping a duplicate compatibility Skill.

**Tech Stack:** Markdown Agent Skill instructions, YAML UI metadata and schemas, Python 3.9+ validator, `unittest`, Git, Codex Skill validation.

## Global Constraints

- Human-facing display name remains exactly `ZJSkills`.
- Technical folder and Skill name become exactly lowercase `zjskills`.
- Explicit invocation becomes `$zjskills` for Codex and `/zjskills` for Claude Code.
- Release version becomes `2.0.0`.
- Current public repository URL becomes `https://github.com/zhijianZJ/ZJSkills.git`.
- Do not retain a second discoverable `learning-architect` runtime directory.
- Do not create a standalone web UI or assume clickable host controls.
- Beginner mode is the default and hides YAML, schemas, engine names, version IDs, and internal confidence fields.
- A clear user request routes directly; only an ambiguous request opens the six-option navigation.
- The interaction layer never replaces evidence, gate, rollback, privacy, or safety rules.
- Historical specifications may retain historical identifiers, but current runtime, tests, README, installation docs, usage docs, examples, and contribution commands must use `zjskills`.

---

### Task 1: Lock naming and interaction behavior with failing tests

**Files:**
- Modify: `tests/learning-architect/test_open_source_package.py`
- Modify: `tests/learning-architect/test_validate_learning_system.py`
- Modify: `tests/learning-architect/scenarios.yaml`

**Interfaces:**
- Consumes: approved interaction and identifier migration specification.
- Produces: failing assertions that define the `zjskills` directory, metadata, version, public URLs, navigation contract, global commands, display depths, and routing scenarios.

- [ ] **Step 1: Change package-path expectations before moving files**

Set `RUNTIME_ROOT = REPO_ROOT / "zjskills"`, assert `(REPO_ROOT / "learning-architect").exists()` is false, require `VERSION == "2.0.0"`, and require current public documents to use `https://github.com/zhijianZJ/ZJSkills.git`, `zjskills/`, `$zjskills`, and `/zjskills`.

- [ ] **Step 2: Add interaction contract assertions**

Require `references/interaction-orchestrator.md` and assert the exact six navigation items, direct-route rule, state-card labels, weekly-card labels, global intents, `beginner | standard | professional`, missing-state behavior, and the statement that the interaction layer does not replace decision engines.

- [ ] **Step 3: Add pressure scenarios**

Append scenarios `ambiguous-ai-entry`, `explicit-error-bypasses-menu`, `numeric-stuck-selection`, `unknown-selection`, `resume-without-state`, `beginner-hides-internals`, and `professional-shows-state`. Give each at least three observable required behaviors.

- [ ] **Step 4: Run RED tests**

Run: `/Users/wangshucheng/miniconda3/bin/python3 -m unittest discover -s tests/learning-architect -p 'test_*.py' -q`

Expected: FAIL because `zjskills/`, `interaction-orchestrator.md`, version `2.0.0`, new identifiers, and updated public docs do not yet exist.

### Task 2: Migrate runtime and test directories

**Files:**
- Move: `learning-architect/` -> `zjskills/`
- Move: `tests/learning-architect/` -> `tests/zjskills/`
- Modify: `zjskills/SKILL.md`
- Modify: `zjskills/agents/openai.yaml`
- Modify: `zjskills/scripts/validate_learning_system.py`
- Modify: `tests/zjskills/test_open_source_package.py`
- Modify: `tests/zjskills/test_validate_learning_system.py`
- Modify: `VERSION`

**Interfaces:**
- Consumes: existing runtime files and tests under the old paths.
- Produces: one runtime at `zjskills/`, one test suite at `tests/zjskills/`, `name: zjskills`, and version `2.0.0`.

- [ ] **Step 1: Move directories with Git history**

Run: `git mv learning-architect zjskills`

Run: `git mv tests/learning-architect tests/zjskills`

Expected: old runtime/test directories disappear and their files appear at the new paths as Git renames.

- [ ] **Step 2: Update technical identity**

Change the frontmatter to `name: zjskills`, change the validator module docstring from Learning Architect to ZJSkills-neutral wording, update test roots to `REPO_ROOT / "zjskills"`, and write `2.0.0` to `VERSION`.

- [ ] **Step 3: Regenerate UI metadata deterministically**

Run:

```bash
/Users/wangshucheng/miniconda3/bin/python3 \
  /Users/wangshucheng/.codex/skills/.system/skill-creator/scripts/generate_openai_yaml.py \
  zjskills \
  --interface 'display_name=ZJSkills' \
  --interface 'short_description=面向AI新手的学习导航、职业路线、问题拆解与动态调整' \
  --interface 'default_prompt=Use $zjskills to show me the beginner-friendly learning navigation and guide me to one clear next step.'
```

Expected: `zjskills/agents/openai.yaml` contains `display_name: "ZJSkills"`, the supplied short description, and `$zjskills` in `default_prompt`, while retaining implicit invocation.

- [ ] **Step 4: Run focused identity tests**

Run: `/Users/wangshucheng/miniconda3/bin/python3 -m unittest discover -s tests/zjskills -p 'test_open_source_package.py' -k 'skill_ui or version or technical_identifier' -q`

Expected: tests may still fail only for current public documentation that Task 4 has not migrated; runtime identity assertions pass.

### Task 3: Implement the interaction orchestrator

**Files:**
- Create: `zjskills/references/interaction-orchestrator.md`
- Modify: `zjskills/SKILL.md`
- Modify: `zjskills/references/beginner-interaction.md`
- Modify: `zjskills/references/workflow.md`
- Modify: `tests/zjskills/test_validate_learning_system.py`

**Interfaces:**
- Consumes: user utterance, optional valid `system-state.yaml`, active weekly plan, open learning issue, last next action, and explicit interaction-depth preference.
- Produces: direct engine routing or one of four plain-language view contracts, plus a maximum of three context-relevant next choices.

- [ ] **Step 1: Write the six-option navigation contract**

Create `interaction-orchestrator.md` with exact Chinese navigation items for industry direction, learning/career route, today/weekly plan, current learning problem, changed circumstances, and resume. Require equivalent English labels when the conversation language is English.

- [ ] **Step 2: Define routing precedence**

Specify: explicit learning problem -> Problem-Solving; explicit day/week request -> Weekly Planner; explicit constraint/goal change -> impact classification and relevant replan; explicit resume -> validate state; ambiguous learning request -> navigation. State that an explicit request bypasses the home navigation.

- [ ] **Step 3: Define view contracts and global intents**

Add the regular state card, weekly progress card, problem-solving card, and completion-feedback card. Define natural-language handling for continue, back, switch method, unknown, view detail, change constraints, change goal, save, and pause; distinguish conversational back from artifact rollback.

- [ ] **Step 4: Define display-depth and failure behavior**

Default to `beginner`, allow explicit `standard` and `professional`, and persist only an explicitly selected depth when a workspace is authorized. Define behavior for no state, corrupt state, invalid choice, unavailable persistence, and safety handoff.

- [ ] **Step 5: Route the new reference from SKILL.md**

Load `interaction-orchestrator.md` on ambiguous entry, global navigation command, resume request, or display-depth request. Keep the numbered 11-stage workflow unchanged and state that navigation never advances a gate.

- [ ] **Step 6: Run interaction contract tests**

Run: `/Users/wangshucheng/miniconda3/bin/python3 -m unittest discover -s tests/zjskills -p 'test_validate_learning_system.py' -k interaction -q`

Expected: all interaction contract tests pass.

### Task 4: Migrate current public documentation and installation guidance

**Files:**
- Modify: `README.md`
- Modify: `README.en.md`
- Modify: `CONTRIBUTING.md`
- Modify: `docs/getting-started.md`
- Modify: `docs/getting-started.en.md`
- Modify: `docs/usage-guide.md`
- Modify: `docs/usage-guide.en.md`
- Modify: `docs/examples.md`
- Modify: `docs/examples.en.md`
- Modify: `docs/platform-installation.md`
- Modify: `docs/platform-installation.en.md`
- Modify: `docs/domain-pack-guide.md`
- Modify: `docs/domain-pack-guide.en.md`
- Modify: `tests/zjskills/test_open_source_package.py`

**Interfaces:**
- Consumes: new technical identifier, navigation contract, release version, and safe migration sequence.
- Produces: bilingual quick starts, current commands, examples, installation paths, and rollback-safe migration instructions.

- [ ] **Step 1: Update current paths, calls, URL, and version**

Replace active public references from `learning-architect` to `zjskills`, `$learning-architect` to `$zjskills`, `/learning-architect` to `/zjskills`, repository URL `zhijianZJ/ZJSklls` to `zhijianZJ/ZJSkills`, and version `1.0.0` to `2.0.0`. Do not mechanically rewrite historical files under `docs/superpowers/`.

- [ ] **Step 2: Put the navigation before the long planning prompt**

In both READMEs and getting-started guides, show the shortest `$zjskills`/`/zjskills` invocation and six-option navigation before the full learner-profile prompt. Explain that clear requests bypass the menu.

- [ ] **Step 3: Document interaction depth and global commands**

Add paired Chinese/English sections covering beginner, standard, and professional views; continue, back, unknown, switch method, view detail, change, save, and pause; and the distinction between dialogue navigation and version rollback.

- [ ] **Step 4: Add examples for every routing branch**

Add paired examples for ambiguous entry, numeric selection `4`, a direct 401 problem, unknown selection, resume with and without state, and requesting professional structured output.

- [ ] **Step 5: Add safe 1.x -> 2.0 migration instructions**

Document backup, new `zjskills` installation, explicit-call verification, learner-workspace verification, old-directory removal, and rollback. State that the learner workspace does not need to move and that old/new Skill directories must not remain discoverable together.

- [ ] **Step 6: Run public-package tests**

Run: `/Users/wangshucheng/miniconda3/bin/python3 -m unittest discover -s tests/zjskills -p 'test_open_source_package.py' -q`

Expected: all public-package, link, naming, platform, and runtime-neutrality tests pass.

### Task 5: Validate packaging and an isolated installation

**Files:**
- Modify only if validation reveals a contract defect.

**Interfaces:**
- Consumes: completed `zjskills/` package and current tests.
- Produces: validation evidence for package structure, learner fixture compatibility, and install-path discovery without mutating the user's active Skill installation.

- [ ] **Step 1: Validate Skill structure**

Run: `/Users/wangshucheng/miniconda3/bin/python3 /Users/wangshucheng/.codex/skills/.system/skill-creator/scripts/quick_validate.py zjskills`

Expected: `Skill is valid!`

- [ ] **Step 2: Validate the bundled learner fixture**

Run: `/Users/wangshucheng/miniconda3/bin/python3 zjskills/scripts/validate_learning_system.py --skill-root zjskills --learner-dir tests/zjskills/fixtures/valid-learner`

Expected: `VALID`.

- [ ] **Step 3: Test an isolated user-level installation**

Create `/tmp/zjskills-install-test/.agents/skills`, copy only `zjskills/` into its `zjskills/` child, then assert that `SKILL.md` contains `name: zjskills`, `agents/openai.yaml` contains `$zjskills`, and no sibling `learning-architect` exists. Remove only the temporary test root after assertions pass.

- [ ] **Step 4: Run the complete regression suite**

Run: `/Users/wangshucheng/miniconda3/bin/python3 -m unittest discover -s tests/zjskills -p 'test_*.py' -q`

Expected: all tests pass with no failures or errors.

### Task 6: Review, commit, push, and publish a Draft PR

**Files:**
- Modify only when a review or validation failure identifies an in-scope defect.

**Interfaces:**
- Consumes: the complete verified diff.
- Produces: a clean branch, one implementation commit, remote branch update, and a Draft PR with the complete 2.0.0 description. PR #4 was merged before this task completed, so the 2.0.0 work requires a new Draft PR.

- [ ] **Step 1: Review requirements and diff**

Run: `git diff --check`

Run: `git status -sb`

Run: `git diff --stat origin/main...HEAD`

Expected: no whitespace errors, no unrelated changes, and only one active runtime directory named `zjskills`.

- [ ] **Step 2: Commit the implementation**

Stage only runtime migration, tests, VERSION, current public docs, and this implementation plan. Commit with:

```text
feat: migrate runtime to zjskills
```

- [ ] **Step 3: Push the current branch**

Run: `git push origin codex/learning-architect`

Expected: remote branch advances to the implementation commit.

- [ ] **Step 4: Create the new Draft PR**

Create a Draft PR titled `feat: add guided learning UX and migrate to zjskills`. Include the navigation layer, breaking identifier migration, 2.0.0 upgrade guidance, exact test count, Skill validation, learner-fixture validation, isolated installation result, and behavioral evaluation. Keep the PR in Draft state until the user requests Ready for Review.
