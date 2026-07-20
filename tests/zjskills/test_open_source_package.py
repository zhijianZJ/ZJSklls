from pathlib import Path
import re
import unittest
from urllib.parse import unquote

REPO_ROOT = Path(__file__).resolve().parents[2]
RUNTIME_ROOT = REPO_ROOT / "zjskills"


def read_text(path: str) -> str:
    return (REPO_ROOT / path).read_text(encoding="utf-8")


class OpenSourcePackageTests(unittest.TestCase):
    def test_readme_pair_and_version_surface(self):
        self.assertFalse((REPO_ROOT / "README.zh-CN.md").exists())
        chinese = read_text("README.md")
        english = read_text("README.en.md")
        for text in (chinese, english):
            self.assertIn("2.0.0", text)
            self.assertIn("MIT", text)
            self.assertIn("ZJSkills", text)
            self.assertIn("https://github.com/zhijianZJ/ZJSkills.git", text)
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
        self.assertEqual(read_text("VERSION").strip(), "2.0.0")
        license_text = read_text("LICENSE")
        self.assertIn("MIT License", license_text)
        self.assertIn("Copyright (c) 2026 ZJSkills", license_text)

    def test_contributing_guide_is_bilingual_and_enforces_boundaries(self):
        text = read_text("CONTRIBUTING.md")
        for phrase in (
            "## 中文贡献指南",
            "## English Contribution Guide",
            "python3 -m unittest",
            "禁止隐藏推广",
            "No hidden promotion",
        ):
            self.assertIn(phrase, text)

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
        }
        for path, phrases in required.items():
            text = read_text(path)
            for phrase in phrases:
                self.assertIn(phrase, text, f"{path}: {phrase}")

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
        }
        for path, phrases in required.items():
            text = read_text(path)
            for phrase in phrases:
                self.assertIn(phrase, text, f"{path}: {phrase}")

    def test_platform_installation_guides_cover_supported_hosts_and_boundaries(self):
        required = {
            "docs/platform-installation.md": (
                "# ZJSkills 多平台安装与使用",
                "## 兼容性矩阵",
                "## Codex",
                "## Claude Code",
                "## Tencent WorkBuddy",
                "## 豆包",
                "$HOME/.agents/skills/zjskills",
                "$HOME/.claude/skills/zjskills",
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
                "$HOME/.agents/skills/zjskills",
                "$HOME/.claude/skills/zjskills",
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

    def test_beginner_learning_support_is_documented_in_both_languages(self):
        required = {
            "README.md": ("学习中遇到问题", "我卡住了", "问题拆解"),
            "README.en.md": ("Problems during learning", "I'm stuck", "problem decomposition"),
            "docs/getting-started.md": ("## 学习中遇到问题", "现在只做这一步"),
            "docs/getting-started.en.md": ("## When you get stuck", "Do only this now"),
            "docs/usage-guide.md": ("## 学习陪跑与问题拆解",),
            "docs/usage-guide.en.md": ("## Learning support and problem decomposition",),
            "docs/examples.md": ("## 场景五：学习中卡住", "401"),
            "docs/examples.en.md": ("## Scenario 5: Getting stuck while learning", "401"),
        }
        for path, phrases in required.items():
            text = read_text(path)
            for phrase in phrases:
                self.assertIn(phrase, text, f"{path}: {phrase}")

    def test_v2_migration_commands_fail_closed_on_existing_paths(self):
        chinese = read_text("docs/platform-installation.md")
        english = read_text("docs/platform-installation.en.md")
        for text in (chinese, english):
            migration = text.split("1.x", 1)[1].split("\n## ", 1)[0]
            self.assertIn("(\n  set -e", migration)
            self.assertIn("learning-architect.backup", migration)
            self.assertIn('destination="$skills_root/zjskills"', migration)
            self.assertIn("exit 1", migration)
            self.assertIn("Windows PowerShell", migration)
            self.assertIn("throw", migration)

    def test_public_documents_use_zjskills_brand_and_repository_url(self):
        documents = [REPO_ROOT / "README.md", REPO_ROOT / "README.en.md", REPO_ROOT / "CONTRIBUTING.md"]
        documents.extend(sorted((REPO_ROOT / "docs").glob("*.md")))
        for document in documents:
            text = document.read_text(encoding="utf-8")
            self.assertNotIn("king-wsc", text, document)
            self.assertNotIn("LearningArchitectSklls", text, document)
            self.assertNotIn("Learning Architect", text, document)
        self.assertIn("https://github.com/zhijianZJ/ZJSkills.git", read_text("README.md"))

    def test_repository_documents_do_not_retain_the_old_github_location(self):
        documents = [REPO_ROOT / "README.md", REPO_ROOT / "README.en.md", REPO_ROOT / "CONTRIBUTING.md"]
        documents.extend(sorted((REPO_ROOT / "docs").rglob("*.md")))
        for document in documents:
            text = document.read_text(encoding="utf-8")
            self.assertNotIn("king-wsc/LearningArchitectSklls", text, document)
            if "docs/superpowers" not in document.as_posix():
                self.assertNotIn("zhijianZJ/ZJSklls", text, document)

    def test_v2_technical_identifier_migration_contract(self):
        new_runtime = REPO_ROOT / "zjskills"
        old_runtime = REPO_ROOT / "learning-architect"
        self.assertTrue(new_runtime.is_dir(), new_runtime)
        self.assertFalse(old_runtime.exists(), old_runtime)
        self.assertTrue((new_runtime / "SKILL.md").is_file())
        self.assertTrue((REPO_ROOT / "tests" / "zjskills").is_dir())
        self.assertFalse((REPO_ROOT / "tests" / "learning-architect").exists())

        skill = (new_runtime / "SKILL.md").read_text(encoding="utf-8")
        metadata = (new_runtime / "agents" / "openai.yaml").read_text(
            encoding="utf-8"
        )
        self.assertIn("name: zjskills", skill)
        self.assertIn('display_name: "ZJSkills"', metadata)
        self.assertIn("$zjskills", metadata)
        self.assertNotIn("$learning-architect", metadata)

        current_documents = [
            REPO_ROOT / "README.md",
            REPO_ROOT / "README.en.md",
            REPO_ROOT / "CONTRIBUTING.md",
            *sorted(
                path
                for path in (REPO_ROOT / "docs").glob("*.md")
                if not path.name.startswith("platform-installation")
            ),
        ]
        for document in current_documents:
            text = document.read_text(encoding="utf-8")
            self.assertNotIn("learning-architect", text, document)

        current_runtime_and_fixtures = [
            *RUNTIME_ROOT.rglob("*.md"),
            *RUNTIME_ROOT.rglob("*.yaml"),
            *(REPO_ROOT / "tests" / "zjskills").rglob("*.md"),
            *(REPO_ROOT / "tests" / "zjskills").rglob("*.yaml"),
        ]
        for document in current_runtime_and_fixtures:
            text = document.read_text(encoding="utf-8")
            self.assertNotIn("learning-architect", text, document)

        archive = (
            REPO_ROOT
            / "docs/superpowers/history/learning-architect-evaluations/README.md"
        )
        self.assertTrue(archive.is_file(), archive)
        self.assertIn("Historical Evaluation Archive", archive.read_text(encoding="utf-8"))

    def test_public_docs_explain_navigation_and_v2_migration(self):
        chinese = read_text("README.md") + read_text("docs/getting-started.md")
        english = read_text("README.en.md") + read_text("docs/getting-started.en.md")
        for phrase in (
            "ZJSkills 学习导航",
            "回复数字",
            "新手模式",
            "$zjskills",
            "/zjskills",
        ):
            self.assertIn(phrase, chinese)
        for phrase in (
            "ZJSkills Learning Navigation",
            "reply with a number",
            "Beginner mode",
            "$zjskills",
            "/zjskills",
        ):
            self.assertIn(phrase, english)
        for path in ("docs/platform-installation.md", "docs/platform-installation.en.md"):
            text = read_text(path)
            self.assertIn("2.0.0", text)
            self.assertIn("zjskills", text)
            self.assertIn("learning-architect", text)
            self.assertIn("回滚" if path.endswith(".md") and not path.endswith(".en.md") else "rollback", text.lower())

    def test_skill_ui_uses_zjskills_technical_identifier(self):
        metadata = read_text("zjskills/agents/openai.yaml")
        self.assertIn('display_name: "ZJSkills"', metadata)
        self.assertIn("$zjskills", metadata)
        self.assertNotIn("$learning-architect", metadata)

if __name__ == "__main__":
    unittest.main()
