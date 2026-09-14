# -*- coding: utf-8 -*-
"""Grant owner approval request planning repair — lineage v1."""

from __future__ import annotations

from typing import Tuple

from capabilities.midplatform.grant_owner_approval_request_planning_repair_items_v1 import (
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_COMPLETE,
)

WHITELIST_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/field_first_common_validation_v1.py",
    "capabilities/midplatform/grant_owner_approval_request_planning_repair_items_v1.py",
    "capabilities/midplatform/grant_owner_approval_request_planning_repair_lineage_v1.py",
    "capabilities/midplatform/grant_owner_approval_request_planning_repair_v1.py",
    "tools/evaluation/midplatform/run_grant_owner_approval_request_planning_repair_v1.py",
    "tools/evaluation/midplatform/verify_grant_owner_approval_request_planning_repair_v1.py",
)

PHASE_PYTHON_FILES: Tuple[str, ...] = WHITELIST_FILES

DOCS: Tuple[str, ...] = ()

ARTIFACTS: Tuple[str, ...] = (
    "grant_owner_approval_request_planning_repair_report_v1.json",
    "canonical_rebuild_input_review_v1.json",
    "grant_owner_approval_request_planning_original_stage_locator_v1.json",
    "grant_owner_approval_request_planning_original_rerun_review_v1.json",
    "grant_owner_approval_request_planning_failure_classification_v1.json",
    "grant_owner_approval_request_planning_downstream_expectation_repair_review_v1.json",
    "grant_owner_approval_request_planning_schema_output_repair_review_v1.json",
    "grant_owner_approval_request_planning_evidence_mapping_repair_review_v1.json",
    "grant_owner_approval_request_planning_final_decision_review_v1.json",
    "grant_owner_approval_request_planning_post_repair_rerun_review_v1.json",
    "canonical_checkpoint_scan_only_after_repair_review_v1.json",
    "no_issue_review_created_review_v1.json",
    "no_original_stage_pollution_review_v1.json",
    "no_protocol_change_review_v1.json",
    "owner_constraint_compliance_review_v1.json",
    "common_validation_reuse_report_v1.json",
    "summary.json",
    "verifier_report.json",
)

GO_CONDITIONS_KEYS: Tuple[str, ...] = (
    "canonical_rebuild_go_confirmed",
    "first_failed_stage_grant_owner_approval_request_planning_confirmed",
    "input_output_registry_patch_checkpoint_go_readable",
    "protocol_shared_code_smoke_checkpoint_go_readable",
    "foundation_handoff_planning_checkpoint_go_readable",
    "freeze_authorization_planning_checkpoint_go_readable",
    "original_grant_owner_approval_request_planning_runner_found",
    "original_grant_owner_approval_request_planning_verifier_found",
    "original_grant_owner_approval_request_planning_rerun_attempted",
    "failure_classification_complete",
    "downstream_expectation_gap_checked",
    "minimal_repair_applied",
    "no_issue_review_stage_created",
    "no_gap_review_stage_created",
    "no_rerun_review_stage_created",
    "no_original_summary_forged",
    "no_original_verifier_report_forged",
    "hold_not_marked_as_go",
    "no_protocol_change",
    "no_model_route_touched",
    "no_world_model_assembly",
    "no_scene_graph_smoke_io",
    "no_task_reasoning",
    "no_field_simulation",
    "canonical_scan_only_after_repair_attempted",
    "common_validation_reuse_ok",
    "grant_owner_approval_request_planning_repair_complete",
    "original_grant_owner_approval_request_planning_rerun_recorded",
    "canonical_scan_only_after_repair_recorded",
    "next_phase_readiness_ok",
)

VALID_FINAL_DECISIONS: Tuple[str, ...] = (FINAL_DECISION_COMPLETE, FINAL_DECISION_BLOCKED)
