# ZJSkills 3.0 Lightweight Career Diagnosis Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the ZJSkills Education OS runtime with a lightweight AI-first career diagnosis Skill that offers one-page diagnosis, compact learning routes, and one-step learning help.

**Architecture:** Ship one `zjskills` entry point and four on-demand references. Default to chat-only output, reuse conversation context, ask at most one decision-changing question, and expand only after user feedback. Remove schemas, templates, Domain Packs, validator scripts, and the 11-stage runtime while preserving public documentation, Git history, technical calls, and commercial neutrality.

**Tech Stack:** Markdown Skill instructions and bilingual docs, YAML `agents/openai.yaml`, Python `unittest` contract tests, Skill Creator `quick_validate.py`, Git/GitHub.

## Global Constraints

- Release version is `3.0.0`.
- Repository URL remains `https://github.com/zhijianZJ/ZJSkills.git`.
- Technical Skill name remains `zjskills`; explicit calls remain `$zjskills` and `/zjskills`.
- Installed runtime contains only `SKILL.md`, `agents/openai.yaml`, and exactly four references: `career-diagnosis.md`, `learning-route.md`, `learning-help.md`, and `ai-career-map.md`.
- Keep `SKILL.md` at approximately 180 lines or fewer and installed Markdown runtime at approximately 800 lines or fewer.
- Default output is chat-only; create one Markdown file only when the user explicitly asks to save, export, or maintain a route.
- Reuse conversation context; ask zero questions when evidence is sufficient and at most one decision-changing question when it is not.
- Default career-diagnosis output is one compact diagnosis and one minimum validation action.
- Default learning route has no more than three stages and one current-week action.
- Default learning-help output has one action, one observable success signal, one fallback, and an explicit route-impact judgment.
- AI careers receive domain-specific support; non-AI careers receive a general method with explicit knowledge boundaries.
- Do not promise employment, salary, promotion, revenue, clients, admissions, or external acceptance.
- Do not expose hidden chain-of-thought; show facts, inference, uncertainty, assumptions, and trade-offs.
- Runtime must not include 智建 contact, answer-group, purchase, course-conversion, community-conversion, or human-referral logic.
- Negative safeguards such as “do not require a specific paid course” are allowed; neutrality tests target promotional or conversion instructions rather than the literal phrase `paid course`.
- The exact 智建 support note appears only in paired public README, getting-started, usage, and platform-installation guides.
- Do not create a runtime `legacy/` directory; Git history is the archive.
- Never delete user-created learning files.
- Multi-platform docs cover Codex, Claude Code, Tencent WorkBuddy, Doubao, and generic file/context hosts without claiming unsupported native Skill behavior.
- Use `/Users/wangshucheng/miniconda3/bin/python3` for repository tests and validation.

---

### Task 1: Lock the lightweight runtime contract with failing tests

**Files:**
- Create: `tests/zjskills/test_lightweight_skill.py`
- Modify: `tests/zjskills/test_open_source_package.py`

**Interfaces:**
- Consumes the approved 3.0 design specification.
- Produces exact tracked-runtime inventory, size limits, three-mode behavior contracts, AI career-map contracts, context/question rules, output-shape rules, and commercial-neutrality checks.
- Does not alter runtime files.

- [ ] **Step 1: Add the tracked-runtime inventory helper**

Add this helper to `test_lightweight_skill.py`:

```python
from pathlib import Path
import subprocess
import unittest

REPO_ROOT = Path(__file__).resolve().parents[2]
RUNTIME_ROOT = REPO_ROOT / "zjskills"

EXPECTED_RUNTIME_FILES = {
    "zjskills/SKILL.md",
    "zjskills/agents/openai.yaml",
    "zjskills/references/ai-career-map.md",
    "zjskills/references/career-diagnosis.md",
    "zjskills/references/learning-help.md",
    "zjskills/references/learning-route.md",
}

def read_runtime(relative_path: str) -> str:
    return (RUNTIME_ROOT / relative_path).read_text(encoding="utf-8")

def tracked_runtime_files() -> set[str]:
    result = subprocess.run(
        ["git", "ls-files", "zjskills"],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return {line for line in result.stdout.splitlines() if line}
```

- [ ] **Step 2: Add exact structure and size tests**

```python
class LightweightSkillTests(unittest.TestCase):
    def test_runtime_contains_only_the_six_approved_files(self):
        self.assertEqual(tracked_runtime_files(), EXPECTED_RUNTIME_FILES)

    def test_runtime_respects_size_budgets(self):
        skill_lines = len(read_runtime("SKILL.md").splitlines())
        markdown_lines = sum(
            len((REPO_ROOT / path).read_text(encoding="utf-8").splitlines())
            for path in EXPECTED_RUNTIME_FILES
            if path.endswith(".md")
        )
        self.assertLessEqual(skill_lines, 180)
        self.assertLessEqual(markdown_lines, 800)
```

- [ ] **Step 3: Add entry and reference-contract tests**

Require:

- frontmatter `name: zjskills`;
- description triggers for AI career direction, learning route, and getting unstuck;
- exactly three modes named `career diagnosis`, `learning route`, and `learning help`;
- `$zjskills`, `/zjskills`, context-first behavior, zero-or-one-question rule, and conditional loading of all four references;
- career diagnosis sections for current situation, real problem, judgment, evidence, what not to do, minimum validation action, and result interpretation;
- route sections for target, starting point, three stages, evidence projects, and current-week action;
- learning-help sections for stuck point, likely cause, one action, success signal, fallback, and route impact;
- AI map coverage of AI Agent, Vibe Coding, AI Product, both AI Operations branches, and AI Tools/Workplace.

Use `assertIn` for exact contract phrases and `assertNotIn` for `11-stage`, `system-state.yaml`, `schema`, and `gate` in beginner-facing runtime instructions.

- [ ] **Step 4: Add commercial-neutrality tests without the false-positive conflict**

```python
    def test_runtime_has_no_referral_or_conversion_instructions(self):
        runtime = "\n".join(
            (REPO_ROOT / path).read_text(encoding="utf-8")
            for path in sorted(EXPECTED_RUNTIME_FILES)
            if path.endswith((".md", ".yaml"))
            and (REPO_ROOT / path).exists()
        ).lower()
        forbidden = (
            "联系智建",
            "答疑群",
            "加入社群",
            "加微信",
            "购买课程",
            "转化用户",
            "人工转介",
            "contact zhijian",
            "join the q&a group",
            "add wechat",
            "lead conversion",
        )
        for phrase in forbidden:
            self.assertNotIn(phrase, runtime, phrase)
```

Do not forbid the standalone literal `paid course`.

- [ ] **Step 5: Remove obsolete runtime assertions from open-source tests**

In `test_open_source_package.py`, remove assertions that require Domain Packs, schema validators, structured state, YAML artifacts, 11-stage navigation, or 2.0 runtime engine names. Keep current README/version assertions unchanged until Task 3 so this task only locks runtime behavior.

- [ ] **Step 6: Run tests and verify RED**

```bash
/Users/wangshucheng/miniconda3/bin/python3 -m unittest \
  tests.zjskills.test_lightweight_skill -q
```

Expected: FAIL because the exact six-file runtime, four new references, and lightweight contracts do not exist.

- [ ] **Step 7: Commit the RED contract**

```bash
git add tests/zjskills/test_lightweight_skill.py tests/zjskills/test_open_source_package.py
git commit -m "test: lock lightweight zjskills runtime"
```

---

### Task 2: Replace the Education OS runtime with the lightweight Skill

**Files:**
- Rewrite: `zjskills/SKILL.md`
- Modify: `zjskills/agents/openai.yaml`
- Create: `zjskills/references/career-diagnosis.md`
- Create: `zjskills/references/learning-route.md`
- Create: `zjskills/references/learning-help.md`
- Create: `zjskills/references/ai-career-map.md`
- Delete: `zjskills/assets/`
- Delete: `zjskills/scripts/`
- Delete: every existing file in `zjskills/references/` other than the four files above
- Delete: `tests/zjskills/test_validate_learning_system.py`
- Delete: `tests/zjskills/fixtures/`
- Delete: `tests/zjskills/v2-interaction-evaluation.md`
- Modify: `tests/zjskills/test_open_source_package.py`

**Interfaces:**
- `SKILL.md` routes one user request to one mode and loads only the matching references.
- `career-diagnosis.md` returns a compact diagnosis or one decisive question.
- `learning-route.md` returns at most three stages and one current-week action.
- `learning-help.md` returns one action, success signal, fallback, and route-impact judgment.
- `ai-career-map.md` supplies five visible AI directions, two Operations branches, five evidence dimensions, and six minimum experience tasks.
- No runtime file reads or depends on a deleted schema, template, script, Domain Pack, or engine reference.

- [ ] **Step 1: Rewrite `SKILL.md`**

Use only `name` and `description` in frontmatter. The body must contain these sections:

```markdown
# ZJSkills

## Identity

Act as an AI-first career diagnostician.
Do not act as a course recommender, fixed questionnaire, or default long-plan generator.
Diagnose the current problem, state the evidence boundary, and advance one useful step.

## Start

Read the current conversation first.
Reuse facts, goals, constraints, prior conclusions, and feedback already supplied.
If evidence is sufficient, work immediately.
If one missing fact could change the judgment, ask only that one question.

## Choose One Mode

1. Career diagnosis
2. Learning route
3. Learning help

## Load Only What Is Needed

[conditional table for the four approved references]

## Shared Rules

[context, evidence, uncertainty, one-action, non-AI, safety, commercial-neutrality, save-only-on-request rules]

## Continue

Use the user's observed result to choose the next mode.
Do not predeclare a fixed chain.
```

Keep the complete file at 180 lines or fewer. Use `$zjskills` and `/zjskills` explicitly.

- [ ] **Step 2: Update `agents/openai.yaml`**

Use:

```yaml
interface:
  display_name: ZJSkills
  short_description: AI 职业诊断、学习路线与学习解题
  default_prompt: Use $zjskills to diagnose my current AI career or learning situation and give me the single most useful next step.
```

Do not add optional interface fields without user-provided values.

- [ ] **Step 3: Write `career-diagnosis.md`**

Include:

- triggers for direction, fit, feasibility, expectation, and learning-support decisions;
- known-fact / inference / uncertainty separation;
- the five evidence dimensions;
- the zero-or-one decisive-question rule;
- allowed judgments: stronger fit, worth testing with risk, do not invest heavily yet, insufficient evidence;
- exact compact output order;
- neutral treatment of self-study versus structured support;
- no external-outcome promise.

- [ ] **Step 4: Write `ai-career-map.md`**

For each direction, include only work object, strong evidence, common false positive, primary risk, and minimum experience task:

- AI Agent Development;
- Vibe Coding / AI Application Building;
- AI Product Management;
- AI Operations: Content/Growth;
- AI Operations: Business Efficiency;
- AI Tools and Workplace Application.

State that AI Tools/Workplace is usually a cross-role capability rather than automatically a standalone job.

- [ ] **Step 5: Write `learning-route.md`**

Define the exact output:

```text
Target
Current starting point
Stage 1: capability and deliverable
Stage 2: capability and deliverable
Stage 3: target-level deliverable
Evidence project for each stage
Only this week's action
Biggest assumption or constraint
```

Allow fewer than three stages when sufficient. Put outcomes before resources. Save one Markdown route only when explicitly requested, with diagnosis, target, stages, current action, evidence, and update log.

- [ ] **Step 6: Write `learning-help.md`**

Define the exact output:

```text
Where you are stuck
Most likely cause
Do this one action first
Observable success signal
If it fails, check this next
Route impact
```

Cover concept confusion, action gap, project start, tool/error evidence, missed work, changed goal, and supplied material. For material, classify fact/opinion/example/inference/unknown and produce one retrieval, practice, or transfer action.

- [ ] **Step 7: Delete the legacy runtime and validator suite**

Delete all tracked files under `zjskills/assets/` and `zjskills/scripts/`. Delete the old references named in the tracked tree, leaving exactly the four approved references. Delete the schema/learner validator test, all learner fixtures, and the v2 evaluation report.

Update remaining open-source tests so they no longer import or require the removed validator, Domain Pack guide, artifact state, or YAML fixtures.

- [ ] **Step 8: Run focused and full tests**

```bash
/Users/wangshucheng/miniconda3/bin/python3 -m unittest \
  tests.zjskills.test_lightweight_skill -q
/Users/wangshucheng/miniconda3/bin/python3 -m unittest discover \
  -s tests/zjskills -p 'test_*.py' -q
/Users/wangshucheng/miniconda3/bin/python3 \
  /Users/wangshucheng/.codex/skills/.system/skill-creator/scripts/quick_validate.py \
  zjskills
```

Expected: all remaining tests PASS; quick validator prints `Skill is valid!`; tracked runtime equals the six approved files.

- [ ] **Step 9: Commit**

```bash
git add -A zjskills tests/zjskills
git commit -m "feat: simplify zjskills into career diagnosis"
```

---

### Task 3: Rewrite bilingual public documentation for 3.0

**Files:**
- Modify: `README.md`
- Modify: `README.en.md`
- Modify: `VERSION`
- Modify: `CHANGELOG.md`
- Modify: `CONTRIBUTING.md`
- Modify: `docs/getting-started.md`
- Modify: `docs/getting-started.en.md`
- Modify: `docs/usage-guide.md`
- Modify: `docs/usage-guide.en.md`
- Modify: `docs/examples.md`
- Modify: `docs/examples.en.md`
- Modify: `docs/platform-installation.md`
- Modify: `docs/platform-installation.en.md`
- Delete: `docs/domain-pack-guide.md`
- Delete: `docs/domain-pack-guide.en.md`
- Modify: `tests/zjskills/test_open_source_package.py`

**Interfaces:**
- Public message: AI-first career diagnosis, then compact route or current learning help.
- Public usage mirrors three runtime modes and one-step interaction.
- Exact transparent 智建 note appears in four Chinese surfaces and its English equivalent in four paired English surfaces, never in runtime.
- Installation remains accurate for five platform categories.

- [ ] **Step 1: Add RED 3.0 documentation tests**

Require:

- `VERSION` equals `3.0.0`;
- both README files show `3.0.0`;
- Chinese headings for `职业诊断`, `学习路线`, and `学习解题`;
- English headings for `Career diagnosis`, `Learning route`, and `Learning help`;
- no `Domain Pack`, `11 阶段`, `11-stage`, `system-state.yaml`, or `--learner-dir` in current public usage guidance;
- deleted Domain Pack guides do not exist;
- copy-paste prompts for direction uncertainty, route generation, and a learning blocker;
- the exact support notes in required public files;
- runtime support-note absence remains passing.

- [ ] **Step 2: Rewrite README pair**

Lead with:

```text
Tell ZJSkills your real AI career or learning situation.
It diagnoses the current problem, explains the evidence boundary,
and gives one useful next step.
```

Explain three modes, five visible AI directions, zero-or-one-question policy, no default files, non-AI boundary, supported platforms, installation link, and support note.

- [ ] **Step 3: Rewrite getting-started pair**

Show:

- one messy first input;
- what a one-page diagnosis contains;
- how `继续` expands to a route;
- how `我卡住了` enters learning help;
- how to request a saved Markdown route;
- the public support note.

- [ ] **Step 4: Rewrite usage-guide pair**

Document mode selection, evidence categories, AI directions, minimum experience tasks, three-stage route, learning-help output, material handling, non-AI limits, safety, commercial neutrality, and saved Markdown shape.

- [ ] **Step 5: Rewrite examples pair**

Include paired examples for:

1. vague AI transition;
2. Agent versus Vibe Coding;
3. no coding evidence;
4. neutral self-study versus structured-support judgment;
5. concept confusion;
6. project error;
7. missed week;
8. changed goal;
9. non-AI request.

- [ ] **Step 6: Update platform guides**

Keep Codex, Claude Code, Tencent WorkBuddy, Doubao, and generic context hosts. Replace schema/validator verification with:

- installed directory contains `SKILL.md`;
- four references exist;
- `$zjskills` or `/zjskills` responds with a diagnosis;
- native support and manual file/context use are clearly distinguished.

Include 2.x-to-3.0 migration: back up the installed Skill, replace it, keep user-created learning files, and optionally summarize old YAML workspaces into Markdown.

- [ ] **Step 7: Update contribution and release files**

Set `VERSION` to `3.0.0`. Add a changelog entry dated `2026-07-20`. Rewrite contribution guidance around concise references, interaction tests, no runtime promotion, bilingual docs, and no new runtime file without forward-test evidence.

- [ ] **Step 8: Run tests and commit**

```bash
/Users/wangshucheng/miniconda3/bin/python3 -m unittest \
  tests.zjskills.test_open_source_package -q
/Users/wangshucheng/miniconda3/bin/python3 -m unittest discover \
  -s tests/zjskills -p 'test_*.py' -q
git add -A README.md README.en.md VERSION CHANGELOG.md CONTRIBUTING.md docs tests/zjskills
git commit -m "docs: publish zjskills 3.0 guidance"
```

Expected: all tests PASS; all relative documentation links resolve.

---

### Task 4: Forward-test real interactions and correct only observed failures

**Files:**
- Rewrite: `tests/zjskills/scenarios.yaml`
- Create: `tests/zjskills/v3-forward-evaluation.md`
- Modify: `tests/zjskills/test_lightweight_skill.py`
- Modify runtime files only after a failing scenario demonstrates the need.

**Interfaces:**
- Scenario IDs: `vague-ai-transition`, `compare-agent-vibe`, `no-coding-evidence`, `training-decision`, `concept-confusion`, `incomplete-error`, `missed-week`, `changed-goal`, `non-ai-without-source`, `enough-context-no-question`.
- Each evaluation records mode, question count, main action count, facts/inference/uncertainty, promise boundary, commercial neutrality, concision, and verdict.
- Raw evaluator prompts do not reveal expected outputs or suspected defects.

- [ ] **Step 1: Rewrite scenario inventory**

Use these exact scenario inputs:

```yaml
scenarios:
  - {id: vague-ai-transition, language: zh-CN, prompt: "我想转行 AI，但不知道该学什么。"}
  - {id: compare-agent-vibe, language: zh-CN, prompt: "我在 AI Agent 开发和 Vibe Coding 之间犹豫。我会一点 Python，但还没独立部署过项目。"}
  - {id: no-coding-evidence, language: zh-CN, prompt: "我零编程基础，看到 Agent 工程师工资高，所以想三个月转行。"}
  - {id: training-decision, language: zh-CN, prompt: "我该自学还是报一个系统课程？我每周能学 8 小时，做过一次 AI 表格自动化，但没人带我复盘。"}
  - {id: concept-confusion, language: zh-CN, prompt: "我一直没搞懂 RAG 和直接把资料放进上下文有什么区别。"}
  - {id: incomplete-error, language: zh-CN, prompt: "我做的 AI 小工具报错了，运行不起来，怎么办？"}
  - {id: missed-week, language: zh-CN, prompt: "这周计划的三个任务我一个都没完成，下周是不是要全部补回来？"}
  - {id: changed-goal, language: zh-CN, prompt: "我原来想找 Agent 开发工作，现在更想先用 AI 提升现有运营岗位，学习路线怎么调整？"}
  - {id: non-ai-without-source, language: zh-CN, prompt: "我想转行营养师，请直接告诉我从零到就业要学什么。"}
  - {id: enough-context-no-question, language: en, prompt: "I work in operations, use spreadsheets daily, have 5 hours a week, and want to automate weekly reporting before considering a career switch. Give me the best next step."}
evaluation_dimensions:
  - mode
  - question_count
  - main_action_count
  - evidence_boundary
  - promise_boundary
  - commercial_neutrality
  - beginner_readability
```

Do not add expected answers to the scenario prompts.

- [ ] **Step 2: Add scenario-contract tests**

Require exactly ten IDs, nonempty prompts, the seven evaluation dimensions above, and no expected-output leakage terms such as `must answer`, `expected response`, `应该输出`, or `正确答案`.

- [ ] **Step 3: Run fresh-context forward evaluations**

For each scenario, dispatch a fresh evaluator. Its complete instruction is the fixed prefix:

```text
Use $zjskills at /Users/wangshucheng/Documents/AI职业培训教育课程设计/.worktrees/learning-architect/zjskills to respond to this user:
```

followed only by that scenario's exact `prompt` value from Step 1. For example, the complete first dispatch is:

```text
Use $zjskills at /Users/wangshucheng/Documents/AI职业培训教育课程设计/.worktrees/learning-architect/zjskills to respond to this user:
我想转行 AI，但不知道该学什么。
```

Do not show the design, expected behavior, or prior diagnosis. Save raw outputs outside the repository under a unique temporary evaluation directory.

- [ ] **Step 4: Score outputs**

Create `v3-forward-evaluation.md` with one row per scenario:

```markdown
| Scenario | Mode | Questions | Main actions | Evidence boundary | Neutral | Concise | Verdict |
```

A scenario passes only when:

- mode is appropriate;
- questions are zero when context is enough and no more than one otherwise;
- one main action is given;
- facts, inference, and uncertainty are distinguishable when a judgment is made;
- no unsupported promise/domain authority appears;
- no course/community/referral conversion appears;
- response is beginner-readable.

- [ ] **Step 5: Fix observed failures with RED/GREEN evidence**

For every failed scenario:

1. add one focused assertion reproducing the behavior contract;
2. run it and capture RED;
3. make the smallest runtime edit;
4. rerun focused and complete tests;
5. rerun only the failed forward scenario with a fresh context;
6. update the evaluation row with the new verdict.

Do not add a file or general framework for a one-scenario wording defect.

- [ ] **Step 6: Run all tests and commit**

```bash
/Users/wangshucheng/miniconda3/bin/python3 -m unittest discover \
  -s tests/zjskills -p 'test_*.py' -q
git add zjskills tests/zjskills
git commit -m "test: forward evaluate zjskills career diagnosis"
```

Expected: all automated tests PASS and all ten scenario rows are PASS.

---

### Task 5: Verify the isolated package, review the branch, and publish a Draft PR

**Files:**
- Modify only when a failed check proves a contract defect.
- Do not change the approved design or add runtime features during release cleanup.

**Interfaces:**
- Produces a clean `codex/zjskills-learning-routes` branch and a new Draft PR.
- Does not merge, create a GitHub release, or alter PR #5.

- [ ] **Step 1: Run complete tests and Skill validation**

```bash
/Users/wangshucheng/miniconda3/bin/python3 -m unittest discover \
  -s tests/zjskills -p 'test_*.py' -q
/Users/wangshucheng/miniconda3/bin/python3 \
  /Users/wangshucheng/.codex/skills/.system/skill-creator/scripts/quick_validate.py \
  zjskills
```

Expected: zero failures/errors and `Skill is valid!`.

- [ ] **Step 2: Verify exact tracked runtime and budgets**

```bash
git ls-files zjskills
wc -l zjskills/SKILL.md zjskills/references/*.md
```

Expected: exactly six tracked files; `SKILL.md` at most 180 lines; Markdown total at most 800 lines.

- [ ] **Step 3: Test isolated installation**

```bash
install_root="$(mktemp -d)"
mkdir -p "$install_root/zjskills"
cp -R zjskills/. "$install_root/zjskills/"
/Users/wangshucheng/miniconda3/bin/python3 \
  /Users/wangshucheng/.codex/skills/.system/skill-creator/scripts/quick_validate.py \
  "$install_root/zjskills"
test -f "$install_root/zjskills/references/career-diagnosis.md"
test -f "$install_root/zjskills/references/learning-route.md"
test -f "$install_root/zjskills/references/learning-help.md"
test -f "$install_root/zjskills/references/ai-career-map.md"
```

Expected: isolated validation prints `Skill is valid!` and all four reference checks return status 0.

- [ ] **Step 4: Audit names, links, neutrality, and placeholders**

```bash
rg -n "LearningArchitectSklls|king-wsc|TO[D]O|T[B]D|PLACE[H]OLDER" \
  README.md README.en.md VERSION CHANGELOG.md CONTRIBUTING.md docs zjskills tests/zjskills \
  -g '!docs/superpowers/**'
rg -ni "联系智建|答疑群|加入社群|加微信|购买课程|转化用户|人工转介|contact zhijian|join the q&a group|lead conversion" \
  zjskills
git diff --check
git status --short
```

Expected: no obsolete names/placeholders; no runtime promotion/referral matches; no whitespace errors; clean status after commits.

- [ ] **Step 5: Request final whole-branch review**

Use `superpowers:requesting-code-review` with a review package from branch start `ca9b746` through current HEAD. Give the reviewer both:

- `docs/superpowers/specs/2026-07-20-zjskills-lightweight-career-diagnosis-design.md`;
- this implementation plan.

Resolve every confirmed Critical or Important finding with a focused failing test, one fix subagent, covering tests, and re-review.

- [ ] **Step 6: Use the branch-finishing workflow**

Invoke `superpowers:finishing-a-development-branch`. Keep the user-selected outcome as push plus new Draft PR; do not merge locally.

- [ ] **Step 7: Push and open the new Draft PR**

```bash
git push -u origin codex/zjskills-learning-routes
gh pr create \
  --draft \
  --base main \
  --head codex/zjskills-learning-routes \
  --title "feat: simplify ZJSkills into AI career diagnosis" \
  --body-file docs/superpowers/specs/2026-07-20-zjskills-lightweight-career-diagnosis-design.md
```

Expected: GitHub returns a Draft PR URL distinct from PR #5.

## Final Acceptance Checklist

- [ ] Runtime has exactly six tracked files and four focused references.
- [ ] `SKILL.md` is at most 180 lines and runtime Markdown is at most 800 lines.
- [ ] `$zjskills` and `/zjskills` remain the only public technical calls.
- [ ] Career diagnosis, learning route, and learning help satisfy their compact output contracts.
- [ ] Five AI directions, two Operations branches, and six experience tasks are covered.
- [ ] Non-AI help labels domain limits.
- [ ] Runtime contains no human referral or commercial-conversion behavior.
- [ ] The negative `paid course` safeguard is not falsely rejected.
- [ ] Public bilingual docs show version `3.0.0`, supported platforms, migration, and the approved support note.
- [ ] Ten forward evaluations pass without expected-output leakage.
- [ ] Complete tests, quick validation, isolated installation, diff checks, and final review pass.
- [ ] Branch is pushed and presented in a new Draft PR without altering PR #5.
