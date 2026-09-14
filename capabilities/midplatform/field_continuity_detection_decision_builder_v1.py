# -*- coding: utf-8 -*-
"""Field Continuity Detection — decision builder v1."""

from __future__ import annotations

import uuid
from typing import Any, Dict, List, Tuple

from capabilities.midplatform.field_continuity_detection_types_v1 import NON_EXECUTION_FLAGS, STATUS_TO_ACTION

DECISION_RULES: Tuple[Dict[str, Any], ...] = (
    {"rule_id": "new_field_strong", "priority": 1},
    {"rule_id": "occlusion_strong", "priority": 2},
    {"rule_id": "recovery_signals", "priority": 3},
    {"rule_id": "long_gap_uncertain", "priority": 4},
    {"rule_id": "field_shift_signals", "priority": 5},
    {"rule_id": "same_field_signals", "priority": 6},
    {"rule_id": "uncertain_fallback", "priority": 7},
)


def _by_id(signals: List[Dict[str, Any]], sid: str) -> Dict[str, Any]:
    return next((s for s in signals if s.get("signal_id") == sid), {})


def build_field_continuity_decision_candidate(
    *,
    previous_field_scene_summary: Dict[str, Any],
    current_field_scene_summary: Dict[str, Any],
    signal_results: List[Dict[str, Any]],
    previous_field_session_state: str = "active",
    previous_field_session_ref: str = "fsess_prev",
) -> Dict[str, Any]:
    loc = _by_id(signal_results, "location_continuity_signal")
    ent = _by_id(signal_results, "key_entity_overlap_signal")
    layout = _by_id(signal_results, "spatial_layout_similarity_signal")
    recovery = _by_id(signal_results, "session_recovery_signal")
    visual = _by_id(signal_results, "visual_quality_change_signal")
    occlusion = _by_id(signal_results, "occlusion_signal")
    heading = _by_id(signal_results, "camera_heading_signal")
    time_gap = _by_id(signal_results, "time_gap_signal")

    supporting: List[str] = []
    reason_codes: List[str] = []
    status = "uncertain_need_recheck"

    if loc.get("support_status") == "supports_new_field" and ent.get("support_status") == "supports_new_field":
        status, reason_codes, supporting = "new_field_required", ["new_field_strong_signals"], ["location_continuity_signal", "key_entity_overlap_signal"]
    elif ent.get("support_status") == "supports_new_field" and layout.get("support_status") == "supports_new_field":
        status, reason_codes, supporting = "new_field_required", ["new_field_strong_signals"], ["key_entity_overlap_signal", "spatial_layout_similarity_signal"]
    elif visual.get("support_status") == "supports_occlusion" or occlusion.get("support_status") == "supports_occlusion":
        if loc.get("support_status") != "supports_new_field":
            status, reason_codes, supporting = "field_occluded", ["occlusion_strong_signals"], [s["signal_id"] for s in (visual, occlusion) if s.get("support_status") == "supports_occlusion"]
    elif recovery.get("support_status") == "supports_recovery" and previous_field_session_state in ("lost", "occluded"):
        status, reason_codes, supporting = "field_recovering", ["recovery_signals"], ["session_recovery_signal"]
    elif time_gap.get("support_status") == "supports_lost":
        status, reason_codes, supporting = "uncertain_need_recheck", ["long_gap_uncertain"], ["time_gap_signal"]
    elif heading.get("support_status") == "supports_field_shift":
        status, reason_codes, supporting = "field_shift", ["field_shift_signals"], ["camera_heading_signal"]
    elif ent.get("support_status") == "supports_same_field" and layout.get("support_status") == "supports_same_field":
        status, reason_codes, supporting = "same_field", ["same_field_signals"], ["key_entity_overlap_signal", "spatial_layout_similarity_signal"]
    elif ent.get("support_status") == "supports_same_field" and heading.get("support_status") == "supports_same_field":
        status, reason_codes, supporting = "same_field", ["same_field_signals"], ["key_entity_overlap_signal", "camera_heading_signal"]
    elif ent.get("support_status") == "supports_same_field" and loc.get("support_status") == "supports_uncertain" and layout.get("support_status") == "supports_same_field":
        status, reason_codes, supporting = "same_field", ["same_field_without_location"], ["key_entity_overlap_signal", "spatial_layout_similarity_signal"]
    elif ent.get("support_status") == "supports_uncertain":
        status, reason_codes, supporting = "uncertain_need_recheck", ["uncertain_fallback"], ["key_entity_overlap_signal"]
    elif occlusion.get("support_status") == "supports_lost":
        status, reason_codes, supporting = "field_lost", ["long_occlusion_lost"], ["occlusion_signal"]
    else:
        status, reason_codes, supporting = "uncertain_need_recheck", ["uncertain_fallback"], []

    action = STATUS_TO_ACTION[status]
    return {
        "continuity_decision_id": f"fcd_{uuid.uuid4().hex[:12]}",
        "previous_field_scene_ref": previous_field_scene_summary.get("field_scene_id", "fs_prev"),
        "current_field_scene_ref": current_field_scene_summary.get("field_scene_id", "fs_curr"),
        "previous_field_session_ref": previous_field_session_ref,
        "recommended_field_session_ref": previous_field_session_ref if status != "new_field_required" else f"{previous_field_session_ref}_new_candidate",
        "continuity_status": status,
        "continuity_confidence": min(0.95, 0.5 + 0.1 * max(len(supporting), 1)),
        "signal_results": signal_results,
        "supporting_signals": supporting,
        "conflicting_signals": [],
        "reason_codes": reason_codes,
        "missing_information": [],
        "recommended_action": action,
        "should_keep_field_session": status != "new_field_required",
        "should_create_new_field_session": status == "new_field_required",
        "should_request_recheck": status == "uncertain_need_recheck",
        "non_execution_flags": dict(NON_EXECUTION_FLAGS),
    }
