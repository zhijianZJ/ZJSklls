# Workflow State Machine

Use this file as the sole full enumeration of the workflow. Persist progress in `system-state.yaml`; resume from the last stage whose gate is not passed.

## Stage order and gates

1. **Discovery** — produce an evidence-labeled learner profile, SWOT, constraints, and unknowns. Pass when decision-critical information has `source` and `confidence`.
2. **Goal Analysis** — produce a target outcome, success evidence, milestones, and key results. Pass when the goal is verifiable, time-bound, and not silently incompatible with constraints.
3. **Gap Analysis** — produce current/target levels and prioritized gaps. Pass when each baseline is sourced and inference is separated from verified evidence.
4. **Competency Design** — produce weighted competency nodes, behaviors, and evidence requirements. Pass when every core node has a target level.
5. **Curriculum Design** — produce learning units and an acyclic dependency graph. Pass when prerequisites are complete and every unit serves a gap.
6. **Project Design** — produce projects, deliverables, business value, coverage, and rubrics. Pass when every core competency has authentic evidence coverage.
7. **Roadmap** — produce phases, milestones, project links, capacity, buffers, and checkpoints. Pass when time, budget, and dependencies are feasible.
8. **Weekly Planner** — produce weekly outcome, capacity-bounded tasks, retrieval practice, and minimum delivery. Pass when load fits available time and produces evidence.
9. **Assessment** — produce scores, evidence links, observed behaviors, feedback, and next action. Pass only at the evidence threshold; otherwise choose a named rollback.
10. **Outcome Preparation** — produce route-specific minimum viable materials or performance. Pass when the target context can evaluate the learner's evidence.
11. **Continuous Optimization** — produce diagnosis, versioned changes, expected effect, and review date. Pass when the change is explainable and all affected artifacts are rechecked.

Do not silently skip a stage. When genuinely irrelevant, persist a stage record containing `state: not_applicable`, a nonempty `reason`, operational `source`, `confidence`, and `affected_downstream`. All five fields are required and machine-validated.

## Horizontal learning-support loop

Do not change the 11-stage order. A learner may invoke the problem-solving loop during execution by reporting confusion, inability to perform, a tool or environment error, an oversized task, a missed commitment, a capacity change, or a goal change. Load `problem-solving-engine.md` and `beginner-interaction.md`; do not force the learner through Discovery again when current context is sufficient.

The loop is `hear -> locate earliest blocker -> distinguish -> shrink -> define success -> try -> verify -> assess plan impact`. It returns to the active stage when resolved. Route `task` and `week` impact to Weekly Planner, `roadmap` impact to Roadmap and affected downstream gates, and `goal_system` impact to Goal Analysis and all affected downstream artifacts. The loop may persist a `learning-issue`, but it never becomes a twelfth stage and never advances a stage gate by itself.

For a horizontal support interaction, maintain the canonical `engine_result` internally or in the authorized learner workspace and show the beginner support card by default. If the user asks for structured state, return the same wrapper with `engine: problem-solving`; never invent a second wrapper.

## State transitions

Allow `not_started -> collecting -> draft -> validated -> active`. Use `needs_input` when missing information can materially change the decision; use `blocked` only for a substantive condition that prevents safe progress. Allow `active -> superseded -> archived` while retaining history.

Retain the stable artifact `id` across content revisions. Version identity is `(artifact_type, id, content_version)`: reject an exact duplicate tuple, allow the same `(artifact_type, id)` at different content versions, and permit at most one `status: active` record in that identity group. Singleton artifact types (`system-state`, `learner-profile`, `target-outcome`, `competency-model`, `curriculum-graph`, `learning-roadmap`, and `optimization-state`) additionally permit at most one active record across the entire type, regardless of ID. `active_versions` must uniquely cover every active singleton except `system-state` itself and select its one active record whose `content_version` equals the recorded value.

Build one resolved active-artifact view before any cross-artifact semantic check. Use only the unique active competency, curriculum, project, roadmap, weekly plan, evidence, assessment, and Domain Pack selection for current-state references. Validate historical and superseded artifacts only for schema, version identity, duplicate tuples, and the one-active invariant; never let a superseded competency or project satisfy a current reference.

When evidence is incomplete but risk is low, create a `draft` with explicit assumptions and a next validation action. Do not present it as validated.

## Persistent-state write safety

Before any write, compare the current active version and `updated_at`—or a content hash when either value is unavailable—with the values in the loaded snapshot. If the learner file was externally modified, stop automatic writes, preserve both states, report the conflict and changed fields, and request a merge decision. Never silently select or overwrite either version.

If validation identifies corrupted state, stop automatic writes and report the validation errors. Restore only the most recent valid version after identifying it deterministically; preserve the corrupt artifact and write a recovery trace containing the source version, restored version, validation evidence, time, reason, and affected artifacts. If no valid version exists, return `blocked` and request recovery input rather than synthesizing state.

## Multi-goal conflict

When goals compete for the same capacity, name exactly one primary goal, classify compatible work as a secondary goal, and place incompatible work under a deferred goal with a review condition. Do not stack multiple full-time routes into one roadmap; expose the trade-off and obtain the learner's priority decision before activating downstream plans.

## Engine return contract

Return every stage result in two synchronized layers: first, a concise natural-language explanation of the conclusion, evidence, uncertainty, and next action; second, structured state using this canonical wrapper. Do not omit the explanation or return prose without state.

```yaml
engine_result:
  engine: discovery | goal-analysis | gap-analysis | other-stage-engine
  run_id: unique-run-id
  status: draft | validated | active | needs_input | blocked | not_applicable
  summary: concise decision summary
  inputs_used: []
  decisions: []
  evidence_refs: []
  assumptions: []
  confidence: low | medium | high
  artifacts_written: []
  affected_downstream: []
  gate:
    passed: false
    missing: []
  next_action: single concrete action
```

Keep `gate.passed` false whenever `gate.missing` is non-empty. List only inputs actually consulted, evidence identifiers that exist, artifacts actually persisted, and downstream artifacts that require validation or recomputation.

## Rollback protocol

- On target change, return to Goal Analysis; create a new content version and recompute every item in `affected_downstream`.
- On constraint change, recheck Roadmap and Weekly Planner, then any downstream stage affected by feasibility.
- On assessment failure, return to the earliest causal Gap, Competency, Curriculum, Project, or Weekly Planner decision; do not automatically add advanced theory.
- On Domain Pack revision or staleness, recheck Gap, Competency, Curriculum, and Project decisions.
- On contradictory evidence, retain both sources, lower confidence, request the smallest discriminating assessment, and supersede only after resolution.

## Gate record

For every transition record: `stage`, `status`, `decision`, `source`, `confidence`, `assumptions`, `evidence_ids`, `affected_downstream`, `next_action`, and version timestamps. Never advance solely because a course or checklist was completed.
