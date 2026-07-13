from pathlib import Path
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
