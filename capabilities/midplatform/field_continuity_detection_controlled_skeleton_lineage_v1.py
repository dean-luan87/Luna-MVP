# -*- coding: utf-8 -*-
"""Field Continuity Detection Controlled Skeleton lineage v1."""

from __future__ import annotations

from typing import Dict, Tuple

FIELD_CONTINUITY_SKELETON_WHITELIST_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/field_continuity_detection_planning_v1.py",
    "tools/evaluation/midplatform/run_field_continuity_detection_planning_v1.py",
    "tools/evaluation/midplatform/verify_field_continuity_detection_planning_v1.py",
)

FIELD_CONTINUITY_SKELETON_STAGE_TERM_OVERRIDES: Tuple[Dict[str, str], ...] = (
    {"base_term": "field_continuity_detection_planning", "stage_term": "field_continuity_detection_controlled_skeleton_implementation"},
    {"base_term": "field_continuity_detection_planning_only", "stage_term": "field_continuity_detection_controlled_skeleton_only"},
    {"base_term": "field_continuity_detection_planning_pass", "stage_term": "field_continuity_detection_controlled_skeleton_pass"},
)

FIELD_CONTINUITY_SKELETON_STAGE_ADDITIONS: Tuple[str, ...] = (
    "prior_field_continuity_detection_planning_go",
    "controlled_skeleton_implementation_complete",
    "signal_scoring_complete",
    "decision_builder_complete",
    "state_transition_validator_complete",
    "all_mock_cases_passed",
    "implementation_not_split_into_subphases",
    "strong_coupled_single_package_ok",
    "file_size_governance_review_ok",
)
