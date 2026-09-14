# -*- coding: utf-8 -*-
"""Field Scene Small Range Construction template lineage v1."""

from __future__ import annotations

from typing import Dict, Tuple

FIELD_SCENE_SMALL_RANGE_WHITELIST_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/field_first_core_model_io_compatibility_precheck_v1.py",
    "tools/evaluation/midplatform/run_field_first_core_model_io_compatibility_precheck_v1.py",
    "tools/evaluation/midplatform/verify_field_first_core_model_io_compatibility_precheck_v1.py",
)

FIELD_SCENE_SMALL_RANGE_STAGE_TERM_OVERRIDES: Tuple[Dict[str, str], ...] = (
    {"base_term": "field_first_core_model_io_compatibility_precheck", "stage_term": "field_scene_small_range_construction_core_definition"},
    {"base_term": "field_first_core_model_io_precheck_only", "stage_term": "field_scene_small_range_construction_only"},
    {"base_term": "field_first_core_model_io_compatibility_precheck_pass", "stage_term": "field_scene_small_range_construction_pass"},
)

FIELD_SCENE_SMALL_RANGE_STAGE_ADDITIONS: Tuple[str, ...] = (
    "prior_model_io_compatibility_precheck_go",
    "small_range_field_scene_construction_complete",
    "field_scene_candidate_generated",
    "field_entity_candidates_generated",
    "depth_uncertainty_policy_complete",
    "field_zone_assignment_policy_complete",
    "mock_cases_all_passed",
    "field_scene_small_range_construction_only",
    "file_size_governance_review_ok",
)
