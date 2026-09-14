#!/usr/bin/env python3
"""Final phase verifier for controlled Dynamic Cognitive Regulation v1.

User Terminal only.  The verifier performs read-only source/contract checks,
executes deterministic synthetic fixtures in memory, and verifies artifacts
written by the separately invoked controlled Runner.
"""

from __future__ import annotations

import ast
import json
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Any, Dict, Iterable


DOC_BASE = Path(__file__).resolve().parent
READY = "LUNA_DYNAMIC_COGNITIVE_REGULATION_CONTROLLED_IMPLEMENTATION_READY"
REMEDIATION = (
    "LUNA_DYNAMIC_COGNITIVE_REGULATION_CONTROLLED_IMPLEMENTATION_REMEDIATION_REQUIRED"
)

CODE_FILES = {
    "__init__.py",
    "dynamic_cognitive_regulation_registry_v1.py",
    "dynamic_cognitive_regulation_error_types_v1.py",
    "dynamic_cognitive_regulation_core_types_v1.py",
    "cognitive_parameter_types_v1.py",
    "cognitive_parameter_bounds_types_v1.py",
    "cognitive_parameter_genome_types_v1.py",
    "dynamic_regulation_candidate_types_v1.py",
    "self_regulation_state_types_v1.py",
    "dynamic_regulation_trace_types_v1.py",
    "dynamic_regulation_handoff_types_v1.py",
    "dynamic_regulation_io_types_v1.py",
    "dynamic_cognitive_regulation_protocol_v1.py",
    "dynamic_cognitive_regulation_ownership_guard_v1.py",
    "dynamic_cognitive_regulation_static_validators_v1.py",
    "dynamic_cognitive_regulation_fixture_v1.py",
    "dynamic_cognitive_regulation_engine_v1.py",
    "run_dynamic_cognitive_regulation_controlled_implementation_v1.py",
}

DOC_FILES = {
    "dynamic_cognitive_regulation_controlled_implementation_overview_v1.md",
    "dynamic_cognitive_regulation_controlled_execution_contract_v1.json",
    "dynamic_cognitive_regulation_negative_guards_v1.json",
    "dynamic_cognitive_regulation_planning_to_code_mapping_v1.json",
    "dynamic_cognitive_regulation_controlled_change_manifest_v1.json",
    "dynamic_cognitive_regulation_implementation_summary_v1.md",
    "phase_contract.json",
    "verify_dynamic_cognitive_regulation_controlled_implementation_v1.py",
}

JSON_FILES = {
    "dynamic_cognitive_regulation_controlled_execution_contract_v1.json",
    "dynamic_cognitive_regulation_negative_guards_v1.json",
    "dynamic_cognitive_regulation_planning_to_code_mapping_v1.json",
    "dynamic_cognitive_regulation_controlled_change_manifest_v1.json",
    "phase_contract.json",
}

PLANNING_FILES = {
    "attention_influence_boundary_v1.json",
    "cognitive_parameter_bounds_contract_v1.json",
    "cognitive_parameter_classification_v1.json",
    "cognitive_parameter_genome_candidate_schema_v1.json",
    "cognitive_state_vector_input_contract_v1.json",
    "dynamic_cognitive_regulation_architecture_plan_v1.md",
    "dynamic_cognitive_regulation_concept_boundary_matrix_v1.json",
    "dynamic_cognitive_regulation_owner_boundary_v1.json",
    "dynamic_regulation_candidate_schema_v1.json",
    "dynamic_regulation_existing_asset_reuse_mapping_v1.json",
    "dynamic_regulation_function_contract_v1.json",
    "dynamic_regulation_gap_registry_v1.json",
    "dynamic_regulation_minimum_scenario_suite_v1.json",
    "dynamic_regulation_negative_guards_v1.json",
    "dynamic_regulation_revision_revocation_model_v1.json",
    "dynamic_regulation_trace_provenance_contract_v1.json",
    "emotion_influence_boundary_v1.json",
    "hypothesis_influence_boundary_v1.json",
    "intent_influence_boundary_v1.json",
    "learning_boundary_v1.json",
    "phase_contract.json",
    "resource_influence_boundary_v1.json",
    "self_regulation_state_model_v1.json",
    "verify_dynamic_cognitive_regulation_module_planning_v1.py",
}


def find_repo_root() -> Path:
    current = Path.cwd().resolve()
    for candidate in (current,) + tuple(current.parents):
        if (
            candidate
            / "capabilities/midplatform/core/dynamic_cognitive_regulation"
        ).is_dir():
            return candidate
    raise RuntimeError("repository_root_with_dynamic_cognitive_regulation_not_found")


def load_json(path: Path) -> Dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError(f"{path.name} must contain a JSON object")
    return value


def emit(checks: list[str], failures: list[str]) -> None:
    print(f"CHECKS: {len(checks)}")
    print(f"FAILED_CHECKS: {failures}")
    print(f"PASSED_CHECK_COUNT: {len(checks) - len(failures)}")
    print(f"FAILED_CHECK_COUNT: {len(failures)}")
    print(f"BLOCKER_COUNT: {len(failures)}")
    if failures:
        print("FINAL_DECISION: BLOCKED_BY_VERIFIER_FAILURE")
        print(f"READINESS: {REMEDIATION}")
        print("NEXT: REMEDIATE_REPORTED_FAILURES_ONLY")
    else:
        print("FINAL_DECISION: V2_FINAL_VERIFICATION_PASSED")
        print(f"READINESS: {READY}")
        print("NEXT: RETURN_COMPLETE_OUTPUT_TO_CHATGPT_FOR_V3_AUDIT")


def _find_case(items: Iterable[Dict[str, Any]], scenario_id: str) -> Dict[str, Any]:
    for item in items:
        if item.get("scenario_id") == scenario_id:
            return item
    return {}


def main() -> int:
    checks: list[str] = []
    failures: list[str] = []

    def check(condition: bool, check_id: str) -> None:
        checks.append(check_id)
        if not condition:
            failures.append(check_id)

    try:
        repo_root = find_repo_root()
        check(True, "repo_root_resolved")
    except RuntimeError:
        repo_root = Path.cwd().resolve()
        check(False, "repo_root_resolved")

    code_dir = repo_root / "capabilities/midplatform/core/dynamic_cognitive_regulation"
    planning_dir = repo_root / "docs/architecture/luna_dynamic_cognitive_regulation_module_planning_v1"
    output_dir = repo_root / "_eval_out/dynamic_cognitive_regulation_controlled_implementation_v1"

    actual_code = {item.name for item in code_dir.iterdir() if item.is_file()}
    actual_doc = {item.name for item in DOC_BASE.iterdir() if item.is_file()}
    actual_planning = {
        item.name for item in planning_dir.iterdir() if item.is_file()
    }
    check(actual_code == CODE_FILES, "exact_code_file_set")
    check(actual_doc == DOC_FILES, "exact_doc_file_set")
    check(actual_planning == PLANNING_FILES, "planning_asset_set_preserved")

    docs: Dict[str, Dict[str, Any]] = {}
    for name in sorted(JSON_FILES):
        try:
            docs[name] = load_json(DOC_BASE / name)
            check(True, f"json_parse:{name}")
        except (OSError, TypeError, json.JSONDecodeError):
            docs[name] = {}
            check(False, f"json_parse:{name}")

    for name in sorted(CODE_FILES):
        try:
            ast.parse((code_dir / name).read_text(encoding="utf-8"))
            check(True, f"ast_parse:{name}")
        except (OSError, SyntaxError):
            check(False, f"ast_parse:{name}")

    contract = docs.get(
        "dynamic_cognitive_regulation_controlled_execution_contract_v1.json", {}
    )
    check(
        contract.get("canonical_owner")
        == "Dynamic Cognitive Regulation Governance",
        "canonical_owner",
    )
    flags = contract.get("boundary_flags", {})
    expected_flags = {
        "synthetic_only": True,
        "candidate_only": True,
        "runtime_executed": False,
        "database_write": False,
        "device_control": False,
        "scheduler_execution": False,
        "task_mutation": False,
        "model_call": False,
        "source_module_mutation": False,
    }
    check(flags == expected_flags, "controlled_boundary_flags")
    check(
        contract.get("input_contract", {}).get("source_mutation_allowed") is False,
        "input_no_source_mutation",
    )
    parameter_model = contract.get("parameter_model", {})
    check(set(parameter_model.get("classes", [])) == {"A", "B", "C", "D", "E"}, "parameter_class_contract")
    check(len(parameter_model.get("required_kinds", [])) == 8, "parameter_kind_contract")
    check(parameter_model.get("silent_coercion") is False, "no_silent_coercion_contract")

    guards = docs.get("dynamic_cognitive_regulation_negative_guards_v1.json", {})
    guard_flags = guards.get("guard_flags", {})
    check(guard_flags.get("integration_has_no_parallel_owner") is True, "no_parallel_owner_guard")
    for key in (
        "source_mutation",
        "intent_mutation",
        "attention_mutation",
        "hypothesis_mutation",
        "causal_mutation",
        "emotion_mutation",
        "learning_direct_activation",
        "database_write",
        "device_control",
        "scheduler_execution",
        "task_mutation",
        "runtime_side_effect",
        "model_call",
        "parameter_bounds_bypass",
        "parameter_genome_auto_activation",
        "cross_user_genome_propagation",
        "silent_parameter_coercion",
    ):
        check(guard_flags.get(key) is False, f"negative_guard:{key}")
    check(
        set(guards.get("forbidden_parallel_owners", []))
        == {
            "Dynamic Function Governance",
            "Self Regulation Governance",
            "Parameter Governance",
            "Parameter Genome Governance",
        },
        "parallel_owner_tokens",
    )

    mapping = docs.get(
        "dynamic_cognitive_regulation_planning_to_code_mapping_v1.json", {}
    )
    mapped_planning = {
        item.get("planning_asset") for item in mapping.get("mappings", [])
    }
    check(mapped_planning == PLANNING_FILES, "planning_to_code_completeness")
    check(mapping.get("mapping_complete") is True, "planning_mapping_complete_flag")

    manifest = docs.get(
        "dynamic_cognitive_regulation_controlled_change_manifest_v1.json", {}
    )
    check(set(manifest.get("created_code_files", [])) == CODE_FILES, "manifest_code_set")
    check(set(manifest.get("created_doc_files", [])) == DOC_FILES, "manifest_doc_set")
    for key in (
        "modified_existing_files",
        "deleted_files",
        "moved_files",
        "renamed_files",
        "source_module_mutations",
        "planning_asset_mutations",
        "runtime_changes",
        "database_changes",
        "device_changes",
        "scheduler_changes",
        "task_changes",
        "model_changes",
    ):
        check(manifest.get(key) == [], f"manifest_empty:{key}")
    check(manifest.get("agent_runner_executed") is False, "agent_runner_not_executed")
    check(manifest.get("agent_final_verifier_executed") is False, "agent_verifier_not_executed")

    phase = docs.get("phase_contract.json", {})
    check(
        phase.get("phase_id")
        == "Phase-Luna-Dynamic-Cognitive-Regulation-Controlled-Implementation-v1-001",
        "phase_id",
    )
    check(phase.get("execution_mode") == "controlled_implementation", "phase_mode")
    check(phase.get("agent_stop_status") == "WAITING_FOR_USER_TERMINAL_VERIFICATION", "phase_stop")
    check(phase.get("boundary_flags") == expected_flags, "phase_boundary_flags")
    check(phase.get("next_phase_not_automatically_authorized") is True, "phase_no_auto_next")

    source_by_file = {
        name: (code_dir / name).read_text(encoding="utf-8")
        for name in CODE_FILES
    }
    all_source = "\n".join(source_by_file.values())
    check("Dynamic Cognitive Regulation Governance" in all_source, "owner_literal_present")
    check("PARAMETER_CLASSES" in all_source and '"A"' in all_source and '"E"' in all_source, "parameter_classes_in_code")
    check("CLAMPED_TO_FROZEN_UPPER_BOUND" in all_source, "upper_bound_enforcement")
    check("CLAMPED_TO_FROZEN_LOWER_BOUND" in all_source, "lower_bound_enforcement")
    check("NO_SILENT_COERCION" in all_source, "silent_coercion_rejection")
    check("cross_user_propagated: bool = False" in all_source, "genome_no_cross_user")
    check("active: bool = False" in all_source, "genome_not_active")
    check("model_weights_rewritten: bool = False" in all_source, "genome_no_weight_rewrite")
    check("user_identity_modified: bool = False" in all_source, "genome_no_identity_change")

    try:
        if str(repo_root) not in sys.path:
            sys.path.insert(0, str(repo_root))

        from capabilities.midplatform.core.dynamic_cognitive_regulation.dynamic_cognitive_regulation_engine_v1 import (
            DynamicCognitiveRegulationEngineV1,
        )
        from capabilities.midplatform.core.dynamic_cognitive_regulation.dynamic_cognitive_regulation_fixture_v1 import (
            get_dynamic_regulation_synthetic_fixtures_v1,
        )
        from capabilities.midplatform.core.dynamic_cognitive_regulation.dynamic_cognitive_regulation_static_validators_v1 import (
            validate_bounds_contract,
            validate_handoff_boundary,
            validate_negative_guard_status,
            validate_parameter_class_coverage,
            validate_parameter_kind_coverage,
            validate_trace_reverse_locatable,
        )

        engine = DynamicCognitiveRegulationEngineV1()
        fixtures = get_dynamic_regulation_synthetic_fixtures_v1()
        expected_ids = {f"R{index:02d}" for index in range(1, 21)}
        check(len(fixtures) == 20, "fixture_count_20")
        check({item.scenario_id for item in fixtures} == expected_ids, "fixture_id_coverage")
        check(validate_parameter_class_coverage(), "parameter_class_coverage")
        all_kinds = tuple(
            parameter.parameter_kind
            for item in fixtures
            for parameter in item.request.parameter_candidates
        )
        check(validate_parameter_kind_coverage(all_kinds), "parameter_kind_coverage")

        in_memory_results: list[Dict[str, Any]] = []
        for item in fixtures:
            output = engine.evaluate(item.request)
            duplicate = engine.evaluate(item.request)
            reasons = set(output.regulation_candidate.reason_codes)
            influence_kinds = {
                value.influence_kind
                for value in output.regulation_candidate.influence_candidates
            }
            case_checks = {
                "expected_status": output.regulation_candidate.evaluation_status
                == item.expected_status,
                "expected_reasons": set(item.expected_reason_tokens).issubset(reasons),
                "expected_influences": set(item.expected_influence_kinds).issubset(influence_kinds),
                "bounds_valid": validate_bounds_contract(item.request.parameter_bounds),
                "handoff_valid": validate_handoff_boundary(output.handoff_candidate),
                "trace_valid": validate_trace_reverse_locatable(output.trace, output.provenance),
                "guards_valid": validate_negative_guard_status(output.negative_guard_status),
                "deterministic": asdict(output) == asdict(duplicate),
                "candidate_only": output.candidate_only is True,
                "synthetic_only": output.synthetic_only is True,
                "no_runtime": output.runtime_executed is False,
                "no_mutation": output.source_mutation_executed is False,
            }
            in_memory_results.append(
                {
                    "scenario_id": item.scenario_id,
                    "output": output,
                    "checks": case_checks,
                    "all_passed": all(case_checks.values()),
                }
            )
        check(all(item["all_passed"] for item in in_memory_results), "all_fixture_behavior_checks")

        r06 = _find_case(in_memory_results, "R06")
        r07 = _find_case(in_memory_results, "R07")
        r10 = _find_case(in_memory_results, "R10")
        r13 = _find_case(in_memory_results, "R13")
        r16 = _find_case(in_memory_results, "R16")
        r17 = _find_case(in_memory_results, "R17")
        r18 = _find_case(in_memory_results, "R18")
        r19 = _find_case(in_memory_results, "R19")
        r20 = _find_case(in_memory_results, "R20")
        check(r06["output"].negative_guard_status.emotion_mutation is False, "emotion_boundary")
        check(r07["output"].negative_guard_status.intent_mutation is False, "intent_boundary")
        check(r10["output"].regulation_candidate.evaluation_status == "REJECTED", "immutable_parameter_rejected")
        check(bool(r13["output"].regulation_candidate.conflict_candidates), "conflicts_preserved")
        check(r16["output"].genome_candidate.active is False, "genome_candidate_only")
        check(r16["output"].negative_guard_status.learning_direct_activation is False, "learning_boundary")
        check(r17["output"].revision_candidate is not None and bool(r17["output"].trace.revision_lineage_refs), "revision_behavior")
        check(r18["output"].revocation_candidate is not None and bool(r18["output"].trace.revocation_lineage_refs), "revocation_behavior")
        check(r19["checks"]["deterministic"] is True, "idempotent_behavior")
        check(r20["output"].handoff_candidate.candidate_only is True, "candidate_handoff")
        check(all(item["output"].negative_guard_status.attention_mutation is False for item in in_memory_results), "attention_boundary")
        check(all(item["output"].negative_guard_status.hypothesis_mutation is False for item in in_memory_results), "hypothesis_boundary")
        check(all(item["output"].negative_guard_status.causal_mutation is False for item in in_memory_results), "causal_boundary")
        check(all(item["output"].negative_guard_status.scheduler_execution is False for item in in_memory_results), "resource_no_scheduler")
    except (ImportError, AttributeError, KeyError, TypeError, ValueError):
        check(False, "implementation_import_and_behavior")

    result_path = output_dir / "dynamic_cognitive_regulation_result_v1.json"
    cases_path = output_dir / "dynamic_cognitive_regulation_case_results_v1.json"
    trace_path = output_dir / "dynamic_cognitive_regulation_trace_v1.json"
    check(result_path.is_file(), "runner_result_artifact_exists")
    check(cases_path.is_file(), "runner_case_artifact_exists")
    check(trace_path.is_file(), "runner_trace_artifact_exists")
    try:
        result_doc = load_json(result_path)
        cases_doc = json.loads(cases_path.read_text(encoding="utf-8"))
        trace_doc = load_json(trace_path)
        check(True, "runner_artifacts_json_parse")
        check(result_doc.get("scenario_count") == 20, "runner_scenario_count")
        check(result_doc.get("passed_case_count") == 20, "runner_passed_case_count")
        check(result_doc.get("failed_case_count") == 0, "runner_failed_case_count")
        check(set(result_doc.get("scenario_ids", [])) == {f"R{i:02d}" for i in range(1, 21)}, "runner_scenario_ids")
        check(isinstance(cases_doc, list) and len(cases_doc) == 20, "runner_case_coverage")
        check(all(item.get("all_checks_passed") is True for item in cases_doc), "runner_all_case_checks")
        check(all(item.get("expected_behavior") and item.get("actual_behavior") for item in cases_doc), "runner_expected_actual_behavior")
        check(trace_doc.get("reverse_locatable") is True, "runner_trace_reverse_locatable")
        check(trace_doc.get("provenance_grants_authority") is False, "runner_trace_no_authority")
        for key, expected in expected_flags.items():
            check(result_doc.get(key) is expected, f"runner_boundary:{key}")
    except (OSError, TypeError, json.JSONDecodeError):
        check(False, "runner_artifacts_json_parse")

    emit(checks, failures)
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
