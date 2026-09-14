# -*- coding: utf-8 -*-
"""Depth-Object Fusion Skeleton — lineage v1."""

from __future__ import annotations

from typing import Dict, Tuple

FUSION_SKELETON_WHITELIST_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/multi_model_alignment_skeleton_v1.py",
    "tools/evaluation/midplatform/run_multi_model_alignment_skeleton_v1.py",
    "tools/evaluation/midplatform/verify_multi_model_alignment_skeleton_v1.py",
)

FUSION_SKELETON_STAGE_TERM_OVERRIDES: Tuple[Dict[str, str], ...] = (
    {"base_term": "multi_model_alignment_skeleton", "stage_term": "depth_object_fusion_skeleton"},
    {"base_term": "multi_model_alignment_skeleton_only", "stage_term": "depth_object_fusion_skeleton_only"},
    {"base_term": "multi_model_alignment_skeleton_pass", "stage_term": "depth_object_fusion_skeleton_pass"},
)

FUSION_SKELETON_STAGE_ADDITIONS: Tuple[str, ...] = (
    "prior_multi_model_alignment_skeleton_go",
    "depth_object_fusion_skeleton_complete",
    "bbox_depth_sampling_policy_complete",
    "object_depth_hint_candidate_builder_complete",
    "depth_object_fusion_result_assembler_complete",
    "all_mock_cases_passed",
    "readiness_for_field_geometry_ok",
    "no_field_geometry_generation",
    "no_pseudo_3d_position_generation",
    "no_field_scene_assembly",
    "common_validation_reuse_ok",
    "depth_object_fusion_skeleton_only",
    "file_size_governance_review_ok",
)

WHITELIST_FILES: Tuple[str, ...] = FUSION_SKELETON_WHITELIST_FILES + (
    "capabilities/midplatform/field_first_common_validation_v1.py",
    "capabilities/midplatform/depth_object_fusion_types_v1.py",
    "capabilities/midplatform/bbox_depth_sampling_policy_v1.py",
    "capabilities/midplatform/object_depth_hint_candidate_builder_v1.py",
    "capabilities/midplatform/depth_object_fusion_fallback_policy_v1.py",
    "capabilities/midplatform/depth_object_fusion_result_assembler_v1.py",
    "capabilities/midplatform/depth_object_fusion_static_validators_v1.py",
    "capabilities/midplatform/depth_object_fusion_core_v1.py",
    "capabilities/midplatform/depth_object_fusion_skeleton_v1.py",
    "capabilities/midplatform/depth_object_fusion_skeleton_items_v1.py",
    "capabilities/midplatform/depth_object_fusion_skeleton_lineage_v1.py",
    "tools/evaluation/midplatform/run_depth_object_fusion_skeleton_v1.py",
    "tools/evaluation/midplatform/verify_depth_object_fusion_skeleton_v1.py",
)

PHASE_PYTHON_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/depth_object_fusion_types_v1.py",
    "capabilities/midplatform/bbox_depth_sampling_policy_v1.py",
    "capabilities/midplatform/object_depth_hint_candidate_builder_v1.py",
    "capabilities/midplatform/depth_object_fusion_fallback_policy_v1.py",
    "capabilities/midplatform/depth_object_fusion_result_assembler_v1.py",
    "capabilities/midplatform/depth_object_fusion_static_validators_v1.py",
    "capabilities/midplatform/depth_object_fusion_core_v1.py",
    "capabilities/midplatform/depth_object_fusion_skeleton_v1.py",
    "capabilities/midplatform/depth_object_fusion_skeleton_items_v1.py",
    "capabilities/midplatform/depth_object_fusion_skeleton_lineage_v1.py",
    "tools/evaluation/midplatform/run_depth_object_fusion_skeleton_v1.py",
    "tools/evaluation/midplatform/verify_depth_object_fusion_skeleton_v1.py",
)

DOCS: Tuple[str, ...] = (
    "docs/architecture/midplatform/LUNA_MIDPLATFORM_DEPTH_OBJECT_FUSION_SKELETON_V1.md",
    "docs/architecture/evaluation/LUNA_EVALUATION_DEPTH_OBJECT_FUSION_SKELETON_V1.md",
    "docs/architecture/evaluation/LUNA_EVALUATION_DEPTH_OBJECT_FUSION_SKELETON_V1_GO_NO_GO_PACK_V0.md",
)

ARTIFACTS: Tuple[str, ...] = (
    "depth_object_fusion_skeleton_report_v1.json",
    "depth_object_fusion_input_contract_v1.json",
    "bbox_depth_sampling_policy_v1.json",
    "object_depth_hint_candidate_registry_v1.json",
    "depth_object_fusion_result_candidate_registry_v1.json",
    "depth_bucket_field_zone_hint_policy_v1.json",
    "depth_object_fusion_mock_case_results_v1.json",
    "depth_object_fusion_fallback_policy_v1.json",
    "readiness_for_field_geometry_review_v1.json",
    "common_validation_reuse_report_v1.json",
    "non_execution_boundary_review_v1.json",
    "file_size_governance_review_v1.json",
    "prohibited_scope_v1.json",
    "summary.json",
    "verifier_report.json",
)

FINAL_DECISION_GO = (
    "MIDPLATFORM_DEPTH_OBJECT_FUSION_SKELETON_READY_FOR_FIELD_GEOMETRY_CANDIDATE_SKELETON"
)

GO_CONDITIONS_KEYS: Tuple[str, ...] = (
    "prior_multi_model_alignment_skeleton_go",
    "depth_object_fusion_skeleton_complete",
    "bbox_depth_sampling_policy_complete",
    "object_depth_hint_candidate_builder_complete",
    "depth_object_fusion_result_assembler_complete",
    "all_mock_cases_passed",
    "field_zone_hint_assignment_ok",
    "readiness_for_field_geometry_ok",
    "metric_depth_bucket_supported",
    "relative_depth_weak_hint_supported",
    "missing_depth_unknown_hint_supported",
    "rejected_alignment_no_fusion",
    "no_field_geometry_generation",
    "no_pseudo_3d_position_generation",
    "no_field_scene_assembly",
    "common_validation_reuse_ok",
    "no_model_download",
    "no_weight_download",
    "no_real_depth_inference",
    "no_runtime_execution",
    "next_phase_readiness_ok",
)
