# -*- coding: utf-8 -*-
"""Field-First Minimal Real Model Adapter Integration Planning — lineage v1."""

from __future__ import annotations

from typing import Dict, Tuple

ADAPTER_PLANNING_WHITELIST_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/field_first_core_logic_formal_implementation_v1.py",
    "tools/evaluation/midplatform/run_field_first_core_logic_formal_implementation_v1.py",
    "tools/evaluation/midplatform/verify_field_first_core_logic_formal_implementation_v1.py",
)

ADAPTER_PLANNING_STAGE_TERM_OVERRIDES: Tuple[Dict[str, str], ...] = (
    {"base_term": "field_first_core_logic_formal_implementation", "stage_term": "field_first_minimal_real_model_adapter_integration_planning"},
    {"base_term": "field_first_core_logic_formal_implementation_only", "stage_term": "minimal_real_model_adapter_integration_planning_only"},
    {"base_term": "field_first_core_logic_formal_implementation_pass", "stage_term": "minimal_real_model_adapter_integration_planning_pass"},
)

ADAPTER_PLANNING_STAGE_ADDITIONS: Tuple[str, ...] = (
    "prior_field_first_core_logic_go",
    "minimal_real_model_adapter_integration_planning_complete",
    "detector_adapter_plan_complete",
    "supervision_normalization_plan_complete",
    "observation_candidate_mapping_complete",
    "depth_missing_fallback_policy_complete",
    "real_model_success_path_readiness_plan_complete",
    "common_validation_reuse_ok",
    "minimal_real_model_adapter_integration_planning_only",
    "file_size_governance_review_ok",
)

WHITELIST_FILES: Tuple[str, ...] = ADAPTER_PLANNING_WHITELIST_FILES + (
    "capabilities/midplatform/field_first_common_validation_v1.py",
    "capabilities/midplatform/field_first_minimal_real_model_adapter_integration_planning_v1.py",
    "capabilities/midplatform/field_first_minimal_real_model_adapter_integration_items_v1.py",
    "capabilities/midplatform/field_first_minimal_real_model_adapter_integration_lineage_v1.py",
    "tools/evaluation/midplatform/run_field_first_minimal_real_model_adapter_integration_planning_v1.py",
    "tools/evaluation/midplatform/verify_field_first_minimal_real_model_adapter_integration_planning_v1.py",
)

PHASE_PYTHON_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/field_first_minimal_real_model_adapter_integration_planning_v1.py",
    "capabilities/midplatform/field_first_minimal_real_model_adapter_integration_items_v1.py",
    "capabilities/midplatform/field_first_minimal_real_model_adapter_integration_lineage_v1.py",
    "tools/evaluation/midplatform/run_field_first_minimal_real_model_adapter_integration_planning_v1.py",
    "tools/evaluation/midplatform/verify_field_first_minimal_real_model_adapter_integration_planning_v1.py",
)

DOCS: Tuple[str, ...] = (
    "docs/architecture/midplatform/LUNA_MIDPLATFORM_FIELD_FIRST_MINIMAL_REAL_MODEL_ADAPTER_INTEGRATION_PLANNING_V1.md",
    "docs/architecture/evaluation/LUNA_EVALUATION_FIELD_FIRST_MINIMAL_REAL_MODEL_ADAPTER_INTEGRATION_PLANNING_V1.md",
    "docs/architecture/evaluation/LUNA_EVALUATION_FIELD_FIRST_MINIMAL_REAL_MODEL_ADAPTER_INTEGRATION_PLANNING_V1_GO_NO_GO_PACK_V0.md",
)

ARTIFACTS: Tuple[str, ...] = (
    "minimal_real_model_adapter_integration_planning_report_v1.json",
    "minimal_detector_adapter_plan_v1.json",
    "supervision_normalization_plan_v1.json",
    "real_observation_candidate_ingestion_plan_v1.json",
    "detector_output_to_observation_candidate_mapping_v1.json",
    "depth_missing_fallback_policy_v1.json",
    "real_model_success_path_readiness_plan_v1.json",
    "model_download_authorization_status_v1.json",
    "prohibited_scope_v1.json",
    "common_validation_reuse_report_v1.json",
    "file_size_governance_review_v1.json",
    "summary.json",
    "verifier_report.json",
)

FINAL_DECISION_GO = (
    "MIDPLATFORM_FIELD_FIRST_MINIMAL_REAL_MODEL_ADAPTER_INTEGRATION_PLANNING_READY_FOR_REAL_OBSERVATION_CANDIDATE_INGESTION_SKELETON"
)

GO_CONDITIONS_KEYS: Tuple[str, ...] = (
    "prior_field_first_core_logic_go",
    "minimal_real_model_adapter_integration_planning_complete",
    "detector_adapter_plan_complete",
    "supervision_normalization_plan_complete",
    "observation_candidate_mapping_complete",
    "depth_missing_fallback_policy_complete",
    "real_model_success_path_readiness_plan_complete",
    "no_weight_download",
    "no_large_dependency_install",
    "no_production_model_selection",
    "no_field_simulation",
    "no_task_execution",
    "no_runtime_execution",
    "no_world_model_fact_creation",
    "candidate_only_outputs",
    "common_validation_reuse_ok",
    "next_phase_readiness_ok",
    "first_batch_scope_limited_to_detector_and_normalization",
    "model_output_maps_to_observation_candidate",
    "depth_unknown_policy_defined",
)
