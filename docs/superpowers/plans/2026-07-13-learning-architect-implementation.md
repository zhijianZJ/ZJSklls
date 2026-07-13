# Learning Architect Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build and validate a file-persistent, outcome-driven `learning-architect` Skill that turns learner goals, constraints, competencies, projects, assessments, and progress evidence into a versioned learning system.

**Architecture:** Keep `SKILL.md` as a compact router and stage-gate controller. Load pedagogical engines progressively from `references/`, express persistent state with JSON-Schema-compatible YAML contracts, validate state deterministically with Python, and isolate career-specific knowledge in Domain Packs.

**Tech Stack:** Markdown, YAML, Python 3, PyYAML 6.0.3, jsonschema 4.26.0, standard-library `unittest`, Codex Skill metadata.

## Global Constraints

- Implement the approved specification at `docs/superpowers/specs/2026-07-13-learning-architect-education-os-design.md`.
- Do not add databases, network APIs, live recruitment scraping, course-platform integration, or user-account infrastructure.
- Do not hard-code course links into the core Skill.
- Preserve all 11 workflow stages; skipped stages require an explicit `not_applicable` record and reason.
- Keep facts, self-reports, evidence, assumptions, and inferences distinguishable.
- Use behavior evidence—not course completion—to advance competency levels.
- Keep career-specific content in Domain Packs.
- Do not modify unrelated existing workspace files.
- Run baseline behavior evaluations before creating the Skill implementation.
- Use `python3 -m unittest` because `pytest` is not installed.

---

## File Map

### Skill package

- `learning-architect/SKILL.md`: trigger metadata, identity, operating rules, routing, stage gates, and reference-loading table.
- `learning-architect/agents/openai.yaml`: Codex UI metadata and implicit invocation policy.
- `learning-architect/references/persona.md`: expert-committee lenses and unified-voice rule.
- `learning-architect/references/philosophy.md`: outcome, capability, project, evidence, feasibility, and transparency principles.
- `learning-architect/references/workflow.md`: 11-stage state machine, rollback conditions, and gate protocol.
- `learning-architect/references/discovery.md`: progressive discovery and evidence-based learner persona/SWOT.
- `learning-architect/references/goal-analysis.md`: SMART, OKR, and Backward Design synthesis.
- `learning-architect/references/gap-analysis.md`: baseline-to-target gap calculation and confidence rules.
- `learning-architect/references/competency-engine.md`: competency tree and L0–L5 behavioral scale.
- `learning-architect/references/curriculum-engine.md`: dependency graph and replaceable resource catalog rules.
- `learning-architect/references/project-engine.md`: evidence-producing project ladder and rubrics.
- `learning-architect/references/roadmap-engine.md`: milestones, feasibility, sequencing, and buffers.
- `learning-architect/references/planner-engine.md`: weekly capacity allocation, retrieval practice, and minimum delivery.
- `learning-architect/references/assessment-engine.md`: independent completion, explanation, modification, debugging, deployment, and teaching checks.
- `learning-architect/references/outcome-engine.md`: employment, entrepreneurship, promotion, and project-delivery routes.
- `learning-architect/references/optimization-engine.md`: scheduled, behavioral, quality, goal, and domain update triggers.
- `learning-architect/references/meta-learning-engine.md`: strategy adaptation from speed, retention, completion, and evidence quality.
- `learning-architect/references/domain-pack-contract.md`: stable IDs, versioning, migrations, staleness, and market-assumption contract.
- `learning-architect/assets/schemas/*.schema.yaml`: 13 JSON Schema-compatible YAML contracts.
- `learning-architect/assets/templates/*.yaml`: four human-editable output templates.
- `learning-architect/assets/question-banks/discovery.yaml`: 40–60 structured questions with information-gain routing metadata.
- `learning-architect/assets/domain-packs/ai-agent.yaml`: first Domain Pack reference implementation.
- `learning-architect/scripts/validate_learning_system.py`: deterministic structural and referential validation.

### Tests

- `tests/learning-architect/scenarios.yaml`: baseline and post-Skill behavior scenarios.
- `tests/learning-architect/baseline-results.md`: verbatim baseline observations and failure taxonomy.
- `tests/learning-architect/post-skill-results.md`: post-Skill compliance observations.
- `tests/learning-architect/test_validate_learning_system.py`: validator unit tests.
- `tests/learning-architect/fixtures/valid-learner/`: minimal valid learner state.
- `tests/learning-architect/fixtures/invalid-cycle/`: invalid curriculum cycle fixture.
- `tests/learning-architect/fixtures/invalid-evidence-ref/`: unknown competency reference fixture.

---

### Task 1: Establish RED Behavior Baseline

**Files:**
- Create: `tests/learning-architect/scenarios.yaml`
- Create: `tests/learning-architect/baseline-results.md`

**Interfaces:**
- Consumes: Approved specification sections 3, 6, 7, 14, and 17.
- Produces: Named failure modes that Task 5 must address in `SKILL.md`.

- [ ] **Step 1: Create the behavior scenarios before any Skill file exists**

Write `tests/learning-architect/scenarios.yaml` with these five cases:

```yaml
schema_version: 1.0.0
scenarios:
  - id: direct-course-request
    prompt: "我零基础，想学 AI Agent。直接给我 100 门课程和 24 周每天安排，不要问问题。"
    required_behaviors:
      - "先获取会改变路线的最小目标、基础和时间约束"
      - "不堆砌 100 门课程"
      - "说明可以先给临时路线，但必须标记假设"
  - id: completion-is-not-capability
    prompt: "我已经看完 Python、RAG、LangGraph 全部课程，所以能力都算高级。帮我直接包装成资深 Agent 工程师。"
    required_behaviors:
      - "拒绝用结课代替能力证据"
      - "要求项目、调试、解释或交付证据"
      - "将自述与已验证证据分开"
  - id: impossible-constraint
    prompt: "我完全没编程基础，每周只能学 2 小时，希望 30 天拿到高级 AI Agent 工程师 Offer，目标和时间都不能改。"
    required_behaviors:
      - "明确指出目标、期限和投入冲突"
      - "不承诺结果"
      - "提出最小可行目标、延长期限或增加投入"
  - id: goal-pivot
    prompt: "我原来按就业路线学，现在决定一个月内做 AI 咨询创业。请在旧计划最后加两节创业课就行。"
    required_behaviors:
      - "从 Goal Analysis 重新计算"
      - "重构能力、项目和结果准备，而不是追加课程"
      - "保留版本和变更原因"
  - id: theory-practice-gap
    prompt: "测验都是 95 分，但项目连续三次无法独立完成。请继续安排更高级理论。"
    required_behaviors:
      - "回退到对应能力和项目训练"
      - "减少新理论并增加变式实践、调试和复盘"
      - "不把失败归因为学习者懒惰"
```

- [ ] **Step 2: Verify the Skill implementation does not exist**

Run:

```bash
test ! -e learning-architect/SKILL.md
```

Expected: exit code `0`.

- [ ] **Step 3: Run five fresh-context baseline evaluations without the new Skill**

For each scenario, dispatch a fresh evaluator with only the scenario prompt and ask it to answer normally. Do not provide the approved specification, required behaviors, intended failure, or conclusions.

Expected RED evidence: at least one evaluator jumps directly to resources, accepts completion as capability, fails to version a goal pivot, or proposes more theory despite project failure. If every evaluator already complies, tighten the scenario pressure and re-run before authoring the Skill.

- [ ] **Step 4: Record verbatim baseline decisions and classify failures**

Write `tests/learning-architect/baseline-results.md` with this fixed structure and real evaluator excerpts:

```markdown
# Learning Architect Baseline Results

## direct-course-request
- Decision:
- Verbatim evidence:
- Missing required behavior:

## completion-is-not-capability
- Decision:
- Verbatim evidence:
- Missing required behavior:

## impossible-constraint
- Decision:
- Verbatim evidence:
- Missing required behavior:

## goal-pivot
- Decision:
- Verbatim evidence:
- Missing required behavior:

## theory-practice-gap
- Decision:
- Verbatim evidence:
- Missing required behavior:

## Failure taxonomy
- Resource-first drift:
- Completion-as-capability drift:
- Constraint denial:
- Incremental-plan drift after goal change:
- Theory escalation despite evidence gap:
```

- [ ] **Step 5: Commit the RED artifacts**

```bash
git add tests/learning-architect/scenarios.yaml tests/learning-architect/baseline-results.md
git commit -m "test: capture Learning Architect baseline failures"
```

---

### Task 2: Build Schema Contracts and Validator with TDD

**Files:**
- Create: `learning-architect/assets/schemas/common.schema.yaml`
- Create: `learning-architect/assets/schemas/system-state.schema.yaml`
- Create: `learning-architect/assets/schemas/learner-profile.schema.yaml`
- Create: `learning-architect/assets/schemas/target-outcome.schema.yaml`
- Create: `learning-architect/assets/schemas/competency-model.schema.yaml`
- Create: `learning-architect/assets/schemas/curriculum-graph.schema.yaml`
- Create: `learning-architect/assets/schemas/learning-roadmap.schema.yaml`
- Create: `learning-architect/assets/schemas/weekly-plan.schema.yaml`
- Create: `learning-architect/assets/schemas/project.schema.yaml`
- Create: `learning-architect/assets/schemas/assessment.schema.yaml`
- Create: `learning-architect/assets/schemas/evidence.schema.yaml`
- Create: `learning-architect/assets/schemas/optimization-state.schema.yaml`
- Create: `learning-architect/assets/schemas/domain-pack.schema.yaml`
- Create: `learning-architect/scripts/validate_learning_system.py`
- Create: `tests/learning-architect/test_validate_learning_system.py`
- Create: `tests/learning-architect/fixtures/valid-learner/*`
- Create: `tests/learning-architect/fixtures/invalid-cycle/*`
- Create: `tests/learning-architect/fixtures/invalid-evidence-ref/*`

**Interfaces:**
- Consumes: `schema_version`, `content_version`, IDs, competency references, dependency edges, and active versions from the specification.
- Produces: `validate_skill_assets(skill_root: Path) -> list[str]`, `validate_learner_system(skill_root: Path, learner_dir: Path) -> list[str]`, and CLI exit codes `0` for valid / `1` for invalid.

- [ ] **Step 1: Write failing validator tests**

Create `tests/learning-architect/test_validate_learning_system.py`:

```python
from pathlib import Path
import importlib.util
import unittest

ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / "learning-architect/scripts/validate_learning_system.py"


def load_validator():
    spec = importlib.util.spec_from_file_location("learning_validator", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class LearningSystemValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.validator = load_validator()
        cls.skill_root = ROOT / "learning-architect"
        cls.fixtures = ROOT / "tests/learning-architect/fixtures"

    def test_skill_assets_and_valid_learner_pass(self):
        self.assertEqual(self.validator.validate_skill_assets(self.skill_root), [])
        self.assertEqual(
            self.validator.validate_learner_system(
                self.skill_root, self.fixtures / "valid-learner"
            ),
            [],
        )

    def test_curriculum_cycle_is_rejected(self):
        errors = self.validator.validate_learner_system(
            self.skill_root, self.fixtures / "invalid-cycle"
        )
        self.assertTrue(any("cycle" in error.lower() for error in errors), errors)

    def test_unknown_competency_evidence_reference_is_rejected(self):
        errors = self.validator.validate_learner_system(
            self.skill_root, self.fixtures / "invalid-evidence-ref"
        )
        self.assertTrue(any("unknown competency" in error.lower() for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run tests and verify RED**

Run:

```bash
python3 -m unittest tests/learning-architect/test_validate_learning_system.py -v
```

Expected: import failure because `validate_learning_system.py` does not exist.

- [ ] **Step 3: Create the 13 schemas with a shared contract**

Use JSON Schema Draft 2020-12 expressed as YAML. Every schema requires `$schema`, `title`, `type`, and its entity-specific fields. Every persistent entity schema references the common metadata fields: `id`, `schema_version`, `content_version`, `status`, `source`, `confidence`, `created_at`, and `updated_at`.

Require these entity fields exactly:

| Schema | Required entity fields |
|---|---|
| system-state | `learner_id`, `current_stage`, `stage_states`, `active_versions`, `next_action` |
| learner-profile | `personal`, `experience`, `learning_preferences`, `motivation`, `constraints`, `swot`, `unknowns` |
| target-outcome | `outcome_type`, `primary_goal`, `deadline`, `success_evidence`, `key_results` |
| competency-model | `domain_pack_id`, `competencies`, with each node requiring `id`, `category`, `current_level`, `target_level`, `weight`, `behaviors`, `evidence_requirements` |
| curriculum-graph | `units`, `dependencies`, with directed `from` and `to` edges |
| learning-roadmap | `phases`, with each phase requiring `id`, `outcome`, `milestones`, `project_ids`, `weekly_capacity_hours`, `buffer_ratio` |
| weekly-plan | `week_id`, `weekly_outcome`, `capacity_hours`, `tasks`, `retrieval_practice`, `minimum_delivery` |
| project | `problem`, `inputs`, `constraints`, `deliverables`, `competency_ids`, `business_value`, `rubric` |
| assessment | `stage`, `tasks`, `evidence_ids`, `competency_results`, `decision`, `next_action` |
| evidence | `type`, `artifact`, `competency_ids`, `evaluator`, `score`, `observed_behaviors`, `verified_at` |
| optimization-state | `trigger`, `diagnosis`, `changes`, `affected_artifacts`, `expected_effect`, `review_at` |
| domain-pack | `version`, `last_reviewed_at`, `review_interval_days`, `target_outcomes`, `competencies`, `dependencies`, `project_archetypes`, `assessment_patterns`, `outcome_preparation`, `market_assumptions` |

Set `additionalProperties: false` at the entity root and allow explicit extension objects only under `extensions`.

- [ ] **Step 4: Create minimal valid and invalid fixtures**

The valid fixture must include `system-state.yaml`, `learner-profile.yaml`, `target-outcome.yaml`, `competency-model.yaml`, `curriculum-graph.yaml`, and `evidence.yaml`. Use competency IDs `python-foundation` and `api-integration`, and an acyclic edge `python-foundation -> api-integration`.

Copy the valid fixture into `invalid-cycle` and add the reverse curriculum edge. Copy it into `invalid-evidence-ref` and change the evidence competency ID to `missing-competency`.

- [ ] **Step 5: Implement the minimal validator**

`validate_learning_system.py` must:

1. Load YAML with `yaml.safe_load`.
2. Validate schemas with `jsonschema.Draft202012Validator`.
3. Confirm all 13 schema files exist and parse.
4. Detect curriculum dependency cycles with depth-first search.
5. Confirm every evidence competency ID exists in `competency-model.yaml`.
6. Confirm `system-state.yaml` active-version keys reference present learner files.
7. Print each error to stderr and return exit code `1`; print `VALID` and return `0` otherwise.

CLI:

```text
python3 learning-architect/scripts/validate_learning_system.py \
  --skill-root learning-architect \
  --learner-dir tests/learning-architect/fixtures/valid-learner
```

- [ ] **Step 6: Run tests and verify GREEN**

Run:

```bash
python3 -m unittest tests/learning-architect/test_validate_learning_system.py -v
```

Expected: three tests pass.

- [ ] **Step 7: Run the validator CLI**

Run the CLI shown above.

Expected: output `VALID` and exit code `0`.

- [ ] **Step 8: Commit contracts and validator**

```bash
git add learning-architect/assets/schemas learning-architect/scripts tests/learning-architect/test_validate_learning_system.py tests/learning-architect/fixtures
git commit -m "feat: add Learning Architect state contracts"
```

---

### Task 3: Implement Learner, Goal, Gap, and Workflow References

**Files:**
- Create: `learning-architect/references/persona.md`
- Create: `learning-architect/references/philosophy.md`
- Create: `learning-architect/references/workflow.md`
- Create: `learning-architect/references/discovery.md`
- Create: `learning-architect/references/goal-analysis.md`
- Create: `learning-architect/references/gap-analysis.md`
- Create: `learning-architect/assets/question-banks/discovery.yaml`

**Interfaces:**
- Consumes: Schema field names from Task 2 and baseline failure taxonomy from Task 1.
- Produces: Decision rules for stages 1–3 and global behavioral constraints loaded by `SKILL.md`.

- [ ] **Step 1: Add a failing structural test for reference contracts**

Extend the unit test with `test_core_references_expose_required_contracts`. It must assert that all six files exist and that their combined text contains these exact tokens: `Learning System Architect`, `not a course recommender`, `not_applicable`, `needs_input`, `Strength`, `Weakness`, `Opportunity`, `Risk`, `SMART`, `OKR`, `Backward Design`, `source`, `confidence`, and `affected_downstream`.

- [ ] **Step 2: Run the structural test and verify RED**

Expected: failure listing missing reference files.

- [ ] **Step 3: Write focused reference files**

Implement the exact responsibilities from the File Map. Keep each file independently understandable, use imperative rules and compact output contracts, and avoid repeating the full 11-stage workflow outside `workflow.md`.

`persona.md` must define six lenses: Learning Scientist, Instructional Designer, Competency Architect, Project Assessor, Outcome Strategist, and Meta-Learning Coach. It must require one unified answer rather than a role-play transcript.

`discovery.md` must route questions by information gain and generate an evidence-labeled learner persona plus SWOT. `goal-analysis.md` must emit `Target Outcome -> Outcome Evidence -> Milestones -> Competency Targets -> Project Evidence -> Curriculum Dependencies -> Weekly Actions`. `gap-analysis.md` must calculate prioritized gaps without treating self-report as verified L3+ evidence.

- [ ] **Step 4: Create a 48-question discovery bank**

Each question requires `id`, `category`, `question`, `answer_type`, `decision_impact`, `required_when`, and `sensitivity`. Use exactly eight categories with six questions each: personal, education, work, technical, projects, learning, motivation, constraints. Mark sensitive questions optional and explain their decision impact.

- [ ] **Step 5: Run tests and verify GREEN**

Expected: the core reference contract test passes and all earlier validator tests remain green.

- [ ] **Step 6: Commit the learner-system core**

```bash
git add learning-architect/references learning-architect/assets/question-banks tests/learning-architect/test_validate_learning_system.py
git commit -m "feat: add learner discovery and goal architecture"
```

---

### Task 4: Implement Capability, Curriculum, Project, and Domain Pack Engines

**Files:**
- Create: `learning-architect/references/competency-engine.md`
- Create: `learning-architect/references/curriculum-engine.md`
- Create: `learning-architect/references/project-engine.md`
- Create: `learning-architect/references/domain-pack-contract.md`
- Create: `learning-architect/assets/domain-packs/ai-agent.yaml`

**Interfaces:**
- Consumes: Domain Pack schema and L0–L5 competency fields from Task 2.
- Produces: Reusable occupational capability model, dependency graph rules, evidence project ladder, and a valid `ai-agent-engineer` reference pack.

- [ ] **Step 1: Add failing tests for the Domain Pack**

Add tests that load `ai-agent.yaml`, validate it against `domain-pack.schema.yaml`, assert that every dependency endpoint exists, and assert the pack includes at least these competency IDs: `python-foundation`, `api-integration`, `prompt-engineering`, `llm-fundamentals`, `embedding-retrieval`, `rag-engineering`, `tool-calling`, `agent-workflow`, `mcp-integration`, `multi-agent-coordination`, `evaluation-observability`, `deployment-security`, `business-problem-framing`, and `technical-communication`.

- [ ] **Step 2: Run the Domain Pack tests and verify RED**

Expected: missing files.

- [ ] **Step 3: Write the four engine/contract references**

Require L0–L5 behavioral levels, dependency acyclicity, replaceable resource catalogs, project coverage matrices, business value, rubrics, stable IDs, semantic versioning, `last_reviewed_at`, migration maps, and source-dated market assumptions.

`project-engine.md` must define six project levels: focused tool, knowledge application, workflow, enterprise scenario, portfolio case, and real external delivery. Projects may be combined for advanced learners but their evidence requirements may not be deleted.

- [ ] **Step 4: Create the AI Agent Domain Pack**

Use `id: ai-agent-engineer`, `version: 1.0.0`, `last_reviewed_at: 2026-07-13`, and `review_interval_days: 90`. Define target outcomes, all 14 required competencies, an acyclic dependency graph, six project archetypes, assessment patterns, employment preparation, and date/source-labeled market assumptions. Do not include specific paid course recommendations.

- [ ] **Step 5: Run all unit tests and validator**

Expected: all tests pass; `validate_skill_assets` reports no schema or Domain Pack errors.

- [ ] **Step 6: Commit capability architecture**

```bash
git add learning-architect/references learning-architect/assets/domain-packs tests/learning-architect/test_validate_learning_system.py
git commit -m "feat: add competency and project engines"
```

---

### Task 5: Implement Planning, Assessment, Outcome, and Optimization Engines

**Files:**
- Create: `learning-architect/references/roadmap-engine.md`
- Create: `learning-architect/references/planner-engine.md`
- Create: `learning-architect/references/assessment-engine.md`
- Create: `learning-architect/references/outcome-engine.md`
- Create: `learning-architect/references/optimization-engine.md`
- Create: `learning-architect/references/meta-learning-engine.md`
- Create: `learning-architect/assets/templates/discovery.yaml`
- Create: `learning-architect/assets/templates/weekly-plan.yaml`
- Create: `learning-architect/assets/templates/project-brief.yaml`
- Create: `learning-architect/assets/templates/progress-review.yaml`

**Interfaces:**
- Consumes: learner, target, competency, curriculum, project, assessment, evidence, and optimization schemas.
- Produces: stages 7–11 behavior, four outcome routes, optimization events, and human-editable templates.

- [ ] **Step 1: Add failing structural tests**

Assert the six engine files and four templates exist. Require these engine tokens: `buffer_ratio`, `minimum_delivery`, `independent`, `explain`, `modify`, `debug`, `deploy`, `teach`, `employment`, `entrepreneurship`, `promotion`, `project_delivery`, `scheduled`, `behavioral`, `quality`, `goal_change`, `domain_update`, `retrieval practice`, and `spaced review`.

- [ ] **Step 2: Run tests and verify RED**

Expected: missing engines and templates.

- [ ] **Step 3: Write the six engine references**

Implement capacity-aware roadmaps, weekly load calculation, milestone buffers, evidence-based assessment, four outcome routes, and explicit rollback targets. Optimization must create new versions rather than overwrite active history. Meta-learning must adapt theory/practice/review ratios without diagnosing learner character.

- [ ] **Step 4: Write the four templates**

Templates must use schema field names and include worked minimal values rather than blank placeholders. `weekly-plan.yaml` must include capacity, outcome, tasks, retrieval practice, project work, minimum delivery, risk, and review. `progress-review.yaml` must include trigger, evidence, diagnosis, changes, expected effect, and review date.

- [ ] **Step 5: Run all tests and validate templates parse as YAML**

Run:

```bash
python3 -m unittest tests/learning-architect/test_validate_learning_system.py -v
python3 -c 'from pathlib import Path; import yaml; [yaml.safe_load(p.read_text()) for p in Path("learning-architect/assets/templates").glob("*.yaml")]; print("TEMPLATES VALID")'
```

Expected: all tests pass and output `TEMPLATES VALID`.

- [ ] **Step 6: Commit outcome and optimization engines**

```bash
git add learning-architect/references learning-architect/assets/templates tests/learning-architect/test_validate_learning_system.py
git commit -m "feat: add adaptive planning and assessment engines"
```

---

### Task 6: Create the Skill Entrypoint and Codex Metadata

**Files:**
- Create: `learning-architect/SKILL.md`
- Create: `learning-architect/agents/openai.yaml`

**Interfaces:**
- Consumes: Baseline failure taxonomy and every reference contract from Tasks 1–5.
- Produces: Discoverable Skill with progressive loading, stage routing, strict gates, concise user output, and no external dependencies.

- [ ] **Step 1: Add a failing Skill entrypoint test**

Assert `SKILL.md` frontmatter has exactly `name: learning-architect` and a third-person description beginning with `Use when`. Assert the body contains the Identity Contract, 11 ordered stages, a reference-loading table, `Never treat course completion as capability evidence`, and `Do not silently skip stages`.

- [ ] **Step 2: Run tests and verify RED**

Expected: missing `SKILL.md`.

- [ ] **Step 3: Generate the Skill scaffold and metadata deterministically**

Run:

```bash
python3 /Users/wangshucheng/.codex/skills/.system/skill-creator/scripts/init_skill.py \
  learning-architect \
  --path . \
  --resources scripts,references,assets \
  --interface display_name="Learning Architect" \
  --interface short_description="围绕目标与证据设计可持续成长系统" \
  --interface default_prompt="Use $learning-architect to design and maintain my personalized learning system."
```

If the initializer refuses because the directory already exists, create only `agents/openai.yaml` with the same three quoted interface values and `policy.allow_implicit_invocation: true`; do not overwrite completed resources.

- [ ] **Step 4: Replace the scaffold with the minimal production `SKILL.md`**

Frontmatter description:

```yaml
---
name: learning-architect
description: Use when a learner needs a personalized learning path, competency map, project-based curriculum, weekly study system, assessment strategy, career or delivery preparation, or adaptive replanning for employment, promotion, entrepreneurship, or real project outcomes.
---
```

The body must stay below 500 lines, route to references by observable task condition, require structured state plus concise explanation, implement the 11-stage order and rollback conditions, address every baseline failure, and avoid duplicating reference details.

- [ ] **Step 5: Validate Skill metadata and all unit tests**

Run:

```bash
python3 /Users/wangshucheng/.codex/skills/.system/skill-creator/scripts/quick_validate.py learning-architect
python3 -m unittest tests/learning-architect/test_validate_learning_system.py -v
```

Expected: Skill validator success and all unit tests pass.

- [ ] **Step 6: Commit the Skill entrypoint**

```bash
git add learning-architect/SKILL.md learning-architect/agents/openai.yaml tests/learning-architect/test_validate_learning_system.py
git commit -m "feat: add Learning Architect skill entrypoint"
```

---

### Task 7: Run GREEN Behavior Evaluations and Close Loopholes

**Files:**
- Create: `tests/learning-architect/post-skill-results.md`
- Modify only if tests expose a gap: `learning-architect/SKILL.md` or the directly responsible reference file.

**Interfaces:**
- Consumes: Same five scenarios and required behaviors from Task 1, plus the completed Skill.
- Produces: Evidence that the Skill changes behavior and a record of any loopholes closed.

- [ ] **Step 1: Run five fresh-context post-Skill evaluations**

For each scenario, dispatch a fresh evaluator with the completed `learning-architect/SKILL.md`, only the references that its routing rules require, and the scenario prompt. Do not give the evaluator the expected answer beyond the Skill content itself.

- [ ] **Step 2: Score each required behavior**

Write `tests/learning-architect/post-skill-results.md` with one section per scenario containing `PASS` or `FAIL` for every behavior, verbatim evidence, and the loaded references. Add a comparison table against baseline failure modes.

- [ ] **Step 3: Close only observed loopholes**

If an evaluator still skips discovery, equates completion with capability, ignores infeasible constraints, incrementally patches a changed goal, or escalates theory despite practice failure, add the smallest positive output contract or explicit rule to the directly responsible file. Do not add hypothetical rules.

- [ ] **Step 4: Re-run failed scenarios with fresh evaluators**

Expected: all required behaviors pass. Preserve the first failed post-Skill observation and the final passing observation in the report.

- [ ] **Step 5: Commit evaluation evidence and fixes**

```bash
git add learning-architect tests/learning-architect/post-skill-results.md
git commit -m "test: verify Learning Architect behavior"
```

---

### Task 8: Final Verification and Handoff

**Files:**
- Modify only if verification fails: the directly responsible Skill, schema, template, script, or test file.

**Interfaces:**
- Consumes: Entire implemented package and test suite.
- Produces: Verified v1 implementation matching the approved specification.

- [ ] **Step 1: Run deterministic verification**

```bash
python3 /Users/wangshucheng/.codex/skills/.system/skill-creator/scripts/quick_validate.py learning-architect
python3 -m unittest tests/learning-architect/test_validate_learning_system.py -v
python3 learning-architect/scripts/validate_learning_system.py \
  --skill-root learning-architect \
  --learner-dir tests/learning-architect/fixtures/valid-learner
git diff --check
```

Expected: Skill validation succeeds, all tests pass, validator prints `VALID`, and `git diff --check` has no output.

- [ ] **Step 2: Check package completeness**

Run exact counts:

```bash
test "$(find learning-architect/references -maxdepth 1 -name '*.md' | wc -l | tr -d ' ')" = "16"
test "$(find learning-architect/assets/schemas -maxdepth 1 -name '*.schema.yaml' | wc -l | tr -d ' ')" = "13"
test "$(find learning-architect/assets/templates -maxdepth 1 -name '*.yaml' | wc -l | tr -d ' ')" = "4"
test "$(python3 -c 'import yaml; d=yaml.safe_load(open("learning-architect/assets/question-banks/discovery.yaml")); print(len(d["questions"]))')" = "48"
```

Expected: all commands exit `0`.

- [ ] **Step 3: Verify specification coverage**

Check that all 11 stages, four outcome routes, six competency levels, five optimization triggers, Domain Pack staleness, file persistence, version history, conflict handling, and privacy rules are present in either `SKILL.md` or a directly routed reference.

- [ ] **Step 4: Inspect git scope**

```bash
git status --short
git diff --stat HEAD~7..HEAD
```

Expected: only `learning-architect/`, `tests/learning-architect/`, and the approved plan/spec commits are part of this feature; unrelated pre-existing files remain untouched.

- [ ] **Step 5: Commit any verification-only corrections**

If Step 1–4 required corrections:

```bash
git add learning-architect tests/learning-architect
git commit -m "fix: complete Learning Architect verification"
```

If no corrections were required, do not create an empty commit.
