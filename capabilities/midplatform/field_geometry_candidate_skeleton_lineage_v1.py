# -*- coding: utf-8 -*-
"""Field Geometry Candidate Skeleton — lineage v1."""

from __future__ import annotations

from typing import Dict, Tuple

GEOMETRY_SKELETON_WHITELIST_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/depth_object_fusion_skeleton_v1.py",
    "tools/evaluation/midplatform/run_depth_object_fusion_skeleton_v1.py",
    "tools/evaluation/midplatform/verify_depth_object_fusion_skeleton_v1.py",
)

GEOMETRY_SKELETON_STAGE_TERM_OVERRIDES: Tuple[Dict[str, str], ...] = (
    {"base_term": "depth_object_fusion_skeleton", "stage_term": "field_geometry_candidate_skeleton"},
    {"base_term": "depth_object_fusion_skeleton_only", "stage_term": "field_geometry_candidate_skeleton_only"},
    {"base_term": "depth_object_fusion_skeleton_pass", "stage_term": "field_geometry_candidate_skeleton_pass"},
)

GEOMETRY_SKELETON_STAGE_ADDITIONS: Tuple[str, ...] = (
    "prior_depth_object_fusion_skeleton_go",
    "field_geometry_candidate_skeleton_complete",
    "pseudo_3d_projection_policy_complete",
    "field_zone_assignment_policy_complete",
    "geometry_confidence_policy_complete",
    "all_mock_cases_passed",
    "readiness_for_field_assembly_ok",
    "no_field_scene_assembly",
    "no_scene_relation_generation",
    "common_validation_reuse_ok",
    "field_geometry_candidate_skeleton_only",
    "file_size_governance_review_ok",
)

WHITELIST_FILES: Tuple[str, ...] = GEOMETRY_SKELETON_WHITELIST_FILES + (
    "capabilities/midplatform/field_first_common_validation_v1.py",
    "capabilities/midplatform/field_geometry_candidate_types_v1.py",
    "capabilities/midplatform/pseudo_3d_projection_policy_v1.py",
    "capabilities/midplatform/field_zone_assignment_policy_v1.py",
    "capabilities/midplatform/geometry_confidence_policy_v1.py",
    "capabilities/midplatform/field_geometry_candidate_builder_v1.py",
    "capabilities/midplatform/field_geometry_generation_result_assembler_v1.py",
    "capabilities/midplatform/field_geometry_candidate_static_validators_v1.py",
    "capabilities/midplatform/field_geometry_candidate_core_v1.py",
    "capabilities/midplatform/field_geometry_candidate_skeleton_v1.py",
    "capabilities/midplatform/field_geometry_candidate_skeleton_items_v1.py",
    "capabilities/midplatform/field_geometry_candidate_skeleton_lineage_v1.py",
    "tools/evaluation/midplatform/run_field_geometry_candidate_skeleton_v1.py",
    "tools/evaluation/midplatform/verify_field_geometry_candidate_skeleton_v1.py",
)

PHASE_PYTHON_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/field_geometry_candidate_types_v1.py",
    "capabilities/midplatform/pseudo_3d_projection_policy_v1.py",
    "capabilities/midplatform/field_zone_assignment_policy_v1.py",
    "capabilities/midplatform/geometry_confidence_policy_v1.py",
    "capabilities/midplatform/field_geometry_candidate_builder_v1.py",
    "capabilities/midplatform/field_geometry_generation_result_assembler_v1.py",
    "capabilities/midplatform/field_geometry_candidate_static_validators_v1.py",
    "capabilities/midplatform/field_geometry_candidate_core_v1.py",
    "capabilities/midplatform/field_geometry_candidate_skeleton_v1.py",
    "capabilities/midplatform/field_geometry_candidate_skeleton_items_v1.py",
    "capabilities/midplatform/field_geometry_candidate_skeleton_lineage_v1.py",
    "tools/evaluation/midplatform/run_field_geometry_candidate_skeleton_v1.py",
    "tools/evaluation/midplatform/verify_field_geometry_candidate_skeleton_v1.py",
)

DOCS: Tuple[str, ...] = (
    "docs/architecture/midplatform/LUNA_MIDPLATFORM_FIELD_GEOMETRY_CANDIDATE_SKELETON_V1.md",
    "docs/architecture/evaluation/LUNA_EVALUATION_FIELD_GEOMETRY_CANDIDATE_SKELETON_V1.md",
    "docs/architecture/evaluation/LUNA_EVALUATION_FIELD_GEOMETRY_CANDIDATE_SKELETON_V1_GO_NO_GO_PACK_V0.md",
)

ARTIFACTS: Tuple[str, ...] = (
    "field_geometry_candidate_skeleton_report_v1.json",
    "object_spatial_state_candidate_registry_v1.json",
    "field_geometry_candidate_registry_v1.json",
    "pseudo_3d_projection_policy_v1.json",
    "field_zone_assignment_policy_v1.json",
    "geometry_confidence_policy_v1.json",
    "field_geometry_generation_result_registry_v1.json",
    "field_geometry_mock_case_results_v1.json",
    "readiness_for_field_assembly_review_v1.json",
    "common_validation_reuse_report_v1.json",
    "non_execution_boundary_review_v1.json",
    "file_size_governance_review_v1.json",
    "prohibited_scope_v1.json",
    "summary.json",
    "verifier_report.json",
)

FINAL_DECISION_GO = (
    "MIDPLATFORM_FIELD_GEOMETRY_CANDIDATE_SKELETON_READY_FOR_FIELD_ASSEMBLY_SKELETON"
)

GO_CONDITIONS_KEYS: Tuple[str, ...] = (
    "prior_depth_object_fusion_skeleton_go",
    "field_geometry_candidate_skeleton_complete",
    "pseudo_3d_projection_policy_complete",
    "field_zone_assignment_policy_complete",
    "geometry_confidence_policy_complete",
    "all_mock_cases_passed",
    "readiness_for_field_assembly_ok",
    "pseudo_3d_position_generation_supported",
    "metric_depth_zone_assignment_supported",
    "relative_depth_weak_geometry_supported",
    "unknown_depth_geometry_unknown_supported",
    "invalid_bbox_geometry_rejected",
    "geometry_confidence_degradation_supported",
    "no_field_scene_assembly",
    "no_scene_relation_generation",
    "common_validation_reuse_ok",
    "no_model_download",
    "no_weight_download",
    "no_real_depth_inference",
    "no_runtime_execution",
    "next_phase_readiness_ok",
)
