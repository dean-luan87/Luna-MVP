# -*- coding: utf-8 -*-
"""Static/Dynamic Target Locking & Tracking — types v1."""

from __future__ import annotations

from typing import Dict, Tuple

STATIC_LOCK_FIELDS: Tuple[str, ...] = (
    "lock_candidate_id", "field_session_ref", "field_scene_ref", "entity_candidate_ref",
    "label", "bbox", "pseudo_3d_position", "field_zone", "confidence", "lock_status",
    "visibility_status", "stability_score", "anchor_candidate", "task_impact_hint",
    "source_refs", "evidence_refs", "reason_codes", "candidate_only",
)

DYNAMIC_TRACK_FIELDS: Tuple[str, ...] = (
    "track_candidate_id", "field_session_ref", "previous_entity_candidate_ref",
    "current_entity_candidate_ref", "label", "previous_bbox", "current_bbox",
    "previous_pseudo_3d_position", "current_pseudo_3d_position", "visibility_status",
    "motion_status", "lock_status", "tracker_hint_id", "tracker_id_is_hint_not_fact",
    "continuity_confidence", "task_impact_hint", "source_refs", "evidence_refs",
    "reason_codes", "candidate_only",
)

IMPACT_FIELDS: Tuple[str, ...] = (
    "impact_candidate_id", "target_ref", "label", "priority_level", "task_impact_hint",
    "safety_relevant", "task_relevant", "background_only", "reason_codes", "candidate_only",
)

PLAN_FIELDS: Tuple[str, ...] = (
    "plan_candidate_id", "field_session_ref", "continuity_status", "static_locks",
    "dynamic_tracks", "target_impacts", "tracking_allowed", "tracking_frozen",
    "tracking_reset", "reason_codes", "non_execution_flags",
)

NON_EXECUTION_FLAGS: Dict[str, bool] = {
    "candidate_only": True,
    "no_world_model_fact": True,
    "no_persistent_memory": True,
    "no_runtime_execution": True,
    "no_real_tracking_execution": True,
    "no_trajectory_prediction": True,
    "tracker_id_is_hint_not_fact": True,
}

CONTINUITY_ALLOWED: Tuple[str, ...] = ("same_field", "field_shift", "field_recovering")
CONTINUITY_FREEZE: Tuple[str, ...] = ("field_occluded",)
CONTINUITY_LOST: Tuple[str, ...] = ("field_lost",)
CONTINUITY_RESET: Tuple[str, ...] = ("new_field_required",)
