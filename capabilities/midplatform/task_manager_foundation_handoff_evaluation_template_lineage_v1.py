# -*- coding: utf-8 -*-
"""Luna Midplatform Task Manager Foundation Handoff evaluation template lineage v1."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

TEMPLATE_FAMILY = "Task Manager Foundation Handoff Freeze Authorization"
REUSE_MODE = "whitelist_file_template_reuse"

CORE_GO_NO_GO_SCHEMA_KEYS: Tuple[str, ...] = (
    "passed_checks",
    "failed_checks",
    "blocker_count",
    "verifier",
    "summary",
    "go_conditions",
    "forbidden_runtime_flags",
    "chain_trace_nodes",
    "go_no_go_decision",
    "final_decision",
    "next_phase",
    "template_lineage",
)

BASE_DRYRUN_TEMPLATE_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/task_manager_foundation_handoff_freeze_authorization_dryrun_v1.py",
    "tools/evaluation/midplatform/run_midplatform_task_manager_foundation_handoff_freeze_authorization_dryrun_v1.py",
    "tools/evaluation/midplatform/verify_midplatform_task_manager_foundation_handoff_freeze_authorization_dryrun_v1.py",
    "docs/architecture/evaluation/LUNA_EVALUATION_MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_DRYRUN_V1_GO_NO_GO_PACK_V0.md",
)

BASE_GRANT_PLANNING_TEMPLATE_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/task_manager_foundation_handoff_freeze_authorization_grant_planning_v1.py",
    "tools/evaluation/midplatform/run_midplatform_task_manager_foundation_handoff_freeze_authorization_grant_planning_v1.py",
    "tools/evaluation/midplatform/verify_midplatform_task_manager_foundation_handoff_freeze_authorization_grant_planning_v1.py",
    "docs/architecture/evaluation/LUNA_EVALUATION_MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_PLANNING_V1_GO_NO_GO_PACK_V0.md",
)

GRANT_REQUEST_PLANNING_WHITELIST_FILES: Tuple[str, ...] = BASE_GRANT_PLANNING_TEMPLATE_FILES + (
    "capabilities/midplatform/task_manager_foundation_handoff_freeze_authorization_grant_post_dryrun_review_v1.py",
    "tools/evaluation/midplatform/verify_midplatform_task_manager_foundation_handoff_freeze_authorization_grant_post_dryrun_review_v1.py",
)

GRANT_REQUEST_PLANNING_STAGE_TERM_OVERRIDES: Tuple[Dict[str, str], ...] = (
    {"base_term": "grant_planning", "stage_term": "grant_request_planning"},
    {"base_term": "grant_candidate", "stage_term": "request_candidate"},
    {"base_term": "grant-planning-scope", "stage_term": "grant-request-planning-scope"},
    {"base_term": "freeze-authorization-grant-candidate", "stage_term": "grant-request-candidate"},
    {"base_term": "grant_plan_complete", "stage_term": "grant_request_plan_complete"},
    {"base_term": "grant_scope_planning_only", "stage_term": "request_scope_planning_only"},
    {"base_term": "grant_candidate_only", "stage_term": "request_candidate_only"},
)
GRANT_REQUEST_PLANNING_STAGE_ADDITIONS: Tuple[str, ...] = (
    "owner_approval_candidate_only",
    "request_record_absent",
    "owner_approval_candidate",
    "upstream_review_phase",
)

BASE_PLANNING_TEMPLATE_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/task_manager_foundation_handoff_freeze_authorization_planning_v1.py",
    "tools/evaluation/midplatform/run_midplatform_task_manager_foundation_handoff_freeze_authorization_planning_v1.py",
    "tools/evaluation/midplatform/verify_midplatform_task_manager_foundation_handoff_freeze_authorization_planning_v1.py",
    "docs/architecture/evaluation/LUNA_EVALUATION_MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_PLANNING_V1_GO_NO_GO_PACK_V0.md",
)

BASE_POST_REVIEW_TEMPLATE_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/task_manager_foundation_handoff_freeze_authorization_post_dryrun_review_v1.py",
    "tools/evaluation/midplatform/run_midplatform_task_manager_foundation_handoff_freeze_authorization_post_dryrun_review_v1.py",
    "tools/evaluation/midplatform/verify_midplatform_task_manager_foundation_handoff_freeze_authorization_post_dryrun_review_v1.py",
    "docs/architecture/evaluation/LUNA_EVALUATION_MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_POST_DRYRUN_REVIEW_V1_GO_NO_GO_PACK_V0.md",
)

GRANT_DRYRUN_STAGE_TERM_OVERRIDES: Tuple[Dict[str, str], ...] = (
    {"base_term": "freeze_authorization_dryrun", "stage_term": "freeze_authorization_grant_dryrun"},
    {"base_term": "freeze_authorization_candidate", "stage_term": "grant_candidate"},
    {"base_term": "authorization_scope_preserved", "stage_term": "grant_scope_preserved"},
    {"base_term": "freeze_authorization_plan_integrity_ok", "stage_term": "grant_plan_integrity_ok"},
    {"base_term": "freeze_authorization_chain_traceability_ok", "stage_term": "grant_evidence_traceability_ok"},
    {"base_term": "dryrun_only", "stage_term": "grant_dryrun_only"},
    {"base_term": "chain_traceability_matrix", "stage_term": "evidence_traceability"},
    {"base_term": "freeze_state_absence_validation", "stage_term": "prerequisite_validation+boundary_validation"},
)
GRANT_DRYRUN_STAGE_ADDITIONS: Tuple[str, ...] = (
    "grant_token_absent",
    "grant_record_absent",
    "owner_approval_record_absent",
    "grant_prerequisites_satisfied",
)

GRANT_REQUEST_DRYRUN_WHITELIST_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/task_manager_foundation_handoff_freeze_authorization_grant_dryrun_v1.py",
    "tools/evaluation/midplatform/run_midplatform_task_manager_foundation_handoff_freeze_authorization_grant_dryrun_v1.py",
    "tools/evaluation/midplatform/verify_midplatform_task_manager_foundation_handoff_freeze_authorization_grant_dryrun_v1.py",
    "docs/architecture/evaluation/LUNA_EVALUATION_MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_DRYRUN_V1_GO_NO_GO_PACK_V0.md",
    "capabilities/midplatform/task_manager_foundation_handoff_freeze_authorization_grant_request_planning_v1.py",
    "tools/evaluation/midplatform/run_midplatform_task_manager_foundation_handoff_freeze_authorization_grant_request_planning_v1.py",
    "tools/evaluation/midplatform/verify_midplatform_task_manager_foundation_handoff_freeze_authorization_grant_request_planning_v1.py",
)

GRANT_REQUEST_DRYRUN_STAGE_TERM_OVERRIDES: Tuple[Dict[str, str], ...] = (
    {"base_term": "freeze_authorization_grant_dryrun", "stage_term": "freeze_authorization_grant_request_dryrun"},
    {"base_term": "grant_candidate", "stage_term": "request_candidate"},
    {"base_term": "grant_scope_preserved", "stage_term": "request_scope_preserved"},
    {"base_term": "grant_plan_integrity_ok", "stage_term": "grant_request_plan_integrity_ok"},
    {"base_term": "grant_evidence_traceability_ok", "stage_term": "request_evidence_traceability_ok"},
    {"base_term": "grant_dryrun_only", "stage_term": "grant_request_dryrun_only"},
    {"base_term": "grant_prerequisites_satisfied", "stage_term": "request_prerequisites_satisfied"},
    {"base_term": "grant-planning-scope", "stage_term": "grant-request-planning-scope"},
    {"base_term": "grant-dryrun-scope", "stage_term": "grant-request-dryrun-scope"},
    {"base_term": "freeze-authorization-grant-candidate", "stage_term": "grant-request-candidate"},
    {"base_term": "grant_candidate_preserved", "stage_term": "request_candidate_preserved"},
)
GRANT_REQUEST_DRYRUN_STAGE_ADDITIONS: Tuple[str, ...] = (
    "prior_grant_request_planning_go",
    "request_record_absent",
    "owner_approval_candidate_preserved",
    "owner_approval_candidate_validation",
    "grant_token_candidate_ne_grant_token",
)

GRANT_REQUEST_POST_REVIEW_WHITELIST_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/task_manager_foundation_handoff_freeze_authorization_grant_post_dryrun_review_v1.py",
    "tools/evaluation/midplatform/run_midplatform_task_manager_foundation_handoff_freeze_authorization_grant_post_dryrun_review_v1.py",
    "tools/evaluation/midplatform/verify_midplatform_task_manager_foundation_handoff_freeze_authorization_grant_post_dryrun_review_v1.py",
    "docs/architecture/evaluation/LUNA_EVALUATION_MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_POST_DRYRUN_REVIEW_V1_GO_NO_GO_PACK_V0.md",
    "capabilities/midplatform/task_manager_foundation_handoff_freeze_authorization_grant_request_dryrun_v1.py",
    "tools/evaluation/midplatform/verify_midplatform_task_manager_foundation_handoff_freeze_authorization_grant_request_dryrun_v1.py",
)

GRANT_REQUEST_POST_REVIEW_STAGE_TERM_OVERRIDES: Tuple[Dict[str, str], ...] = (
    {"base_term": "freeze_authorization_grant_post_dryrun_review", "stage_term": "freeze_authorization_grant_request_post_dryrun_review"},
    {"base_term": "grant_dryrun_result_accepted", "stage_term": "grant_request_dryrun_result_accepted"},
    {"base_term": "grant_chain_evidence_accepted", "stage_term": "grant_request_chain_evidence_accepted"},
    {"base_term": "grant_absence_confirmed", "stage_term": "request_absence_confirmed"},
    {"base_term": "grant_planning_ready", "stage_term": "issuance_planning_ready"},
    {"base_term": "next_planning_readiness", "stage_term": "issuance_planning_readiness"},
    {"base_term": "grant_absence_review", "stage_term": "request_absence_review"},
    {"base_term": "grant_candidate", "stage_term": "request_candidate"},
    {"base_term": "grant-post-dryrun-review-scope", "stage_term": "grant-request-post-review-scope"},
    {"base_term": "next_planning_ready", "stage_term": "issuance_planning_ready"},
)
GRANT_REQUEST_POST_REVIEW_STAGE_ADDITIONS: Tuple[str, ...] = (
    "request_record_absent",
    "request_absence_confirmed",
    "owner_approval_candidate_preserved",
    "grant_token_candidate_ne_grant_token",
    "authorization_request_absent",
)

GRANT_REQUEST_ISSUANCE_PLANNING_WHITELIST_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/task_manager_foundation_handoff_freeze_authorization_grant_request_planning_v1.py",
    "tools/evaluation/midplatform/run_midplatform_task_manager_foundation_handoff_freeze_authorization_grant_request_planning_v1.py",
    "tools/evaluation/midplatform/verify_midplatform_task_manager_foundation_handoff_freeze_authorization_grant_request_planning_v1.py",
    "capabilities/midplatform/task_manager_foundation_handoff_freeze_authorization_grant_request_post_dryrun_review_v1.py",
    "tools/evaluation/midplatform/verify_midplatform_task_manager_foundation_handoff_freeze_authorization_grant_request_post_dryrun_review_v1.py",
)

GRANT_REQUEST_ISSUANCE_PLANNING_STAGE_TERM_OVERRIDES: Tuple[Dict[str, str], ...] = (
    {"base_term": "grant_request_planning", "stage_term": "grant_request_issuance_planning"},
    {"base_term": "grant-request-planning-scope", "stage_term": "request-issuance-planning-scope"},
    {"base_term": "grant-request-candidate", "stage_term": "request-issuance-candidate"},
    {"base_term": "grant_request_plan_complete", "stage_term": "request_issuance_plan_complete"},
    {"base_term": "request_scope_planning_only", "stage_term": "issuance_scope_planning_only"},
    {"base_term": "request_candidate_only", "stage_term": "request_issuance_candidate_only"},
    {"base_term": "prior_grant_post_review_go", "stage_term": "prior_grant_request_post_review_go"},
)
GRANT_REQUEST_ISSUANCE_PLANNING_STAGE_ADDITIONS: Tuple[str, ...] = (
    "request_record_candidate_only",
    "request_record_candidate",
    "request_issuance_planning_only",
)

GRANT_REQUEST_ISSUANCE_DRYRUN_WHITELIST_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/task_manager_foundation_handoff_freeze_authorization_grant_request_dryrun_v1.py",
    "tools/evaluation/midplatform/run_midplatform_task_manager_foundation_handoff_freeze_authorization_grant_request_dryrun_v1.py",
    "tools/evaluation/midplatform/verify_midplatform_task_manager_foundation_handoff_freeze_authorization_grant_request_dryrun_v1.py",
    "capabilities/midplatform/task_manager_foundation_handoff_freeze_authorization_grant_request_issuance_planning_v1.py",
    "tools/evaluation/midplatform/verify_midplatform_task_manager_foundation_handoff_freeze_authorization_grant_request_issuance_planning_v1.py",
)

GRANT_REQUEST_ISSUANCE_DRYRUN_STAGE_TERM_OVERRIDES: Tuple[Dict[str, str], ...] = (
    {"base_term": "freeze_authorization_grant_request_dryrun", "stage_term": "freeze_authorization_grant_request_issuance_dryrun"},
    {"base_term": "grant_request_plan_integrity_ok", "stage_term": "request_issuance_plan_integrity_ok"},
    {"base_term": "request_scope_preserved", "stage_term": "issuance_scope_preserved"},
    {"base_term": "request_candidate_preserved", "stage_term": "request_issuance_candidate_preserved"},
    {"base_term": "request_prerequisites_satisfied", "stage_term": "issuance_prerequisites_satisfied"},
    {"base_term": "request_evidence_traceability_ok", "stage_term": "issuance_evidence_traceability_ok"},
    {"base_term": "grant_request_dryrun_only", "stage_term": "request_issuance_dryrun_only"},
    {"base_term": "grant-request-dryrun-scope", "stage_term": "request-issuance-dryrun-scope"},
    {"base_term": "grant-request-planning-scope", "stage_term": "request-issuance-planning-scope"},
    {"base_term": "grant-request-candidate", "stage_term": "request-issuance-candidate"},
    {"base_term": "prior_grant_request_planning_go", "stage_term": "prior_request_issuance_planning_go"},
)
GRANT_REQUEST_ISSUANCE_DRYRUN_STAGE_ADDITIONS: Tuple[str, ...] = (
    "prior_request_issuance_planning_go",
    "request_record_candidate_preserved",
    "request_record_candidate_validation",
)

GRANT_REQUEST_ISSUANCE_POST_REVIEW_WHITELIST_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/task_manager_foundation_handoff_freeze_authorization_grant_request_post_dryrun_review_v1.py",
    "tools/evaluation/midplatform/run_midplatform_task_manager_foundation_handoff_freeze_authorization_grant_request_post_dryrun_review_v1.py",
    "tools/evaluation/midplatform/verify_midplatform_task_manager_foundation_handoff_freeze_authorization_grant_request_post_dryrun_review_v1.py",
    "capabilities/midplatform/task_manager_foundation_handoff_freeze_authorization_grant_request_issuance_dryrun_v1.py",
    "tools/evaluation/midplatform/verify_midplatform_task_manager_foundation_handoff_freeze_authorization_grant_request_issuance_dryrun_v1.py",
)

GRANT_REQUEST_ISSUANCE_POST_REVIEW_STAGE_TERM_OVERRIDES: Tuple[Dict[str, str], ...] = (
    {"base_term": "freeze_authorization_grant_request_post_dryrun_review", "stage_term": "freeze_authorization_grant_request_issuance_post_dryrun_review"},
    {"base_term": "grant_request_dryrun_result_accepted", "stage_term": "request_issuance_dryrun_result_accepted"},
    {"base_term": "grant_request_chain_evidence_accepted", "stage_term": "request_issuance_chain_evidence_accepted"},
    {"base_term": "request_absence_confirmed", "stage_term": "issuance_absence_confirmed"},
    {"base_term": "issuance_planning_ready", "stage_term": "request_record_planning_ready"},
    {"base_term": "issuance_planning_readiness", "stage_term": "request_record_planning_readiness"},
    {"base_term": "request_absence_review", "stage_term": "issuance_absence_review"},
    {"base_term": "request_candidate", "stage_term": "request_issuance_candidate"},
    {"base_term": "request_candidate_preserved", "stage_term": "request_issuance_candidate_preserved"},
    {"base_term": "grant-request-post-review-scope", "stage_term": "request-issuance-post-review-scope"},
)
GRANT_REQUEST_ISSUANCE_POST_REVIEW_STAGE_ADDITIONS: Tuple[str, ...] = (
    "request_record_candidate_preserved",
    "issuance_absence_confirmed",
    "request_issuance_candidate_preserved",
    "authorization_request_issued",
    "request_record_absent",
)

GRANT_REQUEST_RECORD_PLANNING_WHITELIST_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/task_manager_foundation_handoff_freeze_authorization_grant_request_issuance_planning_v1.py",
    "tools/evaluation/midplatform/run_midplatform_task_manager_foundation_handoff_freeze_authorization_grant_request_issuance_planning_v1.py",
    "tools/evaluation/midplatform/verify_midplatform_task_manager_foundation_handoff_freeze_authorization_grant_request_issuance_planning_v1.py",
    "capabilities/midplatform/task_manager_foundation_handoff_freeze_authorization_grant_request_issuance_post_dryrun_review_v1.py",
    "tools/evaluation/midplatform/verify_midplatform_task_manager_foundation_handoff_freeze_authorization_grant_request_issuance_post_dryrun_review_v1.py",
)

GRANT_REQUEST_RECORD_PLANNING_STAGE_TERM_OVERRIDES: Tuple[Dict[str, str], ...] = (
    {"base_term": "grant_request_issuance_planning", "stage_term": "grant_request_record_planning"},
    {"base_term": "request-issuance-planning-scope", "stage_term": "request-record-planning-scope"},
    {"base_term": "request-issuance-candidate", "stage_term": "request-record-candidate"},
    {"base_term": "request_issuance_plan_complete", "stage_term": "request_record_plan_complete"},
    {"base_term": "issuance_scope_planning_only", "stage_term": "record_scope_planning_only"},
    {"base_term": "request_issuance_candidate_only", "stage_term": "request_record_candidate_only"},
    {"base_term": "prior_grant_request_post_review_go", "stage_term": "prior_request_issuance_post_review_go"},
    {"base_term": "request_issuance_planning_only", "stage_term": "request_record_planning_only"},
)
GRANT_REQUEST_RECORD_PLANNING_STAGE_ADDITIONS: Tuple[str, ...] = (
    "request_record_schema_candidate_only",
    "evidence_binding_candidate_only",
    "owner_approval_binding_candidate_only",
    "revocation_reference_candidate_only",
    "authorization_request_candidate",
    "request_record_schema_candidate",
    "evidence_binding_candidate",
    "owner_approval_binding_candidate",
    "revocation_reference_candidate",
)

GRANT_REQUEST_RECORD_DRYRUN_WHITELIST_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/task_manager_foundation_handoff_freeze_authorization_grant_request_issuance_dryrun_v1.py",
    "tools/evaluation/midplatform/run_midplatform_task_manager_foundation_handoff_freeze_authorization_grant_request_issuance_dryrun_v1.py",
    "tools/evaluation/midplatform/verify_midplatform_task_manager_foundation_handoff_freeze_authorization_grant_request_issuance_dryrun_v1.py",
    "capabilities/midplatform/task_manager_foundation_handoff_freeze_authorization_grant_request_record_planning_v1.py",
    "tools/evaluation/midplatform/verify_midplatform_task_manager_foundation_handoff_freeze_authorization_grant_request_record_planning_v1.py",
)

GRANT_REQUEST_RECORD_DRYRUN_STAGE_TERM_OVERRIDES: Tuple[Dict[str, str], ...] = (
    {"base_term": "freeze_authorization_grant_request_issuance_dryrun", "stage_term": "freeze_authorization_grant_request_record_dryrun"},
    {"base_term": "request_issuance_plan_integrity_ok", "stage_term": "request_record_plan_integrity_ok"},
    {"base_term": "issuance_scope_preserved", "stage_term": "record_scope_preserved"},
    {"base_term": "request_issuance_candidate_preserved", "stage_term": "request_record_candidate_preserved"},
    {"base_term": "issuance_prerequisites_satisfied", "stage_term": "record_prerequisites_satisfied"},
    {"base_term": "issuance_evidence_traceability_ok", "stage_term": "record_evidence_traceability_ok"},
    {"base_term": "request_issuance_dryrun_only", "stage_term": "request_record_dryrun_only"},
    {"base_term": "prior_request_issuance_planning_go", "stage_term": "prior_request_record_planning_go"},
    {"base_term": "request-issuance-dryrun-scope", "stage_term": "request-record-dryrun-scope"},
    {"base_term": "request-issuance-planning-scope", "stage_term": "request-record-planning-scope"},
    {"base_term": "owner_approval_candidate_preserved", "stage_term": "owner_approval_binding_candidate_preserved"},
)
GRANT_REQUEST_RECORD_DRYRUN_STAGE_ADDITIONS: Tuple[str, ...] = (
    "prior_request_record_planning_go",
    "request_record_schema_candidate_preserved",
    "evidence_binding_candidate_preserved",
    "candidate_lifecycle_preserved",
    "revocation_reference_candidate_preserved",
    "request_record_schema_final_absent",
    "evidence_bound_record_absent",
)

GRANT_REQUEST_RECORD_POST_REVIEW_WHITELIST_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/task_manager_foundation_handoff_freeze_authorization_grant_request_issuance_post_dryrun_review_v1.py",
    "tools/evaluation/midplatform/run_midplatform_task_manager_foundation_handoff_freeze_authorization_grant_request_issuance_post_dryrun_review_v1.py",
    "tools/evaluation/midplatform/verify_midplatform_task_manager_foundation_handoff_freeze_authorization_grant_request_issuance_post_dryrun_review_v1.py",
    "capabilities/midplatform/task_manager_foundation_handoff_freeze_authorization_grant_request_record_dryrun_v1.py",
    "tools/evaluation/midplatform/verify_midplatform_task_manager_foundation_handoff_freeze_authorization_grant_request_record_dryrun_v1.py",
)

GRANT_REQUEST_RECORD_POST_REVIEW_STAGE_TERM_OVERRIDES: Tuple[Dict[str, str], ...] = (
    {"base_term": "freeze_authorization_grant_request_issuance_post_dryrun_review", "stage_term": "freeze_authorization_grant_request_record_post_dryrun_review"},
    {"base_term": "request_issuance_dryrun_result_accepted", "stage_term": "request_record_dryrun_result_accepted"},
    {"base_term": "request_issuance_chain_evidence_accepted", "stage_term": "request_record_chain_evidence_accepted"},
    {"base_term": "issuance_absence_confirmed", "stage_term": "record_absence_confirmed"},
    {"base_term": "request_record_planning_ready", "stage_term": "owner_approval_planning_ready"},
    {"base_term": "request_record_planning_readiness", "stage_term": "owner_approval_planning_readiness"},
    {"base_term": "issuance_absence_review", "stage_term": "record_absence_review"},
    {"base_term": "request-issuance-post-review-scope", "stage_term": "request-record-post-review-scope"},
    {"base_term": "request_issuance_candidate_preserved", "stage_term": "request_record_candidate_preserved"},
)
GRANT_REQUEST_RECORD_POST_REVIEW_STAGE_ADDITIONS: Tuple[str, ...] = (
    "request_record_schema_candidate_preserved",
    "evidence_binding_candidate_preserved",
    "owner_approval_binding_candidate_preserved",
    "candidate_lifecycle_preserved",
    "revocation_reference_candidate_preserved",
    "record_absence_confirmed",
    "request_record_schema_final_absent",
    "evidence_bound_record_absent",
    "schema_review",
    "binding_review",
    "lifecycle_review",
    "revocation_review",
)

GRANT_OWNER_APPROVAL_PLANNING_WHITELIST_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/task_manager_foundation_handoff_freeze_authorization_grant_request_record_planning_v1.py",
    "tools/evaluation/midplatform/run_midplatform_task_manager_foundation_handoff_freeze_authorization_grant_request_record_planning_v1.py",
    "tools/evaluation/midplatform/verify_midplatform_task_manager_foundation_handoff_freeze_authorization_grant_request_record_planning_v1.py",
    "capabilities/midplatform/task_manager_foundation_handoff_freeze_authorization_grant_request_record_post_dryrun_review_v1.py",
    "tools/evaluation/midplatform/verify_midplatform_task_manager_foundation_handoff_freeze_authorization_grant_request_record_post_dryrun_review_v1.py",
)

GRANT_OWNER_APPROVAL_PLANNING_STAGE_TERM_OVERRIDES: Tuple[Dict[str, str], ...] = (
    {"base_term": "grant_request_record_planning", "stage_term": "grant_owner_approval_planning"},
    {"base_term": "request-record-planning-scope", "stage_term": "owner-approval-planning-scope"},
    {"base_term": "request-record-candidate", "stage_term": "owner-approval-candidate"},
    {"base_term": "request_record_plan_complete", "stage_term": "owner_approval_plan_complete"},
    {"base_term": "record_scope_planning_only", "stage_term": "approval_scope_planning_only"},
    {"base_term": "prior_request_issuance_post_review_go", "stage_term": "prior_request_record_post_review_go"},
    {"base_term": "request_record_planning_only", "stage_term": "owner_approval_planning_only"},
    {"base_term": "evidence_binding_candidate_only", "stage_term": "approval_evidence_binding_candidate_only"},
)
GRANT_OWNER_APPROVAL_PLANNING_STAGE_ADDITIONS: Tuple[str, ...] = (
    "owner_operator_ack_candidate_only",
    "request_record_binding_candidate_only",
    "approval_lifecycle_candidate_only",
    "expiry_revocation_reference_candidate_only",
    "owner_operator_ack_candidate",
    "approval_evidence_binding_candidate",
    "approval_scope_candidate",
    "owner_operator_ack_record_absent",
    "approval_evidence_bound_record_absent",
)

GRANT_OWNER_APPROVAL_DRYRUN_WHITELIST_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/task_manager_foundation_handoff_freeze_authorization_grant_request_record_dryrun_v1.py",
    "tools/evaluation/midplatform/run_midplatform_task_manager_foundation_handoff_freeze_authorization_grant_request_record_dryrun_v1.py",
    "tools/evaluation/midplatform/verify_midplatform_task_manager_foundation_handoff_freeze_authorization_grant_request_record_dryrun_v1.py",
    "capabilities/midplatform/task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_planning_v1.py",
    "tools/evaluation/midplatform/verify_midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_planning_v1.py",
)

GRANT_OWNER_APPROVAL_DRYRUN_STAGE_TERM_OVERRIDES: Tuple[Dict[str, str], ...] = (
    {"base_term": "freeze_authorization_grant_request_record_dryrun", "stage_term": "freeze_authorization_grant_owner_approval_dryrun"},
    {"base_term": "request_record_plan_integrity_ok", "stage_term": "owner_approval_plan_integrity_ok"},
    {"base_term": "record_scope_preserved", "stage_term": "approval_scope_preserved"},
    {"base_term": "request_record_candidate_preserved", "stage_term": "owner_approval_candidate_preserved"},
    {"base_term": "record_prerequisites_satisfied", "stage_term": "approval_prerequisites_satisfied"},
    {"base_term": "record_evidence_traceability_ok", "stage_term": "approval_evidence_traceability_ok"},
    {"base_term": "request_record_dryrun_only", "stage_term": "owner_approval_dryrun_only"},
    {"base_term": "prior_request_record_planning_go", "stage_term": "prior_owner_approval_planning_go"},
    {"base_term": "request-record-dryrun-scope", "stage_term": "owner-approval-dryrun-scope"},
    {"base_term": "request-record-planning-scope", "stage_term": "owner-approval-planning-scope"},
    {"base_term": "owner_approval_binding_candidate_preserved", "stage_term": "owner_operator_ack_candidate_preserved"},
)
GRANT_OWNER_APPROVAL_DRYRUN_STAGE_ADDITIONS: Tuple[str, ...] = (
    "prior_owner_approval_planning_go",
    "owner_operator_ack_candidate_preserved",
    "approval_evidence_binding_candidate_preserved",
    "request_record_binding_candidate_preserved",
    "approval_lifecycle_candidate_preserved",
    "expiry_revocation_reference_candidate_preserved",
    "owner_operator_ack_record_absent",
    "approval_evidence_bound_record_absent",
    "protocol_standard_reference_ok",
    "protocol_id_reference_ok",
    "error_namespace_reference_ok",
    "protocol_execution_result_schema_ref_ok",
    "separation_rule_ref_ok",
    "shared_protocol_system_revalidation",
)

GRANT_OWNER_APPROVAL_POST_REVIEW_WHITELIST_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/task_manager_foundation_handoff_freeze_authorization_grant_request_record_post_dryrun_review_v1.py",
    "tools/evaluation/midplatform/run_midplatform_task_manager_foundation_handoff_freeze_authorization_grant_request_record_post_dryrun_review_v1.py",
    "tools/evaluation/midplatform/verify_midplatform_task_manager_foundation_handoff_freeze_authorization_grant_request_record_post_dryrun_review_v1.py",
    "capabilities/midplatform/task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_dryrun_v1.py",
    "tools/evaluation/midplatform/verify_midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_dryrun_v1.py",
)

GRANT_OWNER_APPROVAL_POST_REVIEW_STAGE_TERM_OVERRIDES: Tuple[Dict[str, str], ...] = (
    {
        "base_term": "freeze_authorization_grant_request_record_post_dryrun_review",
        "stage_term": "freeze_authorization_grant_owner_approval_post_dryrun_review",
    },
    {"base_term": "request_record_dryrun_result_accepted", "stage_term": "owner_approval_dryrun_result_accepted"},
    {"base_term": "request_record_chain_evidence_accepted", "stage_term": "evidence_chain_review_ok"},
    {"base_term": "record_absence_confirmed", "stage_term": "absence_review_ok"},
    {"base_term": "owner_approval_planning_ready", "stage_term": "owner_approval_request_planning_ready"},
    {"base_term": "request-record-post-review-scope", "stage_term": "owner-approval-post-review-scope"},
    {"base_term": "request_record_candidate_preserved", "stage_term": "candidate_state_preserved"},
    {"base_term": "owner_approval_binding_candidate_preserved", "stage_term": "owner_operator_ack_candidate_preserved"},
)
GRANT_OWNER_APPROVAL_POST_REVIEW_STAGE_ADDITIONS: Tuple[str, ...] = (
    "prior_owner_approval_dryrun_go",
    "protocol_reference_review_ok",
    "separation_rule_review_ok",
    "approval_evidence_binding_candidate_preserved",
    "request_record_binding_candidate_preserved",
    "approval_lifecycle_candidate_preserved",
    "expiry_revocation_reference_candidate_preserved",
    "owner_operator_ack_record_absent",
    "approval_evidence_bound_record_absent",
    "protocol_reference_review",
    "separation_rule_review",
    "shared_protocol_system_revalidation",
    "next_phase_readiness_ok",
)

GRANT_OWNER_APPROVAL_REQUEST_PLANNING_WHITELIST_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_post_dryrun_review_v1.py",
    "tools/evaluation/midplatform/run_midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_post_dryrun_review_v1.py",
    "tools/evaluation/midplatform/verify_midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_post_dryrun_review_v1.py",
    "capabilities/midplatform/protocol_input_output_symmetry_registry_patch_v1.py",
    "tools/evaluation/midplatform/run_midplatform_protocol_input_output_symmetry_registry_patch_v1.py",
    "tools/evaluation/midplatform/verify_midplatform_protocol_input_output_symmetry_registry_patch_v1.py",
    "capabilities/midplatform/protocol_canonical_standard_shared_code_smoke_v1.py",
)

GRANT_OWNER_APPROVAL_REQUEST_PLANNING_STAGE_TERM_OVERRIDES: Tuple[Dict[str, str], ...] = (
    {"base_term": "grant_owner_approval_planning", "stage_term": "grant_owner_approval_request_planning"},
    {"base_term": "owner-approval-planning-scope", "stage_term": "owner-approval-request-planning-scope"},
    {"base_term": "owner_approval_plan_complete", "stage_term": "owner_approval_request_plan_complete"},
    {"base_term": "owner_approval_candidate_only", "stage_term": "approval_request_candidate_only"},
    {"base_term": "prior_request_record_post_review_go", "stage_term": "prior_owner_approval_post_review_go"},
    {"base_term": "owner_approval_planning_only", "stage_term": "owner_approval_request_planning_only"},
    {"base_term": "owner_approval_candidate", "stage_term": "approval_request_candidate"},
    {"base_term": "owner_approval_planning_ready", "stage_term": "owner_approval_request_dryrun_ready"},
)

GRANT_OWNER_APPROVAL_REQUEST_PLANNING_STAGE_ADDITIONS: Tuple[str, ...] = (
    "prior_input_output_registry_patch_go",
    "prior_shared_code_smoke_go",
    "approval_request_candidate_classified_as_input_candidate",
    "input_candidate_protocol_reference_ok",
    "output_candidate_protocol_reference_ok",
    "input_output_symmetry_reference_ok",
    "protocol_traceability_reference_ok",
    "l2_taskmanager_owner_approval_request_protocol_reference_ok",
    "traceability_rule_ref_ok",
    "input_candidate_contract_complete",
    "output_candidate_contract_complete",
    "input_output_traceability_contract_complete",
    "error_namespace_mapping_ok",
    "whitebox_candidate_ref_mapping_ok",
    "owner_operator_notification_candidate_only",
    "rejection_reference_candidate_only",
    "expiry_reference_candidate_only",
    "revocation_reference_candidate_only",
    "owner_approval_request_absent",
    "protocol_runtime_absent",
    "whitebox_runtime_integration_absent",
    "input_output_registry_patch_ref",
)

GRANT_OWNER_APPROVAL_REQUEST_DRYRUN_WHITELIST_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_planning_v1.py",
    "tools/evaluation/midplatform/run_midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_planning_v1.py",
    "tools/evaluation/midplatform/verify_midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_planning_v1.py",
    "capabilities/midplatform/task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_dryrun_v1.py",
    "tools/evaluation/midplatform/verify_midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_dryrun_v1.py",
    "capabilities/midplatform/protocol_input_output_symmetry_registry_patch_v1.py",
    "capabilities/midplatform/protocol_canonical_standard_shared_code_smoke_v1.py",
)

GRANT_OWNER_APPROVAL_REQUEST_DRYRUN_STAGE_TERM_OVERRIDES: Tuple[Dict[str, str], ...] = (
    {"base_term": "freeze_authorization_grant_owner_approval_dryrun", "stage_term": "freeze_authorization_grant_owner_approval_request_dryrun"},
    {"base_term": "owner_approval_plan_integrity_ok", "stage_term": "owner_approval_request_plan_integrity_ok"},
    {"base_term": "owner_approval_candidate_preserved", "stage_term": "approval_request_candidate_validation_ok"},
    {"base_term": "approval_scope_preserved", "stage_term": "approval_request_scope_preserved"},
    {"base_term": "prior_owner_approval_planning_go", "stage_term": "prior_owner_approval_request_planning_go"},
    {"base_term": "owner_approval_dryrun_only", "stage_term": "owner_approval_request_dryrun_only"},
    {"base_term": "owner-approval-dryrun-scope", "stage_term": "owner-approval-request-dryrun-scope"},
    {"base_term": "owner_approval_candidate", "stage_term": "approval_request_candidate"},
    {"base_term": "owner_operator_ack_candidate_preserved", "stage_term": "output_candidate_contract_validation_ok"},
)

GRANT_OWNER_APPROVAL_REQUEST_DRYRUN_STAGE_ADDITIONS: Tuple[str, ...] = (
    "prior_input_output_registry_patch_go",
    "prior_shared_code_smoke_go",
    "approval_request_candidate_validation_ok",
    "input_candidate_protocol_reference_ok",
    "output_candidate_protocol_reference_ok",
    "input_output_symmetry_reference_ok",
    "protocol_traceability_reference_ok",
    "l2_taskmanager_owner_approval_request_protocol_reference_ok",
    "traceability_rule_ref_ok",
    "input_candidate_contract_validation_ok",
    "output_candidate_contract_validation_ok",
    "input_output_traceability_validation_ok",
    "protocol_traceability_validation_ok",
    "error_namespace_validation_ok",
    "whitebox_candidate_ref_validation_ok",
    "owner_operator_notification_candidate_only",
    "rejection_reference_candidate_only",
    "expiry_reference_candidate_only",
    "revocation_reference_candidate_only",
    "owner_approval_request_absent",
    "protocol_runtime_absent",
    "whitebox_runtime_integration_absent",
    "input_output_registry_patch_ref",
    "traceability_rule_ref",
    "validate_once_per_module_rule_ok",
    "first_protocol_validation_recorded",
)

GRANT_OWNER_APPROVAL_REQUEST_POST_REVIEW_WHITELIST_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_post_dryrun_review_v1.py",
    "tools/evaluation/midplatform/run_midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_post_dryrun_review_v1.py",
    "tools/evaluation/midplatform/verify_midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_post_dryrun_review_v1.py",
    "capabilities/midplatform/task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_dryrun_v1.py",
    "tools/evaluation/midplatform/verify_midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_dryrun_v1.py",
)

GRANT_OWNER_APPROVAL_REQUEST_POST_REVIEW_STAGE_TERM_OVERRIDES: Tuple[Dict[str, str], ...] = (
    {
        "base_term": "freeze_authorization_grant_owner_approval_post_dryrun_review",
        "stage_term": "freeze_authorization_grant_owner_approval_request_post_dryrun_review",
    },
    {
        "base_term": "owner_approval_dryrun_result_accepted",
        "stage_term": "owner_approval_request_dryrun_result_accepted",
    },
    {
        "base_term": "prior_owner_approval_dryrun_go",
        "stage_term": "prior_owner_approval_request_dryrun_go",
    },
    {"base_term": "owner-approval-post-review-scope", "stage_term": "owner-approval-request-post-review-scope"},
    {"base_term": "candidate_state_preserved", "stage_term": "approval_request_candidate_review_ok"},
    {"base_term": "owner_operator_ack_candidate_preserved", "stage_term": "output_candidate_review_ok"},
    {
        "base_term": "owner_approval_request_planning_ready",
        "stage_term": "owner_approval_request_issuance_planning_ready",
    },
    {"base_term": "evidence_chain_review_ok", "stage_term": "evidence_chain_review_ok"},
)

GRANT_OWNER_APPROVAL_REQUEST_ISSUANCE_PLANNING_WHITELIST_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_planning_v1.py",
    "tools/evaluation/midplatform/run_midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_planning_v1.py",
    "tools/evaluation/midplatform/verify_midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_planning_v1.py",
    "capabilities/midplatform/task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_post_dryrun_review_v1.py",
    "tools/evaluation/midplatform/verify_midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_post_dryrun_review_v1.py",
)

GRANT_OWNER_APPROVAL_REQUEST_ISSUANCE_PLANNING_STAGE_TERM_OVERRIDES: Tuple[Dict[str, str], ...] = (
    {"base_term": "grant_owner_approval_request_planning", "stage_term": "grant_owner_approval_request_issuance_planning"},
    {"base_term": "owner-approval-request-planning-scope", "stage_term": "owner-approval-request-issuance-planning-scope"},
    {"base_term": "owner_approval_request_plan_complete", "stage_term": "owner_approval_request_issuance_plan_complete"},
    {"base_term": "approval_request_candidate_only", "stage_term": "issuance_candidate_only"},
    {"base_term": "prior_owner_approval_post_review_go", "stage_term": "prior_owner_approval_request_post_review_go"},
    {"base_term": "approval_request_candidate", "stage_term": "owner_approval_request_issuance_candidate"},
    {"base_term": "owner_approval_request_dryrun_ready", "stage_term": "owner_approval_request_issuance_dryrun_ready"},
)

GRANT_OWNER_APPROVAL_REQUEST_ISSUANCE_PLANNING_STAGE_ADDITIONS: Tuple[str, ...] = (
    "prior_owner_approval_request_post_review_go",
    "prior_validate_once_rule_review_go",
    "issuance_candidate_classified_as_input_candidate",
    "issuance_candidate_source_input_ref_ok",
    "issuance_input_candidate_contract_complete",
    "issuance_output_candidate_contract_complete",
    "issuance_input_output_traceability_contract_complete",
    "issuance_protocol_traceability_contract_complete",
    "validate_once_per_module_rule_ref_ok",
    "reuse_first_rule_ref_ok",
    "l1_input_output_protocol_revalidation",
    "owner_approval_request_issued_absent",
    "owner_operator_notification_sent_absent",
    "precondition_candidate_only",
    "owner_operator_notification_issuance_candidate_only",
    "prior_owner_approval_request_post_review_ref",
)

GRANT_OWNER_APPROVAL_REQUEST_ISSUANCE_DRYRUN_WHITELIST_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_issuance_planning_v1.py",
    "tools/evaluation/midplatform/run_midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_issuance_planning_v1.py",
    "tools/evaluation/midplatform/verify_midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_issuance_planning_v1.py",
    "capabilities/midplatform/task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_dryrun_v1.py",
    "tools/evaluation/midplatform/verify_midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_dryrun_v1.py",
)

GRANT_OWNER_APPROVAL_REQUEST_ISSUANCE_DRYRUN_STAGE_TERM_OVERRIDES: Tuple[Dict[str, str], ...] = (
    {"base_term": "grant_owner_approval_request_issuance_planning", "stage_term": "grant_owner_approval_request_issuance_dryrun"},
    {"base_term": "owner_approval_request_issuance_planning_only", "stage_term": "owner_approval_request_issuance_dryrun_only"},
    {"base_term": "owner_approval_request_issuance_plan_complete", "stage_term": "owner_approval_request_issuance_plan_integrity_ok"},
    {"base_term": "issuance_candidate_only", "stage_term": "issuance_candidate_validation_ok"},
    {"base_term": "issuance_input_candidate_contract_complete", "stage_term": "issuance_input_candidate_validation_ok"},
    {"base_term": "issuance_output_candidate_contract_complete", "stage_term": "issuance_output_candidate_validation_ok"},
    {"base_term": "issuance_input_output_traceability_contract_complete", "stage_term": "issuance_input_output_traceability_validation_ok"},
    {"base_term": "issuance_protocol_traceability_contract_complete", "stage_term": "issuance_protocol_traceability_validation_ok"},
    {"base_term": "prior_owner_approval_request_post_review_go", "stage_term": "prior_owner_approval_request_issuance_planning_go"},
    {"base_term": "owner_approval_request_issuance_dryrun_ready", "stage_term": "owner_approval_request_issuance_post_review_ready"},
)

GRANT_OWNER_APPROVAL_REQUEST_ISSUANCE_DRYRUN_STAGE_ADDITIONS: Tuple[str, ...] = (
    "prior_owner_approval_request_issuance_planning_go",
    "owner_approval_request_issuance_plan_integrity_ok",
    "issuance_candidate_validation_ok",
    "issuance_candidate_classified_as_input_candidate",
    "issuance_candidate_source_input_ref_ok",
    "issuance_input_candidate_validation_ok",
    "issuance_output_candidate_validation_ok",
    "issuance_input_output_traceability_validation_ok",
    "issuance_protocol_traceability_validation_ok",
    "validate_once_per_module_rule_ref_ok",
    "owner_approval_request_issued_absent",
    "owner_operator_notification_sent_absent",
    "owner_operator_notification_issuance_candidate_only",
    "precondition_candidate_only",
    "prior_owner_approval_request_issuance_planning_ref",
    "l1_input_output_protocol_revalidation",
)

GRANT_OWNER_APPROVAL_REQUEST_ISSUANCE_POST_REVIEW_WHITELIST_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_post_dryrun_review_v1.py",
    "tools/evaluation/midplatform/run_midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_post_dryrun_review_v1.py",
    "tools/evaluation/midplatform/verify_midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_post_dryrun_review_v1.py",
    "capabilities/midplatform/task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_issuance_dryrun_v1.py",
    "tools/evaluation/midplatform/verify_midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_issuance_dryrun_v1.py",
)

GRANT_OWNER_APPROVAL_REQUEST_ISSUANCE_POST_REVIEW_STAGE_TERM_OVERRIDES: Tuple[Dict[str, str], ...] = (
    {
        "base_term": "freeze_authorization_grant_owner_approval_request_post_dryrun_review",
        "stage_term": "freeze_authorization_grant_owner_approval_request_issuance_post_dryrun_review",
    },
    {
        "base_term": "owner_approval_request_dryrun_result_accepted",
        "stage_term": "issuance_dryrun_result_accepted",
    },
    {
        "base_term": "prior_owner_approval_request_dryrun_go",
        "stage_term": "prior_owner_approval_request_issuance_dryrun_go",
    },
    {
        "base_term": "owner-approval-request-post-review-scope",
        "stage_term": "owner-approval-request-issuance-post-review-scope",
    },
    {
        "base_term": "approval_request_candidate_review_ok",
        "stage_term": "issuance_candidate_review_ok",
    },
    {
        "base_term": "output_candidate_review_ok",
        "stage_term": "issuance_output_candidate_review_ok",
    },
    {
        "base_term": "validate_once_per_module_rule_review_ok",
        "stage_term": "validate_once_reference_review_ok",
    },
    {
        "base_term": "owner_approval_request_issuance_planning_ready",
        "stage_term": "record_approval_closure_planning_ready",
    },
)

GRANT_OWNER_APPROVAL_REQUEST_ISSUANCE_POST_REVIEW_STAGE_ADDITIONS: Tuple[str, ...] = (
    "prior_owner_approval_request_issuance_dryrun_go",
    "issuance_dryrun_result_accepted",
    "issuance_candidate_review_ok",
    "issuance_output_candidate_review_ok",
    "issuance_input_output_traceability_review_ok",
    "issuance_protocol_traceability_review_ok",
    "protocol_reference_review_ok",
    "error_namespace_review_ok",
    "whitebox_candidate_ref_review_ok",
    "validate_once_reference_review_ok",
    "timeout_event_review_ok",
    "owner_operator_notification_issuance_candidate_only",
    "precondition_candidate_only",
    "rejection_reference_candidate_only",
    "expiry_reference_candidate_only",
    "revocation_reference_candidate_only",
    "l1_input_output_protocol_revalidation",
    "next_phase_readiness_ok",
    "file_size_governance_review_ok",
    "file_size_governance_review_exists",
    "monolithic_file_absent",
    "large_file_read_avoidance_ok",
    "summary_index_first_reading_ok",
    "template_lineage_growth_controlled",
    "shared_constants_split_ok",
    "verifier_large_file_scan_absent",
)

GRANT_OWNER_APPROVAL_REQUEST_RECORD_APPROVAL_CLOSURE_PLANNING_WHITELIST_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_issuance_post_dryrun_review_v1.py",
    "tools/evaluation/midplatform/run_midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_issuance_post_dryrun_review_v1.py",
    "tools/evaluation/midplatform/verify_midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_issuance_post_dryrun_review_v1.py",
    "capabilities/midplatform/task_manager_foundation_handoff_freeze_authorization_grant_request_record_planning_v1.py",
    "tools/evaluation/midplatform/verify_midplatform_task_manager_foundation_handoff_freeze_authorization_grant_request_record_planning_v1.py",
)

GRANT_OWNER_APPROVAL_REQUEST_RECORD_APPROVAL_CLOSURE_PLANNING_STAGE_TERM_OVERRIDES: Tuple[Dict[str, str], ...] = (
    {
        "base_term": "grant_request_record_planning",
        "stage_term": "grant_owner_approval_request_record_approval_closure_planning",
    },
    {
        "base_term": "request-record-planning-scope",
        "stage_term": "record-approval-closure-planning-scope",
    },
    {
        "base_term": "request_record_plan_complete",
        "stage_term": "record_approval_closure_plan_complete",
    },
    {
        "base_term": "request_record_candidate_only",
        "stage_term": "owner_approval_request_record_candidate_only",
    },
    {
        "base_term": "prior_request_issuance_post_review_go",
        "stage_term": "prior_owner_approval_request_issuance_post_review_go",
    },
    {
        "base_term": "request_record_planning_only",
        "stage_term": "record_approval_closure_planning_only",
    },
    {
        "base_term": "request-record-candidate",
        "stage_term": "owner-approval-request-record-candidate",
    },
    {
        "base_term": "request_record_dryrun_ready",
        "stage_term": "record_approval_closure_dryrun_ready",
    },
)

GRANT_OWNER_APPROVAL_REQUEST_RECORD_APPROVAL_CLOSURE_PLANNING_STAGE_ADDITIONS: Tuple[str, ...] = (
    "prior_owner_approval_request_issuance_post_review_go",
    "record_candidate_closure_matrix_complete",
    "approval_candidate_closure_matrix_complete",
    "ack_candidate_closure_matrix_complete",
    "evidence_binding_closure_matrix_complete",
    "traceability_matrix_complete",
    "protocol_reference_matrix_ok",
    "error_namespace_matrix_ok",
    "whitebox_candidate_ref_matrix_ok",
    "rejection_reference_candidate_only",
    "expiry_reference_candidate_only",
    "revocation_reference_candidate_only",
    "owner_approval_request_record_candidate",
    "owner_approval_record_candidate",
    "owner_operator_ack_record_candidate",
    "approval_evidence_bound_record_candidate",
    "owner_approval_request_record_approval_closure_candidate",
    "request_issued_absent",
    "notification_sent_absent",
    "ack_record_absent",
    "evidence_bound_record_absent",
    "grant_absent",
    "runtime_execution_absent",
    "protocol_runtime_absent",
    "whitebox_runtime_integration_absent",
    "module_adapter_implementation_absent",
    "shared_protocol_system_revalidation",
    "l1_input_output_protocol_revalidation",
    "file_size_governance_review_exists",
    "file_size_governance_review_ok",
    "monolithic_file_absent",
    "large_file_read_avoidance_ok",
    "summary_index_first_reading_ok",
    "full_repo_scan_absent",
    "tmp_eval_out_scan_absent",
    "limited_directory_scan_ok",
    "template_lineage_growth_controlled",
    "template_lineage_growth_warning",
    "verifier_large_file_scan_absent",
)

GRANT_OWNER_APPROVAL_REQUEST_RECORD_APPROVAL_CLOSURE_DRYRUN_WHITELIST_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/task_manager_foundation_handoff_freeze_authorization_grant_request_record_dryrun_v1.py",
    "tools/evaluation/midplatform/run_midplatform_task_manager_foundation_handoff_freeze_authorization_grant_request_record_dryrun_v1.py",
    "tools/evaluation/midplatform/verify_midplatform_task_manager_foundation_handoff_freeze_authorization_grant_request_record_dryrun_v1.py",
    "capabilities/midplatform/task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_planning_v1.py",
    "tools/evaluation/midplatform/verify_midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_planning_v1.py",
)

GRANT_OWNER_APPROVAL_REQUEST_RECORD_APPROVAL_CLOSURE_DRYRUN_STAGE_TERM_OVERRIDES: Tuple[Dict[str, str], ...] = (
    {
        "base_term": "freeze_authorization_grant_request_record_dryrun",
        "stage_term": "freeze_authorization_grant_owner_approval_request_record_approval_closure_dryrun",
    },
    {
        "base_term": "request_record_plan_integrity_ok",
        "stage_term": "record_approval_closure_plan_integrity_ok",
    },
    {
        "base_term": "request_record_candidate_preserved",
        "stage_term": "record_candidate_closure_preserved",
    },
    {
        "base_term": "owner_approval_binding_candidate_preserved",
        "stage_term": "approval_candidate_closure_preserved",
    },
    {
        "base_term": "request_record_dryrun_only",
        "stage_term": "record_approval_closure_dryrun_only",
    },
    {
        "base_term": "prior_request_record_planning_go",
        "stage_term": "prior_record_approval_closure_planning_go",
    },
    {
        "base_term": "request-record-dryrun-scope",
        "stage_term": "record-approval-closure-dryrun-scope",
    },
    {
        "base_term": "request-record-planning-scope",
        "stage_term": "record-approval-closure-planning-scope",
    },
    {
        "base_term": "evidence_binding_candidate_preserved",
        "stage_term": "evidence_binding_closure_preserved",
    },
    {
        "base_term": "request_record_schema_candidate_preserved",
        "stage_term": "protocol_reference_preserved",
    },
)

GRANT_OWNER_APPROVAL_REQUEST_RECORD_APPROVAL_CLOSURE_DRYRUN_STAGE_ADDITIONS: Tuple[str, ...] = (
    "prior_record_approval_closure_planning_go",
    "lightweight_compliance_dryrun_only",
    "candidate_validation_ok",
    "matrix_validation_ok",
    "traceability_reference_validation_ok",
    "absence_validation_ok",
    "boundary_validation_ok",
    "shared_protocol_system_revalidation",
    "l1_input_output_protocol_revalidation",
    "file_size_governance_review_ok",
    "file_size_governance_review_exists",
)

GRANT_OWNER_APPROVAL_REQUEST_RECORD_APPROVAL_CLOSURE_POST_REVIEW_WHITELIST_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_dryrun_v1.py",
    "tools/evaluation/midplatform/run_midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_dryrun_v1.py",
    "tools/evaluation/midplatform/verify_midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_dryrun_v1.py",
)

GRANT_OWNER_APPROVAL_REQUEST_RECORD_APPROVAL_CLOSURE_POST_REVIEW_STAGE_TERM_OVERRIDES: Tuple[Dict[str, str], ...] = (
    {
        "base_term": "freeze_authorization_grant_owner_approval_request_record_approval_closure_dryrun",
        "stage_term": "freeze_authorization_grant_owner_approval_request_record_approval_closure_post_dryrun_review",
    },
    {
        "base_term": "record_approval_closure_plan_integrity_ok",
        "stage_term": "dryrun_result_accepted",
    },
    {
        "base_term": "candidate_validation_ok",
        "stage_term": "candidate_review_ok",
    },
    {
        "base_term": "absence_validation_ok",
        "stage_term": "absence_review_ok",
    },
    {
        "base_term": "boundary_validation_ok",
        "stage_term": "boundary_review_ok",
    },
    {
        "base_term": "traceability_reference_validation_ok",
        "stage_term": "traceability_reference_review_ok",
    },
    {
        "base_term": "prior_record_approval_closure_planning_go",
        "stage_term": "prior_record_approval_closure_dryrun_go",
    },
    {
        "base_term": "record-approval-closure-dryrun-scope",
        "stage_term": "record-approval-closure-post-review-scope",
    },
    {
        "base_term": "lightweight_compliance_dryrun_only",
        "stage_term": "post_review_only",
    },
)

GRANT_OWNER_APPROVAL_REQUEST_RECORD_APPROVAL_CLOSURE_POST_REVIEW_STAGE_ADDITIONS: Tuple[str, ...] = (
    "prior_record_approval_closure_dryrun_go",
    "dryrun_result_accepted",
    "candidate_review_ok",
    "absence_review_ok",
    "boundary_review_ok",
    "traceability_reference_review_ok",
    "post_review_only",
    "lightweight_compliance_post_review_only",
    "final_gate_planning_readiness",
    "file_size_governance_review_ok",
    "file_size_governance_review_exists",
)

GRANT_OWNER_APPROVAL_REQUEST_POST_REVIEW_STAGE_ADDITIONS: Tuple[str, ...] = (
    "prior_owner_approval_request_dryrun_go",
    "owner_approval_request_dryrun_result_accepted",
    "approval_request_candidate_review_ok",
    "output_candidate_review_ok",
    "input_output_traceability_review_ok",
    "protocol_traceability_review_ok",
    "protocol_reference_review_ok",
    "error_namespace_review_ok",
    "whitebox_candidate_ref_review_ok",
    "validate_once_per_module_rule_review_ok",
    "separation_rule_review_ok",
    "owner_operator_notification_candidate_only",
    "rejection_reference_candidate_only",
    "expiry_reference_candidate_only",
    "revocation_reference_candidate_only",
    "input_output_registry_patch_ref",
    "traceability_rule_ref",
    "validate_once_per_module_rule_ref",
    "first_protocol_validation_confirmed",
    "subsequent_failures_default_to_module_local_proc",
    "next_phase_readiness_ok",
)

GRANT_POST_REVIEW_STAGE_TERM_OVERRIDES: Tuple[Dict[str, str], ...] = (
    {"base_term": "freeze_authorization_post_dryrun_review", "stage_term": "freeze_authorization_grant_post_dryrun_review"},
    {"base_term": "freeze_authorization_dryrun_result_accepted", "stage_term": "grant_dryrun_result_accepted"},
    {"base_term": "freeze_authorization_chain_evidence_accepted", "stage_term": "grant_chain_evidence_accepted"},
    {"base_term": "freeze_authorization_candidate", "stage_term": "grant_candidate"},
    {"base_term": "grant_planning_ready", "stage_term": "next_planning_ready"},
    {"base_term": "request_absence_review+grant_absence_review", "stage_term": "grant_absence_review"},
    {"base_term": "freeze_state_absence_review", "stage_term": "grant_state_absence_review"},
    {"base_term": "grant_planning_readiness", "stage_term": "next_planning_readiness"},
)
GRANT_POST_REVIEW_STAGE_ADDITIONS: Tuple[str, ...] = (
    "grant_absence_confirmed",
    "grant_token_absent",
    "grant_record_absent",
    "owner_approval_record_absent",
    "template_lineage_review",
    "template_lineage_ok",
    "full_repo_scan_absent",
)


def base_template_files_exist(repo_root: Path, template_files: Tuple[str, ...]) -> bool:
    return all((repo_root / rel).is_file() for rel in template_files)


def build_template_lineage(
    *,
    base_phase: str,
    base_capability: str,
    base_runner: str,
    base_verifier: str,
    base_go_no_go_pack: str,
    stage_phase: str,
    stage_term_overrides: Tuple[Dict[str, str], ...],
    stage_additions: Tuple[str, ...] = (),
    template_files: Tuple[str, ...],
    repo_root: Path,
    upstream_review_phase: Optional[str] = None,
) -> Dict[str, Any]:
    files_exist = base_template_files_exist(repo_root, template_files)
    family_match = TEMPLATE_FAMILY == "Task Manager Foundation Handoff Freeze Authorization"
    stage_overridden = len(stage_term_overrides) > 0
    return {
        "template_family": TEMPLATE_FAMILY,
        "base_phase": base_phase,
        "base_capability": base_capability,
        "base_runner": base_runner,
        "base_verifier": base_verifier,
        "base_go_no_go_pack": base_go_no_go_pack,
        "stage_phase": stage_phase,
        "reuse_mode": REUSE_MODE,
        "full_repo_scan_allowed": False,
        "base_template_files_exist": files_exist,
        "base_template_family_match": family_match,
        "stage_specific_terms_overridden": stage_overridden,
        "stage_term_overrides": list(stage_term_overrides),
        "stage_additions": list(stage_additions),
        "upstream_review_phase": upstream_review_phase,
        "core_go_no_go_schema_preserved": True,
        "template_lineage_ok": files_exist and family_match and stage_overridden,
    }


def build_core_go_no_go_summary_fields(
    *,
    go_conditions: Dict[str, bool],
    forbidden_runtime_flags: Tuple[str, ...],
    chain_trace_nodes: Tuple[str, ...],
    go_no_go_decision: str,
    final_decision: str,
    next_phase: str,
    template_lineage: Dict[str, Any],
) -> Dict[str, Any]:
    return {
        "go_conditions": go_conditions,
        "forbidden_runtime_flags": list(forbidden_runtime_flags),
        "chain_trace_nodes": list(chain_trace_nodes),
        "go_no_go_decision": go_no_go_decision,
        "final_decision": final_decision,
        "next_phase": next_phase,
        "recommended_next_phase": next_phase,
        "template_lineage": template_lineage,
        "template_lineage_ok": template_lineage.get("template_lineage_ok") is True,
        "base_template_files_exist": template_lineage.get("base_template_files_exist") is True,
        "full_repo_scan_allowed": False,
        "full_repo_scan_absent": template_lineage.get("full_repo_scan_allowed") is False,
        "core_go_no_go_schema_preserved": True,
        "stage_specific_terms_overridden": template_lineage.get("stage_specific_terms_overridden") is True,
    }


def validate_core_go_no_go_schema(summary: Dict[str, Any], verifier_report: Dict[str, Any]) -> bool:
    summary_field_keys = tuple(
        key for key in CORE_GO_NO_GO_SCHEMA_KEYS
        if key not in ("passed_checks", "failed_checks", "blocker_count", "verifier", "summary")
    )
    summary_ok = all(key in summary for key in summary_field_keys)
    verifier_ok = all(key in verifier_report for key in ("passed_checks", "failed_checks", "blocker_count", "verifier", "final_decision"))
    lineage = summary.get("template_lineage") or {}
    lineage_ok = (
        summary.get("template_lineage_ok") is True
        and summary.get("base_template_files_exist") is True
        and summary.get("full_repo_scan_absent") is True
        and summary.get("core_go_no_go_schema_preserved") is True
        and summary.get("stage_specific_terms_overridden") is True
        and lineage.get("reuse_mode") == REUSE_MODE
        and lineage.get("full_repo_scan_allowed") is False
    )
    return summary_ok and verifier_ok and lineage_ok
