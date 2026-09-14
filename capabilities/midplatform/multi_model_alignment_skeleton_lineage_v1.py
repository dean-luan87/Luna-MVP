# -*- coding: utf-8 -*-
"""Multi-Model Alignment Skeleton — lineage v1."""

from __future__ import annotations

from typing import Dict, Tuple

ALIGNMENT_SKELETON_WHITELIST_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/multi_model_field_assembly_core_planning_v1.py",
    "tools/evaluation/midplatform/run_multi_model_field_assembly_core_planning_v1.py",
    "tools/evaluation/midplatform/verify_multi_model_field_assembly_core_planning_v1.py",
)

ALIGNMENT_SKELETON_STAGE_TERM_OVERRIDES: Tuple[Dict[str, str], ...] = (
    {"base_term": "multi_model_field_assembly_core_planning", "stage_term": "multi_model_alignment_skeleton"},
    {"base_term": "multi_model_field_assembly_core_planning_only", "stage_term": "multi_model_alignment_skeleton_only"},
    {"base_term": "multi_model_field_assembly_core_planning_pass", "stage_term": "multi_model_alignment_skeleton_pass"},
)

ALIGNMENT_SKELETON_STAGE_ADDITIONS: Tuple[str, ...] = (
    "prior_multi_model_field_assembly_planning_go",
    "multi_model_alignment_skeleton_complete",
    "alignment_signal_scoring_complete",
    "alignment_builder_complete",
    "alignment_result_assembler_complete",
    "all_mock_cases_passed",
    "readiness_for_depth_object_fusion_ok",
    "no_depth_object_fusion",
    "no_field_geometry_generation",
    "no_field_scene_assembly",
    "common_validation_reuse_ok",
    "multi_model_alignment_skeleton_only",
    "file_size_governance_review_ok",
)

WHITELIST_FILES: Tuple[str, ...] = ALIGNMENT_SKELETON_WHITELIST_FILES + (
    "capabilities/midplatform/field_first_common_validation_v1.py",
    "capabilities/midplatform/multi_model_alignment_types_v1.py",
    "capabilities/midplatform/multi_model_alignment_signal_scoring_v1.py",
    "capabilities/midplatform/multi_model_alignment_builder_v1.py",
    "capabilities/midplatform/multi_model_alignment_result_assembler_v1.py",
    "capabilities/midplatform/multi_model_alignment_static_validators_v1.py",
    "capabilities/midplatform/multi_model_alignment_core_v1.py",
    "capabilities/midplatform/multi_model_alignment_skeleton_v1.py",
    "capabilities/midplatform/multi_model_alignment_skeleton_items_v1.py",
    "capabilities/midplatform/multi_model_alignment_skeleton_lineage_v1.py",
    "tools/evaluation/midplatform/run_multi_model_alignment_skeleton_v1.py",
    "tools/evaluation/midplatform/verify_multi_model_alignment_skeleton_v1.py",
)

PHASE_PYTHON_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/multi_model_alignment_types_v1.py",
    "capabilities/midplatform/multi_model_alignment_signal_scoring_v1.py",
    "capabilities/midplatform/multi_model_alignment_builder_v1.py",
    "capabilities/midplatform/multi_model_alignment_result_assembler_v1.py",
    "capabilities/midplatform/multi_model_alignment_static_validators_v1.py",
    "capabilities/midplatform/multi_model_alignment_core_v1.py",
    "capabilities/midplatform/multi_model_alignment_skeleton_v1.py",
    "capabilities/midplatform/multi_model_alignment_skeleton_items_v1.py",
    "capabilities/midplatform/multi_model_alignment_skeleton_lineage_v1.py",
    "tools/evaluation/midplatform/run_multi_model_alignment_skeleton_v1.py",
    "tools/evaluation/midplatform/verify_multi_model_alignment_skeleton_v1.py",
)

DOCS: Tuple[str, ...] = (
    "docs/architecture/midplatform/LUNA_MIDPLATFORM_MULTI_MODEL_ALIGNMENT_SKELETON_V1.md",
    "docs/architecture/evaluation/LUNA_EVALUATION_MULTI_MODEL_ALIGNMENT_SKELETON_V1.md",
    "docs/architecture/evaluation/LUNA_EVALUATION_MULTI_MODEL_ALIGNMENT_SKELETON_V1_GO_NO_GO_PACK_V0.md",
)

ARTIFACTS: Tuple[str, ...] = (
    "multi_model_alignment_skeleton_report_v1.json",
    "multi_model_alignment_input_contract_v1.json",
    "alignment_signal_registry_v1.json",
    "multi_model_aligned_observation_candidate_registry_v1.json",
    "multi_model_alignment_result_candidate_registry_v1.json",
    "multi_model_alignment_mock_case_results_v1.json",
    "rejected_alignment_policy_v1.json",
    "missing_model_roles_summary_v1.json",
    "readiness_for_depth_object_fusion_review_v1.json",
    "common_validation_reuse_report_v1.json",
    "non_execution_boundary_review_v1.json",
    "file_size_governance_review_v1.json",
    "prohibited_scope_v1.json",
    "summary.json",
    "verifier_report.json",
)

FINAL_DECISION_GO = (
    "MIDPLATFORM_MULTI_MODEL_ALIGNMENT_SKELETON_READY_FOR_DEPTH_OBJECT_FUSION_SKELETON"
)

GO_CONDITIONS_KEYS: Tuple[str, ...] = (
    "prior_multi_model_field_assembly_planning_go",
    "multi_model_alignment_skeleton_complete",
    "alignment_signal_scoring_complete",
    "alignment_builder_complete",
    "alignment_result_assembler_complete",
    "all_mock_cases_passed",
    "missing_model_roles_handled",
    "rejected_alignment_policy_ok",
    "readiness_for_depth_object_fusion_ok",
    "frame_ref_alignment_supported",
    "timestamp_alignment_supported",
    "camera_ref_alignment_supported",
    "frame_size_alignment_supported",
    "missing_depth_keeps_object",
    "depth_without_object_no_entity_alignment",
    "no_depth_object_fusion",
    "no_field_geometry_generation",
    "no_field_scene_assembly",
    "common_validation_reuse_ok",
    "no_model_download",
    "no_weight_download",
    "no_real_multi_model_runtime",
    "no_runtime_execution",
    "next_phase_readiness_ok",
)
