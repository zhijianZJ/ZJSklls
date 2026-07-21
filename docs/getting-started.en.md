# ZJSkills Getting Started

[简体中文](getting-started.md)

You do not need to understand a career model or prepare a complete profile. Describe the real situation, even if it is messy. ZJSkills reads the existing conversation first, diagnoses immediately when it can, and asks one question only when one missing fact could change the judgment.

## First: describe the real situation

This is a complete and useful first input:

```text
I want to move into AI, but I do not know whether Agent, Vibe Coding, AI Product, or AI Operations fits me.
I work in traditional operations, use AI for content and spreadsheets, have never coded, and have no complete project.
I can spend about six hours per week, have a limited budget, and hope to produce work I can use to pursue a new opportunity in six months, although I do not know whether that is realistic.
Analyze my situation first, identify the real problem, and give me the most suitable next step.
```

It supplies the desired result, current work, observable experience, time, and budget constraints. Do not fill every gap as a questionnaire. If a missing fact does not change the useful next step, ZJSkills labels the uncertainty and continues.

For a shorter copy-paste prompt, use:

```text
I want to move into AI, but I do not know whether Agent, Vibe Coding, AI Product, or AI Operations fits me.
Use the experience I have already described in this conversation and diagnose first. Ask one question only if one missing fact could change the judgment.
```

If a job title is too broad, start with the problem you repeatedly solved and add an observable result:

```text
My job title is [title]. The problem I repeatedly solved was [problem], and the result was [result]. Separate demonstrated assets, transfer hypotheses, and unverified boundaries.
```

## What a one-page career diagnosis contains

The initial diagnosis stays within seven compact sections:

1. current situation;
2. transferable career assets;
3. real problem to solve;
4. opportunity hypotheses;
5. judgment and evidence;
6. one minimum validation action;
7. how the result changes the decision.

“Stronger fit,” “worth testing with risk,” “do not invest heavily yet,” and “insufficient evidence” are provisional judgments, not capability certificates. They do not guarantee an offer, transition, or income. Interest, education, content exposure, and confidence are context, not standalone proof.

After completing the minimum experience task in section 6, return to the same conversation with the result:

```text
I completed the minimum experience task. The observed result was [result]. Reuse the previous diagnosis and decide whether I am ready to enter a route, still need comparison, should build foundations first, or should apply this in my current role first. Give only one next step.
```

This review uses the same seven headings but records only changes caused by the new evidence instead of repeating the full diagnosis. Its seventh section gives one current stage decision and one next action without expanding the other three alternatives. Only “ready to enter a route” hands off to Learning route. The other decisions remain in Career diagnosis and use one action to close the most important evidence or foundation gap.

## Reply “Continue”: expand a learning route

When the direction is clear, “Continue” is enough. For a more explicit request, copy:

```text
The direction is clear. Expand it into a learning route with no more than three stages.
For each stage, put the capability, observable deliverable, and evidence project before resources.
End with one action for this week, its completion signal, and the assumption or constraint most likely to change the route.
```

The route does not automatically become a daily task list. A real project or target behavior under changed conditions supports a capability judgment better than content completion alone.

## Say “I'm stuck”: enter learning help

You do not need to resubmit your background or classify the problem. Say:

```text
I'm stuck: [paste the observed result, error, attempts, or say “I do not know where to start”].
Locate the smallest blocker. Give me one action to do now, an observable success signal, and one fallback check, then say whether the existing route is affected.
```

For concept confusion, it finds the distinction you cannot explain or apply. For an error, it uses the exact message, reproduction steps, input, output, and environment already supplied. For a missed week, it distinguishes a one-off interruption from a persistent capacity mismatch. One failure does not automatically rewrite the whole route.

## Save one Markdown route

Results stay in chat by default. ZJSkills creates a file only after an explicit request:

```text
Save the current diagnosis and learning route as one Markdown file.
Include only the current diagnosis, target, no more than three stages, current action, evidence, and a short update log. Do not create companion state files.
```

Later, provide the observed result and ask it to append an update. If the path, write permission, or destination is unclear, it should explain the limit rather than claim that it saved anything.

## What to say next

- Direction still uncertain: “Give me one minimum experience task that distinguishes Agent from Vibe Coding.”
- Experience task completed: “I finished it. Here is the result... Reassess without repeating answered questions.”
- Conditions changed: “I now have only three hours per week. Decide whether to adjust the current task, the stage, or the direction.”
- You have material: “Extract only what matters to my current target and turn it into one retrieval, practice, or transfer action.”

## Public support note

If you encounter usage issues, planning questions, or other unresolved problems while using ZJSkills, contact Zhijian to join the Q&A group.

This transparent note does not enter runtime diagnoses or route recommendations. See the [Full Usage Guide](usage-guide.en.md) for the complete rules and the [multi-platform guide](platform-installation.en.md) for installation.
