# -*- coding: utf-8 -*-
"""Tracking / Optical Flow model smoke IO inspection — lineage v1."""

from __future__ import annotations

from typing import Dict, Tuple

from capabilities.midplatform.tracking_opticalflow_model_smoke_io_inspection_types_v1 import FINAL_DECISION_GO

WHITELIST_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/slam_spatial_mapping_task_collaboration_planning_v1.py",
    "tools/evaluation/midplatform/run_slam_spatial_mapping_task_collaboration_planning_v1.py",
    "tools/evaluation/midplatform/verify_slam_spatial_mapping_task_collaboration_planning_v1.py",
    "capabilities/midplatform/field_first_common_validation_v1.py",
    "capabilities/midplatform/tracking_opticalflow_model_smoke_io_inspection_types_v1.py",
    "capabilities/midplatform/tracking_opticalflow_model_availability_checker_v1.py",
    "capabilities/midplatform/tracking_opticalflow_model_smoke_runner_v1.py",
    "capabilities/midplatform/tracking_opticalflow_io_inspector_v1.py",
    "capabilities/midplatform/tracking_opticalflow_candidate_mapping_reviewer_v1.py",
    "capabilities/midplatform/tracking_opticalflow_model_smoke_io_inspection_static_validators_v1.py",
    "capabilities/midplatform/tracking_opticalflow_model_smoke_io_inspection_core_v1.py",
    "capabilities/midplatform/tracking_opticalflow_model_smoke_io_inspection_v1.py",
    "capabilities/midplatform/tracking_opticalflow_model_smoke_io_inspection_items_v1.py",
    "capabilities/midplatform/tracking_opticalflow_model_smoke_io_inspection_lineage_v1.py",
    "tools/evaluation/midplatform/run_tracking_opticalflow_model_smoke_io_inspection_v1.py",
    "tools/evaluation/midplatform/verify_tracking_opticalflow_model_smoke_io_inspection_v1.py",
)

STAGE_TERM_OVERRIDES: Tuple[Dict[str, str], ...] = (
    {"base_term": "slam_task_collaboration_planning", "stage_term": "tracking_opticalflow_model_smoke_io_inspection"},
    {"base_term": "slam_task_collaboration_planning_pass", "stage_term": "tracking_opticalflow_smoke_io_inspection_pass"},
)

STAGE_ADDITIONS: Tuple[str, ...] = (
    "prior_slam_task_collaboration_planning_go",
    "route_follows_model_smoke_io_first",
    "tracking_opticalflow_smoke_io_inspection_complete",
    "no_adapter_skeleton_yet",
    "file_size_governance_review_ok",
)

PHASE_PYTHON_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/tracking_opticalflow_model_smoke_io_inspection_types_v1.py",
    "capabilities/midplatform/tracking_opticalflow_model_availability_checker_v1.py",
    "capabilities/midplatform/tracking_opticalflow_model_smoke_runner_v1.py",
    "capabilities/midplatform/tracking_opticalflow_io_inspector_v1.py",
    "capabilities/midplatform/tracking_opticalflow_candidate_mapping_reviewer_v1.py",
    "capabilities/midplatform/tracking_opticalflow_model_smoke_io_inspection_static_validators_v1.py",
    "capabilities/midplatform/tracking_opticalflow_model_smoke_io_inspection_core_v1.py",
    "capabilities/midplatform/tracking_opticalflow_model_smoke_io_inspection_v1.py",
    "capabilities/midplatform/tracking_opticalflow_model_smoke_io_inspection_items_v1.py",
    "capabilities/midplatform/tracking_opticalflow_model_smoke_io_inspection_lineage_v1.py",
    "tools/evaluation/midplatform/run_tracking_opticalflow_model_smoke_io_inspection_v1.py",
    "tools/evaluation/midplatform/verify_tracking_opticalflow_model_smoke_io_inspection_v1.py",
)

DOCS: Tuple[str, ...] = (
    "docs/architecture/midplatform/LUNA_MIDPLATFORM_TRACKING_OPTICALFLOW_MODEL_SMOKE_IO_INSPECTION_V1.md",
    "docs/architecture/evaluation/LUNA_EVALUATION_TRACKING_OPTICALFLOW_MODEL_SMOKE_IO_INSPECTION_V1.md",
    "docs/architecture/evaluation/LUNA_EVALUATION_TRACKING_OPTICALFLOW_MODEL_SMOKE_IO_INSPECTION_V1_GO_NO_GO_PACK_V0.md",
)

ARTIFACTS: Tuple[str, ...] = (
    "tracking_opticalflow_model_smoke_io_inspection_report_v1.json",
    "model_smoke_run_candidate_registry_v1.json",
    "model_io_inspection_candidate_registry_v1.json",
    "model_candidate_mapping_feasibility_registry_v1.json",
    "tracking_opticalflow_available_model_review_v1.json",
    "tracking_opticalflow_input_format_review_v1.json",
    "tracking_opticalflow_output_format_review_v1.json",
    "tracking_opticalflow_failure_point_review_v1.json",
    "tracking_opticalflow_candidate_mapping_review_v1.json",
    "model_execution_authorization_review_v1.json",
    "new_protocol_reason_required_report_v1.json",
    "owner_constraint_compliance_review_v1.json",
    "smoke_io_case_results_v1.json",
    "prohibited_scope_v1.json",
    "non_execution_boundary_review_v1.json",
    "file_size_governance_review_v1.json",
    "common_validation_reuse_report_v1.json",
    "summary.json",
    "verifier_report.json",
)

GO_CONDITIONS_KEYS: Tuple[str, ...] = (
    "prior_slam_task_collaboration_planning_go",
    "route_follows_model_smoke_io_first",
    "tracking_opticalflow_smoke_io_inspection_complete",
    "execution_authorization_review_ok",
    "input_output_inspection_complete",
    "candidate_mapping_feasibility_review_complete",
    "no_unauthorized_download",
    "no_adapter_skeleton_yet",
    "no_field_simulation",
    "no_world_model_assembly",
    "no_task_reasoning",
    "no_new_protocol_without_reason",
    "traceability_preserved",
    "candidate_only_outputs",
    "common_validation_reuse_ok",
    "next_phase_readiness_ok",
)

__all__ = ["FINAL_DECISION_GO", "ARTIFACTS", "DOCS", "GO_CONDITIONS_KEYS", "PHASE_PYTHON_FILES", "WHITELIST_FILES"]
