# -*- coding: utf-8 -*-
"""Module handoff gap closure — lineage v1."""

from __future__ import annotations

from typing import Tuple

from capabilities.midplatform.task_manager_owner_approval_request_module_handoff_gap_closure_items_v1 import (
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_COMPLETE,
)

FINAL_DECISION_GO = FINAL_DECISION_COMPLETE

WHITELIST_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/field_first_common_validation_v1.py",
    "capabilities/midplatform/task_manager_owner_approval_request_module_handoff_gap_closure_items_v1.py",
    "capabilities/midplatform/task_manager_owner_approval_request_module_handoff_gap_closure_lineage_v1.py",
    "capabilities/midplatform/task_manager_owner_approval_request_module_handoff_gap_closure_v1.py",
    "tools/evaluation/midplatform/run_task_manager_owner_approval_request_module_handoff_gap_closure_v1.py",
    "tools/evaluation/midplatform/verify_task_manager_owner_approval_request_module_handoff_gap_closure_v1.py",
)

PHASE_PYTHON_FILES: Tuple[str, ...] = WHITELIST_FILES

DOCS: Tuple[str, ...] = (
    "docs/architecture/midplatform/LUNA_MIDPLATFORM_TASK_MANAGER_OWNER_APPROVAL_REQUEST_MODULE_HANDOFF_GAP_CLOSURE_V1.md",
    "docs/architecture/evaluation/LUNA_EVALUATION_TASK_MANAGER_OWNER_APPROVAL_REQUEST_MODULE_HANDOFF_GAP_CLOSURE_V1.md",
    "docs/architecture/evaluation/LUNA_EVALUATION_TASK_MANAGER_OWNER_APPROVAL_REQUEST_MODULE_HANDOFF_GAP_CLOSURE_V1_GO_NO_GO_PACK_V0.md",
)

ARTIFACTS: Tuple[str, ...] = (
    "task_manager_owner_approval_request_module_handoff_gap_closure_report_v1.json",
    "module_handoff_gap_review_v1.json",
    "downstream_roadmap_expected_artifact_review_v1.json",
    "owner_approval_request_handoff_artifact_visibility_review_v1.json",
    "handoff_output_field_alignment_review_v1.json",
    "task_manager_owner_approval_request_module_handoff_rerun_review_v1.json",
    "task_manager_broader_midplatform_closure_roadmap_readiness_review_v1.json",
    "no_protocol_change_review_v1.json",
    "owner_constraint_compliance_review_v1.json",
    "file_size_governance_review_v1.json",
    "common_validation_reuse_report_v1.json",
    "summary.json",
    "verifier_report.json",
)

GO_CONDITIONS_KEYS: Tuple[str, ...] = (
    "first_non_go_stage_confirmed",
    "direct_upstream_module_handoff_confirmed",
    "owner_approval_request_module_handoff_files_exist",
    "owner_approval_request_module_handoff_rerun_attempted",
    "owner_approval_request_module_handoff_result_recorded",
    "downstream_broader_roadmap_expectation_review_exists",
    "handoff_artifact_visibility_review_exists",
    "field_alignment_review_exists",
    "no_protocol_change",
    "no_model_route_touched",
    "no_world_model_assembly",
    "no_scene_graph_smoke_io",
    "no_task_reasoning",
    "no_field_simulation",
    "no_fake_go_artifacts",
    "common_validation_reuse_ok",
    "next_phase_readiness_ok",
)

VALID_FINAL_DECISIONS: Tuple[str, ...] = (
    FINAL_DECISION_COMPLETE,
    FINAL_DECISION_BLOCKED,
)
