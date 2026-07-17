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

    def test_chinese_document_set_is_complete(self):
        required = {
            "docs/getting-started.md": (
                "# Learning Architect 新手入门",
                "## 第一次使用",
                "## 为什么先提问",
                "## 如何继续",
                "## 如何重新规划",
            ),
            "docs/usage-guide.md": (
                "# Learning Architect 完整使用手册",
                "## 完整工作流",
                "## 产物与结构化状态",
                "## 证据与能力判断",
                "## 异常与安全边界",
            ),
            "docs/examples.md": (
                "# Learning Architect 使用场景与提示词",
                "## 场景一：零基础了解 AI 行业",
                "## 场景二：转岗 AI Agent 工程师",
                "## 场景三：转岗 AI 产品经理",
                "## 场景四：在当前工作中应用 AI",
            ),
            "docs/domain-pack-guide.md": (
                "# Domain Pack 扩展指南",
                "## 数据契约",
                "## 能力与依赖",
                "## 项目原型与评分关卡",
                "## 验证与提交",
            ),
        }
        for path, phrases in required.items():
            text = read_text(path)
            for phrase in phrases:
                self.assertIn(phrase, text, f"{path}: {phrase}")


if __name__ == "__main__":
    unittest.main()
