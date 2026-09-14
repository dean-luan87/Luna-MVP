# -*- coding: utf-8 -*-
"""Module governance closure gap review — lineage v1."""

from __future__ import annotations

from typing import Tuple

from capabilities.midplatform.task_manager_owner_approval_request_module_governance_closure_gap_review_items_v1 import (
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_COMPLETE,
)

FINAL_DECISION_GO = FINAL_DECISION_COMPLETE

WHITELIST_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/field_first_common_validation_v1.py",
    "capabilities/midplatform/task_manager_owner_approval_request_module_governance_closure_gap_review_items_v1.py",
    "capabilities/midplatform/task_manager_owner_approval_request_module_governance_closure_gap_review_lineage_v1.py",
    "capabilities/midplatform/task_manager_owner_approval_request_module_governance_closure_gap_review_v1.py",
    "tools/evaluation/midplatform/run_task_manager_owner_approval_request_module_governance_closure_gap_review_v1.py",
    "tools/evaluation/midplatform/verify_task_manager_owner_approval_request_module_governance_closure_gap_review_v1.py",
)

PHASE_PYTHON_FILES: Tuple[str, ...] = WHITELIST_FILES

DOCS: Tuple[str, ...] = (
    "docs/architecture/midplatform/LUNA_MIDPLATFORM_TASK_MANAGER_OWNER_APPROVAL_REQUEST_MODULE_GOVERNANCE_CLOSURE_GAP_REVIEW_V1.md",
    "docs/architecture/evaluation/LUNA_EVALUATION_TASK_MANAGER_OWNER_APPROVAL_REQUEST_MODULE_GOVERNANCE_CLOSURE_GAP_REVIEW_V1.md",
    "docs/architecture/evaluation/LUNA_EVALUATION_TASK_MANAGER_OWNER_APPROVAL_REQUEST_MODULE_GOVERNANCE_CLOSURE_GAP_REVIEW_V1_GO_NO_GO_PACK_V0.md",
)

ARTIFACTS: Tuple[str, ...] = (
    "task_manager_owner_approval_request_module_governance_closure_gap_review_report_v1.json",
    "module_governance_closure_gap_review_v1.json",
    "functional_slice_dryrun_gap_review_v1.json",
    "functional_slice_dryrun_artifact_visibility_review_v1.json",
    "functional_slice_dryrun_boundary_gap_review_v1.json",
    "functional_slice_dryrun_real_execution_preconditions_review_v1.json",
    "module_governance_closure_rerun_review_v1.json",
    "handoff_rerun_readiness_review_v1.json",
    "first_unresolved_gap_review_v1.json",
    "no_protocol_change_review_v1.json",
    "owner_constraint_compliance_review_v1.json",
    "file_size_governance_review_v1.json",
    "common_validation_reuse_report_v1.json",
    "summary.json",
    "verifier_report.json",
)

GO_CONDITIONS_KEYS: Tuple[str, ...] = (
    "handoff_gap_closure_result_b_confirmed",
    "next_required_fix_confirmed",
    "module_governance_closure_files_exist",
    "module_governance_closure_rerun_attempted",
    "module_governance_closure_result_recorded",
    "functional_slice_dryrun_gap_review_exists",
    "functional_slice_dryrun_visibility_review_exists",
    "functional_slice_dryrun_boundary_gap_review_exists",
    "real_execution_preconditions_review_exists",
    "first_unresolved_gap_review_exists",
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
