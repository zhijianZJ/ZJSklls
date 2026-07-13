from pathlib import Path
from collections import Counter
import importlib.util
import shutil
import subprocess
import sys
import tempfile
import unittest

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

    def test_discovery_starts_with_eight_to_twelve_questions(self):
        text = (
            self.skill_root / "references" / "discovery.md"
        ).read_text(encoding="utf-8")
        self.assertIn("8–12", text)
        self.assertIn("adaptive follow-up", text)

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


if __name__ == "__main__":
    unittest.main()
