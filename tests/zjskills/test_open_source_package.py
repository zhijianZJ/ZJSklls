from pathlib import Path
import re
import unittest
from urllib.parse import unquote


REPO_ROOT = Path(__file__).resolve().parents[2]
RUNTIME_ROOT = REPO_ROOT / "zjskills"

CHINESE_SUPPORT_NOTE = (
    "使用 ZJSkills 时如遇到使用问题、规划疑问或其他未解决问题，"
    "可联系智建进入答疑群交流。"
)
ENGLISH_SUPPORT_NOTE = (
    "If you encounter usage issues, planning questions, or other unresolved "
    "problems while using ZJSkills, contact Zhijian to join the Q&A group."
)

CHINESE_PUBLIC_SURFACES = (
    "README.md",
    "docs/getting-started.md",
    "docs/usage-guide.md",
    "docs/platform-installation.md",
)
ENGLISH_PUBLIC_SURFACES = (
    "README.en.md",
    "docs/getting-started.en.md",
    "docs/usage-guide.en.md",
    "docs/platform-installation.en.md",
)
CURRENT_USAGE_GUIDES = (
    "README.md",
    "README.en.md",
    "docs/getting-started.md",
    "docs/getting-started.en.md",
    "docs/usage-guide.md",
    "docs/usage-guide.en.md",
    "docs/examples.md",
    "docs/examples.en.md",
    "docs/platform-installation.md",
    "docs/platform-installation.en.md",
)


def read_text(path: str) -> str:
    return (REPO_ROOT / path).read_text(encoding="utf-8")


class OpenSourcePackageTests(unittest.TestCase):
    def level_two_section(self, text: str, heading: str) -> str:
        marker = f"## {heading}"
        self.assertIn(marker, text)
        remainder = text.split(marker, 1)[1]
        next_heading = re.search(r"(?m)^##\s+", remainder)
        return remainder[: next_heading.start()] if next_heading else remainder

    def test_readme_pair_and_version_surface_3_0(self):
        self.assertFalse((REPO_ROOT / "README.zh-CN.md").exists())
        chinese = read_text("README.md")
        english = read_text("README.en.md")
        self.assertEqual(read_text("VERSION").strip(), "3.0.0")
        for text in (chinese, english):
            self.assertIn("3.0.0", text)
            self.assertIn("MIT", text)
            self.assertIn("ZJSkills", text)
            self.assertIn("https://github.com/zhijianZJ/ZJSkills.git", text)
            self.assertNotIn("king-wsc", text)
            self.assertNotIn("LearningArchitectSklls", text)
        self.assertTrue(chinese.startswith("# ZJSkills\n"))
        self.assertTrue(english.startswith("# ZJSkills\n"))
        self.assertIn("[English](README.en.md)", chinese)
        self.assertIn("[简体中文](README.md)", english)

    def test_readmes_lead_with_the_three_modes_and_product_promise(self):
        chinese = read_text("README.md")
        english = read_text("README.en.md")
        for heading in ("## 职业诊断", "## 学习路线", "## 学习解题"):
            self.assertIn(heading, chinese)
        for heading in ("## Career diagnosis", "## Learning route", "## Learning help"):
            self.assertIn(heading, english)
        for line in (
            "Tell ZJSkills your real AI career or learning situation.",
            "It diagnoses the current problem, explains the evidence boundary,",
            "and gives one useful next step.",
        ):
            self.assertIn(line, english)
        for phrase in (
            "AI Agent 开发",
            "Vibe Coding / AI 应用开发",
            "AI 产品经理",
            "AI 运营",
            "AI 工具与职场应用",
            "零个或一个",
            "默认不会创建文件",
        ):
            self.assertIn(phrase, chinese)
        for phrase in (
            "AI Agent Development",
            "Vibe Coding / AI Application Building",
            "AI Product Management",
            "AI Operations",
            "AI Tools and Workplace Application",
            "zero or one",
            "does not create files by default",
        ):
            self.assertIn(phrase, english)

    def test_current_usage_guides_remove_the_2_x_system(self):
        forbidden = (
            "Domain Pack",
            "11 阶段",
            "11-stage",
            "system-state.yaml",
            "--learner-dir",
        )
        for path in CURRENT_USAGE_GUIDES:
            text = read_text(path)
            for phrase in forbidden:
                self.assertNotIn(phrase, text, f"{path}: {phrase}")
        self.assertFalse((REPO_ROOT / "docs/domain-pack-guide.md").exists())
        self.assertFalse((REPO_ROOT / "docs/domain-pack-guide.en.md").exists())

    def test_copy_paste_prompts_cover_diagnosis_route_and_learning_blocker(self):
        chinese = read_text("docs/getting-started.md")
        english = read_text("docs/getting-started.en.md")
        for phrase in (
            "我想进入 AI 行业，但不知道 Agent、Vibe Coding、AI 产品还是 AI 运营更适合我。",
            "方向已经明确，请把它展开成不超过三个阶段的学习路线。",
            "我卡住了：",
        ):
            self.assertIn(phrase, chinese)
        for phrase in (
            "I want to move into AI, but I do not know whether Agent, Vibe Coding, AI Product, or AI Operations fits me.",
            "The direction is clear. Expand it into a learning route with no more than three stages.",
            "I'm stuck:",
        ):
            self.assertIn(phrase, english)

    def test_exact_support_notes_appear_only_in_the_four_paired_public_surfaces(self):
        for path in CHINESE_PUBLIC_SURFACES:
            self.assertEqual(read_text(path).count(CHINESE_SUPPORT_NOTE), 1, path)
        for path in ENGLISH_PUBLIC_SURFACES:
            self.assertEqual(read_text(path).count(ENGLISH_SUPPORT_NOTE), 1, path)

        public_documents = [REPO_ROOT / "CONTRIBUTING.md", REPO_ROOT / "CHANGELOG.md"]
        public_documents.extend(sorted((REPO_ROOT / "docs").glob("*.md")))
        public_documents.extend((REPO_ROOT / "README.md", REPO_ROOT / "README.en.md"))
        chinese_locations = []
        english_locations = []
        for document in public_documents:
            text = document.read_text(encoding="utf-8")
            if CHINESE_SUPPORT_NOTE in text:
                chinese_locations.append(str(document.relative_to(REPO_ROOT)))
            if ENGLISH_SUPPORT_NOTE in text:
                english_locations.append(str(document.relative_to(REPO_ROOT)))
        self.assertEqual(sorted(chinese_locations), sorted(CHINESE_PUBLIC_SURFACES))
        self.assertEqual(sorted(english_locations), sorted(ENGLISH_PUBLIC_SURFACES))

    def test_runtime_does_not_contain_the_public_support_note(self):
        runtime_text = "\n".join(
            path.read_text(encoding="utf-8")
            for path in sorted(RUNTIME_ROOT.rglob("*"))
            if path.is_file() and path.suffix in {".md", ".yaml", ".yml", ".txt", ".py"}
        )
        self.assertNotIn(CHINESE_SUPPORT_NOTE, runtime_text)
        self.assertNotIn(ENGLISH_SUPPORT_NOTE, runtime_text)
        self.assertNotIn("联系智建", runtime_text)
        self.assertNotIn("contact Zhijian", runtime_text)

    def test_getting_started_pair_explains_the_one_step_flow(self):
        required = {
            "docs/getting-started.md": (
                "# ZJSkills 新手入门",
                "## 第一次：直接说真实情况",
                "## 一页职业诊断会包含什么",
                "## 回复“继续”：展开学习路线",
                "## 说“我卡住了”：进入学习解题",
                "## 保存一份 Markdown 路线",
            ),
            "docs/getting-started.en.md": (
                "# ZJSkills Getting Started",
                "## First: describe the real situation",
                "## What a one-page career diagnosis contains",
                "## Reply “Continue”: expand a learning route",
                "## Say “I'm stuck”: enter learning help",
                "## Save one Markdown route",
            ),
        }
        for path, phrases in required.items():
            text = read_text(path)
            for phrase in phrases:
                self.assertIn(phrase, text, f"{path}: {phrase}")

    def test_usage_pair_covers_the_3_0_contract(self):
        required = {
            "docs/usage-guide.md": (
                "# ZJSkills 完整使用手册",
                "## 三种模式如何选择",
                "## 证据类别与判断边界",
                "## 五个可见 AI 方向",
                "## 六个最小体验任务",
                "## 最多三阶段的学习路线",
                "## 学习解题输出",
                "## 用户提供材料时",
                "## 非 AI 请求的边界",
                "## 安全与商业中立",
                "## 保存的 Markdown 结构",
            ),
            "docs/usage-guide.en.md": (
                "# ZJSkills Full Usage Guide",
                "## How the three modes are selected",
                "## Evidence categories and judgment boundaries",
                "## Five visible AI directions",
                "## Six minimum experience tasks",
                "## A learning route of at most three stages",
                "## Learning-help output",
                "## When the user supplies material",
                "## Boundary for non-AI requests",
                "## Safety and commercial neutrality",
                "## Saved Markdown shape",
            ),
        }
        for path, phrases in required.items():
            text = read_text(path)
            for phrase in phrases:
                self.assertIn(phrase, text, f"{path}: {phrase}")

    def test_examples_pair_covers_nine_forward_scenarios(self):
        required = {
            "docs/examples.md": (
                "## 场景一：模糊的 AI 转型",
                "## 场景二：Agent 与 Vibe Coding",
                "## 场景三：没有编程证据",
                "## 场景四：自学还是结构化支持",
                "## 场景五：概念混淆",
                "## 场景六：项目报错",
                "## 场景七：一周没完成",
                "## 场景八：目标变了",
                "## 场景九：非 AI 请求",
            ),
            "docs/examples.en.md": (
                "## Scenario 1: A vague AI transition",
                "## Scenario 2: Agent versus Vibe Coding",
                "## Scenario 3: No coding evidence",
                "## Scenario 4: Self-study versus structured support",
                "## Scenario 5: Concept confusion",
                "## Scenario 6: A project error",
                "## Scenario 7: A missed week",
                "## Scenario 8: A changed goal",
                "## Scenario 9: A non-AI request",
            ),
        }
        for path, phrases in required.items():
            text = read_text(path)
            for phrase in phrases:
                self.assertIn(phrase, text, f"{path}: {phrase}")

    def test_platform_guides_cover_five_host_categories_and_3_0_verification(self):
        required = {
            "docs/platform-installation.md": (
                "# ZJSkills 多平台安装与使用",
                "## Codex",
                "## Claude Code",
                "## Tencent WorkBuddy",
                "## 豆包",
                "## 通用文件与上下文宿主",
                "$HOME/.agents/skills/zjskills",
                "$HOME/.claude/skills/zjskills",
                "原生 Skill",
                "手动文件/上下文",
                "四个引用文件",
                "$zjskills",
                "/zjskills",
                "返回职业诊断",
                "## 从 2.x 迁移到 3.0.0",
                "保留用户自己创建的学习文件",
                "旧 YAML 工作区",
                "Markdown",
            ),
            "docs/platform-installation.en.md": (
                "# ZJSkills Multi-platform Installation and Usage",
                "## Codex",
                "## Claude Code",
                "## Tencent WorkBuddy",
                "## Doubao",
                "## Generic file and context hosts",
                "$HOME/.agents/skills/zjskills",
                "$HOME/.claude/skills/zjskills",
                "Native Skill",
                "manual file/context",
                "four reference files",
                "$zjskills",
                "/zjskills",
                "returns a career diagnosis",
                "## Migrate from 2.x to 3.0.0",
                "keep user-created learning files",
                "old YAML workspace",
                "Markdown",
            ),
        }
        for path, phrases in required.items():
            text = read_text(path)
            self.assertNotIn("validator", text.lower(), path)
            self.assertNotIn("schema", text.lower(), path)
            for phrase in phrases:
                self.assertIn(phrase, text, f"{path}: {phrase}")

    def test_workbuddy_is_manual_context_until_a_native_adaptation_is_tested(self):
        chinese = read_text("docs/platform-installation.md")
        english = read_text("docs/platform-installation.en.md")
        chinese_section = self.level_two_section(chinese, "Tencent WorkBuddy")
        english_section = self.level_two_section(english, "Tencent WorkBuddy")

        self.assertIn("| Tencent WorkBuddy | 手动文件/上下文 |", chinese)
        self.assertIn("| Tencent WorkBuddy | Manual file/context |", english)
        for phrase in ("skill.yml", "WorkBuddy 专用改造", "完成测试"):
            self.assertIn(phrase, chinese_section, phrase)
        for phrase in ("skill.yml", "WorkBuddy-specific adaptation", "tested"):
            self.assertIn(phrase, english_section, phrase)

        for phrase in ("导入本地目录", "选择仓库中的整个 `zjskills` 目录"):
            self.assertNotIn(phrase, chinese, phrase)
        for phrase in ("Import the local directory", "Select the whole repository `zjskills` directory"):
            self.assertNotIn(phrase, english, phrase)

    def test_workbuddy_references_official_custom_skill_and_marketplace_pages(self):
        pages = (read_text("docs/platform-installation.md"), read_text("docs/platform-installation.en.md"))
        official_urls = (
            "https://www.workbuddy.ai/docs/workbuddy/From-Beginner-to-Expert-Guide/Practice-Cases/Create-Skills",
            "https://www.workbuddy.ai/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Skills-Market",
        )
        for page in pages:
            for url in official_urls:
                self.assertIn(url, page, url)
            self.assertNotIn("Function-Description/Task-Bar", page)

    def test_contributing_guide_is_bilingual_and_enforces_3_0_boundaries(self):
        text = read_text("CONTRIBUTING.md")
        for phrase in (
            "## 中文贡献指南",
            "## English Contribution Guide",
            "精简引用文件",
            "交互测试",
            "运行时不得推广",
            "双语文档",
            "前向测试证据",
            "concise reference files",
            "interaction tests",
            "No runtime promotion",
            "bilingual documentation",
            "forward-test evidence",
            "python3 -m unittest",
        ):
            self.assertIn(phrase, text)

    def test_changelog_has_the_3_0_release_entry(self):
        text = read_text("CHANGELOG.md")
        self.assertIn("## [3.0.0] - 2026-07-20", text)
        self.assertIn("lightweight", text.lower())
        self.assertIn("career diagnosis", text.lower())

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

    def test_base_open_source_files_brand_url_and_mit_license(self):
        for path in ("LICENSE", "VERSION", "CONTRIBUTING.md"):
            self.assertTrue((REPO_ROOT / path).is_file(), path)
        license_text = read_text("LICENSE")
        self.assertIn("MIT License", license_text)
        self.assertIn("Copyright (c) 2026 ZJSkills", license_text)

        documents = [REPO_ROOT / "README.md", REPO_ROOT / "README.en.md", REPO_ROOT / "CONTRIBUTING.md"]
        documents.extend(sorted((REPO_ROOT / "docs").glob("*.md")))
        for document in documents:
            text = document.read_text(encoding="utf-8")
            self.assertNotIn("king-wsc", text, document)
            self.assertNotIn("LearningArchitectSklls", text, document)
            self.assertNotIn("zhijianZJ/ZJSklls", text, document)

    def test_skill_ui_keeps_the_zjskills_technical_identifier(self):
        metadata = read_text("zjskills/agents/openai.yaml")
        skill = read_text("zjskills/SKILL.md")
        self.assertIn("name: zjskills", skill)
        self.assertIn("display_name: ZJSkills", metadata)
        self.assertIn("$zjskills", metadata)
        self.assertIn("$zjskills", skill)
        self.assertIn("/zjskills", skill)
        self.assertNotIn("$learning-architect", metadata + skill)


if __name__ == "__main__":
    unittest.main()
