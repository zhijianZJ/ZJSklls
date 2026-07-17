# Learning Architect ZJSkills Open-Source Productization Design

**Date:** 2026-07-17

**Status:** Approved design, pending implementation plan

**Project:** Learning Architect
**Initiator mark:** ZJSkills（智建）

## 1. Objective

Turn the existing Learning Architect repository into a complete bilingual open-source product without changing its core learning-system methodology.

The repository should help a new user:

1. understand the value in under 30 seconds;
2. install the Skill;
3. submit a real AI-learning or career-transition situation;
4. understand why the Skill may ask questions before planning;
5. obtain a capability-, project-, evidence-, and outcome-driven learning system;
6. continue updating that system as evidence, constraints, or goals change.

The product should establish a light professional connection with ZJSkills through the quality of the methodology, examples, tests, and maintenance. It must not use the learner-facing Skill output as an advertising channel.

## 2. Positioning

### 2.1 Product positioning

Chinese:

> Learning Architect 是由 ZJSkills（智建）发起的开源 AI 职业学习决策与规划系统。

English:

> Learning Architect is an open-source AI career learning decision and planning system initiated by ZJSkills.

### 2.2 Target users

- people exploring the AI industry;
- people deciding what AI direction to learn;
- career changers targeting AI roles;
- practitioners using AI to improve their current work or project delivery;
- educators and contributors extending occupational Domain Packs.

### 2.3 Target psychological account

ZJSkills should be perceived as the initiator and maintainer of a credible decision methodology, not as an information aggregator, an unsupported authority figure, or an embedded sales agent.

The expression posture is decision-oriented and peer-level:

- help users understand their situation and trade-offs;
- show the methodology through executable artifacts and tests;
- avoid unsupported credentials, claims, guarantees, and authority language;
- allow future community or training support to remain separate and user-initiated.

## 3. Reference Project Findings

The open-source packaging of [dontbesilent2025/dbskill](https://github.com/dontbesilent2025/dbskill) provides a useful structural reference:

- a clear one-sentence value proposition;
- quick-start prompts before method explanations;
- capability tables organized by real user situations;
- installation and update instructions;
- a full beginner guide;
- project structure, version, author, support, and license sections;
- multilingual entry points.

Learning Architect will borrow this information hierarchy, not its promotional density, personal-proof claims, command system, knowledge-base scale, community funnel, or multi-platform plugin architecture.

## 4. Brand Boundary

The approved brand strings are:

```text
Initiated and maintained by ZJSkills
由 ZJSkills（智建）发起并维护
Copyright (c) 2026 ZJSkills
```

Brand references may appear only in:

- root README files;
- author or maintainer sections in public documentation;
- repository metadata;
- the MIT copyright notice.

Brand references must not appear in:

- learner-facing decisions or plans;
- the canonical `engine_result` payload;
- competency, curriculum, project, roadmap, weekly-plan, assessment, or optimization artifacts;
- prompts that redirect users to a community, course, product, or contact channel;
- runtime instructions that alter the Learning Architect methodology.

No personal biography, private experience, client result, unverifiable claim, social link, QR code, community link, course link, or sales copy will be added in this phase.

## 5. License and Version

The repository will use the MIT License.

```text
Copyright (c) 2026 ZJSkills
```

The initial public productized release will use version `1.0.0`, recorded in a root `VERSION` file and shown consistently in both README files.

MIT permits personal, institutional, and commercial use, modification, and redistribution while requiring preservation of the license and copyright notice.

## 6. Repository Information Architecture

```text
LearningArchitectSkills/
├── README.md                       # Chinese default homepage
├── README.en.md                    # English homepage
├── LICENSE                         # MIT License
├── VERSION                         # 1.0.0
├── CONTRIBUTING.md                 # Bilingual contribution guide
│
├── docs/
│   ├── getting-started.md          # Chinese beginner guide
│   ├── getting-started.en.md       # English beginner guide
│   ├── usage-guide.md              # Chinese full usage guide
│   ├── usage-guide.en.md           # English full usage guide
│   ├── examples.md                 # Chinese scenarios and prompts
│   ├── examples.en.md              # English scenarios and prompts
│   ├── domain-pack-guide.md        # Chinese extension guide
│   └── domain-pack-guide.en.md     # English extension guide
│
├── learning-architect/             # Runtime Skill remains isolated
└── tests/                          # Existing validation and behavior tests
```

The current English `README.md` becomes `README.en.md`. The current Chinese `README.zh-CN.md` becomes the default `README.md`. Links must be updated without leaving duplicate or stale language entry points.

## 7. Document Contracts

### 7.1 README files

Both README files must contain equivalent information in their respective language:

1. language switcher;
2. one-sentence value proposition;
3. version, test-count, and MIT badges or plain-text indicators;
4. supported use cases;
5. what makes Learning Architect different from a course recommender;
6. a copyable quick-start prompt;
7. installation instructions;
8. capability and output overview;
9. a concise workflow;
10. links to full documentation;
11. repository structure;
12. contribution and license links;
13. one light ZJSkills initiator and maintainer statement.

### 7.2 Getting-started guides

The beginner guides must explain:

- what information a learner should provide;
- why the first response may be Discovery rather than a full plan;
- how the smallest-question rule works;
- how to answer follow-up questions;
- how to request the first complete learning-system draft;
- how to continue from an existing learner state;
- how to submit new evidence, constraints, or target changes.

### 7.3 Full usage guides

The usage guides must explain the complete system:

```text
Discovery
→ Goal Analysis
→ Gap Analysis
→ Competency Design
→ Curriculum Design
→ Project Design
→ Roadmap
→ Weekly Planner
→ Assessment
→ Outcome Preparation
→ Continuous Optimization
```

They must distinguish:

- learner activity from capability evidence;
- courses and resources from system outcomes;
- self-report, evidence, inference, and assumption;
- a target outcome from a promised external result;
- an initial plan from a versioned adaptive system.

They must also explain the major artifact types and the synchronized natural-language plus `engine_result` return contract.

### 7.4 Scenario examples

The bilingual example documents must cover:

1. zero-background AI industry exploration;
2. transition to AI Agent Engineer;
3. transition to AI Product Manager;
4. using AI to improve current work and project delivery.

Each scenario must include:

- a copyable first prompt;
- the critical information the Skill is expected to request;
- likely competency, project, and roadmap outputs;
- a second-turn continuation prompt;
- a later progress-review or replanning prompt;
- a note that the example is illustrative rather than a guaranteed outcome.

### 7.5 Domain Pack guides

The Domain Pack guides must explain how contributors can extend the system to AIGC, Vibe Coding, AI operations, or another occupation without rewriting the core Skill.

They must document:

- the Domain Pack contract;
- stable IDs and versions;
- target outcomes;
- competency seeds and dependencies;
- project archetypes and typed rubric gates;
- evidence requirements;
- sourcing and review metadata;
- schema validation and test expectations.

### 7.6 Contribution guide

`CONTRIBUTING.md` will contain clearly separated Chinese and English sections covering:

- issue reporting;
- documentation changes;
- Domain Pack contributions;
- scope and brand boundaries;
- required validation commands;
- pull-request expectations;
- privacy and evidence requirements;
- prohibition on hidden promotion or unsupported professional claims.

## 8. User Journey

```text
Discover repository
→ Understand value in 30 seconds
→ Install Skill
→ Submit real situation
→ Complete decision-critical Discovery
→ Receive a versioned learning system
→ Submit evidence and feedback
→ Reassess and optimize
```

The README quick start must begin with a real situation, not a methodology lesson:

```text
请使用 Learning Architect。

我想在 6 个月内转岗 AI Agent 工程师。
目前会基础 Python，每周可投入 12 小时，预算 3000 元。
请先分析我的情况，不要直接推荐课程。
```

The documentation must explicitly set these expectations:

- the Skill may ask questions before producing a complete route;
- users do not need to answer the full question bank at once;
- resources are replaceable inputs;
- authentic projects and observable behavior provide capability evidence;
- impossible target, time, budget, or environment combinations produce trade-offs;
- previous state can be resumed;
- target changes cause downstream recomputation rather than course-list patching.

## 9. Failure and Boundary Behavior

Documentation must accurately describe existing runtime behavior:

| Condition | Expected behavior |
| --- | --- |
| Decision-critical information is missing | Return `needs_input` and ask only material questions |
| Target and constraints are infeasible | Explain conflict and offer a minimum viable outcome or explicit trade-off |
| Capability evidence is missing | Label capability as a hypothesis; do not claim mastery |
| Authentic performance fails | Return to the earliest causal gap |
| State is corrupted or versions conflict | Stop writes, preserve state, and request repair or merge judgment |
| Goal is medical, legal, financial, or otherwise high-risk | Hold the gate for qualified professional review |
| Sensitive information is involved | Keep it local by default and avoid unnecessary collection |

Documentation must not describe functionality that is not implemented and tested.

## 10. Skill Metadata Changes

The Skill frontmatter description may be expanded to trigger for:

- AI industry exploration;
- AI learning-direction decisions;
- AI career-transition planning;
- personalized competency and project roadmaps;
- progress assessment and replanning.

Any change to `learning-architect/SKILL.md` must remain imperative, concise, and under the existing progressive-disclosure architecture.

`learning-architect/agents/openai.yaml` must be checked and regenerated only if its display metadata or default prompt becomes inconsistent with `SKILL.md`.

The runtime Skill must remain brand-neutral.

## 11. Explicit Non-Goals

This phase will not add:

- community QR codes, community links, course links, or contact information;
- biography, credentials, or client metrics;
- a website, demo GIF, or marketing landing page;
- a plugin marketplace package or multi-platform installer;
- an automatic update system;
- promotional messages in learner output;
- a new router command or multiple new Skills;
- unrelated schema, workflow, or validator refactors.

## 12. Verification Strategy

### 12.1 Open-source structure

- Chinese and English pages link to each other.
- Every relative Markdown link resolves.
- Documented installation and validation commands execute in the stated context.
- `LICENSE`, `VERSION`, and README version references agree.
- Copyright strings use only `ZJSkills`.

### 12.2 Skill regression

- `quick_validate.py learning-architect` passes.
- All existing 84 unit tests pass.
- The valid learner fixture returns `VALID`.
- All YAML files parse.
- Brand and promotion strings do not appear in learner-facing runtime instructions or fixtures.

### 12.3 Reader testing

Fresh readers must be able to answer from each language set:

- what the Skill does;
- who it is for;
- how to install it;
- what first prompt to send;
- why it asks questions before planning;
- what outputs to expect;
- how to continue or replan;
- how to contribute a Domain Pack.

### 12.4 Behavior forward tests

Each of the four scenarios must demonstrate:

- correct entry into Discovery when information is incomplete;
- evidence and assumption labeling;
- no immediate course-list dumping;
- no external-outcome guarantee;
- no ZJSkills, community, or course promotion in learner output.

### 12.5 Installed-copy verification

After repository verification:

1. update the local installed copy at `~/.codex/skills/learning-architect`;
2. run Skill structure validation against the installed path;
3. run a realistic first-turn request using the installed Skill;
4. confirm the installed content matches the repository release content;
5. document that a newly installed Skill becomes discoverable on the next Codex turn.

## 13. Delivery

Implementation will be delivered on the existing `codex/learning-architect` branch and will update the existing Draft Pull Request.

The implementation must be split into reviewable commits, at minimum:

1. open-source structure, license, and version;
2. Chinese documentation;
3. English documentation;
4. Skill metadata and validation updates, if required;
5. verification or corrective follow-up.

No merge, PR readiness change, or community/course link will be performed without explicit user authorization.
