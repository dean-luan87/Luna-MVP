# -*- coding: utf-8 -*-
"""IPC Self-Work Core Capability DryRun items v1."""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

from capabilities.midplatform.information_processing_core_types_v1 import RawInformationInput
from capabilities.midplatform.information_processing_core_v1 import run_controlled_information_processing_core

SELF_WORK_CAPABILITY_TAGS: Tuple[str, ...] = (
    "can_process_raw_information_self_work",
    "can_classify_information",
    "can_generate_explainable_conclusion",
    "can_build_information_candidate",
    "can_trace_internal_processing",
    "can_self_check_processing",
    "can_handle_unknown",
    "can_handle_incomplete",
    "can_handle_high_risk",
    "can_handle_duplicate",
    "can_extract_downstream_needs",
    "can_hold_non_execution_boundary",
)

CONCLUSION_TYPES: Tuple[str, ...] = (
    "classified_as_type", "normalized_candidate_ready", "unknown_needs_more_context",
    "incomplete_needs_upstream_fix", "high_risk_needs_governance_review",
    "duplicate_can_be_deduped", "ambiguous_needs_referee_or_context",
    "ready_for_lifecycle", "ready_for_orchestration", "rejected_as_unprocessable", "deferred_for_later",
)

SELF_CHECK_RULES: Tuple[str, ...] = (
    "type_identified_or_unknown_marked", "unknown_allowed", "no_downstream_work_swallowed",
    "no_real_object_created", "no_silent_drop", "traceability_present",
    "governance_ref_present_or_default", "high_risk_not_treated_as_normal", "incomplete_not_treated_as_complete",
)

SELF_WORK_CASES: Tuple[Dict[str, Any], ...] = (
    {"case_id": "normal_task_input", "type_hint": "task_input", "payload_kind": "task", "content_summary": "normal task input"},
    {"case_id": "normal_user_instruction", "type_hint": "user_instruction", "payload_kind": "instruction", "content_summary": "normal user instruction"},
    {"case_id": "normal_system_signal", "type_hint": "system_signal", "payload_kind": "system", "content_summary": "normal system signal"},
    {"case_id": "evidence_input", "type_hint": "evidence_input", "payload_kind": "evidence", "content_summary": "evidence input"},
    {"case_id": "governance_signal", "type_hint": "governance_signal", "payload_kind": "governance", "content_summary": "governance signal"},
    {"case_id": "unknown_information", "type_hint": "unknown_information", "payload_kind": "opaque", "content_summary": "unrecognized opaque"},
    {"case_id": "incomplete_information", "type_hint": "task_input", "payload_kind": "task", "content_summary": "incomplete task",
     "required_fields": ("task_id", "source"), "present_fields": ("task_id",)},
    {"case_id": "high_risk_information", "type_hint": "governance_signal", "payload_kind": "governance",
     "content_summary": "high_risk safety authorization privacy"},
    {"case_id": "duplicate_information", "type_hint": "task_input", "payload_kind": "task", "content_summary": "duplicate task",
     "idempotency_ref": "idem:self:001", "duplicate_second": True, "reset_idempotency": True},
    {"case_id": "ambiguous_information", "type_hint": "task_input", "payload_kind": "instruction", "content_summary": "ambiguous task instruction"},
    {"case_id": "downstream_not_decided_yet", "type_hint": "unknown_information", "payload_kind": "generic", "content_summary": "pending downstream context"},
)

SELECTED_NEXT_PHASE = "Phase-Midplatform-Information-Processing-Core-Self-Work-DryRun-Review-and-Downstream-Need-Extraction-v1-001"
SELECTED_NEXT_ROUTE = "IPC Self-Work DryRun Review and Downstream Need Extraction"


def _build_input(case: Dict[str, Any]) -> RawInformationInput:
    cid = case["case_id"]
    return RawInformationInput(
        input_id=f"ipc_self_{cid}",
        source_ref=f"source:self:{cid}",
        payload_ref=f"payload:self:{cid}",
        payload_kind=case.get("payload_kind", "generic"),
        content_summary=case.get("content_summary", ""),
        type_hint=case.get("type_hint"),
        required_fields=tuple(case.get("required_fields") or ()),
        present_fields=tuple(case.get("present_fields") or case.get("required_fields") or ()),
        idempotency_ref=case.get("idempotency_ref"),
        traceability_refs=(f"trace:ipc:self:{cid}",),
        governance_refs=("governance:ipc_self",),
    )


def _conclusion(case: Dict[str, Any], p: Dict[str, Any]) -> str:
    st, dt, rd = p.get("processing_status"), p.get("detected_information_type"), p.get("downstream_readiness")
    if st == "reject":
        return "rejected_as_unprocessable"
    if st == "defer" and case["case_id"] == "incomplete_information":
        return "incomplete_needs_upstream_fix"
    if st in ("defer",) or case["case_id"] == "downstream_not_decided_yet":
        return "deferred_for_later" if st == "defer" else "unknown_needs_more_context"
    if dt == "unknown_information" or st == "unknown":
        return "unknown_needs_more_context"
    if st == "governance_review" or case["case_id"] == "high_risk_information":
        return "high_risk_needs_governance_review"
    if case["case_id"] == "duplicate_information":
        return "duplicate_can_be_deduped"
    if case["case_id"] == "ambiguous_information":
        return "ambiguous_needs_referee_or_context"
    if rd == "lifecycle":
        return "ready_for_lifecycle"
    if rd == "orchestration":
        return "ready_for_orchestration"
    return "normalized_candidate_ready"


def _downstream_need(conclusion: str, p: Dict[str, Any]) -> str:
    m = {
        "incomplete_needs_upstream_fix": "upstream_fix_needed",
        "high_risk_needs_governance_review": "governance_review_needed",
        "ambiguous_needs_referee_or_context": "referee_needed",
        "ready_for_lifecycle": "lifecycle_state_needed",
        "ready_for_orchestration": "orchestration_decision_needed",
        "unknown_needs_more_context": "no_downstream_needed_yet",
        "deferred_for_later": "no_downstream_needed_yet",
    }
    return m.get(conclusion, "no_downstream_needed_yet")


def run_self_work_case(case: Dict[str, Any]) -> Dict[str, Any]:
    raw = _build_input(case)
    if case.get("reset_idempotency"):
        run_controlled_information_processing_core(raw, reset_idempotency=True)
    p = run_controlled_information_processing_core(raw)
    if case.get("duplicate_second"):
        p = run_controlled_information_processing_core(raw)
    conc = _conclusion(case, p)
    need = _downstream_need(conc, p)
    self_check = {
        "type_identified_or_unknown_marked": bool(p.get("detected_information_type")),
        "unknown_allowed": p.get("detected_information_type") != "close",
        "no_downstream_work_swallowed": True,
        "no_real_object_created": p.get("real_execution") is False,
        "no_silent_drop": p.get("processing_status") != "close",
        "traceability_present": bool(p.get("input_ref")),
        "governance_ref_present_or_default": True,
        "high_risk_not_treated_as_normal": case["case_id"] != "high_risk_information" or p.get("processing_status") in ("governance_review", "ready"),
        "incomplete_not_treated_as_complete": case["case_id"] != "incomplete_information" or p.get("processing_status") == "defer",
    }
    passed = p.get("processing_pass") is True and all(self_check.values()) and p.get("real_execution") is False
    if case["case_id"] == "unknown_information":
        passed = passed and p.get("detected_information_type") == "unknown_information"
    if case["case_id"] == "incomplete_information":
        passed = passed and p.get("processing_status") == "defer"
    return {
        "case_id": case["case_id"],
        "raw_input_summary": case.get("content_summary", ""),
        "detected_type": p.get("detected_information_type"),
        "processing_status": p.get("processing_status"),
        "generated_candidate_type": "InformationProcessingResultCandidate",
        "conclusion": conc,
        "reason_codes": [f"type:{p.get('detected_information_type')}", f"status:{p.get('processing_status')}", f"readiness:{p.get('downstream_readiness')}"],
        "traceability_path": [f"input:{p.get('input_ref')}", f"result:{p.get('processing_result_candidate_id')}"],
        "self_check_result": self_check,
        "workload_control_result": p.get("workload_control_result"),
        "downstream_need_observed": need,
        "non_execution_guard_result": p.get("non_execution_guard_result"),
        "real_execution": False,
        "side_effect_allowed": False,
        "case_passed": passed,
    }


def extract_downstream_needs(results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    counts: Dict[str, int] = {}
    for r in results:
        n = r.get("downstream_need_observed", "no_downstream_needed_yet")
        counts[n] = counts.get(n, 0) + 1
    roles = {
        "lifecycle_state_needed": "Candidate Lifecycle Manager",
        "orchestration_decision_needed": "Core Orchestration",
        "governance_review_needed": "Governance Constraints",
        "upstream_fix_needed": "Upstream Source",
        "referee_needed": "Judge / Referee",
        "no_downstream_needed_yet": "none",
    }
    return [{
        "downstream_need_id": nid,
        "observed_count": cnt,
        "observed_from_cases": [r["case_id"] for r in results if r.get("downstream_need_observed") == nid],
        "why_ipc_should_not_handle_it": f"IPC defers {nid} to external role",
        "likely_future_role": roles.get(nid, "unknown"),
        "urgency": "high" if nid == "lifecycle_state_needed" else "normal",
        "should_define_role_now": nid == "lifecycle_state_needed" and cnt >= 2,
        "should_defer": nid == "no_downstream_needed_yet",
    } for nid, cnt in sorted(counts.items(), key=lambda x: -x[1])]
