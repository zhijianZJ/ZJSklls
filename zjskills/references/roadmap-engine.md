# Roadmap Engine

## Purpose and inputs

The Roadmap Engine turns the learner profile, target outcome, competency gaps, dependency-safe curriculum, and projects into a feasible Stage 7 sequence. Consult only current, non-superseded artifacts and retain their IDs and versions in `inputs_used`. Read the learner's dated budget amount, currency, budget source, and any per-resource or employer-funding limits alongside time constraints. A roadmap is a capacity and budget commitment, not a calendar-shaped course list.

## Capacity and buffer calculation

For each week in a phase, then for the complete phase, calculate values with matching time units:

```text
weekly_available_hours[week] = min(learner.constraints.weekly_hours, dated_capacity_limit[week])
weekly_buffer_hours[week] = weekly_available_hours[week] * buffer_ratio
weekly_delivery_hours[week] = weekly_available_hours[week] - weekly_buffer_hours[week]
weekly_planned_hours[week] = curriculum + project + retrieval/review + assessment hours
phase_delivery_hours = sum(weekly_delivery_hours[week] for week in phase)
phase_planned_hours = sum(weekly_planned_hours[week] for week in phase)
total_estimated_cost = sum(phase.estimated_cost for phase in phases)
```

Use a `buffer_ratio` of 0.20 by default. Raise it for volatile work schedules, unfamiliar delivery environments, or a milestone with external dependencies; record the evidence and assumption. Never count the buffer as assignable task time, and never solve overload by silently increasing learner capacity. Require `weekly_planned_hours[week] <= weekly_delivery_hours[week]` for every week and `phase_planned_hours <= phase_delivery_hours` for the phase. Record every phase's `estimated_cost` and `currency`; normalize only with a sourced exchange rate and dated assumption. Require matching currency and `total_estimated_cost <= budget.amount` before the budget gate passes.

Sequence the smallest prerequisite closure first. Place project milestones after their required curriculum nodes and include evidence checkpoints before a dependent milestone begins. For each milestone window, calculate `milestone_buffer_hours = sum(weekly_buffer_hours[week] for week in milestone_window)` and persist `buffer_start_at` and `buffer_end_at`; scheduled milestone work must finish by `buffer_start_at`, while the buffer covers recovery through `buffer_end_at`. For an externally fixed deadline, require a nonzero buffer sized from the evidenced recovery or dependency-delay estimate. If the critical path plus this buffer cannot fit, reduce scope to a named `minimum_delivery`, move the deadline with learner agreement, or return `needs_input`/`blocked` with the violated constraint.

## Roadmap artifact and gate

Write a `learning-roadmap` artifact with stable phase IDs, outcomes, milestones, project IDs, `weekly_capacity_hours`, and `buffer_ratio`. Each milestone records its deliverable, evidence threshold, due date, prerequisites, checkpoint, minimum delivery, and rollback target. Recompute affected dates when capacity, goal, competency, curriculum, or project versions change; preserve the prior roadmap as `superseded`.

Pass only when dependencies are valid, every phase fits capacity after its buffer, every phase cost is included, total cost fits the sourced budget, every core competency reaches authentic evidence, milestone buffers protect external commitments, and assumptions are visible. A missing budget/currency/cost or an over-budget total appears in `gate.missing`. A failed feasibility check rolls back to the earliest causal target, curriculum, project, or roadmap decision rather than compressing practice.

Return a concise natural-language explanation followed by the canonical `engine_result` from `workflow.md` with `engine: roadmap`, enum `confidence: low | medium | high`, roadmap artifact IDs and versions, affected weekly plans and assessments, gate details, and one concrete next action.
