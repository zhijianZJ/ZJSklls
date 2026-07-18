# ZJSkills Getting Started

ZJSkills is an outcome-driven learning-system Skill, not a course recommender. It starts with your target, baseline, capacity, and constraints, then works backward into capabilities, projects, a roadmap, weekly commitments, and verifiable evidence. When evidence or circumstances change, it replans the affected system instead of merely adding more content.

## Before you begin

You do not need a complete personal dossier. Bring as much of this as you can:

- the result you want and the evidence you hope to have by a given date;
- your current work, education, and relevant experience;
- sustainable weekly time, budget, and available equipment;
- language, math, programming, or business baseline;
- hard constraints involving work, family, health, privacy, or access;
- the authentic outcome you want to produce, such as a portfolio case, deployed project, work sample, or real delivery.

Use “unknown” or a range when necessary. Self-assessment is treated as `self-report`, not automatically as verified capability.

## First use

Enable `learning-architect` in a Skill-capable AI client, then copy and adapt this prompt:

```text
Use ZJSkills to design my personalized learning system.
Target: [target]
Current situation: [work, education, and relevant experience]
Weekly capacity: [hours]
Target date: [date or duration]
Binding constraints: [budget, language, equipment, family, work, or other limits]
Evidence I want to produce: [project, portfolio, real delivery, work sample, and so on]
First identify the missing information that could change the route. Ask only the highest-impact question at a time, and do not jump to a course list.
```

The first response may not be a polished timetable. The Skill first checks whether the outcome is verifiable, whether constraints conflict, and which conclusions are facts, evidence, inferences, or assumptions.

## Why it asks before planning

“Learn AI” can mean industry exploration, improving current work, becoming an AI Product Manager, becoming an AI Agent Engineer, or delivering an enterprise project. Those targets require different capability evidence and project sequences. Capacity, budget, and baseline can also change the dependency order.

The Skill should ask only decision-critical questions. You do not need to answer the full discovery bank at once:

1. Start with the target, baseline, weekly capacity, and hard constraints.
2. Mark unknowns explicitly.
3. Let low-risk work continue as a labeled draft with assumptions and validation actions.
4. Add reliable sources or qualified human review for hiring rules, regulation, health, finance, production deployment, and other high-risk decisions.

## How to continue

Once the critical inputs are clear, request the first complete system:

```text
Using the confirmed information, create version 1 of the complete learning system: target outcome, capability gaps, competency tree, dependency graph, project ladder, phased roadmap, next weekly plan, assessment criteria, and replanning triggers. Separate facts, self-reports, evidence, inference, and assumptions, and show every gate that has not passed.
```

You can resume without starting over. For cross-task persistence, name a learner workspace you authorize and ask for `system-state.yaml` to be written there. The Skill does not select a global storage location, and it must not claim persistence when file writes are unavailable.

```text
Read and validate [learner workspace path]/system-state.yaml, then continue the previous ZJSkills state from the earliest stage whose gate has not passed.
```

```text
Here is new evidence from this week: [repository, artifact, test result, feedback, or reflection]. Update the capability judgment and only recompute affected decisions.
```

```text
I now have only four hours this week. Keep the target, recalculate capacity, and give me the minimum viable delivery.
```

Every stage should return concise natural-language guidance plus synchronized structured state in the canonical `engine_result` wrapper. `artifacts_written` must list only files actually persisted.

## How to replan

Replanning rolls back to the earliest affected decision:

- target change: return to Goal Analysis and recompute all affected downstream artifacts;
- time, budget, or environment change: recheck Roadmap and Weekly Planner;
- failed project or assessment: locate the earliest causal gap and add focused practice, debugging, or reflection;
- changed domain evidence: recheck the Domain Pack, capabilities, curriculum, and projects;
- contradictory evidence: retain the conflict, lower confidence, and run the smallest discriminating assessment.

```text
My target changed from [old target] to [new target] because [reason]. Create a new version, identify all affected downstream artifacts, and replan from the correct stage without overwriting history.
```

```text
This stage missed its rubric threshold. The failure evidence is [evidence]. Find the earliest causal gap, design a guided-to-independent recovery path, and update the downstream roadmap.
```

ZJSkills can improve learning decisions, capability evidence, and adaptation. It cannot guarantee an offer, career transition, promotion, income, venture outcome, client acceptance, or any result controlled by external parties.
