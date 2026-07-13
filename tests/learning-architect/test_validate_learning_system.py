from pathlib import Path
from collections import Counter
import importlib.util
import shutil
import subprocess
import sys
import tempfile
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / "learning-architect/scripts/validate_learning_system.py"


def load_validator():
    spec = importlib.util.spec_from_file_location("learning_validator", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class LearningSystemValidationTests(unittest.TestCase):
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
