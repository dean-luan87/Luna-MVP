#!/usr/bin/env python3
"""Final phase verifier for Runtime Executor controlled implementation v1."""

from __future__ import annotations

import ast
import json
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List


DOC_BASE = Path(__file__).resolve().parent
READY = "LUNA_RUNTIME_EXECUTOR_CONTROLLED_IMPLEMENTATION_READY"
REMEDIATION = "LUNA_RUNTIME_EXECUTOR_CONTROLLED_IMPLEMENTATION_REMEDIATION_REQUIRED"

CODE_FILES = {
    "__init__.py",
    "runtime_executor_registry_v1.py",
    "runtime_executor_error_types_v1.py",
    "runtime_executor_core_types_v1.py",
    "execution_request_types_v1.py",
    "execution_state_types_v1.py",
    "admission_result_types_v1.py",
    "execution_final_gate_types_v1.py",
    "execution_idempotency_types_v1.py",
    "execution_attempt_types_v1.py",
    "execution_retry_types_v1.py",
    "execution_timeout_types_v1.py",
    "execution_cancellation_types_v1.py",
    "execution_partial_result_types_v1.py",
    "execution_failure_types_v1.py",
    "execution_rollback_types_v1.py",
    "execution_scheduler_reference_types_v1.py",
    "execution_task_reference_types_v1.py",
    "execution_adapter_reference_types_v1.py",
    "execution_result_types_v1.py",
    "execution_diagnostics_handoff_types_v1.py",
    "execution_trace_types_v1.py",
    "runtime_executor_handoff_types_v1.py",
    "runtime_executor_io_types_v1.py",
    "runtime_executor_protocol_v1.py",
    "runtime_executor_ownership_guard_v1.py",
    "runtime_executor_static_validators_v1.py",
    "runtime_executor_fixture_v1.py",
    "runtime_executor_engine_v1.py",
    "run_runtime_executor_controlled_implementation_v1.py",
}

DOC_FILES = {
    "runtime_executor_controlled_implementation_overview_v1.md",
    "runtime_executor_controlled_execution_contract_v1.json",
    "runtime_executor_negative_guards_v1.json",
    "runtime_executor_planning_to_code_mapping_v1.json",
    "runtime_executor_controlled_change_manifest_v1.json",
    "runtime_executor_implementation_summary_v1.md",
    "phase_contract.json",
    "verify_runtime_executor_controlled_implementation_v1.py",
}

JSON_FILES = {
    "runtime_executor_controlled_execution_contract_v1.json",
    "runtime_executor_negative_guards_v1.json",
    "runtime_executor_planning_to_code_mapping_v1.json",
    "runtime_executor_controlled_change_manifest_v1.json",
    "phase_contract.json",
}

REQUIRED_SCENARIO_IDS = {
    "R01",
    "R02",
    "R03",
    "R04",
    "R05",
    "R06",
    "R07",
    "R08",
    "R09",
    "R10",
    "R11",
    "R12",
    "R13",
    "R14",
    "R15",
    "R16",
    "R17",
    "R18",
}


def find_repo_root() -> Path:
    current = Path.cwd().resolve()
    for candidate in (current,) + tuple(current.parents):
        if (candidate / "capabilities/midplatform/core/runtime_executor").is_dir():
            return candidate
    raise RuntimeError("repository_root_with_runtime_executor_not_found")


def load_json(path: Path) -> Dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError(f"{path.name} must contain a JSON object")
    return value


def emit(checks: List[str], failures: List[str]) -> None:
    print("CHECKS")
    for item in checks:
        print(item)

    print("FAILED_CHECKS")
    for item in failures:
        print(item)

    print("PASSED_CHECK_COUNT")
    print(max(0, len(checks) - len(failures)))

    print("FAILED_CHECK_COUNT")
    print(len(failures))

    print("BLOCKER_COUNT")
    print(len(failures))

    print("FINAL_DECISION")
    print(READY if not failures else "BLOCKED_BY_VERIFIER_FAILURE")

    print("READINESS")
    print(READY if not failures else REMEDIATION)

    print("NEXT")
    print(
        "RETURN_COMPLETE_OUTPUT_TO_CHATGPT_FOR_V3_AUDIT"
        if not failures
        else "REMEDIATE_REPORTED_FAILURES_ONLY"
    )


def _find_case(items: Iterable[Dict[str, Any]], case_id: str) -> Dict[str, Any]:
    for item in items:
        if item.get("case_id") == case_id:
            return item
    return {}


def main() -> int:
    checks: List[str] = []
    failures: List[str] = []

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

    code_dir = repo_root / "capabilities/midplatform/core/runtime_executor"
    actual_code = {item.name for item in code_dir.iterdir() if item.is_file()}
    actual_doc = {item.name for item in DOC_BASE.iterdir() if item.is_file()}
    check(actual_code == CODE_FILES, "exact_code_file_set")
    check(actual_doc == DOC_FILES, "exact_doc_file_set")

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

    contract = docs.get("runtime_executor_controlled_execution_contract_v1.json", {})
    check(contract.get("canonical_owner") == "Runtime Executor", "canonical_owner")
    aliases = contract.get("legacy_aliases", [])
    check(
        all(item.get("mutation_authority") is False for item in aliases),
        "legacy_alias_no_mutation_authority",
    )
    check(
        all(item.get("authority") is False for item in aliases),
        "legacy_alias_no_parallel_authority",
    )
    check(contract.get("synthetic_execution_lifecycle") is True, "synthetic_lifecycle")
    check(contract.get("candidate_only") is True, "candidate_only_contract")
    check(contract.get("planning_only") is True, "planning_only_contract")
    check(contract.get("runtime_execution") is False, "no_runtime_execution")
    check(contract.get("adapter_call_execution") is False, "no_adapter_execution")
    check(contract.get("provider_call_execution") is False, "no_provider_execution")
    check(contract.get("device_control") is False, "no_device_control")
    check(contract.get("scheduler_execution") is False, "no_scheduler_execution")
    check(
        contract.get("task_lifecycle_mutation") is False,
        "no_task_lifecycle_mutation",
    )
    check(contract.get("database_write") is False, "no_database_write")

    mapping = docs.get("runtime_executor_planning_to_code_mapping_v1.json", {})
    mapped = {Path(item).name for item in mapping.get("all_code_assets", [])}
    check(mapped == CODE_FILES, "planning_to_code_completeness")
    scenario_map = mapping.get("scenario_mapping", [])
    check(len(scenario_map) == 18, "scenario_mapping_count_18")
    check(
        {item.get("scenario_id") for item in scenario_map} == REQUIRED_SCENARIO_IDS,
        "scenario_mapping_ids_covered",
    )
    check(
        mapping.get("planning_assets_modified") is False, "planning_assets_unmodified"
    )
    check(
        mapping.get("parallel_implementation_created") is False,
        "no_parallel_runtime_executor_owner",
    )

    manifest = docs.get("runtime_executor_controlled_change_manifest_v1.json", {})
    created_code = {Path(item).name for item in manifest.get("created_code_files", [])}
    created_doc = {
        Path(item).name for item in manifest.get("created_documentation_files", [])
    }
    check(created_code == CODE_FILES, "manifest_code_set")
    check(created_doc == DOC_FILES, "manifest_doc_set")
    check(
        manifest.get("modified_existing_files") == [], "no_existing_asset_modification"
    )
    check(
        manifest.get("planning_assets_modified") is False,
        "manifest_planning_unmodified",
    )
    check(manifest.get("runtime_executed") is False, "manifest_runtime_false")
    check(manifest.get("adapter_called") is False, "manifest_adapter_false")
    check(manifest.get("provider_called") is False, "manifest_provider_false")
    check(manifest.get("device_accessed") is False, "manifest_device_false")
    check(manifest.get("scheduler_executed") is False, "manifest_scheduler_false")
    check(manifest.get("task_mutated") is False, "manifest_task_mutation_false")
    check(manifest.get("database_accessed") is False, "manifest_database_false")

    guards = docs.get("runtime_executor_negative_guards_v1.json", {})
    guard_set = set(guards.get("negative_guards", []))
    required_guards = {
        "action candidate != execution request",
        "execution readiness != execution",
        "executor != decision governance",
        "executor != action governance",
        "executor != task manager",
        "executor != scheduler",
        "permission bypass forbidden",
        "safety bypass forbidden",
        "final gate skip forbidden",
        "automatic retry forbidden",
        "retry without authority forbidden",
        "timeout without trace forbidden",
        "cancellation without trace forbidden",
        "partial result marked success forbidden",
        "rollback execution claim without trigger forbidden",
        "adapter direct side effect claim forbidden",
        "diagnostics as decision authority forbidden",
        "result handoff as owner transfer forbidden",
        "parallel runtime executor authority forbidden",
        "runtime/device/provider call forbidden",
        "scheduler runtime forbidden",
        "task mutation forbidden",
        "database write forbidden",
    }
    check(required_guards <= guard_set, "negative_guard_completeness")

    phase = docs.get("phase_contract.json", {})
    check(
        phase.get("phase")
        == "Phase-Luna-Runtime-Executor-Controlled-Implementation-v1-001",
        "phase_id",
    )
    check(
        phase.get("agent_stop_point") == "WAITING_FOR_USER_TERMINAL_VERIFICATION",
        "phase_waiting",
    )

    try:
        if str(repo_root) not in sys.path:
            sys.path.insert(0, str(repo_root))

        from capabilities.midplatform.core.runtime_executor.runtime_executor_engine_v1 import (
            RuntimeExecutorEngineV1,
        )
        from capabilities.midplatform.core.runtime_executor.runtime_executor_fixture_v1 import (
            get_runtime_executor_synthetic_fixtures_v1,
        )
        from capabilities.midplatform.core.runtime_executor.runtime_executor_static_validators_v1 import (
            validate_final_gate,
            validate_idempotency_behavior,
            validate_negative_guards,
            validate_no_side_effects,
            validate_partial_not_success,
            validate_result_handoffs,
            validate_retry_boundary,
            validate_state,
            validate_timeout_cancel,
            validate_trace,
        )

        engine = RuntimeExecutorEngineV1()
        fixtures = get_runtime_executor_synthetic_fixtures_v1()
        check(len(fixtures) == 18, "scenario_fixture_count_18")
        check(
            REQUIRED_SCENARIO_IDS == {item.case_id for item in fixtures},
            "scenario_id_coverage_18",
        )

        case_results: List[Dict[str, Any]] = []
        for case in fixtures:
            output = engine.run_case(case.request)
            expectation_checks_for_case = {
                "status_expected": output.result.status == case.expected_status,
                "state_expected": output.state.state == case.expected_state,
                "admitted_expected": output.admission.admitted
                is case.expected_admitted,
                "retry_blocked_expected": (
                    output.retry.blocked_reason == "retry_without_authority"
                )
                is case.expected_retry_blocked,
                "idempotency_duplicate_expected": output.idempotency_duplicate
                is case.expected_idempotency_duplicate,
                "idempotency_scope_mismatch_expected": output.idempotency_scope_mismatch
                is case.expected_idempotency_scope_mismatch,
                "partial_present_expected": (output.partial_result is not None)
                is case.expected_partial_present,
                "failure_present_expected": (output.failure is not None)
                is case.expected_failure_present,
                "rollback_required_expected": output.rollback.rollback_required
                is case.expected_rollback_required,
            }
            behavior_checks_for_case = {
                "validate_state": validate_state(output),
                "validate_final_gate": validate_final_gate(output),
                "validate_idempotency_behavior": validate_idempotency_behavior(output),
                "validate_retry_boundary": validate_retry_boundary(output),
                "validate_timeout_cancel": validate_timeout_cancel(output),
                "validate_partial_not_success": validate_partial_not_success(output),
                "validate_handoffs": validate_result_handoffs(output),
                "validate_trace": validate_trace(output),
                "validate_no_side_effects": validate_no_side_effects(output),
                "validate_negative_guards": validate_negative_guards(),
            }
            case_results.append(
                {
                    "case_id": case.case_id,
                    "status": output.result.status,
                    "state": output.state.state,
                    "idempotency_duplicate": output.idempotency_duplicate,
                    "idempotency_scope_mismatch": output.idempotency_scope_mismatch,
                    "retry_blocked_reason": output.retry.blocked_reason,
                    "partial_present": output.partial_result is not None,
                    "failure_present": output.failure is not None,
                    "rollback_required": output.rollback.rollback_required,
                    "handoff_reference_only": output.action_handoff.reference_only
                    and output.task_handoff.reference_only
                    and output.diagnostics_result_handoff.reference_only,
                    "all_expectations_passed": all(
                        expectation_checks_for_case.values()
                    ),
                    "all_behaviors_passed": all(behavior_checks_for_case.values()),
                }
            )

        check(
            all(item["all_expectations_passed"] for item in case_results),
            "all_fixture_expectations_pass",
        )
        check(
            all(item["all_behaviors_passed"] for item in case_results),
            "all_fixture_behaviors_pass",
        )

        r06 = _find_case(case_results, "R06")
        check(
            r06.get("idempotency_duplicate") is True, "idempotency_duplicate_behavior"
        )
        r07 = _find_case(case_results, "R07")
        check(
            r07.get("idempotency_scope_mismatch") is True,
            "idempotency_scope_mismatch_behavior",
        )
        r09 = _find_case(case_results, "R09")
        check(
            r09.get("retry_blocked_reason") == "retry_without_authority",
            "retry_without_authority_behavior",
        )
        r10 = _find_case(case_results, "R10")
        check(r10.get("status") == "TIMEOUT_CANDIDATE", "timeout_behavior")
        r11 = _find_case(case_results, "R11")
        check(r11.get("status") == "CANCELLED_CANDIDATE", "cancellation_behavior")
        r12 = _find_case(case_results, "R12")
        check(
            r12.get("status") == "PARTIAL_RESULT_CANDIDATE",
            "partial_not_success_behavior",
        )
        r13 = _find_case(case_results, "R13")
        check(
            r13.get("failure_present") is True and r13.get("rollback_required") is True,
            "failure_rollback_behavior",
        )
        r17 = _find_case(case_results, "R17")
        check(
            r17.get("handoff_reference_only") is True,
            "result_handoff_reference_only_behavior",
        )

    except Exception:
        check(False, "in_process_behavior_verification")

    eval_dir = repo_root / "_eval_out/runtime_executor_controlled_implementation_v1"
    result_file = eval_dir / "runtime_executor_result_v1.json"
    case_file = eval_dir / "runtime_executor_case_results_v1.json"
    trace_file = eval_dir / "runtime_executor_trace_v1.json"

    check(result_file.is_file(), "runner_artifact_result_exists")
    check(case_file.is_file(), "runner_artifact_cases_exists")
    check(trace_file.is_file(), "runner_artifact_trace_exists")

    if result_file.is_file():
        try:
            summary_payload = json.loads(result_file.read_text(encoding="utf-8"))
            check(summary_payload.get("case_count") == 18, "runner_summary_case_count")
            check(
                summary_payload.get("runtime_executed") is False,
                "runner_summary_runtime_false",
            )
            check(
                summary_payload.get("database_write_executed") is False,
                "runner_summary_database_false",
            )
        except Exception:
            check(False, "runner_summary_parse")

    if case_file.is_file():
        try:
            payload = json.loads(case_file.read_text(encoding="utf-8"))
            check(
                isinstance(payload, list) and len(payload) == 18,
                "runner_case_file_coverage",
            )
            c06 = _find_case(payload, "R06")
            c07 = _find_case(payload, "R07")
            c09 = _find_case(payload, "R09")
            c10 = _find_case(payload, "R10")
            c12 = _find_case(payload, "R12")
            c17 = _find_case(payload, "R17")
            check(
                c06.get("idempotency", {}).get("duplicate") is True,
                "runner_case_r06_duplicate",
            )
            check(
                c07.get("idempotency", {}).get("scope_mismatch") is True,
                "runner_case_r07_scope_mismatch",
            )
            check(
                c09.get("retry", {}).get("blocked_reason") == "retry_without_authority",
                "runner_case_r09_retry_blocked",
            )
            check(c10.get("status") == "TIMEOUT_CANDIDATE", "runner_case_r10_timeout")
            check(
                c12.get("status") == "PARTIAL_RESULT_CANDIDATE",
                "runner_case_r12_partial",
            )
            check(
                c17.get("checks", {}).get("handoffs_valid") is True,
                "runner_case_r17_handoff",
            )
        except Exception:
            check(False, "runner_case_file_parse")

    emit(checks, failures)
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
