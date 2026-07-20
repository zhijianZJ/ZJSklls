# ZJSkills Scenarios and Prompts

[简体中文](examples.md)

These examples show the real 3.0 entry points. Copy a prompt and replace bracketed text with your observed result. A good response stays compact, reuses existing context, selects one mode, and ends with one action.

## Scenario 1: A vague AI transition

```text
I have worked in administration for five years and want to move into AI, but I only use chat tools for everyday work and do not know what to learn. I have about five hours per week and do not know whether I should quit to study. Diagnose first.
```

This should enter career diagnosis, separating the wish to “enter AI” from the unresolved work object. If existing facts support it, ZJSkills gives one minimum experience task. If the desired result is the one decisive gap, it asks only that question. It should not begin with a six-month curriculum or advise quitting.

## Scenario 2: Agent versus Vibe Coding

```text
I know a little Python and followed a tutorial to build a chatbot, but I have never changed a requirement independently. I cannot choose between AI Agent Development and Vibe Coding. Give me one minimum task that separates them; do not decide from interest alone.
```

The response should state that a running tutorial is not independent capability evidence. A discriminating task can build and verify a changed requirement in a small tool, then add a model/API call and one diagnosable failure. Reassess from understanding, modification, testing, and debugging results.

## Scenario 3: No coding evidence

```text
I have never coded, but I strongly want to become an AI Agent Engineer. I watch many Agent videos and feel that I understand them. Am I a fit?
```

The desire and video study are known context, but there is no coding or project evidence. A sound judgment is “insufficient evidence—validate first” or “do not invest heavily yet.” The next step is one bounded model/API task with an explanation of how to interpret success or failure.

## Scenario 4: Too many resources and no clear starting point

```text
I saved many Agent, Python, and RAG resources. I switch topics every day and no longer know what comes first. I have eight hours per week and want a demonstrable project in three months. Help me identify the real problem and sequence the learning.
```

The response should identify that the main problem is not a lack of material but the absence of a target deliverable, dependency order, and acceptance criteria. Define the three-month project first, compress the missing capabilities into no more than three stages, and give one action this week that exposes the most important gap.

## Scenario 5: Concept confusion

```text
I cannot distinguish “context” from “instruction” in a prompt. I read the articles, but a new example still confuses me. I'm stuck.
```

This should enter learning help and locate the inability to apply the distinction in a changed example. One action might label the context that supplies decision material and the instruction that states what the model should do. The success signal is an explanation of both labels plus one changed example.

## Scenario 6: A project error

```text
My Python project returns 401 when it calls the model. I reinstalled dependencies, but the error remains. I use macOS, and the full error is: [paste the error]. I'm stuck.
```

Use the environment, error, and attempted fix already supplied. The first action should safely check whether the running process receives its authentication configuration, with an observable signal. Never request the secret itself or dump every plausible cause when evidence is incomplete.

## Scenario 7: A missed week

```text
Unexpected overtime reduced my planned six hours to one, so I did not deliver the project. My time returns to normal next week. Should I delay the entire route by a month?
```

Treat this as one explained interruption, not automatic evidence that the stage route is wrong. Adjust only the current task or next week's minimum deliverable and define completion. If the pattern repeats, use the new evidence to assess a persistent capacity mismatch.

## Scenario 8: A changed goal

```text
I was preparing for AI Agent Development, but my company offered an internal AI Product opportunity. I prefer that opportunity and must present a proposal in three months. Decide which parts of my old route still apply.
```

Recognize a changed target. Return to career diagnosis or, when evidence is sufficient, generate an AI Product route. Preserve transferable model understanding and project experience while rebuilding only affected stages. Do not delete history or treat the internal opportunity as an offer guarantee.

## Scenario 9: A non-AI request

```text
I want to become a registered dietitian within six months. Give me authoritative examination requirements, employment-market facts, and a complete learning route.
```

Say that the target is mainly outside AI and that the Skill has not established local licensing, examination, or market evidence. It can confirm the region, organize official material the user supplies, and clarify one validation step, but it must not impersonate a nutrition or licensing expert or invent authoritative standards.

See the [Full Usage Guide](usage-guide.en.md) for output rules and [Getting Started](getting-started.en.md) for first use.
