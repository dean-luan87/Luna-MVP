# -*- coding: utf-8 -*-
"""Static/Dynamic Target Locking & Tracking Planning lineage v1."""

from __future__ import annotations

from typing import Dict, Tuple

TARGET_LOCKING_TRACKING_PLANNING_WHITELIST_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/field_continuity_detection_controlled_skeleton_implementation_v1.py",
    "tools/evaluation/midplatform/run_field_continuity_detection_controlled_skeleton_implementation_v1.py",
    "tools/evaluation/midplatform/verify_field_continuity_detection_controlled_skeleton_implementation_v1.py",
)

TARGET_LOCKING_TRACKING_PLANNING_STAGE_TERM_OVERRIDES: Tuple[Dict[str, str], ...] = (
    {"base_term": "field_continuity_detection_controlled_skeleton_implementation", "stage_term": "static_dynamic_target_locking_tracking_planning"},
    {"base_term": "field_continuity_detection_controlled_skeleton_only", "stage_term": "static_dynamic_target_locking_tracking_planning_only"},
    {"base_term": "field_continuity_detection_controlled_skeleton_pass", "stage_term": "static_dynamic_target_locking_tracking_planning_pass"},
)

TARGET_LOCKING_TRACKING_PLANNING_STAGE_ADDITIONS: Tuple[str, ...] = (
    "prior_field_continuity_controlled_skeleton_go",
    "target_locking_tracking_planning_complete",
    "target_classification_registry_complete",
    "static_target_lock_model_complete",
    "dynamic_target_track_model_complete",
    "task_impact_hint_policy_complete",
    "mock_cases_complete",
    "static_dynamic_target_locking_tracking_planning_only",
    "file_size_governance_review_ok",
)
