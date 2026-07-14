# Learning Architect

[中文文档](README.zh-CN.md)

**Build personalized learning systems, not just learning plans.**

Learning Architect is an outcome-driven Education OS (Education Operating System) skill for designing, validating, and continuously improving a learner's path to a real result: employment, promotion, entrepreneurship, or project delivery.

It treats learning as capability building. Courses and resources are optional inputs; demonstrated behavior, authentic projects, assessment evidence, and feasible practice are the system's outputs.

## What it does

- Collects a decision-ready learner profile, including constraints, baseline evidence, motivation, and risks.
- Translates a target outcome into competencies, prerequisite-safe curriculum, authentic projects, milestones, weekly commitments, and assessment gates.
- Keeps plans adaptive: target, constraint, assessment, and domain changes create versioned updates and revalidate affected downstream artifacts.
- Distinguishes self-report, evidence, inference, and assumptions; prevents course completion or certificates from being treated as capability proof.
- Includes an initial AI Agent Engineer Domain Pack and reusable contracts for additional occupations.

## Workflow

```text
Discovery → Goal Analysis → Gap Analysis → Competency Design
→ Curriculum Design → Project Design → Roadmap → Weekly Planner
→ Assessment → Outcome Preparation → Continuous Optimization
```

Every stage has an explicit gate. If evidence is missing or a learner cannot yet perform independently, the system returns to the earliest causal gap instead of simply adding more content.

## Contents

| Location | Purpose |
| --- | --- |
| `learning-architect/SKILL.md` | Core operating contract and workflow router |
| `learning-architect/references/` | Detailed engines for discovery, competency, curriculum, projects, assessment, outcomes, and optimization |
| `learning-architect/assets/schemas/` | Machine-readable learner-system contracts |
| `learning-architect/assets/templates/` | Starting shapes for learner artifacts |
| `learning-architect/assets/domain-packs/ai-agent.yaml` | Initial AI Agent Engineer domain pack |
| `learning-architect/scripts/validate_learning_system.py` | Offline validator for learner-system artifacts |
| `tests/learning-architect/` | Regression tests and valid/invalid fixtures |

## Use it

Once installed in Codex, ask naturally, for example:

> I want an AI Agent Engineer job in six months. I can study 12 hours per week, have basic Python, and need a project-first path. Use Learning Architect.

The skill starts with only the questions that can change the current decision. It then returns both a concise explanation and traceable `engine_result` structured state.

## Validation

For repository regression checks, run these commands from the repository root:

```bash
python3 "${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-creator/scripts/quick_validate.py" learning-architect
python3 -m unittest tests/learning-architect/test_validate_learning_system.py -q
python3 learning-architect/scripts/validate_learning_system.py \
  --skill-root learning-architect \
  --learner-dir tests/learning-architect/fixtures/valid-learner
```

The current suite contains 84 tests covering schema validation, dependency cycles, evidence references, active-version governance, project contracts, and Domain Pack scoring gates.

To check an installed copy's skill structure without the repository fixtures (this is not the full regression suite):

```bash
SKILL_ROOT="${CODEX_HOME:-$HOME/.codex}/skills/learning-architect"
python3 "${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-creator/scripts/quick_validate.py" "$SKILL_ROOT"
```

## Add another domain

Do not rewrite the core skill for a new occupation. Add a versioned Domain Pack with target outcomes, competency seeds, dependencies, project archetypes, evidence requirements, and sourcing metadata. The existing workflow and validation contracts then remain reusable across careers.
