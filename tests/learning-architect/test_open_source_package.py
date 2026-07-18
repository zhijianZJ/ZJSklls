from pathlib import Path
import re
import unittest
from urllib.parse import unquote


REPO_ROOT = Path(__file__).resolve().parents[2]
RUNTIME_ROOT = REPO_ROOT / "learning-architect"


def read_text(path: str) -> str:
    return (REPO_ROOT / path).read_text(encoding="utf-8")


class OpenSourcePackageTests(unittest.TestCase):
    def test_readme_pair_and_version_surface(self):
        self.assertFalse((REPO_ROOT / "README.zh-CN.md").exists())
        chinese = read_text("README.md")
        english = read_text("README.en.md")
        for text in (chinese, english):
            self.assertIn("1.0.0", text)
            self.assertIn("MIT", text)
            self.assertIn("ZJSkills", text)
            self.assertIn("https://github.com/zhijianZJ/ZJSklls.git", text)
            self.assertNotIn("king-wsc", text)
            self.assertNotIn("LearningArchitectSklls", text)
        self.assertTrue(chinese.startswith("# ZJSkills\n"))
        self.assertTrue(english.startswith("# ZJSkills\n"))
        self.assertIn("[English](README.en.md)", chinese)
        self.assertIn("[简体中文](README.md)", english)

    def test_all_relative_markdown_links_resolve(self):
        documents = [REPO_ROOT / "README.md", REPO_ROOT / "README.en.md"]
        documents.extend(sorted((REPO_ROOT / "docs").glob("*.md")))
        documents.append(REPO_ROOT / "CONTRIBUTING.md")
        pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
        broken = []
        for document in documents:
            for raw_target in pattern.findall(document.read_text(encoding="utf-8")):
                target = raw_target.split("#", 1)[0].strip()
                if not target or target.startswith(("http://", "https://", "mailto:")):
                    continue
                resolved = (document.parent / unquote(target)).resolve()
                if not resolved.exists():
                    broken.append(f"{document.relative_to(REPO_ROOT)} -> {raw_target}")
        self.assertEqual(broken, [])

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
        self.assertIn("domain-pack.schema.yaml", text)
        self.assertNotIn("domain-pack.schema.json", text)

    def test_chinese_document_set_is_complete(self):
        required = {
            "docs/getting-started.md": (
                "# ZJSkills 新手入门",
                "## 第一次使用",
                "## 为什么先提问",
                "## 如何继续",
                "## 如何重新规划",
            ),
            "docs/usage-guide.md": (
                "# ZJSkills 完整使用手册",
                "## 完整工作流",
                "## 产物与结构化状态",
                "## 证据与能力判断",
                "## 异常与安全边界",
            ),
            "docs/examples.md": (
                "# ZJSkills 使用场景与提示词",
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
        for path in ("docs/usage-guide.md", "docs/domain-pack-guide.md"):
            self.assertIn("--learner-dir", read_text(path), path)

    def test_english_document_set_is_complete(self):
        required = {
            "docs/getting-started.en.md": (
                "# ZJSkills Getting Started",
                "## First use",
                "## Why it asks before planning",
                "## How to continue",
                "## How to replan",
            ),
            "docs/usage-guide.en.md": (
                "# ZJSkills Full Usage Guide",
                "## Complete workflow",
                "## Artifacts and structured state",
                "## Evidence and capability judgment",
                "## Failure and safety boundaries",
            ),
            "docs/examples.en.md": (
                "# ZJSkills Scenarios and Prompts",
                "## Scenario 1: Explore the AI industry from zero",
                "## Scenario 2: Transition to AI Agent Engineer",
                "## Scenario 3: Transition to AI Product Manager",
                "## Scenario 4: Apply AI in current work",
            ),
            "docs/domain-pack-guide.en.md": (
                "# Domain Pack Extension Guide",
                "## Data contract",
                "## Competencies and dependencies",
                "## Project archetypes and rubric gates",
                "## Validation and contribution",
            ),
        }
        for path, phrases in required.items():
            text = read_text(path)
            for phrase in phrases:
                self.assertIn(phrase, text, f"{path}: {phrase}")
        for path in ("docs/usage-guide.en.md", "docs/domain-pack-guide.en.md"):
            self.assertIn("--learner-dir", read_text(path), path)

    def test_platform_installation_guides_cover_supported_hosts_and_boundaries(self):
        required = {
            "docs/platform-installation.md": (
                "# ZJSkills 多平台安装与使用",
                "## 兼容性矩阵",
                "## Codex",
                "## Claude Code",
                "## Tencent WorkBuddy",
                "## 豆包",
                "$HOME/.agents/skills/learning-architect",
                "$HOME/.claude/skills/learning-architect",
                "原生 Skill",
                "对话接入",
            ),
            "docs/platform-installation.en.md": (
                "# ZJSkills Multi-platform Installation and Usage",
                "## Compatibility matrix",
                "## Codex",
                "## Claude Code",
                "## Tencent WorkBuddy",
                "## Doubao",
                "$HOME/.agents/skills/learning-architect",
                "$HOME/.claude/skills/learning-architect",
                "Native Skill",
                "prompt-based",
            ),
        }
        for path, phrases in required.items():
            text = read_text(path)
            for phrase in phrases:
                self.assertIn(phrase, text, f"{path}: {phrase}")

    def test_readmes_link_to_platform_guides_and_name_all_hosts(self):
        chinese = read_text("README.md")
        english = read_text("README.en.md")
        self.assertIn("docs/platform-installation.md", chinese)
        self.assertIn("docs/platform-installation.en.md", english)
        for text in (chinese, english):
            for host in ("Codex", "Claude Code", "Tencent WorkBuddy"):
                self.assertIn(host, text)
        self.assertIn("豆包", chinese)
        self.assertIn("Doubao", english)

    def test_public_documents_use_zjskills_brand_and_repository_url(self):
        documents = [REPO_ROOT / "README.md", REPO_ROOT / "README.en.md", REPO_ROOT / "CONTRIBUTING.md"]
        documents.extend(sorted((REPO_ROOT / "docs").glob("*.md")))
        for document in documents:
            text = document.read_text(encoding="utf-8")
            self.assertNotIn("king-wsc", text, document)
            self.assertNotIn("LearningArchitectSklls", text, document)
            self.assertNotIn("Learning Architect", text, document)
        self.assertIn("https://github.com/zhijianZJ/ZJSklls.git", read_text("README.md"))

    def test_repository_documents_do_not_retain_the_old_github_location(self):
        documents = [REPO_ROOT / "README.md", REPO_ROOT / "README.en.md", REPO_ROOT / "CONTRIBUTING.md"]
        documents.extend(sorted((REPO_ROOT / "docs").rglob("*.md")))
        for document in documents:
            text = document.read_text(encoding="utf-8")
            self.assertNotIn("king-wsc/LearningArchitectSklls", text, document)

    def test_skill_metadata_covers_ai_exploration_and_transition(self):
        skill = read_text("learning-architect/SKILL.md")
        for phrase in (
            "AI industry exploration",
            "AI learning-direction decisions",
            "AI career-transition planning",
            "personalized learning path",
        ):
            self.assertIn(phrase, skill)

    def test_skill_ui_uses_zjskills_while_preserving_technical_identifier(self):
        metadata = read_text("learning-architect/agents/openai.yaml")
        self.assertIn('display_name: "ZJSkills"', metadata)
        self.assertIn("$learning-architect", metadata)

    def test_runtime_skill_is_brand_and_promotion_neutral(self):
        forbidden = ("ZJSkills", "智建", "社群", "community link", "课程推广")
        violations = []
        allowed_brand_metadata = RUNTIME_ROOT / "agents" / "openai.yaml"
        for path in RUNTIME_ROOT.rglob("*"):
            if not path.is_file() or "__pycache__" in path.parts:
                continue
            if path.suffix.lower() not in {".md", ".yaml", ".yml", ".txt", ".py"}:
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            for phrase in forbidden:
                if path == allowed_brand_metadata and phrase == "ZJSkills":
                    continue
                if phrase in text:
                    violations.append(f"{path.relative_to(REPO_ROOT)}: {phrase}")
        self.assertEqual(violations, [])


if __name__ == "__main__":
    unittest.main()
