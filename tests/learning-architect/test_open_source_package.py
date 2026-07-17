from pathlib import Path
import unittest


REPO_ROOT = Path(__file__).resolve().parents[2]
RUNTIME_ROOT = REPO_ROOT / "learning-architect"


def read_text(path: str) -> str:
    return (REPO_ROOT / path).read_text(encoding="utf-8")


class OpenSourcePackageTests(unittest.TestCase):
    def test_base_open_source_files_and_mit_license(self):
        for path in ("LICENSE", "VERSION", "CONTRIBUTING.md"):
            self.assertTrue((REPO_ROOT / path).is_file(), path)
        self.assertEqual(read_text("VERSION").strip(), "1.0.0")
        license_text = read_text("LICENSE")
        self.assertIn("MIT License", license_text)
        self.assertIn("Copyright (c) 2026 ZJSkills", license_text)

    def test_contributing_guide_is_bilingual_and_enforces_boundaries(self):
        text = read_text("CONTRIBUTING.md")
        for phrase in (
            "## 中文贡献指南",
            "## English Contribution Guide",
            "Domain Pack",
            "python3 -m unittest",
            "禁止隐藏推广",
            "No hidden promotion",
        ):
            self.assertIn(phrase, text)


if __name__ == "__main__":
    unittest.main()
