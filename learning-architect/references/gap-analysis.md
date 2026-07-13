# Gap Analysis

Calculate the shortest evidence-responsible path from the learner's current behaviors to target competency behaviors.

## Baseline rules

For each competency record `current_level`, `target_level`, behavioral observations, evidence requirements, `source`, and `confidence`. Distinguish:

- verified performance: independently observable task or artifact evaluated against criteria;
- supported inference: indirect evidence with an explicit inference chain;
- self-report: useful for routing an assessment, never verified capability;
- unknown: no defensible baseline.

Never treat self-report, attendance, reading, watching, quiz completion, or course completion as verified L3+ evidence. Cap an unsupported provisional level below L3 and schedule a discriminating performance task. Lower confidence when evidence is old, assisted, narrow, or contradictory.

## Prioritization

1. Compute `level_gap = max(target_level - current_level, 0)` only after establishing the baseline class.
2. Score each gap using: `priority = level_gap * outcome_weight * dependency_leverage * evidence_risk * urgency`.
3. Raise `dependency_leverage` for prerequisites that unblock multiple downstream competencies or projects.
4. Raise `evidence_risk` when confidence is low or the target requires independent, production-like performance.
5. Defer gaps that do not serve the target outcome; do not inflate the curriculum for completeness.
6. Break ties by prerequisite order, then by the cheapest task that reduces uncertainty.

Do not collapse “knows,” “can follow,” “can complete with help,” and “can independently deliver” into one label. If project performance contradicts quiz results, prioritize the observed transfer gap and prescribe guided example, faded support, variant practice, debugging, reflection, then independent reassessment.

## Output contract

For each prioritized gap emit: `competency_id`, `current_level`, `target_level`, `level_gap`, `baseline_class`, `source`, `confidence`, `evidence_ids`, `priority`, `priority_factors`, `blocking_dependencies`, `required_evidence`, `next_validation`, and `affected_downstream`. Mark missing decision-critical evidence as `needs_input`; otherwise retain it as an explicit low-confidence hypothesis.

Return a concise natural-language explanation plus a structured `engine_result` conforming to the canonical wrapper in `workflow.md`. Set `engine: gap-analysis`; identify the competency-model artifact, cite only verified evidence identifiers in `evidence_refs`, and place missing discriminating evidence in `gate.missing`.
