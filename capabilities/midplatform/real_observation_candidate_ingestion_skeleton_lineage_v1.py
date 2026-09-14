# -*- coding: utf-8 -*-
"""Real Observation Candidate Ingestion Skeleton — lineage v1."""

from __future__ import annotations

from typing import Dict, Tuple

INGESTION_SKELETON_WHITELIST_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/field_first_minimal_real_model_adapter_integration_planning_v1.py",
    "tools/evaluation/midplatform/run_field_first_minimal_real_model_adapter_integration_planning_v1.py",
    "tools/evaluation/midplatform/verify_field_first_minimal_real_model_adapter_integration_planning_v1.py",
)

INGESTION_SKELETON_STAGE_TERM_OVERRIDES: Tuple[Dict[str, str], ...] = (
    {"base_term": "field_first_minimal_real_model_adapter_integration_planning", "stage_term": "real_observation_candidate_ingestion_skeleton"},
    {"base_term": "minimal_real_model_adapter_integration_planning_only", "stage_term": "real_observation_candidate_ingestion_skeleton_only"},
    {"base_term": "minimal_real_model_adapter_integration_planning_pass", "stage_term": "real_observation_candidate_ingestion_skeleton_pass"},
)

INGESTION_SKELETON_STAGE_ADDITIONS: Tuple[str, ...] = (
    "prior_minimal_real_model_adapter_planning_go",
    "real_observation_candidate_ingestion_skeleton_complete",
    "object_observation_candidate_builder_complete",
    "detection_normalizer_complete",
    "ingestion_result_assembler_complete",
    "all_mock_cases_passed",
    "field_first_core_readiness_ok",
    "common_validation_reuse_ok",
    "real_observation_candidate_ingestion_skeleton_only",
    "file_size_governance_review_ok",
)

WHITELIST_FILES: Tuple[str, ...] = INGESTION_SKELETON_WHITELIST_FILES + (
    "capabilities/midplatform/field_first_common_validation_v1.py",
    "capabilities/midplatform/real_observation_candidate_ingestion_types_v1.py",
    "capabilities/midplatform/real_observation_detection_normalizer_v1.py",
    "capabilities/midplatform/object_observation_candidate_builder_v1.py",
    "capabilities/midplatform/real_observation_ingestion_result_assembler_v1.py",
    "capabilities/midplatform/real_observation_candidate_ingestion_static_validators_v1.py",
    "capabilities/midplatform/real_observation_candidate_ingestion_core_v1.py",
    "capabilities/midplatform/real_observation_candidate_ingestion_skeleton_v1.py",
    "capabilities/midplatform/real_observation_candidate_ingestion_skeleton_items_v1.py",
    "capabilities/midplatform/real_observation_candidate_ingestion_skeleton_lineage_v1.py",
    "tools/evaluation/midplatform/run_real_observation_candidate_ingestion_skeleton_v1.py",
    "tools/evaluation/midplatform/verify_real_observation_candidate_ingestion_skeleton_v1.py",
)

PHASE_PYTHON_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/real_observation_candidate_ingestion_types_v1.py",
    "capabilities/midplatform/real_observation_detection_normalizer_v1.py",
    "capabilities/midplatform/object_observation_candidate_builder_v1.py",
    "capabilities/midplatform/real_observation_ingestion_result_assembler_v1.py",
    "capabilities/midplatform/real_observation_candidate_ingestion_static_validators_v1.py",
    "capabilities/midplatform/real_observation_candidate_ingestion_core_v1.py",
    "capabilities/midplatform/real_observation_candidate_ingestion_skeleton_v1.py",
    "capabilities/midplatform/real_observation_candidate_ingestion_skeleton_items_v1.py",
    "capabilities/midplatform/real_observation_candidate_ingestion_skeleton_lineage_v1.py",
    "tools/evaluation/midplatform/run_real_observation_candidate_ingestion_skeleton_v1.py",
    "tools/evaluation/midplatform/verify_real_observation_candidate_ingestion_skeleton_v1.py",
)

DOCS: Tuple[str, ...] = (
    "docs/architecture/midplatform/LUNA_MIDPLATFORM_REAL_OBSERVATION_CANDIDATE_INGESTION_SKELETON_V1.md",
    "docs/architecture/evaluation/LUNA_EVALUATION_REAL_OBSERVATION_CANDIDATE_INGESTION_SKELETON_V1.md",
    "docs/architecture/evaluation/LUNA_EVALUATION_REAL_OBSERVATION_CANDIDATE_INGESTION_SKELETON_V1_GO_NO_GO_PACK_V0.md",
)

ARTIFACTS: Tuple[str, ...] = (
    "real_observation_candidate_ingestion_skeleton_report_v1.json",
    "detector_output_mock_contract_v1.json",
    "supervision_normalized_detection_contract_v1.json",
    "object_observation_candidate_contract_v1.json",
    "detector_to_observation_ingestion_mapping_v1.json",
    "depth_missing_fallback_execution_policy_v1.json",
    "real_observation_ingestion_mock_case_results_v1.json",
    "rejected_detection_policy_v1.json",
    "field_first_core_readiness_review_v1.json",
    "common_validation_reuse_report_v1.json",
    "non_execution_boundary_review_v1.json",
    "file_size_governance_review_v1.json",
    "prohibited_scope_v1.json",
    "summary.json",
    "verifier_report.json",
)

FINAL_DECISION_GO = (
    "MIDPLATFORM_REAL_OBSERVATION_CANDIDATE_INGESTION_SKELETON_READY_FOR_REAL_MODEL_SUCCESS_PATH_DRYRUN_PLANNING"
)

GO_CONDITIONS_KEYS: Tuple[str, ...] = (
    "prior_minimal_real_model_adapter_planning_go",
    "real_observation_candidate_ingestion_skeleton_complete",
    "object_observation_candidate_builder_complete",
    "detection_normalizer_complete",
    "ingestion_result_assembler_complete",
    "all_mock_cases_passed",
    "depth_missing_fallback_ok",
    "tracker_hint_not_fact_ok",
    "field_first_core_readiness_ok",
    "common_validation_reuse_ok",
    "no_model_download",
    "no_weight_download",
    "no_real_inference_execution",
    "no_runtime_execution",
    "next_phase_readiness_ok",
)
