"""Controlled verifier for Governance Verification Backbone core rules."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, is_dataclass
from pathlib import Path
from typing import Any, Dict, List

from capabilities.midplatform.protocol_manager.module.governance_verification_backbone_v1 import (
    compute_unified_final_decision,
    resolve_applicable_governance_set,
)

from .fixtures_v1 import build_governance_backbone_cases_v1


OUTPUT_DIR = Path("_eval_out/governance_verification_backbone_core_rules_v1")
REQUIRED_CASES = {
    "GOVERNED_PHASE_VALID",
    "NO_APPLICABLE_RULES_FAIL_CLOSED",
    "UNKNOWN_RULE_OWNER",
    "UNKNOWN_RULE_SOURCE",
    "ORPHAN_GOVERNANCE_RULE",
    "INVALID_GOVERNANCE_PROFILE",
    "RULE_VERSION_MISSING",
    "AUTHORITY_WITH_RESPONSIBILITY",
    "AUTHORITY_WITHOUT_RESPONSIBILITY",
    "RESPONSIBILITY_WITHOUT_AUTHORITY",
    "AUTHORITY_OWNER_MISSING",
    "AUTHORITY_COLLISION",
    "RESPONSIBILITY_OWNER_MISMATCH",
    "CANDIDATE_ONLY_VALID",
    "CANDIDATE_ATTEMPTS_AUTHORITY",
    "NO_RUNTIME_VALID",
    "NO_RUNTIME_BUT_EXECUTION_CREATED",
    "NO_TRUTH_VALID",
    "NO_TRUTH_BUT_TRUTH_DECLARED",
    "REQUESTER_OWNS_REQUIREMENT_COMPLEXITY",
    "DOWNSTREAM_INVENTS_REQUIREMENT",
    "EXECUTOR_OWNS_EXECUTION_COMPLEXITY",
    "REQUESTER_ASSIGNED_RESOURCE_FAILURE",
    "GATEWAY_INGRESS_ADMISSION_NOT_PRE_EXECUTION_AUTHORITY",
    "ADAPTER_PRESERVES_LINEAGE",
    "ADAPTER_ACQUIRES_SEMANTIC_AUTHORITY",
    "ALL_GOVERNANCE_AND_FUNCTIONAL_PASS_GO",
    "GOVERNANCE_FAIL_FORCES_NO_GO",
    "FUNCTIONAL_FAIL_FORCES_NO_GO",
    "CONTRACT_FAILURE_FORCES_NO_GO",
    "WAITING_STATUS_NOT_USED_AS_FINAL_DECISION",
    "DETERMINISTIC_RULE_RESOLUTION",
    "DETERMINISTIC_FINAL_DECISION",
    "MALFORMED_PROFILE_FAIL_CLOSED",
    "MALFORMED_RULE_FAIL_CLOSED",
}


def _json_safe(value: Any) -> Any:
    if is_dataclass(value):
        return _json_safe(asdict(value))
    if isinstance(value, tuple):
        return [_json_safe(item) for item in value]
    if isinstance(value, list):
        return [_json_safe(item) for item in value]
    if isinstance(value, dict):
        return {str(key): _json_safe(item) for key, item in value.items()}
    return value


def _validated_cases(summary: Dict[str, Any]) -> tuple[Dict[str, Dict[str, Any]], tuple[str, ...]]:
    raw_cases = summary.get("cases")
    if raw_cases is None:
        return {}, ("cases_missing",)
    if not isinstance(raw_cases, list):
        return {}, ("cases_wrong_type",)
    if not raw_cases:
        return {}, ("cases_empty",)
    cases: Dict[str, Dict[str, Any]] = {}
    errors: List[str] = []
    for index, item in enumerate(raw_cases):
        if not isinstance(item, dict):
            errors.append(f"case_{index}_wrong_type")
            continue
        case_id = item.get("case_id")
        if not isinstance(case_id, str) or not case_id.strip():
            errors.append(f"case_{index}_identity_missing")
            continue
        if case_id in cases:
            errors.append(f"duplicate_case_id:{case_id}")
            continue
        cases[case_id] = item
    return cases, tuple(errors)


def _independent_expected() -> Dict[str, Any]:
    return {
        case["case_id"]: _json_safe(case["expected"])
        for case in build_governance_backbone_cases_v1()
    }


def _independent_determinism(case_id: str) -> Dict[str, Any]:
    case = next(case for case in build_governance_backbone_cases_v1() if case["case_id"] == case_id)
    payload = case["payload"]
    if case_id == "DETERMINISTIC_RULE_RESOLUTION":
        profile, registry = payload
        first = resolve_applicable_governance_set(profile, registry)
        second = resolve_applicable_governance_set(profile, registry)
        first_safe = _json_safe(first)
        second_safe = _json_safe(second)
        return {"first": first_safe, "second": second_safe, "deterministic": first_safe == second_safe}
    decision_inputs = {key: value for key, value in payload.items() if key != "runner_status"}
    first = compute_unified_final_decision(**decision_inputs)
    second = compute_unified_final_decision(**decision_inputs)
    return {"first": first, "second": second, "deterministic": first == second}


def _run_checks(summary: Dict[str, Any]) -> List[Dict[str, Any]]:
    cases, case_errors = _validated_cases(summary)
    independent_expected = _independent_expected()
    checks: List[Dict[str, Any]] = []

    def check(check_id: str, passed: bool, detail: str = "") -> None:
        checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail})

    check("required_cases_present", not case_errors and REQUIRED_CASES.issubset(cases), "all 35 core cases")
    check("controlled_marker", summary.get("source_mode") == "CONTROLLED_GOVERNANCE_VERIFICATION_BACKBONE")
    check("protocol_manager_owner", summary.get("canonical_owner") == "Protocol Manager")
    check("protocol_manager_reused", summary.get("protocol_manager_reused") is True)
    check("permission_assets_reused", summary.get("permission_admission_assets_reused") is True)
    check("no_new_governance_owner", summary.get("new_governance_super_owner_created") is False)
    check("constitutional_sources_present", all(summary.get(key) for key in ("constitution_source_ref", "protocol_source_ref", "architecture_source_ref")))
    for key in (
        "runtime_execution", "provider_invocation", "model_invocation", "gateway_invocation",
        "world_mutation", "truth_mutation", "resource_allocation", "slot_reservation",
        "capability_activation", "decision_formed", "task_formed", "action_formed",
        "database_used", "ui_used", "dynamic_rule_loading", "llm_rule_inference", "fuzzy_rule_matching",
    ):
        check(f"negative_guard:{key}", summary.get(key) is False)
    check("rule_registry_present", bool(summary.get("governance_rule_registry", {}).get("rules")))
    required_rule_refs = {
        "RULE_GOVERNED_EXECUTION",
        "AUTHORITY_RESPONSIBILITY_UNITY",
        "NO_AUTHORITY_WITHOUT_RESPONSIBILITY",
        "NO_RESPONSIBILITY_WITHOUT_AUTHORITY",
        "OWNER_BOUNDARY_REQUIRED",
        "CANDIDATE_IS_NOT_AUTHORITY",
        "NO_TRUTH_WITHOUT_TRUTH_AUTHORITY",
        "NO_RUNTIME_WITHOUT_RUNTIME_AUTHORITY",
        "REQUESTER_OWNS_REQUIREMENT_COMPLEXITY",
        "EXECUTOR_OWNS_EXECUTION_COMPLEXITY",
        "FAILURE_RESPONSIBILITY_FOLLOWS_AUTHORITY",
        "ADAPTER_HAS_NO_SEMANTIC_AUTHORITY",
    }
    registered_rule_refs = {
        item.get("rule_ref")
        for item in summary.get("governance_rule_registry", {}).get("rules", [])
    }
    check("core_rules_present", required_rule_refs.issubset(registered_rule_refs))
    check("common_profiles_present", len(summary.get("common_profiles", [])) >= 8)
    check("provider_reference_candidate_only", summary.get("provider_binding_preparation_reference", {}).get("candidate_only") is True)
    check("provider_preparation_has_no_binding_authority", summary.get("provider_binding_preparation_reference", {}).get("provider_binding_authority_declared") is False)
    check("provider_reference_no_runtime", all(summary.get("provider_binding_preparation_reference", {}).get(key) is False for key in ("runtime_allocated", "execution_instance_created", "provider_session_started", "gateway_submission", "runtime_started", "resource_allocated")))
    check("provider_reference_no_truth", summary.get("provider_binding_preparation_reference", {}).get("truth_declared") is False and summary.get("provider_binding_preparation_reference", {}).get("world_truth_declared") is False)

    for case_id in REQUIRED_CASES:
        case = cases.get(case_id, {})
        expected = independent_expected.get(case_id) or {}
        result = case.get("result")
        result = result if isinstance(result, dict) else {}
        for key, expected_value in expected.items():
            if key == "error":
                actual_errors = json.dumps(
                    {
                        "errors": result.get("errors", []),
                        "profile_errors": result.get("profile_errors", []),
                        "authority_responsibility_errors": result.get("authority_responsibility_errors", []),
                        "protocol_errors": result.get("protocol_errors", []),
                        "applicable_validation_errors": (result.get("applicable_governance") or {}).get("validation_errors", []),
                    },
                    ensure_ascii=False,
                )
                passed = expected_value in actual_errors
            elif key == "errors":
                passed = tuple(result.get("errors", [])) == tuple(expected_value)
            elif key == "status":
                passed = result.get("status", result.get("formation_status")) == expected_value
            else:
                passed = result.get(key) == expected_value
            check(f"{case_id}:{key}", passed)

    deterministic = cases.get("DETERMINISTIC_RULE_RESOLUTION", {}).get("result", {})
    independent_rule = _independent_determinism("DETERMINISTIC_RULE_RESOLUTION")
    check("deterministic_rule_resolution_equal", deterministic == independent_rule)
    deterministic_decision = cases.get("DETERMINISTIC_FINAL_DECISION", {}).get("result", {})
    independent_decision = _independent_determinism("DETERMINISTIC_FINAL_DECISION")
    check("deterministic_final_decision_equal", deterministic_decision == independent_decision)
    waiting = cases.get("WAITING_STATUS_NOT_USED_AS_FINAL_DECISION", {}).get("result", {})
    check("runner_status_separate_from_final_decision", waiting.get("runner_status") == "WAITING_FOR_USER_TERMINAL_VERIFICATION" and waiting.get("final_decision") == "GO")
    return checks


def main() -> None:
    parser = argparse.ArgumentParser(description="Verify controlled governance backbone core rules.")
    parser.add_argument("--output-root", type=Path, default=OUTPUT_DIR)
    args = parser.parse_args()
    summary = json.loads((args.output_root / "runner_summary_v1.json").read_text(encoding="utf-8"))
    checks = _run_checks(summary)
    failed = [item["check_id"] for item in checks if not item["passed"]]
    functional_checks_passed = not failed
    contract_failures = failed
    governance_preflight = "PASS" if functional_checks_passed else "FAIL"
    governance_postflight = "PASS" if functional_checks_passed else "FAIL"
    cognitive_logic_result = "PASS" if functional_checks_passed else "FAIL"
    operational_result = "PASS" if functional_checks_passed else "FAIL"
    # The backbone helper is exercised by the controlled decision cases.  The
    # verifier retains the same aggregate inputs and only emits the final
    # decision after its own checks have completed.
    final_decision = compute_unified_final_decision(
        functional_checks_passed=functional_checks_passed,
        contract_failures=tuple(contract_failures),
        governance_preflight=governance_preflight,
        governance_postflight=governance_postflight,
        cognitive_logic_result=cognitive_logic_result,
        operational_result=operational_result,
    )
    report = {
        "phase": summary.get("phase"),
        "check_count": len(checks),
        "passed_count": len(checks) - len(failed),
        "failed_checks": failed,
        "contract_failures": contract_failures,
        "all_checks_passed": functional_checks_passed,
        "governance_preflight": governance_preflight,
        "governance_postflight": governance_postflight,
        "cognitive_logic_result": cognitive_logic_result,
        "operational_result": operational_result,
        "final_decision": final_decision,
        "status": "VERIFIED_ARTIFACT_RESULT",
        "runner_status": summary.get("status"),
        "cognitive_logic_observations": [],
        "checks": checks,
    }
    args.output_root.mkdir(parents=True, exist_ok=True)
    (args.output_root / "verification_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    raise SystemExit(0 if not failed else 1)


if __name__ == "__main__":
    main()
