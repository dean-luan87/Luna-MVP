# -*- coding: utf-8 -*-
"""Static/Dynamic Target Locking Tracking Controlled Skeleton lineage v1."""

from __future__ import annotations

from typing import Dict, Tuple

TARGET_LOCKING_SKELETON_WHITELIST_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/static_dynamic_target_locking_tracking_planning_v1.py",
    "tools/evaluation/midplatform/run_static_dynamic_target_locking_tracking_planning_v1.py",
    "tools/evaluation/midplatform/verify_static_dynamic_target_locking_tracking_planning_v1.py",
)

TARGET_LOCKING_SKELETON_STAGE_TERM_OVERRIDES: Tuple[Dict[str, str], ...] = (
    {"base_term": "static_dynamic_target_locking_tracking_planning", "stage_term": "static_dynamic_target_locking_tracking_controlled_skeleton_implementation"},
    {"base_term": "static_dynamic_target_locking_tracking_planning_only", "stage_term": "static_dynamic_target_locking_tracking_controlled_skeleton_only"},
    {"base_term": "static_dynamic_target_locking_tracking_planning_pass", "stage_term": "static_dynamic_target_locking_tracking_controlled_skeleton_pass"},
)

TARGET_LOCKING_SKELETON_STAGE_ADDITIONS: Tuple[str, ...] = (
    "prior_static_dynamic_target_locking_tracking_planning_go",
    "controlled_skeleton_implementation_complete",
    "static_lock_builder_complete",
    "dynamic_track_builder_complete",
    "task_impact_scorer_complete",
    "all_mock_cases_passed",
    "target_tracking_plan_generated",
    "implementation_not_split_into_subphases",
    "strong_coupled_single_package_ok",
    "file_size_governance_review_ok",
)
