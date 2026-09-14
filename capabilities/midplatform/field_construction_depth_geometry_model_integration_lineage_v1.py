# -*- coding: utf-8 -*-
"""Field Construction Depth Geometry Model Integration Planning — lineage v1."""

from __future__ import annotations

from typing import Dict, Tuple

DEPTH_GEOMETRY_PLANNING_WHITELIST_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/real_observation_candidate_ingestion_skeleton_v1.py",
    "tools/evaluation/midplatform/run_real_observation_candidate_ingestion_skeleton_v1.py",
    "tools/evaluation/midplatform/verify_real_observation_candidate_ingestion_skeleton_v1.py",
)

DEPTH_GEOMETRY_PLANNING_STAGE_TERM_OVERRIDES: Tuple[Dict[str, str], ...] = (
    {"base_term": "real_observation_candidate_ingestion_skeleton", "stage_term": "field_construction_depth_geometry_model_integration_planning"},
    {"base_term": "real_observation_candidate_ingestion_skeleton_only", "stage_term": "field_construction_depth_geometry_model_integration_planning_only"},
    {"base_term": "real_observation_candidate_ingestion_skeleton_pass", "stage_term": "field_construction_depth_geometry_model_integration_planning_pass"},
)

DEPTH_GEOMETRY_PLANNING_STAGE_ADDITIONS: Tuple[str, ...] = (
    "prior_real_observation_ingestion_skeleton_go",
    "field_construction_depth_geometry_model_integration_planning_complete",
    "depth_model_adapter_plan_complete",
    "depth_observation_candidate_contract_complete",
    "object_depth_hint_candidate_contract_complete",
    "field_geometry_candidate_contract_complete",
    "yolo_depth_fusion_mapping_complete",
    "spatial_relation_candidate_contract_complete",
    "field_construction_model_priority_plan_complete",
    "depth_unreliable_fallback_policy_complete",
    "no_repeat_detector_planning",
    "common_validation_reuse_ok",
    "field_construction_depth_geometry_model_integration_planning_only",
    "file_size_governance_review_ok",
)

WHITELIST_FILES: Tuple[str, ...] = DEPTH_GEOMETRY_PLANNING_WHITELIST_FILES + (
    "capabilities/midplatform/field_first_common_validation_v1.py",
    "capabilities/midplatform/field_construction_depth_geometry_model_integration_planning_v1.py",
    "capabilities/midplatform/field_construction_depth_geometry_model_integration_items_v1.py",
    "capabilities/midplatform/field_construction_depth_geometry_model_integration_lineage_v1.py",
    "tools/evaluation/midplatform/run_field_construction_depth_geometry_model_integration_planning_v1.py",
    "tools/evaluation/midplatform/verify_field_construction_depth_geometry_model_integration_planning_v1.py",
)

PHASE_PYTHON_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/field_construction_depth_geometry_model_integration_planning_v1.py",
    "capabilities/midplatform/field_construction_depth_geometry_model_integration_items_v1.py",
    "capabilities/midplatform/field_construction_depth_geometry_model_integration_lineage_v1.py",
    "tools/evaluation/midplatform/run_field_construction_depth_geometry_model_integration_planning_v1.py",
    "tools/evaluation/midplatform/verify_field_construction_depth_geometry_model_integration_planning_v1.py",
)

DOCS: Tuple[str, ...] = (
    "docs/architecture/midplatform/LUNA_MIDPLATFORM_FIELD_CONSTRUCTION_DEPTH_GEOMETRY_MODEL_INTEGRATION_PLANNING_V1.md",
    "docs/architecture/evaluation/LUNA_EVALUATION_FIELD_CONSTRUCTION_DEPTH_GEOMETRY_MODEL_INTEGRATION_PLANNING_V1.md",
    "docs/architecture/evaluation/LUNA_EVALUATION_FIELD_CONSTRUCTION_DEPTH_GEOMETRY_MODEL_INTEGRATION_PLANNING_V1_GO_NO_GO_PACK_V0.md",
)

ARTIFACTS: Tuple[str, ...] = (
    "field_construction_depth_geometry_model_integration_planning_report_v1.json",
    "depth_model_adapter_plan_v1.json",
    "depth_observation_candidate_contract_v1.json",
    "object_depth_hint_candidate_contract_v1.json",
    "field_geometry_candidate_contract_v1.json",
    "yolo_depth_fusion_mapping_v1.json",
    "spatial_relation_candidate_contract_v1.json",
    "field_construction_model_priority_plan_v1.json",
    "field_geometry_adapter_plan_v1.json",
    "depth_unreliable_fallback_execution_policy_v1.json",
    "streaming_3d_slam_candidate_review_v1.json",
    "scene_graph_spatial_relation_review_v1.json",
    "field_scene_candidate_enhancement_plan_v1.json",
    "depth_model_download_authorization_status_v1.json",
    "field_construction_planning_case_registry_v1.json",
    "field_construction_planning_rules_v1.json",
    "prohibited_scope_v1.json",
    "common_validation_reuse_report_v1.json",
    "file_size_governance_review_v1.json",
    "summary.json",
    "verifier_report.json",
)

FINAL_DECISION_GO = (
    "MIDPLATFORM_FIELD_CONSTRUCTION_DEPTH_GEOMETRY_MODEL_INTEGRATION_PLANNING_READY_FOR_DEPTH_OBSERVATION_CANDIDATE_INGESTION_SKELETON"
)

GO_CONDITIONS_KEYS: Tuple[str, ...] = (
    "prior_real_observation_ingestion_skeleton_go",
    "field_construction_depth_geometry_model_integration_planning_complete",
    "depth_model_adapter_plan_complete",
    "depth_observation_candidate_contract_complete",
    "object_depth_hint_candidate_contract_complete",
    "field_geometry_candidate_contract_complete",
    "yolo_depth_fusion_mapping_complete",
    "spatial_relation_candidate_contract_complete",
    "field_construction_model_priority_plan_complete",
    "depth_unreliable_fallback_policy_complete",
    "no_repeat_detector_planning",
    "no_weight_download",
    "no_large_dependency_install",
    "no_production_depth_model_selection",
    "no_slam_runtime",
    "no_scene_graph_runtime",
    "no_field_simulation",
    "no_task_execution",
    "no_runtime_execution",
    "no_world_model_fact_creation",
    "candidate_only_outputs",
    "common_validation_reuse_ok",
    "next_phase_readiness_ok",
    "first_batch_scope_limited_to_depth_and_geometry",
    "yolo_depth_alignment_defined",
    "pseudo_3d_field_scene_path_defined",
)
