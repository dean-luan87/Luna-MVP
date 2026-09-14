from __future__ import annotations

from typing import Any, Dict, Mapping

from capabilities.midplatform.navigation_manager.module.navigation_manager_module_types_v1 import (
    BOUNDARY_FALSE_FIELDS,
    CAPABILITY_ID,
)


def resolve_navigation_manager_module_status_v1(
    input_candidate: Mapping[str, Any],
    request_classification: Mapping[str, Any],
    route_state: Mapping[str, Any],
    route_memory: Mapping[str, Any],
    evidence_state: Mapping[str, Any],
    crossing_assessment: Mapping[str, Any],
    obstacle_assessment: Mapping[str, Any],
    deviation_assessment: Mapping[str, Any],
    arrival_candidate: Mapping[str, Any],
) -> str:
    if not input_candidate.get("navigation_request_id") or not input_candidate.get(
        "task_id"
    ):
        return "invalid_input"
    if not request_classification.get("navigation_mode_supported"):
        return "invalid_input"
    if bool(
        (input_candidate.get("permission_context") or {}).get("request_rejected", False)
    ):
        return "request_rejected"
    if bool(evidence_state.get("map_visual_conflict", False)):
        return "conflicted"

    mode = str(input_candidate.get("navigation_mode") or "")
    if mode == "pause_navigation":
        return "navigation_paused"

    route_available = bool(route_state.get("route_present")) or bool(
        route_memory.get("route_memory_available")
    )
    if bool(request_classification.get("route_required")) and not route_available:
        return "route_unavailable"
    if mode == "route_memory" and route_available:
        return "route_ready"

    crossing = crossing_assessment.get("crossing_assessment") or {}
    if bool(crossing.get("attention_required", False)):
        return "crossing_attention_required"

    obstacle = obstacle_assessment.get("obstacle_risk_assessment") or {}
    if bool(obstacle.get("attention_required", False)):
        return "obstacle_attention_required"

    deviation = deviation_assessment.get("deviation_assessment") or {}
    if bool(deviation.get("deviation_detected", False)):
        if bool(deviation.get("reroute_candidate")):
            return "reroute_candidate_ready"
        return "deviation_detected"

    arrival = arrival_candidate.get("arrival_candidate") or {}
    if bool(arrival.get("arrived", False)):
        return "arrival_candidate_ready"

    if bool(request_classification.get("visual_evidence_preferred")) and not (
        bool(evidence_state.get("vision_evidence_present"))
        or bool(evidence_state.get("ocr_evidence_present"))
    ):
        return "insufficient_evidence"

    if mode in {"baseline_safety", "crossing_support", "obstacle_support"} and not bool(
        evidence_state.get("vision_evidence_present")
    ):
        return "degraded"

    if route_available:
        return "navigation_active"
    return "guidance_candidate_ready"


def build_navigation_manager_module_output_v1(
    input_candidate: Mapping[str, Any],
    module_status: str,
    route_state: Mapping[str, Any],
    route_memory: Mapping[str, Any],
    progress_state: Mapping[str, Any],
    landmark_assessment: Mapping[str, Any],
    crossing_assessment: Mapping[str, Any],
    obstacle_assessment: Mapping[str, Any],
    deviation_assessment: Mapping[str, Any],
    guidance_candidate: Mapping[str, Any],
    arrival_candidate: Mapping[str, Any],
    task_handoff: Mapping[str, Any],
    speech_handoff: Mapping[str, Any],
    diagnostics: Mapping[str, Any],
    trace_ref: str,
    replay_key: str,
    rejection_reasons: tuple[str, ...],
) -> Dict[str, Any]:
    output = {
        "capability_id": CAPABILITY_ID,
        "module_status": module_status,
        "navigation_request_id": input_candidate.get("navigation_request_id"),
        "task_id": input_candidate.get("task_id"),
        "navigation_mode": input_candidate.get("navigation_mode"),
        "route_state": {
            "route_ref": route_state.get("route_ref"),
            "route_present": route_state.get("route_present"),
            "route_memory_ref": route_memory.get("route_memory_ref"),
            "effective_route_ref": route_memory.get("effective_route_ref"),
        },
        "route_progress_candidate": progress_state.get("route_progress_candidate"),
        "current_position_candidate": progress_state.get("current_position_candidate"),
        "landmark_assessment": landmark_assessment.get("landmark_assessment"),
        "crossing_assessment": crossing_assessment.get("crossing_assessment"),
        "obstacle_risk_assessment": obstacle_assessment.get("obstacle_risk_assessment"),
        "deviation_assessment": deviation_assessment.get("deviation_assessment"),
        "guidance_candidate": guidance_candidate.get("guidance_candidate"),
        "arrival_candidate": arrival_candidate.get("arrival_candidate"),
        "task_handoff_candidate": task_handoff.get("task_handoff_candidate"),
        "speech_handoff_candidate": speech_handoff.get("speech_handoff_candidate"),
        "diagnostics": diagnostics,
        "trace_ref": trace_ref,
        "replay_key": replay_key,
        "rejection_reasons": tuple(rejection_reasons),
        "boundary_flags": {field: False for field in BOUNDARY_FALSE_FIELDS},
        "candidate_only": True,
        "fact_status": "not_fact",
        "write_allowed": False,
    }
    for field in BOUNDARY_FALSE_FIELDS:
        output[field] = False
    return output
