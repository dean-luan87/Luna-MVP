# -*- coding: utf-8 -*-
"""Model adapter priority sequence planning — lineage v1."""

from __future__ import annotations

from typing import Dict, Tuple

from capabilities.midplatform.model_adapter_priority_sequence_planning_types_v1 import FINAL_DECISION_GO

PLANNING_WHITELIST_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/model_workflow_protocol_reuse_and_cleanup_review_v1.py",
    "tools/evaluation/midplatform/run_model_workflow_protocol_reuse_and_cleanup_review_v1.py",
    "tools/evaluation/midplatform/verify_model_workflow_protocol_reuse_and_cleanup_review_v1.py",
)

PLANNING_STAGE_TERM_OVERRIDES: Tuple[Dict[str, str], ...] = (
    {"base_term": "model_workflow_protocol_reuse_and_cleanup_review", "stage_term": "model_adapter_priority_sequence_planning"},
    {"base_term": "cleanup_review_pass", "stage_term": "model_adapter_priority_sequence_planning_pass"},
)

PLANNING_STAGE_ADDITIONS: Tuple[str, ...] = (
    "prior_model_workflow_protocol_reuse_and_cleanup_review_go",
    "model_adapter_priority_sequence_planning_complete",
    "priority_registry_complete",
    "reuse_path_registry_complete",
    "world_model_mapping_complete",
    "task_collaboration_mapping_complete",
    "no_new_protocol_without_reason",
    "no_field_simulation_route",
    "no_task_reasoning_route",
    "file_size_governance_review_ok",
)

WHITELIST_FILES: Tuple[str, ...] = PLANNING_WHITELIST_FILES + (
    "capabilities/midplatform/field_first_common_validation_v1.py",
    "capabilities/midplatform/model_adapter_priority_sequence_planning_types_v1.py",
    "capabilities/midplatform/model_adapter_priority_sequence_planning_items_v1.py",
    "capabilities/midplatform/model_adapter_priority_sequence_planning_lineage_v1.py",
    "capabilities/midplatform/model_adapter_priority_sequence_planning_v1.py",
    "tools/evaluation/midplatform/run_model_adapter_priority_sequence_planning_v1.py",
    "tools/evaluation/midplatform/verify_model_adapter_priority_sequence_planning_v1.py",
)

PHASE_PYTHON_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/model_adapter_priority_sequence_planning_types_v1.py",
    "capabilities/midplatform/model_adapter_priority_sequence_planning_items_v1.py",
    "capabilities/midplatform/model_adapter_priority_sequence_planning_lineage_v1.py",
    "capabilities/midplatform/model_adapter_priority_sequence_planning_v1.py",
    "tools/evaluation/midplatform/run_model_adapter_priority_sequence_planning_v1.py",
    "tools/evaluation/midplatform/verify_model_adapter_priority_sequence_planning_v1.py",
)

DOCS: Tuple[str, ...] = (
    "docs/architecture/midplatform/LUNA_MIDPLATFORM_MODEL_ADAPTER_PRIORITY_SEQUENCE_PLANNING_V1.md",
    "docs/architecture/evaluation/LUNA_EVALUATION_MODEL_ADAPTER_PRIORITY_SEQUENCE_PLANNING_V1.md",
    "docs/architecture/evaluation/LUNA_EVALUATION_MODEL_ADAPTER_PRIORITY_SEQUENCE_PLANNING_V1_GO_NO_GO_PACK_V0.md",
)

ARTIFACTS: Tuple[str, ...] = (
    "model_adapter_priority_sequence_planning_report_v1.json",
    "model_adapter_priority_registry_v1.json",
    "model_adapter_reuse_path_registry_v1.json",
    "world_model_construction_model_mapping_v1.json",
    "task_collaboration_model_mapping_v1.json",
    "scenario_2_to_3_model_group_registry_v1.json",
    "model_adapter_protocol_reuse_decision_v1.json",
    "model_adapter_new_protocol_reason_required_report_v1.json",
    "next_model_adapter_skeleton_recommendation_v1.json",
    "deferred_model_adapter_registry_v1.json",
    "owner_constraint_compliance_review_v1.json",
    "planning_case_results_v1.json",
    "non_execution_boundary_review_v1.json",
    "file_size_governance_review_v1.json",
    "prohibited_scope_v1.json",
    "summary.json",
    "verifier_report.json",
)

GO_CONDITIONS_KEYS: Tuple[str, ...] = (
    "prior_model_workflow_protocol_reuse_and_cleanup_review_go",
    "model_adapter_priority_sequence_planning_complete",
    "priority_registry_complete",
    "reuse_path_registry_complete",
    "world_model_mapping_complete",
    "task_collaboration_mapping_complete",
    "scenario_model_group_registry_complete",
    "no_new_protocol_without_reason",
    "no_field_simulation_route",
    "no_task_reasoning_route",
    "owner_constraints_inherited",
    "slam_or_spatial_mapping_prioritized",
    "tracking_second_priority",
    "ocr_third_priority",
    "segmentation_fourth_priority",
    "scene_graph_deferred",
    "candidate_only_outputs",
    "common_validation_reuse_ok",
    "next_phase_readiness_ok",
)

__all__ = ["FINAL_DECISION_GO", "ARTIFACTS", "DOCS", "GO_CONDITIONS_KEYS", "PHASE_PYTHON_FILES", "WHITELIST_FILES"]
