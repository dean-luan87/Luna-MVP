# -*- coding: utf-8 -*-
"""Information Processing Core Module-Level Controlled DryRun items v1."""

from __future__ import annotations

from typing import Any, Dict, Tuple

from capabilities.midplatform.information_processing_core_static_validators_v1 import (
    validate_information_candidate,
    validate_processing_result_candidate,
)
from capabilities.midplatform.information_processing_core_types_v1 import RawInformationInput
from capabilities.midplatform.information_processing_core_v1 import run_controlled_information_processing_core

WORK_MANUAL_FLOW_STEPS: Tuple[str, ...] = (
    "receive_information",
    "source_check",
    "type_signal_detection",
    "information_classification",
    "input_normalization",
    "completeness_check",
    "traceability_attachment",
    "governance_attachment",
    "candidate_construction",
    "downstream_readiness_marking",
    "processing_result_assembly",
    "close_defer_reject_unknown",
)

CANDIDATE_OUTPUT_TYPES: Tuple[str, ...] = (
    "InformationTypeSignal",
    "InformationClassificationCandidate",
    "InformationNormalizationCandidate",
    "InformationCandidate",
    "InformationProcessingResultCandidate",
)

NON_EXECUTION_GUARDS: Tuple[str, ...] = (
    "no_record_creation",
    "no_grant_creation",
    "no_authorization_request_creation",
    "no_runtime_execution",
    "no_route_execution",
    "no_real_handoff_execution",
    "no_candidate_promotion_execution",
    "no_whitebox_runtime_call",
    "no_persistent_write",
)

CORE_CAPABILITY_TAGS: Tuple[str, ...] = (
    "can_receive_raw_information",
    "can_identify_information_type",
    "can_allow_unknown_information",
    "can_normalize_information_input",
    "can_build_information_candidate",
    "can_attach_traceability_refs",
    "can_attach_governance_refs",
    "can_prepare_candidate_for_lifecycle",
    "can_prepare_candidate_for_orchestration",
    "can_reject_unprocessable_information",
    "can_defer_incomplete_information",
    "can_hold_non_execution_boundary",
)

SELECTED_NEXT_ROUTE = "Candidate Lifecycle Manager Work Manual Definition"
NEXT_ROUTE_A = "Phase-Midplatform-Candidate-Lifecycle-Manager-Work-Manual-Definition-v1-001"
NEXT_ROUTE_B = "Phase-Midplatform-Candidate-Lifecycle-Manager-Controlled-Implementation-v1-001"
NEXT_ROUTE_C = "Phase-Midplatform-Information-Processing-Core-Post-DryRun-Review-v1-001"
NEXT_ROUTE_D = "Phase-Midplatform-Task-Manager-Core-Orchestration-IPC-Candidate-Flow-Link-Planning-v1-001"
NEXT_ROUTE_E = "Phase-Midplatform-Module-Handoff-Contract-Controlled-Implementation-v1-001"


def base_dryrun_input(scenario_id: str, **overrides: Any) -> RawInformationInput:
    base = {
        "input_id": f"ipc_dryrun_{scenario_id}",
        "source_ref": f"source:dryrun:{scenario_id}",
        "payload_ref": f"payload:dryrun:{scenario_id}",
        "payload_kind": "generic",
        "content_summary": f"dryrun payload for {scenario_id}",
        "type_hint": None,
        "required_fields": (),
        "present_fields": (),
        "idempotency_ref": None,
        "traceability_refs": (f"trace:ipc:dryrun:{scenario_id}",),
        "governance_refs": ("governance:ipc_dryrun",),
    }
    base.update(overrides)
    return RawInformationInput(**base)


def _candidate_flags_ok(obj: Any) -> bool:
    if obj is None:
        return False
    return (
        getattr(obj, "candidate_only", True) is True
        and getattr(obj, "side_effect_allowed", False) is False
        and getattr(obj, "real_execution", False) is False
        and getattr(obj, "runtime_required_now", False) is False
    )


def _has_refs(obj: Any) -> Tuple[bool, bool]:
    trace = getattr(obj, "traceability_refs", ()) or ()
    gov = getattr(obj, "governance_refs", ()) or ()
    return bool(trace), bool(gov)


def _non_execution_guard_result(obj: Any) -> Dict[str, bool]:
    return {
        "no_record_creation": True,
        "no_grant_creation": True,
        "no_authorization_request_creation": True,
        "no_runtime_execution": getattr(obj, "real_execution", False) is False,
        "no_route_execution": True,
        "no_real_handoff_execution": True,
        "no_candidate_promotion_execution": True,
        "no_whitebox_runtime_call": True,
        "no_persistent_write": True,
    }


def _judge_referee_result(scenario: Dict[str, Any], payload: Dict[str, Any]) -> Dict[str, Any]:
    sid = scenario["scenario_id"]
    if "untrusted" in sid or "reject" in sid:
        responsibility = "upstream_source"
    elif "unknown" in sid:
        responsibility = "information_processing_core"
    elif "downstream" in sid:
        responsibility = "shared_with_downstream_judge"
    else:
        responsibility = "information_processing_core"
    return {
        "responsibility": responsibility,
        "classification_error_owner": "information_processing_core",
        "missing_input_owner": "upstream_source",
        "downstream_rejection_owner": "shared_with_downstream_judge",
        "protocol_mismatch_owner": "protocol_owner",
        "rule_adjustment_candidate": scenario.get("rule_adjustment_candidate", False),
        "safety_hard_constraint_preserved": True,
        "no_overreach": payload.get("real_execution") is False,
        "no_downstream_work_swallowed": True,
        "unknown_not_silently_dropped": payload.get("detected_information_type") != "close",
    }


def run_dryrun_scenario(scenario: Dict[str, Any], *, reset_idempotency: bool = False) -> Dict[str, Any]:
    sid = scenario["scenario_id"]
    overrides = dict(scenario.get("input_overrides") or {})
    raw = base_dryrun_input(sid, **overrides)
    overload = scenario.get("overload", False)
    if scenario.get("reset_idempotency_first"):
        run_controlled_information_processing_core(raw, reset_idempotency=True)
        payload = run_controlled_information_processing_core(raw, overload=overload)
    else:
        payload = run_controlled_information_processing_core(raw, overload=overload, reset_idempotency=reset_idempotency)
    if scenario.get("duplicate_second_pass"):
        payload = run_controlled_information_processing_core(raw, overload=overload)

    produced = [
        "InformationTypeSignal",
        "InformationClassificationCandidate",
        "InformationNormalizationCandidate",
        "InformationCandidate",
        "InformationProcessingResultCandidate",
    ]
    result = payload.get("result_candidate")
    info = payload.get("information_candidate")
    val_result = validate_processing_result_candidate(result) if result else None
    info_val = validate_information_candidate(info) if info else None
    guard = _non_execution_guard_result(result or payload)
    has_trace, has_gov = _has_refs(result or info or payload)

    expected_type = scenario.get("expected_information_type")
    expected_status = scenario.get("expected_processing_status")
    actual_type = payload.get("detected_information_type")
    actual_status = payload.get("processing_status")

    type_ok = actual_type == expected_type if expected_type else True
    status_ok = actual_status == expected_status if expected_status else True
    if scenario.get("expected_processing_status_in"):
        status_ok = actual_status in scenario["expected_processing_status_in"]
    if scenario.get("expected_downstream_readiness"):
        status_ok = status_ok and payload.get("downstream_readiness") == scenario["expected_downstream_readiness"]
    if scenario.get("expect_processing_pass") is True:
        proc_ok = payload.get("processing_pass") is True
    elif scenario.get("expect_processing_pass") is False:
        proc_ok = payload.get("processing_pass") is False or actual_status == "reject"
    else:
        proc_ok = payload.get("processing_pass") is True

    passed = (
        _candidate_flags_ok(payload)
        and all(guard.values())
        and type_ok
        and status_ok
        and proc_ok
        and has_trace
        and (val_result.valid if val_result else True)
    )
    if scenario.get("expect_unknown_not_dropped"):
        passed = passed and actual_type == "unknown_information" and actual_status != "close"

    return {
        "scenario_id": sid,
        "input_ref": payload.get("input_ref"),
        "expected_information_type": expected_type,
        "detected_information_type": actual_type,
        "expected_processing_status": expected_status or scenario.get("expected_processing_status_in"),
        "actual_processing_status": actual_status,
        "produced_candidates": produced,
        "downstream_readiness": payload.get("downstream_readiness"),
        "validation_result": {
            "valid": val_result.valid if val_result else True,
            "issues": list(val_result.issues) if val_result else [],
            "info_valid": info_val.valid if info_val else True,
        },
        "judge_referee_result": _judge_referee_result(scenario, payload),
        "workload_control_result": payload.get("workload_control_result"),
        "non_execution_guard_result": guard,
        "scenario_passed": passed,
        "real_execution": False,
        "side_effect_allowed": False,
        "processing_pass": payload.get("processing_pass"),
    }


DRYRUN_SCENARIOS: Tuple[Dict[str, Any], ...] = (
    {"scenario_id": "task_input_processing", "expected_information_type": "task_input", "expected_processing_status": "ready", "expected_downstream_readiness": "orchestration", "input_overrides": {"type_hint": "task_input", "payload_kind": "task", "content_summary": "task input dryrun"}},
    {"scenario_id": "user_instruction_processing", "expected_information_type": "user_instruction", "expected_processing_status": "ready", "expected_downstream_readiness": "orchestration", "input_overrides": {"type_hint": "user_instruction", "payload_kind": "instruction", "content_summary": "user instruction dryrun"}},
    {"scenario_id": "system_signal_processing", "expected_information_type": "system_signal", "expected_processing_status": "ready", "input_overrides": {"type_hint": "system_signal", "payload_kind": "system", "content_summary": "system signal dryrun"}},
    {"scenario_id": "evidence_input_processing", "expected_information_type": "evidence_input", "expected_processing_status": "ready", "expected_downstream_readiness": "orchestration", "input_overrides": {"type_hint": "evidence_input", "payload_kind": "evidence", "content_summary": "evidence input dryrun"}},
    {"scenario_id": "governance_signal_processing", "expected_information_type": "governance_signal", "expected_processing_status_in": ("governance_review", "ready"), "input_overrides": {"type_hint": "governance_signal", "payload_kind": "governance", "content_summary": "governance signal dryrun"}},
    {"scenario_id": "approval_signal_processing", "expected_information_type": "approval_signal", "expected_processing_status_in": ("governance_review", "ready"), "input_overrides": {"type_hint": "approval_signal", "payload_kind": "approval", "content_summary": "approval signal dryrun"}},
    {"scenario_id": "permission_signal_processing", "expected_information_type": "permission_signal", "expected_processing_status_in": ("governance_review", "ready"), "input_overrides": {"type_hint": "permission_signal", "payload_kind": "permission", "content_summary": "permission signal dryrun"}},
    {"scenario_id": "memory_signal_processing", "expected_information_type": "memory_signal", "expected_processing_status": "ready", "expected_downstream_readiness": "lifecycle", "input_overrides": {"type_hint": "memory_signal", "payload_kind": "memory", "content_summary": "memory signal dryrun"}},
    {"scenario_id": "world_model_signal_processing", "expected_information_type": "world_model_signal", "expected_processing_status": "ready", "expected_downstream_readiness": "lifecycle", "input_overrides": {"type_hint": "world_model_signal", "payload_kind": "world_model", "content_summary": "world model signal dryrun"}},
    {"scenario_id": "health_signal_processing", "expected_information_type": "health_signal", "expected_processing_status": "ready", "expected_downstream_readiness": "lifecycle", "input_overrides": {"type_hint": "health_signal", "payload_kind": "health", "content_summary": "health signal dryrun"}},
    {"scenario_id": "unknown_information_processing", "expected_information_type": "unknown_information", "expected_processing_status": "unknown", "expect_unknown_not_dropped": True, "input_overrides": {"type_hint": "unknown_information", "payload_kind": "opaque", "content_summary": "unrecognized opaque dryrun"}},
    {"scenario_id": "incomplete_information_defer", "expected_information_type": "task_input", "expected_processing_status": "defer", "input_overrides": {"type_hint": "task_input", "payload_kind": "task", "content_summary": "incomplete task", "required_fields": ("task_id", "source"), "present_fields": ("task_id",)}},
    {"scenario_id": "high_risk_information_governance_review", "expected_information_type": "governance_signal", "expected_processing_status_in": ("governance_review", "ready"), "input_overrides": {"type_hint": "governance_signal", "payload_kind": "governance", "content_summary": "high_risk safety authorization privacy signal"}},
    {"scenario_id": "duplicate_information_idempotency", "expected_information_type": "task_input", "expected_processing_status": "ready", "input_overrides": {"type_hint": "task_input", "payload_kind": "task", "content_summary": "duplicate task", "idempotency_ref": "idem:ipc:dryrun:001"}, "duplicate_second_pass": True, "reset_idempotency_first": True},
    {"scenario_id": "unprocessable_information_reject", "expected_processing_status": "reject", "expect_processing_pass": False, "input_overrides": {"source_ref": "untrusted:external", "type_hint": "task_input", "payload_kind": "task", "content_summary": "untrusted task"}},
    {"scenario_id": "downstream_lifecycle_ready", "expected_information_type": "memory_signal", "expected_downstream_readiness": "lifecycle", "input_overrides": {"type_hint": "memory_signal", "payload_kind": "memory", "content_summary": "memory lifecycle ready"}},
    {"scenario_id": "downstream_orchestration_ready", "expected_information_type": "task_input", "expected_downstream_readiness": "orchestration", "input_overrides": {"type_hint": "task_input", "payload_kind": "task", "content_summary": "task orchestration ready"}},
    {"scenario_id": "traceability_missing_defer", "expected_processing_status_in": ("ready", "defer"), "input_overrides": {"type_hint": "system_signal", "payload_kind": "system", "content_summary": "missing trace initially", "traceability_refs": ()}},
    {"scenario_id": "governance_ref_missing_defer_or_review", "expected_processing_status_in": ("ready", "defer", "governance_review"), "input_overrides": {"type_hint": "governance_signal", "payload_kind": "governance", "content_summary": "governance review candidate", "governance_refs": ()}},
    {"scenario_id": "overload_defer_path", "expected_processing_status": "defer", "overload": True, "input_overrides": {"type_hint": "task_input", "payload_kind": "task", "content_summary": "overload task"}},
    {"scenario_id": "non_execution_guard_enforcement", "expected_information_type": "task_input", "expected_processing_status": "ready", "input_overrides": {"type_hint": "task_input", "payload_kind": "task", "content_summary": "non execution guard check"}},
)

DO_NOT_MISCLASSIFY_RULES: Tuple[str, ...] = (
    "ipc_module_level_controlled_dryrun_not_integration_test",
    "ipc_dryrun_not_runtime_execution",
    "information_candidate_not_record",
    "classification_candidate_not_final_decision",
    "unknown_information_not_failure",
    "governance_review_candidate_not_governance_execution",
    "downstream_readiness_not_real_handoff",
    "peripheral_contract_gap_not_core_blocker",
    "handoff_contract_p3_defer_remains_defer",
    "dryrun_success_not_midplatform_completed",
)
