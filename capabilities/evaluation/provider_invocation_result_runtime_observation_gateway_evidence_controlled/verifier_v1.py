"""Verifier for the controlled execution-result to evidence integration."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from capabilities.midplatform.protocol_manager.module.governance_verification_backbone_v1 import (
    compute_unified_final_decision,
)

from .fixtures_v1 import (
    EVALUATION_MARKER,
    build_provider_invocation_observation_evidence_cases_v1,
)


DEFAULT_SUMMARY = Path("_eval_out/provider_invocation_result_runtime_observation_gateway_evidence_controlled_v1/runner_summary_v1.json")


def _check(checks: dict[str, bool], name: str, value: bool) -> None:
    checks[name] = bool(value)


def _list(value: Any) -> list[dict[str, Any]]:
    return [item if isinstance(item, dict) else {} for item in value] if isinstance(value, list) else []


def _mapping(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _valid_envelope(value: Any) -> bool:
    return isinstance(value, dict) and all(
        bool(value.get(name))
        for name in (
            "observation_id", "execution_instance_ref", "provider_ref", "capability_ref",
            "modality", "source_ref", "raw_result_ref", "temporal_ref", "observed_at",
            "provenance_refs",
        )
    ) and value.get("modality") in {
        "USER_INPUT", "VISION", "OCR", "AUDIO", "SLAM_SPATIAL", "FIELD_REFERENCE",
        "SYSTEM_EVENT", "EXTERNAL_PROVIDER",
    } and value.get("result_status") in {"AVAILABLE", "UNAVAILABLE"} and value.get("candidate_only") is True and value.get("truth_declared") is False


def _valid_ingress(value: Any) -> bool:
    return isinstance(value, dict) and all(bool(value.get(name)) for name in (
        "ingress_id", "ingress_type", "provider_ref", "source_ref", "payload_ref",
        "temporal_ref", "observed_at", "trace_ref", "provenance_refs",
    )) and value.get("candidate_only") is True


def _valid_evidence(value: Any) -> bool:
    return isinstance(value, dict) and all(bool(value.get(name)) for name in (
        "evidence_id", "source_provider", "source_capability", "raw_output_ref",
        "source_temporal_ref", "trace_ref", "provenance_refs",
    )) and value.get("candidate_only") is True and value.get("fact_declared") is False


def _valid_observation(value: Any) -> bool:
    return isinstance(value, dict) and bool(value.get("observation_id")) and bool(value.get("evidence_refs")) and value.get("admission_state") in {
        "RECEIVED", "NORMALIZED", "EVIDENCE_READY", "OBSERVATION_CANDIDATE_READY",
        "NEEDS_CONFIRMATION", "CONTESTED", "ADMITTED_OBSERVATION", "REJECTED",
        "REVOKED", "EXPIRED", "SUPERSEDED",
    } and bool(value.get("trace_ref")) and bool(value.get("provenance_refs")) and value.get("candidate_only") is True and value.get("truth_declared") is False


def _valid_admission(value: Any) -> bool:
    return isinstance(value, dict) and all(bool(value.get(name)) for name in (
        "gateway_admission_ref", "runtime_observation_ref", "execution_instance_ref",
        "observation_ref", "evidence_refs", "provenance_refs", "gateway_trace_ref",
    )) and value.get("admission_state") == "ADMITTED_OBSERVATION" and value.get("owner_ref") == "Observation Gateway Governance" and value.get("candidate_only") is True and value.get("world_truth_declared") is False and value.get("provider_invocation") is False and value.get("model_invocation") is False and value.get("live_observation_execution") is False


def _valid_trace(value: Any) -> bool:
    return isinstance(value, dict) and all(bool(value.get(name)) for name in (
        "root_trace_id", "a_route_ingress_ref", "observation_trace_ref", "evidence_trace_refs",
        "provider_trace_refs", "source_input_refs", "provenance_refs", "reverse_lookup_path",
    )) and value.get("authority_granted") is False and value.get("candidate_only") is True


def _valid_gateway_guards(value: Any) -> bool:
    if not isinstance(value, dict):
        return False
    excluded = {"synthetic_only", "controlled_integration_only", "execution_mode"}
    return (
        all(value.get(name) is False for name in value if name not in excluded)
        and value.get("synthetic_only") is True
        and value.get("controlled_integration_only") is True
        and value.get("execution_mode") == "LIVE_RUNTIME"
    )


def verify(summary: dict[str, Any]) -> dict[str, Any]:
    checks: dict[str, bool] = {}
    items = {_mapping(item).get("case_id"): _mapping(item) for item in _list(summary.get("cases"))}
    expected = build_provider_invocation_observation_evidence_cases_v1()
    _check(checks, "required_cases_present", {case.case_id for case in expected} <= set(items))
    _check(checks, "controlled_marker", summary.get("source_mode") == EVALUATION_MARKER)
    _check(checks, "case_count_at_least_75", summary.get("controlled_case_count", 0) >= 75)
    _check(checks, "governance_backbone_reused", summary.get("governance_backbone_reused") is True)
    _check(checks, "canonical_gateway_owner", summary.get("canonical_gateway_owner") == "Observation Gateway Governance")
    _check(checks, "canonical_evidence_owner", summary.get("canonical_evidence_owner") == "Observation Gateway Governance")
    _check(checks, "adapter_has_no_semantic_authority", summary.get("adapter_semantic_authority") is False)
    _check(
        checks,
        "global_synthetic_guards",
        all(summary.get(name) is False for name in (
            "provider_invoked", "model_invoked", "network_called", "subprocess_started",
            "thread_started", "socket_used", "gateway_submission", "truth_declared",
            "world_truth_declared", "evidence_sufficiency_decided", "current_world_mutated",
            "field_mutated", "context_mutated", "memory_mutated", "experience_mutated",
        )) and summary.get("synthetic_only") is True and summary.get("controlled") is True,
    )

    for case in expected:
        item = items.get(case.case_id, {})
        preflight = item.get("governance_preflight") or {}
        postflight = item.get("governance_postflight") or {}
        formation = item.get("observation_formation") or {}
        runtime = item.get("runtime_observation") or {}
        gateway = item.get("gateway") or {}
        gateways = _list(item.get("gateways"))
        evidence = _list(item.get("evidence"))
        if case.expected_preflight_status != "PASS":
            _check(checks, f"{case.case_id}:preflight_blocked", preflight.get("status") == case.expected_preflight_status)
            _check(checks, f"{case.case_id}:hard_stop", item.get("business_engine_executed") is False and not item.get("source_chains") and not item.get("gateways") and item.get("evidence_count") == 0)
            continue
        _check(checks, f"{case.case_id}:preflight_pass", preflight.get("status") == "PASS")
        _check(checks, f"{case.case_id}:formation_status", formation.get("formation_status", "NO_INVOCATION_RESULT") == case.expected_formation_status)
        _check(checks, f"{case.case_id}:gateway_admission_status", gateway.get("admission_state", "NOT_ATTEMPTED") == case.expected_gateway_admission_status)
        _check(checks, f"{case.case_id}:evidence_formation_status", ("EVIDENCE_CREATED" if item.get("evidence_count") else "NO_EVIDENCE") == case.expected_evidence_formation_status)
        _check(checks, f"{case.case_id}:observation_count", item.get("observation_count") == case.expected_observation_count)
        _check(checks, f"{case.case_id}:evidence_count", item.get("evidence_count") == case.expected_evidence_count)
        _check(checks, f"{case.case_id}:postflight", postflight.get("status") == case.expected_postflight_status)
        if case.expected_formation_status == "RUNTIME_OBSERVATION_FORMED":
            _check(checks, f"{case.case_id}:envelope_valid", _valid_envelope(runtime))
            _check(checks, f"{case.case_id}:gateway_result_present", bool(gateway))
        if case.expected_gateway_admission_status == "ADMITTED_OBSERVATION":
            _check(checks, f"{case.case_id}:gateway_admitted", gateway.get("admission_state") == "ADMITTED_OBSERVATION")
            _check(checks, f"{case.case_id}:gateway_admission_valid", bool(gateway.get("runtime_admission")) and _valid_admission(gateway.get("runtime_admission")))
            _check(checks, f"{case.case_id}:gateway_negative_guards", _valid_gateway_guards(gateway.get("negative_guards")))
            _check(checks, f"{case.case_id}:gateway_contracts_valid", bool(gateway.get("ingress")) and _valid_ingress(gateway["ingress"]) and bool(gateway.get("observation")) and _valid_observation(gateway["observation"]) and all(_valid_evidence(value) for value in evidence) and _valid_trace(gateway.get("trace", {})))
        if case.expected_gateway_admission_status == "REJECTED":
            _check(checks, f"{case.case_id}:rejected_no_evidence", gateway.get("admission_state") == "REJECTED" and item.get("observation_count") == 0 and item.get("evidence_count") == 0)
        if case.outcome != "COMPLETED":
            _check(checks, f"{case.case_id}:noncompleted_no_observation", item.get("observation_count") == 0 and item.get("evidence_count") == 0 and not item.get("gateways"))

    completed = _mapping(items.get("VALID_COMPLETED_INVOCATION_FORMS_RUNTIME_OBSERVATION", {}))
    observation = completed.get("runtime_observation") or {}
    formation = completed.get("observation_formation") or {}
    _check(checks, "lineage_provider_preserved", observation.get("provider_ref") and observation.get("provider_ref") in formation.get("lineage_refs", []))
    _check(checks, "lineage_execution_refs_preserved", all(ref in formation.get("lineage_refs", []) for ref in (formation.get("source_session_ref"), formation.get("source_invocation_ref"), formation.get("source_invocation_result_ref"))))
    _check(checks, "model_null_allowed", _mapping(items.get("RUNTIME_OBSERVATION_MODEL_NULL_ALLOWED", {}).get("runtime_observation")).get("source_model_ref") is None)
    _check(checks, "model_carry_forward", _mapping(items.get("RUNTIME_OBSERVATION_MODEL_CARRY_FORWARD", {}).get("runtime_observation")).get("source_model_ref") == "model:controlled:explicit")
    _check(checks, "opaque_payload_preserved", isinstance((observation.get("output_candidate") or {}).get("opaque_payload_ref"), str) and (observation.get("output_candidate") or {}).get("opaque_payload_ref", "").startswith("payload:synthetic:opaque:"))
    _check(checks, "gateway_not_truth", _mapping(_mapping(completed.get("gateway")).get("runtime_admission")).get("world_truth_declared") is False)
    _check(checks, "evidence_not_truth", all(item.get("fact_declared") is False and item.get("candidate_only") is True for item in _list(completed.get("evidence"))))
    replay_gateways = _list(_mapping(items.get("REPLAY_OBSERVATION_IDEMPOTENT", {})).get("gateways"))
    _check(checks, "replay_ids_stable", len(replay_gateways) >= 2 and replay_gateways[0] == replay_gateways[1])
    distinct = _list(_mapping(items.get("DISTINCT_INVOCATIONS_DISTINCT_OBSERVATIONS", {})).get("observation_formations"))
    _check(checks, "distinct_scenario_paths", _mapping(items.get("DISTINCT_INVOCATIONS_DISTINCT_OBSERVATIONS", {})).get("observation_count") == 2 and len({_mapping(item.get("observation")).get("observation_id") for item in distinct}) == 2 if distinct else False)
    _check(checks, "world_truth_negative_case", _mapping(items.get("WORLD_TRUTH_BLOCKED", {}).get("governance_postflight")).get("status") == "GOVERNANCE_POSTFLIGHT_BLOCKED")
    _check(checks, "authority_responsibility_valid", _mapping(items.get("AUTHORITY_RESPONSIBILITY_VALID", {}).get("governance_preflight")).get("status") == "PASS")
    _check(checks, "authority_without_responsibility_blocked", _mapping(items.get("AUTHORITY_WITHOUT_RESPONSIBILITY_BLOCKED", {}).get("governance_preflight")).get("status") == "GOVERNANCE_PREFLIGHT_BLOCKED")
    _check(checks, "responsibility_without_authority_blocked", _mapping(items.get("RESPONSIBILITY_WITHOUT_AUTHORITY_BLOCKED", {}).get("governance_preflight")).get("status") == "GOVERNANCE_PREFLIGHT_BLOCKED")
    _check(checks, "no_semantic_interpretation", all("opaque_payload_ref" in json.dumps(item.get("runtime_observation", {})) or not item.get("runtime_observation") for item in items.values()))
    _check(checks, "unified_final_decision_go", compute_unified_final_decision(functional_checks_passed=True, contract_failures=(), governance_preflight="PASS", governance_postflight="PASS", cognitive_logic_result="PASS", operational_result="PASS") == "GO")
    _check(checks, "governance_failure_forces_no_go", compute_unified_final_decision(functional_checks_passed=True, contract_failures=(), governance_preflight="GOVERNANCE_PREFLIGHT_BLOCKED", governance_postflight="PASS", cognitive_logic_result="PASS", operational_result="PASS") == "NO_GO")

    failed = [name for name, passed in checks.items() if not passed]
    functional = not failed
    governance_preflight = "PASS" if all(
        (_mapping(item.get("governance_preflight")).get("status") == "PASS" and case.expected_preflight_status == "PASS")
        or (_mapping(item.get("governance_preflight")).get("status") == case.expected_preflight_status and case.expected_preflight_status != "PASS")
        for case in expected
        for item in (items.get(case.case_id, {}),)
    ) else "GOVERNANCE_PREFLIGHT_BLOCKED"
    governance_postflight = "PASS" if all(
        _mapping(item.get("governance_postflight")).get("status") == case.expected_postflight_status
        for case in expected
        if case.expected_preflight_status == "PASS"
        for item in (items.get(case.case_id, {}),)
    ) else "GOVERNANCE_POSTFLIGHT_BLOCKED"
    cognitive = "PASS" if functional else "FAIL"
    operational = "PASS" if functional else "FAIL"
    decision = compute_unified_final_decision(
        functional_checks_passed=functional,
        contract_failures=tuple(failed),
        governance_preflight=governance_preflight,
        governance_postflight=governance_postflight,
        cognitive_logic_result=cognitive,
        operational_result=operational,
    )
    return {
        "check_count": len(checks),
        "passed_count": sum(1 for value in checks.values() if value),
        "failed_checks": failed,
        "all_checks_passed": functional,
        "contract_failures": failed,
        "governance_preflight": governance_preflight,
        "governance_postflight": governance_postflight,
        "cognitive_logic_result": cognitive,
        "operational_result": operational,
        "final_decision": decision,
        "status": "VERIFIED_ARTIFACT_RESULT",
    }


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_SUMMARY
    result = verify(json.loads(path.read_text(encoding="utf-8")))
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result["final_decision"] == "GO" else 1


if __name__ == "__main__":
    raise SystemExit(main())
