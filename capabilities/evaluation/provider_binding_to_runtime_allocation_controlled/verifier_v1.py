"""Verifier for the controlled Provider Binding → Runtime Preparation seam."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from capabilities.midplatform.protocol_manager.module.governance_verification_backbone_v1 import (
    compute_unified_final_decision,
)

from .fixtures_v1 import build_provider_binding_to_runtime_allocation_cases_v1


SUMMARY_PATH = Path("_eval_out/provider_binding_to_runtime_allocation_v1/runner_summary_v1.json")


def _check(checks: dict[str, bool], name: str, value: bool) -> None:
    checks[name] = bool(value)


def _case_map(summary: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {item["case_id"]: item for item in summary.get("cases", ())}


def verify(summary: dict[str, Any]) -> dict[str, Any]:
    checks: dict[str, bool] = {}
    expected_cases = build_provider_binding_to_runtime_allocation_cases_v1()
    actual = _case_map(summary)
    _check(checks, "required_cases_present", {case.case_id for case in expected_cases} <= set(actual))
    _check(checks, "controlled_marker", summary.get("source_mode") == "CONTROLLED_PROVIDER_BINDING_TO_RUNTIME_ALLOCATION")
    _check(checks, "governance_backbone_reused", summary.get("governance_backbone_reused") is True)
    _check(checks, "provider_owner_reused", summary.get("canonical_provider_binding_owner") == "Provider Governance")
    _check(checks, "runtime_owner_reused", summary.get("canonical_runtime_owner") == "Runtime Executor")
    _check(checks, "candidate_only", summary.get("candidate_only") is True)
    _check(checks, "read_only", summary.get("read_only") is True)
    _check(checks, "no_provider_binding", summary.get("provider_binding_decision_formed") is False and summary.get("provider_bound") is False)
    _check(checks, "no_runtime_allocation", summary.get("runtime_allocated") is False and summary.get("resource_allocated") is False)
    _check(checks, "no_execution_instance", summary.get("execution_instance_created") is False)
    _check(checks, "no_session_or_gateway", summary.get("provider_session_started") is False and summary.get("gateway_submission") is False)
    _check(checks, "no_provider_or_model_invocation", summary.get("provider_invocation") is False and summary.get("model_invocation") is False)
    _check(checks, "no_truth", summary.get("truth_declared") is False and summary.get("world_truth_declared") is False)
    _check(checks, "requester_executor_boundary", summary.get("requester_owns_requirement_complexity") is True and summary.get("executor_owns_execution_complexity") is True)
    _check(checks, "preflight_before_business_engine", summary.get("preflight_before_business_engine") is True)

    for case in expected_cases:
        item = actual.get(case.case_id, {})
        binding = item.get("binding") or {}
        allocation = item.get("allocation") or {}
        execution = item.get("execution_instance_preparation") or {}
        expected = item.get("expected") or {}
        preflight = item.get("governance_preflight") or {}
        postflight = item.get("governance_postflight") or {}
        if item.get("business_engine_executed") is False:
            _check(checks, f"{case.case_id}:preflight_blocked", preflight.get("status") == "GOVERNANCE_PREFLIGHT_BLOCKED")
            _check(checks, f"{case.case_id}:business_not_executed", item.get("business_engine_executed") is False)
            _check(checks, f"{case.case_id}:no_business_output", not binding and not allocation and not execution)
        else:
            _check(checks, f"{case.case_id}:preflight_pass", preflight.get("status") == "PASS")
            _check(checks, f"{case.case_id}:applicable_rules_resolved", bool((item.get("applicable_governance") or {}).get("resolved_rule_refs")))
            _check(checks, f"{case.case_id}:binding_status", binding.get("formation_status") == case.expected_binding_status)
            _check(checks, f"{case.case_id}:binding_count", len(binding.get("candidates", ())) == case.expected_binding_count)
            _check(checks, f"{case.case_id}:allocation_status", allocation.get("formation_status", case.expected_allocation_status) == case.expected_allocation_status)
            _check(checks, f"{case.case_id}:allocation_count", len(allocation.get("candidates", ())) == case.expected_allocation_count)
            _check(checks, f"{case.case_id}:execution_status", execution.get("formation_status", case.expected_execution_status) == case.expected_execution_status)
            _check(checks, f"{case.case_id}:execution_count", len(execution.get("candidates", ())) == case.expected_execution_count)
        if case.postflight_artifact is not None or case.failure_ownership_payload is not None:
            _check(checks, f"{case.case_id}:postflight_present", bool(postflight))
        if case.expected_owner and case.case_id != "RESPONSIBILITY_LAUNDERING_BLOCKED":
            _check(
                checks,
                f"{case.case_id}:failure_owner",
                not item.get("failure_ownership_errors")
                and (
                    (case.failure_ownership_payload or {}).get("failure_owner_ref")
                    == case.expected_owner
                ),
            )

    single = actual.get("SINGLE_PROVIDER_BINDING_CANDIDATE", {})
    _check(checks, "single_provider_candidate", len((single.get("binding") or {}).get("candidates", ())) == 1)
    multiple = actual.get("MULTIPLE_PROVIDER_BINDING_CANDIDATES", {})
    multiple_refs = {(item.get("provider_candidate_ref")) for item in (multiple.get("binding") or {}).get("candidates", ())}
    _check(checks, "multiple_provider_candidates_all_retained", len(multiple_refs) == 2)
    same_class = actual.get("SAME_CLASS_DISTINCT_PROVIDERS", {})
    same_class_candidates = (same_class.get("binding") or {}).get("candidates", ())
    _check(checks, "same_provider_class_not_deduplicated", len(same_class_candidates) == 2 and len({item.get("provider_candidate_ref") for item in same_class_candidates}) == 2)
    shared = actual.get("SAME_PROVIDER_MULTI_DEMAND", {})
    _check(checks, "same_provider_multi_demand_not_merged", len({item.get("source_observation_demand_ref") for item in (shared.get("binding") or {}).get("candidates", ())}) == 2)
    provider_only = actual.get("PROVIDER_ONLY_NO_MODEL", {})
    _check(checks, "provider_only_no_model", all(item.get("source_model_ref") is None for item in (provider_only.get("binding") or {}).get("candidates", ())))
    _check(checks, "provider_not_eligible_stays_provider_owned", (actual.get("PROVIDER_NOT_ELIGIBLE", {}).get("failure_ownership_payload") or {}).get("provider_eligible") is False if actual.get("PROVIDER_NOT_ELIGIBLE") else False)
    explicit_model = actual.get("EXPLICIT_MODEL_CARRY_FORWARD", {})
    _check(checks, "explicit_model_carry_forward", {item.get("source_model_ref") for item in (explicit_model.get("binding") or {}).get("candidates", ())} == {"model:controlled:explicit"})
    runtime = actual.get("RUNTIME_REQUIREMENT_PREPARATION", {})
    runtime_candidates = (runtime.get("allocation") or {}).get("candidates", ())
    _check(checks, "runtime_requirement_preparation", len(runtime_candidates) == 1 and bool(runtime_candidates[0].get("runtime_requirement_refs")))
    _check(checks, "no_concrete_resource_allocation", all(not item.get("resource_allocation") for item in runtime_candidates))
    execution_case = actual.get("EXECUTION_INSTANCE_PREPARATION_ONLY", {})
    execution_candidates = (execution_case.get("execution_instance_preparation") or {}).get("candidates", ())
    _check(checks, "execution_instance_preparation_only", len(execution_candidates) == 1 and execution_candidates[0].get("execution_instance_created") is False)
    _check(checks, "scenario12_abstract", all("ocr" not in json.dumps(actual.get(case_id, {})).lower() and "vlm" not in json.dumps(actual.get(case_id, {})).lower() for case_id in ("SCENARIO12_SIGNAGE", "SCENARIO12_HUMAN_FLOW", "SCENARIO12_INDEPENDENT_BINDING_PATHS")))
    _check(checks, "scenario12_independent_paths", len((actual.get("SCENARIO12_INDEPENDENT_BINDING_PATHS", {}).get("binding") or {}).get("candidates", ())) == 2)
    malformed = actual.get("MALFORMED_INPUT_FAIL_CLOSED", {})
    _check(checks, "malformed_input_fails_closed", (malformed.get("governance_preflight") or {}).get("status") == "PASS" and (malformed.get("binding") or {}).get("formation_status") == "INVALID_INPUT")
    _check(checks, "authority_laundering_blocked", "candidate_authoritative_effect" in (actual.get("AUTHORITY_LAUNDERING_BLOCKED", {}).get("governance_postflight") or {}).get("blocker_refs", ()))
    _check(checks, "responsibility_laundering_blocked", bool((actual.get("RESPONSIBILITY_LAUNDERING_BLOCKED", {}).get("failure_ownership_errors") or ())))
    _check(checks, "no_applicable_rules_fail_closed", (actual.get("NO_APPLICABLE_RULES_FAIL_CLOSED", {}).get("governance_preflight") or {}).get("status") == "GOVERNANCE_PREFLIGHT_BLOCKED")
    _check(checks, "upstream_snapshots_unchanged", all(item.get("request_snapshot_before") == item.get("request_snapshot_after") for item in actual.values()))
    deterministic = actual.get("DETERMINISTIC_REPLAY", {})
    _check(checks, "deterministic_replay", (deterministic.get("binding") or {}).get("provider_binding_candidate_refs") == (deterministic.get("deterministic_replay") or {}).get("provider_binding_candidate_refs") and (deterministic.get("binding") or {}).get("formation_status") == (deterministic.get("deterministic_replay") or {}).get("formation_status"))

    functional = all(checks.values())
    governance_preflight = "PASS" if (
        (actual.get("GOVERNANCE_PREFLIGHT_REQUIRED", {}).get("governance_preflight") or {}).get("status") == "PASS"
        and all(
            ((actual.get(case.case_id, {}).get("governance_preflight") or {}).get("status") == "PASS")
            or actual.get(case.case_id, {}).get("business_engine_executed") is False
            for case in expected_cases
        )
    ) else "GOVERNANCE_PREFLIGHT_BLOCKED"
    governance_postflight = "PASS" if (
        (actual.get("GOVERNANCE_POSTFLIGHT_REQUIRED", {}).get("governance_postflight") or {}).get("status") == "PASS"
    ) else "GOVERNANCE_POSTFLIGHT_BLOCKED"
    contract_failures = tuple(name for name, passed in checks.items() if not passed)
    final_decision = compute_unified_final_decision(
        functional_checks_passed=functional,
        contract_failures=contract_failures,
        governance_preflight=governance_preflight,
        governance_postflight=governance_postflight,
        cognitive_logic_result="PASS" if functional else "FAIL",
        operational_result="PASS" if functional else "FAIL",
    )
    return {
        "check_count": len(checks),
        "passed_count": sum(1 for passed in checks.values() if passed),
        "failed_checks": [name for name, passed in checks.items() if not passed],
        "all_checks_passed": functional,
        "governance_preflight": governance_preflight,
        "governance_postflight": governance_postflight,
        "cognitive_logic_result": "PASS" if functional else "FAIL",
        "operational_result": "PASS" if functional else "FAIL",
        "contract_failures": list(contract_failures),
        "final_decision": final_decision,
        "status": "VERIFIED_ARTIFACT_RESULT",
    }


def main() -> int:
    summary = json.loads(SUMMARY_PATH.read_text(encoding="utf-8"))
    result = verify(summary)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["final_decision"] == "GO" else 1


if __name__ == "__main__":
    raise SystemExit(main())
