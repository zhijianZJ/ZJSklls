# ZJSkills 2.1 AI Routes and Learning Companion Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Release ZJSkills 2.1.0 with a versioned shared AI foundation, five visible AI learning routes backed by six validated Domain Packs, evidence-based route selection, learning-material synthesis, and a transferable generic learning mode.

**Architecture:** Keep the ZJSkills learning-system core and six-item beginner navigation stable. Add a separately versioned Capability Library layer, let Domain Packs opt into compatible foundation competencies, resolve one effective competency graph during validation, and add typed artifacts for route decisions and learning-material maps. Keep all 智建/group guidance in public documentation only; runtime behavior remains neutral and outcome-driven.

**Tech Stack:** Markdown Skill instructions and documentation, YAML Draft 2020-12 schemas/templates/domain data, Python 3.9+ validator, `unittest`, `PyYAML`, `jsonschema`, `referencing`, Git/GitHub.

## Global Constraints

- Technical Skill identifier and explicit calls remain `zjskills`, `$zjskills`, and `/zjskills`.
- Release version becomes `2.1.0`; work stays on `codex/zjskills-learning-routes` and uses a new pull request rather than modifying PR #5.
- Keep the canonical 11-stage workflow and six-item beginner home navigation unchanged.
- Present five user-visible AI routes; implement AI Operations with two independent technical packs, for six Domain Packs total.
- Existing self-contained Domain Packs and learner workspaces must validate without a `foundation` block.
- Capability evidence, project rubrics, feasibility gates, safety boundaries, stale-source checks, and non-guarantee language remain mandatory.
- Show concise conclusions, evidence, assumptions, alternatives, trade-offs, and next actions; never expose hidden chain-of-thought.
- Runtime files under `zjskills/` must not include 智建 contact, answer-group, community, course-sales, purchase, or conversion routing.
- The approved 智建 answer-group sentence appears only in public usage and installation documentation.
- Use `/Users/wangshucheng/miniconda3/bin/python3` for repository validation because it has the required YAML/schema packages.
- Add no vendor-specific course dependency and no unsupported non-AI professional claim.

---

### Task 1: Lock the 2.1 release contracts with failing tests

**Files:**
- Modify: `tests/zjskills/test_validate_learning_system.py`
- Modify: `tests/zjskills/test_open_source_package.py`

**Interfaces:**
- Requires `ai-foundation.yaml`, six Domain Packs, three new schemas, two new templates, and three new references.
- Requires public version `2.1.0`, five visible route names, bilingual material/generic-mode guidance, and the documentation-only 智建 note.
- Forbids 智建/group/referral/conversion language below `zjskills/`.

- [ ] **Step 1: Add `test_210_release_surface_exists`**

Assert the exact new paths exist. Assert README surfaces contain `2.1.0`, `Vibe Coding`, `AI 产品经理`, `AI 运营`, and `AI 工具`.

- [ ] **Step 2: Add `test_runtime_has_no_human_referral_or_conversion_logic`**

Recursively read text/YAML below `zjskills/` and reject these case-insensitive terms: `智建`, `答疑群`, `社群`, `加微信`, `contact zj`, `answer group`, `paid course`, `购买课程`, `转化用户`, and `人工转介`.

- [ ] **Step 3: Add schema and route inventory tests**

Require registry members `capability-library`, `route-decision`, and `learning-material-map`. Require these pack IDs exactly:

```python
{
    "ai-agent",
    "vibe-coding",
    "ai-product-manager",
    "ai-operations-content-growth",
    "ai-operations-business-efficiency",
    "ai-tools-workplace",
}
```

- [ ] **Step 4: Run tests and verify RED**

```bash
/Users/wangshucheng/miniconda3/bin/python3 -m unittest \
  tests.zjskills.test_validate_learning_system \
  tests.zjskills.test_open_source_package -q
```

Expected: FAIL only on absent 2.1 assets, version text, route inventory, and documentation contracts.

- [ ] **Step 5: Commit the contract tests**

```bash
git add tests/zjskills
git commit -m "test: lock zjskills 2.1 contracts"
```

---

### Task 2: Add the versioned AI Capability Library contract

**Files:**
- Create: `zjskills/assets/schemas/capability-library.schema.yaml`
- Create: `zjskills/assets/capability-libraries/ai-foundation.yaml`
- Modify: `zjskills/scripts/validate_learning_system.py`
- Modify: `tests/zjskills/test_validate_learning_system.py`

**Interfaces:**
- Library identity: `id: ai-foundation`, `schema_version: 1.0.0`, `content_version: 1.0.0`.
- Stable competency IDs: `ai-literacy`, `prompt-context`, `tool-selection-verification`, `data-privacy-safety`, `workflow-automation`, and `project-evidence-value`.
- Each competency supplies L0-L5 observable behavior/evidence; dependencies reference competency IDs; experience tasks reference one or more competency IDs.

- [ ] **Step 1: Add RED schema/semantic tests**

Add `test_capability_library_schema_and_semantics` with one valid library and mutations that fail for duplicate competency ID, missing L3 evidence, nonexistent dependency endpoint, dependency cycle, nonexistent experience-task competency, invalid review date, and stale assumptions.

- [ ] **Step 2: Define the schema**

Use Draft 2020-12 and `common.schema.yaml` references. Require common metadata, source assumptions, migration map, exactly six level records numbered 0-5, nonempty behavior/evidence, and closed contract objects.

- [ ] **Step 3: Register and validate libraries**

Extend `SCHEMA_NAMES` with `capability-library`. Add:

```python
def _load_capability_libraries(
    skill_root: Path,
    schemas: dict[str, dict[str, Any]],
    registry: Registry,
) -> tuple[dict[str, dict[str, Any]], list[str]]:
    """Load, schema-check, semantically validate, and index libraries by ID."""
```

Check duplicate IDs, L0-L5 coverage, dependency endpoints/cycles, experience-task references, migration integrity, and review governance.

- [ ] **Step 4: Create `ai-foundation.yaml`**

Populate all six competencies and three starter experience tasks:

- `compare-ai-output`: compare and verify two AI answers;
- `context-to-result`: improve a task with context and acceptance criteria;
- `workflow-value-test`: map a repeatable task and measure before/after value.

Use dated assumptions and tool categories, not vendor-mandatory instructions.

- [ ] **Step 5: Run and verify GREEN**

```bash
/Users/wangshucheng/miniconda3/bin/python3 -m unittest \
  tests.zjskills.test_validate_learning_system.LearningSystemValidationTests.test_capability_library_schema_and_semantics -q
/Users/wangshucheng/miniconda3/bin/python3 zjskills/scripts/validate_learning_system.py --skill-root zjskills
```

Expected: test PASS and validator prints `VALID`.

- [ ] **Step 6: Commit**

```bash
git add zjskills/assets/schemas/capability-library.schema.yaml \
  zjskills/assets/capability-libraries/ai-foundation.yaml \
  zjskills/scripts/validate_learning_system.py \
  tests/zjskills/test_validate_learning_system.py
git commit -m "feat: add shared ai capability foundation"
```

---

### Task 3: Compose foundation competencies into Domain Packs

**Files:**
- Modify: `zjskills/assets/schemas/domain-pack.schema.yaml`
- Modify: `zjskills/assets/domain-packs/ai-agent.yaml`
- Modify: `zjskills/scripts/validate_learning_system.py`
- Modify: `tests/zjskills/test_validate_learning_system.py`

**Interfaces:**

```yaml
foundation:
  library_id: ai-foundation
  version_constraint: ">=1.0.0 <2.0.0"
  competency_ids:
    - ai-literacy
    - prompt-context
```

Supported constraint syntax is exactly `>=MAJOR.MINOR.PATCH <MAJOR.MINOR.PATCH`. The effective graph combines selected foundation and route-specific competencies/dependencies. A pack without `foundation` remains valid.

- [ ] **Step 1: Add RED composition tests**

Cover valid composition; missing library; incompatible version; missing selected competency; duplicate effective ID; unresolved endpoint; cross-layer cycle; and a passing legacy self-contained pack.

- [ ] **Step 2: Extend the schema**

Add optional closed `foundation` requiring `library_id`, `version_constraint`, and unique nonempty `competency_ids`.

- [ ] **Step 3: Implement resolvers**

```python
def _parse_semver(value: str) -> tuple[int, int, int] | None:
    """Return strict numeric SemVer core or None."""

def _satisfies_version_constraint(version: str, constraint: str) -> bool:
    """Evaluate the supported closed-open constraint."""

def _resolve_domain_pack_foundation(
    pack_name: str,
    pack: dict[str, Any],
    libraries: dict[str, dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, str]], list[str]]:
    """Return effective competencies, dependencies, and deterministic errors."""
```

Pass resolved lists into `_validate_domain_pack_semantics` and sort errors deterministically.

- [ ] **Step 4: Migrate the AI Agent pack**

Reference all six foundation competencies. Remove copied definitions only after every project/assessment reference resolves. Preserve its route capabilities, six projects, rubrics, and assessment coverage.

- [ ] **Step 5: Run regression and commit**

```bash
/Users/wangshucheng/miniconda3/bin/python3 -m unittest discover \
  -s tests/zjskills -p 'test_*.py' -q
git add zjskills/assets/schemas/domain-pack.schema.yaml \
  zjskills/assets/domain-packs/ai-agent.yaml \
  zjskills/scripts/validate_learning_system.py \
  tests/zjskills/test_validate_learning_system.py
git commit -m "feat: compose domain packs with ai foundation"
```

Expected: all tests through Task 3 PASS, including legacy compatibility.

---

### Task 4: Add the Vibe Coding route pack

**Files:**
- Create: `zjskills/assets/domain-packs/vibe-coding.yaml`
- Modify: `tests/zjskills/test_validate_learning_system.py`

**Interfaces:**
- Competencies: `problem-acceptance-definition`, `ai-coding-collaboration`, `code-reading-change`, `interface-interaction-basics`, `api-data-integration`, `debugging-testing`, `deployment-observability`, `product-iteration`.
- Projects: `vibe-single-page-tool`, `vibe-data-application`, `vibe-api-application`, `vibe-complete-web-product`, `vibe-deployable-ai-application`, `vibe-real-user-delivery`.
- Assisted generation alone cannot pass; inspection, change, debugging, testing, and delivery evidence are required.

- [ ] **Step 1: Add RED `test_vibe_coding_pack_contract`**

Require exact IDs, six ordered levels, suitability/unsuitability, non-generation readiness evidence, effective-graph coverage, rubric weights/critical dimensions, and current review metadata.

- [ ] **Step 2: Author the pack**

Reference all six foundation competencies. Define L0-L5 behavior, dependencies, six projects, analytic rubrics summing to 100, failure modes, assessments, and employment/current-role/entrepreneurship/delivery outcomes.

- [ ] **Step 3: Validate and commit**

```bash
/Users/wangshucheng/miniconda3/bin/python3 -m unittest \
  tests.zjskills.test_validate_learning_system.LearningSystemValidationTests.test_vibe_coding_pack_contract -q
/Users/wangshucheng/miniconda3/bin/python3 zjskills/scripts/validate_learning_system.py --skill-root zjskills
git add zjskills/assets/domain-packs/vibe-coding.yaml tests/zjskills/test_validate_learning_system.py
git commit -m "feat: add vibe coding learning route"
```

Expected: test PASS, validator `VALID`, commit created.

---

### Task 5: Add the AI Product Manager route pack

**Files:**
- Create: `zjskills/assets/domain-packs/ai-product-manager.yaml`
- Modify: `tests/zjskills/test_validate_learning_system.py`

**Interfaces:**
- Competencies: `user-business-problem`, `ai-capability-boundaries`, `data-evaluation-design`, `prototype-experiment`, `requirements-acceptance`, `technical-collaboration`, `responsible-product-risk`, `metrics-delivery`.
- Projects: `pm-problem-analysis`, `pm-ai-feature-proposal`, `pm-testable-prototype`, `pm-complete-product-case`, `pm-cross-functional-simulation`, `pm-real-business-validation`.

- [ ] **Step 1: Add RED `test_ai_product_manager_pack_contract`**

Require exact IDs, six levels, evidence distinguishing slides from testable product decisions, complete rubrics, risk assessment, technical collaboration, and business validation.

- [ ] **Step 2: Author the pack**

Reference the full AI foundation. Encode L0-L5 behavior, dependencies, six projects, rubrics, failure modes, assessments, and outcome preparation. Projects after level 1 require a user/business hypothesis, AI limitation, measurable acceptance criteria, and evidence review.

- [ ] **Step 3: Validate and commit**

```bash
/Users/wangshucheng/miniconda3/bin/python3 -m unittest \
  tests.zjskills.test_validate_learning_system.LearningSystemValidationTests.test_ai_product_manager_pack_contract -q
/Users/wangshucheng/miniconda3/bin/python3 zjskills/scripts/validate_learning_system.py --skill-root zjskills
git add zjskills/assets/domain-packs/ai-product-manager.yaml tests/zjskills/test_validate_learning_system.py
git commit -m "feat: add ai product manager learning route"
```

Expected: test PASS, validator `VALID`, commit created.

---

### Task 6: Add both AI Operations branch packs

**Files:**
- Create: `zjskills/assets/domain-packs/ai-operations-content-growth.yaml`
- Create: `zjskills/assets/domain-packs/ai-operations-business-efficiency.yaml`
- Modify: `tests/zjskills/test_validate_learning_system.py`

**Interfaces:**
- Content/growth competencies: `audience-channel-analysis`, `research-topic-selection`, `ai-content-system`, `distribution-user-operations`, `community-operations`, `growth-experiment`, `growth-measurement-review`, `content-safety`.
- Content/growth projects: `ops-content-single-task`, `ops-content-repeatable-workflow`, `ops-channel-user-experiment`, `ops-automated-growth-workflow`, `ops-evidence-portfolio`, `ops-real-campaign-delivery`.
- Efficiency competencies: `process-mapping`, `information-data-handling`, `workplace-tool-application`, `workflow-design`, `bounded-automation`, `human-review-quality`, `knowledge-system-adoption`, `business-value-measurement`.
- Efficiency projects: `ops-efficiency-single-task`, `ops-information-data-workflow`, `ops-bounded-automation`, `ops-department-scenario`, `ops-measurable-efficiency-case`, `ops-real-operational-delivery`.

- [ ] **Step 1: Add RED `test_ai_operations_branch_contracts`**

Require shared foundation plus disjoint route-specific IDs. Content must measure audience/growth outcomes; efficiency must measure quality, time, errors, adoption, and business value.

- [ ] **Step 2: Author the content/growth pack**

Define complete L0-L5 behavior, dependencies, projects, rubrics, assessments, safety-critical dimensions, failures, and outcomes. Content volume, impressions, or generated text alone cannot pass.

- [ ] **Step 3: Author the business-efficiency pack**

Define complete L0-L5 behavior, dependencies, projects, rubrics, assessments, privacy/human-review critical dimensions, failures, and outcomes. Automation count or tool usage alone cannot pass.

- [ ] **Step 4: Validate and commit**

```bash
/Users/wangshucheng/miniconda3/bin/python3 -m unittest \
  tests.zjskills.test_validate_learning_system.LearningSystemValidationTests.test_ai_operations_branch_contracts -q
/Users/wangshucheng/miniconda3/bin/python3 zjskills/scripts/validate_learning_system.py --skill-root zjskills
git add zjskills/assets/domain-packs/ai-operations-*.yaml tests/zjskills/test_validate_learning_system.py
git commit -m "feat: add ai operations learning branches"
```

Expected: test PASS, validator `VALID`, commit created.

---

### Task 7: Add the AI Tools and Workplace route pack

**Files:**
- Create: `zjskills/assets/domain-packs/ai-tools-workplace.yaml`
- Modify: `tests/zjskills/test_validate_learning_system.py`

**Interfaces:**
- Competencies: `workplace-task-framing`, `research-source-verification`, `document-delivery`, `spreadsheet-analysis`, `presentation-communication`, `knowledge-management`, `multi-tool-collaboration`, `lightweight-automation`.
- Projects: `tools-single-task`, `tools-personal-workflow`, `tools-multi-tool-workflow`, `tools-role-specific-solution`, `tools-team-efficiency-case`, `tools-real-workplace-delivery`.

- [ ] **Step 1: Add RED `test_ai_tools_workplace_pack_contract`**

Require exact IDs, six levels, role transfer, verification/privacy evidence, measurable workplace value, and vendor-neutral wording.

- [ ] **Step 2: Author the pack**

Reference the full foundation. Encode L0-L5 behavior, dependencies, six projects, rubrics, failures, assessments, and outcomes. Changed-condition performance is required so copying a supplied prompt cannot pass.

- [ ] **Step 3: Validate and commit**

```bash
/Users/wangshucheng/miniconda3/bin/python3 -m unittest \
  tests.zjskills.test_validate_learning_system.LearningSystemValidationTests.test_ai_tools_workplace_pack_contract -q
/Users/wangshucheng/miniconda3/bin/python3 zjskills/scripts/validate_learning_system.py --skill-root zjskills
git add zjskills/assets/domain-packs/ai-tools-workplace.yaml tests/zjskills/test_validate_learning_system.py
git commit -m "feat: add ai workplace tools learning route"
```

Expected: test PASS, validator `VALID`, commit created.

---

### Task 8: Add evidence-based route decisions and AI routing

**Files:**
- Create: `zjskills/assets/schemas/route-decision.schema.yaml`
- Create: `zjskills/assets/templates/route-decision.yaml`
- Create: `zjskills/references/ai-route-router.md`
- Modify: `zjskills/scripts/validate_learning_system.py`
- Modify: `zjskills/SKILL.md`
- Modify: `zjskills/references/discovery.md`
- Modify: `zjskills/references/interaction-orchestrator.md`
- Modify: `tests/zjskills/test_validate_learning_system.py`

**Interfaces:**
- Artifact: goal/baseline/constraints, candidates, supporting/opposing evidence, experience results, effort/difficulty/risk, decision groups, confidence, uncertainty, one next validation action.
- Visible IDs: `ai-agent`, `vibe-coding`, `ai-product-manager`, `ai-operations`, `ai-tools-workplace`.
- AI Operations branch: `content-growth`, `business-efficiency`, or `defer`.
- A route decision never counts as capability evidence or passes a gate.

- [ ] **Step 1: Add RED schema/runtime tests**

Validate a complete artifact. Reject zero candidates, unknown route, recommendation outside candidates, overlapping decision groups, absent opposing-evidence field, completed experience without evidence, and missing next validation action. Require a discriminating task at insufficient confidence.

- [ ] **Step 2: Define and register the artifact**

Register `route-decision` for `route-decision.yaml` and `route-decisions/*.yaml`. The template compares AI Agent and Vibe Coding and defers until one bounded build task is reviewed.

- [ ] **Step 3: Write `ai-route-router.md`**

Specify intent classification, comparison dimensions, smallest discriminating tasks, decision/defer rules, Operations branch selection, route switching, and beginner card output. Use ranges/dates; promise no job outcome.

- [ ] **Step 4: Integrate discovery and interaction**

Add natural-language route-comparison triggers without a seventh home choice. Route unclear directions through Discovery and return one next task or one decision-changing question.

- [ ] **Step 5: Validate and commit**

```bash
/Users/wangshucheng/miniconda3/bin/python3 -m unittest \
  tests.zjskills.test_validate_learning_system.LearningSystemValidationTests.test_route_decision_schema_and_runtime -q
/Users/wangshucheng/miniconda3/bin/python3 zjskills/scripts/validate_learning_system.py \
  --skill-root zjskills --learner-dir tests/zjskills/fixtures/valid-learner
git add zjskills tests/zjskills/test_validate_learning_system.py
git commit -m "feat: add evidence based ai route decisions"
```

Expected: test PASS and learner fixture `VALID`.

---

### Task 9: Add learning-material mapping and practice conversion

**Files:**
- Create: `zjskills/assets/schemas/learning-material-map.schema.yaml`
- Create: `zjskills/assets/templates/learning-material-map.yaml`
- Create: `zjskills/references/learning-material-engine.md`
- Modify: `zjskills/scripts/validate_learning_system.py`
- Modify: `zjskills/SKILL.md`
- Modify: `zjskills/references/interaction-orchestrator.md`
- Modify: `zjskills/references/curriculum-engine.md`
- Modify: `zjskills/references/assessment-engine.md`
- Modify: `tests/zjskills/test_validate_learning_system.py`

**Interfaces:**
- Claim classes: `fact`, `opinion`, `example`, `inference`, `unverified_claim`.
- Artifact includes sources/dates/scope, concepts/dependencies, competency links, contradictions, gaps, stale claims, beginner explanation, retrieval questions, practice, transfer task, review schedule, next action.
- Missing contents trigger a request for the smallest usable content. Summary is activity, never capability proof.

- [ ] **Step 1: Add RED artifact tests**

Validate a complete map. Reject unknown claim class, missing date/scope, unknown dependency endpoint, unknown active competency, contradiction to unknown claim, empty transfer task, and review before receipt.

- [ ] **Step 2: Define and register the artifact**

Register `learning-material-map` for singleton and `learning-material-maps/*.yaml`. Use closed core records and ISO fields consistent with existing artifacts.

- [ ] **Step 3: Write the material engine**

Specify intake/availability, traceable claim extraction/classification, concepts/dependencies, competency mapping, contradiction/gap/staleness handling, beginner explanation, retrieval practice, transfer, and spaced review.

- [ ] **Step 4: Integrate runtime engines**

Accept phrases such as “帮我整理这份资料” and “把这些内容变成我能学会的练习”. Feed prerequisites to Curriculum and observable transfer to Assessment without awarding capability for reading.

- [ ] **Step 5: Validate and commit**

```bash
/Users/wangshucheng/miniconda3/bin/python3 -m unittest \
  tests.zjskills.test_validate_learning_system.LearningSystemValidationTests.test_learning_material_map_schema_and_runtime -q
/Users/wangshucheng/miniconda3/bin/python3 zjskills/scripts/validate_learning_system.py --skill-root zjskills
git add zjskills tests/zjskills/test_validate_learning_system.py
git commit -m "feat: turn learning materials into practice maps"
```

Expected: test PASS and asset validator `VALID`.

---

### Task 10: Add safe generic learning mode and companion integration

**Files:**
- Create: `zjskills/references/generic-learning-engine.md`
- Modify: `zjskills/SKILL.md`
- Modify: `zjskills/references/interaction-orchestrator.md`
- Modify: `zjskills/references/problem-solving-engine.md`
- Modify: `zjskills/references/optimization-engine.md`
- Modify: `zjskills/references/meta-learning-engine.md`
- Modify: `tests/zjskills/test_open_source_package.py`
- Modify: `tests/zjskills/scenarios.yaml`

**Interfaces:**
- Claim labels: `sourced`, `user_supplied`, `inferred`, `assumed`, `unknown`.
- May decompose goals, organize supplied material, build provisional models, design practice/projects/schedules/reviews, solve evidence-backed problems, and adapt.
- Must request the smallest source/example/rubric/expert feedback/performance task before unsupported professional, safety, or readiness claims.
- Existing impact levels remain `none`, `task`, `week`, `roadmap`, `goal_system`.

- [ ] **Step 1: Add RED runtime/scenario tests**

Require all five labels, no unsupported domain authority, one-action beginner output, and scenario IDs `non-ai-goal-with-source`, `non-ai-goal-without-source`, `material-link-without-content`, `route-ambiguity-experience-task`, `ai-operations-branch-ambiguity`, and `goal-change-rebuild-route`.

- [ ] **Step 2: Write the generic learning engine**

Define eligibility, provisional-model workflow, evidence labels, missing-source recovery, safety/readiness limits, and handoffs to existing engines.

- [ ] **Step 3: Integrate routing**

Update reference loading and intent routing while preserving six home cards. For non-AI goals, state the method boundary plainly and continue with the smallest safe next step.

- [ ] **Step 4: Verify and commit**

```bash
/Users/wangshucheng/miniconda3/bin/python3 -m unittest \
  tests.zjskills.test_open_source_package.OpenSourcePackageTests.test_runtime_has_no_human_referral_or_conversion_logic \
  tests.zjskills.test_open_source_package.OpenSourcePackageTests.test_generic_learning_runtime_contract -q
git add zjskills tests/zjskills/test_open_source_package.py tests/zjskills/scenarios.yaml
git commit -m "feat: add safe generic learning companion mode"
```

Expected: both tests PASS and commit created.

---

### Task 11: Publish bilingual 2.1 usage and installation guidance

**Files:**
- Modify: `README.md`
- Modify: `README.en.md`
- Modify: `docs/getting-started.md`
- Modify: `docs/getting-started.en.md`
- Modify: `docs/usage-guide.md`
- Modify: `docs/usage-guide.en.md`
- Modify: `docs/platform-installation.md`
- Modify: `docs/platform-installation.en.md`
- Modify: `docs/examples.md`
- Modify: `docs/examples.en.md`
- Modify: `CHANGELOG.md`
- Modify: `zjskills/SKILL.md`
- Modify: `tests/zjskills/test_open_source_package.py`

**Interfaces:**
- Explain five routes, two Operations branches, route comparison, material learning, problem solving, plan adjustment, generic transfer, evidence limits, and beginner prompts.
- Keep URL `https://github.com/zhijianZJ/ZJSkills` and identifier `zjskills`.
- Add exactly to the four Chinese public usage/installation surfaces:

```text
使用 ZJSkills 时如遇到使用问题、规划疑问或其他未解决问题，可联系智建进入答疑群交流。
```

- Add exactly to the paired English surfaces:

```text
If you encounter usage issues, planning questions, or other unresolved problems while using ZJSkills, contact Zhijian to join the Q&A group.
```

- [ ] **Step 1: Add RED bilingual documentation tests**

Require paired headings, route names, prompts, evidence boundary, supported platforms, exact URL, exact note sentences, and `2.1.0`; require note absence below `zjskills/`.

- [ ] **Step 2: Update README/getting started**

Lead with choosing a direction, building a route, learning from materials, solving blockers, and adapting. Add copy-paste prompts for route selection, material learning, and a blocker.

- [ ] **Step 3: Update usage/examples**

Document five routes/six packs, defer behavior, material availability, generic limits, concise rationale, artifact behavior, and paired mini-dialogues. Put the support note in a clearly labeled documentation section.

- [ ] **Step 4: Update platform installation**

Cover Codex, Claude Code, WorkBuddy, Doubao, and generic prompt/file-upload platforms. Distinguish native installation from manual context use; do not claim unsupported native Skills.

- [ ] **Step 5: Update release metadata**

Set version surfaces to `2.1.0`; add a dated changelog entry covering shared foundation, routes, route/material artifacts, generic mode, compatibility, and documentation-only support.

- [ ] **Step 6: Test and commit**

```bash
/Users/wangshucheng/miniconda3/bin/python3 -m unittest tests.zjskills.test_open_source_package -q
git add README.md README.en.md CHANGELOG.md docs zjskills/SKILL.md tests/zjskills/test_open_source_package.py
git commit -m "docs: publish zjskills 2.1 learning guidance"
```

Expected: documentation tests PASS, links resolve, runtime neutrality remains PASS.

---

### Task 12: Run forward evaluations, isolated installation, and release review

**Files:**
- Modify only if a failed check reveals a contract defect.
- Add a fixture under `tests/zjskills/fixtures/` only after reproducing a defect in a failing test.

**Interfaces:**
- Produces a validated 2.1.0 branch and new Draft PR.
- Does not merge, publish a release, or alter PR #5.

- [ ] **Step 1: Run the complete regression suite**

```bash
/Users/wangshucheng/miniconda3/bin/python3 -m unittest discover \
  -s tests/zjskills -p 'test_*.py' -q
```

Expected: all tests PASS with zero failures/errors.

- [ ] **Step 2: Run Skill and learner validators**

```bash
/Users/wangshucheng/miniconda3/bin/python3 \
  /Users/wangshucheng/.codex/skills/.system/skill-creator/scripts/quick_validate.py zjskills
/Users/wangshucheng/miniconda3/bin/python3 zjskills/scripts/validate_learning_system.py \
  --skill-root zjskills --learner-dir tests/zjskills/fixtures/valid-learner
```

Expected: `Skill is valid!` and `VALID`.

- [ ] **Step 3: Review forward scenarios**

Verify:

- ambiguous route -> one discriminating experience task;
- ambiguous Operations route -> both branches preserved or `defer`;
- missing material body -> request content, never invented summary;
- non-AI without sources -> provisional method plus explicit unknowns;
- generated code without debug/test evidence -> no Vibe readiness;
- content volume without growth evidence -> no content-operations readiness;
- automation without review/value evidence -> no efficiency readiness;
- goal change -> versioned rebuild, never silent history overwrite.

Record every defect as a failing automated test before fixing it.

- [ ] **Step 4: Test isolated installation**

```bash
install_root="$(mktemp -d)"
mkdir -p "$install_root/zjskills"
cp -R zjskills/. "$install_root/zjskills/"
/Users/wangshucheng/miniconda3/bin/python3 \
  /Users/wangshucheng/.codex/skills/.system/skill-creator/scripts/quick_validate.py \
  "$install_root/zjskills"
/Users/wangshucheng/miniconda3/bin/python3 \
  "$install_root/zjskills/scripts/validate_learning_system.py" \
  --skill-root "$install_root/zjskills"
```

Expected: isolated copy prints `Skill is valid!` and `VALID`.

- [ ] **Step 5: Audit names, links, placeholders, and diff**

```bash
rg -n "LearningArchitectSklls|king-wsc|TO[D]O|T[B]D|PLACE[H]OLDER" \
  README.md README.en.md CHANGELOG.md docs zjskills tests/zjskills \
  -g '!docs/superpowers/**'
git diff --check
git status --short
git log --oneline --decorate -12
```

Expected: no obsolete repository/name or placeholder matches except intentional migration history covered by tests; no whitespace errors; only intentional changes.

- [ ] **Step 6: Request review**

Use `superpowers:requesting-code-review` against the approved design and this plan. Resolve confirmed blocking/high-impact issues with a failing test first, then rerun Steps 1-5.

- [ ] **Step 7: Push and open a separate Draft PR**

```bash
git push -u origin codex/zjskills-learning-routes
gh pr create \
  --draft \
  --base main \
  --head codex/zjskills-learning-routes \
  --title "feat: expand ZJSkills AI learning routes" \
  --body-file docs/superpowers/specs/2026-07-20-zjskills-ai-routes-and-learning-companion-design.md
```

Expected: new Draft PR URL distinct from PR #5.

## Final Acceptance Checklist

- [ ] Version is `2.1.0` everywhere required.
- [ ] Six Domain Packs validate against one shared foundation and retain six-project ladders.
- [ ] A legacy self-contained pack and existing learner fixture still validate.
- [ ] Route selection can recommend, offer alternatives, or defer from evidence/tasks.
- [ ] Material learning produces traceable concepts, practice, transfer, and review.
- [ ] Generic learning labels certainty and refuses unsupported domain authority.
- [ ] Beginner interaction stays plain-language, one-action-first, and six-navigation compatible.
- [ ] Runtime contains no 智建/group/community/course/referral/conversion logic.
- [ ] Bilingual public docs contain the approved transparent 智建 answer-group note.
- [ ] Full tests, validators, scenarios, isolated installation, and diff checks pass.
- [ ] Work is pushed to `codex/zjskills-learning-routes` in a new Draft PR.
