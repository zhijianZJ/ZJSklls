# Assessment Engine

## Purpose and evidence rules

The Assessment Engine makes Stage 9 capability decisions from authentic evidence, never from attendance, confidence, or content completion alone. It consumes the active competency model, project and six-dimension analytic rubric, assessment pattern, evidence records, target context, and current roadmap/plan versions. Missing, stale, inaccessible, or mismatched evidence cannot be scored as demonstrated.

Every assessment accounts for all six canonical behaviors in typed `behavior_checks`, even when the claimed level makes one genuinely irrelevant. Include checks that require the learner to:

1. complete a bounded task `independent` of repair guidance;
2. `explain` decisions and trade-offs;
3. `modify` the artifact when requirements change;
4. `debug` a controlled failure;
5. `deploy` or deliver in the target context; and
6. `teach` or review the work for another person.

Record task IDs, evidence IDs, evaluator, typed observed behaviors, rubric dimension scores, feedback, verification time, and the next action. Every top-level and behavior-level evidence ID must resolve to an actual Evidence record in learner state. For each applicable behavior, at least one resolved record must contain that same canonical behavior with an observed state matching the `behavior_check.state`: `pass` matches `pass`, and `fail` matches `fail`. An applicable behavior requires evidence and state `pass` for the assessment gate to pass. Under `gate.passed: false` with decision `fail` or `needs_remediation`, a resolved matching `fail` observation is valid failure history and must not be rewritten as missing passing evidence. `independent` and `explain` are always applicable for any passing assessment. `modify`, `debug`, `deploy`, and `teach` may use `not_applicable` only with state `not_applicable`, no evidence IDs, and a specific nonempty decision-relevant reason. Classify results as `understanding`, `guided`, `independent`, or `transfer`; do not infer a higher result from a weighted average alone.

A resolved `learning-issue` is evidence that a bounded blocker was addressed, not proof that the related capability was independently demonstrated. Use its result observation to design or interpret the smallest authentic check. If the learner succeeded only after the Problem-Solving Engine supplied the decisive step, label that attempt guided and schedule a faded or independent repeat before advancing capability.

## Thresholds and independence

Apply the project's analytic rubric exactly: `correctness`, `capability_behavior`, `reliability`, `responsible_practice`, `business_value`, and `technical_communication`, using its weights and observable performance bands. Each dimension declares `critical: true | false` and a named `passing_threshold: developing | proficient | strong`; `insufficient` can never be a passing threshold. A missing declaration, or a rubric where no dimension declares `critical: true`, is added to `gate.missing`, never guessed. Passing requires every critical dimension to meet or exceed its `passing_threshold` and the competency behavior to be directly observed. A strong aggregate score cannot hide an insufficient critical dimension. L4–L5, safety-sensitive, or externally consequential claims require an independent or external evaluator and reproducible evidence.

Use the Domain Pack assessment pattern appropriate to the competency and target. Contradictory evidence lowers confidence and triggers the smallest discriminating assessment while retaining both records. Feedback names the observed gap, its impact, and one executable correction.

## Decision and rollback

The gate fails and lists the behavior in `gate.missing` when any of the six is absent, an evidence ID is unresolved, resolved evidence lacks an observation matching the behavior check's state, an applicable behavior lacks evidence, or an applicable behavior has state `fail`. Enforce the decision invariant in both directions: `decision: pass` if and only if `gate.passed: true`; `decision: fail` or `needs_remediation` requires `gate.passed: false` and correlated `gate.missing`. A passing assessment can never mark all six behaviors `not_applicable`. If the evidence threshold is met, advance only the verified competency and retain evidence links. Otherwise choose an explicit earliest causal rollback target: Gap Analysis for a wrong baseline, Competency Design for a wrong behavior/level, Curriculum Design for missing prerequisite or practice, Project Design for invalid evidence coverage/rubric, or Weekly Planner for insufficient scheduled practice. Do not automatically prescribe more advanced theory.

Return a natural-language explanation followed by the canonical `engine_result` from `workflow.md` with `engine: assessment`, enum confidence, assessment/evidence artifact IDs and versions, `gate.missing`, the named rollback in `decisions`, affected downstream artifacts, and one next action.
