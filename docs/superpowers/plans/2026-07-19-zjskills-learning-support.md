# ZJSkills Learning Support Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a beginner-friendly learning-support loop that decomposes in-progress learning problems, verifies one next action, and escalates only the necessary part of the learning plan.

**Architecture:** Keep the existing 11-stage planning state machine unchanged and add a horizontal problem-solving loop. A focused problem-solving reference owns diagnosis and plan-impact decisions, a beginner-interaction reference owns the default response shape, and a typed `learning-issue` artifact enables optional persistence and validation.

**Tech Stack:** Markdown Skill instructions, YAML Draft 2020-12 schemas and templates, Python 3.9+ validator, `unittest`, `PyYAML`, `jsonschema`, `referencing`.

## Global Constraints

- Runtime directory and technical skill identifier remain `learning-architect`; public documentation uses `ZJSkills`.
- The canonical 11 workflow stages remain in their current order.
- Runtime content stays brand- and promotion-neutral.
- Default user-facing replies use plain language and hide YAML or engine jargon unless requested.
- Complex guided diagnosis asks no more than one decision-changing question per turn.
- Plan changes use the minimum impact level: `none`, `task`, `week`, `roadmap`, or `goal_system`.
- Existing artifacts and active versions are never silently overwritten.

---

### Task 1: Lock the new behavior with failing contract tests

**Files:**
- Modify: `tests/learning-architect/test_validate_learning_system.py`
- Modify: `tests/learning-architect/test_open_source_package.py`
- Modify: `tests/learning-architect/scenarios.yaml`

**Interfaces:**
- Consumes: the approved design specification.
- Produces: failing assertions for new references, routing terms, schema/template assets, validator mapping, beginner documentation, and eight pressure scenarios.

- [ ] **Step 1: Add runtime contract tests**

Add tests that require `problem-solving-engine.md`, `beginner-interaction.md`, `learning-issue.schema.yaml`, `learning-issue.yaml`, the five impact levels, the three routing modes, the six-card reply shape, and canonical `engine_result` usage.

- [ ] **Step 2: Add validator contract tests**

Add a valid learning-issue fixture generated in-test, then mutate it to verify rejection of an absent `success_signal`, an invalid impact level, and `goal_system` without `rollback_target: goal-analysis`.

- [ ] **Step 3: Add public-document and scenario tests**

Require Chinese and English guides to expose beginner problem-solving phrases and append eight scenarios with IDs `concept-confusion`, `theory-action-gap`, `tool-error-401`, `project-first-step`, `missed-week`, `capacity-drop`, `learning-goal-change`, and `unknown-blocker`.

- [ ] **Step 4: Run tests and verify RED**

Run: `python3 -m unittest tests.learning-architect.test_validate_learning_system tests.learning-architect.test_open_source_package -q`

Expected: FAIL because the new files, schema registry entry, documentation sections, and scenarios do not exist yet.

### Task 2: Implement the runtime learning-support contracts

**Files:**
- Create: `learning-architect/references/problem-solving-engine.md`
- Create: `learning-architect/references/beginner-interaction.md`
- Modify: `learning-architect/SKILL.md`
- Modify: `learning-architect/references/workflow.md`
- Modify: `learning-architect/references/planner-engine.md`
- Modify: `learning-architect/references/assessment-engine.md`
- Modify: `learning-architect/references/optimization-engine.md`
- Modify: `learning-architect/references/meta-learning-engine.md`

**Interfaces:**
- Consumes: natural-language learning issue, current stage/artifact context, evidence and constraints.
- Produces: `engine_result` with `engine: problem-solving`, one user action or one question, a success signal, fallback, and one impact level.

- [ ] **Step 1: Write the problem-solving engine**

Define the nine issue types, three routing modes, eight-step loop, evidence rules, five plan-impact levels, escalation conditions, safety handoff, and return contract.

- [ ] **Step 2: Write the beginner interaction layer**

Define plain-language triggers, progressive disclosure, the six-card output order, one-question guided mode, “I don't know” recovery choices, and jargon-free wording rules.

- [ ] **Step 3: Add entrypoint routing**

Extend the frontmatter trigger description and reference-loading table. Add a short “During Learning” section without changing the numbered 11-stage workflow.

- [ ] **Step 4: Integrate existing engines**

Route `task`/`week` to Weekly Planner, `roadmap` to Roadmap plus affected downstream checks, `goal_system` to Goal Analysis, repeated method evidence to Meta-Learning, and resolved observations to Assessment without treating issue closure as capability proof.

- [ ] **Step 5: Run runtime contract tests**

Run: `python3 -m unittest tests.learning-architect.test_validate_learning_system.LearningSystemValidationTests.test_learning_support_runtime_contract -q`

Expected: PASS.

### Task 3: Add the learning-issue artifact and validator support

**Files:**
- Create: `learning-architect/assets/schemas/learning-issue.schema.yaml`
- Create: `learning-architect/assets/templates/learning-issue.yaml`
- Modify: `learning-architect/scripts/validate_learning_system.py`
- Modify: `tests/learning-architect/test_validate_learning_system.py`

**Interfaces:**
- Consumes: YAML document using the approved `learning-issue` fields.
- Produces: schema validation through `SCHEMA_NAMES`, artifact discovery from `learning-issue.yaml` and `learning-issues/*.yaml`, plus semantic validation for goal-level rollback.

- [ ] **Step 1: Add the schema**

Define exact enums for issue type, routing mode, resolution status, and plan impact; require a nonempty next action, success signal, fallback action, impact reason, and next check.

- [ ] **Step 2: Add the worked template**

Create a beginner API 401 example using `routing_mode: direct_action`, `plan_impact.level: none`, observable success and fallback actions, and draft status.

- [ ] **Step 3: Register artifact paths**

Add `learning-issue` to `SCHEMA_NAMES`, root singleton filename mapping, and `learning-issues` directory mapping while allowing multiple active issue IDs.

- [ ] **Step 4: Enforce goal-system semantics**

When `plan_impact.level` is `goal_system`, emit an error unless `rollback_target` is exactly `goal-analysis` and `affected_artifacts` is nonempty.

- [ ] **Step 5: Run schema tests**

Run: `python3 -m unittest tests.learning-architect.test_validate_learning_system.LearningSystemValidationTests.test_learning_issue_schema_and_semantics -q`

Expected: PASS for the template and valid mutation set; invalid mutations are rejected.

### Task 4: Add bilingual beginner usage documentation

**Files:**
- Modify: `README.md`
- Modify: `README.en.md`
- Modify: `docs/getting-started.md`
- Modify: `docs/getting-started.en.md`
- Modify: `docs/usage-guide.md`
- Modify: `docs/usage-guide.en.md`
- Modify: `docs/examples.md`
- Modify: `docs/examples.en.md`

**Interfaces:**
- Consumes: the six-card interaction contract and five impact levels.
- Produces: copy-paste prompts and paired Chinese/English explanations for “I'm stuck,” problem follow-up, and plan adjustment.

- [ ] **Step 1: Update README value and workflow**

Add learning-problem decomposition and in-progress adaptation to “what it solves,” outputs, workflow, and documentation links without changing repository naming or runtime identifier guidance.

- [ ] **Step 2: Add getting-started entrypoints**

Add “学习中遇到问题” / “When you get stuck” sections with plain phrases, one copy-paste prompt, and an explanation of direct versus guided mode.

- [ ] **Step 3: Add full manual contracts**

Document the nine problem types, six-card response, five adjustment levels, persistence behavior, evidence boundary, and safety handoff in both languages.

- [ ] **Step 4: Add paired examples**

Add concept confusion, 401 error, missed week, and goal-change mini-dialogues in Chinese and English.

- [ ] **Step 5: Run documentation tests**

Run: `python3 -m unittest tests.learning-architect.test_open_source_package -q`

Expected: PASS with all relative links resolved and brand-neutral runtime unchanged.

### Task 5: Complete verification and package review

**Files:**
- Modify only if a verification failure identifies a contract defect.

**Interfaces:**
- Consumes: all runtime, schema, validator, scenario, and documentation changes.
- Produces: a clean, validated open-source package.

- [ ] **Step 1: Run Skill quick validation**

Run: `python3 "${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-creator/scripts/quick_validate.py" learning-architect`

Expected: `Skill is valid!`

- [ ] **Step 2: Run the complete regression suite**

Run: `python3 -m unittest discover -s tests/learning-architect -p "test_*.py" -q`

Expected: all tests pass.

- [ ] **Step 3: Validate the bundled learner fixture**

Run: `python3 learning-architect/scripts/validate_learning_system.py --skill-root learning-architect --learner-dir tests/learning-architect/fixtures/valid-learner`

Expected: `Validation passed`.

- [ ] **Step 4: Inspect repository changes**

Run: `git diff --check && git status -sb`

Expected: no whitespace errors; only intended files are modified or added.
