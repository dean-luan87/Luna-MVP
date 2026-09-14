#!/usr/bin/env python3
"""Final phase verifier for Cognitive Learning controlled implementation v1."""

from __future__ import annotations

import ast
import json
from pathlib import Path
from typing import Any, Iterable, List


def _resolve_repo_root() -> Path:
    current = Path(__file__).resolve()
    for candidate in current.parents:
        sentinel = candidate / "capabilities/midplatform/core/cognitive_learning"
        if sentinel.is_dir():
            return candidate
    cwd = Path.cwd().resolve()
    if (cwd / "capabilities/midplatform/core/cognitive_learning").is_dir():
        return cwd
    return Path(__file__).resolve().parents[4]


REPO_ROOT = _resolve_repo_root()
PHASE_DIR = (
    REPO_ROOT / "docs/architecture/luna_cognitive_learning_controlled_implementation_v1"
)
PLANNING_DIR = (
    REPO_ROOT / "docs/architecture/luna_cognitive_learning_governance_planning_v1"
)
EVAL_OUT_DIR = REPO_ROOT / "_eval_out/cognitive_learning_controlled_implementation_v1"

CODE_FILES = [
    "capabilities/midplatform/core/cognitive_learning/__init__.py",
    "capabilities/midplatform/core/cognitive_learning/cognitive_learning_registry_v1.py",
    "capabilities/midplatform/core/cognitive_learning/cognitive_learning_error_types_v1.py",
    "capabilities/midplatform/core/cognitive_learning/learning_evidence_types_v1.py",
    "capabilities/midplatform/core/cognitive_learning/learning_candidate_types_v1.py",
    "capabilities/midplatform/core/cognitive_learning/parameter_update_candidate_types_v1.py",
    "capabilities/midplatform/core/cognitive_learning/learning_admission_types_v1.py",
    "capabilities/midplatform/core/cognitive_learning/learning_generalization_types_v1.py",
    "capabilities/midplatform/core/cognitive_learning/learning_contradiction_types_v1.py",
    "capabilities/midplatform/core/cognitive_learning/learning_lifecycle_types_v1.py",
    "capabilities/midplatform/core/cognitive_learning/learning_influence_types_v1.py",
    "capabilities/midplatform/core/cognitive_learning/cognitive_learning_trace_types_v1.py",
    "capabilities/midplatform/core/cognitive_learning/cognitive_learning_io_types_v1.py",
    "capabilities/midplatform/core/cognitive_learning/cognitive_learning_protocol_v1.py",
    "capabilities/midplatform/core/cognitive_learning/cognitive_learning_ownership_guard_v1.py",
    "capabilities/midplatform/core/cognitive_learning/cognitive_learning_static_validators_v1.py",
    "capabilities/midplatform/core/cognitive_learning/cognitive_learning_fixture_v1.py",
    "capabilities/midplatform/core/cognitive_learning/cognitive_learning_engine_v1.py",
    "capabilities/midplatform/core/cognitive_learning/run_cognitive_learning_controlled_implementation_v1.py",
]
DOC_FILES = [
    "docs/architecture/luna_cognitive_learning_controlled_implementation_v1/cognitive_learning_controlled_implementation_overview_v1.md",
    "docs/architecture/luna_cognitive_learning_controlled_implementation_v1/cognitive_learning_controlled_execution_contract_v1.json",
    "docs/architecture/luna_cognitive_learning_controlled_implementation_v1/cognitive_learning_negative_guards_v1.json",
    "docs/architecture/luna_cognitive_learning_controlled_implementation_v1/cognitive_learning_planning_to_code_mapping_v1.json",
    "docs/architecture/luna_cognitive_learning_controlled_implementation_v1/cognitive_learning_controlled_change_manifest_v1.json",
    "docs/architecture/luna_cognitive_learning_controlled_implementation_v1/cognitive_learning_implementation_summary_v1.md",
    "docs/architecture/luna_cognitive_learning_controlled_implementation_v1/phase_contract.json",
    "docs/architecture/luna_cognitive_learning_controlled_implementation_v1/verify_cognitive_learning_controlled_implementation_v1.py",
]
PLANNING_REQUIRED = [
    "cognitive_learning_owner_boundary_v1.json",
    "learning_evidence_candidate_schema_v1.json",
    "learning_candidate_schema_v1.json",
    "parameter_update_candidate_schema_v1.json",
    "cognitive_learning_minimum_scenario_suite_v1.json",
    "cognitive_learning_negative_guards_v1.json",
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

    owner = _load_json(PLANNING_DIR / "cognitive_learning_owner_boundary_v1.json")
    _expect(
        "canonical_owner",
        owner.get("canonical_owner_candidate") == "Cognitive Learning Governance",
        failed,
    )

    concept = _load_json(
        PLANNING_DIR / "cognitive_learning_concept_boundary_matrix_v1.json"
    )
    inequalities = concept.get("inequalities", [])
    _expect(
        "learning_not_truth",
        _contains_all(
            inequalities,
            [
                "Learning Candidate != Truth",
                "Parameter Update Candidate != Parameter Activation",
            ],
        ),
        failed,
    )

    scenarios = _load_json(
        PLANNING_DIR / "cognitive_learning_minimum_scenario_suite_v1.json"
    )
    ids = [item.get("id", "") for item in scenarios.get("scenarios", [])]
    _expect("scenario_count", scenarios.get("scenario_count") == 32, failed)
    _expect(
        "scenario_ids", _contains_all(ids, [f"L{i:02d}" for i in range(1, 33)]), failed
    )

    result_path = EVAL_OUT_DIR / "cognitive_learning_result_v1.json"
    cases_path = EVAL_OUT_DIR / "cognitive_learning_case_results_v1.json"
    trace_path = EVAL_OUT_DIR / "cognitive_learning_trace_v1.json"
    _expect("runner_result_exists", result_path.exists(), failed)
    _expect("runner_cases_exists", cases_path.exists(), failed)
    _expect("runner_trace_exists", trace_path.exists(), failed)

    if result_path.exists() and cases_path.exists() and trace_path.exists():
        result = _load_json(result_path)
        cases = _load_json(cases_path)
        trace = _load_json(trace_path)
        _expect("runner_scenario_count", result.get("scenario_count") == 32, failed)
        _expect(
            "runner_all_cases_passed", result.get("all_cases_passed") is True, failed
        )
        _expect(
            "runtime_execution_false", result.get("runtime_execution") is False, failed
        )
        _expect(
            "runtime_training_false", result.get("runtime_training") is False, failed
        )
        _expect(
            "model_weight_update_false",
            result.get("model_weight_update") is False,
            failed,
        )
        _expect("database_write_false", result.get("database_write") is False, failed)
        _expect(
            "vector_store_write_false",
            result.get("vector_store_write") is False,
            failed,
        )
        _expect(
            "embedding_execution_false",
            result.get("embedding_execution") is False,
            failed,
        )
        _expect(
            "parameter_mutation_false",
            result.get("parameter_mutation") is False,
            failed,
        )
        _expect(
            "parameter_activation_false",
            result.get("parameter_activation") is False,
            failed,
        )
        _expect(
            "genome_activation_false", result.get("genome_activation") is False, failed
        )
        _expect("memory_mutation_false", result.get("memory_mutation") is False, failed)
        _expect("intent_mutation_false", result.get("intent_mutation") is False, failed)
        _expect("state_mutation_false", result.get("state_mutation") is False, failed)
        _expect(
            "personality_mutation_false",
            result.get("personality_mutation") is False,
            failed,
        )
        _expect(
            "emotion_mutation_false", result.get("emotion_mutation") is False, failed
        )
        _expect(
            "semantic_compression_execution_false",
            result.get("semantic_compression_execution") is False,
            failed,
        )
        _expect(
            "cross_user_transfer_false",
            result.get("cross_user_transfer") is False,
            failed,
        )
        _expect(
            "source_owner_mutation_false",
            result.get("source_owner_mutation") is False,
            failed,
        )
        _expect("synthetic_only_true", result.get("synthetic_only") is True, failed)
        _expect("candidate_only_true", result.get("candidate_only") is True, failed)
        _expect("case_count", len(cases) == 32, failed)
        _expect("trace_case_count", len(trace.get("case_traces", [])) == 32, failed)
        _expect(
            "cases_all_pass",
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
                    "NEXT": "LUNA_COGNITIVE_LEARNING_CONTROLLED_IMPLEMENTATION_REMEDIATION",
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
                "NEXT": "LUNA_COGNITIVE_LEARNING_CONTROLLED_IMPLEMENTATION_GO",
            },
            indent=2,
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
