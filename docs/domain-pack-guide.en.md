# Domain Pack Extension Guide

A Domain Pack is a replaceable, versioned occupational reference. It gives ZJSkills target outcomes, competency levels, dependencies, project archetypes, assessment patterns, outcome preparation, and dated external assumptions. It is not timeless truth, a learner fact, or a required paid-course catalog.

Before editing, read the [Domain Pack contract](../learning-architect/references/domain-pack-contract.md), [Domain Pack schema](../learning-architect/assets/schemas/domain-pack.schema.yaml), and the existing [AI Agent Engineer example](../learning-architect/assets/domain-packs/ai-agent.yaml). Name a new pack after its stable ID at `learning-architect/assets/domain-packs/<stable-id>.yaml`; add tests under `tests/learning-architect/` and privacy-safe samples under its `fixtures/` directory when needed.

## Data contract

Each pack contains:

- a stable occupational `id`, plus `schema_version`, `content_version`, and semantic `version`;
- lifecycle `status`, operational `source`, enum `confidence`, and creation/update times;
- `last_reviewed_at` and `review_interval_days`;
- `target_outcomes`, `competencies`, `dependencies`, and `project_archetypes`;
- `assessment_patterns`, `outcome_preparation`, and `market_assumptions`.

Stable IDs support references across versions. Do not rename an ID for a wording correction. Increment minor for compatible additions, patch for non-semantic corrections, and major for breaking meaning. Renamed, split, merged, or retired nodes require a migration map. Retirement uses `{to: retired, reason: ...}` so old references never fail silently.

`content_version` identifies content revisions of one artifact. Active records must satisfy the one-active-version invariant. Do not add arbitrary fields rejected by the schema; use constrained `extensions` for legitimate domain additions.

Every target outcome states a name, description, success evidence, source, and `as_of`. Every market assumption has a stable ID, dates, source name, accessible URL or durable reference, precise claim, `confidence`, planning implication, and `next_review_at`. Expired or weak evidence triggers review rather than becoming a permanent job requirement.

## Competencies and dependencies

Each competency has a stable ID, name, category, L0–L5 observable behavior, and evidence requirements. The canonical scale is:

- L0: no exposure;
- L1: recognize and explain basics;
- L2: complete with an example, template, or guidance;
- L3: independently complete a bounded real task;
- L4: debug, optimize, migrate, and handle exceptions;
- L5: architect, review, and teach.

Write domain-specific observable behavior, not “beginner/intermediate/advanced” labels or topic lists. Evidence requirements should name runtime results, artifacts, tests, reviews, or observed performance—not watching, reading, attendance, or certificates.

Dependency edges point `from` a prerequisite `to` a downstream capability. All endpoints must exist, IDs must be unique, and the graph must be acyclic. Add only dependencies that materially affect safety or understanding. Do not force every competency into one linear chain. When reusing a competency across domains, preserve its semantic meaning; if the meaning must evolve, use explicit versioning and migration mappings rather than silently repurposing the ID.

## Project archetypes and rubric gates

A complete pack provides exactly six progressive archetypes: focused tool, knowledge application, workflow, enterprise scenario, portfolio case, and real external delivery. Each includes:

- non-empty `inputs`, authentic `constraints`, and verifiable `deliverables`;
- covered `competency_ids` and business value;
- expected evidence and common failure modes;
- demonstration, documentation, and retrospective requirements;
- a six-dimension analytic rubric.

The rubric dimensions are correctness, capability behavior, reliability, responsible practice, business value, and technical communication, with weights totaling 100. Every dimension uses boolean `critical`, a `passing_threshold` of `developing | proficient | strong`, and performance bands for `insufficient`, `developing`, `proficient`, and `strong`. At least one dimension is critical; a critical failure cannot be hidden by the aggregate score.

Assessment patterns define evaluator, artifact, observed behavior, threshold, feedback loop, and capability checks. Across the pack they cover independent completion, explaining trade-offs, modifying for changed requirements, debugging, deployment or delivery, and teaching or review. Results distinguish `understanding`, `guided`, `independent`, and `transfer`.

Outcome preparation defines route-specific minimum evidence, artifacts, and readiness gates for employment, promotion, entrepreneurship, or delivery. Course completion is not readiness, and unsupported public capability claims are prohibited.

## Sources, review, and migration

Prefer primary, traceable sources matched to the target geography and date. Record a specific claim, not merely a link. Set an appropriate review interval. `next_review_at` must not be earlier than the validation date; once that date has passed, the assumption requires review. Material changes in tools, regulation, role demand, or evaluation practice update the pack and trigger rechecks from Gap through Project, Roadmap, and Outcome Preparation as affected.

Keep a changelog and migration map for every material revision. Consuming engines cite pack ID and version and distinguish copied domain facts from learner-specific inference. A missing, stale, contradictory, or insufficient-confidence pack returns `needs_input` instead of silently guessing.

Resource catalogs are optional and replaceable. If included, record coverage, limitations, freshness, accessibility, and selection rationale. Never make one paid course a required recommendation.

## Validation and contribution

Validation requires Python 3.9+ with `PyYAML`, `jsonschema`, and `referencing`. Run from the repository root:

```bash
python3 learning-architect/scripts/validate_learning_system.py \
  --skill-root learning-architect \
  --learner-dir tests/learning-architect/fixtures/valid-learner
python3 -m unittest tests/learning-architect/test_validate_learning_system.py -q
python3 -m unittest tests/learning-architect/test_open_source_package.py -q
```

Validation covers schema requirements and semantic invariants that schemas cannot fully express: unique IDs, valid endpoints, acyclicity, six project levels, complete L0–L5 behavior, current source dates, evidence coverage, rubric weights, and migration integrity.

Before submitting:

1. Test the pack against realistic, privacy-safe samples.
2. Confirm source, date, confidence, and scope.
3. Document changed stable IDs, versions, and migration impact.
4. Add a test that fails before the change and passes after it.
5. Include no personal advertising, hidden promotion, unverifiable credentials, or branding that enters learner output.
6. Keep the pull request scoped and state affected downstream engines and validation results.

See [CONTRIBUTING.md](../CONTRIBUTING.md) for repository-wide contribution and review rules.
