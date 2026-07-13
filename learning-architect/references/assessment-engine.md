# Assessment Engine

## Purpose and evidence rules

The Assessment Engine makes Stage 9 capability decisions from authentic evidence, never from attendance, confidence, or content completion alone. It consumes the active competency model, project and six-dimension analytic rubric, assessment pattern, evidence records, target context, and current roadmap/plan versions. Missing, stale, inaccessible, or mismatched evidence cannot be scored as demonstrated.

Every assessment samples the behaviors relevant to the claimed level. Across the system, include checks that require the learner to:

1. complete a bounded task `independent` of repair guidance;
2. `explain` decisions and trade-offs;
3. `modify` the artifact when requirements change;
4. `debug` a controlled failure;
5. `deploy` or deliver in the target context; and
6. `teach` or review the work for another person.

Record task IDs, evidence IDs, evaluator, observed behaviors, rubric dimension scores, feedback, verification time, and the next action. Classify results as `understanding`, `guided`, `independent`, or `transfer`; do not infer a higher result from a weighted average alone.

## Thresholds and independence

Apply the project's analytic rubric exactly: `correctness`, `capability_behavior`, `reliability`, `responsible_practice`, `business_value`, and `technical_communication`, using its weights and observable performance bands. Each dimension declares `critical: true | false` and a named `passing_threshold: developing | proficient | strong`; `insufficient` can never be a passing threshold. A missing declaration, or a rubric where no dimension declares `critical: true`, is added to `gate.missing`, never guessed. Passing requires every critical dimension to meet or exceed its `passing_threshold` and the competency behavior to be directly observed. A strong aggregate score cannot hide an insufficient critical dimension. L4–L5, safety-sensitive, or externally consequential claims require an independent or external evaluator and reproducible evidence.

Use the Domain Pack assessment pattern appropriate to the competency and target. Contradictory evidence lowers confidence and triggers the smallest discriminating assessment while retaining both records. Feedback names the observed gap, its impact, and one executable correction.

## Decision and rollback

If the evidence threshold is met, advance only the verified competency and retain evidence links. Otherwise choose an explicit earliest causal rollback target: Gap Analysis for a wrong baseline, Competency Design for a wrong behavior/level, Curriculum Design for missing prerequisite or practice, Project Design for invalid evidence coverage/rubric, or Weekly Planner for insufficient scheduled practice. Do not automatically prescribe more advanced theory.

Return a natural-language explanation followed by the canonical `engine_result` from `workflow.md` with `engine: assessment`, enum confidence, assessment/evidence artifact IDs and versions, `gate.missing`, the named rollback in `decisions`, affected downstream artifacts, and one next action.
