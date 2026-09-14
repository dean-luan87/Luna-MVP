#!/usr/bin/env python3
"""Final phase verifier for Action Governance controlled implementation v1."""

from __future__ import annotations

import ast
import json
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List


DOC_BASE = Path(__file__).resolve().parent
READY = "LUNA_ACTION_GOVERNANCE_CONTROLLED_IMPLEMENTATION_READY"
REMEDIATION = "LUNA_ACTION_GOVERNANCE_CONTROLLED_IMPLEMENTATION_REMEDIATION_REQUIRED"

CODE_FILES = {
    "__init__.py",
    "action_registry_v1.py",
    "action_error_types_v1.py",
    "action_core_types_v1.py",
    "action_state_types_v1.py",
    "action_precondition_types_v1.py",
    "action_dependency_types_v1.py",
    "action_permission_safety_types_v1.py",
    "action_confirmation_types_v1.py",
    "action_reversibility_types_v1.py",
    "action_readiness_types_v1.py",
    "action_resource_types_v1.py",
    "action_lifecycle_types_v1.py",
    "action_rollback_types_v1.py",
    "action_failure_types_v1.py",
    "action_trace_types_v1.py",
    "action_handoff_types_v1.py",
    "action_io_types_v1.py",
    "action_governance_protocol_v1.py",
    "action_ownership_guard_v1.py",
    "action_static_validators_v1.py",
    "action_governance_fixture_v1.py",
    "action_governance_engine_v1.py",
    "run_action_governance_controlled_implementation_v1.py",
}

DOC_FILES = {
    "action_governance_controlled_implementation_overview_v1.md",
    "action_governance_controlled_execution_contract_v1.json",
    "action_governance_negative_guards_v1.json",
    "action_governance_planning_to_code_mapping_v1.json",
    "action_governance_controlled_change_manifest_v1.json",
    "action_governance_implementation_summary_v1.md",
    "phase_contract.json",
    "verify_action_governance_controlled_implementation_v1.py",
}

JSON_FILES = {
    "action_governance_controlled_execution_contract_v1.json",
    "action_governance_negative_guards_v1.json",
    "action_governance_planning_to_code_mapping_v1.json",
    "action_governance_controlled_change_manifest_v1.json",
    "phase_contract.json",
}

REQUIRED_SCENARIO_IDS = {
    "A01_SELECTED_DECISION_TO_BASIC_ACTION_CANDIDATE",
    "A02_PERMISSION_VALID_TO_ELIGIBLE",
    "A03_PERMISSION_REVOKED_TO_BLOCKED",
    "A04_SAFETY_VETO_TO_BLOCKED",
    "A05_MISSING_PRECONDITION_TO_PENDING",
    "A06_UNKNOWN_PRECONDITION_NOT_SATISFIED",
    "A07_HUMAN_CONFIRMATION_REQUIRED",
    "A08_STALE_CONFIRMATION_REJECTED",
    "A09_REVERSIBLE_ACTION",
    "A10_IRREVERSIBLE_STRONGER_CONFIRMATION_REQUIRED",
    "A11_RESOURCE_UNAVAILABLE_TO_SUSPENDED",
    "A12_TARGET_INVALIDATED_TO_CANCELLED",
    "A13_DEPENDENCY_INCOMPLETE_TO_PENDING",
    "A14_ROLLBACK_REQUIRED_CANDIDATE",
    "A15_ACTION_TO_EXECUTOR_CANDIDATE_ONLY_HANDOFF",
    "A16_ACTION_TO_TASK_MANAGER_REFERENCE_ONLY_HANDOFF",
}


def find_repo_root() -> Path:
    current = Path.cwd().resolve()
    for candidate in (current,) + tuple(current.parents):
        if (candidate / "capabilities/midplatform/core/action_governance").is_dir():
            return candidate
    raise RuntimeError("repository_root_with_action_governance_not_found")


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

    code_dir = repo_root / "capabilities/midplatform/core/action_governance"
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

    contract = docs.get("action_governance_controlled_execution_contract_v1.json", {})
    check(contract.get("canonical_owner") == "Action Governance", "canonical_owner")
    aliases = contract.get("legacy_aliases", [])
    check(
        all(item.get("mutation_authority") is False for item in aliases),
        "legacy_alias_no_authority",
    )
    check(
        all(item.get("authority") is False for item in aliases),
        "legacy_alias_no_parallel_authority",
    )
    check(contract.get("candidate_only") is True, "candidate_only_contract")
    check(contract.get("runtime_execution") is False, "no_runtime_execution")
    check(contract.get("database_write") is False, "no_database_write")
    check(contract.get("device_control") is False, "no_device_control")
    check(contract.get("scheduler_execution") is False, "no_scheduler_execution")
    check(contract.get("task_creation") is False, "no_task_creation")

    mapping = docs.get("action_governance_planning_to_code_mapping_v1.json", {})
    mapped = {Path(item).name for item in mapping.get("all_code_assets", [])}
    check(mapped == CODE_FILES, "planning_to_code_completeness")
    check(
        mapping.get("planning_assets_modified") is False, "planning_assets_unmodified"
    )
    check(
        mapping.get("parallel_implementation_created") is False,
        "no_parallel_action_owner",
    )

    manifest = docs.get("action_governance_controlled_change_manifest_v1.json", {})
    created_code = {Path(item).name for item in manifest.get("created_code_files", [])}
    created_doc = {
        Path(item).name for item in manifest.get("created_documentation_files", [])
    }
    check(created_code == CODE_FILES, "manifest_code_set")
    check(created_doc == DOC_FILES, "manifest_doc_set")
    check(
        manifest.get("modified_existing_files") == [], "no_existing_asset_modification"
    )
    check(manifest.get("runtime_executed") is False, "manifest_runtime_false")
    check(manifest.get("database_accessed") is False, "manifest_database_false")
    check(manifest.get("device_accessed") is False, "manifest_device_false")
    check(manifest.get("scheduler_executed") is False, "manifest_scheduler_false")

    guards = docs.get("action_governance_negative_guards_v1.json", {})
    guard_set = set(guards.get("negative_guards", []))
    required_guards = {
        "decision != action",
        "selected decision != action execution",
        "action candidate != runtime command",
        "eligible != executed",
        "ready != executed",
        "authorized != executed",
        "action governance != executor",
        "action governance != task manager",
        "permission context != permanent authorization",
        "safety context != permanent authorization",
        "confirmation cannot be fabricated",
        "stale confirmation cannot be reused",
        "unknown precondition != satisfied",
        "rollback candidate != rollback execution",
        "failure result != retry authority",
        "no runtime side effect",
        "no database write",
        "no device control",
        "no task creation",
        "no scheduler execution",
        "no permission bypass",
        "no safety bypass",
    }
    check(required_guards <= guard_set, "negative_guard_completeness")

    phase = docs.get("phase_contract.json", {})
    check(
        phase.get("phase")
        == "Phase-Luna-Action-Governance-Controlled-Implementation-v1-001",
        "phase_id",
    )
    check(
        phase.get("agent_stop_point") == "WAITING_FOR_USER_TERMINAL_VERIFICATION",
        "phase_waiting",
    )

    try:
        if str(repo_root) not in sys.path:
            sys.path.insert(0, str(repo_root))

        from capabilities.midplatform.core.action_governance.action_governance_engine_v1 import (
            ActionGovernanceEngineV1,
        )
        from capabilities.midplatform.core.action_governance.action_governance_fixture_v1 import (
            get_action_synthetic_fixtures_v1,
        )
        from capabilities.midplatform.core.action_governance.action_static_validators_v1 import (
            validate_handoffs,
            validate_negative_guard_flags,
            validate_no_runtime_side_effects,
            validate_trace_completeness,
        )

        engine = ActionGovernanceEngineV1()
        fixtures = get_action_synthetic_fixtures_v1()
        check(len(fixtures) == 16, "scenario_fixture_count_16")
        check(
            REQUIRED_SCENARIO_IDS == {item.case_id for item in fixtures},
            "scenario_id_coverage_16",
        )

        case_results: List[Dict[str, Any]] = []
        for case in fixtures:
            output = engine.run_case(case.request)
            expectation_checks_for_case = {
                "state_expected": output.action_candidate.action_state
                == case.expected_state,
                "readiness_expected": output.readiness.state == case.expected_readiness,
                "runtime_handoff_expected": (
                    output.runtime_handoff.execution_readiness == "candidate_ready"
                )
                is case.expected_runtime_handoff_eligible,
                "task_reference_only_expected": (
                    output.task_handoff.reference_only
                    is case.expected_task_handoff_reference_only
                ),
            }
            behavior_checks_for_case = {
                "trace_complete": validate_trace_completeness(output),
                "handoff_valid": validate_handoffs(output),
                "no_runtime": validate_no_runtime_side_effects(output),
                "negative_guards": validate_negative_guard_flags(),
                "task_reference_only": output.task_handoff.reference_only is True,
            }
            case_results.append(
                {
                    "case_id": case.case_id,
                    "state": output.action_candidate.action_state,
                    "readiness": output.readiness.state,
                    "runtime_handoff_eligible": output.runtime_handoff.execution_readiness
                    == "candidate_ready",
                    "task_reference_only": output.task_handoff.reference_only,
                    "provenance": list(output.trace_candidate.provenance),
                    "expectation_checks": expectation_checks_for_case,
                    "behavior_checks": behavior_checks_for_case,
                    "all_passed": all(expectation_checks_for_case.values()),
                }
            )

        check(
            all(item["all_passed"] for item in case_results),
            "all_fixture_expectations_pass",
        )

        a02 = _find_case(case_results, "A02_PERMISSION_VALID_TO_ELIGIBLE")
        check(a02.get("state") == "ELIGIBLE", "permission_valid_behavior")

        a03 = _find_case(case_results, "A03_PERMISSION_REVOKED_TO_BLOCKED")
        check(
            a03.get("state") == "NEEDS_PERMISSION"
            and a03.get("readiness") == "blocked",
            "permission_revoked_behavior",
        )

        a04 = _find_case(case_results, "A04_SAFETY_VETO_TO_BLOCKED")
        check(a04.get("state") == "BLOCKED", "safety_veto_behavior")

        a05 = _find_case(case_results, "A05_MISSING_PRECONDITION_TO_PENDING")
        check(
            a05.get("state") == "PRECONDITION_PENDING", "missing_precondition_behavior"
        )

        a06 = _find_case(case_results, "A06_UNKNOWN_PRECONDITION_NOT_SATISFIED")
        check(a06.get("readiness") == "blocked", "unknown_precondition_behavior")

        a07 = _find_case(case_results, "A07_HUMAN_CONFIRMATION_REQUIRED")
        check(
            a07.get("state") == "NEEDS_CONFIRMATION", "confirmation_required_behavior"
        )

        a08 = _find_case(case_results, "A08_STALE_CONFIRMATION_REJECTED")
        check(
            a08.get("readiness") == "blocked", "stale_confirmation_rejection_behavior"
        )

        a10 = _find_case(
            case_results, "A10_IRREVERSIBLE_STRONGER_CONFIRMATION_REQUIRED"
        )
        check(
            a10.get("state") == "NEEDS_CONFIRMATION",
            "irreversible_stricter_gate_behavior",
        )

        a11 = _find_case(case_results, "A11_RESOURCE_UNAVAILABLE_TO_SUSPENDED")
        check(a11.get("state") == "SUSPENDED", "resource_suspended_behavior")

        a12 = _find_case(case_results, "A12_TARGET_INVALIDATED_TO_CANCELLED")
        check(a12.get("state") == "CANCELLED", "target_cancelled_behavior")

        a13 = _find_case(case_results, "A13_DEPENDENCY_INCOMPLETE_TO_PENDING")
        check(a13.get("state") == "PRECONDITION_PENDING", "dependency_pending_behavior")

        a14 = _find_case(case_results, "A14_ROLLBACK_REQUIRED_CANDIDATE")
        check(a14.get("state") == "ROLLBACK_REQUIRED", "rollback_required_behavior")

        a15 = _find_case(case_results, "A15_ACTION_TO_EXECUTOR_CANDIDATE_ONLY_HANDOFF")
        check(
            a15.get("runtime_handoff_eligible") is True,
            "executor_candidate_only_handoff_behavior",
        )

        a16 = _find_case(
            case_results, "A16_ACTION_TO_TASK_MANAGER_REFERENCE_ONLY_HANDOFF"
        )
        check(
            a16.get("task_reference_only") is True,
            "task_reference_only_handoff_behavior",
        )

    except Exception:
        check(False, "in_process_behavior_verification")

    eval_dir = repo_root / "_eval_out/action_governance_controlled_implementation_v1"
    case_file = eval_dir / "action_governance_case_results_v1.json"
    if case_file.is_file():
        try:
            payload = json.loads(case_file.read_text(encoding="utf-8"))
            check(
                isinstance(payload, list) and len(payload) == 16,
                "runner_case_file_coverage",
            )
            r_a03 = _find_case(payload, "A03_PERMISSION_REVOKED_TO_BLOCKED")
            r_a04 = _find_case(payload, "A04_SAFETY_VETO_TO_BLOCKED")
            r_a14 = _find_case(payload, "A14_ROLLBACK_REQUIRED_CANDIDATE")
            r_a15 = _find_case(payload, "A15_ACTION_TO_EXECUTOR_CANDIDATE_ONLY_HANDOFF")
            r_a16 = _find_case(
                payload, "A16_ACTION_TO_TASK_MANAGER_REFERENCE_ONLY_HANDOFF"
            )
            check(
                r_a03.get("state") == "NEEDS_PERMISSION", "runner_case_a03_permission"
            )
            check(r_a04.get("state") == "BLOCKED", "runner_case_a04_safety")
            check(r_a14.get("state") == "ROLLBACK_REQUIRED", "runner_case_a14_rollback")
            check(
                r_a15.get("handoff_eligibility", {}).get("runtime_candidate_ready")
                is True,
                "runner_case_a15_executor_handoff",
            )
            check(
                r_a16.get("handoff_eligibility", {}).get("task_reference_only") is True,
                "runner_case_a16_task_handoff",
            )
            check(bool(r_a16.get("provenance")), "runner_case_provenance")
        except Exception:
            check(False, "runner_case_file_parse")
    else:
        check(False, "runner_case_file_exists")

    emit(checks, failures)
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
