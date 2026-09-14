# -*- coding: utf-8 -*-
"""Depth Observation Candidate Ingestion Skeleton — lineage v1."""

from __future__ import annotations

from typing import Dict, Tuple

DEPTH_INGESTION_SKELETON_WHITELIST_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/field_construction_depth_geometry_model_integration_planning_v1.py",
    "tools/evaluation/midplatform/run_field_construction_depth_geometry_model_integration_planning_v1.py",
    "tools/evaluation/midplatform/verify_field_construction_depth_geometry_model_integration_planning_v1.py",
)

DEPTH_INGESTION_SKELETON_STAGE_TERM_OVERRIDES: Tuple[Dict[str, str], ...] = (
    {"base_term": "field_construction_depth_geometry_model_integration_planning", "stage_term": "depth_observation_candidate_ingestion_skeleton"},
    {"base_term": "field_construction_depth_geometry_model_integration_planning_only", "stage_term": "depth_observation_candidate_ingestion_skeleton_only"},
    {"base_term": "field_construction_depth_geometry_model_integration_planning_pass", "stage_term": "depth_observation_candidate_ingestion_skeleton_pass"},
)

DEPTH_INGESTION_SKELETON_STAGE_ADDITIONS: Tuple[str, ...] = (
    "prior_depth_geometry_model_integration_planning_go",
    "depth_observation_candidate_ingestion_skeleton_complete",
    "depth_observation_candidate_builder_complete",
    "object_depth_hint_extractor_complete",
    "depth_fallback_policy_complete",
    "all_mock_cases_passed",
    "field_geometry_readiness_ok",
    "common_validation_reuse_ok",
    "depth_observation_candidate_ingestion_skeleton_only",
    "file_size_governance_review_ok",
)

WHITELIST_FILES: Tuple[str, ...] = DEPTH_INGESTION_SKELETON_WHITELIST_FILES + (
    "capabilities/midplatform/field_first_common_validation_v1.py",
    "capabilities/midplatform/depth_observation_candidate_ingestion_types_v1.py",
    "capabilities/midplatform/depth_observation_candidate_builder_v1.py",
    "capabilities/midplatform/object_depth_hint_extractor_v1.py",
    "capabilities/midplatform/depth_fallback_policy_v1.py",
    "capabilities/midplatform/depth_ingestion_result_assembler_v1.py",
    "capabilities/midplatform/depth_observation_candidate_ingestion_static_validators_v1.py",
    "capabilities/midplatform/depth_observation_candidate_ingestion_core_v1.py",
    "capabilities/midplatform/depth_observation_candidate_ingestion_skeleton_v1.py",
    "capabilities/midplatform/depth_observation_candidate_ingestion_skeleton_items_v1.py",
    "capabilities/midplatform/depth_observation_candidate_ingestion_skeleton_lineage_v1.py",
    "tools/evaluation/midplatform/run_depth_observation_candidate_ingestion_skeleton_v1.py",
    "tools/evaluation/midplatform/verify_depth_observation_candidate_ingestion_skeleton_v1.py",
)

PHASE_PYTHON_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/depth_observation_candidate_ingestion_types_v1.py",
    "capabilities/midplatform/depth_observation_candidate_builder_v1.py",
    "capabilities/midplatform/object_depth_hint_extractor_v1.py",
    "capabilities/midplatform/depth_fallback_policy_v1.py",
    "capabilities/midplatform/depth_ingestion_result_assembler_v1.py",
    "capabilities/midplatform/depth_observation_candidate_ingestion_static_validators_v1.py",
    "capabilities/midplatform/depth_observation_candidate_ingestion_core_v1.py",
    "capabilities/midplatform/depth_observation_candidate_ingestion_skeleton_v1.py",
    "capabilities/midplatform/depth_observation_candidate_ingestion_skeleton_items_v1.py",
    "capabilities/midplatform/depth_observation_candidate_ingestion_skeleton_lineage_v1.py",
    "tools/evaluation/midplatform/run_depth_observation_candidate_ingestion_skeleton_v1.py",
    "tools/evaluation/midplatform/verify_depth_observation_candidate_ingestion_skeleton_v1.py",
)

DOCS: Tuple[str, ...] = (
    "docs/architecture/midplatform/LUNA_MIDPLATFORM_DEPTH_OBSERVATION_CANDIDATE_INGESTION_SKELETON_V1.md",
    "docs/architecture/evaluation/LUNA_EVALUATION_DEPTH_OBSERVATION_CANDIDATE_INGESTION_SKELETON_V1.md",
    "docs/architecture/evaluation/LUNA_EVALUATION_DEPTH_OBSERVATION_CANDIDATE_INGESTION_SKELETON_V1_GO_NO_GO_PACK_V0.md",
)

ARTIFACTS: Tuple[str, ...] = (
    "depth_observation_candidate_ingestion_skeleton_report_v1.json",
    "depth_model_output_mock_contract_v1.json",
    "depth_observation_candidate_contract_v1.json",
    "object_depth_hint_candidate_contract_v1.json",
    "depth_sampling_policy_v1.json",
    "depth_reliability_policy_v1.json",
    "yolo_depth_alignment_policy_v1.json",
    "depth_missing_fallback_execution_policy_v1.json",
    "depth_ingestion_mock_case_results_v1.json",
    "field_geometry_readiness_review_v1.json",
    "common_validation_reuse_report_v1.json",
    "non_execution_boundary_review_v1.json",
    "file_size_governance_review_v1.json",
    "prohibited_scope_v1.json",
    "summary.json",
    "verifier_report.json",
)

FINAL_DECISION_GO = (
    "MIDPLATFORM_DEPTH_OBSERVATION_CANDIDATE_INGESTION_SKELETON_READY_FOR_YOLO_DEPTH_REAL_FIELD_SCENE_DRYRUN_PLANNING"
)

GO_CONDITIONS_KEYS: Tuple[str, ...] = (
    "prior_depth_geometry_model_integration_planning_go",
    "depth_observation_candidate_ingestion_skeleton_complete",
    "depth_observation_candidate_builder_complete",
    "object_depth_hint_extractor_complete",
    "depth_fallback_policy_complete",
    "all_mock_cases_passed",
    "yolo_depth_alignment_ok",
    "depth_missing_fallback_ok",
    "estimated_depth_error_expected_ok",
    "field_geometry_readiness_ok",
    "common_validation_reuse_ok",
    "no_depth_model_download",
    "no_weight_download",
    "no_real_depth_inference",
    "no_runtime_execution",
    "next_phase_readiness_ok",
)
