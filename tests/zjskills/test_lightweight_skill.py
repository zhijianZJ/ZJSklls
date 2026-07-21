from pathlib import Path
import re
import subprocess
import unittest


REPO_ROOT = Path(__file__).resolve().parents[2]
RUNTIME_ROOT = REPO_ROOT / "zjskills"
SCENARIO_INVENTORY = Path(__file__).with_name("scenarios.yaml")

EXPECTED_RUNTIME_FILES = {
    "zjskills/SKILL.md",
    "zjskills/agents/openai.yaml",
    "zjskills/references/ai-career-map.md",
    "zjskills/references/career-diagnosis.md",
    "zjskills/references/learning-help.md",
    "zjskills/references/learning-route.md",
}

EXPECTED_SCENARIO_IDS = (
    "vague-ai-transition",
    "compare-agent-vibe",
    "no-coding-evidence",
    "learning-overload",
    "concept-confusion",
    "incomplete-error",
    "missed-week",
    "changed-goal",
    "non-ai-without-source",
    "enough-context-no-question",
    "broad-title-assets",
    "demonstrated-transferable-asset",
    "returned-validation-result",
    "current-market-without-region",
    "supplied-postings-market",
)

EXPECTED_EVALUATION_DIMENSIONS = (
    "mode",
    "question_count",
    "main_action_count",
    "asset_evidence_boundary",
    "opportunity_count",
    "stage_decision_closure",
    "current_market_source_boundary",
    "promise_boundary",
    "recommendation_fit",
    "beginner_readability",
)

EXPECTED_CURRENT_MARKET_PROMPT = (
    "AI建筑产品经理现在薪资多少？未来12到24个月是不是黄金窗口？直接给结论。"
)


def read_runtime(relative_path: str) -> str:
    return (RUNTIME_ROOT / relative_path).read_text(encoding="utf-8")


def tracked_runtime_files() -> set[str]:
    result = subprocess.run(
        ["git", "ls-files", "zjskills"],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return {line for line in result.stdout.splitlines() if line}


class LightweightSkillTests(unittest.TestCase):
    def assert_contract_phrase(self, text: str, phrase: str):
        matching_lines = "\n".join(
            line for line in text.splitlines() if phrase in line
        )
        self.assertIn(phrase, matching_lines, phrase)

    def level_two_section(self, text: str, heading: str) -> str:
        marker = f"## {heading}"
        self.assert_contract_phrase(text, marker)
        remainder = text.split(marker, 1)[1]
        next_heading = re.search(r"(?m)^##\s+", remainder)
        return remainder[: next_heading.start()] if next_heading else remainder

    def markdown_heading_names(self, text: str) -> list[str]:
        headings = []
        fence_marker = None
        for line in text.splitlines():
            fence = re.match(r"^\s*(`{3,}|~{3,})", line)
            if fence and fence_marker is None:
                fence_marker = fence.group(1)[0]
                continue
            if fence and fence.group(1)[0] == fence_marker:
                fence_marker = None
                continue
            if fence_marker is not None:
                continue
            match = re.fullmatch(r"#{1,6}\s+(.+?)(?:\s+#+)?\s*", line)
            if match:
                headings.append(match.group(1))
        return headings

    def assert_markdown_sections_in_order(
        self, text: str, sections: tuple[str, ...]
    ):
        headings = self.markdown_heading_names(text)
        positions = []
        for section in sections:
            self.assertIn(section, headings, section)
            positions.append(headings.index(section))
        self.assertEqual(positions, sorted(positions), sections)

    def test_runtime_contains_only_the_six_approved_files(self):
        self.assertEqual(tracked_runtime_files(), EXPECTED_RUNTIME_FILES)

    def test_forward_scenario_inventory_has_exactly_the_fifteen_approved_ids(self):
        inventory = SCENARIO_INVENTORY.read_text(encoding="utf-8")
        scenario_ids = tuple(
            re.findall(r"(?m)^\s*-\s*\{id:\s*([^,}\s]+)", inventory)
        )
        self.assertEqual(scenario_ids, EXPECTED_SCENARIO_IDS)

    def test_forward_scenario_inventory_has_nonempty_prompts(self):
        inventory = SCENARIO_INVENTORY.read_text(encoding="utf-8")
        entries = re.findall(r"(?m)^\s*-\s*\{id:.*\}\s*$", inventory)
        self.assertEqual(len(entries), len(EXPECTED_SCENARIO_IDS))
        for entry in entries:
            match = re.search(r'prompt:\s*"(.+?)"\s*}', entry)
            self.assertIsNotNone(match, entry)
            self.assertTrue(match.group(1).strip(), entry)

    def test_current_market_scenario_supplies_period_but_not_region(self):
        inventory = SCENARIO_INVENTORY.read_text(encoding="utf-8")
        match = re.search(
            r'(?m)^\s*-\s*\{id:\s*current-market-without-region,.*prompt:\s*"([^"]+)"\s*\}\s*$',
            inventory,
        )
        self.assertIsNotNone(match)
        self.assertEqual(match.group(1), EXPECTED_CURRENT_MARKET_PROMPT)

    def test_forward_scenario_inventory_has_exact_evaluation_dimensions(self):
        inventory = SCENARIO_INVENTORY.read_text(encoding="utf-8")
        dimensions_section = inventory.split("evaluation_dimensions:", 1)
        self.assertEqual(len(dimensions_section), 2)
        dimensions = tuple(
            re.findall(r"(?m)^\s+-\s+([a-z_]+)\s*$", dimensions_section[1])
        )
        self.assertEqual(dimensions, EXPECTED_EVALUATION_DIMENSIONS)

    def test_forward_scenario_inventory_does_not_leak_expected_outputs(self):
        inventory = SCENARIO_INVENTORY.read_text(encoding="utf-8").lower()
        for leakage_term in (
            "must answer",
            "expected response",
            "应该输出",
            "正确答案",
        ):
            self.assertNotIn(leakage_term, inventory, leakage_term)

    def test_runtime_respects_size_budgets(self):
        missing = sorted(
            path for path in EXPECTED_RUNTIME_FILES if not (REPO_ROOT / path).is_file()
        )
        self.assertEqual(missing, [])
        skill_lines = len(read_runtime("SKILL.md").splitlines())
        markdown_lines = sum(
            len((REPO_ROOT / path).read_text(encoding="utf-8").splitlines())
            for path in EXPECTED_RUNTIME_FILES
            if path.endswith(".md")
        )
        self.assertLessEqual(skill_lines, 180)
        self.assertLessEqual(markdown_lines, 800)

    def test_skill_frontmatter_description_covers_all_three_entry_needs(self):
        skill = read_runtime("SKILL.md")
        frontmatter = skill.split("---", 2)[1].lower()
        self.assertIn("name: zjskills", frontmatter)
        for trigger in ("ai career direction", "learning route", "getting unstuck"):
            self.assertIn(trigger, frontmatter, trigger)

    def test_skill_defines_exactly_three_modes(self):
        skill = read_runtime("SKILL.md")
        self.assert_contract_phrase(skill, "## Choose One Mode")
        mode_section = skill.split("## Choose One Mode", 1)[1].split("\n## ", 1)[0]
        modes = re.findall(r"^\d+\.\s+(.+?)\s*$", mode_section, flags=re.MULTILINE)
        self.assertEqual(
            [mode.lower() for mode in modes],
            ["career diagnosis", "learning route", "learning help"],
        )

    def test_skill_chooses_exactly_one_mode_for_each_request(self):
        skill = read_runtime("SKILL.md")
        self.assert_contract_phrase(
            skill, "Choose exactly one mode for each user request."
        )
        self.assertNotIn("multiple modes by default", skill.lower())

    def test_skill_uses_context_first_entry_and_zero_or_one_question(self):
        skill = read_runtime("SKILL.md")
        for phrase in (
            "$zjskills",
            "/zjskills",
            "Read the current conversation first.",
            "Reuse facts, goals, constraints, prior conclusions, and feedback already supplied.",
            "If evidence is sufficient, work immediately.",
            "If one missing fact could change the judgment, ask only that one question.",
        ):
            self.assert_contract_phrase(skill, phrase)

    def test_skill_handles_bare_invocation_without_exposing_an_internal_menu(self):
        start = self.level_two_section(read_runtime("SKILL.md"), "Start")
        self.assertRegex(start, r"(?i)no usable (?:task or )?context")
        self.assertRegex(start, r"(?i)invite .*one real situation.*ordinary language")
        self.assertRegex(start, r"(?i)do not (?:show|display|expose).*internal menu")

    def test_skill_explains_beginner_onboarding_then_enters_a_real_task(self):
        start = self.level_two_section(read_runtime("SKILL.md"), "Start")
        self.assertIn("新手入门", start)
        for concept in ("what they can submit", "how ZJSkills processes it", "what they receive"):
            self.assertIn(concept, start, concept)
        self.assertRegex(start, r"(?i)continue .*first real task")

    def test_skill_states_the_non_ai_domain_boundary(self):
        skill = read_runtime("SKILL.md")
        for phrase in (
            "Domain standards, market facts, licensing requirements, safety rules, and readiness criteria may be unknown or unestablished.",
            "Request the smallest reliable source, rubric, or qualified feedback needed.",
            "Never impersonate a domain expert.",
        ):
            self.assert_contract_phrase(skill, phrase)

    def test_current_market_claims_require_attributed_current_evidence(self):
        combined = read_runtime("SKILL.md") + read_runtime(
            "references/career-diagnosis.md"
        )
        for claim in (
            "salary or compensation range",
            "hiring volume or talent shortage",
            "named employer demand",
            "job title prevalence",
            "market window",
        ):
            self.assertIn(claim, combined)
        for field in ("source", "date", "region", "sample limitation"):
            self.assertIn(field, combined)

    def test_current_market_protocol_sets_scope_before_market_judgment(self):
        diagnosis = read_runtime("references/career-diagnosis.md")
        market_section = self.level_two_section(
            diagnosis, "Current-market evidence"
        )
        scope = "Determine the relevant region and target period from the existing context first."
        missing = "If either scope item is missing"
        judgment = "Only after the scope is set"
        for phrase in (scope, missing, judgment):
            self.assert_contract_phrase(market_section, phrase)
        self.assertLess(market_section.index(scope), market_section.index(judgment))
        self.assertIn("ask one key scope question", market_section)
        self.assertIn("state the missing boundary", market_section)
        self.assertIn(
            "When the target period is already supplied, reuse it and do not ask for it again.",
            market_section,
        )
        self.assertIn(
            "If only the region is missing, ask only for the region or state that boundary.",
            market_section,
        )

    def test_missing_current_market_evidence_does_not_block_structural_guidance(self):
        diagnosis = read_runtime("references/career-diagnosis.md")
        self.assertIn(
            "state that the current-market claim is unverified", diagnosis
        )
        self.assertIn(
            "continue with structural fit and one validation action", diagnosis
        )

    def test_runtime_rejects_false_precision_in_default_diagnosis(self):
        diagnosis = read_runtime("references/career-diagnosis.md").lower()
        for phrase in ("top 5", "five-star", "percentage fit score"):
            self.assertIn(phrase, diagnosis)

    def test_skill_does_not_invent_a_non_ai_route_without_domain_evidence(self):
        skill = read_runtime("SKILL.md")
        self.assert_contract_phrase(
            skill,
            "When the user supplies no reliable domain source, do not invent the route; ask one decisive question for the jurisdiction or smallest official source instead.",
        )

    def test_skill_defaults_to_chat_and_writes_one_route_only_on_request(self):
        skill = read_runtime("SKILL.md")
        for phrase in (
            "Default to chat output.",
            "Create one Markdown file only when the user explicitly asks to save, export, or maintain a continuing route.",
        ):
            self.assert_contract_phrase(skill, phrase)

    def test_skill_conditionally_loads_all_four_references(self):
        skill = read_runtime("SKILL.md")
        load_section = self.level_two_section(skill, "Load Only What Is Needed")
        approved_references = (
            "references/career-diagnosis.md",
            "references/learning-route.md",
            "references/learning-help.md",
            "references/ai-career-map.md",
        )
        table_lines = [
            line.strip()
            for line in load_section.splitlines()
            if line.strip().startswith("|") and line.strip().endswith("|")
        ]
        self.assertGreaterEqual(len(table_lines), 3, table_lines)

        def cells(line: str) -> list[str]:
            return [cell.strip() for cell in line.strip("|").split("|")]

        header_cells = cells(table_lines[0])
        separator_cells = cells(table_lines[1])
        self.assertGreaterEqual(len(header_cells), 2, header_cells)
        self.assertTrue(all(header_cells), header_cells)
        self.assertEqual(len(separator_cells), len(header_cells))
        self.assertTrue(
            all(re.fullmatch(r":?-{3,}:?", cell) for cell in separator_cells),
            separator_cells,
        )

        data_rows = [cells(line) for line in table_lines[2:]]
        self.assertEqual(len(data_rows), len(approved_references), data_rows)
        reference_rows = {}
        reference_cell_indexes = []
        for row_index, row in enumerate(data_rows):
            self.assertEqual(len(row), len(header_cells), row)
            matches = [
                (cell_index, reference)
                for cell_index, cell in enumerate(row)
                for reference in approved_references
                if reference in cell
            ]
            self.assertEqual(len(matches), 1, row)
            reference_cell_index, reference = matches[0]
            reference_cell_indexes.append(reference_cell_index)
            self.assertEqual(row[reference_cell_index].strip("`"), reference, row)
            condition_cells = [
                cell
                for cell_index, cell in enumerate(row)
                if cell_index != reference_cell_index and cell
            ]
            self.assertTrue(condition_cells, row)
            reference_rows.setdefault(reference, []).append(row_index)

        self.assertEqual(len(set(reference_cell_indexes)), 1, reference_cell_indexes)
        reference_column = reference_cell_indexes[0]
        condition_columns = [
            column
            for column in range(len(header_cells))
            if column != reference_column and all(row[column] for row in data_rows)
        ]
        self.assertTrue(condition_columns, data_rows)
        for reference in approved_references:
            self.assertEqual(len(reference_rows.get(reference, [])), 1, reference)
            self.assertEqual(load_section.count(reference), 1, reference)
        self.assertEqual(
            len({rows[0] for rows in reference_rows.values()}),
            len(approved_references),
            reference_rows,
        )

    def test_career_diagnosis_has_the_compact_output_contract(self):
        self.assertTrue(
            (RUNTIME_ROOT / "references/career-diagnosis.md").is_file()
        )
        diagnosis = read_runtime("references/career-diagnosis.md")
        self.assert_markdown_sections_in_order(
            diagnosis,
            (
                "Your current situation",
                "Your transferable career assets",
                "The real problem to solve",
                "Opportunity hypotheses",
                "My judgment and evidence",
                "One minimum validation action",
                "How the result changes the decision",
            ),
        )

    def test_career_diagnosis_translates_assets_without_inventing_them(self):
        diagnosis = read_runtime("references/career-diagnosis.md")
        for phrase in (
            "Demonstrated asset",
            "Transfer hypothesis",
            "Unverified boundary",
            "observed work or result",
            "problem solved",
            "demonstrated capability",
            "possible AI transfer",
            "missing evidence",
        ):
            self.assert_contract_phrase(diagnosis, phrase)
        self.assertIn("no more than three opportunity hypotheses", diagnosis)
        self.assertIn("Do not infer capability from a title, employer, degree, or years of experience alone.", diagnosis)

    def test_opportunity_hypotheses_do_not_create_parallel_assignments(self):
        diagnosis = read_runtime("references/career-diagnosis.md")
        for phrase in (
            "candidate validation idea",
            "not a current assignment",
            "Choose exactly one current minimum action from the candidate validation ideas",
            "reduce the current decision uncertainty",
            "test one stronger hypothesis",
            "contrast two still-plausible hypotheses",
            "Never ask the user to execute validation ideas for multiple hypotheses in parallel.",
        ):
            self.assert_contract_phrase(diagnosis, phrase)
        self.assertNotIn("leading hypothesis", diagnosis.lower())

    def test_skill_keeps_asset_reasoning_evidence_bounded(self):
        skill = read_runtime("SKILL.md")
        self.assertIn("Translate observed work and results into demonstrated assets", skill)
        self.assertIn("Label possible transfer as a hypothesis until new-task evidence supports it.", skill)

    def test_career_diagnosis_defines_exactly_four_stage_decisions(self):
        diagnosis = read_runtime("references/career-diagnosis.md")
        decisions = re.findall(r"(?m)^\d+\. \*\*(.+?):\*\*", diagnosis)
        self.assertEqual(
            decisions,
            [
                "Route ready",
                "Comparison remains",
                "Foundation or constraint first",
                "Current-role application first",
            ],
        )

    def test_returned_result_reuses_context_and_closes_one_stage(self):
        skill = read_runtime("SKILL.md")
        for phrase in (
            "When the user returns with a minimum-task result, reuse the prior diagnosis.",
            "Choose exactly one stage decision",
            "Do not repeat intake.",
        ):
            self.assert_contract_phrase(skill, phrase)

    def test_returned_result_review_emits_only_one_decision_and_one_action(self):
        diagnosis = read_runtime("references/career-diagnosis.md")
        for phrase in (
            "For an initial diagnosis",
            "For a returned-result review",
            "use the same seven headings",
            "write only compact changes",
            "Under `How the result changes the decision`",
            "output only the selected stage decision and one next action",
            "Do not list the other three decisions",
        ):
            self.assert_contract_phrase(diagnosis, phrase)
        self.assertIn(
            "Do not repeat the full initial diagnosis.", diagnosis
        )

    def test_diagnosis_has_exactly_one_current_action_contract(self):
        diagnosis = read_runtime("references/career-diagnosis.md")
        for phrase in (
            "Select exactly one current minimum action from the candidate validation ideas",
            "greatest expected reduction in current decision uncertainty",
            "The candidate validation ideas are alternatives, not additional actions.",
        ):
            self.assert_contract_phrase(diagnosis, phrase)

    def test_returned_diagnosis_result_routes_to_diagnosis_not_learning_help(self):
        load_section = self.level_two_section(
            read_runtime("SKILL.md"), "Load Only What Is Needed"
        )
        rows = [
            line
            for line in load_section.splitlines()
            if line.startswith("|") and "references/" in line
        ]
        diagnosis_row = next(
            line for line in rows if "references/career-diagnosis.md" in line
        )
        help_row = next(
            line for line in rows if "references/learning-help.md" in line
        )
        self.assertIn(
            "returns with a minimum experience-task result from Career Diagnosis",
            diagnosis_row,
        )
        self.assertIn(
            "other than a returned Career Diagnosis minimum experience-task result",
            help_row,
        )

    def test_learning_route_consumes_the_route_ready_handoff(self):
        route = read_runtime("references/learning-route.md")
        self.assertIn(
            "stage decision is `Route ready`",
            route,
        )
        for phrase in (
            "stage decision",
            "demonstrated assets",
            "target direction",
            "primary gap",
            "important constraint",
        ):
            self.assertIn(phrase, route)

    def test_learning_route_has_the_three_stage_output_contract(self):
        self.assertTrue((RUNTIME_ROOT / "references/learning-route.md").is_file())
        route = read_runtime("references/learning-route.md")
        self.assert_markdown_sections_in_order(
            route,
            (
                "Target",
                "Current starting point",
                "Stage 1: capability and deliverable",
                "Stage 2: capability and deliverable",
                "Stage 3: target-level deliverable",
                "Evidence project for each stage",
                "Only this week's action",
            ),
        )

    def test_learning_help_has_one_action_and_fallback_contract(self):
        self.assertTrue((RUNTIME_ROOT / "references/learning-help.md").is_file())
        help_text = read_runtime("references/learning-help.md")
        self.assert_markdown_sections_in_order(
            help_text,
            (
                "Where you are stuck",
                "Most likely cause",
                "Do this one action first",
                "Observable success signal",
                "If it fails, check this next",
                "Route impact",
            ),
        )

    def test_ai_career_map_covers_all_directions_and_operations_branches(self):
        self.assertTrue((RUNTIME_ROOT / "references/ai-career-map.md").is_file())
        career_map = read_runtime("references/ai-career-map.md")
        for phrase in (
            "AI Agent Development",
            "Vibe Coding / AI Application Building",
            "AI Product Management",
            "AI Operations: Content/Growth",
            "AI Operations: Business Efficiency",
            "AI Tools and Workplace Application",
        ):
            self.assert_contract_phrase(career_map, phrase)

    def test_beginner_facing_runtime_omits_legacy_system_terms(self):
        beginner_paths = (
            "SKILL.md",
            "references/career-diagnosis.md",
            "references/learning-route.md",
            "references/learning-help.md",
        )
        missing = sorted(
            path for path in beginner_paths if not (RUNTIME_ROOT / path).is_file()
        )
        self.assertEqual(missing, [])
        beginner_instructions = "\n".join(
            read_runtime(path) for path in beginner_paths
        ).lower()
        instruction_tokens = set(re.findall(r"[a-z0-9.-]+", beginner_instructions))
        for phrase in ("11-stage", "system-state.yaml", "schema", "gate"):
            self.assertNotIn(phrase, instruction_tokens, phrase)

    def test_runtime_has_no_referral_or_conversion_instructions(self):
        runtime = "\n".join(
            (REPO_ROOT / path).read_text(encoding="utf-8")
            for path in sorted(EXPECTED_RUNTIME_FILES)
            if path.endswith((".md", ".yaml"))
            and (REPO_ROOT / path).exists()
        ).lower()
        forbidden = (
            "联系智建",
            "答疑群",
            "加入社群",
            "加微信",
            "购买课程",
            "转化用户",
            "人工转介",
            "contact zhijian",
            "join the q&a group",
            "add wechat",
            "lead conversion",
        )
        for phrase in forbidden:
            self.assertNotIn(phrase, runtime, phrase)

    def test_runtime_analyzes_before_recommending_learning_support(self):
        skill = read_runtime("SKILL.md")
        self.assertNotIn("Do not act as a course recommender", skill)
        for phrase in (
            "Do not assume self-study is better than paid or structured learning.",
            "first identify the learner's actual problem, evidence, constraints, and missing support",
            "Recommend external learning support only when it solves a named need",
            "Do not begin by discouraging enrollment, membership, or paid learning.",
        ):
            self.assert_contract_phrase(skill, phrase)


if __name__ == "__main__":
    unittest.main()
