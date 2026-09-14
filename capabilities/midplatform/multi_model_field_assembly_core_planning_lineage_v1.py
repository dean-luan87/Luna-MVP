# -*- coding: utf-8 -*-
"""Multi-Model Field Assembly Core Planning — lineage v1."""

from __future__ import annotations

from typing import Dict, Tuple

MULTI_MODEL_PLANNING_WHITELIST_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/depth_observation_candidate_ingestion_skeleton_v1.py",
    "tools/evaluation/midplatform/run_depth_observation_candidate_ingestion_skeleton_v1.py",
    "tools/evaluation/midplatform/verify_depth_observation_candidate_ingestion_skeleton_v1.py",
)

MULTI_MODEL_PLANNING_STAGE_TERM_OVERRIDES: Tuple[Dict[str, str], ...] = (
    {"base_term": "depth_observation_candidate_ingestion_skeleton", "stage_term": "multi_model_field_assembly_core_planning"},
    {"base_term": "depth_observation_candidate_ingestion_skeleton_only", "stage_term": "multi_model_field_assembly_core_planning_only"},
    {"base_term": "depth_observation_candidate_ingestion_skeleton_pass", "stage_term": "multi_model_field_assembly_core_planning_pass"},
)

MULTI_MODEL_PLANNING_STAGE_ADDITIONS: Tuple[str, ...] = (
    "prior_depth_observation_ingestion_skeleton_go",
    "multi_model_field_assembly_core_planning_complete",
    "multi_model_interaction_policy_complete",
    "field_assembly_plan_complete",
    "field_geometry_candidate_contract_complete",
    "aligned_observation_candidate_contract_complete",
    "conflict_and_missing_fallback_policy_complete",
    "route_focus_shifted_to_multi_model_field_assembly",
    "no_repeat_detector_planning",
    "no_single_depth_only_route",
    "common_validation_reuse_ok",
    "multi_model_field_assembly_core_planning_only",
    "file_size_governance_review_ok",
)

WHITELIST_FILES: Tuple[str, ...] = MULTI_MODEL_PLANNING_WHITELIST_FILES + (
    "capabilities/midplatform/field_first_common_validation_v1.py",
    "capabilities/midplatform/multi_model_field_assembly_core_planning_v1.py",
    "capabilities/midplatform/multi_model_field_assembly_core_planning_items_v1.py",
    "capabilities/midplatform/multi_model_field_assembly_core_planning_lineage_v1.py",
    "tools/evaluation/midplatform/run_multi_model_field_assembly_core_planning_v1.py",
    "tools/evaluation/midplatform/verify_multi_model_field_assembly_core_planning_v1.py",
)

PHASE_PYTHON_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/multi_model_field_assembly_core_planning_v1.py",
    "capabilities/midplatform/multi_model_field_assembly_core_planning_items_v1.py",
    "capabilities/midplatform/multi_model_field_assembly_core_planning_lineage_v1.py",
    "tools/evaluation/midplatform/run_multi_model_field_assembly_core_planning_v1.py",
    "tools/evaluation/midplatform/verify_multi_model_field_assembly_core_planning_v1.py",
)

DOCS: Tuple[str, ...] = (
    "docs/architecture/midplatform/LUNA_MIDPLATFORM_MULTI_MODEL_FIELD_ASSEMBLY_CORE_PLANNING_V1.md",
    "docs/architecture/evaluation/LUNA_EVALUATION_MULTI_MODEL_FIELD_ASSEMBLY_CORE_PLANNING_V1.md",
    "docs/architecture/evaluation/LUNA_EVALUATION_MULTI_MODEL_FIELD_ASSEMBLY_CORE_PLANNING_V1_GO_NO_GO_PACK_V0.md",
)

ARTIFACTS: Tuple[str, ...] = (
    "multi_model_field_assembly_core_planning_report_v1.json",
    "multi_model_role_registry_v1.json",
    "multi_model_interaction_policy_v1.json",
    "multi_model_alignment_policy_v1.json",
    "object_depth_linking_policy_v1.json",
    "confidence_fusion_policy_v1.json",
    "conflict_handling_policy_v1.json",
    "missing_model_fallback_policy_v1.json",
    "field_geometry_candidate_contract_v1.json",
    "multi_model_aligned_observation_candidate_contract_v1.json",
    "field_assembly_result_candidate_contract_v1.json",
    "field_assembly_plan_v1.json",
    "multi_model_field_assembly_mock_case_registry_v1.json",
    "next_implementation_sequence_v1.json",
    "prohibited_scope_v1.json",
    "common_validation_reuse_report_v1.json",
    "file_size_governance_review_v1.json",
    "summary.json",
    "verifier_report.json",
)

FINAL_DECISION_GO = (
    "MIDPLATFORM_MULTI_MODEL_FIELD_ASSEMBLY_CORE_PLANNING_READY_FOR_MULTI_MODEL_ALIGNMENT_SKELETON"
)

GO_CONDITIONS_KEYS: Tuple[str, ...] = (
    "prior_depth_observation_ingestion_skeleton_go",
    "yolo_detector_already_integrated",
    "route_focus_shifted_to_multi_model_field_assembly",
    "multi_model_field_assembly_core_planning_complete",
    "multi_model_interaction_policy_complete",
    "field_assembly_plan_complete",
    "field_geometry_candidate_contract_complete",
    "aligned_observation_candidate_contract_complete",
    "conflict_and_missing_fallback_policy_complete",
    "no_repeat_detector_planning",
    "no_single_depth_only_route",
    "model_interaction_core_question_answered",
    "field_assembly_core_question_answered",
    "no_weight_download",
    "no_large_dependency_install",
    "no_real_multi_model_runtime",
    "no_slam_runtime",
    "no_scene_graph_runtime",
    "no_field_simulation",
    "no_task_execution",
    "no_runtime_execution",
    "no_world_model_fact_creation",
    "candidate_only_outputs",
    "common_validation_reuse_ok",
    "next_phase_readiness_ok",
)
