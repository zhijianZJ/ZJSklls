#!/usr/bin/env python3
"""Validate Learning Architect schemas and learner state directories."""

from __future__ import annotations

import argparse
from pathlib import Path
import re
import sys
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker
from jsonschema.exceptions import SchemaError
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
    archetype_ids = {archetype["id"] for archetype in archetypes}
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

    assessment_checks = {
        check
        for pattern in pack["assessment_patterns"]
        for check in pattern["capability_checks"]
    }
    if assessment_checks != REQUIRED_ASSESSMENT_CHECKS:
        errors.append(
            f"Domain Pack {pack_name}: assessment capability coverage mismatch"
        )

    pack_strings = list(_iter_strings(pack))
    if any(re.search(r"https?://", value, flags=re.IGNORECASE) for value in pack_strings):
        errors.append(
            f"Domain Pack {pack_name}: HTTP/HTTPS URL is forbidden"
        )
    if any(
        re.search(pattern, value, flags=re.IGNORECASE)
        for value in pack_strings
        for pattern in COURSE_PURCHASE_PATTERNS
    ):
        errors.append(
            f"Domain Pack {pack_name}: paid course purchase or enrollment "
            "recommendation is forbidden"
        )

    if pack.get("id") == "ai-agent-engineer":
        expected_metadata = {
            "version": "1.0.0",
            "last_reviewed_at": "2026-07-13",
            "review_interval_days": 90,
        }
        for field, expected in expected_metadata.items():
            if pack.get(field) != expected:
                errors.append(
                    f"Domain Pack {pack_name}: {field} must be {expected!r}"
                )
    return errors


def _has_dependency_cycle(dependencies: list[dict[str, str]]) -> bool:
    graph: dict[str, list[str]] = {}
    for edge in dependencies:
        graph.setdefault(edge["from"], []).append(edge["to"])
        graph.setdefault(edge["to"], [])

    state: dict[str, int] = {}

    def visit(node: str) -> bool:
        if state.get(node) == 1:
            return True
        if state.get(node) == 2:
            return False
        state[node] = 1
        if any(visit(neighbor) for neighbor in graph[node]):
            return True
        state[node] = 2
        return False

    return any(visit(node) for node in graph if state.get(node, 0) == 0)


def validate_learner_system(skill_root: Path, learner_dir: Path) -> list[str]:
    errors = validate_skill_assets(skill_root)
    if errors:
        return errors

    try:
        schemas, registry = _load_schemas(skill_root)
    except (OSError, yaml.YAMLError) as exc:
        return [f"Unable to load schemas: {exc}"]

    documents: dict[str, dict[str, Any]] = {}
    for path in sorted(learner_dir.glob("*.yaml")):
        name = path.stem
        if name not in schemas or name == "common":
            continue
        try:
            document = _load_yaml(path)
        except (OSError, yaml.YAMLError) as exc:
            errors.append(f"Invalid learner YAML {path}: {exc}")
            continue
        if not isinstance(document, dict):
            errors.append(f"Learner document is not an object: {path}")
            continue
        validator = Draft202012Validator(schemas[name], registry=registry)
        issues = sorted(
            validator.iter_errors(document), key=lambda item: list(item.path)
        )
        for issue in issues:
            location = ".".join(str(part) for part in issue.path) or "<root>"
            errors.append(f"{path.name}:{location}: {issue.message}")
        if not issues:
            documents[name] = document

    curriculum = documents.get("curriculum-graph")
    if curriculum and _has_dependency_cycle(curriculum.get("dependencies", [])):
        errors.append("Curriculum dependency cycle detected")

    competency_model = documents.get("competency-model")
    evidence = documents.get("evidence")
    if competency_model and evidence:
        competency_ids = {
            competency["id"] for competency in competency_model.get("competencies", [])
        }
        for competency_id in evidence.get("competency_ids", []):
            if competency_id not in competency_ids:
                errors.append(
                    f"Evidence references unknown competency: {competency_id}"
                )

    system_state = documents.get("system-state")
    if system_state:
        for artifact_name in system_state.get("active_versions", {}):
            if not (learner_dir / f"{artifact_name}.yaml").is_file():
                errors.append(
                    f"Active version references missing learner file: {artifact_name}.yaml"
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
