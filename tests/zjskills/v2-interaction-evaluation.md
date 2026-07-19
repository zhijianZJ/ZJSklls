# ZJSkills 2.0 Interaction Evaluation

Date: 2026-07-19
Method: a fresh read-only evaluator loaded the runtime entrypoint and interaction, workflow, beginner, and problem-solving references, then applied each scenario without modifying learner state or repository files.

| Scenario | Result | Observed routing and presentation |
|---|---|---|
| ambiguous-ai-entry | PASS | Shows the six-option navigation once; accepts number or natural language; does not start a route or questionnaire. |
| explicit-error-bypasses-menu | PASS | Bypasses navigation for 401; gives one safe check, a visible success signal, and no request for secrets. |
| numeric-stuck-selection | PASS | With the menu in prior context, `4` routes to problem solving and asks one plain-language discriminating question. |
| unknown-selection | PASS | Offers two or three ordinary choices or one tiny experience task without internal terminology. |
| resume-without-state | PASS | Validates first, invents no history, and offers exactly create-new or specify-workspace. |
| beginner-hides-internals | PASS | Shows one action and one observable completion signal while hiding raw structured state. |
| professional-shows-state | PASS | Shows requested evidence, assumptions, gates, versions, and canonical `engine_result` without weakening evidence rules. |
| capacity-drop | PASS | Classifies capacity change, asks whether it is temporary or persistent, then routes `week` or feasibility-changing `roadmap` impact. |
| learning-goal-change | PASS | Classifies `goal_system` before Goal Analysis, preserves history, and recomputes affected downstream artifacts. |

The first evaluation identified a conflict between unconditional Roadmap checks and minimum-impact weekly changes. After the runtime contracts were unified, the evaluator reran `capacity-drop` and `learning-goal-change`; both passed and no routing conflict remained.
