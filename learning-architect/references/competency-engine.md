# Competency Engine

## Purpose and inputs

The Competency Engine turns a target outcome, learner evidence, and a versioned Domain Pack into a reusable occupational capability model. It models capabilities, not courses. Every decision cites an input or is labeled as an assumption with `confidence: low | medium | high`.

## Competency contract

Each competency has a stable, kebab-case `id`, category, weight, target level, observable behaviors, and evidence requirements. IDs survive wording changes; replacements require a migration map. Use this canonical behavioral scale everywhere without redefining, skipping, or shifting a level:

- **L0 — no exposure:** has not encountered the capability's concepts or practice.
- **L1 — recognize/describe/explain basics:** recognizes the capability and describes or explains its basic terms, purpose, and limits.
- **L2 — complete with example/template/guidance:** completes a representative exercise using an example, template, prompts, or guidance.
- **L3 — independently complete a bounded real task:** independently completes a bounded real task under stated constraints and supplies evidence.
- **L4 — debug/optimize/migrate/handle exceptions:** debugs failures, optimizes trade-offs, migrates an implementation, and handles important exceptions.
- **L5 — architect/review/teach:** architects a solution or standard, reviews others' work, and teaches the capability with accountable judgment.

Every level statement must begin with an observable action. Level evidence is cumulative: evidence for L4 must also demonstrate the required L0–L3 behaviors. A target level without a behavior and evidence requirement fails the gate.

## Generation rules

1. Start from the target outcome and work backward to observable workplace decisions and deliverables.
2. Reuse stable Domain Pack IDs where semantics match; add an extension ID only when the pack has a genuine gap.
3. Separate core, supporting, and differentiating capabilities. Normalize core weights so prioritization is explicit.
4. Set current levels only from dated evidence; otherwise record `needs_input` or a low-confidence hypothesis and request the smallest discriminating assessment.
5. Attach evidence requirements that name an artifact, an observable behavior, an evaluator, and a threshold.
6. Persist `schema_version`, semantic `content_version`, `source`, `confidence`, timestamps, and `affected_downstream`.

## Change control

Use semantic versioning: patch for clarification without changed meaning, minor for backward-compatible additions, and major for removed or redefined IDs. Each release records `last_reviewed_at`, review interval, source-dated market assumptions, and a migration map such as `old-id -> new-id | retired | split:[...]`. A Domain Pack review invalidates stale capability decisions and triggers Gap, Curriculum, and Project revalidation.

## Gate and return

Pass only when every core competency has a stable ID, L0–L5 behavioral scale, target level, weight, and authentic evidence requirement. Return a concise natural-language explanation followed by the canonical `engine_result` from `workflow.md`; do not invent another wrapper. Set `engine: competency-design`, list artifacts actually written, and keep `gate.passed: false` while any required field or evidence source is missing.
