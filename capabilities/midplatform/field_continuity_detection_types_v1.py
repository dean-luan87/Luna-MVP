# -*- coding: utf-8 -*-
"""Field Continuity Detection — types v1."""

from __future__ import annotations

from typing import Any, Dict, Tuple

SUPPORT_STATUSES: Tuple[str, ...] = (
    "supports_same_field", "supports_field_shift", "supports_occlusion",
    "supports_lost", "supports_recovery", "supports_new_field", "supports_uncertain",
)

CONTINUITY_STATUSES: Tuple[str, ...] = (
    "same_field", "field_shift", "field_occluded", "field_lost", "field_recovering",
    "new_field_required", "uncertain_need_recheck",
)

RECOMMENDED_ACTIONS: Tuple[str, ...] = (
    "keep_session", "keep_session_with_shift", "mark_occluded", "mark_lost",
    "attempt_recovery", "create_new_session_candidate", "request_recheck_observation",
)

STATUS_TO_ACTION: Dict[str, str] = {
    "same_field": "keep_session",
    "field_shift": "keep_session_with_shift",
    "field_occluded": "mark_occluded",
    "field_lost": "mark_lost",
    "field_recovering": "attempt_recovery",
    "new_field_required": "create_new_session_candidate",
    "uncertain_need_recheck": "request_recheck_observation",
}

STATUS_TO_SESSION_STATE: Dict[str, str] = {
    "same_field": "active",
    "field_shift": "shifted",
    "field_occluded": "occluded",
    "field_lost": "lost",
    "field_recovering": "recovering",
    "new_field_required": "replaced",
    "uncertain_need_recheck": "active",
}

SIGNAL_RESULT_FIELDS: Tuple[str, ...] = (
    "signal_id", "signal_type", "score", "support_status", "confidence",
    "reason_codes", "missing_information", "candidate_only",
)

DECISION_FIELDS: Tuple[str, ...] = (
    "continuity_decision_id", "previous_field_scene_ref", "current_field_scene_ref",
    "previous_field_session_ref", "recommended_field_session_ref", "continuity_status",
    "continuity_confidence", "signal_results", "supporting_signals", "conflicting_signals",
    "reason_codes", "missing_information", "recommended_action", "should_keep_field_session",
    "should_create_new_field_session", "should_request_recheck", "non_execution_flags",
)

NON_EXECUTION_FLAGS: Dict[str, bool] = {
    "candidate_only": True,
    "no_world_model_fact": True,
    "no_persistent_memory": True,
    "no_runtime_execution": True,
    "no_tracking_execution": True,
    "no_trajectory_simulation": True,
}
