# ZJSkills Full Usage Guide

ZJSkills manages growth as a versioned decision system. Define a verifiable outcome first, design capabilities and authentic projects next, and only then schedule knowledge and time. Learning activity supports a capability judgment only when it produces observable behavior and resolved evidence.

## Complete workflow

Stages run in order. Prose output alone never passes a gate. A genuinely irrelevant stage must be recorded as `not_applicable` with a reason, source, confidence, and affected downstream items.

| Stage | Decision purpose | Minimum input | Primary artifact | Gate | Continuation prompt |
|---|---|---|---|---|---|
| 1. Discovery | Establish the learner and constraint boundary | target signal, background, capacity, hard constraints | learner profile, SWOT, unknowns | decision-critical data has source and confidence | “Ask the one question most likely to change the route.” |
| 2. Goal Analysis | Turn intent into a timed, verifiable outcome | target, deadline, success evidence, constraints | target outcome, milestones, key results | verifiable and not silently incompatible with constraints | “Rewrite my target as an observable outcome.” |
| 3. Gap Analysis | Compare current evidence with target behavior | target capabilities, current evidence | current/target levels, prioritized gaps | baselines are sourced and inference is separate | “Prioritize the causal gaps from current evidence.” |
| 4. Competency Design | Define what the learner must be able to do | prioritized gaps, target context | nodes, L0–L5 behaviors, weights, evidence needs | every core node has a target level | “Build an observable competency tree, not a topic list.” |
| 5. Curriculum Design | Build the smallest dependency-safe learning graph | gaps and prerequisites | learning units, acyclic graph, practice | every unit serves a gap and prerequisites are complete | “Design the minimum dependency graph.” |
| 6. Project Design | Produce authentic capability evidence | competency model, context, constraints | project briefs, deliverables, coverage, rubrics | every core competency has authentic coverage | “Design a progressive project ladder with gates.” |
| 7. Roadmap | Sequence feasible phases with buffers | project dependencies, capacity, budget, deadline | phases, milestones, checkpoints | time, cost, and dependencies are feasible | “Show conservative, baseline, and minimum-viable routes.” |
| 8. Weekly Planner | Convert the roadmap into a bounded commitment | current phase, real available hours, and risks | weekly outcome, tasks, retrieval, minimum delivery | load fits capacity and produces evidence | “Build this week around the minimum delivery.” |
| 9. Assessment | Judge independent performance | artifacts, runtime results, rubric | scores, observed behavior, evidence, next action | every critical dimension meets its evidence threshold | “Score the evidence and name the earliest causal gap.” |
| 10. Outcome Preparation | Make verified capability evaluable in context | verified evidence and target route | portfolio, work sample, demo, or handoff | target evaluators can verify relevant evidence | “Prepare the target materials using verified evidence only.” |
| 11. Continuous Optimization | Adapt through explainable version changes | progress, quality, feedback, triggers | diagnosis, version change, expected effect, review date | cause is explained and affected artifacts rechecked | “Update the system from this week’s evidence and keep history.” |

When goals compete for the same capacity, name one primary goal. Compatible work may be secondary; incompatible work is deferred with a review condition.

## Artifacts and structured state

Each stage returns two synchronized layers:

1. concise prose stating the decision, decisive evidence, uncertainty, and one next action;
2. the canonical `engine_result` recording inputs, decisions, evidence, assumptions, confidence, writes, downstream effects, gate, and next action.

```yaml
engine_result:
  engine: goal-analysis
  run_id: run-2026-001
  status: needs_input
  summary: Direction is clear, but deadline and success evidence are missing
  inputs_used: [learner-statement-001]
  decisions: []
  evidence_refs: []
  assumptions: []
  confidence: low
  artifacts_written: []
  affected_downstream: [gap-analysis]
  gate:
    passed: false
    missing: [deadline, success-evidence]
  next_action: Confirm the date and artifact that would demonstrate success
```

Whenever `gate.missing` is non-empty, `gate.passed` remains `false`. Use `needs_input` for an unanswered question that can materially change the decision. Reserve `blocked` for a substantive obstacle to safe progress. Low-risk work may become a `draft` only with explicit assumptions and a validation action.

Persistent artifacts retain a stable `id` and increment `content_version`. Material changes create a new version; old versions become `superseded` or archived instead of being overwritten. Resume from the earliest failed gate without rebuilding validated upstream decisions.

The Skill assumes no global or automatic storage directory. To continue across tasks, name a learner workspace you authorize and ask it to persist the entry state as `system-state.yaml` in that directory; other schema-backed artifacts live in the same workspace or its subdirectories. If the current tool cannot write files, state remains in the conversation and `artifacts_written` must be empty. In a new task, provide the workspace path again and ask the Skill to read and validate `system-state.yaml` first.

Before writing, compare the loaded active version and timestamp or content hash with the file on disk. On an external modification, stop automatic overwrite, preserve both states, and request a merge decision. Preserve corrupt state and a recovery trace; if no valid version can be identified deterministically, return `blocked` instead of inventing one.

## Evidence and capability judgment

Important claims use `epistemic_class` independently from operational source and confidence:

- `fact`: verifiable through a stable external source;
- `self-report`: what the learner says about themselves;
- `evidence`: artifact, code, test, review, or observed performance;
- `inference`: a conclusion derived from inputs;
- `assumption`: a temporary premise that enables a draft and still needs validation.

Self-report can form a hypothesis, but cannot by itself prove independent delivery. Contradictory evidence remains visible, lowers confidence, and triggers the smallest discriminating assessment.

Watching videos, reading books, attending programs, checking boxes, earning certificates, and feeling confident are activity evidence. Capability evidence asks whether the learner can:

- complete a bounded real task independently;
- explain trade-offs and limits;
- modify the solution for changed requirements;
- debug failures;
- deploy or deliver with rollback evidence;
- teach or review the work.

Assessment distinguishes `understanding`, `guided`, `independent`, and `transfer` and cites resolved evidence IDs. A failed project should roll back to its earliest causal gap, not automatically add more advanced theory.

## Versioning, review, and optimization

Replanning triggers include target changes; altered time, budget, tools, or access; persistently low completion; weak retention or transfer; project, interview, or delivery feedback; and stale technical, market, or regulatory evidence.

Record stable ID, prior and new version, trigger, reason, evidence, assumptions, confidence, rollback target, timestamps, and `affected_downstream`. Revalidate dependencies and gates before activation. Define an observation window and success measure so one noisy result does not cause constant route changes.

Useful review inputs include planned versus actual hours, minimum delivery status, retrieval performance, project rubric results, failure category, external feedback, and constraint changes. Optimize transfer and delivery probability, not content completion.

## Failure and safety boundaries

- Feasibility: expose conflicts among target, deadline, capacity, budget, and environment; offer trade-offs or a minimum viable outcome without promising external results.
- Privacy: collect the minimum decision-relevant information and redact portfolios, resumes, feedback, and enterprise data. Never store passwords, API keys, identity documents, or unauthorized data.
- High-risk decisions: hiring policy, law, health, finance, production safety, and current-market claims need dated sources, limitations, and appropriate qualified review.
- External evidence: record access date and scope. When sources are stale, contradictory, or too weak, return `needs_input` or a validation action.
- Tool honesty: never claim a search, deployment, or write that did not occur. `artifacts_written` contains only persisted files.
- Public claims: do not write “mastered,” “independent delivery,” or “job ready” into public materials without resolved evidence.
- Outcomes: the Skill cannot guarantee employment, promotion, revenue, venture success, project acceptance, or another party’s decision.

Maintainers can run:

```bash
python3 learning-architect/scripts/validate_learning_system.py \
  --skill-root learning-architect \
  --learner-dir tests/learning-architect/fixtures/valid-learner
python3 -m unittest tests/learning-architect/test_validate_learning_system.py -q
```
