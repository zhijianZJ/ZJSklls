# ZJSkills 3.1 Career Consulting Loop Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add evidence-bounded career-asset translation, a returned-result stage decision, and a current-market evidence boundary while preserving ZJSkills' lightweight three-mode runtime.

**Architecture:** Keep the six-file runtime and strengthen the existing Career Diagnosis reference. Put cross-mode routing and evidence rules in `SKILL.md`, detailed diagnosis behavior in `references/career-diagnosis.md`, and route handoff behavior in `references/learning-route.md`; update bilingual public documentation only after runtime contracts pass.

**Tech Stack:** Markdown Agent Skill files, YAML scenario inventory and interface metadata, Python `unittest`, Git.

## Global Constraints

Post-review clarifications supersede narrower examples later in this plan:

- opportunity-level validation ideas are alternatives; select one current action by expected reduction in decision uncertainty, without requiring a leading hypothesis;
- a returned-result review retains the seven Career Diagnosis headings as a compact delta, with only one selected stage decision and one next action in the seventh section;
- reuse any supplied target period before asking for missing market scope, so the `current-market-without-region` scenario asks only for its missing region or states that boundary.

- Release version is exactly `3.1.0`.
- Keep exactly three modes: Career Diagnosis, Learning Route, and Learning Help.
- Keep exactly six tracked runtime files under `zjskills/`.
- Keep `zjskills/SKILL.md` at 180 lines or fewer and all runtime Markdown at 800 lines or fewer.
- Ask zero or one decision-changing question per reply.
- End with one current action rather than a backlog.
- Do not add a fixed questionnaire, fourth mode, default long report, Top 5 job list, star rating, percentage fit score, schema, script, template, state file, referral, or conversion path.
- Current salary, hiring volume, talent shortage, employer demand, job-title prevalence, and market-window claims require current attributable evidence.
- Chinese and English learner-facing documentation must remain paired.
- Preserve the exact public support notes and keep them outside runtime files.

---

## File Map

- `zjskills/SKILL.md`: thin routing, shared asset boundary, returned-result continuity, and current-market claim boundary.
- `zjskills/references/career-diagnosis.md`: asset translation, opportunity hypotheses, seven-section output, four stage decisions, and market evidence protocol.
- `zjskills/references/learning-route.md`: consume demonstrated assets and a route-ready handoff.
- `zjskills/agents/openai.yaml`: keep UI metadata aligned with the stronger diagnosis promise.
- `tests/zjskills/test_lightweight_skill.py`: runtime inventory, size, output-contract, asset, closure, and market tests.
- `tests/zjskills/scenarios.yaml`: fifteen non-leaking forward prompts and ten evaluation dimensions.
- `tests/zjskills/test_open_source_package.py`: version and bilingual documentation contracts.
- `README.md`, `README.en.md`: concise public product promise.
- `docs/getting-started.md`, `docs/getting-started.en.md`: copy-paste prompts and returned-result continuation.
- `docs/usage-guide.md`, `docs/usage-guide.en.md`: complete asset, closure, and market rules.
- `docs/examples.md`, `docs/examples.en.md`: twelve public scenarios.
- `docs/platform-installation.md`, `docs/platform-installation.en.md`: 3.1.0 version and replacement guidance.
- `VERSION`, `CHANGELOG.md`: release metadata.

---

### Task 1: Add Evidence-Bounded Career Asset Translation

**Files:**
- Modify: `tests/zjskills/test_lightweight_skill.py`
- Modify: `zjskills/SKILL.md`
- Modify: `zjskills/references/career-diagnosis.md`
- Modify: `zjskills/agents/openai.yaml`

**Interfaces:**
- Consumes: current Career Diagnosis mode, five evidence dimensions, zero-or-one-question policy.
- Produces: `Demonstrated asset`, `Transfer hypothesis`, and `Unverified boundary` categories plus at most three opportunity hypotheses.

- [ ] **Step 1: Write the RED asset-translation tests**

Replace the old seven-heading assertion in `test_career_diagnosis_has_the_compact_output_contract` with:

```python
self.assert_markdown_sections_in_order(
    diagnosis,
    (
        "Your current situation",
        "Your transferable career assets",
        "The real problem to solve",
        "Opportunity hypotheses",
        "My judgment and evidence",
        "One minimum validation action",
        "How the result changes the decision",
    ),
)
```

Add:

```python
def test_career_diagnosis_translates_assets_without_inventing_them(self):
    diagnosis = read_runtime("references/career-diagnosis.md")
    for phrase in (
        "Demonstrated asset",
        "Transfer hypothesis",
        "Unverified boundary",
        "observed work or result",
        "problem solved",
        "demonstrated capability",
        "possible AI transfer",
        "missing evidence",
    ):
        self.assert_contract_phrase(diagnosis, phrase)
    self.assertIn("no more than three opportunity hypotheses", diagnosis)
    self.assertIn("Do not infer capability from a title, employer, degree, or years of experience alone.", diagnosis)

def test_skill_keeps_asset_reasoning_evidence_bounded(self):
    skill = read_runtime("SKILL.md")
    self.assertIn("Translate observed work and results into demonstrated assets", skill)
    self.assertIn("Label possible transfer as a hypothesis until new-task evidence supports it.", skill)
```

- [ ] **Step 2: Run the focused tests and verify RED**

Run:

```bash
python3 -m unittest \
  tests.zjskills.test_lightweight_skill.LightweightSkillTests.test_career_diagnosis_has_the_compact_output_contract \
  tests.zjskills.test_lightweight_skill.LightweightSkillTests.test_career_diagnosis_translates_assets_without_inventing_them \
  tests.zjskills.test_lightweight_skill.LightweightSkillTests.test_skill_keeps_asset_reasoning_evidence_bounded
```

Expected: FAIL because the new headings and asset categories do not exist.

- [ ] **Step 3: Implement the minimal runtime contract**

Add one shared rule to `zjskills/SKILL.md`:

```markdown
- Career assets: Translate observed work and results into demonstrated assets. Label possible transfer as a hypothesis until new-task evidence supports it. Do not infer capability from a title, employer, degree, or years alone.
```

In `zjskills/references/career-diagnosis.md`, define:

```markdown
Translate experience through:

observed work or result → problem solved → demonstrated capability → possible AI transfer → missing evidence

- **Demonstrated asset:** supported by a task, result, responsibility, artifact, or repeated behavior the user supplied.
- **Transfer hypothesis:** a named way that asset may create value in an AI direction or AI-enhanced current role.
- **Unverified boundary:** the missing fact or performance needed before relying on that transfer.

Do not infer capability from a title, employer, degree, or years of experience alone. When a broad title hides the work performed, ask at most one question about the problem the user repeatedly solved.

For a direction decision, give no more than three opportunity hypotheses and prefer one or two. For each, name the work object, demonstrated asset reused, primary gap, and one task that can raise or lower confidence.
```

Replace the output headings with the seven headings asserted by the RED test. Keep known facts, inference, and uncertainty inside the relevant sections.

Update `zjskills/agents/openai.yaml` to:

```yaml
interface:
  display_name: ZJSkills
  short_description: AI 职业资产诊断、学习路线与学习解题
  default_prompt: Use $zjskills to diagnose my AI career situation, identify transferable assets, and give me the single most useful next step.
```

- [ ] **Step 4: Run focused and full tests**

Run:

```bash
python3 -m unittest tests.zjskills.test_lightweight_skill -v
python3 -m unittest discover -s tests/zjskills -p 'test_*.py'
```

Expected: all existing and new tests PASS.

- [ ] **Step 5: Commit Task 1**

```bash
git add tests/zjskills/test_lightweight_skill.py zjskills/SKILL.md zjskills/references/career-diagnosis.md zjskills/agents/openai.yaml
git commit -m "feat: translate transferable career assets"
```

---

### Task 2: Close the Consultation Loop with One Stage Decision

**Files:**
- Modify: `tests/zjskills/test_lightweight_skill.py`
- Modify: `zjskills/SKILL.md`
- Modify: `zjskills/references/career-diagnosis.md`
- Modify: `zjskills/references/learning-route.md`

**Interfaces:**
- Consumes: the minimum validation action and the user's returned observed result.
- Produces: exactly one of `Route ready`, `Comparison remains`, `Foundation or constraint first`, or `Current-role application first`.

- [ ] **Step 1: Write the RED closure tests**

Add:

```python
def test_career_diagnosis_defines_exactly_four_stage_decisions(self):
    diagnosis = read_runtime("references/career-diagnosis.md")
    decisions = re.findall(r"(?m)^\d+\. \*\*(.+?):\*\*", diagnosis)
    self.assertEqual(
        decisions,
        [
            "Route ready",
            "Comparison remains",
            "Foundation or constraint first",
            "Current-role application first",
        ],
    )

def test_returned_result_reuses_context_and_closes_one_stage(self):
    skill = read_runtime("SKILL.md")
    for phrase in (
        "When the user returns with a minimum-task result, reuse the prior diagnosis.",
        "Choose exactly one stage decision",
        "Do not repeat intake.",
    ):
        self.assert_contract_phrase(skill, phrase)

def test_learning_route_consumes_the_route_ready_handoff(self):
    route = read_runtime("references/learning-route.md")
    for phrase in (
        "stage decision",
        "demonstrated assets",
        "target direction",
        "primary gap",
        "important constraint",
    ):
        self.assertIn(phrase, route)
```

- [ ] **Step 2: Run the focused tests and verify RED**

Run:

```bash
python3 -m unittest \
  tests.zjskills.test_lightweight_skill.LightweightSkillTests.test_career_diagnosis_defines_exactly_four_stage_decisions \
  tests.zjskills.test_lightweight_skill.LightweightSkillTests.test_returned_result_reuses_context_and_closes_one_stage \
  tests.zjskills.test_lightweight_skill.LightweightSkillTests.test_learning_route_consumes_the_route_ready_handoff
```

Expected: FAIL because no stage-decision contract exists.

- [ ] **Step 3: Implement closure and route handoff**

Add to `SKILL.md` under `Continue`:

```markdown
When the user returns with a minimum-task result, reuse the prior diagnosis. Do not repeat intake. Choose exactly one stage decision from the Career Diagnosis reference, then end with one next action.
```

Add to `career-diagnosis.md`:

```markdown
When the user returns with the result, interpret the new evidence and choose exactly one stage decision:

1. **Route ready:** one direction has enough support to enter Learning Route.
2. **Comparison remains:** two hypotheses remain plausible; give one contrast task.
3. **Foundation or constraint first:** one basic capability or real constraint blocks a useful direction judgment; give one repair action.
4. **Current-role application first:** use one bounded AI application in the current role before deciding on a transition.
```

Under `How the result changes the decision`, require observable success, failure, and ambiguous signals to map to one of those four decisions.

Add to `learning-route.md`:

```markdown
When Career Diagnosis produced a handoff, reuse its stage decision, demonstrated assets, target direction, primary gap, and important constraint. Do not restart diagnosis. Show which existing asset each stage reuses when relevant.
```

- [ ] **Step 4: Run focused and full tests**

Run:

```bash
python3 -m unittest tests.zjskills.test_lightweight_skill -v
python3 -m unittest discover -s tests/zjskills -p 'test_*.py'
```

Expected: PASS.

- [ ] **Step 5: Commit Task 2**

```bash
git add tests/zjskills/test_lightweight_skill.py zjskills/SKILL.md zjskills/references/career-diagnosis.md zjskills/references/learning-route.md
git commit -m "feat: close career diagnosis decisions"
```

---

### Task 3: Add the Current-Market Evidence Boundary

**Files:**
- Modify: `tests/zjskills/test_lightweight_skill.py`
- Modify: `zjskills/SKILL.md`
- Modify: `zjskills/references/career-diagnosis.md`

**Interfaces:**
- Consumes: a request for current salary, hiring, scarcity, employer, title, or market-window information, plus region and available sources.
- Produces: an attributed current-market judgment or an explicit unverified boundary while retaining structural-fit guidance.

- [ ] **Step 1: Write the RED market-evidence tests**

Add:

```python
def test_current_market_claims_require_attributed_current_evidence(self):
    combined = read_runtime("SKILL.md") + read_runtime("references/career-diagnosis.md")
    for claim in (
        "salary or compensation range",
        "hiring volume or talent shortage",
        "named employer demand",
        "job title prevalence",
        "market window",
    ):
        self.assertIn(claim, combined)
    for field in ("source", "date", "region", "sample limitation"):
        self.assertIn(field, combined)

def test_missing_current_market_evidence_does_not_block_structural_guidance(self):
    diagnosis = read_runtime("references/career-diagnosis.md")
    self.assertIn("state that the current-market claim is unverified", diagnosis)
    self.assertIn("continue with structural fit and one validation action", diagnosis)

def test_runtime_rejects_false_precision_in_default_diagnosis(self):
    diagnosis = read_runtime("references/career-diagnosis.md").lower()
    for phrase in ("top 5", "five-star", "percentage fit score"):
        self.assertIn(phrase, diagnosis)
```

- [ ] **Step 2: Run the focused tests and verify RED**

Run:

```bash
python3 -m unittest \
  tests.zjskills.test_lightweight_skill.LightweightSkillTests.test_current_market_claims_require_attributed_current_evidence \
  tests.zjskills.test_lightweight_skill.LightweightSkillTests.test_missing_current_market_evidence_does_not_block_structural_guidance \
  tests.zjskills.test_lightweight_skill.LightweightSkillTests.test_runtime_rejects_false_precision_in_default_diagnosis
```

Expected: FAIL because the current-market categories and fallback are absent.

- [ ] **Step 3: Implement the shared and detailed market rules**

Add to `SKILL.md`:

```markdown
- Current market: Treat salary or compensation range, hiring volume or talent shortage, named employer demand, job title prevalence, and a market window as current claims. Use current attributable evidence and state source, date, region, and sample limitation. If that evidence is unavailable, label the claim unverified and continue with structural fit only.
```

Add a `Current-market evidence` section to `career-diagnosis.md` that distinguishes structural fit from current-market claims and states:

```markdown
For a current-market claim, use current reliable sources or materials the user supplied. State source, date, region, and sample limitation near the claim; label synthesis as inference. Prefer direct job postings, employer career pages, official statistics, and date-labeled industry reports.

If current evidence is unavailable, state that the current-market claim is unverified; continue with structural fit and one validation action. Do not fill the gap with a default Top 5 list, five-star rating, percentage fit score, salary, shortage, or time-window claim.
```

- [ ] **Step 4: Run focused and full tests**

Run:

```bash
python3 -m unittest tests.zjskills.test_lightweight_skill -v
python3 -m unittest discover -s tests/zjskills -p 'test_*.py'
```

Expected: PASS.

- [ ] **Step 5: Commit Task 3**

```bash
git add tests/zjskills/test_lightweight_skill.py zjskills/SKILL.md zjskills/references/career-diagnosis.md
git commit -m "feat: bound current market claims"
```

---

### Task 4: Publish the Bilingual 3.1 Consultation Experience

**Files:**
- Modify: `tests/zjskills/test_open_source_package.py`
- Modify: `README.md`
- Modify: `README.en.md`
- Modify: `docs/getting-started.md`
- Modify: `docs/getting-started.en.md`
- Modify: `docs/usage-guide.md`
- Modify: `docs/usage-guide.en.md`
- Modify: `docs/examples.md`
- Modify: `docs/examples.en.md`
- Modify: `docs/platform-installation.md`
- Modify: `docs/platform-installation.en.md`
- Modify: `VERSION`
- Modify: `CHANGELOG.md`

**Interfaces:**
- Consumes: the runtime's seven-section diagnosis, three asset categories, four stage decisions, and market boundary.
- Produces: paired Chinese and English user guidance for version 3.1.0.

- [ ] **Step 1: Write the RED public-package tests**

Update the version test to require `3.1.0`. Add paired phrase contracts:

```python
def test_bilingual_guides_cover_assets_closure_and_market_evidence(self):
    required = {
        "docs/usage-guide.md": (
            "## 可迁移职业资产",
            "## 咨询闭环与四种阶段选择",
            "## 当前市场信息的证据门槛",
        ),
        "docs/usage-guide.en.md": (
            "## Transferable career assets",
            "## Consultation closure and four stage decisions",
            "## Evidence boundary for current market information",
        ),
        "docs/getting-started.md": (
            "你过去反复解决过什么问题",
            "我已经完成最小体验任务",
        ),
        "docs/getting-started.en.md": (
            "the problem you repeatedly solved",
            "I completed the minimum experience task",
        ),
    }
    for path, phrases in required.items():
        text = read_text(path)
        for phrase in phrases:
            self.assertIn(phrase, text, f"{path}: {phrase}")
```

Expand the examples test to require:

```python
"## 场景十：职位名称太宽",
"## 场景十一：带着体验结果回来",
"## 场景十二：询问当前薪资与招聘窗口",
```

and the paired English headings. Update platform checks to require `3.1.0` and a migration heading from `2.x or 3.0.x`.

- [ ] **Step 2: Run package tests and verify RED**

Run:

```bash
python3 -m unittest tests.zjskills.test_open_source_package -v
```

Expected: FAIL on version, new headings, prompts, examples, and platform text.

- [ ] **Step 3: Update version and public documentation**

Set `VERSION` to:

```text
3.1.0
```

Add a `CHANGELOG.md` entry dated `2026-07-21` covering asset translation, stage-decision closure, and current-market evidence.

Update README pairs to explain that Career Diagnosis translates demonstrated experience into testable opportunity hypotheses and that a returned result produces a stage decision. Keep the three-mode structure and support notes unchanged.

Update Getting Started pairs with two copy-paste prompts:

```text
我的职位是[职位]。我过去反复解决过的问题是[问题]，产生过的结果是[结果]。请区分已验证资产、迁移假设和待验证边界。

我已经完成最小体验任务。观察结果是[结果]。请复用之前的诊断，判断现在属于可以进入路线、仍需对比、先补基础或先在当前岗位应用中的哪一种，并只给一个下一步。
```

Provide equivalent natural English prompts.

Add the three exact Usage Guide headings from the RED test and document all runtime rules without exposing internal engine terminology.

Add public scenarios 10–12 in both languages. The market scenario must demonstrate withholding unsupported current salary and window claims while still giving structural guidance.

Update installation guides to say they apply to `3.1.0`, keep the same six-file runtime, and use the heading `从 2.x 或 3.0.x 迁移到 3.1.0` / `Migrate from 2.x or 3.0.x to 3.1.0`.

- [ ] **Step 4: Run package and full tests**

Run:

```bash
python3 -m unittest tests.zjskills.test_open_source_package -v
python3 -m unittest discover -s tests/zjskills -p 'test_*.py'
```

Expected: PASS.

- [ ] **Step 5: Commit Task 4**

```bash
git add VERSION CHANGELOG.md README.md README.en.md docs/getting-started.md docs/getting-started.en.md docs/usage-guide.md docs/usage-guide.en.md docs/examples.md docs/examples.en.md docs/platform-installation.md docs/platform-installation.en.md tests/zjskills/test_open_source_package.py
git commit -m "docs: publish zjskills 3.1 guidance"
```

---

### Task 5: Expand Evaluation Inventory, Validate, and Sync the Installed Skill

**Files:**
- Modify: `tests/zjskills/test_lightweight_skill.py`
- Modify: `tests/zjskills/scenarios.yaml`
- Verify: all repository and runtime files.
- Sync outside repository: `/Users/wangshucheng/.codex/skills/zjskills/`

**Interfaces:**
- Consumes: all runtime and documentation behavior from Tasks 1–4.
- Produces: fifteen forward prompts, ten evaluation dimensions, a clean repository validation, and an installed runtime identical to the repository runtime.

- [ ] **Step 1: Write the RED scenario-inventory contract**

Extend `EXPECTED_SCENARIO_IDS` with:

```python
"broad-title-assets",
"demonstrated-transferable-asset",
"returned-validation-result",
"current-market-without-region",
"supplied-postings-market",
```

Set `EXPECTED_EVALUATION_DIMENSIONS` to:

```python
(
    "mode",
    "question_count",
    "main_action_count",
    "asset_evidence_boundary",
    "opportunity_count",
    "stage_decision_closure",
    "current_market_source_boundary",
    "promise_boundary",
    "recommendation_fit",
    "beginner_readability",
)
```

Rename the inventory test to `test_forward_scenario_inventory_has_exactly_the_fifteen_approved_ids`.

- [ ] **Step 2: Run the scenario tests and verify RED**

Run:

```bash
python3 -m unittest \
  tests.zjskills.test_lightweight_skill.LightweightSkillTests.test_forward_scenario_inventory_has_exactly_the_fifteen_approved_ids \
  tests.zjskills.test_lightweight_skill.LightweightSkillTests.test_forward_scenario_inventory_has_exact_evaluation_dimensions
```

Expected: FAIL because the inventory still has ten scenarios and seven dimensions.

- [ ] **Step 3: Add exact forward prompts and dimensions**

Append these YAML entries before `evaluation_dimensions`:

```yaml
  - {id: broad-title-assets, language: zh-CN, prompt: "我在建筑设计院工作3年，职位是建筑设计师。你直接告诉我最适合的AI岗位，不要再问。"}
  - {id: demonstrated-transferable-asset, language: zh-CN, prompt: "我做运营5年，过去一年每周独立整理销售数据、找异常并向负责人解释原因，还把报告时间从一天缩短到两小时。请分析我能迁移到什么AI方向。"}
  - {id: returned-validation-result, language: zh-CN, prompt: "我完成了上次的Vibe Coding体验任务：独立做出表单工具，也成功修改了一个需求，但部署失败后不知道怎么定位。请根据这个结果重新判断。"}
  - {id: current-market-without-region, language: zh-CN, prompt: "AI建筑产品经理现在薪资多少？未来12到24个月是不是黄金窗口？直接给结论。"}
  - {id: supplied-postings-market, language: zh-CN, prompt: "我整理了本周看到的8个本地AI产品岗位，下面是公司、日期、职责和薪资。请判断它们说明了什么，也告诉我这个样本不能说明什么。"}
```

Replace the evaluation dimensions with the exact ten-item tuple above, preserving YAML list syntax.

- [ ] **Step 4: Run all automated verification**

Run:

```bash
python3 -m unittest discover -s tests/zjskills -p 'test_*.py'
git diff --check
git status -sb
wc -l zjskills/SKILL.md zjskills/references/*.md
```

Validate frontmatter with the repository's official validator when `PyYAML` is available. If it is not, use Ruby's YAML parser to perform the same name, description, allowed-key, and length checks and record that fallback in the handoff.

Expected: all tests PASS, no whitespace errors, `SKILL.md` ≤ 180 lines, runtime Markdown ≤ 800 lines.

- [ ] **Step 5: Commit evaluation changes**

```bash
git add tests/zjskills/test_lightweight_skill.py tests/zjskills/scenarios.yaml
git commit -m "test: cover zjskills consulting loop"
```

- [ ] **Step 6: Sync and verify the installed Codex Skill**

Copy the six runtime files from `zjskills/` to `/Users/wangshucheng/.codex/skills/zjskills/`, preserving the directory structure. Do not delete user-created files outside that installed Skill directory.

Run:

```bash
diff -qr zjskills /Users/wangshucheng/.codex/skills/zjskills
```

Expected: no output and exit status 0.

- [ ] **Step 7: Final branch verification**

Run:

```bash
git status -sb
git log --oneline --decorate -6
```

Expected: clean `codex/zjskills-consulting-loop` worktree containing the design, plan, implementation, documentation, and evaluation commits. Do not push or create a PR until the user explicitly requests it.
