# ZJSkills Open-Source Productization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Productize Learning Architect as a bilingual MIT-licensed open-source project initiated by ZJSkills while preserving a brand-neutral learner runtime.

**Architecture:** Keep the runtime Skill isolated under `learning-architect/` and place all human-facing branding, onboarding, examples, contribution guidance, license, and version information at repository level. Lock the packaging contract with a focused standard-library test module, then build Chinese docs, English docs, root navigation, metadata changes, and installed-copy verification in independently reviewable tasks.

**Tech Stack:** Markdown, YAML, Python 3.11 standard library `unittest`, existing PyYAML/jsonschema validator environment, Git, Codex Skill validation scripts.

## Global Constraints

- Use MIT License with `Copyright (c) 2026 ZJSkills`.
- Set the initial public productized version to exactly `1.0.0`.
- Use `README.md` as the Chinese default homepage and `README.en.md` as the English homepage.
- Keep brand strings limited to repository documentation, repository metadata, and the license copyright notice.
- Do not add ZJSkills, 智建, community, course, QR-code, or sales promotion to learner-facing runtime instructions or outputs.
- Do not add biographies, credentials, client metrics, social links, community links, course links, a website, demo GIF, plugin marketplace, multi-platform installer, or automatic updater.
- Preserve all existing 84 Learning Architect tests and validator behavior.
- Use `apply_patch` for file creation and edits; preserve unrelated user changes.
- Use Miniconda Python for validation: `export PATH="/Users/wangshucheng/miniconda3/bin:$PATH"`.

---

## File Map

### Create

- `LICENSE` — MIT license and ZJSkills copyright.
- `VERSION` — single line `1.0.0`.
- `CONTRIBUTING.md` — bilingual contribution contract.
- `README.en.md` — English default-product documentation moved from the current root README and expanded.
- `docs/getting-started.md` — Chinese first-use guide.
- `docs/getting-started.en.md` — English first-use guide.
- `docs/usage-guide.md` — Chinese full workflow and artifact guide.
- `docs/usage-guide.en.md` — English full workflow and artifact guide.
- `docs/examples.md` — Chinese scenario prompts.
- `docs/examples.en.md` — English scenario prompts.
- `docs/domain-pack-guide.md` — Chinese Domain Pack contribution guide.
- `docs/domain-pack-guide.en.md` — English Domain Pack contribution guide.
- `tests/learning-architect/test_open_source_package.py` — open-source packaging, link, version, metadata, and brand-isolation tests.

### Modify

- `README.md` — replace English homepage with the Chinese default homepage and productized navigation.
- `learning-architect/SKILL.md` — broaden trigger description for AI exploration, direction decisions, and transition planning without changing runtime workflow.
- `learning-architect/agents/openai.yaml` — align the neutral default prompt with the broadened Skill trigger.

### Delete

- `README.zh-CN.md` — remove after its content becomes the default `README.md` and every language link targets `README.en.md` or `README.md`.

---

### Task 1: Establish the Open-Source Base Contract

**Files:**
- Create: `tests/learning-architect/test_open_source_package.py`
- Create: `LICENSE`
- Create: `VERSION`
- Create: `CONTRIBUTING.md`

**Interfaces:**
- Consumes: repository root resolved from `Path(__file__).resolve().parents[2]`.
- Produces: `REPO_ROOT`, `RUNTIME_ROOT`, `read_text(path: str) -> str`, and the base files required by later documentation tasks.

- [ ] **Step 1: Write failing base-package tests**

Create `tests/learning-architect/test_open_source_package.py` with:

```python
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
```

- [ ] **Step 2: Run the focused test and verify RED**

Run:

```bash
export PATH="/Users/wangshucheng/miniconda3/bin:$PATH"
python3 -m unittest tests/learning-architect/test_open_source_package.py -q
```

Expected: nonzero result with one assertion failure for missing base files and one file-read error for missing `CONTRIBUTING.md`.

- [ ] **Step 3: Add the MIT license and version**

Create `LICENSE` with the canonical MIT License text, beginning with:

```text
MIT License

Copyright (c) 2026 ZJSkills
```

Create `VERSION` with exactly:

```text
1.0.0
```

- [ ] **Step 4: Add the bilingual contribution contract**

Create `CONTRIBUTING.md` with Chinese first and English second. Both sections must cover:

- issue reports with reproduction inputs and expected/actual behavior;
- documentation fixes;
- Domain Pack additions and schema requirements;
- privacy-safe evidence and source metadata;
- the exact test commands from the repository;
- PR scope and review expectations;
- prohibition on hidden promotion, unsupported credentials, and learner-output branding.

Use these exact headings so the test contract is stable:

```markdown
# Contributing to Learning Architect

## 中文贡献指南

### 可以贡献什么
### Domain Pack 贡献要求
### 提交前验证
### 品牌、隐私与内容边界
### Pull Request 要求

## English Contribution Guide

### What you can contribute
### Domain Pack requirements
### Validation before submission
### Brand, privacy, and content boundaries
### Pull Request requirements
```

Include the literal phrases `禁止隐藏推广` and `No hidden promotion` in the boundary sections.

- [ ] **Step 5: Run the focused test and verify GREEN**

Run the same focused command.

Expected: `Ran 2 tests` and `OK`.

- [ ] **Step 6: Commit Task 1**

```bash
git add LICENSE VERSION CONTRIBUTING.md tests/learning-architect/test_open_source_package.py
git commit -m "chore: add open-source project contract"
```

---

### Task 2: Write the Chinese Documentation Set

**Files:**
- Modify: `tests/learning-architect/test_open_source_package.py`
- Create: `docs/getting-started.md`
- Create: `docs/usage-guide.md`
- Create: `docs/examples.md`
- Create: `docs/domain-pack-guide.md`

**Interfaces:**
- Consumes: existing Skill workflow, schemas, Domain Pack contract, and root version `1.0.0`.
- Produces: complete Chinese reader path later linked from `README.md`.

- [ ] **Step 1: Add a failing Chinese-doc contract test**

Add this method to `OpenSourcePackageTests`:

```python
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
```

- [ ] **Step 2: Run the Chinese contract and verify RED**

```bash
python3 -m unittest tests/learning-architect/test_open_source_package.py -q
```

Expected: `Ran 3 tests` with a failure on missing `docs/getting-started.md`.

- [ ] **Step 3: Write `docs/getting-started.md`**

Use the required headings and include:

- a 30-second explanation of the Skill;
- prerequisites: goal, current baseline, weekly capacity, budget, constraints, and preferred evidence/project outcome;
- one copyable first prompt;
- why the Skill asks decision-critical questions before planning;
- how to answer without completing all 48 discovery questions at once;
- the second-turn request for a first complete system;
- resume, evidence update, constraint change, and target-change prompts;
- explicit statement that external outcomes are not guaranteed.

- [ ] **Step 4: Write `docs/usage-guide.md`**

Document every workflow stage in order and for each stage state:

- its decision purpose;
- minimum inputs;
- output artifact;
- gate behavior;
- common user continuation prompt.

Also document the natural-language plus `engine_result` return contract, epistemic classes, activity-versus-capability distinction, versioned state, rollback, privacy, and high-risk review behavior.

- [ ] **Step 5: Write `docs/examples.md`**

For each of the four required scenarios, include exactly these five labeled blocks:

```markdown
### 首次提示词
### Skill 可能追问什么
### 可能形成的产物
### 第二轮继续提示词
### 学习后的复盘与重规划提示词
```

Use realistic but non-guaranteed examples. Do not mention ZJSkills, community, or courses inside prompt outputs.

- [ ] **Step 6: Write `docs/domain-pack-guide.md`**

Explain stable IDs, `schema_version`, `content_version`, `status`, target outcomes, competency L0-L5 behaviors, dependency rules, project archetypes, typed `critical` and `passing_threshold` rubric fields, sourcing, review dates, migrations, validator commands, and contribution expectations. Link to the existing schema and AI Agent pack with relative paths.

- [ ] **Step 7: Run the Chinese contract and existing tests**

Run:

```bash
python3 -m unittest tests/learning-architect/test_open_source_package.py -q
python3 -m unittest tests/learning-architect/test_validate_learning_system.py -q
```

Expected: open-source tests `Ran 3 tests ... OK`; existing tests `Ran 84 tests ... OK`.

- [ ] **Step 8: Commit Task 2**

```bash
git add docs/getting-started.md docs/usage-guide.md docs/examples.md docs/domain-pack-guide.md tests/learning-architect/test_open_source_package.py
git commit -m "docs: add Chinese Learning Architect guides"
```

---

### Task 3: Write the English Documentation Set

**Files:**
- Modify: `tests/learning-architect/test_open_source_package.py`
- Create: `docs/getting-started.en.md`
- Create: `docs/usage-guide.en.md`
- Create: `docs/examples.en.md`
- Create: `docs/domain-pack-guide.en.md`

**Interfaces:**
- Consumes: approved Chinese information architecture and existing English Skill terminology.
- Produces: semantically equivalent English reader path later linked from `README.en.md`.

- [ ] **Step 1: Add a failing English-doc contract test**

Add:

```python
def test_english_document_set_is_complete(self):
    required = {
        "docs/getting-started.en.md": (
            "# Learning Architect Getting Started",
            "## First use",
            "## Why it asks before planning",
            "## How to continue",
            "## How to replan",
        ),
        "docs/usage-guide.en.md": (
            "# Learning Architect Full Usage Guide",
            "## Complete workflow",
            "## Artifacts and structured state",
            "## Evidence and capability judgment",
            "## Failure and safety boundaries",
        ),
        "docs/examples.en.md": (
            "# Learning Architect Scenarios and Prompts",
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
```

- [ ] **Step 2: Run and verify RED**

Run the focused open-source test file.

Expected: failure on missing `docs/getting-started.en.md`.

- [ ] **Step 3: Write all four English guides**

Translate concepts, not sentence order. Preserve stable identifiers and exact machine terms such as `engine_result`, `needs_input`, `epistemic_class`, `critical`, and `passing_threshold`. Match every content contract from Task 2 and keep the same five scenario blocks under English labels:

```markdown
### First prompt
### What the Skill may ask
### Likely artifacts
### Second-turn continuation prompt
### Progress review and replanning prompt
```

- [ ] **Step 4: Run English, Chinese, and existing regression tests**

Expected: open-source tests `Ran 4 tests ... OK`; existing tests `Ran 84 tests ... OK`.

- [ ] **Step 5: Commit Task 3**

```bash
git add docs/getting-started.en.md docs/usage-guide.en.md docs/examples.en.md docs/domain-pack-guide.en.md tests/learning-architect/test_open_source_package.py
git commit -m "docs: add English Learning Architect guides"
```

---

### Task 4: Productize the Bilingual Repository Homepages

**Files:**
- Modify: `tests/learning-architect/test_open_source_package.py`
- Modify: `README.md`
- Create: `README.en.md`
- Delete: `README.zh-CN.md`

**Interfaces:**
- Consumes: all docs from Tasks 2 and 3, `VERSION`, `LICENSE`, and `CONTRIBUTING.md`.
- Produces: Chinese default entry, English entry, and a repository-wide Markdown link contract.

- [ ] **Step 1: Add failing homepage, version, and link tests**

Add these imports, then add the tests:

```python
import re
from urllib.parse import unquote
```

Add:

```python
def test_readme_pair_and_version_surface(self):
    self.assertFalse((REPO_ROOT / "README.zh-CN.md").exists())
    chinese = read_text("README.md")
    english = read_text("README.en.md")
    for text in (chinese, english):
        self.assertIn("1.0.0", text)
        self.assertIn("MIT", text)
        self.assertIn("ZJSkills", text)
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
```

- [ ] **Step 2: Run and verify RED**

Expected: missing `README.en.md`, stale `README.zh-CN.md`, and unresolved target failures.

- [ ] **Step 3: Replace the root README with the Chinese product homepage**

Use these exact top-level sections:

```markdown
# Learning Architect
## 它解决什么问题
## 快速开始
## 安装
## 你会得到什么
## 工作方式
## 完整文档
## 项目结构
## 贡献
## 发起与维护
## 许可证
```

The top must include `[English](README.en.md)`, version `1.0.0`, `84 tests`, and `MIT`. The maintainer section may contain only `由 ZJSkills（智建）发起并维护。` Do not add personal proof, contact, community, or course copy.

- [ ] **Step 4: Create the semantically equivalent English homepage**

Use:

```markdown
# Learning Architect
## What it helps you solve
## Quick start
## Install
## What you get
## How it works
## Full documentation
## Project structure
## Contributing
## Initiator and maintainer
## License
```

The top must include `[简体中文](README.md)`, version `1.0.0`, `84 tests`, and `MIT`. The maintainer sentence is `Initiated and maintained by ZJSkills.`

- [ ] **Step 5: Remove the stale language file and update all links**

Delete `README.zh-CN.md` with `apply_patch`. Ensure no tracked file links to it:

```bash
rg -n "README\.zh-CN\.md" README.md README.en.md CONTRIBUTING.md docs/*.md
```

Expected: no output. Historical design and plan documents may mention the migration intentionally and are excluded from this command.

- [ ] **Step 6: Run open-source and existing tests**

Expected: open-source tests `Ran 6 tests ... OK`; existing tests `Ran 84 tests ... OK`.

- [ ] **Step 7: Commit Task 4**

```bash
git add README.md README.en.md README.zh-CN.md tests/learning-architect/test_open_source_package.py
git commit -m "docs: productize bilingual repository homepages"
```

---

### Task 5: Broaden Skill Discovery Without Brand Leakage

**Files:**
- Modify: `tests/learning-architect/test_open_source_package.py`
- Modify: `learning-architect/SKILL.md:1-3`
- Modify: `learning-architect/agents/openai.yaml:1-6`

**Interfaces:**
- Consumes: existing runtime workflow and current `agents/openai.yaml` interface contract.
- Produces: broader trigger metadata while guaranteeing runtime brand isolation.

- [ ] **Step 1: Add failing metadata and brand-isolation tests**

Add:

```python
def test_skill_metadata_covers_ai_exploration_and_transition(self):
    skill = read_text("learning-architect/SKILL.md")
    for phrase in (
        "AI industry exploration",
        "AI learning-direction decisions",
        "AI career-transition planning",
        "personalized learning path",
    ):
        self.assertIn(phrase, skill)

def test_runtime_skill_is_brand_and_promotion_neutral(self):
    forbidden = ("ZJSkills", "智建", "社群", "community link", "课程推广")
    violations = []
    for path in RUNTIME_ROOT.rglob("*"):
        if not path.is_file() or "__pycache__" in path.parts:
            continue
        if path.suffix.lower() not in {".md", ".yaml", ".yml", ".txt", ".py"}:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for phrase in forbidden:
            if phrase in text:
                violations.append(f"{path.relative_to(REPO_ROOT)}: {phrase}")
    self.assertEqual(violations, [])
```

- [ ] **Step 2: Run and verify RED**

Expected: metadata test fails because the current frontmatter does not contain the three new AI discovery phrases; brand-isolation test passes.

- [ ] **Step 3: Update the Skill frontmatter description**

Replace only the `description` value with:

```yaml
description: Use when someone needs AI industry exploration, AI learning-direction decisions, AI career-transition planning, a personalized learning path, competency map, project-based curriculum, weekly study system, assessment strategy, outcome preparation, or adaptive replanning for employment, promotion, entrepreneurship, or real project delivery.
```

Do not add a brand section or change ordered workflow behavior.

- [ ] **Step 4: Check and update Codex interface metadata only if inconsistent**

Retain `display_name: "Learning Architect"` and the current neutral Chinese short description. Update `default_prompt` to:

```yaml
default_prompt: "Use $learning-architect to analyze my AI learning or career goal and design an evidence-based personalized learning system."
```

Do not add ZJSkills to `agents/openai.yaml`.

- [ ] **Step 5: Run Skill and package validation**

Run:

```bash
python3 /Users/wangshucheng/.codex/skills/.system/skill-creator/scripts/quick_validate.py learning-architect
python3 -m unittest tests/learning-architect/test_open_source_package.py -q
python3 -m unittest tests/learning-architect/test_validate_learning_system.py -q
```

Expected: Skill valid; open-source tests `Ran 8 tests ... OK`; existing tests `Ran 84 tests ... OK`.

- [ ] **Step 6: Commit Task 5**

```bash
git add learning-architect/SKILL.md learning-architect/agents/openai.yaml tests/learning-architect/test_open_source_package.py
git commit -m "feat: broaden Learning Architect discovery"
```

---

### Task 6: Complete Verification, Reader Tests, Installation, and PR Update

**Files:**
- Modify only if verification exposes a defect: files from Tasks 1-5.
- Verify: `learning-architect/`, `tests/learning-architect/`, root docs, installed copy.

**Interfaces:**
- Consumes: complete bilingual open-source package and existing feature branch.
- Produces: verified branch, refreshed installed Skill, reader/behavior evidence, and updated Draft PR.

- [ ] **Step 1: Run the complete local gate**

Run:

```bash
export PATH="/Users/wangshucheng/miniconda3/bin:$PATH"
export PYTHONDONTWRITEBYTECODE=1
python3 /Users/wangshucheng/.codex/skills/.system/skill-creator/scripts/quick_validate.py learning-architect
python3 -m unittest discover -s tests/learning-architect -p "test_*.py" -q
python3 learning-architect/scripts/validate_learning_system.py --skill-root learning-architect --learner-dir tests/learning-architect/fixtures/valid-learner
python3 -c 'from pathlib import Path; import yaml; files=list(Path("learning-architect").rglob("*.yaml"))+list(Path("tests/learning-architect").rglob("*.yaml")); [yaml.safe_load(p.read_text()) for p in files]; print(f"YAML VALID {len(files)}")'
git diff --check
```

Expected:

- `Skill is valid!`
- `Ran 92 tests ... OK` (84 existing + 8 packaging tests)
- `VALID`
- `YAML VALID 40`
- no `git diff --check` output.

- [ ] **Step 2: Run command and link smoke checks from both README paths**

Execute every non-destructive validation command documented in both README files and confirm the stated working directory. Re-run:

```bash
rg -n "README\.zh-CN\.md|ZJSkills|智建|社群|课程推广" learning-architect
```

Expected: no output.

- [ ] **Step 3: Run fresh Chinese and English reader tests**

Dispatch fresh readers with only the corresponding README and docs. Each reader must answer:

1. What does the Skill solve?
2. Who should use it?
3. How is it installed?
4. What first prompt should be sent?
5. Why might Discovery precede a plan?
6. What artifacts should be expected?
7. How does replanning work?
8. How is a Domain Pack contributed?

Treat any incorrect answer, broken link, missing prerequisite, or mismatched Chinese/English claim as a defect; fix and rerun the affected reader.

- [ ] **Step 4: Run four fresh behavior forward tests**

Use the worktree Skill path for these realistic requests without providing expected answers:

- zero-background AI industry exploration;
- transition to AI Agent Engineer;
- transition to AI Product Manager;
- apply AI in current work.

Review raw outputs for Discovery routing, evidence labeling, no course-list dumping, no outcome guarantee, and no brand/community/course promotion. Fix only real transferable defects and rerun the affected case.

- [ ] **Step 5: Commit any verification corrections**

If corrections were needed:

```bash
git add README.md README.en.md LICENSE VERSION CONTRIBUTING.md docs/getting-started.md docs/getting-started.en.md docs/usage-guide.md docs/usage-guide.en.md docs/examples.md docs/examples.en.md docs/domain-pack-guide.md docs/domain-pack-guide.en.md learning-architect/SKILL.md learning-architect/agents/openai.yaml tests/learning-architect/test_open_source_package.py
git commit -m "fix: close open-source documentation gaps"
```

If no corrections were needed, do not create an empty commit.

- [ ] **Step 6: Push the branch and refresh the installed copy**

Push `codex/learning-architect` to the existing remote and Draft PR. Then preserve the current installed copy as a temporary backup, install the branch version using the system installer, and validate the new installed path. Do not silently delete a user-modified installed copy.

Use these exact commands after confirming `/tmp/learning-architect-installed-backup-20260717` does not already exist:

```bash
git push
test ! -e /tmp/learning-architect-installed-backup-20260717
mv /Users/wangshucheng/.codex/skills/learning-architect /tmp/learning-architect-installed-backup-20260717
python3 /Users/wangshucheng/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py --repo zhijianZJ/ZJSklls --path learning-architect --ref codex/learning-architect
```

If installation fails before the new destination exists, restore with:

```bash
mv /tmp/learning-architect-installed-backup-20260717 /Users/wangshucheng/.codex/skills/learning-architect
```

Required checks:

```bash
git status -sb
python3 /Users/wangshucheng/.codex/skills/.system/skill-creator/scripts/quick_validate.py /Users/wangshucheng/.codex/skills/learning-architect
diff -qr learning-architect /Users/wangshucheng/.codex/skills/learning-architect
```

Expected: clean tracking branch, successful push, installed Skill valid, and no content difference except ignored Python cache files.

After the installed-copy checks, run one fresh AI Agent Engineer first-turn request against `/Users/wangshucheng/.codex/skills/learning-architect` and confirm Discovery routing, evidence labeling, no guarantee, and no promotion. This satisfies the installed-copy behavior gate separately from the worktree forward tests.

- [ ] **Step 7: Verify the Draft PR**

Use GitHub CLI to confirm the existing Draft PR contains all new commits, still targets `main`, and remains Draft. Update the PR description to mention:

- ZJSkills light attribution;
- MIT `1.0.0` packaging;
- bilingual README and guides;
- broadened discovery metadata;
- total test count and installed-copy validation.

- [ ] **Step 8: Final handoff**

Report exact commit IDs, PR URL, validation counts, installed path, reader-test verdict, behavior-test verdict, and any intentionally deferred non-goals. Remind the user that the refreshed installed Skill is discoverable on the next Codex turn.
