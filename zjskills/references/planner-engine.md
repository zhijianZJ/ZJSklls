# Weekly Planner Engine

## Purpose

The Weekly Planner Engine converts the active roadmap into one capacity-bounded Stage 8 commitment that produces evidence. It consumes the learner constraints, roadmap phase and milestone, curriculum dependencies, project deliverables, prior assessment evidence, and active optimization state.

## Load calculation and selection

Calculate the week from explicit effort values:

```text
usable_capacity = capacity_hours * (1 - buffer_ratio)
planned_load = task_hours + retrieval_practice_hours + project_work_hours + review_hours
```

Include setup and coordination inside task estimates. Require `planned_load <= usable_capacity`; the reserved remainder is recovery capacity, not an invitation to add work. Select only tasks whose prerequisites are met. Prefer one evidence-producing weekly outcome, retrieval practice for previously learned material, spaced review at evidence-informed intervals, and project work that advances the next milestone.

Every task has an ID, outcome link, competency IDs, estimate, scheduled time block, dependency, evidence output, and completion criterion. Every plan identifies a `minimum_delivery`: the smallest artifact that still creates useful evidence if capacity drops. When overloaded, remove optional breadth, reduce polish, or defer a non-critical task before changing the outcome. Do not delete retrieval needed for a weak or decaying capability. Record the risk, early warning, mitigation, and the condition that activates minimum delivery.

## Review and gate

At week end, compare planned versus actual hours, completed evidence, assessment feedback, obstacles, and learner-reported sustainability. Do not treat time spent or content completion as capability evidence. Carry an incomplete task forward only after diagnosing the cause and rechecking dependencies and capacity; repeated overload triggers Roadmap review.

When the Problem-Solving Engine reports `plan_impact.level: task`, change only the affected task: split, scaffold, replace, reschedule, or reduce it while preserving the weekly outcome and evidence intent. When it reports `week`, recalculate usable capacity, protect minimum delivery and necessary retrieval, and create a new weekly-plan content version. One missed task or one difficult session does not justify a roadmap change; use dated repeated evidence or a confirmed constraint change before escalating.

Pass when the outcome is testable, all work fits usable capacity, project work and retrieval practice produce named evidence, `minimum_delivery` is viable, risks have actions, and the review is scheduled. Return a natural-language explanation plus the canonical `engine_result` from `workflow.md` with `engine: weekly-planner`, enum confidence, the plan artifact/version, affected project and assessment artifacts, gate details, and one next action.
