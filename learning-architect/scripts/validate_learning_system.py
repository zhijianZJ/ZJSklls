#!/usr/bin/env python3
"""Validate Learning Architect schemas and learner state directories."""

from __future__ import annotations

import argparse
from collections import deque
from datetime import date, datetime, timedelta
from pathlib import Path
import re
import sys
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker
from jsonschema.exceptions import FormatError, SchemaError
from referencing import Registry, Resource
import yaml


SCHEMA_NAMES = (
    "common",
    "system-state",
    "learner-profile",
    "target-outcome",
    "competency-model",
    "curriculum-graph",
    "learning-roadmap",
    "weekly-plan",
    "project",
    "assessment",
    "evidence",
    "optimization-state",
    "domain-pack",
)

REQUIRED_PROJECT_ARCHETYPES = {
    "focused-tool",
    "knowledge-application",
    "workflow",
    "enterprise-scenario",
    "portfolio-case",
    "real-external-delivery",
}
REQUIRED_ASSESSMENT_CHECKS = {
    "independent-completion",
    "explain-trade-offs",
    "modify-requirements",
    "debug",
    "deploy-deliver",
    "teach-review",
}
COURSE_PURCHASE_PATTERNS = (
    r"\bpaid\s+course\b",
    r"\b(?:buy|purchase|enroll(?:ment)?(?:\s+in)?)\b.{0,60}\bcourse\b",
    r"\bcourse\b.{0,30}\b(?:purchase|enrollment)\b",
    r"付费\s*课程",
    r"购买[^。！？.!?\n]{0,60}课程",
    r"报名[^。！？.!?\n]{0,60}课程",
)
CANONICAL_STAGES = (
    "discovery",
    "goal-analysis",
    "gap-analysis",
    "competency-design",
    "curriculum-design",
    "project-design",
    "roadmap",
    "weekly-planner",
    "assessment",
    "outcome-preparation",
    "continuous-optimization",
)
SINGLETON_ARTIFACTS = {
    "system-state.yaml": "system-state",
    "learner-profile.yaml": "learner-profile",
    "target-outcome.yaml": "target-outcome",
    "competency-model.yaml": "competency-model",
    "curriculum-graph.yaml": "curriculum-graph",
    "roadmap.yaml": "learning-roadmap",
    "learning-roadmap.yaml": "learning-roadmap",
    "optimization-log.yaml": "optimization-state",
    "assessment.yaml": "assessment",
    "evidence.yaml": "evidence",
    "weekly-plan.yaml": "weekly-plan",
    "project.yaml": "project",
}
SINGLETON_ARTIFACT_TYPES = {
    "system-state",
    "learner-profile",
    "target-outcome",
    "competency-model",
    "curriculum-graph",
    "learning-roadmap",
    "optimization-state",
}
DIRECTORY_ARTIFACTS = {
    "weekly-plans": "weekly-plan",
    "projects": "project",
    "assessments": "assessment",
    "portfolio": "evidence",
    "evidence": "evidence",
}
LEARNER_FORMAT_CHECKER = FormatChecker()


@LEARNER_FORMAT_CHECKER.checks("date-time")
def _is_iso_datetime(value: object) -> bool:
    if not isinstance(value, str):
        return True
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    return parsed.tzinfo is not None


def _load_yaml(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as stream:
        return yaml.safe_load(stream)


def _iter_strings(value: Any):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for item in value.values():
            yield from _iter_strings(item)
    elif isinstance(value, list):
        for item in value:
            yield from _iter_strings(item)


def _iter_string_paths(value: Any, path: tuple[str, ...] = ()):
    if isinstance(value, str):
        yield path, value
    elif isinstance(value, dict):
        for key, item in value.items():
            yield from _iter_string_paths(item, path + (str(key),))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            yield from _iter_string_paths(item, path + (str(index),))


def _artifact_schema_name(learner_dir: Path, path: Path) -> str | None:
    relative = path.relative_to(learner_dir)
    parts = list(relative.parts)
    while parts and parts[0] in {"history", "versions", "version-history"}:
        parts.pop(0)
    if not parts:
        return None
    if len(parts) == 1:
        return SINGLETON_ARTIFACTS.get(parts[0])
    for part in parts[:-1]:
        if part in DIRECTORY_ARTIFACTS:
            return DIRECTORY_ARTIFACTS[part]
    return SINGLETON_ARTIFACTS.get(parts[-1])


def _load_schemas(skill_root: Path) -> tuple[dict[str, dict[str, Any]], Registry]:
    schema_dir = skill_root / "assets" / "schemas"
    schemas: dict[str, dict[str, Any]] = {}
    resources = []
    for name in SCHEMA_NAMES:
        path = schema_dir / f"{name}.schema.yaml"
        schema = _load_yaml(path)
        uri = path.resolve().as_uri()
        schema["$id"] = uri
        schemas[name] = schema
        resources.append((uri, Resource.from_contents(schema)))
    return schemas, Registry().with_resources(resources)


def validate_skill_assets(skill_root: Path) -> list[str]:
    errors: list[str] = []
    schema_dir = skill_root / "assets" / "schemas"
    for name in SCHEMA_NAMES:
        path = schema_dir / f"{name}.schema.yaml"
        if not path.is_file():
            errors.append(f"Missing schema: {path}")
            continue
        try:
            schema = _load_yaml(path)
            if not isinstance(schema, dict):
                errors.append(f"Schema is not an object: {path}")
                continue
            Draft202012Validator.check_schema(schema)
        except (OSError, yaml.YAMLError, SchemaError) as exc:
            errors.append(f"Invalid schema {path}: {exc}")
    if errors:
        return errors

    try:
        schemas, registry = _load_schemas(skill_root)
    except (OSError, yaml.YAMLError) as exc:
        return [f"Unable to load schemas: {exc}"]

    pack_dir = skill_root / "assets" / "domain-packs"
    pack_paths = sorted(pack_dir.glob("*.yaml")) if pack_dir.is_dir() else []
    if not pack_paths:
        return [f"Missing Domain Pack: {pack_dir}"]

    for path in pack_paths:
        try:
            pack = _load_yaml(path)
        except (OSError, yaml.YAMLError) as exc:
            errors.append(f"Invalid Domain Pack {path}: {exc}")
            continue
        if not isinstance(pack, dict):
            errors.append(f"Domain Pack is not an object: {path}")
            continue
        validator = Draft202012Validator(
            schemas["domain-pack"],
            registry=registry,
            format_checker=FormatChecker(),
        )
        issues = sorted(validator.iter_errors(pack), key=lambda item: list(item.path))
        for issue in issues:
            location = ".".join(str(part) for part in issue.path) or "<root>"
            errors.append(f"Domain Pack {path.name}:{location}: {issue.message}")
        if not issues:
            errors.extend(_validate_domain_pack_semantics(path.name, pack))
    return errors


def _validate_domain_pack_semantics(
    pack_name: str, pack: dict[str, Any]
) -> list[str]:
    errors: list[str] = []
    target_outcome_ids = [
        outcome["id"] for outcome in pack.get("target_outcomes", [])
    ]
    if len(target_outcome_ids) != len(set(target_outcome_ids)):
        errors.append(f"Domain Pack {pack_name}: duplicate target outcome IDs")
    competencies = pack["competencies"]
    competency_ids = [competency["id"] for competency in competencies]
    competency_id_set = set(competency_ids)
    if len(competency_ids) != len(competency_id_set):
        errors.append(f"Domain Pack {pack_name}: duplicate competency IDs")

    dependencies = pack["dependencies"]
    unknown_endpoints = sorted(
        {
            endpoint
            for dependency in dependencies
            for endpoint in (dependency["from"], dependency["to"])
            if endpoint not in competency_id_set
        }
    )
    if unknown_endpoints:
        errors.append(
            f"Domain Pack {pack_name}: unknown dependency endpoints: "
            f"{', '.join(unknown_endpoints)}"
        )
    if _has_dependency_cycle(dependencies):
        errors.append(f"Domain Pack dependency cycle detected: {pack_name}")

    archetypes = pack["project_archetypes"]
    archetype_id_list = [archetype["id"] for archetype in archetypes]
    archetype_ids = set(archetype_id_list)
    if len(archetype_id_list) != len(archetype_ids):
        errors.append(f"Domain Pack {pack_name}: duplicate project archetype IDs")
    if archetype_ids != REQUIRED_PROJECT_ARCHETYPES:
        errors.append(
            f"Domain Pack {pack_name}: project archetypes must be exactly "
            f"{sorted(REQUIRED_PROJECT_ARCHETYPES)}"
        )
    covered_ids = {
        competency_id
        for archetype in archetypes
        for competency_id in archetype["competency_ids"]
    }
    if covered_ids != competency_id_set:
        errors.append(
            f"Domain Pack {pack_name}: project competency coverage mismatch"
        )
    for archetype in archetypes:
        rubric_weight = sum(
            dimension["weight"] for dimension in archetype["rubric"].values()
        )
        if abs(rubric_weight - 100) > 1e-9:
            errors.append(
                f"Domain Pack {pack_name}: project {archetype['id']} rubric "
                f"weights must total 100"
            )
        if not any(
            dimension.get("critical") is True
            for dimension in archetype["rubric"].values()
        ):
            errors.append(
                f"Domain Pack {pack_name}: project {archetype['id']} rubric "
                "requires at least one critical dimension"
            )

    pattern_ids = [pattern["id"] for pattern in pack["assessment_patterns"]]
    if len(pattern_ids) != len(set(pattern_ids)):
        errors.append(f"Domain Pack {pack_name}: duplicate assessment pattern IDs")
    assessment_checks = {
        check
        for pattern in pack["assessment_patterns"]
        for check in pattern["capability_checks"]
    }
    if assessment_checks != REQUIRED_ASSESSMENT_CHECKS:
        errors.append(
            f"Domain Pack {pack_name}: assessment capability coverage mismatch"
        )

    forbidden_urls = [
        value
        for path, value in _iter_string_paths(pack)
        if path[-1:] != ("source_url",)
        and re.search(r"https?://", value, flags=re.IGNORECASE)
    ]
    if forbidden_urls:
        errors.append(
            f"Domain Pack {pack_name}: HTTP/HTTPS URL is allowed only in source_url"
        )
    pack_strings = list(_iter_strings(pack))
    if any(
        re.search(pattern, value, flags=re.IGNORECASE)
        for value in pack_strings
        for pattern in COURSE_PURCHASE_PATTERNS
    ):
        errors.append(
            f"Domain Pack {pack_name}: paid course purchase or enrollment "
            "recommendation is forbidden"
        )

    try:
        reviewed = date.fromisoformat(pack["last_reviewed_at"])
        interval = int(pack["review_interval_days"])
        if date.today() > reviewed + timedelta(days=interval):
            errors.append(
                f"Domain Pack {pack_name}: stale review; last_reviewed_at plus "
                "review_interval_days is in the past"
            )
    except (KeyError, TypeError, ValueError):
        errors.append(f"Domain Pack {pack_name}: invalid review governance")

    assumptions = pack.get("market_assumptions", [])
    assumption_ids = [assumption.get("id") for assumption in assumptions]
    if len(assumption_ids) != len(set(assumption_ids)):
        errors.append(f"Domain Pack {pack_name}: duplicate market assumption IDs")
    for assumption in assumptions:
        assumption_id = assumption.get("id", "<unknown>")
        if not assumption.get("source_name") or not assumption.get("as_of"):
            errors.append(
                f"Domain Pack {pack_name}: market assumption {assumption_id} "
                "requires source and date"
            )
            continue
        try:
            as_of = date.fromisoformat(assumption["as_of"])
            next_review = date.fromisoformat(assumption["next_review_at"])
            if next_review < as_of:
                errors.append(
                    f"Domain Pack {pack_name}: market assumption {assumption_id} "
                    "next_review_at precedes as_of"
                )
            if next_review < date.today():
                errors.append(
                    f"Domain Pack {pack_name}: market assumption {assumption_id} "
                    "review is expired"
                )
        except (TypeError, ValueError):
            errors.append(
                f"Domain Pack {pack_name}: market assumption {assumption_id} "
                "has invalid as_of or next_review_at date"
            )

    migration_map = pack.get("extensions", {}).get("migration_map", {})
    if not isinstance(migration_map, dict):
        errors.append(f"Domain Pack {pack_name}: migration_map must be an object")
    else:
        for old_id, migration in migration_map.items():
            documented_retirement = False
            if isinstance(migration, dict):
                destination = migration.get("to")
                documented_retirement = (
                    destination == "retired"
                    and isinstance(migration.get("reason"), str)
                    and bool(migration["reason"].strip())
                )
                new_ids = destination
            else:
                new_ids = migration
            targets = new_ids if isinstance(new_ids, list) else [new_ids]
            if not old_id or not targets or any(
                not isinstance(target, str)
                or (
                    target not in competency_id_set
                    and not (target == "retired" and documented_retirement)
                )
                for target in targets
            ):
                errors.append(
                    f"Domain Pack {pack_name}: migration for {old_id!r} "
                    "must target installed competency IDs"
                )
    return errors


def _has_dependency_cycle(dependencies: list[dict[str, str]]) -> bool:
    graph: dict[str, list[str]] = {}
    indegree: dict[str, int] = {}
    for edge in dependencies:
        graph.setdefault(edge["from"], []).append(edge["to"])
        graph.setdefault(edge["to"], [])
        indegree.setdefault(edge["from"], 0)
        indegree[edge["to"]] = indegree.get(edge["to"], 0) + 1

    ready = deque(node for node in graph if indegree.get(node, 0) == 0)
    visited = 0
    while ready:
        node = ready.popleft()
        visited += 1
        for neighbor in graph[node]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                ready.append(neighbor)

    return visited != len(graph)


def validate_learner_system(skill_root: Path, learner_dir: Path) -> list[str]:
    errors = validate_skill_assets(skill_root)
    if errors:
        return errors

    if not learner_dir.exists():
        return [f"Learner directory does not exist: {learner_dir}"]
    if not learner_dir.is_dir():
        return [f"Learner path is not a directory: {learner_dir}"]
    learner_yaml_paths = sorted(learner_dir.rglob("*.yaml"))
    if not learner_yaml_paths:
        return [f"Learner directory contains no YAML artifacts: {learner_dir}"]

    try:
        schemas, registry = _load_schemas(skill_root)
    except (OSError, yaml.YAMLError) as exc:
        return [f"Unable to load schemas: {exc}"]

    artifacts: dict[str, list[tuple[Path, dict[str, Any]]]] = {}
    artifact_by_key: dict[str, tuple[str, Path, dict[str, Any]]] = {}
    seen_artifact_versions: dict[tuple[str, str, int], Path] = {}
    artifact_identity_groups: dict[
        tuple[str, str], list[tuple[Path, dict[str, Any]]]
    ] = {}
    for path in learner_yaml_paths:
        name = _artifact_schema_name(learner_dir, path)
        if name is None or name == "common":
            errors.append(f"Unknown learner artifact path: {path.relative_to(learner_dir)}")
            continue
        try:
            document = _load_yaml(path)
        except (OSError, yaml.YAMLError) as exc:
            errors.append(f"Invalid learner YAML {path.relative_to(learner_dir)}: {exc}")
            continue
        if not isinstance(document, dict):
            errors.append(f"Learner document is not an object: {path}")
            continue
        validator = Draft202012Validator(
            schemas[name], registry=registry, format_checker=LEARNER_FORMAT_CHECKER
        )
        issues = sorted(
            validator.iter_errors(document), key=lambda item: list(item.path)
        )
        checker = LEARNER_FORMAT_CHECKER
        format_invalid = False
        for timestamp_field in ("created_at", "updated_at"):
            if timestamp_field in document:
                try:
                    checker.check(document[timestamp_field], "date-time")
                except FormatError as exc:
                    errors.append(
                        f"{path.relative_to(learner_dir)}:{timestamp_field}: {exc}"
                    )
                    format_invalid = True
        for date_field in ("deadline",):
            if date_field in document:
                try:
                    checker.check(document[date_field], "date")
                except FormatError as exc:
                    errors.append(
                        f"{path.relative_to(learner_dir)}:{date_field}: {exc}"
                    )
                    format_invalid = True
        for issue in issues:
            location = ".".join(str(part) for part in issue.path) or "<root>"
            errors.append(
                f"{path.relative_to(learner_dir)}:{location}: {issue.message}"
            )
            if name == "project" and list(issue.path)[:1] == ["rubric"]:
                errors.append(
                    f"Project rubric schema invalid: {path.relative_to(learner_dir)}"
                )
        if not issues and not format_invalid:
            artifacts.setdefault(name, []).append((path, document))
            relative_key = path.relative_to(learner_dir).with_suffix("").as_posix()
            artifact_by_key[relative_key] = (name, path, document)
            if path.parent == learner_dir:
                artifact_by_key[path.stem] = (name, path, document)
            document_id = document["id"]
            version_key = (name, document_id, document["content_version"])
            previous = seen_artifact_versions.get(version_key)
            if previous is not None:
                errors.append(
                    f"Duplicate artifact version {name}/{document_id}@"
                    f"{document['content_version']}: "
                    f"{previous.relative_to(learner_dir)} and {path.relative_to(learner_dir)}"
                )
            else:
                seen_artifact_versions[version_key] = path
            artifact_identity_groups.setdefault((name, document_id), []).append(
                (path, document)
            )

    current_artifacts: dict[str, list[tuple[Path, dict[str, Any]]]] = {}
    for (name, document_id), records in artifact_identity_groups.items():
        active_record_pairs = [
            (path, document)
            for path, document in records
            if document.get("status") == "active"
        ]
        active_records = [path for path, _ in active_record_pairs]
        if len(active_records) > 1:
            errors.append(
                f"Multiple active versions for {name}/{document_id}: "
                + ", ".join(
                    str(path.relative_to(learner_dir)) for path in active_records
                )
            )
        elif len(active_record_pairs) == 1:
            current_artifacts.setdefault(name, []).append(active_record_pairs[0])

    for name in SINGLETON_ARTIFACT_TYPES:
        active_records = current_artifacts.get(name, [])
        if len(active_records) > 1:
            errors.append(
                f"Multiple active singleton artifacts for {name}: "
                + ", ".join(
                    f"{document['id']} ({path.relative_to(learner_dir)})"
                    for path, document in active_records
                )
            )

    active_system_states = current_artifacts.get("system-state", [])
    root_system_state = learner_dir / "system-state.yaml"
    if (
        len(active_system_states) != 1
        or active_system_states[0][0] != root_system_state
    ):
        errors.append(
            "Learner system requires exactly one active root system-state.yaml"
        )

    def first(name: str) -> dict[str, Any] | None:
        records = current_artifacts.get(name, [])
        return records[0][1] if len(records) == 1 else None

    curriculum = first("curriculum-graph")
    if curriculum and _has_dependency_cycle(curriculum.get("dependencies", [])):
        errors.append("Curriculum dependency cycle detected")
    if curriculum:
        unit_ids = [unit["id"] for unit in curriculum.get("units", [])]
        if len(unit_ids) != len(set(unit_ids)):
            errors.append("Duplicate curriculum unit IDs")
        unknown = sorted(
            {
                endpoint
                for edge in curriculum.get("dependencies", [])
                for endpoint in (edge["from"], edge["to"])
                if endpoint not in set(unit_ids)
            }
        )
        if unknown:
            errors.append(f"Unknown curriculum dependency endpoints: {', '.join(unknown)}")

    roadmap = first("learning-roadmap")
    if roadmap:
        phases = roadmap.get("phases", [])
        phase_cost_sum = sum(phase.get("estimated_cost", 0) for phase in phases)
        total_estimated_cost = roadmap.get("total_estimated_cost", 0)
        if abs(phase_cost_sum - total_estimated_cost) > 1e-9:
            errors.append(
                "Learning roadmap total_estimated_cost must equal phase cost sum"
            )
        budget_amount = roadmap.get("budget", {}).get("amount", 0)
        if total_estimated_cost > budget_amount:
            errors.append("Learning roadmap estimated cost exceeds budget")
        roadmap_currency = roadmap.get("currency")
        mismatched_phases = [
            phase.get("id", "<unknown>")
            for phase in phases
            if phase.get("currency") != roadmap_currency
        ]
        if mismatched_phases:
            errors.append(
                "Learning roadmap phase currency mismatch: "
                + ", ".join(mismatched_phases)
            )

    competency_model = first("competency-model")
    competency_id_list = [
        competency["id"]
        for competency in (competency_model or {}).get("competencies", [])
    ]
    competency_ids = set(competency_id_list)
    if len(competency_id_list) != len(competency_ids):
        errors.append("Duplicate competency IDs in competency model")
    installed_domain_pack_ids = {
        pack.get("id")
        for path in (skill_root / "assets" / "domain-packs").glob("*.yaml")
        if isinstance((pack := _load_yaml(path)), dict)
    }
    if competency_model and competency_model.get("domain_pack_id") not in installed_domain_pack_ids:
        errors.append(
            "Competency model references uninstalled Domain Pack: "
            f"{competency_model.get('domain_pack_id')}"
        )

    evidence_records: dict[str, dict[str, Any]] = {}
    for _, evidence in current_artifacts.get("evidence", []):
        evidence_records[evidence["id"]] = evidence
        for competency_id in evidence.get("competency_ids", []):
            if competency_id not in competency_ids:
                errors.append(
                    f"Evidence references unknown competency: {competency_id}"
                )

    learner_profile = first("learner-profile")
    if learner_profile:
        material_sections = [
            learner_profile.get(name, {})
            for name in (
                "personal", "experience", "learning_preferences", "motivation", "constraints"
            )
        ]
        material_items = [
            item for section in material_sections for item in section.values()
        ]
        material_items.extend(
            item
            for items in learner_profile.get("swot", {}).values()
            for item in items
        )
        material_items.extend(learner_profile.get("unknowns", []))
        for item in material_items:
            for evidence_id in item.get("evidence_ids", []):
                if evidence_id not in evidence_records:
                    errors.append(
                        f"Learner profile references unknown Evidence record: {evidence_id}"
                    )

    for project_path, project in current_artifacts.get("project", []):
        for competency_id in project.get("competency_ids", []):
            if competency_id not in competency_ids:
                errors.append(
                    f"Project references unknown competency: {competency_id} "
                    f"({project_path.relative_to(learner_dir)})"
                )
        rubric = project.get("rubric", {})
        rubric_weight = sum(
            dimension.get("weight", 0) for dimension in rubric.values()
        )
        if abs(rubric_weight - 100) > 1e-9:
            errors.append(
                f"Project rubric weights must total 100: "
                f"{project_path.relative_to(learner_dir)}"
            )
        if rubric and not any(
            dimension.get("critical") is True for dimension in rubric.values()
        ):
            errors.append(
                f"Project rubric requires at least one critical dimension: "
                f"{project_path.relative_to(learner_dir)}"
            )

    project_ids = {
        project["id"] for _, project in current_artifacts.get("project", [])
    }
    if roadmap:
        for phase in roadmap.get("phases", []):
            for project_id in phase.get("project_ids", []):
                if project_id not in project_ids:
                    errors.append(f"Roadmap references unknown project: {project_id}")

    for weekly_path, weekly in current_artifacts.get("weekly-plan", []):
        task_ids = {task["id"] for task in weekly.get("tasks", [])}
        for task in weekly.get("tasks", []):
            dependency = task.get("dependency")
            if dependency not in {None, "none"} and dependency not in task_ids:
                errors.append(
                    f"Weekly task references unknown task: {dependency} "
                    f"({weekly_path.relative_to(learner_dir)})"
                )
            for competency_id in task.get("competency_ids", []):
                if competency_id not in competency_ids:
                    errors.append(f"Weekly task references unknown competency: {competency_id}")
        for retrieval in weekly.get("retrieval_practice", []):
            competency_id = retrieval.get("competency_id")
            if competency_id not in competency_ids:
                errors.append(
                    f"Weekly retrieval references unknown competency: {competency_id}"
                )
        project_id = weekly.get("project_work", {}).get("project_id")
        if project_id and project_id not in project_ids:
            errors.append(f"Weekly plan references unknown project: {project_id}")
        planned_hours = (
            sum(item.get("estimated_hours", 0) for item in weekly.get("tasks", []))
            + sum(item.get("estimated_hours", 0) for item in weekly.get("retrieval_practice", []))
            + weekly.get("project_work", {}).get("estimated_hours", 0)
            + weekly.get("review", {}).get("estimated_hours", 0)
        )
        buffer_ratio = weekly.get("extensions", {}).get("buffer_ratio", 0)
        usable_capacity = weekly.get("capacity_hours", 0) * (1 - buffer_ratio)
        if planned_hours > usable_capacity + 1e-9:
            errors.append(
                f"Weekly planned load {planned_hours:g} exceeds usable capacity "
                f"{usable_capacity:g}: {weekly_path.relative_to(learner_dir)}"
            )
        declared_planned = weekly.get("extensions", {}).get("planned_load_hours")
        declared_usable = weekly.get("extensions", {}).get("usable_capacity_hours")
        if declared_planned is not None and abs(declared_planned - planned_hours) > 1e-9:
            errors.append("Weekly planned_load_hours does not equal typed task arithmetic")
        if declared_usable is not None and abs(declared_usable - usable_capacity) > 1e-9:
            errors.append("Weekly usable_capacity_hours does not equal capacity arithmetic")

    for _, assessment in current_artifacts.get("assessment", []):
        for evidence_id in assessment.get("evidence_ids", []):
            if evidence_id not in evidence_records:
                errors.append(
                    "Assessment references unknown Evidence record: "
                    f"{evidence_id}"
                )
        for check in assessment.get("behavior_checks", []):
            if check.get("applicability") != "applicable":
                continue
            behavior = check.get("behavior", "<unknown>")
            expected_state = check.get("state", "<unknown>")
            resolved_records = []
            for evidence_id in check.get("evidence_ids", []):
                record = evidence_records.get(evidence_id)
                if record is None:
                    errors.append(
                        f"Assessment behavior {behavior} references unknown "
                        f"Evidence record: {evidence_id}"
                    )
                else:
                    resolved_records.append(record)
            has_matching_observation = any(
                observation.get("behavior") == behavior
                and observation.get("state") == expected_state
                for record in resolved_records
                for observation in record.get("observed_behaviors", [])
            )
            if resolved_records and not has_matching_observation:
                errors.append(
                    "Assessment evidence does not contain matching observed "
                    f"behavior state: {behavior}={expected_state}"
                )
            if expected_state == "fail" and not resolved_records:
                errors.append(
                    f"Assessment behavior {behavior} requires resolved failure evidence"
                )
        for result in assessment.get("competency_results", []):
            if result.get("competency_id") not in competency_ids:
                errors.append(
                    "Assessment references unknown competency: "
                    f"{result.get('competency_id')}"
                )
        applicable_problems = {
            check["behavior"]
            for check in assessment.get("behavior_checks", [])
            if check.get("applicability") == "applicable"
            and (check.get("state") == "fail" or not check.get("evidence_ids"))
        }
        gate_missing = set(assessment.get("gate", {}).get("missing", []))
        if not assessment.get("gate", {}).get("passed") and gate_missing != applicable_problems:
            errors.append(
                "Assessment gate.missing must exactly match failed or missing "
                "applicable behaviors"
            )

    system_state = first("system-state")
    if system_state:
        stage_states = system_state.get("stage_states", {})
        current_stage = system_state.get("current_stage")
        current_index = CANONICAL_STAGES.index(current_stage)
        completed_states = {"validated", "not_applicable", "superseded", "archived"}
        illegal = []
        for index, stage in enumerate(CANONICAL_STAGES):
            stage_state = stage_states.get(stage, {}).get("state")
            if index < current_index and stage_state not in completed_states:
                illegal.append(f"{stage}={stage_state}")
            if index > current_index and stage_state not in {"not_started"}:
                illegal.append(f"{stage}={stage_state}")
        current_value = stage_states.get(current_stage, {}).get("state")
        if current_value not in {"collecting", "draft", "validated", "active", "needs_input", "blocked"}:
            illegal.append(f"current {current_stage}={current_value}")
        if illegal:
            errors.append("Illegal stage progression: " + ", ".join(illegal))

        stage_artifact_requirements = {
            "discovery": ("learner-profile",),
            "goal-analysis": ("target-outcome",),
            "competency-design": ("competency-model",),
            "curriculum-design": ("curriculum-graph",),
            "project-design": ("project",),
            "roadmap": ("learning-roadmap",),
            "weekly-planner": ("weekly-plan",),
            "assessment": ("assessment",),
            "outcome-preparation": ("evidence",),
            "continuous-optimization": ("optimization-state",),
        }
        for stage, required_artifact_types in stage_artifact_requirements.items():
            stage_state = stage_states.get(stage, {}).get("state")
            if stage_state not in {"validated", "active"}:
                continue
            for artifact_type in required_artifact_types:
                if not current_artifacts.get(artifact_type):
                    errors.append(
                        f"Stage {stage} is {stage_state} but requires active "
                        f"{artifact_type}"
                    )

        singleton_coverage: dict[tuple[str, str, int], int] = {}
        for artifact_name, active_version in system_state.get("active_versions", {}).items():
            resolved = artifact_by_key.get(artifact_name)
            if resolved is None:
                errors.append(
                    f"Active version references missing learner artifact: {artifact_name}"
                )
                continue
            schema_name, _, artifact = resolved
            expected_schema = SINGLETON_ARTIFACTS.get(f"{artifact_name}.yaml")
            if expected_schema and schema_name != expected_schema:
                errors.append(f"Active version has wrong artifact type: {artifact_name}")
            matching_active = [
                candidate
                for _, candidate in artifact_identity_groups.get(
                    (schema_name, artifact.get("id")), []
                )
                if candidate.get("content_version") == active_version
                and candidate.get("status") == "active"
            ]
            if len(matching_active) != 1:
                errors.append(
                    f"Active version mismatch for {artifact_name}: "
                    f"no unique active content_version {active_version!r}"
                )
                active_artifact = artifact
            else:
                active_artifact = matching_active[0]
                if schema_name in SINGLETON_ARTIFACT_TYPES:
                    coverage_key = (
                        schema_name,
                        active_artifact["id"],
                        active_artifact["content_version"],
                    )
                    singleton_coverage[coverage_key] = (
                        singleton_coverage.get(coverage_key, 0) + 1
                    )
            artifact_id = str(active_artifact.get("id", ""))
            expected_id = Path(artifact_name).name
            history_or_version_key = artifact_name.split("/", 1)[0] in {
                "history", "versions", "version-history"
            }
            id_matches = (
                artifact_id.startswith(expected_id)
                if history_or_version_key or "/" not in artifact_name
                else artifact_id == expected_id
            )
            if not id_matches:
                errors.append(f"Active version has wrong artifact ID/type: {artifact_name}")

        for schema_name in SINGLETON_ARTIFACT_TYPES - {"system-state"}:
            for _, artifact in current_artifacts.get(schema_name, []):
                coverage_key = (
                    schema_name,
                    artifact["id"],
                    artifact["content_version"],
                )
                if singleton_coverage.get(coverage_key, 0) != 1:
                    errors.append(
                        "active_versions must uniquely cover active singleton "
                        f"{schema_name}/{artifact['id']}@{artifact['content_version']}"
                    )

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skill-root", type=Path, required=True)
    parser.add_argument("--learner-dir", type=Path, required=True)
    args = parser.parse_args()

    errors = validate_learner_system(args.skill_root, args.learner_dir)
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print("VALID")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
