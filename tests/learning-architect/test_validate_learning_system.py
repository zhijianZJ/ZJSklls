from pathlib import Path
from collections import Counter
import importlib.util
import shutil
import subprocess
import sys
import tempfile
import unittest
from datetime import date, timedelta

import yaml
from jsonschema import FormatChecker

ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / "learning-architect/scripts/validate_learning_system.py"


def load_validator():
    spec = importlib.util.spec_from_file_location("learning_validator", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class LearningSystemValidationTests(unittest.TestCase):
    CANONICAL_LEVEL_MARKERS = {
        "L0": ("no exposure",),
        "L1": ("recognize", "explain basics"),
        "L2": ("complete with example/template/guidance",),
        "L3": ("independently complete a bounded real task",),
        "L4": ("debug", "optimize", "migrate", "handle exceptions"),
        "L5": ("architect", "review", "teach"),
    }
    PROJECT_ARCHETYPE_IDS = {
        "focused-tool",
        "knowledge-application",
        "workflow",
        "enterprise-scenario",
        "portfolio-case",
        "real-external-delivery",
    }
    PROJECT_EVIDENCE_FIELDS = {
        "inputs",
        "constraints",
        "deliverables",
        "competency_ids",
        "business_value",
        "common_failure_modes",
        "demonstration_requirements",
        "documentation_requirements",
        "retrospective_requirements",
        "rubric",
    }
    RUBRIC_DIMENSIONS = {
        "correctness",
        "capability_behavior",
        "reliability",
        "responsible_practice",
        "business_value",
        "technical_communication",
    }
    PERFORMANCE_BANDS = {
        "insufficient",
        "developing",
        "proficient",
        "strong",
    }
    ASSESSMENT_CAPABILITY_CHECKS = {
        "independent-completion",
        "explain-trade-offs",
        "modify-requirements",
        "debug",
        "deploy-deliver",
        "teach-review",
    }
    ASSESSMENT_RESULT_LEVELS = {
        "understanding",
        "guided",
        "independent",
        "transfer",
    }
    CANONICAL_ASSESSMENT_BEHAVIORS = {
        "independent",
        "explain",
        "modify",
        "debug",
        "deploy",
        "teach",
    }
    ADAPTIVE_ENGINE_NAMES = [
        "roadmap-engine.md",
        "planner-engine.md",
        "assessment-engine.md",
        "outcome-engine.md",
        "optimization-engine.md",
        "meta-learning-engine.md",
    ]
    ADAPTIVE_TEMPLATE_NAMES = [
        "discovery.yaml",
        "weekly-plan.yaml",
        "project-brief.yaml",
        "progress-review.yaml",
    ]

    @classmethod
    def setUpClass(cls):
        cls.validator = load_validator()
        cls.skill_root = ROOT / "learning-architect"
        cls.fixtures = ROOT / "tests/learning-architect/fixtures"

    def test_skill_assets_and_valid_learner_pass(self):
        self.assertEqual(self.validator.validate_skill_assets(self.skill_root), [])
        self.assertEqual(
            self.validator.validate_learner_system(
                self.skill_root, self.fixtures / "valid-learner"
            ),
            [],
        )
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary_root = Path(temporary_directory)
            missing = temporary_root / "missing"
            self.assertTrue(
                any(
                    "does not exist" in error
                    for error in self.validator.validate_learner_system(
                        self.skill_root, missing
                    )
                )
            )

            empty = temporary_root / "empty"
            empty.mkdir()
            self.assertTrue(
                any(
                    "contains no YAML artifacts" in error
                    for error in self.validator.validate_learner_system(
                        self.skill_root, empty
                    )
                )
            )

            history_only = temporary_root / "history-only"
            history = history_only / "history"
            history.mkdir(parents=True)
            shutil.copy2(
                self.fixtures / "valid-learner" / "system-state.yaml",
                history / "system-state.yaml",
            )
            self.assertTrue(
                any(
                    "active root system-state.yaml" in error
                    for error in self.validator.validate_learner_system(
                        self.skill_root, history_only
                    )
                )
            )

            for current_stage in ("assessment", "continuous-optimization"):
                with self.subTest(root_only_stage=current_stage):
                    root_only = temporary_root / f"root-only-{current_stage}"
                    root_only.mkdir()
                    state = yaml.safe_load(
                        (self.fixtures / "valid-learner" / "system-state.yaml").read_text(
                            encoding="utf-8"
                        )
                    )
                    state["current_stage"] = current_stage
                    for stage in self.validator.CANONICAL_STAGES:
                        if stage == current_stage:
                            state["stage_states"][stage] = {"state": "active"}
                        elif self.validator.CANONICAL_STAGES.index(stage) < self.validator.CANONICAL_STAGES.index(current_stage):
                            state["stage_states"][stage] = {"state": "validated"}
                        else:
                            state["stage_states"][stage] = {"state": "not_started"}
                    state["active_versions"] = {"system-state": 1}
                    (root_only / "system-state.yaml").write_text(
                        yaml.safe_dump(state), encoding="utf-8"
                    )
                    root_only_errors = self.validator.validate_learner_system(
                        self.skill_root, root_only
                    )
                    self.assertTrue(
                        any(
                            "Stage discovery is validated but requires active learner-profile"
                            in error
                            for error in root_only_errors
                        ),
                        root_only_errors,
                    )

        stage_artifact_cases = (
            ("discovery", "learner-profile", "learner-profile.yaml"),
            ("goal-analysis", "target-outcome", "target-outcome.yaml"),
            ("competency-design", "competency-model", "competency-model.yaml"),
            ("curriculum-design", "curriculum-graph", "curriculum-graph.yaml"),
            ("project-design", "project", None),
            ("roadmap", "learning-roadmap", None),
            ("weekly-planner", "weekly-plan", None),
            ("assessment", "assessment", "assessment.yaml"),
            ("outcome-preparation", "evidence", "evidence.yaml"),
            ("continuous-optimization", "optimization-state", None),
        )
        for stage, artifact_type, artifact_file in stage_artifact_cases:
            with self.subTest(stage_missing_artifact=stage), self.copied_valid_learner() as learner_dir:
                state_path = learner_dir / "system-state.yaml"
                state = yaml.safe_load(state_path.read_text(encoding="utf-8"))
                state["stage_states"][stage] = {"state": "validated"}
                state_path.write_text(yaml.safe_dump(state), encoding="utf-8")
                if artifact_file is not None:
                    (learner_dir / artifact_file).unlink()
                stage_errors = self.validator.validate_learner_system(
                    self.skill_root, learner_dir
                )
                self.assertTrue(
                    any(
                        f"Stage {stage} is validated but requires active {artifact_type}"
                        in error
                        for error in stage_errors
                    ),
                    stage_errors,
                )

    def test_skill_entrypoint_exposes_progressive_workflow_contract(self):
        skill_path = self.skill_root / "SKILL.md"
        self.assertTrue(skill_path.is_file(), f"Missing Skill entrypoint: {skill_path}")

        text = skill_path.read_text(encoding="utf-8")
        self.assertTrue(text.startswith("---\n"))
        _, frontmatter_text, body = text.split("---", 2)
        frontmatter = yaml.safe_load(frontmatter_text)
        self.assertEqual(set(frontmatter), {"name", "description"})
        self.assertEqual(frontmatter["name"], "learning-architect")
        self.assertTrue(frontmatter["description"].startswith("Use when "))

        self.assertIn("## Identity Contract", body)
        stages = [
            "Discovery",
            "Goal Analysis",
            "Gap Analysis",
            "Competency Design",
            "Curriculum Design",
            "Project Design",
            "Roadmap",
            "Weekly Planner",
            "Assessment",
            "Outcome Preparation",
            "Continuous Optimization",
        ]
        positions = []
        for number, stage in enumerate(stages, start=1):
            marker = f"{number}. **{stage}**"
            self.assertIn(marker, body)
            positions.append(body.index(marker))
        self.assertEqual(positions, sorted(positions))

        self.assertIn("| Observable condition | Load |", body)
        self.assertIn("Never treat course completion as capability evidence", body)
        self.assertIn("Do not silently skip stages", body)

    def test_core_references_expose_required_contracts(self):
        reference_names = [
            "persona.md",
            "philosophy.md",
            "workflow.md",
            "discovery.md",
            "goal-analysis.md",
            "gap-analysis.md",
        ]
        reference_paths = [
            self.skill_root / "references" / name for name in reference_names
        ]
        missing = [path.name for path in reference_paths if not path.is_file()]
        self.assertEqual(missing, [], f"Missing core reference files: {missing}")

        combined_text = "\n".join(
            path.read_text(encoding="utf-8") for path in reference_paths
        )
        required_tokens = [
            "Learning System Architect",
            "not a course recommender",
            "not_applicable",
            "needs_input",
            "Strength",
            "Weakness",
            "Opportunity",
            "Risk",
            "SMART",
            "OKR",
            "Backward Design",
            "source",
            "confidence",
            "affected_downstream",
        ]
        missing_tokens = [
            token for token in required_tokens if token not in combined_text
        ]
        self.assertEqual(missing_tokens, [], f"Missing contract tokens: {missing_tokens}")

    def test_workflow_guards_persistent_state_and_multi_goal_conflicts(self):
        workflow = (
            self.skill_root / "references" / "workflow.md"
        ).read_text(encoding="utf-8")
        required_tokens = [
            "loaded snapshot",
            "active version",
            "updated_at",
            "content hash",
            "externally modified",
            "stop automatic writes",
            "merge decision",
            "corrupted state",
            "validation errors",
            "most recent valid version",
            "recovery trace",
            "primary goal",
            "secondary goal",
            "deferred goal",
            "full-time routes",
        ]
        missing = [token for token in required_tokens if token not in workflow]
        self.assertEqual(missing, [], f"Missing state/conflict rules: {missing}")

    def test_philosophy_covers_local_privacy_high_risk_review_and_override(self):
        philosophy = (
            self.skill_root / "references" / "philosophy.md"
        ).read_text(encoding="utf-8").lower()
        required_tokens = [
            "user-designated local directory",
            "medical",
            "legal",
            "financial",
            "high-risk",
            "qualified professional review",
            "override a recommendation",
            "override reason",
            "explained risks",
            "affected_downstream",
            "revalidation",
        ]
        missing = [token for token in required_tokens if token not in philosophy]
        self.assertEqual(missing, [], f"Missing privacy/safety rules: {missing}")

    def test_core_engines_return_canonical_engine_result(self):
        references = self.skill_root / "references"
        workflow_text = (references / "workflow.md").read_text(encoding="utf-8")
        wrapper_fields = [
            "engine",
            "run_id",
            "status",
            "summary",
            "inputs_used",
            "decisions",
            "evidence_refs",
            "assumptions",
            "confidence",
            "artifacts_written",
            "affected_downstream",
            "gate",
            "next_action",
        ]
        contract_text = workflow_text.split("```yaml", 1)[1].split("```", 1)[0]
        engine_result = yaml.safe_load(contract_text)["engine_result"]
        missing_fields = [field for field in wrapper_fields if field not in engine_result]
        missing_fields.extend(
            f"gate.{field}"
            for field in ["passed", "missing"]
            if field not in engine_result.get("gate", {})
        )
        self.assertEqual(missing_fields, [], f"Missing engine_result fields: {missing_fields}")

        for name in ["discovery.md", "goal-analysis.md", "gap-analysis.md"]:
            with self.subTest(reference=name):
                text = (references / name).read_text(encoding="utf-8")
                self.assertIn("engine_result", text)
                self.assertIn("natural-language explanation", text)

    def test_adaptive_engines_and_worked_templates_exist(self):
        references = self.skill_root / "references"
        templates = self.skill_root / "assets" / "templates"
        missing_engines = [
            name for name in self.ADAPTIVE_ENGINE_NAMES
            if not (references / name).is_file()
        ]
        missing_templates = [
            name for name in self.ADAPTIVE_TEMPLATE_NAMES
            if not (templates / name).is_file()
        ]
        self.assertEqual(missing_engines, [], f"Missing adaptive engines: {missing_engines}")
        self.assertEqual(missing_templates, [], f"Missing worked templates: {missing_templates}")

    def test_adaptive_engines_expose_required_contracts(self):
        references = self.skill_root / "references"
        combined_text = "\n".join(
            (references / name).read_text(encoding="utf-8")
            for name in self.ADAPTIVE_ENGINE_NAMES
        )
        required_tokens = [
            "buffer_ratio",
            "minimum_delivery",
            "independent",
            "explain",
            "modify",
            "debug",
            "deploy",
            "teach",
            "employment",
            "entrepreneurship",
            "promotion",
            "project_delivery",
            "scheduled",
            "behavioral",
            "quality",
            "goal_change",
            "domain_update",
            "retrieval practice",
            "spaced review",
        ]
        missing_tokens = [token for token in required_tokens if token not in combined_text]
        self.assertEqual(missing_tokens, [], f"Missing adaptive-engine tokens: {missing_tokens}")
        for name in self.ADAPTIVE_ENGINE_NAMES:
            with self.subTest(reference=name):
                text = (references / name).read_text(encoding="utf-8")
                self.assertIn("engine_result", text)
                self.assertIn("natural-language explanation", text)

    def test_adaptive_engine_semantics_are_executable(self):
        references = self.skill_root / "references"
        curriculum = (references / "curriculum-engine.md").read_text(encoding="utf-8")
        project = (references / "project-engine.md").read_text(encoding="utf-8")
        roadmap = (references / "roadmap-engine.md").read_text(encoding="utf-8")
        assessment = (references / "assessment-engine.md").read_text(encoding="utf-8")
        outcome = (references / "outcome-engine.md").read_text(encoding="utf-8")
        optimization = (references / "optimization-engine.md").read_text(encoding="utf-8")

        self.assertIn("positive integer `content_version`", curriculum)
        self.assertIn("positive integer `content_version`", project)

        for token in [
            "weekly_delivery_hours[week]",
            "phase_delivery_hours = sum",
            "milestone_buffer_hours",
        ]:
            self.assertIn(token, roadmap)
        for token in ["critical", "passing_threshold", "gate.missing"]:
            self.assertIn(token, assessment)
        for token in [
            "JD matching",
            "technical interview prep",
            "HR interview",
            "offer analysis",
            "acquisition experiment",
            "unit economics",
            "competency-gap material",
            "business impact/performance evidence",
            "communication material",
            "negotiation prep",
            "retrospective",
        ]:
            self.assertIn(token, outcome)
        for token in [
            "Never overwrite active history",
            "active -> superseded -> archived",
            "goal_change` -> Goal Analysis",
            "domain_update` -> Gap, Competency, Curriculum, and Project",
        ]:
            self.assertIn(token, optimization)

    def test_assessment_schema_accepts_all_six_passing_behaviors(self):
        document = self.make_assessment_document()
        self.assertEqual(self.schema_issues("assessment", document), [])

        evidence = yaml.safe_load(
            (self.fixtures / "valid-learner" / "evidence.yaml").read_text(
                encoding="utf-8"
            )
        )
        self.assertIsInstance(evidence["observed_behaviors"][0], dict)
        self.assertEqual(self.schema_issues("evidence", evidence), [])

    def test_assessment_schema_rejects_missing_behavior(self):
        document = self.make_assessment_document()
        document["behavior_checks"] = document["behavior_checks"][:-1]
        self.assertTrue(self.schema_issues("assessment", document))

    def test_assessment_schema_accepts_explicit_not_applicable_with_reason(self):
        document = self.make_assessment_document()
        teach = document["behavior_checks"][-1]
        teach.update(
            applicability="not_applicable",
            state="not_applicable",
            evidence_ids=[],
            reason="The bounded L3 assessment does not make peer instruction decision-relevant.",
        )
        self.assertEqual(self.schema_issues("assessment", document), [])

        del teach["reason"]
        self.assertTrue(self.schema_issues("assessment", document))

    def test_assessment_gate_records_applicable_missing_or_failing_evidence(self):
        for mutation in ["missing_evidence", "failed_behavior"]:
            with self.subTest(mutation=mutation):
                document = self.make_assessment_document()
                independent = next(
                    item
                    for item in document["behavior_checks"]
                    if item["behavior"] == "independent"
                )
                if mutation == "missing_evidence":
                    independent["evidence_ids"] = []
                else:
                    independent["state"] = "fail"
                document["decision"] = "needs_remediation"
                document["gate"] = {"passed": False, "missing": ["independent"]}
                self.assertEqual(self.schema_issues("assessment", document), [])

                document["gate"] = {"passed": True, "missing": []}
                self.assertTrue(self.schema_issues("assessment", document))

    def test_valid_learner_has_semantically_linked_assessment_evidence(self):
        assessment_path = self.fixtures / "valid-learner" / "assessment.yaml"
        self.assertTrue(assessment_path.is_file())
        errors = self.validator.validate_learner_system(
            self.skill_root, self.fixtures / "valid-learner"
        )
        self.assertEqual(errors, [])

    def test_assessment_semantics_reject_fake_evidence_ids(self):
        for location in ["top_level", "behavior"]:
            with self.subTest(location=location), tempfile.TemporaryDirectory() as temporary_directory:
                learner_dir = Path(temporary_directory) / "learner"
                shutil.copytree(self.fixtures / "valid-learner", learner_dir)
                assessment_path = learner_dir / "assessment.yaml"
                assessment = yaml.safe_load(
                    assessment_path.read_text(encoding="utf-8")
                )
                if location == "top_level":
                    assessment["evidence_ids"] = ["fake-evidence-id"]
                else:
                    assessment["behavior_checks"][0]["evidence_ids"] = [
                        "fake-evidence-id"
                    ]
                assessment_path.write_text(
                    yaml.safe_dump(assessment), encoding="utf-8"
                )
                errors = self.validator.validate_learner_system(
                    self.skill_root, learner_dir
                )
                self.assertTrue(
                    any("unknown Evidence record" in error for error in errors),
                    errors,
                )

    def test_assessment_semantics_require_matching_passing_observation(self):
        for mutation in ["missing_behavior", "failing_observation"]:
            with self.subTest(mutation=mutation), tempfile.TemporaryDirectory() as temporary_directory:
                learner_dir = Path(temporary_directory) / "learner"
                shutil.copytree(self.fixtures / "valid-learner", learner_dir)
                evidence_path = learner_dir / "evidence.yaml"
                evidence = yaml.safe_load(evidence_path.read_text(encoding="utf-8"))
                explain = next(
                    item
                    for item in evidence["observed_behaviors"]
                    if item["behavior"] == "explain"
                )
                if mutation == "missing_behavior":
                    evidence["observed_behaviors"].remove(explain)
                else:
                    explain["state"] = "fail"
                evidence_path.write_text(
                    yaml.safe_dump(evidence), encoding="utf-8"
                )
                errors = self.validator.validate_learner_system(
                    self.skill_root, learner_dir
                )
                self.assertTrue(
                    any(
                        "matching observed behavior state: explain=pass" in error
                        for error in errors
                    ),
                    errors,
                )

    def test_assessment_semantics_match_resolved_failure_state(self):
        for evidence_state, should_pass in [("fail", True), ("pass", False)]:
            with self.subTest(evidence_state=evidence_state), tempfile.TemporaryDirectory() as temporary_directory:
                learner_dir = Path(temporary_directory) / "learner"
                shutil.copytree(self.fixtures / "valid-learner", learner_dir)

                assessment_path = learner_dir / "assessment.yaml"
                assessment = yaml.safe_load(
                    assessment_path.read_text(encoding="utf-8")
                )
                independent_check = next(
                    item
                    for item in assessment["behavior_checks"]
                    if item["behavior"] == "independent"
                )
                independent_check["state"] = "fail"
                assessment["decision"] = "fail"
                assessment["gate"] = {
                    "passed": False,
                    "missing": ["independent"],
                }
                assessment_path.write_text(
                    yaml.safe_dump(assessment), encoding="utf-8"
                )

                evidence_path = learner_dir / "evidence.yaml"
                evidence = yaml.safe_load(
                    evidence_path.read_text(encoding="utf-8")
                )
                independent_observation = next(
                    item
                    for item in evidence["observed_behaviors"]
                    if item["behavior"] == "independent"
                )
                independent_observation["state"] = evidence_state
                evidence_path.write_text(
                    yaml.safe_dump(evidence), encoding="utf-8"
                )

                errors = self.validator.validate_learner_system(
                    self.skill_root, learner_dir
                )
                if should_pass:
                    self.assertEqual(errors, [])
                else:
                    self.assertTrue(
                        any(
                            "matching observed behavior state: independent=fail"
                            in error
                            for error in errors
                        ),
                        errors,
                    )

    def test_passing_assessment_rejects_all_six_not_applicable(self):
        document = self.make_assessment_document()
        for check in document["behavior_checks"]:
            check.update(
                applicability="not_applicable",
                state="not_applicable",
                evidence_ids=[],
                reason=f"{check['behavior']} was excluded by the worked counterexample.",
            )
        self.assertTrue(self.schema_issues("assessment", document))

    def test_roadmap_schema_requires_budget_feasibility(self):
        schemas, _ = self.validator._load_schemas(self.skill_root)
        roadmap = schemas["learning-roadmap"]
        self.assertTrue(
            {"budget", "total_estimated_cost", "currency"}
            <= set(roadmap["required"])
        )
        phase = roadmap["properties"]["phases"]["items"]
        self.assertTrue({"estimated_cost", "currency"} <= set(phase["required"]))
        roadmap_text = (
            self.skill_root / "references" / "roadmap-engine.md"
        ).read_text(encoding="utf-8")
        for token in [
            "total_estimated_cost = sum",
            "total_estimated_cost <= budget.amount",
            "budget source",
            "currency",
        ]:
            self.assertIn(token, roadmap_text)

    def test_roadmap_budget_semantics_are_validated(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            learner_dir = Path(temporary_directory) / "learner"
            shutil.copytree(self.fixtures / "valid-learner", learner_dir)
            roadmap = {
                "id": "roadmap-budget-test",
                "schema_version": "1.0.0",
                "content_version": 1,
                "status": "active",
                "source": "budget test",
                "confidence": "high",
                "created_at": "2026-07-13T00:00:00Z",
                "updated_at": "2026-07-13T00:00:00Z",
                "budget": {"amount": 1000, "source": "learner confirmed"},
                "currency": "CNY",
                "total_estimated_cost": 1200,
                "phases": [
                    {
                        "id": "phase-1",
                        "outcome": "First evidence",
                        "milestones": [],
                        "project_ids": [],
                        "weekly_capacity_hours": 8,
                        "buffer_ratio": 0.2,
                        "estimated_cost": 700,
                        "currency": "CNY",
                    },
                    {
                        "id": "phase-2",
                        "outcome": "Second evidence",
                        "milestones": [],
                        "project_ids": [],
                        "weekly_capacity_hours": 8,
                        "buffer_ratio": 0.2,
                        "estimated_cost": 400,
                        "currency": "USD",
                    },
                ],
            }
            (learner_dir / "learning-roadmap.yaml").write_text(
                yaml.safe_dump(roadmap), encoding="utf-8"
            )
            errors = self.validator.validate_learner_system(
                self.skill_root, learner_dir
            )
            self.assertTrue(any("phase cost sum" in error for error in errors), errors)
            self.assertTrue(any("budget" in error.lower() for error in errors), errors)
            self.assertTrue(any("currency" in error.lower() for error in errors), errors)

    def test_optimization_trigger_enum_is_exact(self):
        schemas, registry = self.validator._load_schemas(self.skill_root)
        schema = schemas["optimization-state"]
        expected = {"scheduled", "behavioral", "quality", "goal_change", "domain_update"}
        self.assertEqual(set(schema["properties"]["trigger"]["enum"]), expected)

        progress = yaml.safe_load(
            (self.skill_root / "assets" / "templates" / "progress-review.yaml").read_text(
                encoding="utf-8"
            )
        )
        progress["trigger"] = "unsupported"
        issues = list(
            self.validator.Draft202012Validator(
                schema, registry=registry, format_checker=FormatChecker()
            ).iter_errors(progress)
        )
        self.assertTrue(issues)

    def test_adaptive_templates_are_worked_and_match_schema_contracts(self):
        templates = self.skill_root / "assets" / "templates"
        template_to_schema = {
            "discovery.yaml": "learner-profile",
            "weekly-plan.yaml": "weekly-plan",
            "project-brief.yaml": "project",
            "progress-review.yaml": "optimization-state",
        }
        schemas, registry = self.validator._load_schemas(self.skill_root)
        documents = {}
        for name, schema_name in template_to_schema.items():
            with self.subTest(template=name):
                document = yaml.safe_load((templates / name).read_text(encoding="utf-8"))
                documents[name] = document
                self.assertIsInstance(document, dict)
                self.assertNotIn(None, document.values())
                issues = list(
                    self.validator.Draft202012Validator(
                        schemas[schema_name],
                        registry=registry,
                        format_checker=FormatChecker(),
                    ).iter_errors(document)
                )
                self.assertEqual([issue.message for issue in issues], [])

        weekly_plan = documents["weekly-plan.yaml"]
        self.assertTrue(
            {
                "capacity_hours",
                "weekly_outcome",
                "tasks",
                "retrieval_practice",
                "project_work",
                "minimum_delivery",
                "risk",
                "review",
            }
            <= weekly_plan.keys()
        )
        self.assertTrue(
            {"project_work", "risk", "review"}
            <= set(schemas["weekly-plan"]["required"])
        )
        task_hours = sum(task["estimated_hours"] for task in weekly_plan["tasks"])
        retrieval_hours = sum(
            item["estimated_hours"] for item in weekly_plan["retrieval_practice"]
        )
        worked_hours = (
            task_hours
            + retrieval_hours
            + weekly_plan["project_work"]["estimated_hours"]
            + weekly_plan["review"]["estimated_hours"]
        )
        self.assertEqual(worked_hours, weekly_plan["extensions"]["planned_load_hours"])
        self.assertLessEqual(
            worked_hours, weekly_plan["extensions"]["usable_capacity_hours"]
        )

        project_brief = documents["project-brief.yaml"]
        rubric_dimension_schema = schemas["project"]["$defs"]["rubric_dimension"]
        self.assertTrue(
            {"critical", "passing_threshold"}
            <= rubric_dimension_schema["properties"].keys()
        )
        self.assertTrue(
            {"critical", "passing_threshold"}
            <= set(rubric_dimension_schema["required"])
        )
        self.assertEqual(
            set(rubric_dimension_schema["properties"]["passing_threshold"]["enum"]),
            {"developing", "proficient", "strong"},
        )
        assessment_text = (
            self.skill_root / "references" / "assessment-engine.md"
        ).read_text(encoding="utf-8")
        self.assertIn("no dimension declares `critical: true`", assessment_text)
        self.assertTrue(any(item["critical"] for item in project_brief["rubric"].values()))
        for name, dimension in project_brief["rubric"].items():
            with self.subTest(rubric_dimension=name):
                self.assertIn("critical", dimension)
                self.assertIn(
                    dimension["passing_threshold"],
                    {"developing", "proficient", "strong"},
                )

        progress_review = documents["progress-review.yaml"]
        self.assertTrue(
            {"trigger", "evidence", "diagnosis", "changes", "expected_effect", "review_at"}
            <= progress_review.keys()
        )
        self.assertTrue(progress_review["evidence"])
        self.assertIn("evidence", schemas["optimization-state"]["required"])
        self.assertNotIn("review_date", progress_review)
        serialized_progress = yaml.safe_dump(progress_review)
        self.assertNotIn("1.1.0", serialized_progress)
        self.assertIn("content version 2", serialized_progress)
        competency_text = (
            self.skill_root / "references" / "competency-engine.md"
        ).read_text(encoding="utf-8")
        domain_text = (
            self.skill_root / "references" / "domain-pack-contract.md"
        ).read_text(encoding="utf-8")
        self.assertIn("positive integer `content_version`", competency_text)
        self.assertIn("positive integer `content_version`", domain_text)

    def test_discovery_starts_with_eight_to_twelve_questions(self):
        text = (
            self.skill_root / "references" / "discovery.md"
        ).read_text(encoding="utf-8")
        self.assertIn("8–12", text)
        self.assertIn("adaptive follow-up", text)
        skill_text = (self.skill_root / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("initial Discovery batch", skill_text)

    def test_discovery_question_bank_contract(self):
        path = self.skill_root / "assets" / "question-banks" / "discovery.yaml"
        questions = yaml.safe_load(path.read_text(encoding="utf-8"))["questions"]
        required_fields = {
            "id",
            "category",
            "question",
            "answer_type",
            "decision_impact",
            "required_when",
            "sensitivity",
        }
        expected_categories = {
            "personal",
            "education",
            "work",
            "technical",
            "projects",
            "learning",
            "motivation",
            "constraints",
        }

        self.assertEqual(len(questions), 48)
        self.assertEqual(len({question["id"] for question in questions}), 48)
        for question in questions:
            with self.subTest(question=question["id"]):
                self.assertTrue(required_fields <= question.keys())
                if question["sensitivity"] == "sensitive":
                    self.assertTrue(question["required_when"].startswith("optional;"))

        category_counts = Counter(question["category"] for question in questions)
        self.assertEqual(set(category_counts), expected_categories)
        self.assertEqual(set(category_counts.values()), {6})

    def test_ai_agent_domain_pack_matches_schema(self):
        pack = self.load_ai_agent_domain_pack()
        schemas, registry = self.validator._load_schemas(self.skill_root)
        issues = sorted(
            self.validator.Draft202012Validator(
                schemas["domain-pack"],
                registry=registry,
                format_checker=FormatChecker(),
            ).iter_errors(pack),
            key=lambda item: list(item.path),
        )
        messages = [
            f"{'.'.join(str(part) for part in issue.path) or '<root>'}: "
            f"{issue.message}"
            for issue in issues
        ]
        self.assertEqual(messages, [])

    def test_domain_pack_review_date_accepts_calendar_date(self):
        pack = self.load_ai_agent_domain_pack()
        issues = self.domain_pack_issues(pack)
        self.assertFalse(
            any(list(issue.path) == ["last_reviewed_at"] for issue in issues),
            [issue.message for issue in issues],
        )

    def test_domain_pack_review_date_rejects_invalid_calendar_date(self):
        pack = self.load_ai_agent_domain_pack()
        pack["last_reviewed_at"] = "2026-02-30"
        issues = self.domain_pack_issues(pack)
        self.assertTrue(
            any(list(issue.path) == ["last_reviewed_at"] for issue in issues),
            [issue.message for issue in issues],
        )

    def test_ai_agent_domain_pack_dependency_endpoints_exist(self):
        pack = self.load_ai_agent_domain_pack()
        competency_ids = {
            competency["id"] for competency in pack["competencies"]
        }
        unknown_endpoints = sorted(
            {
                endpoint
                for dependency in pack["dependencies"]
                for endpoint in (dependency["from"], dependency["to"])
                if endpoint not in competency_ids
            }
        )
        self.assertEqual(unknown_endpoints, [])

    def test_ai_agent_domain_pack_includes_required_competencies(self):
        pack = self.load_ai_agent_domain_pack()
        competency_ids = {
            competency["id"] for competency in pack["competencies"]
        }
        required_ids = {
            "python-foundation",
            "api-integration",
            "prompt-engineering",
            "llm-fundamentals",
            "embedding-retrieval",
            "rag-engineering",
            "tool-calling",
            "agent-workflow",
            "mcp-integration",
            "multi-agent-coordination",
            "evaluation-observability",
            "deployment-security",
            "business-problem-framing",
            "technical-communication",
        }
        self.assertEqual(sorted(required_ids - competency_ids), [])

    def test_ai_agent_competencies_use_canonical_behavior_levels(self):
        pack = self.load_ai_agent_domain_pack()
        for competency in pack["competencies"]:
            with self.subTest(competency=competency["id"]):
                levels = competency["levels"]
                self.assertEqual(set(levels), set(self.CANONICAL_LEVEL_MARKERS))
                for level, markers in self.CANONICAL_LEVEL_MARKERS.items():
                    behavior = levels[level].lower()
                    for marker in markers:
                        self.assertIn(marker, behavior)

    def test_project_contracts_require_complete_evidence_fields(self):
        project_schema = yaml.safe_load(
            (self.skill_root / "assets/schemas/project.schema.yaml").read_text(
                encoding="utf-8"
            )
        )
        self.assertTrue(
            self.PROJECT_EVIDENCE_FIELDS <= set(project_schema["required"])
        )
        self.assertGreaterEqual(
            project_schema["properties"]["constraints"].get("minItems", 0), 1
        )
        rubric_schema = project_schema.get("$defs", {}).get("analytic_rubric", {})
        self.assertEqual(
            set(rubric_schema.get("required", [])),
            self.RUBRIC_DIMENSIONS,
        )

        pack = self.load_ai_agent_domain_pack()
        for archetype in pack["project_archetypes"]:
            with self.subTest(archetype=archetype["id"]):
                self.assertTrue(
                    self.PROJECT_EVIDENCE_FIELDS <= archetype.keys(), archetype
                )
                self.assertTrue(archetype.get("constraints"))
                rubric = archetype.get("rubric", {})
                self.assertEqual(set(rubric), self.RUBRIC_DIMENSIONS)
                self.assertEqual(
                    sum(item.get("weight", 0) for item in rubric.values()), 100
                )
                for dimension in rubric.values():
                    self.assertEqual(
                        set(dimension.get("performance_bands", {})),
                        self.PERFORMANCE_BANDS,
                    )

    def test_assessment_patterns_cover_capability_checks_and_result_levels(self):
        pack = self.load_ai_agent_domain_pack()
        covered_checks = set()
        for pattern in pack["assessment_patterns"]:
            with self.subTest(pattern=pattern["id"]):
                self.assertIn("capability_checks", pattern)
                self.assertIn("result_levels", pattern)
            covered_checks.update(pattern.get("capability_checks", []))
        self.assertEqual(covered_checks, self.ASSESSMENT_CAPABILITY_CHECKS)
        for pattern in pack["assessment_patterns"]:
            with self.subTest(pattern=pattern["id"]):
                self.assertEqual(
                    set(pattern.get("result_levels", {})),
                    self.ASSESSMENT_RESULT_LEVELS,
                )

    def test_ai_agent_pack_has_exact_metadata_archetypes_and_coverage(self):
        pack = self.load_ai_agent_domain_pack()
        self.assertEqual(pack["id"], "ai-agent-engineer")
        self.assertEqual(pack["version"], "1.0.0")
        self.assertEqual(pack["last_reviewed_at"], "2026-07-13")
        self.assertEqual(pack["review_interval_days"], 90)
        self.assertEqual(
            {archetype["id"] for archetype in pack["project_archetypes"]},
            self.PROJECT_ARCHETYPE_IDS,
        )
        competency_ids = {
            competency["id"] for competency in pack["competencies"]
        }
        covered_ids = {
            competency_id
            for archetype in pack["project_archetypes"]
            for competency_id in archetype["competency_ids"]
        }
        self.assertEqual(covered_ids, competency_ids)

    def test_ai_agent_pack_is_acyclic_and_has_no_paid_course_recommendations(self):
        pack = self.load_ai_agent_domain_pack()
        self.assertFalse(self.validator._has_dependency_cycle(pack["dependencies"]))
        deep_dependencies = [
            {"from": f"node-{index}", "to": f"node-{index + 1}"}
            for index in range(2000)
        ]
        try:
            self.assertFalse(
                self.validator._has_dependency_cycle(deep_dependencies)
            )
        except RecursionError as exc:
            self.fail(f"Deep acyclic dependency graphs must not recurse: {exc}")
        deep_dependencies.append({"from": "node-2000", "to": "node-0"})
        self.assertTrue(self.validator._has_dependency_cycle(deep_dependencies))
        pack_text = yaml.safe_dump(pack).lower()
        for forbidden in [
            "udemy.com/course/",
            "coursera.org/learn/",
            "edx.org/learn/",
            "buy this course",
            "enroll in this paid course",
        ]:
            self.assertNotIn(forbidden, pack_text)

    def test_skill_asset_validator_reports_domain_pack_cycle(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            skill_root = Path(temporary_directory) / "learning-architect"
            shutil.copytree(self.skill_root, skill_root)
            pack_path = skill_root / "assets/domain-packs/ai-agent.yaml"
            pack = yaml.safe_load(pack_path.read_text(encoding="utf-8"))
            pack["dependencies"].append(
                {"from": "agent-workflow", "to": "python-foundation"}
            )
            pack_path.write_text(yaml.safe_dump(pack), encoding="utf-8")
            errors = self.validator.validate_skill_assets(skill_root)
            self.assertTrue(
                any("domain pack dependency cycle" in error.lower() for error in errors),
                errors,
            )

    def test_skill_asset_validator_rejects_paid_course_recommendation(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            skill_root = Path(temporary_directory) / "learning-architect"
            shutil.copytree(self.skill_root, skill_root)
            pack_path = skill_root / "assets/domain-packs/ai-agent.yaml"
            pack = yaml.safe_load(pack_path.read_text(encoding="utf-8"))
            pack["target_outcomes"][0]["description"] += (
                " See https://training.example.org/program/agent-engineering"
            )
            pack_path.write_text(yaml.safe_dump(pack), encoding="utf-8")
            errors = self.validator.validate_skill_assets(skill_root)
            self.assertTrue(
                any("url" in error.lower() for error in errors), errors
            )

    def test_skill_asset_validator_rejects_general_course_purchase_language(self):
        for phrase in [
            "Choose this paid course",
            "推荐这门付费课程",
            "建议购买这个 Agent 课程",
            "现在报名高级 Agent 课程",
        ]:
            with self.subTest(phrase=phrase), tempfile.TemporaryDirectory() as temporary_directory:
                skill_root = Path(temporary_directory) / "learning-architect"
                shutil.copytree(self.skill_root, skill_root)
                pack_path = skill_root / "assets/domain-packs/ai-agent.yaml"
                pack = yaml.safe_load(pack_path.read_text(encoding="utf-8"))
                pack["target_outcomes"][0]["description"] += f" {phrase}"
                pack_path.write_text(yaml.safe_dump(pack), encoding="utf-8")
                errors = self.validator.validate_skill_assets(skill_root)
                self.assertTrue(
                    any("paid course" in error.lower() for error in errors), errors
                )

    def test_confidence_enum_is_accepted(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            learner_dir = Path(temporary_directory) / "learner"
            shutil.copytree(self.fixtures / "valid-learner", learner_dir)
            self.set_confidence(learner_dir, "high")

            errors = self.validator.validate_learner_system(
                self.skill_root, learner_dir
            )
            self.assertEqual(errors, [])

    def test_numeric_confidence_is_rejected(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            learner_dir = Path(temporary_directory) / "learner"
            shutil.copytree(self.fixtures / "valid-learner", learner_dir)
            self.set_confidence(learner_dir, 1.0)

            errors = self.validator.validate_learner_system(
                self.skill_root, learner_dir
            )
            self.assertTrue(any("confidence" in error for error in errors), errors)

    def test_curriculum_cycle_is_rejected(self):
        errors = self.validator.validate_learner_system(
            self.skill_root, self.fixtures / "invalid-cycle"
        )
        self.assertTrue(any("cycle" in error.lower() for error in errors), errors)

    def test_unknown_competency_evidence_reference_is_rejected(self):
        errors = self.validator.validate_learner_system(
            self.skill_root, self.fixtures / "invalid-evidence-ref"
        )
        self.assertTrue(any("unknown competency" in error.lower() for error in errors), errors)

    def test_malformed_curriculum_edge_returns_errors_without_traceback(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            learner_dir = Path(temporary_directory) / "learner"
            shutil.copytree(self.fixtures / "valid-learner", learner_dir)
            path = learner_dir / "curriculum-graph.yaml"
            document = yaml.safe_load(path.read_text(encoding="utf-8"))
            del document["dependencies"][0]["to"]
            path.write_text(yaml.safe_dump(document), encoding="utf-8")

            errors = self.validator.validate_learner_system(
                self.skill_root, learner_dir
            )
            self.assertTrue(errors)
            result = self.run_cli(learner_dir)
            self.assertEqual(result.returncode, 1, result)
            self.assertNotIn("Traceback", result.stderr)

    def test_malformed_competency_node_returns_errors_without_traceback(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            learner_dir = Path(temporary_directory) / "learner"
            shutil.copytree(self.fixtures / "valid-learner", learner_dir)
            path = learner_dir / "competency-model.yaml"
            document = yaml.safe_load(path.read_text(encoding="utf-8"))
            del document["competencies"][0]["id"]
            path.write_text(yaml.safe_dump(document), encoding="utf-8")

            errors = self.validator.validate_learner_system(
                self.skill_root, learner_dir
            )
            self.assertTrue(errors)
            result = self.run_cli(learner_dir)
            self.assertEqual(result.returncode, 1, result)
            self.assertNotIn("Traceback", result.stderr)

    def test_recursive_loader_rejects_malformed_nested_project(self):
        with self.copied_valid_learner() as learner_dir:
            path = learner_dir / "projects" / "phase-1" / "broken.yaml"
            path.parent.mkdir(parents=True)
            path.write_text("id: [unterminated\n", encoding="utf-8")
            errors = self.validator.validate_learner_system(self.skill_root, learner_dir)
            self.assertTrue(any("broken.yaml" in error and "invalid" in error.lower() for error in errors), errors)

    def test_recursive_loader_rejects_unknown_yaml_in_known_artifact_directory(self):
        with self.copied_valid_learner() as learner_dir:
            path = learner_dir / "projects" / "notes.yaml"
            path.parent.mkdir(parents=True)
            path.write_text("memo: not-a-project\n", encoding="utf-8")
            errors = self.validator.validate_learner_system(self.skill_root, learner_dir)
            self.assertTrue(any("notes.yaml" in error for error in errors), errors)

    def test_recursive_loader_validates_optimization_and_history_paths(self):
        with self.copied_valid_learner() as learner_dir:
            optimization = learner_dir / "optimization-log.yaml"
            optimization.write_text("trigger: unsupported\n", encoding="utf-8")
            history = learner_dir / "history" / "projects" / "old.yaml"
            history.parent.mkdir(parents=True)
            history.write_text("problem: missing-lifecycle\n", encoding="utf-8")
            errors = self.validator.validate_learner_system(self.skill_root, learner_dir)
            self.assertTrue(any("optimization-log.yaml" in error for error in errors), errors)
            self.assertTrue(any("old.yaml" in error for error in errors), errors)

    def test_active_version_must_match_active_artifact_content_version(self):
        with self.copied_valid_learner() as learner_dir:
            state_path = learner_dir / "system-state.yaml"
            state = yaml.safe_load(state_path.read_text(encoding="utf-8"))
            state["active_versions"]["learner-profile"] = 999
            state_path.write_text(yaml.safe_dump(state), encoding="utf-8")
            errors = self.validator.validate_learner_system(self.skill_root, learner_dir)
            self.assertTrue(any("active version" in error.lower() and "learner-profile" in error for error in errors), errors)

    def test_active_versions_must_uniquely_cover_active_singletons(self):
        with self.copied_valid_learner() as learner_dir:
            state_path = learner_dir / "system-state.yaml"
            state = yaml.safe_load(state_path.read_text(encoding="utf-8"))
            del state["active_versions"]["competency-model"]
            state_path.write_text(yaml.safe_dump(state), encoding="utf-8")

            errors = self.validator.validate_learner_system(
                self.skill_root, learner_dir
            )
            self.assertTrue(
                any(
                    "active_versions must uniquely cover active singleton competency-model"
                    in error.lower()
                    for error in errors
                ),
                errors,
            )

    def test_system_state_rejects_empty_and_nonsense_stage_state(self):
        for mutation in ["empty", "nonsense"]:
            with self.subTest(mutation=mutation), self.copied_valid_learner() as learner_dir:
                path = learner_dir / "system-state.yaml"
                state = yaml.safe_load(path.read_text(encoding="utf-8"))
                if mutation == "empty":
                    state["stage_states"] = {}
                    state["active_versions"] = {}
                else:
                    state["current_stage"] = "foundation"
                    state["stage_states"] = {"foundation": {"state": "banana"}}
                path.write_text(yaml.safe_dump(state), encoding="utf-8")
                errors = self.validator.validate_learner_system(self.skill_root, learner_dir)
                self.assertTrue(errors)

    def test_system_state_rejects_illegal_forward_stage_progression(self):
        with self.copied_valid_learner() as learner_dir:
            path = learner_dir / "system-state.yaml"
            state = yaml.safe_load(path.read_text(encoding="utf-8"))
            state["current_stage"] = "project-design"
            state["stage_states"] = self.canonical_stage_states("not_started")
            state["stage_states"]["discovery"] = {"state": "draft"}
            state["stage_states"]["project-design"] = {"state": "active"}
            path.write_text(yaml.safe_dump(state), encoding="utf-8")
            errors = self.validator.validate_learner_system(self.skill_root, learner_dir)
            self.assertTrue(any("stage progression" in error.lower() for error in errors), errors)

    def test_system_state_rejects_multiple_active_stages(self):
        with self.copied_valid_learner() as learner_dir:
            path = learner_dir / "system-state.yaml"
            state = yaml.safe_load(path.read_text(encoding="utf-8"))
            state["stage_states"]["discovery"] = {"state": "active"}
            path.write_text(yaml.safe_dump(state), encoding="utf-8")
            errors = self.validator.validate_learner_system(self.skill_root, learner_dir)
            self.assertTrue(any("stage progression" in error.lower() for error in errors), errors)

    def test_curriculum_rejects_dangling_dependency_endpoint(self):
        with self.copied_valid_learner() as learner_dir:
            path = learner_dir / "curriculum-graph.yaml"
            graph = yaml.safe_load(path.read_text(encoding="utf-8"))
            graph["dependencies"][0]["to"] = "missing-unit"
            path.write_text(yaml.safe_dump(graph), encoding="utf-8")
            errors = self.validator.validate_learner_system(self.skill_root, learner_dir)
            self.assertTrue(any("unknown curriculum" in error.lower() for error in errors), errors)

    def test_duplicate_competency_ids_are_rejected(self):
        with self.copied_valid_learner() as learner_dir:
            path = learner_dir / "competency-model.yaml"
            model = yaml.safe_load(path.read_text(encoding="utf-8"))
            model["competencies"][1]["id"] = model["competencies"][0]["id"]
            path.write_text(yaml.safe_dump(model), encoding="utf-8")
            errors = self.validator.validate_learner_system(self.skill_root, learner_dir)
            self.assertTrue(any("duplicate competency" in error.lower() for error in errors), errors)

    def test_invalid_learner_timestamp_is_rejected(self):
        with self.copied_valid_learner() as learner_dir:
            path = learner_dir / "learner-profile.yaml"
            profile = yaml.safe_load(path.read_text(encoding="utf-8"))
            profile["updated_at"] = "not-a-timestamp"
            path.write_text(yaml.safe_dump(profile), encoding="utf-8")
            errors = self.validator.validate_learner_system(self.skill_root, learner_dir)
            self.assertTrue(any("updated_at" in error for error in errors), errors)

    def test_common_lifecycle_contract_is_semantic(self):
        profile = yaml.safe_load((self.fixtures / "valid-learner" / "learner-profile.yaml").read_text(encoding="utf-8"))
        profile["schema_version"] = "latest"
        profile["content_version"] = 0
        profile["status"] = "verified"
        issues = self.schema_issues("learner-profile", profile)
        self.assertTrue(any(list(issue.path) == ["schema_version"] for issue in issues), [issue.message for issue in issues])
        self.assertTrue(any(list(issue.path) == ["content_version"] for issue in issues), [issue.message for issue in issues])
        self.assertTrue(any(list(issue.path) == ["status"] for issue in issues), [issue.message for issue in issues])
        for unsupported in ("0.9.0", "2.0.0", "99.0.0"):
            with self.subTest(unsupported_schema_version=unsupported):
                candidate = yaml.safe_load(
                    (self.fixtures / "valid-learner" / "learner-profile.yaml").read_text(
                        encoding="utf-8"
                    )
                )
                candidate["schema_version"] = unsupported
                version_issues = self.schema_issues("learner-profile", candidate)
                self.assertTrue(
                    any(list(issue.path) == ["schema_version"] for issue in version_issues),
                    [issue.message for issue in version_issues],
                )

    def test_competency_contract_rejects_invalid_levels_weights_and_empty_evidence(self):
        model = yaml.safe_load((self.fixtures / "valid-learner" / "competency-model.yaml").read_text(encoding="utf-8"))
        model["competencies"][0].update(current_level=-1, target_level=6, weight=0)
        model["competencies"][0]["behaviors"] = []
        model["competencies"][0]["evidence_requirements"] = []
        self.assertTrue(self.schema_issues("competency-model", model))

    def test_failed_assessment_requires_resolved_failure_evidence(self):
        with self.copied_valid_learner() as learner_dir:
            assessment_path = learner_dir / "assessment.yaml"
            assessment = yaml.safe_load(assessment_path.read_text(encoding="utf-8"))
            failed = next(item for item in assessment["behavior_checks"] if item["behavior"] == "independent")
            failed.update(state="fail", evidence_ids=[])
            assessment["decision"] = "fail"
            assessment["gate"] = {"passed": False, "missing": ["independent"]}
            assessment_path.write_text(yaml.safe_dump(assessment), encoding="utf-8")
            errors = self.validator.validate_learner_system(self.skill_root, learner_dir)
            self.assertTrue(any("failure evidence" in error.lower() for error in errors), errors)

    def test_gate_missing_must_name_failed_or_missing_applicable_behavior(self):
        with self.copied_valid_learner() as learner_dir:
            assessment_path = learner_dir / "assessment.yaml"
            assessment = yaml.safe_load(assessment_path.read_text(encoding="utf-8"))
            assessment["gate"] = {"passed": False, "missing": ["unrelated"]}
            assessment["decision"] = "fail"
            assessment_path.write_text(yaml.safe_dump(assessment), encoding="utf-8")
            errors = self.validator.validate_learner_system(self.skill_root, learner_dir)
            self.assertTrue(any("gate.missing" in error for error in errors), errors)

    def test_domain_pack_patch_version_and_current_review_are_accepted(self):
        pack = self.load_ai_agent_domain_pack()
        pack["version"] = "1.0.1"
        pack["content_version"] = 2
        pack["last_reviewed_at"] = date.today().isoformat()
        self.assertEqual(self.validator._validate_domain_pack_semantics("patch.yaml", pack), [])

    def test_domain_pack_stale_and_invalid_governance_are_rejected(self):
        pack = self.load_ai_agent_domain_pack()
        pack["last_reviewed_at"] = (date.today() - timedelta(days=pack["review_interval_days"] + 1)).isoformat()
        pack["market_assumptions"][0].pop("as_of")
        pack["extensions"]["migration_map"] = {"removed-node": "missing-node"}
        errors = self.validator._validate_domain_pack_semantics("stale.yaml", pack)
        self.assertTrue(any("stale" in error.lower() for error in errors), errors)
        self.assertTrue(any("market assumption" in error.lower() for error in errors), errors)
        self.assertTrue(any("migration" in error.lower() for error in errors), errors)

    def test_domain_pack_allows_source_url_only_in_explicit_field(self):
        pack = self.load_ai_agent_domain_pack()
        pack["market_assumptions"][0]["source_url"] = "https://example.org/research"
        self.assertEqual(self.domain_pack_issues(pack), [])
        self.assertEqual(self.validator._validate_domain_pack_semantics("source-url.yaml", pack), [])

    def test_duplicate_domain_pack_archetype_and_pattern_ids_are_rejected(self):
        pack = self.load_ai_agent_domain_pack()
        pack["project_archetypes"][1]["id"] = pack["project_archetypes"][0]["id"]
        pack["assessment_patterns"][1]["id"] = pack["assessment_patterns"][0]["id"]
        errors = self.validator._validate_domain_pack_semantics("duplicates.yaml", pack)
        self.assertTrue(any("duplicate project archetype" in error.lower() for error in errors), errors)
        self.assertTrue(any("duplicate assessment pattern" in error.lower() for error in errors), errors)

    def test_weekly_plan_semantics_reject_huge_load(self):
        with self.copied_valid_learner() as learner_dir:
            weekly_path = learner_dir / "weekly-plans" / "2026-W29.yaml"
            weekly_path.parent.mkdir(parents=True)
            weekly = yaml.safe_load((self.skill_root / "assets/templates/weekly-plan.yaml").read_text(encoding="utf-8"))
            weekly["capacity_hours"] = 2
            weekly["tasks"][0]["estimated_hours"] = 100
            weekly_path.write_text(yaml.safe_dump(weekly), encoding="utf-8")
            errors = self.validator.validate_learner_system(self.skill_root, learner_dir)
            self.assertTrue(any("weekly" in error.lower() and "capacity" in error.lower() for error in errors), errors)

    def test_cross_artifact_references_resolve(self):
        with self.copied_valid_learner() as learner_dir:
            project_path = learner_dir / "projects" / "project-1.yaml"
            project_path.parent.mkdir(parents=True)
            project = yaml.safe_load((self.skill_root / "assets/templates/project-brief.yaml").read_text(encoding="utf-8"))
            project["competency_ids"] = ["missing-competency"]
            project["status"] = "active"
            project_path.write_text(yaml.safe_dump(project), encoding="utf-8")
            errors = self.validator.validate_learner_system(self.skill_root, learner_dir)
            self.assertTrue(any("project references unknown competency" in error.lower() for error in errors), errors)

    def test_weekly_retrieval_and_profile_evidence_references_resolve(self):
        with self.copied_valid_learner() as learner_dir:
            profile_path = learner_dir / "learner-profile.yaml"
            profile = yaml.safe_load(profile_path.read_text(encoding="utf-8"))
            profile["personal"]["name"]["evidence_ids"] = ["missing-profile-evidence"]
            profile_path.write_text(yaml.safe_dump(profile), encoding="utf-8")
            weekly_path = learner_dir / "weekly-plans" / "2026-W29.yaml"
            weekly_path.parent.mkdir(parents=True)
            weekly = yaml.safe_load((self.skill_root / "assets/templates/weekly-plan.yaml").read_text(encoding="utf-8"))
            weekly["retrieval_practice"][0]["competency_id"] = "missing-retrieval-competency"
            weekly_path.write_text(yaml.safe_dump(weekly), encoding="utf-8")
            errors = self.validator.validate_learner_system(self.skill_root, learner_dir)
            self.assertTrue(any("profile references unknown evidence" in error.lower() for error in errors), errors)
            self.assertTrue(any("retrieval references unknown competency" in error.lower() for error in errors), errors)

    def test_nested_active_version_can_resolve_artifact_id_and_path(self):
        with self.copied_valid_learner() as learner_dir:
            project_path = learner_dir / "projects" / "focused-tool-ticket-intake.yaml"
            project_path.parent.mkdir(parents=True)
            project = yaml.safe_load((self.skill_root / "assets/templates/project-brief.yaml").read_text(encoding="utf-8"))
            project["competency_ids"] = ["python-foundation", "api-integration"]
            project["status"] = "active"
            project_path.write_text(yaml.safe_dump(project), encoding="utf-8")
            state_path = learner_dir / "system-state.yaml"
            state = yaml.safe_load(state_path.read_text(encoding="utf-8"))
            state["active_versions"]["projects/focused-tool-ticket-intake"] = 1
            state_path.write_text(yaml.safe_dump(state), encoding="utf-8")
            errors = self.validator.validate_learner_system(self.skill_root, learner_dir)
            self.assertEqual(errors, [])

    def test_learner_profile_material_items_require_provenance_and_impact(self):
        profile = yaml.safe_load((self.skill_root / "assets/templates/discovery.yaml").read_text(encoding="utf-8"))
        self.assertEqual(self.schema_issues("learner-profile", profile), [])
        del profile["personal"]["role"]["decision_impact"]
        self.assertTrue(self.schema_issues("learner-profile", profile))

    def test_not_applicable_stage_requires_machine_readable_reason(self):
        state = yaml.safe_load((self.fixtures / "valid-learner" / "system-state.yaml").read_text(encoding="utf-8"))
        del state["stage_states"]["project-design"]["reason"]
        self.assertTrue(self.schema_issues("system-state", state))

    def test_not_applicable_stage_requires_complete_audit_record(self):
        state = yaml.safe_load((self.fixtures / "valid-learner" / "system-state.yaml").read_text(encoding="utf-8"))
        self.assertEqual(self.schema_issues("system-state", state), [])
        for field in ["source", "confidence", "affected_downstream"]:
            with self.subTest(field=field):
                invalid = yaml.safe_load(yaml.safe_dump(state))
                invalid["stage_states"]["project-design"].pop(field, None)
                self.assertTrue(self.schema_issues("system-state", invalid))

    def test_history_allows_stable_id_across_distinct_content_versions(self):
        with self.copied_valid_learner() as learner_dir:
            current_path = learner_dir / "learner-profile.yaml"
            current = yaml.safe_load(current_path.read_text(encoding="utf-8"))
            current["content_version"] = 2
            current_path.write_text(yaml.safe_dump(current), encoding="utf-8")
            history_path = learner_dir / "history" / "learner-profile.yaml"
            history_path.parent.mkdir(parents=True)
            historical = yaml.safe_load(yaml.safe_dump(current))
            historical["content_version"] = 1
            historical["status"] = "superseded"
            history_path.write_text(yaml.safe_dump(historical), encoding="utf-8")
            state_path = learner_dir / "system-state.yaml"
            state = yaml.safe_load(state_path.read_text(encoding="utf-8"))
            state["active_versions"]["learner-profile"] = 2
            state_path.write_text(yaml.safe_dump(state), encoding="utf-8")
            self.assertEqual(self.validator.validate_learner_system(self.skill_root, learner_dir), [])

    def test_history_rejects_duplicate_version_and_multiple_active_versions(self):
        for mutation in ["duplicate", "multiple_active"]:
            with self.subTest(mutation=mutation), self.copied_valid_learner() as learner_dir:
                current = yaml.safe_load((learner_dir / "learner-profile.yaml").read_text(encoding="utf-8"))
                history_path = learner_dir / "history" / "learner-profile.yaml"
                history_path.parent.mkdir(parents=True)
                historical = yaml.safe_load(yaml.safe_dump(current))
                if mutation == "multiple_active":
                    historical["content_version"] = 2
                else:
                    historical["status"] = "superseded"
                history_path.write_text(yaml.safe_dump(historical), encoding="utf-8")
                errors = self.validator.validate_learner_system(self.skill_root, learner_dir)
                expected = "multiple active" if mutation == "multiple_active" else "duplicate artifact version"
                self.assertTrue(any(expected in error.lower() for error in errors), errors)

    def test_singleton_type_rejects_second_active_artifact_with_different_id(self):
        with self.copied_valid_learner() as learner_dir:
            original = yaml.safe_load(
                (learner_dir / "competency-model.yaml").read_text(encoding="utf-8")
            )
            second = yaml.safe_load(yaml.safe_dump(original))
            second["id"] = "competency-model-learner-002"
            second_path = learner_dir / "versions" / "alternate" / "competency-model.yaml"
            second_path.parent.mkdir(parents=True)
            second_path.write_text(yaml.safe_dump(second), encoding="utf-8")

            errors = self.validator.validate_learner_system(
                self.skill_root, learner_dir
            )
            self.assertTrue(
                any(
                    "multiple active singleton artifacts for competency-model"
                    in error.lower()
                    for error in errors
                ),
                errors,
            )

    def test_cross_artifact_refs_use_active_competency_not_superseded_history(self):
        with self.copied_valid_learner() as learner_dir:
            competency_path = learner_dir / "competency-model.yaml"
            historical = yaml.safe_load(competency_path.read_text(encoding="utf-8"))
            historical["status"] = "superseded"
            competency_path.write_text(yaml.safe_dump(historical), encoding="utf-8")
            active = yaml.safe_load(yaml.safe_dump(historical))
            active["content_version"] = 2
            active["status"] = "active"
            active["competencies"] = [
                item for item in active["competencies"] if item["id"] != "api-integration"
            ]
            active_path = learner_dir / "versions" / "competency-model.yaml"
            active_path.parent.mkdir(parents=True)
            active_path.write_text(yaml.safe_dump(active), encoding="utf-8")
            state_path = learner_dir / "system-state.yaml"
            state = yaml.safe_load(state_path.read_text(encoding="utf-8"))
            del state["active_versions"]["competency-model"]
            state["active_versions"]["versions/competency-model"] = 2
            state_path.write_text(yaml.safe_dump(state), encoding="utf-8")
            errors = self.validator.validate_learner_system(self.skill_root, learner_dir)
            self.assertTrue(any("evidence references unknown competency: api-integration" in error.lower() for error in errors), errors)
            self.assertTrue(any("assessment references unknown competency: api-integration" in error.lower() for error in errors), errors)

    def test_assessment_decision_and_gate_are_biconditional(self):
        cases = [
            ("pass", False, ["independent"]),
            ("fail", True, []),
            ("needs_remediation", True, []),
        ]
        for decision, passed, missing in cases:
            with self.subTest(decision=decision, passed=passed):
                document = self.make_assessment_document()
                document["decision"] = decision
                document["gate"] = {"passed": passed, "missing": missing}
                self.assertTrue(self.schema_issues("assessment", document))

        remediation = self.make_assessment_document()
        independent = next(item for item in remediation["behavior_checks"] if item["behavior"] == "independent")
        independent["state"] = "fail"
        remediation["decision"] = "needs_remediation"
        remediation["gate"] = {"passed": False, "missing": ["independent"]}
        self.assertEqual(self.schema_issues("assessment", remediation), [])

    def test_learner_project_requires_nonempty_evidence_inputs(self):
        for field in ["inputs", "deliverables", "competency_ids"]:
            with self.subTest(field=field):
                project = yaml.safe_load((self.skill_root / "assets/templates/project-brief.yaml").read_text(encoding="utf-8"))
                project[field] = []
                self.assertTrue(self.schema_issues("project", project))

    def test_learner_project_requires_complete_typed_delivery_contract(self):
        fields = ["problem", "business_value", "users", "success_measures", "risks", "evidence_plan"]
        for field in fields:
            for mutation in ["missing", "empty"]:
                with self.subTest(field=field, mutation=mutation):
                    project = yaml.safe_load((self.skill_root / "assets/templates/project-brief.yaml").read_text(encoding="utf-8"))
                    if mutation == "missing":
                        project.pop(field, None)
                    elif isinstance(project.get(field), str):
                        project[field] = ""
                    elif isinstance(project.get(field), list):
                        project[field] = []
                    else:
                        project[field] = {}
                    self.assertTrue(self.schema_issues("project", project))

    def test_learner_project_rejects_invalid_rubric_semantics(self):
        for mutation in ["wrong_total", "zero_weight", "no_critical"]:
            with self.subTest(mutation=mutation), self.copied_valid_learner() as learner_dir:
                project_path = learner_dir / "projects" / "focused-tool-ticket-intake.yaml"
                project_path.parent.mkdir(parents=True)
                project = yaml.safe_load((self.skill_root / "assets/templates/project-brief.yaml").read_text(encoding="utf-8"))
                project["competency_ids"] = ["python-foundation", "api-integration"]
                project["status"] = "active"
                if mutation == "wrong_total":
                    project["rubric"]["correctness"]["weight"] = 99
                elif mutation == "zero_weight":
                    project["rubric"]["correctness"]["weight"] = 0
                else:
                    for dimension in project["rubric"].values():
                        dimension["critical"] = False
                project_path.write_text(yaml.safe_dump(project), encoding="utf-8")
                errors = self.validator.validate_learner_system(self.skill_root, learner_dir)
                self.assertTrue(any("project rubric" in error.lower() for error in errors), errors)

    def test_domain_pack_market_assumption_ids_and_review_dates_are_governed(self):
        for mutation in ["duplicate_id", "expired_review"]:
            with self.subTest(mutation=mutation):
                pack = self.load_ai_agent_domain_pack()
                if mutation == "duplicate_id":
                    pack["market_assumptions"][1]["id"] = pack["market_assumptions"][0]["id"]
                else:
                    pack["market_assumptions"][0]["next_review_at"] = "2020-01-01"
                errors = self.validator._validate_domain_pack_semantics("governance.yaml", pack)
                self.assertTrue(any("market assumption" in error.lower() for error in errors), errors)

    def test_domain_pack_target_outcome_ids_are_unique(self):
        pack = self.load_ai_agent_domain_pack()
        pack["target_outcomes"][1]["id"] = pack["target_outcomes"][0]["id"]
        errors = self.validator._validate_domain_pack_semantics("targets.yaml", pack)
        self.assertTrue(any("duplicate target outcome" in error.lower() for error in errors), errors)

    def test_domain_pack_each_project_rubric_requires_critical_dimension(self):
        pack = self.load_ai_agent_domain_pack()
        for dimension in pack["project_archetypes"][0]["rubric"].values():
            dimension["critical"] = False
        errors = self.validator._validate_domain_pack_semantics("critical.yaml", pack)
        self.assertTrue(any("critical dimension" in error.lower() for error in errors), errors)

    def test_domain_pack_rubric_dimensions_require_typed_gate_fields(self):
        schemas, registry = self.validator._load_schemas(self.skill_root)
        rubric_dimension = schemas["domain-pack"]["$defs"]["rubric_dimension"]
        self.assertTrue(
            {"critical", "passing_threshold"}
            <= set(rubric_dimension.get("required", []))
        )
        self.assertEqual(
            set(rubric_dimension["properties"]["passing_threshold"]["enum"]),
            {"developing", "proficient", "strong"},
        )

        pack = self.load_ai_agent_domain_pack()
        validator = self.validator.Draft202012Validator(
            schemas["domain-pack"],
            registry=registry,
            format_checker=self.validator.LEARNER_FORMAT_CHECKER,
        )
        self.assertEqual(list(validator.iter_errors(pack)), [])
        for archetype in pack["project_archetypes"]:
            for name, dimension in archetype["rubric"].items():
                with self.subTest(archetype=archetype["id"], dimension=name):
                    self.assertIs(type(dimension.get("critical")), bool)
                    self.assertIn(
                        dimension.get("passing_threshold"),
                        {"developing", "proficient", "strong"},
                    )

    def test_domain_pack_migration_accepts_documented_retired_sentinel(self):
        pack = self.load_ai_agent_domain_pack()
        pack["extensions"]["migration_map"] = {
            "legacy-competency": {"to": "retired", "reason": "Merged into the current competency model."}
        }
        self.assertEqual(self.validator._validate_domain_pack_semantics("retired.yaml", pack), [])

    def test_learner_profile_separates_epistemic_class_from_operational_source(self):
        profile = yaml.safe_load((self.skill_root / "assets/templates/discovery.yaml").read_text(encoding="utf-8"))
        items = [
            profile["experience"]["technical"],
            profile["swot"]["Strength"][0],
            profile["constraints"]["privacy"],
        ]
        for item, source in zip(items, ["assessment", "project", "mentor"]):
            item["source"] = source
        self.assertEqual(self.schema_issues("learner-profile", profile), [])
        profile["personal"]["role"]["epistemic_class"] = "belief"
        self.assertTrue(self.schema_issues("learner-profile", profile))

    def test_learner_profile_accepts_evidence_epistemic_class(self):
        profile = yaml.safe_load((self.skill_root / "assets/templates/discovery.yaml").read_text(encoding="utf-8"))
        profile["experience"]["technical"].update(
            epistemic_class="evidence", source="assessment"
        )
        profile["experience"]["projects"].update(
            epistemic_class="evidence", source="project"
        )
        self.assertEqual(self.schema_issues("learner-profile", profile), [])

    def make_assessment_document(self):
        return {
            "id": "assessment-six-behaviors",
            "schema_version": "1.0.0",
            "content_version": 1,
            "status": "validated",
            "source": "worked test assessment",
            "confidence": "high",
            "created_at": "2026-07-13T00:00:00Z",
            "updated_at": "2026-07-13T00:00:00Z",
            "stage": "project",
            "tasks": ["bounded project demonstration"],
            "evidence_ids": ["ev-independent", "ev-explain", "ev-modify", "ev-debug", "ev-deploy", "ev-teach"],
            "behavior_checks": [
                {
                    "behavior": behavior,
                    "applicability": "applicable",
                    "evidence_ids": [f"ev-{behavior}"],
                    "state": "pass",
                }
                for behavior in sorted(self.CANONICAL_ASSESSMENT_BEHAVIORS)
            ],
            "competency_results": [],
            "decision": "pass",
            "gate": {"passed": True, "missing": []},
            "next_action": "Prepare the target-context outcome package.",
        }

    def schema_issues(self, schema_name, document):
        schemas, registry = self.validator._load_schemas(self.skill_root)
        return list(
            self.validator.Draft202012Validator(
                schemas[schema_name],
                registry=registry,
                format_checker=FormatChecker(),
            ).iter_errors(document)
        )

    @staticmethod
    def set_confidence(learner_dir, value):
        for path in learner_dir.glob("*.yaml"):
            document = yaml.safe_load(path.read_text(encoding="utf-8"))
            document["confidence"] = value
            path.write_text(yaml.safe_dump(document), encoding="utf-8")

    def load_ai_agent_domain_pack(self):
        path = self.skill_root / "assets" / "domain-packs" / "ai-agent.yaml"
        self.assertTrue(path.is_file(), f"Missing Domain Pack: {path}")
        return yaml.safe_load(path.read_text(encoding="utf-8"))

    def domain_pack_issues(self, pack):
        schemas, registry = self.validator._load_schemas(self.skill_root)
        return list(
            self.validator.Draft202012Validator(
                schemas["domain-pack"],
                registry=registry,
                format_checker=FormatChecker(),
            ).iter_errors(pack)
        )

    def run_cli(self, learner_dir):
        return subprocess.run(
            [
                sys.executable,
                str(MODULE_PATH),
                "--skill-root",
                str(self.skill_root),
                "--learner-dir",
                str(learner_dir),
            ],
            capture_output=True,
            text=True,
            check=False,
        )

    def copied_valid_learner(self):
        temporary_directory = tempfile.TemporaryDirectory()
        learner_dir = Path(temporary_directory.name) / "learner"
        shutil.copytree(self.fixtures / "valid-learner", learner_dir)

        class CopiedLearner:
            def __enter__(self):
                return learner_dir

            def __exit__(self, exc_type, exc, traceback):
                temporary_directory.cleanup()

        return CopiedLearner()

    @staticmethod
    def canonical_stage_states(default):
        return {
            stage: {"state": default}
            for stage in [
                "discovery", "goal-analysis", "gap-analysis", "competency-design",
                "curriculum-design", "project-design", "roadmap", "weekly-planner",
                "assessment", "outcome-preparation", "continuous-optimization",
            ]
        }


if __name__ == "__main__":
    unittest.main()
