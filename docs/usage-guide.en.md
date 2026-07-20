# ZJSkills Full Usage Guide

[简体中文](usage-guide.md)

ZJSkills 3.0 is a lightweight, AI-first career diagnosis Skill. It reads the current conversation, selects one mode, returns a compact result, and ends with the single most useful action. Users do not need internal terminology or a fixed intake sequence.

## How the three modes are selected

Each request uses exactly one mode:

| Mode | When it applies | Default result |
| --- | --- | --- |
| Career diagnosis | Direction, fit, feasibility, realistic expectations, or the current problem is unresolved | One-page diagnosis and one minimum validation action |
| Learning route | The direction is sufficiently clear, or the user explicitly requests a route | At most three stages, evidence projects, and one action for this week |
| Learning help | Concept confusion, an action gap, project-start difficulty, an error, missed work, a changed goal, or supplied material | One action, success signal, fallback check, and route impact |

Reuse goals, experience, constraints, conclusions, and feedback already in the conversation. Ask no question when the evidence supports a useful next step. Ask only one decisive question when one missing fact could change the judgment or action. Do not launch a fixed questionnaire or predeclare a compulsory chain of later steps.

## Evidence categories and judgment boundaries

Separate three layers in every important judgment:

- **Known facts:** the user's stated situation and observable results;
- **Inference:** a judgment supported by named facts or evidence;
- **Uncertainty:** missing, conflicting, or unvalidated information that may change the conclusion.

Career direction uses five evidence dimensions: the actual desired result; current work and project experience; time, budget, equipment, language, and learning conditions; observed response to coding, product, content, process, or workplace tasks; and the result of a minimum experience task.

Interest, confidence, education, certificates, and content exposure may inform a hypothesis but cannot independently prove capability, independent delivery, or job readiness. A diagnosis uses one of four levels: stronger fit, worth testing with a named risk, do not invest heavily yet, or insufficient evidence—validate first.

## Five visible AI directions

| Direction | Work object | Strong evidence | Common false positive | Primary risk |
| --- | --- | --- | --- | --- |
| AI Agent Development | Model-, API-, tool-, and workflow-based systems | Independently builds, inspects, debugs, evaluates, and delivers a bounded Agent or automation | A copied demo runs once | Weak software fundamentals make failures opaque and delivery unreliable |
| Vibe Coding / AI Application Building | User-facing software built with AI assistance | Understands, changes, tests, debugs, and deploys assisted code | Generated code or a polished screen alone | Speed hides correctness, security, and maintenance gaps |
| AI Product Management | User and business problems translated into testable AI decisions | Defines capability boundaries, failure cases, a prototype, metrics, and acceptance criteria | Feature ideas or prompt lists alone | Probabilistic model behavior is treated as deterministic |
| AI Operations | Content/Growth or Business Efficiency | Produces a measurable result and explains AI's causal contribution | Content volume, impressions, tool count, or automation count alone | Quantity displaces audience response, business value, or process safety |
| AI Tools and Workplace Application | Real role-specific deliverables and workflows | Repeatable improvement in quality, time, verification, or collaboration | Tool familiarity or one unverified draft | A cross-role capability is mistaken for a standalone career |

## Six minimum experience tasks

When evidence is weak or two directions remain plausible, use the smallest real task that separates them:

1. **Agent:** complete a bounded model/API task and diagnose one induced failure;
2. **Vibe Coding:** build a small tool, then implement and verify one changed requirement;
3. **AI Product:** specify one AI feature with limitations, failure cases, and acceptance criteria;
4. **Content/Growth Operations:** complete one research-to-distribution loop and review the observed result;
5. **Business Efficiency Operations:** map one real process and validate one bounded automation point with its user;
6. **AI Tools:** redo one real work deliverable and compare before/after quality or time.

The evidence is the observed result: what worked, what failed, what changed, and what the user can explain. One task is not a lifelong fit verdict, but it is more useful than a self-rating.

## A learning route of at most three stages

When the direction is clear, organize the route in this order:

1. **Target:** the desired result and observable evidence;
2. **Current starting point:** demonstrated capability, experience, constraints, and important unknowns;
3. **Stage 1:** the first missing capability and its proving deliverable;
4. **Stage 2:** the next capability and deliverable, only when needed;
5. **Stage 3:** a bounded target-level deliverable, only when earlier stages do not reach the target;
6. **Evidence project for each stage:** realistic work, its observable result, and acceptance check;
7. **Only this week's action:** one capacity-aware action and completion signal;
8. **Biggest assumption or constraint:** the one factor most likely to change the route.

Define outcomes, deliverables, and evidence projects before resources. Explain the job each resource serves and keep it replaceable. Content completion alone is not evidence. Do not create a daily plan unless asked.

## Learning-help output

Learning help locates the smallest current blocker and returns, in order:

1. where the user is stuck;
2. the most likely cause, with uncertainty labeled;
3. one action to do first;
4. an observable success signal;
5. one fallback check if it fails;
6. whether the route is unchanged, the current task changes, the stage changes, or the direction must be reconsidered after a changed goal.

For an error, use the exact message, reproduction steps, input, output, and environment already supplied; ask only for the decisive missing item. For missed work, distinguish a one-off interruption from a persistent capacity mismatch. For a changed goal, identify whether the target or only the current task changed. One failure does not automatically invalidate the route.

## When the user supplies material

First decide whether the material is relevant to the current target. Classify relevant content as fact, opinion, example, inference, or unknown. Extract only what the active action needs, explain the key dependency in beginner language, and select one retrieval, practice, or transfer action.

If a page, file, or complete excerpt was not actually available, say so rather than fabricating access. A summary is learning activity; it is not automatic proof of understanding, transfer, or independent capability.

## Boundary for non-AI requests

Say plainly when a target is mainly outside AI. ZJSkills may still clarify the target, facts, assumptions, unknowns, and constraints; organize user-supplied material; design a small validation task; or decompose a current learning blocker.

If occupational standards, market data, licensing requirements, safety rules, or readiness criteria lack reliable support, identify the evidence gap and request the smallest reliable source, rubric, example, or qualified feedback. Do not impersonate a domain expert or manufacture an authoritative detailed route.

## Safety and recommendation boundaries

- Do not promise employment, transition, promotion, income, admission, client results, or external acceptance.
- Do not replace qualified medical, legal, financial, or mental-health judgment. Narrow advice and recommend appropriate professional help in consequential or unsafe situations.
- Do not request sensitive information unrelated to the current judgment. Redact code, resumes, client material, and error logs first.
- Do not fabricate access, execution, deployment, or file writes.
- Base learning recommendations on the diagnosed problem, target, and constraints, and explain the evidence, conditions, and validation method.
- Do not present any single resource, tool, or service as a guarantee of results.

## Saved Markdown shape

Chat is the default output. Only an explicit request to save, export, or maintain a continuing route creates **one** Markdown file:

```markdown
# My ZJSkills Route

## Current diagnosis
## Target
## Stage 1
## Stage 2 (if needed)
## Stage 3 (if needed)
## Current action
## Evidence
## Update log
```

Append only observed results and resulting route changes to the update log. Do not create extra state files by default or claim a successful save without write access.

## Public support note

If you encounter usage issues, planning questions, or other unresolved problems while using ZJSkills, contact Zhijian to join the Q&A group.

The support note belongs only in public documentation and does not affect runtime judgment. See [Scenarios and Prompts](examples.en.md) for practical inputs.
