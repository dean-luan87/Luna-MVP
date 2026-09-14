# -*- coding: utf-8 -*-
"""Scene Graph / Relation Model smoke IO decision review — lineage v1."""

from __future__ import annotations

from typing import Dict, Tuple

from capabilities.midplatform.scene_graph_relation_model_smoke_io_decision_review_items_v1 import (
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_DEFERRED,
    FINAL_DECISION_READY,
    VALID_FINAL_DECISIONS,
)

FINAL_DECISION_GO = FINAL_DECISION_READY

PLANNING_WHITELIST_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/segmentation_mask_task_collaboration_planning_v1.py",
    "tools/evaluation/midplatform/run_segmentation_mask_task_collaboration_planning_v1.py",
    "tools/evaluation/midplatform/verify_segmentation_mask_task_collaboration_planning_v1.py",
)

PLANNING_STAGE_TERM_OVERRIDES: Tuple[Dict[str, str], ...] = (
    {
        "base_term": "segmentation_mask_task_collaboration_planning",
        "stage_term": "scene_graph_relation_model_smoke_io_decision_review",
    },
    {
        "base_term": "segmentation_mask_task_collaboration_planning_pass",
        "stage_term": "scene_graph_relation_model_smoke_io_decision_review_pass",
    },
)

PLANNING_STAGE_ADDITIONS: Tuple[str, ...] = (
    "prior_segmentation_mask_task_collaboration_planning_go",
    "scene_graph_relation_is_p4_deferred_review",
    "decision_review_only",
    "p0_p3_prerequisite_chain_review_complete",
    "input_source_review_complete",
    "dependency_review_complete",
    "deferred_status_review_complete",
    "smoke_io_eligibility_review_complete",
    "next_phase_decision_complete",
    "smoke_io_allowed",
    "scene_graph_still_deferred",
    "no_scene_graph_runtime",
    "no_smoke_io_yet",
    "no_relation_candidate_generated",
    "no_world_model_assembly",
    "file_size_governance_review_ok",
)

WHITELIST_FILES: Tuple[str, ...] = PLANNING_WHITELIST_FILES + (
    "capabilities/midplatform/field_first_common_validation_v1.py",
    "capabilities/midplatform/scene_graph_relation_model_smoke_io_decision_review_items_v1.py",
    "capabilities/midplatform/scene_graph_relation_model_smoke_io_decision_review_evaluator_v1.py",
    "capabilities/midplatform/scene_graph_relation_model_smoke_io_decision_review_lineage_v1.py",
    "capabilities/midplatform/scene_graph_relation_model_smoke_io_decision_review_v1.py",
    "tools/evaluation/midplatform/run_scene_graph_relation_model_smoke_io_decision_review_v1.py",
    "tools/evaluation/midplatform/verify_scene_graph_relation_model_smoke_io_decision_review_v1.py",
)

PHASE_PYTHON_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/scene_graph_relation_model_smoke_io_decision_review_items_v1.py",
    "capabilities/midplatform/scene_graph_relation_model_smoke_io_decision_review_evaluator_v1.py",
    "capabilities/midplatform/scene_graph_relation_model_smoke_io_decision_review_lineage_v1.py",
    "capabilities/midplatform/scene_graph_relation_model_smoke_io_decision_review_v1.py",
    "tools/evaluation/midplatform/run_scene_graph_relation_model_smoke_io_decision_review_v1.py",
    "tools/evaluation/midplatform/verify_scene_graph_relation_model_smoke_io_decision_review_v1.py",
)

DOCS: Tuple[str, ...] = (
    "docs/architecture/midplatform/LUNA_MIDPLATFORM_SCENE_GRAPH_RELATION_MODEL_SMOKE_IO_DECISION_REVIEW_V1.md",
    "docs/architecture/evaluation/LUNA_EVALUATION_SCENE_GRAPH_RELATION_MODEL_SMOKE_IO_DECISION_REVIEW_V1.md",
    "docs/architecture/evaluation/LUNA_EVALUATION_SCENE_GRAPH_RELATION_MODEL_SMOKE_IO_DECISION_REVIEW_V1_GO_NO_GO_PACK_V0.md",
)

ARTIFACTS: Tuple[str, ...] = (
    "scene_graph_relation_model_smoke_io_decision_review_report_v1.json",
    "scene_graph_relation_input_source_review_v1.json",
    "scene_graph_relation_candidate_dependency_review_v1.json",
    "scene_graph_relation_deferred_status_review_v1.json",
    "scene_graph_relation_smoke_io_eligibility_review_v1.json",
    "scene_graph_relation_next_phase_decision_v1.json",
    "scene_graph_relation_protocol_reuse_decision_v1.json",
    "new_protocol_reason_required_report_v1.json",
    "no_relation_candidate_generation_review_v1.json",
    "no_world_model_assembly_boundary_review_v1.json",
    "owner_constraint_compliance_review_v1.json",
    "non_execution_boundary_review_v1.json",
    "prohibited_scope_v1.json",
    "decision_case_registry_v1.json",
    "scene_graph_relation_candidate_registry_review_v1.json",
    "scene_graph_relation_prerequisite_chain_review_v1.json",
    "file_size_governance_review_v1.json",
    "common_validation_reuse_report_v1.json",
    "summary.json",
    "verifier_report.json",
)

GO_CONDITIONS_KEYS: Tuple[str, ...] = (
    "prior_segmentation_mask_task_collaboration_planning_go",
    "scene_graph_relation_is_p4_deferred_review",
    "decision_review_only",
    "p0_p3_prerequisite_chain_review_complete",
    "input_source_review_complete",
    "dependency_review_complete",
    "deferred_status_review_complete",
    "smoke_io_eligibility_review_complete",
    "next_phase_decision_complete",
    "smoke_io_gate_decision_made",
    "all_decision_cases_passed",
    "no_scene_graph_runtime",
    "no_scene_graph_model_execution",
    "no_smoke_io_yet",
    "no_adapter_skeleton_yet",
    "no_task_collaboration_planning_yet",
    "no_relation_candidate_generated",
    "no_world_relation_candidate_generated",
    "no_world_model_assembly",
    "no_world_model_candidate_generated",
    "no_world_model_entry_created",
    "no_fact_admission",
    "no_task_reasoning_execution",
    "no_action_output",
    "no_field_simulation",
    "no_new_protocol_without_reason",
    "candidate_only_outputs",
    "common_validation_reuse_ok",
    "next_phase_readiness_ok",
)

__all__ = [
    "FINAL_DECISION_GO",
    "FINAL_DECISION_READY",
    "FINAL_DECISION_DEFERRED",
    "FINAL_DECISION_BLOCKED",
    "VALID_FINAL_DECISIONS",
    "ARTIFACTS",
    "DOCS",
    "GO_CONDITIONS_KEYS",
    "PHASE_PYTHON_FILES",
    "WHITELIST_FILES",
]
