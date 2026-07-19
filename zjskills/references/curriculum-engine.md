# Curriculum Engine

## Purpose

The Curriculum Engine converts prioritized competency gaps into a dependency-safe sequence of learning units. It optimizes for evidence-producing progress, not content consumption or a fixed vendor syllabus.

## Graph contract

Each unit has a stable `id`, served competency IDs and levels, entry evidence, exit evidence, practice, estimated effort, and resource-selection criteria. A directed edge `from -> to` means the `from` unit is a prerequisite of `to`. Every endpoint must exist, self-edges are forbidden, and the graph must be acyclic. Validate with a topological sort; if not all nodes are emitted, return `blocked` with the cycle path and do not publish a roadmap.

Learning units inherit the L0–L5 behavioral definitions in `competency-engine.md`. A unit may advance one or several competencies, but its exit evidence must state the exact behavior and level demonstrated. Remove units that serve no prioritized gap.

## Sequencing rules

1. Select the smallest prerequisite closure for the target competencies.
2. Order foundation before integration, integration before optimization, and insert retrieval and transfer practice after first successful performance.
3. Prefer short feedback loops and early authentic artifacts. Parallelize only nodes whose prerequisites are satisfied and whose combined load fits learner constraints.
4. Preserve alternate paths for verified prior knowledge; skipping requires evidence, not self-report alone.
5. Attach project milestones where several capabilities must be integrated.

## Replaceable resource catalogs

Resources are replaceable catalog entries, never hard-coded requirements. Each entry records stable `resource_id`, topic and level coverage, modality, language, accessibility, expected effort, cost band, prerequisites, `source`, `checked_at`, and selection rationale. Units reference capability coverage and selection criteria, so an unavailable or outdated resource can be replaced without changing the graph. Do not recommend a specific paid course as a Domain Pack requirement.

## Version and gate

Use a positive integer `content_version` for each curriculum artifact revision and stable unit IDs across revisions. Use SemVer only for the source Domain Pack `version`; keep its `last_reviewed_at`, source-dated market assumptions, and migration maps for renamed, split, merged, or retired nodes. Re-run cycle and endpoint validation after every change. Pass only when the graph is acyclic, every endpoint exists, every unit serves a gap, resource choices are replaceable, and each core target has a path to evidence.

Return a natural-language explanation and the canonical `engine_result` from `workflow.md` with `engine: curriculum-design`, `confidence: low | medium | high`, the graph artifact, affected downstream projects and plans, gate status, and one concrete next action.
