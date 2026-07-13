# Outcome Preparation Engine

## Purpose

The Outcome Preparation Engine packages verified evidence for Stage 10 in the context where the learner must be evaluated. It consumes the target outcome, competency results, project artifacts, evidence, rubrics, and audience constraints. It never inflates claims beyond verified evidence and never exposes confidential material; redact or replace sensitive artifacts while preserving evaluability.

## Four routes

Choose one primary route and record any secondary route explicitly:

- `employment`: minimum viable materials are explicit JD matching from requirements to verified evidence, résumé/profile claims linked to evidence, one portfolio case, a rehearsed work sample, an HR interview evidence narrative, and an offer analysis covering role scope, growth, compensation, constraints, and decision criteria. The evaluator must be able to test independent delivery, explanation of trade-offs, debugging of failures, and accurate statement of evidence limits.
- `entrepreneurship`: minimum viable materials are a named customer problem, validated offer hypothesis, working demonstration, delivery scope, value/risk measures, one bounded acquisition experiment with conversion evidence, basic unit economics with assumptions, and one credible customer-validation record. Separate demand evidence from learner optimism.
- `promotion`: minimum viable materials are the target responsibility/level, verified before-and-after business evidence, stakeholder-ready case, expanded-scope demonstration, and a specific advancement conversation plan.
- `project_delivery`: minimum viable materials are the accepted brief, reproducible deliverables, rubric results, deployment or handover guide, operational risks and rollback, stakeholder acceptance evidence, and an evidence-based retrospective covering failures, decisions, and next changes.

For every route define audience, decision, claim-to-evidence map, required artifact, rehearsal or validation activity, success threshold, due date, and gap. Prefer the smallest complete package that the target evaluator can act on. A polished artifact with no evidence link does not pass.

## Gate and rollback

Pass when every material claim resolves to current evidence, the package meets route-specific minimums, confidentiality is protected, and a realistic target-context evaluation has passed. Missing capability evidence rolls back to Assessment; invalid project coverage to Project Design; route/goal mismatch to Goal Analysis; packaging-only gaps remain in Outcome Preparation.

Return a natural-language explanation plus the canonical `engine_result` from `workflow.md` with `engine: outcome-preparation`, enum confidence, route and package decisions, evidence refs, artifact IDs/versions, affected downstream optimization artifacts, gate details, and one next action.
