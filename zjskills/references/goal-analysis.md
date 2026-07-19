# Goal Analysis

Convert an aspiration into a feasible, evidence-verifiable outcome. Do not recommend a curriculum until the minimum goal contract is usable.

## Synthesis procedure

1. Apply **SMART** to test specificity, measurability, feasibility under current constraints, relevance to the learner, and deadline.
2. Apply **OKR** to preserve the directional objective while defining a small set of observable key results. Do not confuse learning activity with a result.
3. Apply **Backward Design** from outcome evidence to milestones, competencies, project proof, dependencies, and weekly action.
4. Surface contradictions among scope, baseline, deadline, weekly capacity, budget, and evidence standard. Never promise employment, promotion, revenue, or other external decisions.
5. Offer explicit trade-offs: reduce outcome scope, extend time, increase capacity/resources, or accept a labeled low-confidence experiment.

## Required goal chain

Emit this exact decision chain and keep every link traceable:

`Target Outcome -> Outcome Evidence -> Milestones -> Competency Targets -> Project Evidence -> Curriculum Dependencies -> Weekly Actions`

Populate the target-outcome contract with `outcome_type`, `primary_goal`, `deadline`, `success_evidence`, and `key_results`, plus common metadata including `source` and `confidence`. Each key result must name a measure, threshold, evidence source, and review date.

## Change control

If the target changes, do not append content to the old plan. Mark the prior target superseded, create a new content version, record the change reason, and enumerate `affected_downstream`. Every goal-change response must show a compact change record with `prior_version`, `candidate_version`, `trigger: goal_change`, `reason`, and `affected_downstream`. A version value must be an actual stable identifier or the exact literal `unknown`; `pending`, `TBD`, and other placeholders are prohibited. If the response proposes a candidate in chat, give it a deterministic draft identifier such as `target-outcome-v2-draft`, while keeping `artifacts_written` empty unless that artifact was actually persisted. If the prior identifier is unavailable, use `prior_version: unknown` and request it rather than inventing one. Return control to Goal Analysis and recompute those artifacts.

Use `needs_input` only when a missing answer blocks a materially safe goal decision. Otherwise issue a provisional `draft`, list assumptions, and name the smallest next validation step.

Return a concise natural-language explanation plus a structured `engine_result` conforming to the canonical wrapper in `workflow.md`. Set `engine: goal-analysis`; identify the target-outcome artifact, include every assumption affecting feasibility, and report unmet goal conditions in `gate.missing`.
