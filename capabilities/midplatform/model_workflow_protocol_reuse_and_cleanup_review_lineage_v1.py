# -*- coding: utf-8 -*-
"""Model workflow protocol reuse and cleanup review — lineage v1."""

from __future__ import annotations

from typing import Dict, Tuple

from capabilities.midplatform.model_workflow_protocol_reuse_and_cleanup_review_types_v1 import (
    FINAL_DECISION_GO,
)

CLEANUP_WHITELIST_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/real_model_field_construction_execution_path_hardening_v1.py",
    "tools/evaluation/midplatform/run_real_model_field_construction_execution_path_hardening_v1.py",
    "tools/evaluation/midplatform/verify_real_model_field_construction_execution_path_hardening_v1.py",
)

CLEANUP_STAGE_TERM_OVERRIDES: Tuple[Dict[str, str], ...] = (
    {"base_term": "real_model_field_construction_execution_path_hardening", "stage_term": "model_workflow_protocol_reuse_and_cleanup_review"},
    {"base_term": "real_model_execution_path_hardening_pass", "stage_term": "cleanup_review_pass"},
)

CLEANUP_STAGE_ADDITIONS: Tuple[str, ...] = (
    "prior_broader_midplatform_closure_roadmap_go",
    "cleanup_review_complete",
    "field_simulation_deactivated_from_mainline",
    "protocol_reuse_review_complete",
    "protocol_overreach_review_complete",
    "active_mainline_registry_complete",
    "deprecated_registry_complete",
    "cleanup_required_registry_complete",
    "next_allowed_phase_recommendation_ok",
    "no_field_simulation_next_phase",
    "no_task_reasoning_next_phase",
    "file_size_governance_review_ok",
)

WHITELIST_FILES: Tuple[str, ...] = CLEANUP_WHITELIST_FILES + (
    "capabilities/midplatform/field_first_common_validation_v1.py",
    "capabilities/midplatform/model_workflow_protocol_reuse_and_cleanup_review_types_v1.py",
    "capabilities/midplatform/model_workflow_protocol_reuse_and_cleanup_scanner_v1.py",
    "capabilities/midplatform/model_workflow_protocol_reuse_and_cleanup_review_items_v1.py",
    "capabilities/midplatform/model_workflow_protocol_reuse_and_cleanup_review_lineage_v1.py",
    "capabilities/midplatform/model_workflow_protocol_reuse_and_cleanup_review_v1.py",
    "tools/evaluation/midplatform/run_model_workflow_protocol_reuse_and_cleanup_review_v1.py",
    "tools/evaluation/midplatform/verify_model_workflow_protocol_reuse_and_cleanup_review_v1.py",
)

PHASE_PYTHON_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/model_workflow_protocol_reuse_and_cleanup_review_types_v1.py",
    "capabilities/midplatform/model_workflow_protocol_reuse_and_cleanup_scanner_v1.py",
    "capabilities/midplatform/model_workflow_protocol_reuse_and_cleanup_review_items_v1.py",
    "capabilities/midplatform/model_workflow_protocol_reuse_and_cleanup_review_lineage_v1.py",
    "capabilities/midplatform/model_workflow_protocol_reuse_and_cleanup_review_v1.py",
    "tools/evaluation/midplatform/run_model_workflow_protocol_reuse_and_cleanup_review_v1.py",
    "tools/evaluation/midplatform/verify_model_workflow_protocol_reuse_and_cleanup_review_v1.py",
)

DOCS: Tuple[str, ...] = (
    "docs/architecture/midplatform/LUNA_MIDPLATFORM_MODEL_WORKFLOW_PROTOCOL_REUSE_AND_CLEANUP_REVIEW_V1.md",
    "docs/architecture/evaluation/LUNA_EVALUATION_MODEL_WORKFLOW_PROTOCOL_REUSE_AND_CLEANUP_REVIEW_V1.md",
    "docs/architecture/evaluation/LUNA_EVALUATION_MODEL_WORKFLOW_PROTOCOL_REUSE_AND_CLEANUP_REVIEW_V1_GO_NO_GO_PACK_V0.md",
)

ARTIFACTS: Tuple[str, ...] = (
    "model_workflow_protocol_reuse_and_cleanup_review_report_v1.json",
    "active_mainline_file_registry_v1.json",
    "deprecated_file_registry_v1.json",
    "cleanup_required_file_registry_v1.json",
    "protocol_reuse_review_v1.json",
    "protocol_overreach_review_v1.json",
    "field_simulation_deactivation_review_v1.json",
    "task_reasoning_defer_review_v1.json",
    "world_model_candidate_scope_review_v1.json",
    "model_task_collaboration_scope_review_v1.json",
    "next_allowed_phase_recommendation_v1.json",
    "non_execution_boundary_review_v1.json",
    "file_size_governance_review_v1.json",
    "prohibited_scope_v1.json",
    "summary.json",
    "verifier_report.json",
)

GO_CONDITIONS_KEYS: Tuple[str, ...] = (
    "prior_broader_midplatform_closure_roadmap_go",
    "cleanup_review_complete",
    "field_simulation_deactivated_from_mainline",
    "protocol_reuse_review_complete",
    "no_unjustified_new_protocol",
    "active_mainline_registry_complete",
    "deprecated_registry_complete",
    "cleanup_required_registry_complete",
    "next_allowed_phase_recommendation_ok",
    "no_field_simulation_next_phase",
    "no_task_reasoning_next_phase",
    "no_world_model_entry_write",
    "no_fact_admission",
    "no_task_action_output",
    "candidate_only_outputs",
    "common_validation_reuse_ok",
    "next_phase_readiness_ok",
)

__all__ = ["FINAL_DECISION_GO", "ARTIFACTS", "DOCS", "GO_CONDITIONS_KEYS", "PHASE_PYTHON_FILES", "WHITELIST_FILES"]
