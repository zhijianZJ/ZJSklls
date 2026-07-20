# ZJSkills 2.1 AI Routes and Learning Companion Design

## 1. Background

ZJSkills 2.0 provides outcome-driven learner discovery, goal analysis, competency and project design, roadmaps, weekly planning, assessment, problem solving, and adaptive replanning. Its only complete occupational Domain Pack is AI Agent Engineer. The next release must support a wider AI-learning audience while preserving the same evidence, feasibility, privacy, and version-control standards.

The product should help a learner perform the early consultation work that often precedes training: understand their situation, compare directions, test assumptions, select a route, see the path from beginner to entry-level performance, and resolve problems while learning. It should also generalize its learning-system method to non-AI goals without pretending to possess unsupported domain expertise.

## 2. Goals

- Add five user-visible AI routes: AI Agent Development, Vibe Coding / AI Application Building, AI Product Management, AI Operations, and AI Tools / Workplace Application.
- Implement AI Operations as a shared foundation with two independent branches: content and growth operations, and enterprise process / business-efficiency operations.
- Reuse one versioned AI foundation rather than copying the same competencies into every route.
- Produce route decisions from learner evidence and low-cost experience tasks, not from job titles or self-confidence alone.
- Extend learning support to material synthesis, knowledge mapping, explanation, correction, practice generation, and review scheduling.
- Keep the existing goal decomposition, project-first learning, evidence gates, problem-solving loop, and minimum-impact replanning.
- Support non-AI learning through a generic learning engine that labels missing domain evidence and never impersonates an unfamiliar-domain expert.
- Add a transparent documentation-only note for contacting 智建 and joining an answer group when users have usage or other unresolved questions.

## 3. Non-goals

- Do not embed human referral, contact details, community promotion, course sales, or lead routing in the runtime Skill.
- Do not optimize learner-facing decisions for conversion into a community or paid program.
- Do not make one course, tool vendor, framework, or certificate a required route component.
- Do not promise employment, promotion, revenue, client acceptance, or another party's decision.
- Do not expose hidden chain-of-thought. Show concise conclusions, evidence, assumptions, trade-offs, and next actions instead.
- Do not claim expert knowledge for a non-AI domain without reliable supplied or sourced material.
- Do not change the `zjskills` technical identifier or force migration of existing learner workspaces.

## 4. System Architecture

```text
ZJSkills learning-system core
├── learner discovery and self-assessment
├── goal, gap, competency, curriculum, and project design
├── roadmap, weekly planning, assessment, and optimization
├── problem solving and learning companion loop
├── material synthesis and knowledge mapping
│
├── shared AI foundation capability library
│   ├── AI literacy and industry orientation
│   ├── prompting and context expression
│   ├── AI tool selection and verification
│   ├── data, privacy, safety, and responsible use
│   ├── workflow and automation thinking
│   └── project, evidence, and value measurement
│
├── AI Agent Development Domain Pack
├── Vibe Coding Domain Pack
├── AI Product Management Domain Pack
├── AI Operations router
│   ├── Content and Growth Operations Domain Pack
│   └── Business Efficiency Operations Domain Pack
├── AI Tools and Workplace Application Domain Pack
│
└── generic learning mode
    └── method support without unsupported domain authority
```

The interaction orchestrator remains the presentation and routing layer. Decision engines remain responsible for evidence and state. The AI route router selects a foundation plus one Domain Pack; it does not independently declare a route suitable.

## 5. Entry and Route Decision

Keep the six-item home navigation introduced in 2.0. Do not add more top-level choices. Material synthesis and route comparison are natural-language direct intents and contextual secondary choices.

Classify entry intent into:

1. AI industry exploration;
2. current-role productivity;
3. AI application capability;
4. AI career transition;
5. active learning problem;
6. non-AI generic learning goal.

For an unclear direction, follow:

```text
current situation
-> target and constraints
-> candidate routes
-> smallest discriminating experience tasks
-> evidence review
-> route comparison
-> recommendation or defer decision
```

Produce a `route-decision` artifact containing the learner goal, baseline and constraints; candidates; supporting and opposing evidence; experience-task results; expected effort, difficulty and risk; recommended, alternative and deferred routes; confidence; and one validation action.

The beginner-facing route decision card shows:

- current stage;
- likely suitable directions;
- decisive evidence and uncertainty;
- minimum experience task;
- what not to commit to yet;
- one next choice.

Route selection never passes a capability gate and never treats interest, confidence, or questionnaire completion as proof of fit.

## 6. Shared AI Foundation

Create `assets/capability-libraries/ai-foundation.yaml` under a new Capability Library contract. The library is versioned independently and contains stable competency IDs, L0-L5 behaviors, evidence requirements, dependencies, starter experience tasks, and review governance.

Every AI Domain Pack declares a compatible foundation library ID and version range, selects required foundation competency IDs, and adds route-specific competencies. The validator resolves an effective competency graph and enforces:

- referenced library and competency IDs exist;
- requested versions are compatible;
- merged IDs are unique;
- dependency endpoints resolve;
- the effective dependency graph is acyclic;
- stable-ID migrations remain explicit;
- current review dates and source governance remain valid.

The shared foundation covers AI literacy, prompting, tools, verification, privacy and safety, workflow thinking, automation, project framing, evidence, and value measurement. It does not impose coding depth that is irrelevant to product, operations, or tool-use routes.

## 7. Route Packs

There are five user-visible routes and six technical Domain Packs.

### 7.1 AI Agent Development

Extend the existing pack to reference the AI foundation while retaining Python, API, LLM, RAG, tool calling, workflow, multi-agent coordination, evaluation, deployment, and responsible engineering. Its six-project ladder remains: focused prompt/tool, knowledge application, workflow agent, enterprise scenario agent, portfolio case, and real external delivery.

### 7.2 Vibe Coding / AI Application Building

Target capabilities: problem and acceptance definition, AI-assisted software collaboration, interface and interaction basics, data and APIs, code reading, debugging, testing, deployment, product iteration, and safe handling of generated code.

Project ladder: single-page tool; data-backed application; API-integrated application; complete web product; deployable AI application; real-user product delivery.

The route must distinguish “can generate code with assistance” from “can inspect, debug, test, change, and safely deliver the result.”

### 7.3 AI Product Management

Target capabilities: user and business problem framing, AI capability boundaries, data and evaluation, prototype experiments, requirements and acceptance criteria, technical collaboration, responsible-product risk, metrics, and delivery.

Project ladder: problem analysis; AI feature proposal; testable prototype; complete product case; cross-functional simulation; real business validation.

### 7.4 AI Operations: Content and Growth

Target capabilities: audience and channel understanding, research and topic selection, AI-assisted content systems, distribution, user operations, private-domain/community operations, growth experiments, measurement, review, and content safety.

Project ladder: single content task; repeatable content workflow; channel or user-operation experiment; automated growth workflow; evidence-backed portfolio case; real campaign or operating delivery.

### 7.5 AI Operations: Business Efficiency

Target capabilities: process mapping, information and data handling, workplace AI tools, workflow design, automation, human review, knowledge systems, quality controls, adoption, and business-value measurement.

Project ladder: single-task productivity; information/data workflow; bounded automation; department scenario; measurable efficiency case; real operational delivery.

### 7.6 AI Tools and Workplace Application

Target capabilities: tool selection, prompt and context design, research and verification, documents, spreadsheets, presentations, knowledge management, multi-tool collaboration, lightweight automation, privacy, and workplace delivery.

Project ladder: one tool task; personal workflow; multi-tool workflow; role-specific solution; team-efficiency case; real workplace delivery.

Every pack includes suitability and unsuitability conditions, target outcomes, source-dated assumptions, competencies, dependencies, exactly six project archetypes, analytic rubrics, common failure modes, assessment patterns, and outcome-preparation routes for employment, transition, current-role improvement, entrepreneurship, or delivery as applicable.

## 8. Learning Material Engine

Add `references/learning-material-engine.md`, `learning-material-map.schema.yaml`, and a worked template.

Accept articles, notes, transcripts, user-provided page contents, documents, or multiple materials. Never imply a referenced source was read when its contents are unavailable.

Produce a `learning-material-map` with:

- source, author or origin when known, access/provided date, and scope;
- core concepts and conclusions;
- fact, opinion, example, inference, and unverified-claim classification;
- concept dependencies;
- links to active target competencies;
- repetition, contradictions, missing prerequisites, and stale claims;
- beginner explanation;
- retrieval questions and practice;
- transfer or project task;
- review schedule and next action.

Material summarization must feed capability practice. A summary alone is activity evidence, not competence.

## 9. Generic Learning Engine

Add `references/generic-learning-engine.md` for non-AI goals. Reuse Discovery through Continuous Optimization, material synthesis, problem solving, and meta-learning.

The engine may:

- clarify and decompose goals;
- organize user-provided materials;
- build a provisional competency and dependency model;
- design practice, projects, schedules, review, and assessment;
- explain problems from supplied evidence;
- correct errors and adapt the learning system.

It must label domain claims as sourced, supplied, inferred, assumed, or unknown. When reliable domain knowledge is absent, request the smallest source, example, rubric, expert feedback, or performance task needed to continue. It must not manufacture professional standards, safety rules, or readiness claims.

## 10. Learning Companion Behavior

The horizontal companion loop supports:

- concept confusion: locate the earliest conceptual break;
- explanation-to-action gap: find the first step the learner cannot perform;
- starting ambiguity: define one minimum input-output loop;
- tool or environment errors: inspect one safe boundary at a time;
- disorganized thinking: restate target, facts, constraints, options, trade-offs, and action;
- task overreach: shrink scope without removing the target capability;
- incorrect work: cite the observed error, propose a cause hypothesis, and define one correction test;
- missed work: select `task`, `week`, `roadmap`, or `goal_system` impact from evidence;
- claimed completion: require an observable result and, when relevant, independent or changed-condition performance.

Default beginner output remains one main action, an observable success signal, and one fallback. “Show my reasoning” means provide a concise decision rationale with evidence, assumptions, alternatives, and trade-offs; never reveal hidden chain-of-thought.

## 11. Documentation-only 智建 Answer Group Note

Add a transparent note to the Chinese and English README, getting-started guide, full usage guide, and platform installation guide:

> 使用 ZJSkills 时如遇到使用问题、规划疑问或其他未解决问题，可联系智建进入答疑群交流。

Use an equivalent English sentence. Do not add a contact address until the maintainer explicitly supplies one.

This note is documentation only. Runtime references, prompts, Domain Packs, cards, state, and recommendations must not contain referral, community, course, purchase, or conversion logic. Tests enforce that separation.

## 12. Error and Boundary Handling

- Ambiguous route: use experience tasks; do not force a decision.
- Conflicting route evidence: retain the conflict, lower confidence, and run the smallest discriminating task.
- Missing or incompatible foundation: block effective-pack activation and report the exact reference error.
- Stale market assumptions: mark the affected pack stale and request updated evidence.
- Impossible target/constraint combination: expose the trade-off and offer a minimum viable outcome.
- Missing material contents: request upload or contents; do not summarize a title or link alone.
- Contradictory materials: show both claims, sources, dates, and a verification action.
- Unsupported non-AI domain: proceed only with general method and explicit uncertainty.
- High-risk legal, medical, financial, psychological, security, or production questions: retain the existing qualified-review boundary.
- No writable workspace: show results but keep `artifacts_written` empty and do not claim persistence.

## 13. Testing and Evaluation

Add automated tests for:

- Capability Library schema and semantic validation;
- foundation reference existence, version compatibility, endpoint resolution, duplicate IDs, and merged cycles;
- all six Domain Packs and exactly six projects per effective route;
- fixed rubric dimensions, weights, thresholds, evidence coverage, and assessment behaviors;
- AI Operations branch separation and shared-foundation reuse;
- route-decision and learning-material-map schemas and worked templates;
- runtime neutrality and documentation-only 智建 note;
- no paid-course requirement or hidden conversion behavior;
- current README paths, version, and public package completeness.

Forward-test at least these behaviors:

- a complete beginner comparing AI Product Management and AI Operations;
- a nontechnical learner selecting AI Tools / Workplace Application;
- a learner confusing Vibe Coding with independent software delivery;
- content-growth versus business-efficiency AI Operations branching;
- an AI Agent learner with insufficient programming evidence;
- multiple materials with conflicting claims;
- a non-AI learning goal with insufficient domain evidence;
- correction after wrong work;
- a request for hidden reasoning;
- a usage question that sees the documentation note but no runtime referral.

## 14. Release and Migration

- Develop on independent branch `codex/zjskills-learning-routes` based on the 2.0 implementation.
- Release as `2.1.0` because the new libraries, packs, engines, and schemas are additive.
- Keep current learner workspace contracts backward compatible.
- Make foundation references optional for legacy third-party Domain Packs; self-contained packs remain valid.
- Document how maintainers migrate a self-contained Pack to the shared foundation without changing learner evidence IDs silently.
- Publish through a separate Draft PR rather than expanding Draft PR #5.

## 15. Acceptance Criteria

The release is ready when:

- all five user-visible AI routes produce distinct, evidence-backed beginner-to-delivery systems;
- the two AI Operations branches share foundation competencies but do not share route-specific projects or readiness claims;
- a route recommendation cites learner evidence or an experience task and can remain undecided;
- material synthesis maps content to capability practice rather than stopping at a summary;
- non-AI mode works without unsupported expert claims;
- runtime behavior contains no 智建/community/course conversion path;
- public documentation contains the approved answer-group note;
- legacy learner fixtures and the existing AI Agent route still validate;
- automated tests, package validation, isolated installation, and forward behavioral evaluations pass.
