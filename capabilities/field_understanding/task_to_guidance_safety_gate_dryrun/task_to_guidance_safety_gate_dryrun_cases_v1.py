# -*- coding: utf-8 -*-
"""Task to Guidance Safety Gate Dry-Run — cases + alignment v1."""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

from capabilities.field_understanding.field_to_task_alignment_dryrun.field_to_task_alignment_dryrun_cases_v1 import (
    align_field_to_task_v1,
    build_positive_input_bundles_v1 as build_field_to_task_input_bundles_v1,
)
from capabilities.field_understanding.task_to_guidance_safety_gate_dryrun.task_to_guidance_safety_gate_dryrun_types_v1 import (
    ACTION_SAFETY_ENTRYPOINT,
    GUIDANCE_ENTRYPOINT,
    NEGATIVE_CASE_REFS,
    POSITIVE_CASE_REFS,
    SOURCE_CHAIN,
    SPEECH_GATE_ENTRYPOINT,
    TASK_MANAGER_ENTRYPOINT,
)

_CHAIN = (SOURCE_CHAIN, "task_to_guidance_cases_v1")

_TASK_CASE_MAP = {
    "mall_find_entrance_guidance_candidate": "mall_find_entrance_task",
    "subway_enter_station_guidance_candidate": "subway_station_enter_station_task",
    "stadium_concert_ticket_gate_guidance_candidate": "stadium_concert_ticket_check_task",
    "plaza_market_crowd_safety_guidance_candidate": "plaza_temporary_market_find_stall_task",
    "gps_slam_conflict_guidance_blocked": "gps_slam_conflict_delay_navigation_task",
    "home_return_stable_guidance_candidate": "home_return_task_stable_field",
}

_GUIDANCE_TYPES = {
    "mall_find_entrance_guidance_candidate": "find_entrance_hint",
    "subway_enter_station_guidance_candidate": "cautious_indoor_guidance_candidate",
    "stadium_concert_ticket_gate_guidance_candidate": "find_ticket_gate_hint",
    "plaza_market_crowd_safety_guidance_candidate": "observe_and_request_evidence",
    "gps_slam_conflict_guidance_blocked": "conflict_blocked_guidance",
    "home_return_stable_guidance_candidate": "coarse_route_with_local_check",
}

_EVIDENCE_REQUESTS = {
    "mall_find_entrance_guidance_candidate": (
        "entrance_sign",
        "doorway",
        "path_accessibility",
    ),
    "subway_enter_station_guidance_candidate": (
        "station_sign",
        "gate",
        "crowd",
        "local_anchor",
    ),
    "stadium_concert_ticket_gate_guidance_candidate": (
        "ocr_sign",
        "ticket_gate",
        "crowd_flow",
    ),
    "plaza_market_crowd_safety_guidance_candidate": (
        "pedestrian_flow",
        "walkable_area",
        "stall_sign",
    ),
    "gps_slam_conflict_guidance_blocked": (
        "conflict_resolution",
        "additional_spatial_evidence",
    ),
    "home_return_stable_guidance_candidate": (
        "coarse_map_route",
        "local_spatial_check",
    ),
}


def _bundle_chain(case_ref: str) -> List[str]:
    return list(_CHAIN + (case_ref,))


def build_task_trace_for_guidance_case(case_ref: str) -> Dict[str, Any]:
    task_case_ref = _TASK_CASE_MAP[case_ref]
    task_bundle = build_field_to_task_input_bundles_v1()[task_case_ref]
    return align_field_to_task_v1(task_bundle)


def build_positive_input_bundles_v1() -> Dict[str, Dict[str, Any]]:
    bundles: Dict[str, Dict[str, Any]] = {}
    for case_ref in POSITIVE_CASE_REFS:
        task_trace = build_task_trace_for_guidance_case(case_ref)
        bundles[case_ref] = {
            "bundle_ref": f"bundle_{case_ref}",
            "case_ref": case_ref,
            "task_case_ref": _TASK_CASE_MAP[case_ref],
            "task_trace": task_trace,
            "source_chain": _bundle_chain(case_ref),
            "task_manager_entrypoint": TASK_MANAGER_ENTRYPOINT,
            "guidance_entrypoint": GUIDANCE_ENTRYPOINT,
            "speech_gate_entrypoint": SPEECH_GATE_ENTRYPOINT,
            "action_safety_entrypoint": ACTION_SAFETY_ENTRYPOINT,
            "candidate_only": True,
        }
    return bundles


def build_negative_input_bundles_v1() -> Dict[str, Dict[str, Any]]:
    base = build_positive_input_bundles_v1()["mall_find_entrance_guidance_candidate"]
    conflict_base = build_positive_input_bundles_v1()["gps_slam_conflict_guidance_blocked"]

    route_as_nav = dict(base)
    route_as_nav.update(
        {
            "bundle_ref": "bundle_invalid_route_as_nav",
            "case_ref": "invalid_task_route_hint_as_navigation_action",
            "execute_route_hint_as_navigation": True,
        }
    )

    speech_tts = dict(base)
    speech_tts.update(
        {
            "bundle_ref": "bundle_invalid_speech_tts",
            "case_ref": "invalid_speech_gate_triggers_tts",
            "trigger_tts_output": True,
        }
    )

    conflict_action = dict(conflict_base)
    conflict_action.update(
        {
            "bundle_ref": "bundle_invalid_conflict_action_guidance",
            "case_ref": "invalid_conflict_action_like_guidance",
            "force_action_like_guidance": True,
        }
    )

    bypass_safety = dict(base)
    bypass_safety.update(
        {
            "bundle_ref": "bundle_invalid_bypass_safety",
            "case_ref": "invalid_guidance_bypasses_action_safety",
            "skip_action_safety": True,
        }
    )

    return {
        "invalid_task_route_hint_as_navigation_action": route_as_nav,
        "invalid_speech_gate_triggers_tts": speech_tts,
        "invalid_conflict_action_like_guidance": conflict_action,
        "invalid_guidance_bypasses_action_safety": bypass_safety,
    }


def validate_task_to_guidance_bundle(bundle: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues: List[str] = []
    task_trace = bundle.get("task_trace") or {}

    if bundle.get("candidate_only") is not True:
        issues.append("bundle_not_candidate_only")
    if not bundle.get("source_chain"):
        issues.append("source_chain_required")
    if not task_trace.get("alignment_ok"):
        issues.append("task_alignment_not_ok")

    route = task_trace.get("task_route_hint_candidate") or {}
    if bundle.get("execute_route_hint_as_navigation") is True:
        issues.append("task_route_hint_as_navigation_action_forbidden")

    if bundle.get("trigger_tts_output") is True:
        issues.append("speech_gate_tts_output_forbidden")

    if bundle.get("force_action_like_guidance") is True:
        conflict_risks = task_trace.get("task_risk_candidate") or {}
        if "conflict_requires_resolution" in (conflict_risks.get("risk_kinds") or []):
            issues.append("conflict_action_like_guidance_forbidden")

    if bundle.get("skip_action_safety") is True:
        issues.append("action_safety_bypass_forbidden")

    if route.get("direct_action_allowed") is True:
        issues.append("task_route_hint_direct_action_forbidden")

    return len(issues) == 0, issues


def align_task_to_guidance_safety_v1(bundle: Dict[str, Any]) -> Dict[str, Any]:
    ok, issues = validate_task_to_guidance_bundle(bundle)
    case_ref = str(bundle.get("case_ref", "unknown"))
    trace_ref = f"task_to_guidance_trace_{case_ref}"
    trace_chain = list(bundle.get("source_chain") or []) + [trace_ref]

    task_trace = bundle.get("task_trace") or {}
    if not ok:
        return {
            "trace_ref": trace_ref,
            "case_ref": case_ref,
            "guidance_ok": False,
            "guidance_evidence_request_candidate": {},
            "guidance_candidate": {},
            "speech_gate_candidate": {},
            "action_safety_candidate": {},
            "guidance_safety_decision": {},
            "guidance_issues": issues,
            "source_chain": trace_chain,
            "candidate_only": True,
        }

    ctx = task_trace.get("task_context_candidate") or {}
    evidence = task_trace.get("task_evidence_need_candidate") or {}
    route = task_trace.get("task_route_hint_candidate") or {}
    risk = task_trace.get("task_risk_candidate") or {}

    route_blocked = route.get("status") == "blocked_or_needs_more_evidence"
    risk_kinds = list(risk.get("risk_kinds") or [])
    has_conflict = "conflict_requires_resolution" in risk_kinds
    high_crowd_risk = any(
        k in risk_kinds for k in ("crowd_density", "queue", "temporary_layout_uncertainty")
    )
    indoor_uncertain = "indoor_navigation_uncertainty" in risk_kinds

    guidance_type = _GUIDANCE_TYPES.get(case_ref, "generic_guidance_hint")
    if route_blocked or has_conflict:
        guidance_status = "blocked_or_needs_more_evidence"
    elif high_crowd_risk or indoor_uncertain:
        guidance_status = "downgraded_cautious"
    else:
        guidance_status = "candidate"

    if bundle.get("force_action_like_guidance") is True:
        guidance_status = "action_like_forbidden"
        guidance_type = "forced_action_like_guidance"

    evidence_request = {
        "candidate_type": "GuidanceEvidenceRequestCandidate",
        "candidate_ref": f"guidance_evidence_request_{case_ref}",
        "evidence_request_id": f"guidance_ev_req_{case_ref}",
        "requested_evidence_kinds": list(_EVIDENCE_REQUESTS.get(case_ref, evidence.get("requested_evidence_kinds") or [])),
        "source_chain": trace_chain + ["guidance_evidence_request_candidate"],
        "guidance_entrypoint": GUIDANCE_ENTRYPOINT,
        "candidate_only": True,
        "live_sensor_trigger_allowed": False,
    }

    guidance = {
        "candidate_type": "GuidanceCandidate",
        "candidate_ref": f"guidance_{case_ref}",
        "guidance_id": f"guidance_{case_ref}",
        "guidance_type": guidance_type,
        "guidance_status": guidance_status,
        "field_label": ctx.get("field_label"),
        "underlying_map_place_ref": ctx.get("underlying_map_place_ref"),
        "source_chain": trace_chain + ["guidance_candidate"],
        "guidance_entrypoint": GUIDANCE_ENTRYPOINT,
        "candidate_only": True,
        "is_navigation_runtime": bundle.get("execute_route_hint_as_navigation") is True,
        "direct_action_allowed": guidance_status == "action_like_forbidden",
    }

    if high_crowd_risk:
        guidance["guidance_action_strength"] = "observe_wait_request_evidence"
    elif route_blocked:
        guidance["guidance_action_strength"] = "explain_only"

    if bundle.get("execute_route_hint_as_navigation") is True:
        guidance["is_navigation_runtime"] = True

    utterance_kind = "explanation" if route_blocked or has_conflict else "guidance_hint"
    if high_crowd_risk:
        utterance_kind = "caution_hint"

    trigger_tts = bundle.get("trigger_tts_output") is True
    speech_gate = {
        "candidate_type": "SpeechGateCandidate",
        "candidate_ref": f"speech_gate_{case_ref}",
        "speech_gate_id": f"speech_gate_{case_ref}",
        "utterance_kind": utterance_kind,
        "wording_hint": f"{ctx.get('field_label')}相关引导候选",
        "source_chain": trace_chain + ["speech_gate_candidate"],
        "speech_gate_entrypoint": SPEECH_GATE_ENTRYPOINT,
        "candidate_only": True,
        "trigger_tts": trigger_tts,
        "direct_speech_allowed": trigger_tts,
        "is_tts_output": False,
    }

    if route_blocked or has_conflict:
        safety_status = "blocked"
        direct_action = False
    elif high_crowd_risk or indoor_uncertain:
        safety_status = "requires_more_evidence"
        direct_action = False
    elif case_ref == "home_return_stable_guidance_candidate":
        safety_status = "pending"
        direct_action = False
    else:
        safety_status = "candidate_clear"
        direct_action = False

    action_safety: Dict[str, Any] = {}
    if bundle.get("skip_action_safety") is not True:
        action_safety = {
            "candidate_type": "ActionSafetyCandidate",
            "candidate_ref": f"action_safety_{case_ref}",
            "safety_id": f"action_safety_{case_ref}",
            "safety_status": safety_status,
            "risk_kinds": risk_kinds,
            "source_chain": trace_chain + ["action_safety_candidate"],
            "action_safety_entrypoint": ACTION_SAFETY_ENTRYPOINT,
            "candidate_only": True,
            "direct_action_allowed": direct_action,
        }
        if high_crowd_risk and "crowd_density" not in risk_kinds:
            action_safety["risk_kinds"] = risk_kinds + ["crowd_density"]

    decision = {
        "decision_ref": f"guidance_safety_decision_{case_ref}",
        "guidance_entrypoint": GUIDANCE_ENTRYPOINT,
        "speech_gate_entrypoint": SPEECH_GATE_ENTRYPOINT,
        "action_safety_entrypoint": ACTION_SAFETY_ENTRYPOINT,
        "action_safety_present": bool(action_safety),
        "real_navigation_started": bundle.get("execute_route_hint_as_navigation") is True,
        "direct_action_allowed": False,
        "direct_speech_allowed": trigger_tts,
        "direct_fact_write_allowed": False,
        "candidate_only": True,
        "source_chain": trace_chain + ["guidance_safety_decision"],
    }

    guidance_ok = True
    out_issues: List[str] = []

    if bundle.get("execute_route_hint_as_navigation") is True:
        guidance_ok = False
        out_issues.append("task_route_hint_as_navigation_action_forbidden")
    if trigger_tts:
        guidance_ok = False
        out_issues.append("speech_gate_tts_output_forbidden")
    if bundle.get("force_action_like_guidance") is True:
        guidance_ok = False
        out_issues.append("conflict_action_like_guidance_forbidden")
    if bundle.get("skip_action_safety") is True:
        guidance_ok = False
        out_issues.append("action_safety_bypass_forbidden")
    if guidance.get("is_navigation_runtime") is True:
        guidance_ok = False
        out_issues.append("guidance_is_navigation_runtime")
    if not action_safety and bundle.get("skip_action_safety") is not True:
        guidance_ok = False
        out_issues.append("action_safety_missing")

    return {
        "trace_ref": trace_ref,
        "case_ref": case_ref,
        "guidance_ok": guidance_ok,
        "guidance_evidence_request_candidate": evidence_request,
        "guidance_candidate": guidance,
        "speech_gate_candidate": speech_gate,
        "action_safety_candidate": action_safety,
        "guidance_safety_decision": decision,
        "guidance_issues": out_issues,
        "source_chain": trace_chain,
        "candidate_only": True,
    }


def evaluate_positive_case(trace: Dict[str, Any], case_ref: str) -> Tuple[bool, List[str]]:
    issues: List[str] = []
    if not trace.get("guidance_ok"):
        issues.append("guidance_failed")
        issues.extend(trace.get("guidance_issues") or [])

    guidance = trace.get("guidance_candidate") or {}
    evidence_req = trace.get("guidance_evidence_request_candidate") or {}
    speech = trace.get("speech_gate_candidate") or {}
    safety = trace.get("action_safety_candidate") or {}
    decision = trace.get("guidance_safety_decision") or {}

    if guidance.get("candidate_only") is not True:
        issues.append("guidance_not_candidate_only")
    if guidance.get("is_navigation_runtime") is True:
        issues.append("guidance_is_navigation_runtime")
    if speech.get("trigger_tts") is True:
        issues.append("speech_gate_triggers_tts")
    if safety.get("direct_action_allowed") is True:
        issues.append("action_safety_direct_action")
    if decision.get("real_navigation_started") is True:
        issues.append("real_navigation_started")
    if not safety:
        issues.append("action_safety_missing")

    if case_ref == "mall_find_entrance_guidance_candidate":
        if guidance.get("guidance_type") != "find_entrance_hint":
            issues.append("guidance_type_mismatch")
        for kind in ("entrance_sign", "doorway", "path_accessibility"):
            if kind not in (evidence_req.get("requested_evidence_kinds") or []):
                issues.append(f"missing_evidence_request:{kind}")

    elif case_ref == "subway_enter_station_guidance_candidate":
        if guidance.get("guidance_type") != "cautious_indoor_guidance_candidate":
            issues.append("guidance_type_mismatch")
        if safety.get("safety_status") != "requires_more_evidence":
            issues.append("action_safety_not_requires_more_evidence")
        for kind in ("station_sign", "gate"):
            if kind not in (evidence_req.get("requested_evidence_kinds") or []):
                issues.append(f"missing_evidence_request:{kind}")

    elif case_ref == "stadium_concert_ticket_gate_guidance_candidate":
        if guidance.get("field_label") != "演唱会现场":
            issues.append("field_label_mismatch")
        if guidance.get("underlying_map_place_ref") != "stadium_stub":
            issues.append("underlying_map_place_ref_mismatch")
        for kind in ("ocr_sign", "ticket_gate"):
            if kind not in (evidence_req.get("requested_evidence_kinds") or []):
                issues.append(f"missing_evidence_request:{kind}")

    elif case_ref == "plaza_market_crowd_safety_guidance_candidate":
        if guidance.get("guidance_action_strength") != "observe_wait_request_evidence":
            issues.append("guidance_not_downgraded")
        if "crowd_density" not in (safety.get("risk_kinds") or []):
            issues.append("missing_crowd_density_risk")

    elif case_ref == "gps_slam_conflict_guidance_blocked":
        if guidance.get("guidance_status") != "blocked_or_needs_more_evidence":
            issues.append("guidance_not_blocked")
        if speech.get("utterance_kind") != "explanation":
            issues.append("speech_gate_not_explanation_only")
        if safety.get("safety_status") != "blocked":
            issues.append("action_safety_not_blocked")

    elif case_ref == "home_return_stable_guidance_candidate":
        if guidance.get("guidance_type") != "coarse_route_with_local_check":
            issues.append("guidance_type_mismatch")
        if safety.get("safety_status") != "pending":
            issues.append("action_safety_not_pending")

    return len(issues) == 0, issues


def build_positive_cases_v1() -> Tuple[Dict[str, Any], ...]:
    bundles = build_positive_input_bundles_v1()
    return tuple(
        {
            "case_ref": case_ref,
            "case_kind": "positive",
            "task_case_ref": bundles[case_ref]["task_case_ref"],
            "input_bundle_ref": bundles[case_ref]["bundle_ref"],
            "expected_outcome": {"guidance_ok": True, "candidate_only": True},
            "input_bundle": bundles[case_ref],
        }
        for case_ref in POSITIVE_CASE_REFS
    )


def build_negative_cases_v1() -> Tuple[Dict[str, Any], ...]:
    bundles = build_negative_input_bundles_v1()
    return tuple(
        {
            "case_ref": case_ref,
            "case_kind": "negative",
            "input_bundle_ref": bundles[case_ref]["bundle_ref"],
            "expected_rejected": True,
            "input_bundle": bundles[case_ref],
        }
        for case_ref in NEGATIVE_CASE_REFS
    )
