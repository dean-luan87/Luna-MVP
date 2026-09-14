"""Controlled verifier for Runtime Grant pre-execution authorization."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from capabilities.midplatform.permission_and_admission_manager.module.runtime_execution_grant_v1 import (
    AUTHORITY_REF,
    OWNER,
    RESPONSIBILITY_REF,
)
from capabilities.midplatform.protocol_manager.module.governance_verification_backbone_v1 import (
    compute_unified_final_decision,
)

from .fixtures_v1 import PHASE, build_runtime_grant_cases_v1


OUTPUT_DIR = Path("_eval_out/runtime_grant_pre_execution_authorization_v1")


def _case_map(summary: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {item.get("case_id"): item for item in summary.get("cases", ())}


def _check(checks: dict[str, bool], name: str, value: bool) -> None:
    checks[name] = bool(value)


def verify(summary: dict[str, Any]) -> dict[str, Any]:
    cases = build_runtime_grant_cases_v1()
    actual = _case_map(summary)
    checks: dict[str, bool] = {}
    _check(checks, "required_cases_present", {case.case_id for case in cases} <= set(actual))
    _check(checks, "phase", summary.get("phase") == PHASE)
    _check(
        checks,
        "controlled_marker",
        summary.get("source_mode") == "controlled_runtime_grant_pre_execution_authorization",
    )
    _check(checks, "permission_owner_reused", summary.get("canonical_runtime_grant_owner") == OWNER)
    _check(checks, "permission_manager_reused", summary.get("permission_admission_manager_reused") is True)
    _check(checks, "runtime_executor_reused", summary.get("runtime_executor_reused") is True)
    _check(checks, "protocol_manager_reused", summary.get("protocol_manager_reused") is True)
    _check(checks, "no_new_grant_owner", summary.get("new_runtime_grant_owner_created") is False)
    _check(checks, "no_new_governance_owner", summary.get("new_governance_super_owner_created") is False)
    _check(checks, "grant_authority", summary.get("runtime_execution_authorization_authority") == AUTHORITY_REF)
    _check(checks, "grant_responsibility", summary.get("runtime_execution_authorization_responsibility") == RESPONSIBILITY_REF)
    _check(checks, "grant_is_authoritative", summary.get("runtime_execution_grant_authoritative") is True and summary.get("runtime_execution_grant_candidate_only") is False)
    _check(checks, "grant_decision_formed_at_authorization_boundary", summary.get("runtime_execution_grant_decision_formed") is True)
    _check(checks, "provider_binding_remains_candidate", summary.get("provider_binding_candidate_formed") is True and summary.get("provider_binding_decision_formed") is False and summary.get("provider_bound") is False)
    _check(checks, "requester_executor_boundary", summary.get("requester_owns_requirement_complexity") is True and summary.get("executor_owns_execution_complexity") is True)

    for key in (
        "runtime_allocated",
        "execution_instance_created",
        "provider_session_started",
        "gateway_submission",
        "provider_invoked",
        "model_invoked",
        "capability_activated",
        "slot_reserved",
        "resource_allocated",
        "runtime_started",
        "runtime_admission_executed",
        "truth_declared",
        "world_truth_declared",
        "provider_selected",
        "model_selected",
        "semantic_rewrite",
        "attention_formed",
        "decision_formed",
        "task_formed",
        "action_formed",
        "current_world_mutation",
        "field_mutation",
        "memory_pcn_mutation",
    ):
        _check(checks, f"negative_guard:{key}", summary.get(key) is False)

    for case in cases:
        item = actual.get(case.case_id, {})
        expected = item.get("expected") or {}
        grant = item.get("grant") or {}
        decisions = grant.get("decisions") or []
        preflight = item.get("governance_preflight") or {}
        postflight = item.get("governance_postflight") or {}
        _check(checks, f"{case.case_id}:expected_status", expected.get("status") == case.expected_status)
        _check(checks, f"{case.case_id}:expected_decision", expected.get("decision") == case.expected_decision)
        _check(checks, f"{case.case_id}:expected_count", expected.get("count") == case.expected_count)
        _check(checks, f"{case.case_id}:preflight_present", bool(preflight))
        if preflight.get("status") == "PASS":
            _check(checks, f"{case.case_id}:applicable_rules", bool((item.get("applicable_governance") or {}).get("resolved_rule_refs")))
            _check(checks, f"{case.case_id}:business_executed", item.get("business_engine_executed") is True)
        else:
            _check(checks, f"{case.case_id}:business_blocked", item.get("business_engine_executed") is False)
        if case.expected_decision is None:
            _check(checks, f"{case.case_id}:no_decision_on_block", not decisions)
            _check(
                checks,
                f"{case.case_id}:formation_fail_closed",
                item.get("pipeline_status") == "INVALID_INPUT"
                or preflight.get("status") == "GOVERNANCE_PREFLIGHT_BLOCKED",
            )
        else:
            _check(checks, f"{case.case_id}:decision_count", len(decisions) == case.expected_count)
            _check(checks, f"{case.case_id}:formation_status", grant.get("formation_status") == case.expected_status)
            if decisions:
                _check(checks, f"{case.case_id}:decision_value", decisions[0].get("decision") == case.expected_decision)
                _check(checks, f"{case.case_id}:decision_authoritative", decisions[0].get("authoritative") is True and decisions[0].get("candidate_only") is False)
                _check(checks, f"{case.case_id}:decision_nontruth", decisions[0].get("truth_declared") is False and decisions[0].get("world_truth_declared") is False)
                _check(checks, f"{case.case_id}:decision_no_execution", all(decision.get(key) is False for decision in decisions for key in ("runtime_allocated", "execution_instance_created", "provider_session_started", "gateway_submission", "provider_invoked", "model_invoked")))
        if case.case_id == "AUTHORIZED_NOT_EXECUTED":
            _check(checks, "authorized_not_executed", decisions and decisions[0].get("execution_authorized") is True and decisions[0].get("execution_instance_created") is False)
        if case.case_id == "AUTHORITY_LAUNDERING_BLOCKED":
            _check(checks, "authority_laundering_blocked", "candidate_authoritative_effect" in postflight.get("blocker_refs", ()))
        if case.case_id == "RESPONSIBILITY_LAUNDERING_BLOCKED":
            _check(checks, "responsibility_laundering_blocked", "RESPONSIBILITY_LAUNDERING" in item.get("failure_ownership_errors", ()))
        if case.case_id == "NO_APPLICABLE_RULES_FAIL_CLOSED":
            _check(checks, "no_applicable_rules_fail_closed", preflight.get("status") == "GOVERNANCE_PREFLIGHT_BLOCKED" and item.get("business_engine_executed") is False)
        if case.case_id == "MALFORMED_INPUT_FAIL_CLOSED":
            _check(checks, "malformed_input_fail_closed", item.get("pipeline_status") == "INVALID_INPUT" and item.get("business_engine_executed") is True)

    for case_id in ("PROVIDER_BINDING_DENIED", "PERMISSION_DENIED", "SAFETY_DENIED", "CONSTITUTION_BLOCKS_EXECUTION", "RUNTIME_BOUNDARY_INVALID", "EXECUTION_READY_NOT_AUTHORIZED", "RESOURCE_AVAILABLE_NOT_EQUAL_GRANT"):
        item = actual.get(case_id, {})
        decisions = (item.get("grant") or {}).get("decisions") or []
        _check(checks, f"{case_id}:blocked_not_started", decisions and decisions[0].get("execution_authorized") is False)

    for case_id in ("SCENARIO12_SIGNAGE", "SCENARIO12_HUMAN_FLOW"):
        _check(checks, f"{case_id}:abstract", all(token not in json.dumps(actual.get(case_id, {})).lower() for token in ("ocr", "vlm", "yolo", "slam", "camera")))
    scenario12 = (actual.get("SCENARIO12_BOTH", {}).get("grant") or {}).get("decisions") or []
    _check(checks, "scenario12_independent_grants", len(scenario12) == 2 and len({item.get("source_observation_demand_ref") for item in scenario12}) == 2)
    _check(checks, "scenario12_no_provider_selection", summary.get("provider_selected") is False and summary.get("model_selected") is False)

    _check(checks, "resource_available_not_grant", ((actual.get("RESOURCE_AVAILABLE_NOT_EQUAL_GRANT", {}).get("grant") or {}).get("decisions") or [{}])[0].get("decision") == "DENIED")
    _check(checks, "fpo_continuation_not_grant", ((actual.get("FPO_CONTINUATION_NOT_EQUAL_GRANT", {}).get("grant") or {}).get("decisions") or [{}])[0].get("decision") == "DENIED")
    _check(checks, "gateway_admission_not_grant", ((actual.get("GATEWAY_ADMISSION_NOT_EQUAL_GRANT", {}).get("grant") or {}).get("decisions") or [{}])[0].get("decision") == "GRANTED")
    _check(checks, "provider_binding_not_grant", ((actual.get("PROVIDER_BINDING_NOT_EQUAL_GRANT", {}).get("grant") or {}).get("decisions") or [{}])[0].get("decision") == "DENIED")
    _check(checks, "model_optional", all(item.get("source_model_ref") is None for item in (actual.get("COMPLETE_REQUEST_READY_FOR_AUTHORIZATION", {}).get("binding") or {}).get("candidates", ())))
    _check(checks, "no_execution_instance_identity", summary.get("execution_instance_created") is False)
    _check(checks, "no_gateway_submission", summary.get("gateway_submission") is False)
    snapshot_pairs = (
        (key, item.get(f"{key}_snapshot_before"), item.get(f"{key}_snapshot_after"))
        for item in actual.values()
        for key in ("target_request", "binding_request", "allocation_request", "execution_request", "grant_request")
        if item.get(f"{key}_snapshot_before") is not None
    )
    _check(checks, "upstream_snapshots_unchanged", all(before == after for _, before, after in snapshot_pairs))
    deterministic = actual.get("DETERMINISTIC_DECISION", {}).get("deterministic_replay") or {}
    _check(checks, "deterministic_decision", deterministic.get("deterministic") is True)
    _check(checks, "failure_owner_permission", ((actual.get("FAILURE_OWNER_PERMISSION", {}).get("grant") or {}).get("decisions") or [{}])[0].get("failure_owner_ref") == OWNER)
    _check(checks, "failure_owner_provider", ((actual.get("FAILURE_OWNER_PROVIDER", {}).get("grant") or {}).get("decisions") or [{}])[0].get("failure_owner_ref") == "Provider Governance")
    _check(checks, "failure_owner_runtime_grant", ((actual.get("FAILURE_OWNER_RUNTIME_GRANT", {}).get("grant") or {}).get("decisions") or [{}])[0].get("failure_owner_ref") == OWNER)
    _check(checks, "failure_owner_resource", ((actual.get("FAILURE_OWNER_RESOURCE", {}).get("grant") or {}).get("decisions") or [{}])[0].get("failure_owner_ref") == "Resource Governance")

    functional = all(checks.values())
    preflight_status = "PASS" if functional else "GOVERNANCE_PREFLIGHT_BLOCKED"
    postflight_status = "PASS" if functional else "GOVERNANCE_POSTFLIGHT_BLOCKED"
    contract_failures = tuple(name for name, passed in checks.items() if not passed)
    final_decision = compute_unified_final_decision(
        functional_checks_passed=functional,
        contract_failures=contract_failures,
        governance_preflight=preflight_status,
        governance_postflight=postflight_status,
        cognitive_logic_result="PASS" if functional else "FAIL",
        operational_result="PASS" if functional else "FAIL",
    )
    return {
        "phase": summary.get("phase"),
        "check_count": len(checks),
        "passed_count": sum(1 for value in checks.values() if value),
        "failed_checks": [name for name, passed in checks.items() if not passed],
        "contract_failures": list(contract_failures),
        "all_checks_passed": functional,
        "governance_preflight": preflight_status,
        "governance_postflight": postflight_status,
        "cognitive_logic_result": "PASS" if functional else "FAIL",
        "operational_result": "PASS" if functional else "FAIL",
        "final_decision": final_decision,
        "status": "VERIFIED_ARTIFACT_RESULT",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify controlled Runtime Grant authorization.")
    parser.add_argument("--output-root", type=Path, default=OUTPUT_DIR)
    args = parser.parse_args()
    summary = json.loads((args.output_root / "runner_summary_v1.json").read_text(encoding="utf-8"))
    result = verify(summary)
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result["final_decision"] == "GO" else 1


if __name__ == "__main__":
    raise SystemExit(main())
