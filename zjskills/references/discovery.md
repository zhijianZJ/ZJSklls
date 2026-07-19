# Progressive Discovery

Discover only information that can change the next learning-system decision. Use `assets/question-banks/discovery.yaml`; do not administer it as a fixed questionnaire.

## Question routing

1. Identify the pending decision and its competing routes.
2. List unknowns that could change the selected route, its feasibility, sequence, evidence standard, or learner safety.
3. Rank candidate questions by expected information gain: `decision_change_probability * decision_impact * uncertainty_reduction`, discounted by response burden and sensitivity.
4. Start with **8–12** high-information, non-duplicative questions that cover the decision-critical learner, goal, baseline, motivation, and constraint unknowns.
5. After the first response, ask adaptive follow-up questions in small batches, reranking by the remaining information gain.
6. Skip questions already answered by current, credible evidence. Ask sensitive questions only with consent and always permit “prefer not to answer.”
7. Stop when remaining answers would not materially change the current decision. Record them in `unknowns` rather than inventing precision.

If the learner refuses discovery, request only target outcome, present baseline, deadline, and weekly capacity when they are decision-critical. Explicitly offer a provisional route when safe; label it `draft`, list its assumptions with `source` and `confidence`, and name the validation action before any schedule or resource catalog. If even a provisional route is unsafe, state the specific missing decision that prevents it.

## Evidence-labeled learner profile

Populate the learner-profile contract: `personal`, `experience`, `learning_preferences`, `motivation`, `constraints`, `swot`, and `unknowns`. For every material item include or link:

- `value`: the claim used by the system;
- `epistemic_class`: fact, self-report, evidence, inference, or assumption;
- `source`: the operational origin—user, assessment, project, mentor, employer, market-research, or inference;
- `confidence`: `low`, `medium`, or `high`;
- `evidence_ids`: supporting artifacts when available;
- `decision_impact`: what changes if the claim is wrong.

Never convert self-report into verified competence. Resolve contradictions with a small task or evidence request, not by choosing the more convenient statement.

## SWOT output

Generate an evidence-labeled SWOT with four explicit keys:

- `Strength`: internal assets already supported by evidence or clearly marked self-report.
- `Weakness`: internal gaps or habits that impede the target; describe behavior, never moral character.
- `Opportunity`: external or contextual openings the learner can realistically use.
- `Risk`: internal or external conditions that threaten feasibility, safety, persistence, or evidence quality.

Attach `epistemic_class`, `source`, `confidence`, `evidence_ids`, and a decision implication to every SWOT item. End with decision-critical unknowns and the next highest-information question or validation task.

Return a concise natural-language explanation plus a structured `engine_result` conforming to the canonical wrapper in `workflow.md`. Set `engine: discovery`; write or identify the learner-profile artifact, reflect unresolved critical unknowns in `gate.missing`, and keep `gate.passed` false until the Discovery gate is satisfied.
