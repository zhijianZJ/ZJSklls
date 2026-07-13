# Competency Engine

## Purpose and inputs

The Competency Engine turns a target outcome, learner evidence, and a versioned Domain Pack into a reusable occupational capability model. It models capabilities, not courses. Every decision cites an input or is labeled as an assumption with `confidence: low | medium | high`.

## Competency contract

Each competency has a stable, kebab-case `id`, category, weight, target level, observable behaviors, and evidence requirements. IDs survive wording changes; replacements require a migration map. Levels are behavioral rather than time-served:

- **L0 — unaware:** cannot yet recognize the concept or perform the behavior.
- **L1 — recognize:** explains terms and follows a demonstrated example with prompts.
- **L2 — execute:** completes a bounded task independently under familiar constraints.
- **L3 — integrate:** combines the capability with adjacent skills, diagnoses routine failures, and explains trade-offs.
- **L4 — optimize:** handles ambiguous constraints, evaluates alternatives with evidence, and improves quality, reliability, cost, or business value.
- **L5 — lead:** defines standards, handles novel cases, mentors others, and makes accountable cross-system decisions.

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
