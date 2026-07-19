# Project Engine

## Purpose

The Project Engine designs authentic work that converts L0–L5 capability claims into assessable evidence and business value. Projects are generated from target outcomes and gaps, not from a predetermined course list.

## Six-level evidence ladder

1. **focused tool:** a bounded component or utility; evidence includes runnable output, tests, usage notes, and a short decision explanation.
2. **knowledge application:** applies domain knowledge to a representative problem; evidence adds a requirements note, data or knowledge provenance, and correctness checks.
3. **workflow:** connects multiple steps or systems; evidence adds an interface contract, failure handling, end-to-end evaluation, and an operating guide.
4. **enterprise scenario:** works under organizational constraints; evidence adds security and privacy analysis, observability, cost or reliability targets, stakeholder acceptance criteria, and rollback operations.
5. **portfolio case:** communicates a defensible professional case; evidence adds a problem narrative, alternatives and trade-offs, before/after measures, architecture, demonstration, and reflection.
6. **real external delivery:** serves an actual external stakeholder; evidence adds a dated brief, scope agreement, change log, acceptance or usage evidence, handover, and stakeholder feedback while protecting confidential data.

Advanced learners may combine projects or deliver one artifact across multiple levels, but no level's evidence requirements may be deleted. Combined projects must map each retained evidence item to its originating level.

## Project contract

Every project and Domain Pack archetype has a stable ID, problem, users, nonempty inputs, nonempty constraints, deliverables, competency targets with levels, business value hypothesis, success measures, risks, evidence plan, and analytic `rubric`. It must explicitly include `common_failure_modes`, `demonstration_requirements`, `documentation_requirements`, and `retrospective_requirements`; these are required evidence contracts, not optional authoring hints. Business value must be concrete—such as time saved, error reduction, decision quality, revenue enablement, risk reduction, or stakeholder adoption—and must identify the beneficiary and measurement method.

The analytic rubric has exactly six dimensions: `correctness`, `capability_behavior`, `reliability`, `responsible_practice`, `business_value`, and `technical_communication`. Every dimension has a positive `weight`, typed `critical` flag, typed `passing_threshold`, and four observable `performance_bands`; weights total 100 and at least one dimension is critical. Demonstration requirements state what must be shown live or reproducibly; documentation requirements identify durable handover artifacts; retrospective requirements require evidence-based analysis of failures, decisions, and next changes. Store evaluator, evidence IDs, score, feedback, and verification date separately from the project brief.

## Coverage matrix

Maintain a matrix with one row per core competency and columns for target L0–L5 behavior, project ID, deliverable or test, rubric dimension, evaluator, and threshold. Every core competency needs at least one authentic evidence cell; high-risk or L4–L5 claims need independent or external evaluation. Detect uncovered competencies, project claims without rubric dimensions, and rubric dimensions without artifacts.

## Version and gate

Use a positive integer `content_version` for each project artifact revision and stable project IDs across revisions. Use SemVer only for the source Domain Pack `version`, with its `last_reviewed_at`, source-dated market assumptions, and migration maps. A changed competency ID or level recomputes the coverage matrix; a changed target or constraint revalidates business value and feasibility.

Pass only when six archetypes are represented, coverage is complete, business value is testable, rubrics name thresholds, and the evidence plan is feasible and ethical. Return a natural-language explanation plus the canonical `engine_result` from `workflow.md` with `engine: project-design`, enum confidence, affected downstream roadmap and assessment artifacts, and one next action.
