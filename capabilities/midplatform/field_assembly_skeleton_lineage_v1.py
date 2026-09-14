# -*- coding: utf-8 -*-
"""Field Assembly Skeleton — lineage v1."""

from __future__ import annotations

from typing import Dict, Tuple

ASSEMBLY_SKELETON_WHITELIST_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/field_geometry_candidate_skeleton_v1.py",
    "tools/evaluation/midplatform/run_field_geometry_candidate_skeleton_v1.py",
    "tools/evaluation/midplatform/verify_field_geometry_candidate_skeleton_v1.py",
)

ASSEMBLY_SKELETON_STAGE_TERM_OVERRIDES: Tuple[Dict[str, str], ...] = (
    {"base_term": "field_geometry_candidate_skeleton", "stage_term": "field_assembly_skeleton"},
    {"base_term": "field_geometry_candidate_skeleton_only", "stage_term": "field_assembly_skeleton_only"},
    {"base_term": "field_geometry_candidate_skeleton_pass", "stage_term": "field_assembly_skeleton_pass"},
)

ASSEMBLY_SKELETON_STAGE_ADDITIONS: Tuple[str, ...] = (
    "prior_field_geometry_candidate_skeleton_go",
    "field_assembly_skeleton_complete",
    "enhanced_field_entity_builder_complete",
    "enhanced_field_scene_assembler_complete",
    "zone_summary_builder_complete",
    "quality_summary_builder_complete",
    "all_mock_cases_passed",
    "readiness_for_field_first_core_ok",
    "readiness_for_real_model_success_path_ok",
    "no_scene_relation_generation",
    "no_field_simulation",
    "common_validation_reuse_ok",
    "field_assembly_skeleton_only",
    "file_size_governance_review_ok",
)

WHITELIST_FILES: Tuple[str, ...] = ASSEMBLY_SKELETON_WHITELIST_FILES + (
    "capabilities/midplatform/field_first_common_validation_v1.py",
    "capabilities/midplatform/field_assembly_types_v1.py",
    "capabilities/midplatform/enhanced_field_entity_builder_v1.py",
    "capabilities/midplatform/enhanced_field_scene_assembler_v1.py",
    "capabilities/midplatform/field_zone_summary_builder_v1.py",
    "capabilities/midplatform/field_quality_summary_builder_v1.py",
    "capabilities/midplatform/field_assembly_result_assembler_v1.py",
    "capabilities/midplatform/field_assembly_static_validators_v1.py",
    "capabilities/midplatform/field_assembly_core_v1.py",
    "capabilities/midplatform/field_assembly_skeleton_v1.py",
    "capabilities/midplatform/field_assembly_skeleton_items_v1.py",
    "capabilities/midplatform/field_assembly_skeleton_lineage_v1.py",
    "tools/evaluation/midplatform/run_field_assembly_skeleton_v1.py",
    "tools/evaluation/midplatform/verify_field_assembly_skeleton_v1.py",
)

PHASE_PYTHON_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/field_assembly_types_v1.py",
    "capabilities/midplatform/enhanced_field_entity_builder_v1.py",
    "capabilities/midplatform/enhanced_field_scene_assembler_v1.py",
    "capabilities/midplatform/field_zone_summary_builder_v1.py",
    "capabilities/midplatform/field_quality_summary_builder_v1.py",
    "capabilities/midplatform/field_assembly_result_assembler_v1.py",
    "capabilities/midplatform/field_assembly_static_validators_v1.py",
    "capabilities/midplatform/field_assembly_core_v1.py",
    "capabilities/midplatform/field_assembly_skeleton_v1.py",
    "capabilities/midplatform/field_assembly_skeleton_items_v1.py",
    "capabilities/midplatform/field_assembly_skeleton_lineage_v1.py",
    "tools/evaluation/midplatform/run_field_assembly_skeleton_v1.py",
    "tools/evaluation/midplatform/verify_field_assembly_skeleton_v1.py",
)

DOCS: Tuple[str, ...] = (
    "docs/architecture/midplatform/LUNA_MIDPLATFORM_FIELD_ASSEMBLY_SKELETON_V1.md",
    "docs/architecture/evaluation/LUNA_EVALUATION_FIELD_ASSEMBLY_SKELETON_V1.md",
    "docs/architecture/evaluation/LUNA_EVALUATION_FIELD_ASSEMBLY_SKELETON_V1_GO_NO_GO_PACK_V0.md",
)

ARTIFACTS: Tuple[str, ...] = (
    "field_assembly_skeleton_report_v1.json",
    "enhanced_field_entity_candidate_registry_v1.json",
    "enhanced_field_scene_candidate_registry_v1.json",
    "field_assembly_result_candidate_registry_v1.json",
    "field_zone_summary_registry_v1.json",
    "field_scene_quality_summary_registry_v1.json",
    "field_depth_quality_summary_registry_v1.json",
    "field_geometry_quality_summary_registry_v1.json",
    "field_assembly_mock_case_results_v1.json",
    "readiness_for_field_first_core_review_v1.json",
    "readiness_for_real_model_success_path_review_v1.json",
    "common_validation_reuse_report_v1.json",
    "non_execution_boundary_review_v1.json",
    "file_size_governance_review_v1.json",
    "prohibited_scope_v1.json",
    "summary.json",
    "verifier_report.json",
)

FINAL_DECISION_GO = (
    "MIDPLATFORM_FIELD_ASSEMBLY_SKELETON_READY_FOR_YOLO_DEPTH_REAL_FIELD_ASSEMBLY_DRYRUN_PLANNING"
)

GO_CONDITIONS_KEYS: Tuple[str, ...] = (
    "prior_field_geometry_candidate_skeleton_go",
    "field_assembly_skeleton_complete",
    "enhanced_field_entity_builder_complete",
    "enhanced_field_scene_assembler_complete",
    "zone_summary_builder_complete",
    "quality_summary_builder_complete",
    "all_mock_cases_passed",
    "readiness_for_field_first_core_ok",
    "readiness_for_real_model_success_path_ok",
    "object_anchor_required",
    "depth_only_no_entity",
    "geometry_without_object_rejected",
    "no_scene_relation_generation",
    "no_field_simulation",
    "no_world_model_fact_creation",
    "common_validation_reuse_ok",
    "no_model_download",
    "no_weight_download",
    "no_real_depth_inference",
    "no_runtime_execution",
    "next_phase_readiness_ok",
)
