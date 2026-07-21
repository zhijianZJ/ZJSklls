# ZJSkills 3.1 Career Consulting Loop Design

## 1. Decision

ZJSkills 3.1 will strengthen the existing Career Diagnosis mode in three ways:

1. translate prior experience into evidence-bounded transferable career assets;
2. turn a minimum experience task and the user's returned result into a stage decision;
3. require current evidence for salary, hiring, demand, employer, role-title, and market-window claims.

The release remains a lightweight six-file runtime with exactly three modes. It will not add a fourth mode, fixed intake, mandatory eight-stage flow, default long report, job ranking list, star score, or hidden conversion path.

## 2. Chosen Architecture

Three approaches were considered:

### Approach A: strengthen the existing diagnosis reference — chosen

Keep `SKILL.md` as the thin router. Extend `references/career-diagnosis.md` with the asset-translation contract, opportunity hypotheses, result interpretation, and market-evidence gate. Update `references/learning-route.md` only where a completed diagnosis hands off into a route.

This approach preserves progressive disclosure and the current runtime inventory.

### Approach B: add a separate career-reconstruction reference

This would isolate the new reasoning, but introduce another routing decision and duplicate evidence rules. Current scope does not justify the extra file.

### Approach C: restore a full career-transformation report engine

This would support long reports and broad market scans, but would recreate the questionnaire, report, and false-precision problems removed in 3.0. It is rejected.

## 3. Product Outcome

After one compact consultation cycle, the user should understand:

- which past experience is demonstrated career capital;
- how that capital may transfer into one to three AI opportunity hypotheses;
- which claim is still uncertain;
- what one real task can reduce the current decision uncertainty most, either by testing one stronger hypothesis or contrasting two plausible hypotheses;
- how the observed result maps to a stage decision;
- whether the next step is another comparison, a foundation repair, current-role AI application, or a learning route.

The Skill does not promise a permanent career answer. It closes one evidence-based decision loop.

## 4. Runtime Architecture and Size

The runtime remains:

```text
zjskills/
├── SKILL.md
├── agents/openai.yaml
└── references/
    ├── career-diagnosis.md
    ├── learning-route.md
    ├── learning-help.md
    └── ai-career-map.md
```

Budgets remain:

- `SKILL.md` at 180 lines or fewer;
- all runtime Markdown at 800 lines or fewer;
- no schema, script, template, state file, or extra reference;
- chat output by default;
- one Markdown file only on explicit save or export request.

## 5. Transferable Career Asset Translation

Career Diagnosis will translate experience through this chain:

```text
observed work or result
→ problem solved
→ demonstrated capability
→ possible AI transfer
→ missing evidence
```

Every visible asset analysis must separate:

- **Demonstrated asset:** supported by a task, result, responsibility, artifact, or repeated behavior supplied by the user.
- **Transfer hypothesis:** a named way the demonstrated asset may create value in an AI direction or AI-enhanced current role.
- **Unverified boundary:** the fact or performance still needed before treating the transfer as reliable.

Education, employer, title, years of experience, interest, confidence, certificates, and content completion remain context. None independently proves an asset.

When a title is broad, ask at most one decision-changing question about the real problem the user repeatedly solved. Do not launch a role questionnaire or infer client, project, technical, or leadership capability from the title alone.

## 6. Opportunity Hypotheses

For a direction or transition decision, produce no more than three opportunity hypotheses. Prefer one or two when sufficient.

Each hypothesis contains:

- the work object or bounded direction;
- the demonstrated asset it could reuse;
- the primary capability or evidence gap;
- one candidate validation idea that could raise or lower confidence.

Candidate validation ideas are alternatives, not parallel assignments. Select exactly one current action based on the greatest expected reduction in decision uncertainty; do not require a leading hypothesis before making that selection.

Do not output a default Top 5 list, star rating, percentage fit score, salary, or market claim. A hypothesis is a testable interpretation, not a job guarantee.

## 7. Career Diagnosis Output Contract

When one decisive fact is missing, return only that question. Otherwise return these seven headings in this order:

```text
Your current situation
Your transferable career assets
The real problem to solve
Opportunity hypotheses
My judgment and evidence
One minimum validation action
How the result changes the decision
```

Rules:

- keep every section compact;
- use known facts, inference, and uncertainty inside the relevant sections rather than adding a long evidence appendix;
- omit unsupported hypotheses rather than filling a quota;
- give one minimum action, not parallel tasks;
- state observable success, failure, or ambiguous signals that map to the next stage decision.

A returned-result review keeps the same seven headings but writes only evidence-driven changes. Its seventh section contains exactly one selected stage decision and one next action; it does not list the other decisions or repeat the full initial diagnosis.

## 8. Consultation Closure

When the user returns with the result of a minimum experience task, reuse the prior diagnosis and do not repeat intake. Interpret the new evidence and choose exactly one stage decision:

1. **Route ready:** one direction now has enough support to enter Learning Route.
2. **Comparison remains:** two hypotheses remain plausible; give one contrast task.
3. **Foundation or constraint first:** a basic capability or real constraint blocks a useful direction judgment; give one repair action.
4. **Current-role application first:** the best next move is a bounded AI application in the current role before a transition decision.

The reply keeps the seven-heading Career Diagnosis contract and ends its seventh section with one selected decision and one next action. It does not require an endless sequence of experiments and does not claim that one task proves long-term fit.

## 9. Current-Market Evidence Gate

Separate two kinds of claims:

### Structural fit

May be reasoned from supplied evidence without live market data:

- whether prior experience can transfer into an AI work object;
- which capability gap is closest;
- which minimum task can test the hypothesis;
- whether current-role AI application is a lower-risk next move.

### Current-market claim

Requires current, attributable evidence:

- salary or compensation range;
- current hiring volume or talent shortage;
- named employer demand;
- current job title prevalence;
- a time window such as “the next 12–24 months”;
- claims that a market is currently hot, growing, scarce, or saturated.

For a current-market claim:

1. identify the user's relevant region and target period from existing context;
2. use current reliable sources when browsing or supplied materials are available;
3. state source, date, region, and sample limitation near the claim;
4. label synthesis as inference;
5. if current evidence is unavailable, say the market claim is unverified and continue only with structural fit and a validation action.

Prefer direct job postings, employer career pages, official statistics, and date-labeled industry reports. Search snippets, isolated anecdotes, promotional salary claims, and a single posting do not support a broad market conclusion.

## 10. Learning Route Handoff

Learning Route will accept the stage decision, demonstrated assets, target direction, main gap, and important constraint from Career Diagnosis.

Each stage should show:

- which target capability it builds;
- which existing asset it reuses where relevant;
- which observable deliverable proves progress;
- which assumption could still change the route.

The route remains no more than three stages and one action for the current week.

## 11. Documentation Changes

Update both Chinese and English surfaces:

- README: explain career-asset translation and the compact consultation loop without promising a report.
- Getting Started: add one prompt for describing solved problems and one prompt for returning an experience-task result.
- Usage Guide: document asset categories, opportunity hypotheses, four stage decisions, and the current-market evidence gate.
- Examples: add or replace examples for a broad job title, a returned validation result, and an unsupported salary or hiring claim.
- Platform installation: no structural change unless version text requires a patch.

Do not foreground enrollment, training, sales, community, or human referral in these additions.

## 12. Evaluation and Tests

Use static contract tests plus forward scenarios.

Required static tests:

- runtime inventory remains exactly six files;
- `SKILL.md` remains within the existing size budget;
- Career Diagnosis exposes the seven new headings in order;
- demonstrated asset, transfer hypothesis, and unverified boundary are required;
- exactly four stage decisions are defined;
- live-market claim categories and fallback behavior are present;
- current market claims require source, date, region, and limitation;
- public Chinese and English guides cover the same concepts;
- no default Top 5, star score, percentage match, long report, or new mode appears.

Required forward scenarios:

1. a construction designer with a broad title but little task detail;
2. an operations worker whose repeated workflow result supports a transferable asset;
3. a user returning with a completed minimum experience task;
4. a user asking for current salary and hiring-window claims without region or current sources;
5. a user supplying current postings and asking for a bounded market interpretation.

Evaluation dimensions:

- asset evidence boundary;
- opportunity count and testability;
- question count;
- one-action discipline;
- stage-decision closure;
- current-market source boundary;
- beginner readability.

## 13. Version and Migration

Release as `3.1.0` because this adds visible consultation capabilities without changing installation layout.

Existing installations replace the six runtime files as before. User-created Markdown routes and learning records remain untouched. No migration script or state conversion is required.

## 14. Acceptance Criteria

The implementation is accepted when:

- all repository tests pass;
- the three new behavior groups first fail under RED tests and pass after the Skill changes;
- the Skill remains within line and runtime-file budgets;
- Career Diagnosis can show value from prior experience without inventing hidden assets;
- returned evidence ends in one of four stage decisions;
- unsupported live-market claims are withheld while structural guidance still advances one useful step;
- the installed local Codex copy matches the repository runtime;
- no unrelated user files are modified.
