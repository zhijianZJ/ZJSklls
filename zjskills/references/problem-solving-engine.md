# Learning Problem-Solving Engine

## Purpose

Use this engine when a learner is stuck during execution, cannot describe what is wrong, encounters a tool failure, misses planned work, or reports a change that may affect the plan. It is a horizontal support loop, not a new numbered workflow stage. Its job is to find the earliest actionable blocker, produce one observable next step, verify the result, and escalate only the smallest affected part of the learning system.

Do not diagnose intelligence, personality, diligence, willpower, or a fixed learning style. A cause remains a hypothesis until an observation, artifact, error message, task attempt, or constraint report distinguishes it from alternatives.

## Routing modes

Choose exactly one mode from current evidence:

- `direct_action`: the problem is bounded, low-risk, and sufficiently clear. Give one action, one success signal, and one fallback without asking a preliminary question.
- `guided_diagnosis`: two or more causes remain plausible, evidence is missing, the learner cannot locate the blocker, or the answer could materially change the plan. Ask one decision-changing question, then wait for the answer before prescribing a sequence.
- `safety_handoff`: the issue requires medical, mental-health, legal, financial, security, production-safety, or other qualified review. State the learning-system boundary, suggest the appropriate human or professional support, and preserve any safe learning action that remains in scope.

Do not choose `direct_action` merely to appear fast. Do not choose `guided_diagnosis` when a safe one-step check can resolve the uncertainty.

## Issue types

Classify the current symptom with one primary type and optional secondary types:

| Type | Observable symptom | First distinction |
|---|---|---|
| `knowledge_confusion` | The learner cannot explain a term, relationship, or example | Which exact sentence, term, or comparison first stopped making sense? |
| `practice_transfer` | The learner can explain but cannot perform | What is the first step they cannot complete without guidance? |
| `starting_ambiguity` | The learner does not know where to begin | What smallest input and output would form a complete loop? |
| `prerequisite_gap` | The current task assumes an unverified earlier behavior | Which required behavior is absent in a small prerequisite check? |
| `tool_environment` | Error, setup, access, authentication, dependency, or runtime failure | What is the exact message and the last action before it, with secrets removed? |
| `task_overreach` | Too many components, unclear boundaries, or excessive difficulty | Which smaller slice preserves useful evidence? |
| `resource_mismatch` | The format, language, accessibility, or level blocks progress | Can the same capability be practiced through a more accessible representation? |
| `capacity_change` | Available time, energy, budget, equipment, or support changed | Is the change temporary, recurring, or permanent, and what capacity remains reliable? |
| `goal_change` | Target outcome, deadline, success evidence, or route changed | What new observable result replaces the prior result? |

Retain the learner's own words separately from the issue type. The label organizes decisions; it does not replace what the learner reported.

## Support loop

1. **Hear** — capture `user_words`, current task or goal, the observed symptom, and available evidence. Restate the problem in one plain sentence so the learner can correct it.
2. **Locate** — identify the earliest point at which the learner could no longer continue independently. Prefer an exact step, artifact, error, or constraint over a broad topic label.
3. **Distinguish** — list no more than three plausible causes. If one low-cost check separates them, use it. Otherwise choose `guided_diagnosis` and ask one decision-changing question.
4. **Shrink** — define one action that can be completed now or in a short bounded session. Reduce scope, guidance, or representation without removing the target behavior being tested.
5. **Signal** — define an observable `success_signal`; “understand,” “learn,” “be familiar with,” or time spent alone are not success signals.
6. **Fallback** — state one `fallback_action` that gathers new evidence or uses a smaller step if the first action fails. Never repeat the same explanation unchanged.
7. **Verify** — record what happened, whether the issue is `open`, `testing`, `resolved`, or `escalated`, and any evidence IDs. Issue resolution is not automatically capability evidence.
8. **Replan minimally** — select one plan-impact level and route only the affected artifacts for recheck.

Do not stop at an explanation. Do not output an unranked list of ten possible fixes. Do not give multiple hours of study before the smallest blocker is verified.

## Plan-impact decision

Choose exactly one level:

- `none`: the issue can be resolved without changing an active artifact.
- `task`: split, replace, reschedule, scaffold, or reduce the current task while preserving the weekly outcome.
- `week`: reliable capacity, sustainability, dependencies, or multiple tasks changed; regenerate the weekly plan and minimum delivery.
- `roadmap`: a persistent capacity shift, prerequisite error, project sequencing problem, or repeated cross-week failure changes phase feasibility; recheck Roadmap and affected downstream gates.
- `goal_system`: the target result, deadline, success evidence, or career/business route changed; roll back to `goal-analysis` and recompute all affected downstream artifacts.

Apply the smallest justified level. A single missed task or first failure is insufficient evidence for `roadmap`. Escalate recurring issues only when dated observations show the current level did not remove the causal blocker. A `goal_system` issue must name `rollback_target: goal-analysis`; it is never handled as a small weekly edit.

## Common one-step patterns

- Concept confusion: ask the learner to distinguish two concrete examples, then explain the rule in their own words.
- Practice-transfer gap: provide a bounded input and ask for only the first independent transformation or decision.
- Tool error: request the exact sanitized message and last action, then check one likely boundary at a time. Never request API keys, passwords, tokens, or private data.
- Oversized project: reduce it to one user, one problem, one input, one output, and one acceptance check.
- Missed plan: identify the earliest obstacle and whether it was one-off or recurring before carrying tasks forward.
- Capacity change: calculate reliable remaining capacity and protect minimum delivery before adding or reshuffling work.

## Persistence and return contract

Persist a `learning-issue` artifact only when a writable learner workspace is authorized and cross-turn tracking adds value. Preserve the stable issue ID across revisions, increment `content_version`, and never claim a write that did not occur.

Return a plain-language support card following `beginner-interaction.md`. Maintain the canonical `engine_result` from `workflow.md` with `engine: problem-solving`, the selected routing mode and issue type in `decisions`, evidence used, assumptions, affected downstream artifacts, gate details, and one next action. Because this is a horizontal support interaction rather than a numbered stage result, keep structured state internal or persisted by default; display it only when the learner requests technical detail or the host requires it.
