# -*- coding: utf-8 -*-
"""Segmentation / Mask task collaboration planning — lineage v1."""

from __future__ import annotations

from typing import Dict, Tuple

from capabilities.midplatform.segmentation_mask_task_collaboration_planning_items_v1 import FINAL_DECISION_GO

PLANNING_WHITELIST_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/segmentation_mask_adapter_skeleton_v1.py",
    "tools/evaluation/midplatform/run_segmentation_mask_adapter_skeleton_v1.py",
    "tools/evaluation/midplatform/verify_segmentation_mask_adapter_skeleton_v1.py",
)

PLANNING_STAGE_TERM_OVERRIDES: Tuple[Dict[str, str], ...] = (
    {"base_term": "segmentation_mask_adapter_skeleton", "stage_term": "segmentation_mask_task_collaboration_planning"},
    {"base_term": "segmentation_mask_adapter_skeleton_pass", "stage_term": "segmentation_mask_task_collaboration_planning_pass"},
)

PLANNING_STAGE_ADDITIONS: Tuple[str, ...] = (
    "prior_segmentation_mask_adapter_skeleton_go",
    "smoke_io_then_adapter_then_task_collaboration_order_respected",
    "segmentation_mask_task_collaboration_planning_complete",
    "model_group_registry_complete",
    "task_input_mapping_complete",
    "task_output_evidence_mapping_complete",
    "invocation_control_review_ok",
    "failure_degradation_policy_complete",
    "no_action_boundary_ok",
    "no_world_model_assembly_boundary_ok",
    "no_world_geometry_candidate_generated",
    "file_size_governance_review_ok",
)

WHITELIST_FILES: Tuple[str, ...] = PLANNING_WHITELIST_FILES + (
    "capabilities/midplatform/field_first_common_validation_v1.py",
    "capabilities/midplatform/segmentation_mask_task_collaboration_planning_items_v1.py",
    "capabilities/midplatform/segmentation_mask_task_collaboration_planning_lineage_v1.py",
    "capabilities/midplatform/segmentation_mask_task_collaboration_planning_v1.py",
    "tools/evaluation/midplatform/run_segmentation_mask_task_collaboration_planning_v1.py",
    "tools/evaluation/midplatform/verify_segmentation_mask_task_collaboration_planning_v1.py",
)

PHASE_PYTHON_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/segmentation_mask_task_collaboration_planning_items_v1.py",
    "capabilities/midplatform/segmentation_mask_task_collaboration_planning_lineage_v1.py",
    "capabilities/midplatform/segmentation_mask_task_collaboration_planning_v1.py",
    "tools/evaluation/midplatform/run_segmentation_mask_task_collaboration_planning_v1.py",
    "tools/evaluation/midplatform/verify_segmentation_mask_task_collaboration_planning_v1.py",
)

DOCS: Tuple[str, ...] = (
    "docs/architecture/midplatform/LUNA_MIDPLATFORM_SEGMENTATION_MASK_TASK_COLLABORATION_PLANNING_V1.md",
    "docs/architecture/evaluation/LUNA_EVALUATION_SEGMENTATION_MASK_TASK_COLLABORATION_PLANNING_V1.md",
    "docs/architecture/evaluation/LUNA_EVALUATION_SEGMENTATION_MASK_TASK_COLLABORATION_PLANNING_V1_GO_NO_GO_PACK_V0.md",
)

ARTIFACTS: Tuple[str, ...] = (
    "segmentation_mask_task_collaboration_planning_report_v1.json",
    "segmentation_mask_task_collaboration_model_group_registry_v1.json",
    "segmentation_mask_task_input_mapping_review_v1.json",
    "segmentation_mask_task_output_evidence_mapping_review_v1.json",
    "segmentation_mask_task_invocation_control_review_v1.json",
    "segmentation_mask_task_failure_degradation_policy_v1.json",
    "segmentation_mask_task_collaboration_case_registry_v1.json",
    "segmentation_mask_task_collaboration_protocol_reuse_decision_v1.json",
    "new_protocol_reason_required_report_v1.json",
    "no_action_boundary_review_v1.json",
    "no_world_model_assembly_boundary_review_v1.json",
    "owner_constraint_compliance_review_v1.json",
    "prohibited_scope_v1.json",
    "file_size_governance_review_v1.json",
    "non_execution_boundary_review_v1.json",
    "common_validation_reuse_report_v1.json",
    "summary.json",
    "verifier_report.json",
)

GO_CONDITIONS_KEYS: Tuple[str, ...] = (
    "prior_segmentation_mask_adapter_skeleton_go",
    "smoke_io_then_adapter_then_task_collaboration_order_respected",
    "segmentation_mask_task_collaboration_planning_complete",
    "model_group_registry_complete",
    "task_input_mapping_complete",
    "task_output_evidence_mapping_complete",
    "invocation_control_review_ok",
    "failure_degradation_policy_complete",
    "all_planning_cases_passed",
    "no_action_boundary_ok",
    "no_world_model_assembly_boundary_ok",
    "no_task_reasoning_execution",
    "no_action_output",
    "no_field_simulation",
    "no_world_geometry_candidate_generated",
    "no_world_entity_candidate_generated",
    "no_world_model_candidate_generated",
    "no_world_model_entry_created",
    "no_fact_admission",
    "no_new_protocol_without_reason",
    "candidate_only_outputs",
    "common_validation_reuse_ok",
    "next_phase_readiness_ok",
)

__all__ = ["FINAL_DECISION_GO", "ARTIFACTS", "DOCS", "GO_CONDITIONS_KEYS", "PHASE_PYTHON_FILES", "WHITELIST_FILES"]
