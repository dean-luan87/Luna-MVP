# -*- coding: utf-8 -*-
"""Field Continuity Detection Planning lineage v1."""

from __future__ import annotations

from typing import Dict, Tuple

FIELD_CONTINUITY_PLANNING_WHITELIST_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/field_scene_small_range_construction_core_definition_v1.py",
    "tools/evaluation/midplatform/run_field_scene_small_range_construction_core_definition_v1.py",
    "tools/evaluation/midplatform/verify_field_scene_small_range_construction_core_definition_v1.py",
)

FIELD_CONTINUITY_PLANNING_STAGE_TERM_OVERRIDES: Tuple[Dict[str, str], ...] = (
    {"base_term": "field_scene_small_range_construction_core_definition", "stage_term": "field_continuity_detection_planning"},
    {"base_term": "field_scene_small_range_construction_only", "stage_term": "field_continuity_detection_planning_only"},
    {"base_term": "field_scene_small_range_construction_pass", "stage_term": "field_continuity_detection_planning_pass"},
)

FIELD_CONTINUITY_PLANNING_STAGE_ADDITIONS: Tuple[str, ...] = (
    "prior_field_scene_small_range_construction_go",
    "field_continuity_detection_planning_complete",
    "signal_registry_complete",
    "decision_model_complete",
    "field_session_state_machine_complete",
    "abnormal_case_policy_complete",
    "mock_cases_complete",
    "field_continuity_detection_planning_only",
    "file_size_governance_review_ok",
)
