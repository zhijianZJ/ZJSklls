# Continuous Optimization Engine

## Purpose and triggers

The Continuous Optimization Engine turns Stage 11 review evidence into explainable, reversible changes. Create an optimization event for each trigger type:

- `scheduled`: a dated weekly, milestone, or quarterly review;
- `behavioral`: repeated mismatch between planned and observed performance or sustainability;
- `quality`: rubric regression, defects, weak evidence, or stakeholder rejection;
- `goal_change`: target outcome, deadline, or success evidence changes; and
- `domain_update`: the Domain Pack is revised, stale, or contradicted by dated market/technical evidence.

An event records trigger, evidence IDs, diagnosis, assumptions, confidence, proposed changes, affected artifacts, expected measurable effect, rollback target, owner, and `review_at`. Diagnosis must distinguish capacity, prerequisite, practice, project/evidence design, target, and domain causes; never attribute a system failure to learner character.

## Versioned change protocol

Never overwrite active history. Copy the affected artifact under the same stable ID, increment `content_version`, record the prior version, change rationale, evidence IDs, timestamp, and migration map, validate the candidate, then transition the old version `active -> superseded -> archived` only after activation. Retain assessment and optimization events as immutable audit records. If validation fails, keep the prior active version and mark the candidate draft or rejected.

Explicit rollback targets are:

- `goal_change` -> Goal Analysis, then recompute all `affected_downstream`;
- temporary or one-week capacity/constraint evidence with `week` impact -> Weekly Planner only; persistent or recurring evidence that changes phase feasibility with `roadmap` impact -> Roadmap, Weekly Planner, and affected downstream gates;
- assessment failure -> earliest causal Gap, Competency, Curriculum, Project, or Weekly Planner decision;
- `domain_update` -> Gap, Competency, Curriculum, and Project decisions;
- packaging-only outcome failure -> Outcome Preparation.

Accept plan-impact decisions from the Problem-Solving Engine without automatically treating every issue as an optimization event. `none` closes or continues the issue without an artifact change; `task` and `week` create the smallest Weekly Planner revision; `roadmap` rechecks Roadmap and named downstream gates; `goal_system` is a `goal_change` event that must return to Goal Analysis. Escalate a recurring learning problem only when dated attempts show that the smaller change did not remove the diagnosed cause.

Revalidate all dependencies, evidence coverage, load, and gates touched by a change. Compare the expected effect at `review_at`; keep, revise, or reverse the candidate based on evidence rather than sunk cost.

Return a natural-language explanation followed by the canonical `engine_result` from `workflow.md` with `engine: continuous-optimization`, enum confidence, the optimization event and new artifact versions, explicit rollback/affected downstream decisions, gate details, and one next action.
