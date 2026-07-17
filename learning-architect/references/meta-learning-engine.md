# Meta-Learning Engine

## Purpose

The Meta-Learning Engine adapts how the plan distributes theory, practice, retrieval, and review without diagnosing personality, intelligence, diligence, motivation, or learner character. It consumes dated plan/actual hours, assessment evidence, error patterns, retention checks, learner-reported accessibility and sustainability, and project performance.

## Evidence-based adaptations

Represent the active mix as explicit ratios whose sum is 1.0: `theory_ratio`, `practice_ratio`, and `review_ratio`. The review share includes retrieval practice and spaced review. Use a small, time-boxed change and state the prediction:

- repeated explanation gaps with adequate practice evidence may increase theory briefly;
- guided success but weak independent performance increases varied independent practice and fades scaffolding;
- successful immediate performance but weak delayed recall increases retrieval practice and shortens the first spaced review interval;
- stable recall with weak `modify`, `debug`, `deploy`, or `teach` performance increases transfer practice;
- overload reduces total scope and protects the minimum effective review dose before changing ratios.

Do not label a modality as the learner's fixed “style.” A preference may shape accessibility or format, but only observed outcome evidence justifies a learning-method claim. Do not make multiple major ratio changes in one review unless safety requires it; otherwise the effect cannot be attributed.

## Experiment and rollback

Record baseline evidence, candidate ratios, one hypothesis, duration, success measure, minimum delivery impact, and `review_at` in a versioned optimization event. Keep the current version active until the candidate passes capacity and dependency gates. If the expected assessment or sustainability effect is absent, restore the prior ratios and diagnose the next smallest causal factor. Preserve all versions and observations.

Return a natural-language explanation plus the canonical `engine_result` from `workflow.md` with `engine: meta-learning`, enum confidence, ratio and experiment decisions, evidence refs, optimization artifact/version, affected weekly plans and assessments, gate details, and one next action.
