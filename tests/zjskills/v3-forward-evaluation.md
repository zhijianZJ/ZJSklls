# ZJSkills 3.0 Forward Evaluation

Ten outputs were produced in distinct fresh contexts from only the fixed Skill-path prefix and the exact scenario prompt. The initial raw outputs are preserved at `/private/tmp/zjskills-v3-eval.Ih7Owf/`. One observed failure was corrected with RED/GREEN evidence and rerun in a fresh context; its replacement is `/private/tmp/zjskills-v3-reeval.33cNEQ/non-ai-without-source.md`.

Question counts below count requests for missing user context, not questions embedded inside a learning exercise. Main actions count the single immediate action, not later conditional interpretation or fallback checks.

| Scenario | Mode | Questions | Main actions | Evidence boundary | Promise boundary | Neutral | Beginner readable | Concise | Verdict |
|---|---|---:|---:|---|---|---|---|---|---|
| `vague-ai-transition` | Career diagnosis, decisive-question gate | 1 | 1 (name the paid result) | Pass: explicitly seeks the one fact needed before judging | Pass: no external outcome claim | Yes | Yes | Yes | PASS |
| `compare-agent-vibe` | Career diagnosis | 0 | 1 (weekend build/deploy/debug project) | Pass: known facts, inference, and uncertainty are explicit | Pass: validation is not framed as job proof | Yes | Yes | Yes | PASS |
| `no-coding-evidence` | Career diagnosis | 0 | 1 (4–6 hour build-and-debug validation) | Pass: zero coding evidence limits the judgment | Pass: no employment or salary promise | Yes | Yes | Yes | PASS |
| `training-decision` | Career diagnosis | 0 | 1 (second project with one review) | Pass: observed project, inference, and missing transfer evidence are separate | Pass: support is not presented as guaranteed success | Yes | Yes | Yes | PASS |
| `concept-confusion` | Learning help | 0 | 1 (one retrieval-vs-context explanation exercise) | Pass: explanation distinguishes the concept and its likely confusion | Pass: no capability or career promise | Yes | Yes | Yes | PASS |
| `incomplete-error` | Learning help, decisive-question gate | 1 | 1 (rerun and provide the complete first error) | Pass: refuses diagnosis without exact error evidence | Pass: no guaranteed technical result | Yes | Yes | Yes | PASS |
| `missed-week` | Learning help | 0 | 1 (10-minute capacity review) | Pass: one-off interruption versus capacity mismatch remains uncertain | Pass: no guaranteed recovery claim | Yes | Yes | Yes | PASS |
| `changed-goal` | Learning route | 0 | 1 (five-case before/after comparison) | Pass: starting facts, absent capability evidence, and main assumption are clear | Pass: no transition or promotion promise | Yes | Yes | Yes | PASS |
| `non-ai-without-source` | Learning route, domain-evidence gate | 1 | 1 (provide employment jurisdiction) | Pass after rerun: states non-AI boundary and withholds route pending official local standards | Pass: no licensing or employment guarantee | Yes | Yes | Yes | PASS |
| `enough-context-no-question` | Learning help | 0 | 1 (automate one reporting step) | Pass: uses supplied constraints and separates career-switch uncertainty | Pass: automation is not framed as career proof | Yes | Yes | Yes | PASS |

## Cross-scenario evidence notes

- Promise boundary: none of the final ten outputs promises employment, income, promotion, admission, client results, or another external outcome.
- Commercial neutrality: no final output converts toward a course, provider, community, or referral. Course-related scenarios compare support by evidence and feedback value.
- Beginner readability: every final output uses direct language, a bounded next step, and an observable completion signal or a single decisive question.
- Initial observed failure: `non-ai-without-source` supplied detailed nutrition licensing and readiness claims without user-provided domain evidence, so it failed evidence and domain-authority boundaries despite otherwise neutral wording.
- Replacement evidence: the fresh rerun asks only for jurisdiction, plainly identifies nutrition as outside AI, and defers the route until local official standards can be used.
