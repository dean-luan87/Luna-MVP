# -*- coding: utf-8 -*-
"""Issuance post-dryrun review issue review — lineage v1."""

from __future__ import annotations

from typing import Tuple

from capabilities.midplatform.issuance_post_dryrun_review_issue_review_items_v1 import (
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_COMPLETE,
)

FINAL_DECISION_GO = FINAL_DECISION_COMPLETE

WHITELIST_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/field_first_common_validation_v1.py",
    "capabilities/midplatform/issuance_post_dryrun_review_issue_review_items_v1.py",
    "capabilities/midplatform/issuance_post_dryrun_review_issue_review_lineage_v1.py",
    "capabilities/midplatform/issuance_post_dryrun_review_issue_review_v1.py",
    "tools/evaluation/midplatform/run_issuance_post_dryrun_review_issue_review_v1.py",
    "tools/evaluation/midplatform/verify_issuance_post_dryrun_review_issue_review_v1.py",
)

PHASE_PYTHON_FILES: Tuple[str, ...] = WHITELIST_FILES

DOCS: Tuple[str, ...] = (
    "docs/architecture/midplatform/LUNA_MIDPLATFORM_ISSUANCE_POST_DRYRUN_REVIEW_ISSUE_REVIEW_V1.md",
    "docs/architecture/evaluation/LUNA_EVALUATION_ISSUANCE_POST_DRYRUN_REVIEW_ISSUE_REVIEW_V1.md",
    "docs/architecture/evaluation/LUNA_EVALUATION_ISSUANCE_POST_DRYRUN_REVIEW_ISSUE_REVIEW_V1_GO_NO_GO_PACK_V0.md",
)

ARTIFACTS: Tuple[str, ...] = (
    "issuance_post_dryrun_review_issue_review_report_v1.json",
    "issuance_post_dryrun_review_gap_review_v1.json",
    "issuance_post_dryrun_review_artifact_visibility_review_v1.json",
    "issuance_post_dryrun_review_direct_upstream_registry_v1.json",
    "issuance_post_dryrun_review_first_non_go_upstream_review_v1.json",
    "issuance_post_dryrun_review_dryrun_acceptance_review_v1.json",
    "issuance_post_dryrun_review_validate_once_reference_review_v1.json",
    "issuance_post_dryrun_review_precondition_leakage_review_v1.json",
    "issuance_post_dryrun_review_evidence_chain_review_v1.json",
    "issuance_post_dryrun_review_rerun_review_v1.json",
    "record_approval_closure_planning_rerun_readiness_review_v1.json",
    "first_unresolved_gap_review_v1.json",
    "no_protocol_change_review_v1.json",
    "owner_constraint_compliance_review_v1.json",
    "file_size_governance_review_v1.json",
    "common_validation_reuse_report_v1.json",
    "summary.json",
    "verifier_report.json",
)

GO_CONDITIONS_KEYS: Tuple[str, ...] = (
    "record_approval_closure_planning_issue_review_result_b_confirmed",
    "direct_prior_review_upstream_confirmed",
    "issuance_post_dryrun_review_files_exist",
    "issuance_post_dryrun_review_rerun_attempted",
    "issuance_post_dryrun_review_result_recorded",
    "direct_upstream_registry_exists",
    "first_non_go_issuance_upstream_identified",
    "dryrun_acceptance_review_exists",
    "validate_once_reference_review_exists",
    "precondition_leakage_review_exists",
    "evidence_chain_review_exists",
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
