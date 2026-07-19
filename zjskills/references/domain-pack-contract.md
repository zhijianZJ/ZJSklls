# Domain Pack Contract

## Role

A Domain Pack is a reusable, versioned occupational reference. It supplies target outcomes, L0–L5 capability definitions, an acyclic prerequisite graph, six project archetypes, assessment patterns, outcome preparation, and source-dated market assumptions. It is a planning baseline, not a universal truth or a paid-course catalog; learner evidence and local context may override it with an explicit rationale.

## Required governance

- Use a stable occupational `id`, the supported `schema_version`, positive integer `content_version`, semantic `version`, lifecycle status, `source`, enum `confidence`, creation/update timestamps, `last_reviewed_at`, and `review_interval_days`. Increment `content_version` for each pack artifact revision; reserve SemVer for `version`.
- Keep competency, dependency, project, assessment, and outcome-preparation IDs stable. Validate unique IDs, dependency endpoints, and acyclicity.
- Store a migration map for every renamed, split, merged, or retired stable ID. A target must resolve to a current competency ID; a retired node uses the documented `{to: retired, reason: ...}` sentinel. A major semantic break increments the major version; additions use minor; non-semantic corrections use patch.
- Record each market assumption with a unique stable ID, `as_of` date, named source and URL or durable reference, claim, confidence, implication, and valid `next_review_at`. Reject an assumption when its review date is expired under the validator's current-date policy. Assumptions are evidence, not timeless requirements.
- Review when the interval expires or material tooling, regulation, role demand, or evaluation practice changes. Mark stale packs and revalidate affected Gap, Competency, Curriculum, Project, Roadmap, and Outcome Preparation artifacts.

## Content rules

Competencies use the unchanged canonical L0–L5 scale in `competency-engine.md` and define domain-specific observable behavior and evidence at each level. Dependencies are a directed acyclic graph. Project archetypes cover focused tool, knowledge application, workflow, enterprise scenario, portfolio case, and real external delivery; combining them cannot delete evidence. Each archetype includes nonempty inputs and constraints, deliverables, competencies, business value, common failure modes, demonstration, documentation and retrospective requirements, and a six-dimension analytic rubric whose weights total 100. Every dimension declares a boolean `critical` flag and a `passing_threshold` of `developing`, `proficient`, or `strong`; at least one dimension is critical.

Assessment patterns state evaluator, artifact, observed behavior, threshold, feedback loop, and named capability checks. Across the pack they explicitly assess independent completion, explanation of trade-offs, modification for changed requirements, debugging, deployment or delivery, and teaching or review. Every pattern distinguishes `understanding` (can explain), `guided` (completes with example/template/guidance), `independent` (completes a bounded real task unaided), and `transfer` (adapts the capability to changed or novel conditions). Outcome preparation is route-specific and never equates course completion with readiness.

Resource catalogs are optional and replaceable. Entries describe coverage, constraints, freshness, accessibility, and selection rationale; no specific paid course may be a required recommendation. Projects include business value, rubrics, and a competency coverage matrix.

## Validation and consumption

Validate the YAML against `assets/schemas/domain-pack.schema.yaml`, then check semantic invariants the schema cannot express: unique stable IDs, all dependency endpoints present, no cycles, six project levels, complete L0–L5 behaviors, source-dated assumptions, evidence coverage, and migration-map integrity.

Consuming engines cite the pack ID and version and distinguish copied facts from inference. If the pack is missing, stale, contradictory, or below the needed confidence, return `needs_input` rather than silently guessing. Each engine responds with a concise natural-language explanation and the unchanged canonical `engine_result` from `workflow.md`, including `confidence: low | medium | high`, artifacts written, affected downstream items, gate status, and a concrete next action.
