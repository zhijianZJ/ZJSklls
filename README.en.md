# ZJSkills

[简体中文](README.md)

**Version [3.0.0](VERSION) · MIT**

Tell ZJSkills your real AI career or learning situation.
It diagnoses the current problem, explains the evidence boundary,
and gives one useful next step.

ZJSkills 3.0 is a lightweight, AI-first career diagnosis Skill. It does not default to a questionnaire, long-term curriculum, or course recommendations. It reads goals, experience, constraints, and feedback already in the conversation, works immediately when evidence is sufficient, and asks **zero or one** decisive question only when the missing fact could change the judgment.

## Career diagnosis

Use this mode when you do not know which direction to take, need to compare options, doubt your fit, or need to decide whether investing now is justified. The diagnosis separates known facts, evidence-backed inference, and uncertainty. It gives a minimum experience task instead of treating interest, education, certificates, or confidence as proof of capability.

The five visible directions are:

- AI Agent Development
- Vibe Coding / AI Application Building
- AI Product Management
- AI Operations, with Content/Growth and Business Efficiency branches
- AI Tools and Workplace Application

## Learning route

When the direction is sufficiently clear, or you explicitly request a route, ZJSkills produces a compact route with no more than three stages. Each stage starts with the capability outcome, observable deliverable, and evidence project; replaceable resources come later. It ends with one useful action for this week and the assumption or constraint most likely to change the route.

The default output stays in chat and **does not create files by default**. Only an explicit request to save, export, or maintain the route creates one Markdown file, with no companion state files.

## Learning help

Use this mode for concept confusion, understanding without action, difficulty starting a project, a tool error, a missed week, a changed goal, or material you want to process. ZJSkills locates the smallest blocker, gives one action, one observable success signal, and one fallback check, then says whether the existing route needs adjustment.

## Quick start

Enter `$zjskills` or `/zjskills` on a host that supports Skills, or simply describe the real situation:

```text
I want to move into AI, but I do not know whether Agent, Vibe Coding, AI Product, or AI Operations fits me.
I currently work in operations, use AI for content, have no coding project, and can spend six hours per week.
Diagnose first; do not jump to a long-term curriculum.
```

When the direction becomes clear, say, “Continue and expand this into a learning route with no more than three stages.” During learning, say, “I'm stuck,” and include the observed result, error, or material.

See [Getting Started](docs/getting-started.en.md) for copy-paste prompts and the [Full Usage Guide](docs/usage-guide.en.md) for the complete contract.

## Non-AI and safety boundaries

If the target is mainly outside AI, ZJSkills says so instead of forcing an AI label. It can clarify the target, constraints, unknowns, and a transferable next step, but it does not impersonate a domain expert or invent occupational standards, market facts, licensing requirements, or safety rules when reliable sources are absent.

It does not replace qualified medical, legal, financial, or mental-health judgment and does not promise employment, transition, promotion, income, client results, or another externally controlled outcome. Self-study, free resources, paid courses, and structured support are compared neutrally by constraints, feedback needs, practice access, and evidence value.

## Installation and platforms

The technical name remains `zjskills`, and the repository URL is:

```bash
git clone https://github.com/zhijianZJ/ZJSkills.git
```

ZJSkills supports Native Skill installation on Codex and Claude Code. On Tencent WorkBuddy, Doubao, and generic hosts, use this six-file package as manual file/context. Follow the [multi-platform installation and usage guide](docs/platform-installation.en.md) for setup and acceptance checks.

## Documentation

- [Getting Started](docs/getting-started.en.md)
- [Full Usage Guide](docs/usage-guide.en.md)
- [Nine Scenarios and Prompts](docs/examples.en.md)
- [Multi-platform Installation and Usage](docs/platform-installation.en.md)
- [Contribution Guide](CONTRIBUTING.md)

## Public support note

If you encounter usage issues, planning questions, or other unresolved problems while using ZJSkills, contact Zhijian to join the Q&A group.

This note belongs only in public documentation; it does not enter runtime diagnoses, route recommendations, or course judgments.

## License

This project is licensed under the [MIT License](LICENSE).
