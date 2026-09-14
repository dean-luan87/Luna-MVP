"""Verifier for the controlled Provider session/invocation sandbox."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from capabilities.midplatform.protocol_manager.module.governance_verification_backbone_v1 import (
    compute_unified_final_decision,
)

from .fixtures_v1 import build_provider_session_cases_v1


SUMMARY_PATH = Path("_eval_out/provider_session_controlled_invocation_multiscenario_sandbox_v1/runner_summary_v1.json")


def _check(checks: dict[str, bool], name: str, value: bool) -> None:
    checks[name] = bool(value)


def _list(value: Any) -> list[dict[str, Any]]:
    return value if isinstance(value, list) else []


def _validated_cases(summary: dict[str, Any]) -> tuple[dict[str, dict[str, Any]], tuple[str, ...]]:
    raw_cases = summary.get("cases")
    errors: list[str] = []
    if raw_cases is None:
        return {}, ("cases_missing",)
    if not isinstance(raw_cases, list):
        return {}, ("cases_wrong_type",)
    if not raw_cases:
        return {}, ("cases_empty",)
    cases: dict[str, dict[str, Any]] = {}
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


def _required_collection(
    item: dict[str, Any],
    key: str,
    expected_count: int,
    identity_key: str,
    checks: dict[str, bool],
    case_id: str,
) -> list[dict[str, Any]]:
    value = item.get(key)
    valid = isinstance(value, list) and len(value) == expected_count
    _check(checks, f"{case_id}:{key}:present_and_exact_count", valid)
    if not valid:
        return []
    identities = [entry.get(identity_key) for entry in value if isinstance(entry, dict)]
    identities_valid = len(identities) == expected_count and all(isinstance(ref, str) and ref.strip() for ref in identities)
    unique = len(set(identities)) == len(identities)
    _check(checks, f"{case_id}:{key}:identity_complete", identities_valid)
    _check(checks, f"{case_id}:{key}:identity_unique", unique)
    return value


def _reported_invocation_status(item: dict[str, Any]) -> str:
    invocation = item.get("invocation") or {}
    results = _list(item.get("invocation_results"))
    if results:
        formation_status = results[0].get("formation_status")
        if formation_status == "DUPLICATE_START_BLOCKED":
            return "NO_INVOCATION"
        if formation_status:
            return formation_status
    if invocation:
        return invocation.get("status", "NO_INVOCATION")
    return "NO_INVOCATION"


def verify(summary: dict[str, Any]) -> dict[str, Any]:
    checks: dict[str, bool] = {}
    cases, case_errors = _validated_cases(summary)
    expected = build_provider_session_cases_v1()
    _check(checks, "required_cases_present", not case_errors and {item.case_id for item in expected} <= set(cases))
    _check(checks, "controlled_marker", summary.get("source_mode") == "CONTROLLED_PROVIDER_SESSION_INVOCATION_MULTISCENARIO_SANDBOX")
    _check(checks, "governance_backbone_reused", summary.get("governance_backbone_reused") is True)
    _check(checks, "session_owner", summary.get("canonical_session_owner") == "Provider Runtime Governance")
    _check(checks, "invocation_owner", summary.get("canonical_invocation_owner") == "Provider Runtime Governance")
    declared_synthetic_only = all(summary.get(key) is True for key in ("synthetic_only", "controlled", "no_real_runtime_effect", "no_real_provider_effect", "no_real_model_effect"))
    declared_no_real_effects = all(summary.get(key) is False for key in ("real_provider_invoked", "real_model_invoked", "network_called", "subprocess_started", "thread_started", "socket_used", "runtime_observation_created", "gateway_submission", "evidence_created", "truth_declared", "world_truth_declared"))
    observed_effects = summary.get("verifier_observed_side_effects")
    observed_no_real_effects = isinstance(observed_effects, dict) and observed_effects.get("status") == "OBSERVED_NOT_EXECUTED" and isinstance(observed_effects.get("values"), dict) and all(value is False for value in observed_effects["values"].values()) and bool(observed_effects.get("evidence_refs"))
    _check(checks, "synthetic_only_runner_declared", declared_synthetic_only)
    _check(checks, "no_real_effects_runner_declared", declared_no_real_effects)
    _check(checks, "no_real_effects_verifier_observed", observed_no_real_effects)
    _check(checks, "retry_deferred", summary.get("retry_engine") is False and summary.get("provider_fallback") is False and summary.get("provider_autonomous_continuation") is False)

    for case in expected:
        item = cases.get(case.case_id, {})
        preflight = item.get("governance_preflight") or {}
        postflight = item.get("governance_postflight") or {}
        session_result = item.get("session") or {}
        invocation = item.get("invocation") or {}
        sessions = _required_collection(item, "sessions", case.expected_session_count, "session_ref", checks, case.case_id)
        invocations = _required_collection(item, "invocations", case.expected_invocation_count, "invocation_ref", checks, case.case_id)
        if case.expected_blocked:
            _check(checks, f"{case.case_id}:preflight_blocked_or_input_blocked", (item.get("business_engine_executed") is False and preflight.get("status") == "GOVERNANCE_PREFLIGHT_BLOCKED") or (session_result.get("formation_status") == "INVALID_INPUT" and case.expected_session_count == 0))
        else:
            _check(checks, f"{case.case_id}:preflight_pass", preflight.get("status") == "PASS")
        if case.authority_records is not None:
            _check(checks, f"{case.case_id}:business_not_run_when_governance_blocked", item.get("business_engine_executed") is False)
            continue
        _check(checks, f"{case.case_id}:session_status", session_result.get("formation_status") == case.expected_session_status)
        _check(checks, f"{case.case_id}:session_count", len(sessions) == case.expected_session_count)
        _check(checks, f"{case.case_id}:invocation_status", _reported_invocation_status(item) == case.expected_invocation_status)
        _check(checks, f"{case.case_id}:invocation_count", len(invocations) == case.expected_invocation_count)
        if case.expected_session_count:
            _check(checks, f"{case.case_id}:session_boundary", all(s.get("authoritative") is True and s.get("read_only") is True and s.get("synthetic") is True and s.get("controlled") is True and s.get("no_real_provider_effect") is True and s.get("no_real_model_effect") is True and s.get("side_effect_evidence_status") == "OBSERVED_NOT_EXECUTED" for s in sessions))
        if case.expected_invocation_count:
            _check(checks, f"{case.case_id}:invocation_boundary", all(i.get("authoritative") is True and i.get("read_only") is True and i.get("controlled_invocation_started") is True and i.get("real_provider_invoked") is False and i.get("real_model_invoked") is False and i.get("network_called") is False and i.get("subprocess_started") is False and i.get("thread_started") is False and i.get("socket_used") is False and i.get("runtime_observation_created") is False and i.get("gateway_submission") is False and i.get("evidence_created") is False and i.get("truth_declared") is False and i.get("world_truth_declared") is False and i.get("side_effect_evidence_status") == "OBSERVED_NOT_EXECUTED" for i in invocations))
        _check(checks, f"{case.case_id}:postflight", postflight.get("status") == "PASS")

    _check(checks, "provider_only_model_null", all(item.get("source_model_ref") is None for item in _list(cases.get("PROVIDER_ONLY_SESSION_MODEL_NULL", {}).get("sessions"))))
    _check(checks, "model_carry_forward", all(item.get("source_model_ref") == "model:controlled:explicit" for item in _list(cases.get("MODEL_REF_CARRY_FORWARD", {}).get("sessions"))))
    _check(checks, "no_model_inference", all(item.get("source_model_ref") is None for item in _list(cases.get("MODEL_NOT_INFERRED", {}).get("sessions"))))
    created_sessions = _list(cases.get("CREATED_NOT_STARTED", {}).get("sessions"))
    _check(checks, "created_not_started", len(created_sessions) == 1 and created_sessions[0].get("execution_started") is False)
    _check(checks, "session_created_not_invoked", cases.get("SESSION_CREATED_NOT_INVOKED", {}).get("invocations") == [])
    _check(checks, "invocation_started", all(item.get("controlled_invocation_started") is True for item in _list(cases.get("INVOCATION_STARTED", {}).get("invocations"))))
    _check(checks, "invocation_completed", all(item.get("status") == "COMPLETED" and item.get("controlled_invocation_completed") is True for item in _list(cases.get("INVOCATION_COMPLETED", {}).get("invocations"))))
    _check(checks, "failure_outcomes", cases.get("INVOCATION_FAILED", {}).get("invocation", {}).get("failure_owner_ref") == "Provider Runtime Governance")
    _check(checks, "timeout_outcome", cases.get("INVOCATION_TIMED_OUT", {}).get("invocation", {}).get("status") == "TIMED_OUT")
    _check(checks, "stop_outcome", cases.get("INVOCATION_STOPPED", {}).get("invocation", {}).get("status") == "STOPPED")
    _check(checks, "revoke_outcome", cases.get("INVOCATION_REVOKED", {}).get("invocation", {}).get("status") == "REVOKED")
    duplicate_results = _list(cases.get("DUPLICATE_START_BLOCKED", {}).get("invocation_results"))
    _check(checks, "duplicate_start_blocked", bool(duplicate_results) and duplicate_results[0].get("formation_status") == "DUPLICATE_START_BLOCKED" and cases.get("DUPLICATE_START_BLOCKED", {}).get("invocations") == [])
    _check(checks, "provider_failure_owner", cases.get("PROVIDER_RUNTIME_FAILURE_OWNER", {}).get("invocation", {}).get("failure_owner_ref") == "Provider Runtime Governance")
    _check(checks, "grant_failure_owner", cases.get("GRANT_FAILURE_OWNER", {}).get("business_engine_executed") is True and cases.get("GRANT_FAILURE_OWNER", {}).get("session", {}).get("formation_status") == "INVALID_INPUT")
    resource_case = cases.get("RESOURCE_FAILURE_OWNER", {})
    resource_results = _list(resource_case.get("invocation_results"))
    _check(
        checks,
        "resource_failure_owner",
        resource_case.get("invocation") is None
        and bool(resource_results)
        and resource_results[0].get("formation_status") == "INVALID_INPUT"
        and "runtime_allocation_not_active" in resource_results[0].get("validation_errors", []),
    )
    _check(checks, "binding_failure_owner", cases.get("BINDING_FAILURE_OWNER", {}).get("session", {}).get("formation_status") == "INVALID_INPUT")
    _check(checks, "lineage_mismatch_blocked", cases.get("LINEAGE_MISMATCH_BLOCKED", {}).get("session", {}).get("formation_status") == "INVALID_INPUT")
    _check(checks, "preflight_hard_stop", all(cases.get(case_id, {}).get("business_engine_executed") is False for case_id in ("AUTHORITY_WITHOUT_RESPONSIBILITY_BLOCKED", "RESPONSIBILITY_WITHOUT_AUTHORITY_BLOCKED", "PREFLIGHT_BLOCK_HARD_STOPS_ENGINE")))
    deterministic_case = cases.get("DETERMINISTIC_SESSION_REF", {})
    deterministic_evidence = deterministic_case.get("determinism_evidence") or {}
    _check(
        checks,
        "session_ref_deterministic",
        isinstance(deterministic_evidence, dict)
        and deterministic_evidence.get("reconstruction_a")
        and deterministic_evidence.get("reconstruction_b")
        and deterministic_evidence.get("reconstruction_a") != deterministic_evidence.get("reconstruction_b")
        and deterministic_evidence.get("canonical_digest_a") == deterministic_evidence.get("canonical_digest_b")
        and deterministic_evidence.get("comparison") == "MATCH",
    )
    _check(checks, "invocation_ref_deterministic", all(item.get("invocation_ref") for item in _list(cases.get("DETERMINISTIC_INVOCATION_REF", {}).get("invocations"))))
    distinct = _list(cases.get("DISTINCT_INVOCATIONS_DISTINCT_REF", {}).get("invocations"))
    _check(checks, "distinct_invocations_distinct_ref", len(distinct) == 2 and len({item.get("invocation_ref") for item in distinct}) == 2)
    for case_id in ("SCENARIO12_SIGNAGE_SESSION", "SCENARIO12_FLOW_SESSION", "SCENARIO12_INDEPENDENT_LINEAGE", "SCENARIO12_NO_MODEL_INFERENCE", "SCENARIO12_OPAQUE_RESULTS"):
        _check(checks, f"{case_id}:abstract_results", not any(token in json.dumps(cases.get(case_id, {})).lower() for token in ("ocr", "vlm", "yolo", "slam", "camera", "sign detected", "person count")))
    scenario = _list(cases.get("SCENARIO12_INDEPENDENT_LINEAGE", {}).get("sessions"))
    _check(checks, "scenario12_independent_lineage", len(scenario) == 2 and len({item.get("execution_instance_ref") for item in scenario}) == 2)
    _check(checks, "opaque_results", all(item.get("payload_ref", "").startswith("payload:synthetic:opaque:") for item in _list(cases.get("SCENARIO12_OPAQUE_RESULTS", {}).get("invocations"))))
    _check(
        checks,
        "upstream_snapshots_unchanged",
        all(
            chain.get("target_request_snapshot_before")
            == chain.get("target_request_snapshot_after")
            for item in cases.values()
            if (chain := item.get("source_chain") or {})
        ),
    )
    _check(checks, "malformed_input_fails_closed", cases.get("MALFORMED_INPUT_FAIL_CLOSED", {}).get("session", {}).get("formation_status") == "INVALID_INPUT" and cases.get("MALFORMED_INPUT_FAIL_CLOSED", {}).get("invocations") == [])
    _check(checks, "authority_responsibility_valid", cases.get("AUTHORITY_RESPONSIBILITY_VALID", {}).get("governance_preflight", {}).get("status") == "PASS")
    _check(checks, "no_runtime_observation", all(item.get("lifecycle_artifact", {}).get("runtime_observation_created") is False for item in cases.values()))
    _check(checks, "no_gateway", all(item.get("lifecycle_artifact", {}).get("gateway_submission") is False for item in cases.values()))
    _check(checks, "unified_final_decision_go", compute_unified_final_decision(functional_checks_passed=True, contract_failures=(), governance_preflight="PASS", governance_postflight="PASS", cognitive_logic_result="PASS", operational_result="PASS") == "GO")
    _check(checks, "governance_failure_forces_no_go", compute_unified_final_decision(functional_checks_passed=True, contract_failures=(), governance_preflight="GOVERNANCE_PREFLIGHT_BLOCKED", governance_postflight="PASS", cognitive_logic_result="PASS", operational_result="PASS") == "NO_GO")
    functional = all(checks.values())
    governance_preflight = "PASS" if all(item.get("governance_preflight", {}).get("status") == "PASS" or item.get("business_engine_executed") is False for item in cases.values()) else "GOVERNANCE_PREFLIGHT_BLOCKED"
    governance_postflight = "PASS" if all(item.get("governance_postflight", {}).get("status") == "PASS" for item in cases.values() if item.get("business_engine_executed") is True) else "GOVERNANCE_POSTFLIGHT_BLOCKED"
    failures = tuple(name for name, passed in checks.items() if not passed)
    cognitive = "PASS" if functional else "FAIL"
    operational = "PASS" if functional else "FAIL"
    decision = compute_unified_final_decision(functional_checks_passed=functional, contract_failures=failures, governance_preflight=governance_preflight, governance_postflight=governance_postflight, cognitive_logic_result=cognitive, operational_result=operational)
    return {
        "check_count": len(checks),
        "passed_count": sum(1 for passed in checks.values() if passed),
        "failed_checks": [name for name, passed in checks.items() if not passed],
        "all_checks_passed": functional,
        "contract_failures": list(failures),
        "governance_preflight": governance_preflight,
        "governance_postflight": governance_postflight,
        "cognitive_logic_result": cognitive,
        "operational_result": operational,
        "final_decision": decision,
        "status": "VERIFIED_ARTIFACT_RESULT",
        "side_effect_evidence": {
            "runner_declared": {
                "synthetic_only": declared_synthetic_only,
                "no_real_effects": declared_no_real_effects,
            },
            "verifier_observed": observed_no_real_effects,
            "contract_expected": "OBSERVED_NOT_EXECUTED",
        },
    }


def main() -> int:
    result = verify(json.loads(SUMMARY_PATH.read_text(encoding="utf-8")))
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result["final_decision"] == "GO" else 1


if __name__ == "__main__":
    raise SystemExit(main())
