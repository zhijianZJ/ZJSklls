# ZJSkills Scenarios and Prompts

These prompts start or continue a learning-system design. The likely artifacts are examples, not guarantees of employment, income, promotion, or delivery outcomes. Replace placeholders with real constraints and require the Skill to separate self-report, evidence, inference, and assumption.

## Scenario 0: Start from the learning navigation

### The need is still ambiguous

```text
Use ZJSkills. I want to learn AI, but I do not know where to start.
```

This should open the six-option learning navigation instead of producing a long route. Replying `4` selects help with a learning problem. Describing the problem directly, such as “I understand tutorials but cannot build alone,” reaches the same support.

### You do not know which option fits

```text
I do not know which option to choose or how to explain what I need.
```

The Skill should offer two or three plain choices or one tiny experience task. It should not require workflow terminology or start a complete profile questionnaire.

### A concrete problem routes directly

```text
My API call returns 401. What should I do now?
```

A concrete problem bypasses the home menu and starts with one safe check and an observable completion signal. It must not request a secret.

### Resume prior progress

```text
Continue my previous learning. Check the state in the workspace I specify first.
```

With valid state, resume from the earliest unpassed gate or open issue. Without state, do not invent progress; offer exactly two paths: create a new plan or specify the workspace containing saved state.

### Inspect professional state

```text
Switch to professional mode and show this decision's evidence, assumptions, gates, and engine_result.
```

Professional mode adds traceability without weakening evidence or safety standards. Say “Make it simpler” to return to beginner mode.

## Scenario 1: Explore the AI industry from zero

### First prompt

```text
Use ZJSkills to help me build a structured understanding of the AI industry in four weeks and decide whether to explore technical, product, or business-application work next. I have no programming experience, five hours per week, and a budget of CNY 300. Ask the decision-critical questions first and do not start with a course list.
```

### What the Skill may ask

Your current industry, problems you have solved, willingness to code, English reading, available equipment, and the evidence you want to use for a direction decision after four weeks.

### Likely artifacts

An AI role map, transferable-capability hypotheses, three small experience tasks, a direction scorecard, a four-week exploration route, and weekly evidence checks.

### Second-turn continuation prompt

```text
I enjoy turning ambiguous needs into solutions and accept light technical work, but do not currently want to become a full-time engineer. Build the first capability-exploration map, three minimum experience projects, and this week’s plan. Label every conclusion that remains an assumption.
```

### Progress review and replanning prompt

```text
I completed all three tasks. The product brief scored highest, but I was most engaged by the automation task. Here are the artifacts and reflection: [content]. Update the direction judgment, preserve the conflicting evidence, and design the next discriminating experiment.
```

## Scenario 2: Transition to AI Agent Engineer

### First prompt

```text
Use ZJSkills to assess a transition to AI Agent Engineer. I have three years in data analysis, know SQL and some Python, can invest ten hours per week, and want credible real-project evidence for role evaluation in eight months. Define success evidence and critical gaps before building a route. Do not treat course completion as capability.
```

### What the Skill may ask

Evidence of Python and engineering practice, API/Git/deployment experience, target job samples, publishable data, cloud budget, documentation language, and deadline flexibility.

### Likely artifacts

An L0–L5 competency tree; a Python/API/LLM/RAG/tool/workflow/evaluation/deployment dependency graph; a six-level project ladder; a capability coverage matrix; a phased roadmap; and independent-delivery rubrics.

### Second-turn continuation prompt

```text
Here are my current Python repository, test results, and target job descriptions: [content]. Judge current levels only from resolvable evidence, then create prioritized gaps, the first three projects, and the first week’s minimum delivery.
```

### Progress review and replanning prompt

```text
The RAG project runs, but retrieval quality dropped after the requirements changed and I could not diagnose it independently. Score the project evidence, locate the earliest causal gap, add guided-to-independent debugging practice, and update the route.
```

## Scenario 3: Transition to AI Product Manager

### First prompt

```text
Use ZJSkills to design my AI Product Manager transition system. I have five years in ecommerce operations, no development background, eight hours per week, and a six-month target to produce AI product cases and work samples that a target team can evaluate. Analyze transferable capability, technical-understanding gaps, and target-role differences first.
```

### What the Skill may ask

Target industry, evidence of requirements and data decisions, cross-functional delivery, technical communication, access to users, a testable problem, and portfolio confidentiality.

### Likely artifacts

A competency model spanning problem framing, AI boundaries, data and evaluation, prototype validation, technical communication, and delivery; a problem-to-prototype project ladder; and case-study and demo rubrics.

### Second-turn continuation prompt

```text
My target is ecommerce service and operations efficiency. Here are prior requirement documents and analytics cases: [content]. Identify verified capabilities versus transfer hypotheses, then create the first project brief around a real user problem.
```

### Progress review and replanning prompt

```text
Interviews confirmed the problem, but the prototype did not improve the key measure and engineering said the requirement boundary was unclear. Preserve this negative evidence, reassess framing, acceptance measures, and technical communication, and revise the project instead of adding generic content.
```

## Scenario 4: Apply AI in current work

### First prompt

```text
Use ZJSkills to help me deliver an AI application in my current manufacturing-procurement role. I have four hours per week and want to reduce repetitive supplier-document work within ten weeks while meeting company data and approval rules. Clarify business value, risk, permissions, and verifiable measures first.
```

### What the Skill may ask

Current process time and error rate, data classification, allowed tools, approver, failure impact, available samples, human-review points, and the acceptance owner.

### Likely artifacts

A baseline, risk boundary, minimum automation competency model, controlled sample experiment, human-review workflow, efficiency and quality measures, delivery documentation, and rollback plan.

### Second-turn continuation prompt

```text
Only redacted samples are allowed, and a procurement manager must approve every final output. The process takes about six hours per week with roughly 12% rework. Design the lowest-risk pilot, capability requirements, acceptance measures, and this week’s plan.
```

### Progress review and replanning prompt

```text
The pilot reduced processing time, but critical-field errors exceeded the threshold and human review increased. Here are the test records: [content]. Diagnose the failure, roll back to the earliest affected capability or project decision, and design the next experiment.
```

## Scenario 5: Getting stuck while learning

These prompts work inside an existing learning plan; you do not need to restart the full planning workflow.

### A concept does not make sense

```text
I am learning embeddings, but every explanation adds more unfamiliar terms and I no longer know where I first got lost. Use beginner-friendly language to locate one blocker, then give me one tiny task that checks understanding. Do not explain the whole chapter at once.
```

### An API returns 401

```text
My API call returns 401. I am a beginner. Explain in one sentence which boundary this usually points to, then give me only one safe check at a time. Never ask me to send an API key, password, or token, and tell me what visible result means the step is complete.
```

### A week was missed

```text
I did not complete this week's plan. Do not assume I lack discipline and do not immediately rebuild the entire route. Ask one question at a time to locate the earliest obstacle, then decide whether to change the current task, this week, or the roadmap.
```

### The target changed

```text
My target changed from becoming an AI Agent Engineer to building an AI consulting business. Decide whether this changes the whole goal system, preserve the old version, and state where replanning must begin. Do not just append startup tasks to the old weekly plan.
```

### Continue after one action

```text
I completed the previous action. The result was [result]. Decide whether the issue is resolved. If not, give me only the next action and success signal. If this affects the plan, state the smallest justified change and why.
```
