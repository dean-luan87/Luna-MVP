#!/usr/bin/env python3
"""Final phase verifier for Cognitive Memory & Experience controlled implementation v1."""

from __future__ import annotations

import ast
import json
from pathlib import Path
from typing import Any, Iterable, List


def _resolve_repo_root() -> Path:
    current = Path(__file__).resolve()
    for candidate in current.parents:
        sentinel = (
            candidate / "capabilities/midplatform/core/cognitive_memory_experience"
        )
        if sentinel.is_dir():
            return candidate
    cwd = Path.cwd().resolve()
    if (cwd / "capabilities/midplatform/core/cognitive_memory_experience").is_dir():
        return cwd
    return Path(__file__).resolve().parents[4]


REPO_ROOT = _resolve_repo_root()
PHASE_DIR = (
    REPO_ROOT
    / "docs/architecture/luna_cognitive_memory_experience_controlled_implementation_v1"
)
PLANNING_DIR = (
    REPO_ROOT
    / "docs/architecture/luna_cognitive_memory_and_experience_governance_planning_v1"
)
EVAL_OUT_DIR = (
    REPO_ROOT / "_eval_out/cognitive_memory_experience_controlled_implementation_v1"
)

CODE_FILES = [
    "capabilities/midplatform/core/cognitive_memory_experience/__init__.py",
    "capabilities/midplatform/core/cognitive_memory_experience/cognitive_memory_experience_registry_v1.py",
    "capabilities/midplatform/core/cognitive_memory_experience/cognitive_memory_experience_error_types_v1.py",
    "capabilities/midplatform/core/cognitive_memory_experience/experience_candidate_types_v1.py",
    "capabilities/midplatform/core/cognitive_memory_experience/memory_candidate_types_v1.py",
    "capabilities/midplatform/core/cognitive_memory_experience/memory_admission_types_v1.py",
    "capabilities/midplatform/core/cognitive_memory_experience/memory_lifecycle_types_v1.py",
    "capabilities/midplatform/core/cognitive_memory_experience/memory_influence_types_v1.py",
    "capabilities/midplatform/core/cognitive_memory_experience/memory_trace_types_v1.py",
    "capabilities/midplatform/core/cognitive_memory_experience/memory_io_types_v1.py",
    "capabilities/midplatform/core/cognitive_memory_experience/cognitive_memory_experience_protocol_v1.py",
    "capabilities/midplatform/core/cognitive_memory_experience/cognitive_memory_experience_ownership_guard_v1.py",
    "capabilities/midplatform/core/cognitive_memory_experience/cognitive_memory_experience_static_validators_v1.py",
    "capabilities/midplatform/core/cognitive_memory_experience/cognitive_memory_experience_engine_v1.py",
    "capabilities/midplatform/core/cognitive_memory_experience/cognitive_memory_experience_fixture_v1.py",
    "capabilities/midplatform/core/cognitive_memory_experience/run_cognitive_memory_experience_controlled_implementation_v1.py",
]
DOC_FILES = [
    "docs/architecture/luna_cognitive_memory_experience_controlled_implementation_v1/cognitive_memory_experience_controlled_implementation_overview_v1.md",
    "docs/architecture/luna_cognitive_memory_experience_controlled_implementation_v1/cognitive_memory_experience_controlled_execution_contract_v1.json",
    "docs/architecture/luna_cognitive_memory_experience_controlled_implementation_v1/cognitive_memory_experience_negative_guards_v1.json",
    "docs/architecture/luna_cognitive_memory_experience_controlled_implementation_v1/cognitive_memory_experience_planning_to_code_mapping_v1.json",
    "docs/architecture/luna_cognitive_memory_experience_controlled_implementation_v1/cognitive_memory_experience_controlled_change_manifest_v1.json",
    "docs/architecture/luna_cognitive_memory_experience_controlled_implementation_v1/cognitive_memory_experience_implementation_summary_v1.md",
    "docs/architecture/luna_cognitive_memory_experience_controlled_implementation_v1/phase_contract.json",
    "docs/architecture/luna_cognitive_memory_experience_controlled_implementation_v1/verify_cognitive_memory_experience_controlled_implementation_v1.py",
]
PLANNING_REQUIRED = [
    "cognitive_memory_experience_owner_boundary_v1.json",
    "experience_candidate_schema_v1.json",
    "memory_candidate_schema_v1.json",
    "memory_type_taxonomy_v1.json",
    "memory_admission_state_model_v1.json",
    "cognitive_memory_experience_minimum_scenario_suite_v1.json",
    "cognitive_memory_experience_negative_guards_v1.json",
]


def _load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _contains_all(items: Iterable[str], required: Iterable[str]) -> bool:
    item_set = set(items)
    return all(r in item_set for r in required)


def _expect(name: str, cond: bool, failed: List[str]) -> None:
    if not cond:
        failed.append(name)


def main() -> int:
    failed: List[str] = []
    for rel in CODE_FILES + DOC_FILES:
        _expect(f"exists:{rel}", (REPO_ROOT / rel).exists(), failed)
        if rel.endswith(".json"):
            try:
                _load_json(REPO_ROOT / rel)
            except Exception:
                failed.append(f"json_parse:{rel}")
        if rel.endswith(".py"):
            try:
                ast.parse((REPO_ROOT / rel).read_text(encoding="utf-8"))
            except Exception:
                failed.append(f"ast_parse:{rel}")

    for rel in PLANNING_REQUIRED:
        _expect(f"planning_exists:{rel}", (PLANNING_DIR / rel).exists(), failed)

    phase = _load_json(PHASE_DIR / "phase_contract.json")
    _expect("code_file_set", phase.get("required_code_files") == CODE_FILES, failed)
    _expect("doc_file_set", phase.get("required_doc_files") == DOC_FILES, failed)

    owner = _load_json(
        PLANNING_DIR / "cognitive_memory_experience_owner_boundary_v1.json"
    )
    _expect(
        "canonical_owner",
        owner.get("canonical_owner_candidate")
        == "Cognitive Memory & Experience Governance",
        failed,
    )

    taxonomy = _load_json(PLANNING_DIR / "memory_type_taxonomy_v1.json")
    types = [item.get("type", "") for item in taxonomy.get("types", [])]
    _expect(
        "taxonomy_coverage",
        _contains_all(
            types,
            [
                "EPISODIC",
                "SEMANTIC",
                "RELATIONAL",
                "SELF_RELATED",
                "PREFERENCE",
                "PROCEDURAL_REFERENCE",
                "ENVIRONMENTAL_CONTEXT",
                "TASK_EXPERIENCE",
                "SOCIAL_EXPERIENCE",
                "EMOTIONAL_EXPERIENCE",
                "UNRESOLVED_EXPERIENCE",
            ],
        ),
        failed,
    )

    states = _load_json(PLANNING_DIR / "memory_admission_state_model_v1.json").get(
        "states", []
    )
    _expect(
        "admission_state_coverage",
        _contains_all(
            states,
            [
                "PROPOSED",
                "ELIGIBLE",
                "INSUFFICIENT_EVIDENCE",
                "CONTESTED",
                "NEEDS_CONFIRMATION",
                "TEMPORARY",
                "ADMITTED_CANDIDATE",
                "REJECTED",
                "SUPERSEDED",
                "REVISED",
                "REVOKED",
                "EXPIRED",
            ],
        ),
        failed,
    )

    result_path = EVAL_OUT_DIR / "cognitive_memory_experience_result_v1.json"
    cases_path = EVAL_OUT_DIR / "cognitive_memory_experience_case_results_v1.json"
    trace_path = EVAL_OUT_DIR / "cognitive_memory_experience_trace_v1.json"
    _expect("runner_result_exists", result_path.exists(), failed)
    _expect("runner_cases_exists", cases_path.exists(), failed)
    _expect("runner_trace_exists", trace_path.exists(), failed)

    if result_path.exists() and cases_path.exists() and trace_path.exists():
        result = _load_json(result_path)
        cases = _load_json(cases_path)
        trace = _load_json(trace_path)
        _expect("runner_scenario_count", result.get("scenario_count") == 28, failed)
        _expect(
            "runner_all_cases_passed", result.get("all_cases_passed") is True, failed
        )
        _expect(
            "runner_runtime_execution_false",
            result.get("runtime_execution") is False,
            failed,
        )
        _expect(
            "runner_database_write_false", result.get("database_write") is False, failed
        )
        _expect(
            "runner_vector_store_write_false",
            result.get("vector_store_write") is False,
            failed,
        )
        _expect(
            "runner_embedding_execution_false",
            result.get("embedding_execution") is False,
            failed,
        )
        _expect("runner_model_call_false", result.get("model_call") is False, failed)
        _expect(
            "runner_source_owner_mutation_false",
            result.get("source_owner_mutation") is False,
            failed,
        )
        _expect(
            "runner_learning_execution_false",
            result.get("learning_execution") is False,
            failed,
        )
        _expect(
            "runner_personality_mutation_false",
            result.get("personality_mutation") is False,
            failed,
        )
        _expect(
            "runner_synthetic_only_true", result.get("synthetic_only") is True, failed
        )
        _expect(
            "runner_candidate_only_true", result.get("candidate_only") is True, failed
        )
        _expect("runner_case_count", len(cases) == 28, failed)
        _expect("trace_case_count", len(trace.get("case_traces", [])) == 28, failed)
        case_ids = [item.get("case_id", "") for item in cases]
        _expect(
            "runner_case_ids",
            _contains_all(case_ids, [f"M{i:02d}" for i in range(1, 29)]),
            failed,
        )
        _expect(
            "case_results_all_pass",
            all(item.get("all_checks_passed") is True for item in cases),
            failed,
        )

    if failed:
        print(
            json.dumps(
                {
                    "CHECKS": {
                        "code_file_set": "pass"
                        if not any(
                            x == "code_file_set" or x.startswith("exists:capabilities")
                            for x in failed
                        )
                        else "fail",
                        "doc_file_set": "pass"
                        if not any(
                            x == "doc_file_set" or x.startswith("exists:docs")
                            for x in failed
                        )
                        else "fail",
                        "json_parse": "pass"
                        if not any(x.startswith("json_parse:") for x in failed)
                        else "fail",
                        "ast_parse": "pass"
                        if not any(x.startswith("ast_parse:") for x in failed)
                        else "fail",
                        "owner_and_boundary": "pass"
                        if not any("owner" in x or "guard" in x for x in failed)
                        else "fail",
                        "scenario_and_fixture": "pass"
                        if not any("scenario" in x or "case_" in x for x in failed)
                        else "fail",
                        "runner_artifacts": "pass"
                        if not any(
                            x.startswith("runner_") or x.startswith("trace_")
                            for x in failed
                        )
                        else "fail",
                    },
                    "FAILED_CHECKS": failed,
                    "PASSED_CHECK_COUNT": 0,
                    "FAILED_CHECK_COUNT": len(failed),
                    "BLOCKER_COUNT": len(failed),
                    "FINAL_DECISION": "BLOCKED",
                    "NEXT": "LUNA_COGNITIVE_MEMORY_EXPERIENCE_CONTROLLED_IMPLEMENTATION_REMEDIATION",
                },
                indent=2,
                ensure_ascii=False,
            )
        )
        return 1

    print(
        json.dumps(
            {
                "CHECKS": {
                    "code_file_set": "pass",
                    "doc_file_set": "pass",
                    "json_parse": "pass",
                    "ast_parse": "pass",
                    "owner_and_boundary": "pass",
                    "scenario_and_fixture": "pass",
                    "runner_artifacts": "pass",
                },
                "FAILED_CHECKS": [],
                "PASSED_CHECK_COUNT": 7,
                "FAILED_CHECK_COUNT": 0,
                "BLOCKER_COUNT": 0,
                "FINAL_DECISION": "PASS",
                "NEXT": "LUNA_COGNITIVE_MEMORY_EXPERIENCE_CONTROLLED_IMPLEMENTATION_GO",
            },
            indent=2,
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
