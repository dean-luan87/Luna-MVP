# -*- coding: utf-8 -*-
"""Tracking / Optical Flow adapter skeleton — lineage v1."""

from __future__ import annotations

from typing import Dict, Tuple

from capabilities.midplatform.tracking_opticalflow_adapter_types_v1 import FINAL_DECISION_GO

SKELETON_WHITELIST_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/tracking_opticalflow_model_smoke_io_inspection_v1.py",
    "tools/evaluation/midplatform/run_tracking_opticalflow_model_smoke_io_inspection_v1.py",
    "tools/evaluation/midplatform/verify_tracking_opticalflow_model_smoke_io_inspection_v1.py",
)

SKELETON_STAGE_TERM_OVERRIDES: Tuple[Dict[str, str], ...] = (
    {"base_term": "tracking_opticalflow_model_smoke_io_inspection", "stage_term": "tracking_opticalflow_adapter_skeleton"},
    {"base_term": "tracking_opticalflow_smoke_io_inspection_pass", "stage_term": "tracking_opticalflow_adapter_skeleton_pass"},
)

SKELETON_STAGE_ADDITIONS: Tuple[str, ...] = (
    "prior_tracking_opticalflow_smoke_io_inspection_go",
    "smoke_io_inspection_artifacts_read",
    "adapter_based_on_real_inspection_results",
    "tracking_opticalflow_adapter_skeleton_complete",
    "raw_output_loader_complete",
    "readiness_for_task_collaboration_ok",
    "readiness_for_later_world_model_candidate_assembly_ok",
    "no_world_model_candidate_generated",
    "no_real_tracking_execution",
    "no_real_opticalflow_execution",
    "no_field_simulation",
    "no_task_reasoning",
    "no_action_output",
    "file_size_governance_review_ok",
)

WHITELIST_FILES: Tuple[str, ...] = SKELETON_WHITELIST_FILES + (
    "capabilities/midplatform/field_first_common_validation_v1.py",
    "capabilities/midplatform/tracking_opticalflow_adapter_types_v1.py",
    "capabilities/midplatform/tracking_opticalflow_adapter_input_builder_v1.py",
    "capabilities/midplatform/tracking_opticalflow_raw_output_loader_v1.py",
    "capabilities/midplatform/tracking_opticalflow_output_normalizer_v1.py",
    "capabilities/midplatform/object_persistence_candidate_builder_v1.py",
    "capabilities/midplatform/motion_candidate_builder_v1.py",
    "capabilities/midplatform/tracking_opticalflow_adapter_result_assembler_v1.py",
    "capabilities/midplatform/tracking_opticalflow_adapter_static_validators_v1.py",
    "capabilities/midplatform/tracking_opticalflow_adapter_core_v1.py",
    "capabilities/midplatform/tracking_opticalflow_adapter_skeleton_v1.py",
    "capabilities/midplatform/tracking_opticalflow_adapter_skeleton_items_v1.py",
    "capabilities/midplatform/tracking_opticalflow_adapter_skeleton_lineage_v1.py",
    "tools/evaluation/midplatform/run_tracking_opticalflow_adapter_skeleton_v1.py",
    "tools/evaluation/midplatform/verify_tracking_opticalflow_adapter_skeleton_v1.py",
)

PHASE_PYTHON_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/tracking_opticalflow_adapter_types_v1.py",
    "capabilities/midplatform/tracking_opticalflow_adapter_input_builder_v1.py",
    "capabilities/midplatform/tracking_opticalflow_raw_output_loader_v1.py",
    "capabilities/midplatform/tracking_opticalflow_output_normalizer_v1.py",
    "capabilities/midplatform/object_persistence_candidate_builder_v1.py",
    "capabilities/midplatform/motion_candidate_builder_v1.py",
    "capabilities/midplatform/tracking_opticalflow_adapter_result_assembler_v1.py",
    "capabilities/midplatform/tracking_opticalflow_adapter_static_validators_v1.py",
    "capabilities/midplatform/tracking_opticalflow_adapter_core_v1.py",
    "capabilities/midplatform/tracking_opticalflow_adapter_skeleton_v1.py",
    "capabilities/midplatform/tracking_opticalflow_adapter_skeleton_items_v1.py",
    "capabilities/midplatform/tracking_opticalflow_adapter_skeleton_lineage_v1.py",
    "tools/evaluation/midplatform/run_tracking_opticalflow_adapter_skeleton_v1.py",
    "tools/evaluation/midplatform/verify_tracking_opticalflow_adapter_skeleton_v1.py",
)

DOCS: Tuple[str, ...] = (
    "docs/architecture/midplatform/LUNA_MIDPLATFORM_TRACKING_OPTICALFLOW_ADAPTER_SKELETON_V1.md",
    "docs/architecture/evaluation/LUNA_EVALUATION_TRACKING_OPTICALFLOW_ADAPTER_SKELETON_V1.md",
    "docs/architecture/evaluation/LUNA_EVALUATION_TRACKING_OPTICALFLOW_ADAPTER_SKELETON_V1_GO_NO_GO_PACK_V0.md",
)

ARTIFACTS: Tuple[str, ...] = (
    "tracking_opticalflow_adapter_skeleton_report_v1.json",
    "tracking_opticalflow_adapter_input_registry_v1.json",
    "tracking_opticalflow_raw_output_candidate_registry_v1.json",
    "object_track_candidate_registry_v1.json",
    "object_persistence_candidate_registry_v1.json",
    "motion_candidate_registry_v1.json",
    "tracking_quality_candidate_registry_v1.json",
    "tracking_opticalflow_adapter_result_candidate_registry_v1.json",
    "tracking_opticalflow_task_collaboration_readiness_review_v1.json",
    "tracking_opticalflow_later_world_model_readiness_review_v1.json",
    "protocol_reuse_decision_v1.json",
    "new_protocol_reason_required_report_v1.json",
    "no_action_boundary_review_v1.json",
    "no_world_model_assembly_boundary_review_v1.json",
    "owner_constraint_compliance_review_v1.json",
    "skeleton_case_results_v1.json",
    "prohibited_scope_v1.json",
    "non_execution_boundary_review_v1.json",
    "file_size_governance_review_v1.json",
    "common_validation_reuse_report_v1.json",
    "summary.json",
    "verifier_report.json",
)

GO_CONDITIONS_KEYS: Tuple[str, ...] = (
    "prior_tracking_opticalflow_smoke_io_inspection_go",
    "smoke_io_inspection_artifacts_read",
    "adapter_based_on_real_inspection_results",
    "tracking_opticalflow_adapter_skeleton_complete",
    "adapter_input_builder_complete",
    "raw_output_loader_complete",
    "output_normalizer_complete",
    "object_persistence_builder_complete",
    "motion_candidate_builder_complete",
    "adapter_result_assembler_complete",
    "all_skeleton_cases_passed",
    "protocol_reuse_decision_ok",
    "readiness_for_task_collaboration_ok",
    "readiness_for_later_world_model_candidate_assembly_ok",
    "existing_io_reuse_ok",
    "no_new_protocol_without_reason",
    "cached_output_not_marked_as_real_run",
    "adapter_stub_not_marked_as_real_run",
    "blocked_cases_do_not_fabricate_outputs",
    "short_track_not_persistent",
    "identity_switch_degrades_persistence",
    "lost_track_degraded",
    "no_real_tracking_execution",
    "no_real_opticalflow_execution",
    "no_model_download",
    "no_field_simulation",
    "no_task_reasoning",
    "no_action_output",
    "no_world_entity_candidate_generated",
    "no_world_model_candidate_generated",
    "no_world_model_entry_created",
    "no_fact_admission",
    "owner_constraints_inherited",
    "candidate_only_outputs",
    "common_validation_reuse_ok",
    "next_phase_readiness_ok",
)

__all__ = ["FINAL_DECISION_GO", "ARTIFACTS", "DOCS", "GO_CONDITIONS_KEYS", "PHASE_PYTHON_FILES", "WHITELIST_FILES"]
