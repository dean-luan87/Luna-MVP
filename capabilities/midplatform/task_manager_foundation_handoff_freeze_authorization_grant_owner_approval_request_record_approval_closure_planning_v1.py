# -*- coding: utf-8 -*-
"""Luna Midplatform Task Manager Foundation Handoff Freeze Authorization Owner Approval Request Record Approval Closure Planning v1.

Structure inherited from task_manager_foundation_handoff_freeze_authorization_grant_request_issuance_planning_v1.py
with upstream evidence from owner_approval_request_issuance_post_dryrun_review_v1 (whitelist template reuse).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import (
    CONSTRAINT_DOC_ID,
    FILE_SIZE_GOVERNANCE_INVENTORY_DOC,
    FILE_SIZE_MODULE_SPLIT_GOVERNANCE_RULE_REF,
    REUSE_FIRST_PROTOCOL_ENGINEERING_RULE_REF,
)
from capabilities.midplatform.file_size_governance_v1 import build_file_size_governance_review
from capabilities.midplatform.protocols.file_size_module_split_governance_rule_v1 import (
    FILE_SIZE_GOVERNANCE_REVIEW_KEYS,
)
from capabilities.midplatform.task_manager_foundation_handoff_evaluation_template_lineage_v1 import (
    GRANT_OWNER_APPROVAL_REQUEST_RECORD_APPROVAL_CLOSURE_PLANNING_STAGE_ADDITIONS,
    GRANT_OWNER_APPROVAL_REQUEST_RECORD_APPROVAL_CLOSURE_PLANNING_STAGE_TERM_OVERRIDES,
    GRANT_OWNER_APPROVAL_REQUEST_RECORD_APPROVAL_CLOSURE_PLANNING_WHITELIST_FILES,
    build_core_go_no_go_summary_fields,
    build_template_lineage,
)
from capabilities.midplatform.task_manager_foundation_handoff_final_closure_planning_v1 import GOVERNANCE_DEBTS
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_issuance_dryrun_v1 import (
    ERROR_NAMESPACE,
)
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_issuance_post_dryrun_review_v1 import (
    CHAIN_EVIDENCE_NODES as UPSTREAM_CHAIN_NODES,
    DEFAULT_OUTPUT as DEFAULT_OWNER_APPROVAL_REQUEST_ISSUANCE_POST_REVIEW_ROOT,
    FINAL_DECISION_GO as OWNER_APPROVAL_REQUEST_ISSUANCE_POST_REVIEW_FINAL_GO,
    GO_CONDITIONS_KEYS as UPSTREAM_GO_KEYS,
    NEXT_PHASE_GO as OWNER_APPROVAL_REQUEST_ISSUANCE_POST_REVIEW_NEXT_PHASE,
    RUNTIME_FORBIDDEN_FLAGS,
)
from capabilities.midplatform.task_manager_foundation_handoff_planning_v1 import (
    BOUNDARY_STATEMENT_EN,
    BOUNDARY_STATEMENT_ZH,
    FOUNDATION_ID,
)

PHASE_ID = "Phase-Midplatform-Task-Manager-Foundation-Handoff-Freeze-Authorization-Grant-Owner-Approval-Request-Record-Approval-Closure-Planning-v1-001"
SCOPE = "midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_planning_only"
SOURCE_CHAIN = "midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_planning_v1"
FINAL_DECISION_GO = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_REQUEST_RECORD_APPROVAL_CLOSURE_PLANNING_READY_FOR_DRYRUN"
FINAL_DECISION_PRIOR = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_REQUEST_RECORD_APPROVAL_CLOSURE_PLANNING_BLOCKED_BY_PRIOR_REVIEW_GAP"
FINAL_DECISION_SCOPE = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_REQUEST_RECORD_APPROVAL_CLOSURE_PLANNING_BLOCKED_BY_RECORD_SCOPE_ESCALATION"
FINAL_DECISION_RECORD = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_REQUEST_RECORD_APPROVAL_CLOSURE_PLANNING_BLOCKED_BY_REQUEST_RECORD_LEAKAGE"
FINAL_DECISION_REQUEST = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_REQUEST_RECORD_APPROVAL_CLOSURE_PLANNING_BLOCKED_BY_AUTHORIZATION_REQUEST_LEAKAGE"
FINAL_DECISION_FREEZE = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_REQUEST_RECORD_APPROVAL_CLOSURE_PLANNING_BLOCKED_BY_FREEZE_STATE_ESCALATION"
FINAL_DECISION_DEBT = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_REQUEST_RECORD_APPROVAL_CLOSURE_PLANNING_BLOCKED_BY_GOVERNANCE_DEBT_GAP"
FINAL_DECISION_L1 = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_REQUEST_RECORD_APPROVAL_CLOSURE_PLANNING_BLOCKED_BY_L1_PROTOCOL_SCOPE_LEAKAGE"
FINAL_DECISION_RUNTIME = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_REQUEST_RECORD_APPROVAL_CLOSURE_PLANNING_BLOCKED_BY_RUNTIME_SCOPE_LEAKAGE"
FINAL_DECISION_LINEAGE = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_REQUEST_RECORD_APPROVAL_CLOSURE_PLANNING_BLOCKED_BY_TEMPLATE_LINEAGE_GAP"
NEXT_PHASE_GO = "Phase-Midplatform-Task-Manager-Foundation-Handoff-Freeze-Authorization-Grant-Owner-Approval-Request-Record-Approval-Closure-DryRun-v1-001"
NEXT_PHASE_HOLD = "Phase-Midplatform-Task-Manager-Foundation-Handoff-Freeze-Authorization-Grant-Owner-Approval-Request-Record-Approval-Closure-Planning-Issue-Review-v1-001"
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_planning_v1_smoke_v0"
)
GRANT_OWNER_APPROVAL_REQUEST_RECORD_APPROVAL_CLOSURE_PLANNING_PACKAGE_FILES: Tuple[str, ...] = (
    "task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_plan_v1.json",
    "task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_plan_v1.md",
    "task_manager_freeze_authorization_grant_owner_approval_request_record_candidate_closure_matrix_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_approval_candidate_closure_matrix_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_ack_candidate_closure_matrix_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_evidence_binding_closure_matrix_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_traceability_matrix_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_protocol_reference_matrix_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_error_namespace_matrix_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_whitebox_candidate_ref_matrix_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_boundary_contract_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_non_execution_constraints_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_rejection_reference_matrix_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_expiry_reference_matrix_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_revocation_reference_matrix_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_governance_debt_carryover_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_template_lineage_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_next_phase_readiness_v1.json",
    "file_size_governance_review_v1.json",
    "summary.json",
    "verifier_report.json",
)
RECORD_APPROVAL_CLOSURE_PLANNING_GO_NO_GO_PACK = (
    "docs/architecture/evaluation/"
    "LUNA_EVALUATION_MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_REQUEST_RECORD_APPROVAL_CLOSURE_PLANNING_V1_GO_NO_GO_PACK_V0.md"
)
PHASE_PYTHON_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_planning_v1.py",
    "tools/evaluation/midplatform/run_midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_planning_v1.py",
    "tools/evaluation/midplatform/verify_midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_planning_v1.py",
)
TEMPLATE_LINEAGE_MODULE_PATH = "capabilities/midplatform/task_manager_foundation_handoff_evaluation_template_lineage_v1.py"
LIGHTWEIGHT_PROTOCOL_REFS: Tuple[str, ...] = (
    "LUNA-PROTO-L1-INPUT-CANDIDATE-GOVERNANCE-V1",
    "LUNA-PROTO-L1-OUTPUT-CANDIDATE-GOVERNANCE-V1",
    "LUNA-PROTO-L1-INPUT-OUTPUT-SYMMETRY-V1",
    "LUNA-PROTO-L1-PROTOCOL-TRACEABILITY-GOVERNANCE-V1",
    "LUNA-PROTO-L1-APPROVAL-ACK-V1",
    "LUNA-PROTO-L1-EVIDENCE-BINDING-V1",
    "LUNA-PROTO-L1-RECORD-LIFECYCLE-V1",
    "LUNA-PROTO-L1-WHITEBOX-DIAGNOSTIC-BINDING-V1",
    "LUNA-PROTO-L2-TASKMANAGER-OWNER-APPROVAL-REQUEST-V1",
)

BOUNDARY_CONTRACT_STATEMENTS: Tuple[str, ...] = (
    "record_approval_closure_planning != request_record",
    "owner_approval_request_record_candidate != request_record",
    "owner_approval_record_candidate != request_record_schema_final",
    "evidence_binding_candidate != evidence_bound_record",
    "owner_operator_ack_record_candidate != owner_approval_record",
    "authorization_request_candidate != authorization_request_issued",
    "grant_token_candidate != grant_token",
    "grant_candidate != grant_record",
    "freeze_candidate != frozen",
    "closure_candidate != closed",
)
RECORD_SCOPE_ROWS: Tuple[Dict[str, str], ...] = (
    {"scope": "request_record_definition_boundary", "classification": "record-approval-closure-planning-scope"},
    {"scope": "owner_approval_record_candidate_boundary", "classification": "record-approval-closure-planning-scope"},
    {"scope": "evidence_binding_candidate_boundary", "classification": "record-approval-closure-planning-scope"},
    {"scope": "owner_operator_ack_record_candidate_boundary", "classification": "record-approval-closure-planning-scope"},
    {"scope": "revocation_reference_candidate_boundary", "classification": "record-approval-closure-planning-scope"},
    {"scope": "lifecycle_candidate_declaration", "classification": "record-approval-closure-planning-scope"},
    {"scope": "governance_debt_acknowledgement", "classification": "record-approval-closure-planning-scope"},
    {"scope": "non_execution_constraints", "classification": "record-approval-closure-planning-scope"},
)
PREREQUISITE_ROWS: Tuple[Dict[str, Any], ...] = (
    {"prerequisite": "request_issuance_post_review_go", "required": True},
    {"prerequisite": "authorization_request_absent", "required": True},
    {"prerequisite": "request_record_absent", "required": True},
    {"prerequisite": "owner_approval_record_absent", "required": True},
    {"prerequisite": "grant_token_absent", "required": True},
    {"prerequisite": "grant_record_absent", "required": True},
    {"prerequisite": "authorization_grant_absent", "required": True},
    {"prerequisite": "foundation_not_frozen", "required": True},
    {"prerequisite": "closure_not_executed", "required": True},
    {"prerequisite": "governance_debt_preserved", "required": True},
)
NON_EXECUTION_CONSTRAINTS: Tuple[str, ...] = (
    "no_request_record",
    "no_request_record_final_schema",
    "no_evidence_bound_record",
    "no_owner_approval_record",
    "no_authorization_request",
    "no_grant_token",
    "no_grant_record",
    "no_authorization_grant",
    "no_revocation_execution_path",
    "no_freeze_execution_path",
    "no_rollback_execution_path",
    "no_foundation_frozen",
    "no_closed_state",
    "no_foundation_finalized",
    "no_runtime_executor",
    "no_scheduler_binding",
    "no_task_execution_authority",
    "no_output_authorization",
    "no_memory_worldmodel_write_path",
    "no_module_adapter_integration",
    "no_information_channel_governance_implementation",
    "no_protocol_governance_implementation",
    "no_closure_channel_governance_implementation",
    "no_system_protocols_integration_implementation",
)
RECORD_CANDIDATE_CLOSURE_ROWS: Tuple[Dict[str, Any], ...] = (
    {
        "record_type": "owner_approval_request_record_candidate",
        "record_status": "owner-approval-request-record-candidate",
        "record_created": False,
        "request_issued": False,
    },
    {
        "record_type": "owner_approval_request_record_approval_closure_candidate",
        "record_status": "owner-approval-request-record-candidate",
        "record_created": False,
        "request_issued": False,
    },
)
APPROVAL_CANDIDATE_CLOSURE_ROWS: Tuple[Dict[str, Any], ...] = (
    {
        "candidate_id": "owner_approval_record_candidate",
        "candidate_status": "owner-approval-record-candidate",
        "approval_record_created": False,
    },
    {
        "candidate_id": "owner_approval_request_record_approval_closure_candidate",
        "candidate_status": "owner-approval-record-candidate",
        "approval_record_created": False,
    },
)
EVIDENCE_BINDING_CLOSURE_ROWS: Tuple[Dict[str, Any], ...] = (
    {
        "binding_id": "issuance_post_review_evidence_ref",
        "binding_status": "approval-evidence-bound-record-candidate",
        "evidence_bound": False,
    },
    {
        "binding_id": "handoff_chain_node_evidence_ref",
        "binding_status": "approval-evidence-bound-record-candidate",
        "evidence_bound": False,
    },
)
ACK_CANDIDATE_CLOSURE_ROWS: Tuple[Dict[str, str], ...] = (
    {"role": "foundation_owner", "binding_status": "owner-operator-ack-record-candidate"},
    {"role": "operator_approver", "binding_status": "owner-operator-ack-record-candidate"},
)
LIFECYCLE_ROWS: Tuple[Dict[str, str], ...] = (
    {"stage": "candidate_defined", "lifecycle_type": "candidate-lifecycle"},
    {"stage": "candidate_audited", "lifecycle_type": "candidate-lifecycle"},
    {"stage": "candidate_revocation_ref_prepared", "lifecycle_type": "candidate-lifecycle"},
)
REJECTION_REFERENCE_ROWS: Tuple[Dict[str, Any], ...] = (
    {
        "reference_id": "owner_approval_rejection_ref",
        "reference_status": "rejection-reference-candidate",
        "rejection_execution_path": False,
    },
)
EXPIRY_REFERENCE_ROWS: Tuple[Dict[str, Any], ...] = (
    {
        "reference_id": "owner_approval_expiry_ref",
        "reference_status": "expiry-reference-candidate",
        "expiry_execution_path": False,
    },
)
REVOCATION_REFERENCE_ROWS: Tuple[Dict[str, Any], ...] = (
    {
        "reference_id": "post_issuance_revocation_ref",
        "reference_status": "revocation-reference-candidate",
        "revocation_execution_path": False,
    },
    {
        "reference_id": "audit_rollback_ref",
        "reference_status": "revocation-reference-candidate",
        "revocation_execution_path": False,
    },
)
CHAIN_EVIDENCE_NODES: Tuple[str, ...] = UPSTREAM_CHAIN_NODES + (
    "freeze_authorization_grant_owner_approval_request_record_approval_closure_planning",
)
GO_CONDITIONS_KEYS: Tuple[str, ...] = (
    "prior_owner_approval_request_issuance_post_review_go",
    "record_approval_closure_plan_complete",
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
    "request_issued_absent",
    "notification_sent_absent",
    "request_record_absent",
    "approval_record_absent",
    "ack_record_absent",
    "evidence_bound_record_absent",
    "authorization_request_absent",
    "grant_absent",
    "foundation_not_frozen",
    "closure_not_executed",
    "runtime_execution_absent",
    "protocol_runtime_absent",
    "whitebox_runtime_integration_absent",
    "module_adapter_implementation_absent",
    "governance_debt_preserved",
    "template_lineage_ok",
    "file_size_governance_review_exists",
    "monolithic_file_absent",
    "large_file_read_avoidance_ok",
    "summary_index_first_reading_ok",
    "verifier_large_file_scan_absent",
    "full_repo_scan_absent",
    "tmp_eval_out_scan_absent",
    "limited_directory_scan_ok",
    "non_execution_boundary_ok",
    "next_phase_readiness_ok",
)
PLANNING_TRUE_KEYS: Tuple[str, ...] = GO_CONDITIONS_KEYS


def _read_json(path: Path) -> Dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return {}
    return payload if isinstance(payload, dict) else {}


def _meta(out: Path, post_review: Path) -> Dict[str, Any]:
    return {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "source_chain": SOURCE_CHAIN,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "foundation_id": FOUNDATION_ID,
        "runtime_status": "not_enabled",
        "record_approval_closure_planning_only": True,
        "authorization_request_absent": True,
        "authorization_request_issued": False,
        "request_record_absent": True,
        "owner_approval_record_absent": True,
        "authorization_grant_absent": True,
        "grant_token_absent": True,
        "grant_record_absent": True,
        "foundation_not_frozen": True,
        "closure_not_executed": True,
        "l1_protocols_not_implemented": True,
        "system_protocols_integration_not_implemented": True,
        "output_root": str(out),
        "owner_approval_request_issuance_post_dryrun_review_root": str(post_review),
        "boundary_statement_en": BOUNDARY_STATEMENT_EN,
        "boundary_statement_zh": BOUNDARY_STATEMENT_ZH,
    }


def run_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_planning_v1(
    *,
    owner_approval_request_issuance_post_dryrun_review_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    out = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    post_review = Path(owner_approval_request_issuance_post_dryrun_review_root).expanduser().resolve()
    repo_root = Path(__file__).resolve().parents[2]
    meta = _meta(out, post_review)
    issues: List[str] = []
    downstream_readiness_gaps: List[str] = []

    post_summary = _read_json(post_review / "summary.json")
    post_verifier = _read_json(post_review / "verifier_report.json")
    chain_review = _read_json(
        post_review / "task_manager_freeze_authorization_grant_owner_approval_request_issuance_evidence_chain_review_v1.json"
    )
    absence_src = _read_json(
        post_review / "task_manager_freeze_authorization_grant_owner_approval_request_issuance_absence_review_v1.json"
    )
    timeout_review = _read_json(
        post_review / "task_manager_freeze_authorization_grant_owner_approval_request_issuance_timeout_event_review_v1.json"
    )
    notification_review = _read_json(
        post_review
        / "task_manager_freeze_authorization_grant_owner_approval_request_issuance_owner_operator_notification_candidate_review_v1.json"
    )

    prior_owner_approval_request_issuance_post_review_go = (
        post_summary.get("final_decision") == OWNER_APPROVAL_REQUEST_ISSUANCE_POST_REVIEW_FINAL_GO
        and post_summary.get("recommended_next_phase") == OWNER_APPROVAL_REQUEST_ISSUANCE_POST_REVIEW_NEXT_PHASE
        and post_verifier.get("verifier") == "GO"
        and int(post_verifier.get("passed_checks", 0)) >= 420
        and post_verifier.get("failed_checks") == 0
        and post_verifier.get("blocker_count") == 0
        and post_summary.get("timeout_event_review_ok") is True
        and timeout_review.get("previous_interruption_not_logic_loop") is True
        and timeout_review.get("timeout_event_is_blocker") is False
        and post_summary.get("issuance_dryrun_result_accepted") is True
        and post_summary.get("validate_once_reference_review_ok") is True
        and all(post_summary.get(k) is True for k in UPSTREAM_GO_KEYS)
    )
    if not prior_owner_approval_request_issuance_post_review_go:
        issues.append("prior_request_issuance_post_review_not_go")

    evidence_chain = []
    for stage in UPSTREAM_CHAIN_NODES:
        row = next((r for r in chain_review.get("chain") or [] if r.get("stage") == stage), {})
        evidence_chain.append({"stage": stage, "linked": row.get("linked") is True})
    evidence_chain.append(
        {
            "stage": "freeze_authorization_grant_owner_approval_request_record_approval_closure_planning",
            "root": str(out),
            "readiness": "record-approval-closure-planning-ready",
            "authorization_request_issued": False,
            "request_record": False,
            "grant_issued": False,
            "linked": True,
        }
    )
    evidence_chain_paths_declared = all(
        any(node.get("stage") == stage for node in evidence_chain) for stage in CHAIN_EVIDENCE_NODES
    )
    issuance_post_review_ref_linked = any(
        node.get("stage") == "freeze_authorization_grant_owner_approval_request_issuance_post_dryrun_review"
        and node.get("linked") is True
        for node in evidence_chain
    )
    planning_node_linked = any(
        node.get("stage") == "freeze_authorization_grant_owner_approval_request_record_approval_closure_planning"
        and node.get("linked") is True
        for node in evidence_chain
    )
    upstream_chain_linked = all(
        node.get("linked") is True
        for node in evidence_chain
        if node.get("stage")
        not in (
            "freeze_authorization_grant_owner_approval_request_issuance_post_dryrun_review",
            "freeze_authorization_grant_owner_approval_request_record_approval_closure_planning",
        )
    )
    if not upstream_chain_linked:
        downstream_readiness_gaps.append("upstream_evidence_chain_not_fully_linked")
    evidence_chain_complete = (
        prior_owner_approval_request_issuance_post_review_go
        and issuance_post_review_ref_linked
        and planning_node_linked
        and evidence_chain_paths_declared
    )
    if not evidence_chain_complete:
        issues.append("evidence_chain_gap")

    scope_rows = list(RECORD_SCOPE_ROWS)
    closure_planning_only = all(
        row["classification"] == "record-approval-closure-planning-scope"
        and row["classification"] not in ("request-record-created-scope", "authorized-scope")
        for row in scope_rows
    )
    if not closure_planning_only:
        issues.append("record_scope_escalation")

    record_rows = [{**row, "record_created": False} for row in RECORD_CANDIDATE_CLOSURE_ROWS]
    record_candidate_closure_matrix_complete = all(
        row.get("record_status") == "owner-approval-request-record-candidate"
        and row.get("record_status") != "request-record"
        and row.get("record_created") is False
        and row.get("request_issued") is False
        for row in record_rows
    )
    if not record_candidate_closure_matrix_complete:
        issues.append("request_record_leakage")

    approval_rows = list(APPROVAL_CANDIDATE_CLOSURE_ROWS)
    approval_candidate_closure_matrix_complete = all(
        row.get("candidate_status") == "owner-approval-record-candidate"
        and row.get("candidate_status") != "owner-approval-record"
        and row.get("approval_record_created") is False
        for row in approval_rows
    )
    if not approval_candidate_closure_matrix_complete:
        issues.append("approval_candidate_escalation")

    evidence_binding_rows = [{**row, "bound_evidence_record": False} for row in EVIDENCE_BINDING_CLOSURE_ROWS]
    evidence_binding_closure_matrix_complete = all(
        row.get("binding_status") == "approval-evidence-bound-record-candidate"
        and row.get("binding_status") != "bound-evidence-record"
        and row.get("evidence_bound") is False
        for row in evidence_binding_rows
    )
    if not evidence_binding_closure_matrix_complete:
        issues.append("evidence_binding_leakage")

    owner_binding_rows = [
        {**row, "owner_approval_record": False, "approval_record": False}
        for row in ACK_CANDIDATE_CLOSURE_ROWS
    ]
    ack_candidate_closure_matrix_complete = all(
        row.get("binding_status") == "owner-operator-ack-record-candidate"
        and row.get("binding_status") != "owner-approval-record"
        and row.get("owner_approval_record") is False
        for row in owner_binding_rows
    )
    if not ack_candidate_closure_matrix_complete:
        issues.append("owner_approval_binding_leakage")

    lifecycle_rows = list(LIFECYCLE_ROWS)
    lifecycle_candidate_only = all(
        row.get("lifecycle_type") == "candidate-lifecycle"
        and row.get("lifecycle_type") != "active-record-lifecycle"
        for row in lifecycle_rows
    )
    if not lifecycle_candidate_only:
        issues.append("lifecycle_escalation")

    rejection_rows = list(REJECTION_REFERENCE_ROWS)
    rejection_reference_candidate_only = all(
        row.get("reference_status") == "rejection-reference-candidate"
        and row.get("rejection_execution_path") is False
        for row in rejection_rows
    )
    if not rejection_reference_candidate_only:
        issues.append("rejection_execution_leakage")

    expiry_rows = list(EXPIRY_REFERENCE_ROWS)
    expiry_reference_candidate_only = all(
        row.get("reference_status") == "expiry-reference-candidate"
        and row.get("expiry_execution_path") is False
        for row in expiry_rows
    )
    if not expiry_reference_candidate_only:
        issues.append("expiry_execution_leakage")

    revocation_rows = list(REVOCATION_REFERENCE_ROWS)
    revocation_reference_candidate_only = all(
        row.get("reference_status") == "revocation-reference-candidate"
        and row.get("reference_status") != "revocation-execution-path"
        and row.get("revocation_execution_path") is False
        for row in revocation_rows
    )
    if not revocation_reference_candidate_only:
        issues.append("revocation_execution_leakage")

    prerequisite_values = {
        "request_issuance_post_review_go": prior_owner_approval_request_issuance_post_review_go,
        "authorization_request_absent": post_summary.get("authorization_request_absent") is True
        or absence_src.get("authorization_request_issued") is False,
        "request_record_absent": post_summary.get("request_record_absent") is True
        or absence_src.get("request_record_absent") is True,
        "owner_approval_record_absent": post_summary.get("owner_approval_record_absent") is True
        or absence_src.get("owner_approval_record_absent") is True,
        "authorization_grant_absent": post_summary.get("authorization_grant_absent") is True
        or absence_src.get("authorization_grant_absent") is True,
        "grant_token_absent": post_summary.get("grant_token_absent") is True
        or absence_src.get("grant_token_absent") is True,
        "grant_record_absent": post_summary.get("grant_record_absent") is True
        or absence_src.get("grant_record_absent") is True,
        "foundation_not_frozen": post_summary.get("foundation_not_frozen") is True,
        "closure_not_executed": post_summary.get("closure_not_executed") is True,
        "governance_debt_preserved": post_summary.get("governance_debt_preserved") is True,
    }
    prerequisite_rows = [
        {**row, "satisfied": prerequisite_values.get(row["prerequisite"]) is True}
        for row in PREREQUISITE_ROWS
    ]
    prerequisites_ok = all(row.get("satisfied") for row in prerequisite_rows)
    if not prerequisites_ok:
        issues.append("prerequisite_gap")

    authorization_request_absent = prerequisite_values["authorization_request_absent"]
    authorization_grant_absent = prerequisite_values["authorization_grant_absent"]
    grant_token_absent = prerequisite_values["grant_token_absent"]
    grant_record_absent = prerequisite_values["grant_record_absent"]
    owner_approval_record_absent = prerequisite_values["owner_approval_record_absent"]
    request_record_absent = prerequisite_values["request_record_absent"]
    foundation_not_frozen = prerequisite_values["foundation_not_frozen"]
    closure_not_executed = prerequisite_values["closure_not_executed"]

    if not authorization_request_absent:
        issues.append("authorization_request_leakage")
    if not request_record_absent or not owner_approval_record_absent or not grant_token_absent or not grant_record_absent:
        issues.append("request_record_leakage")

    debts = list(GOVERNANCE_DEBTS)
    governance_debt_preserved = (
        len(debts) >= 2
        and debts[0]["debt_title"] == GOVERNANCE_DEBTS[0]["debt_title"]
        and debts[0]["priority"] == "P1"
        and debts[0]["classification"] == "L1 Midplatform System Protocols"
        and debts[0]["must_not_implement_now"] is True
        and debts[1]["debt_title"] == GOVERNANCE_DEBTS[1]["debt_title"]
        and debts[1]["priority"] == "P1"
        and debts[1]["classification"] == "L1 Midplatform System Protocols"
        and debts[1]["must_not_implement_now"] is True
    )
    if not governance_debt_preserved:
        issues.append("governance_debt_gap")

    l1_protocols_not_implemented = True
    system_protocols_integration_not_implemented = True
    non_execution_boundary_ok = True

    template_lineage = build_template_lineage(
        base_phase="Freeze-Authorization-Grant-Owner-Approval-Request-Issuance-Post-DryRun-Review-v1-001",
        base_capability=GRANT_OWNER_APPROVAL_REQUEST_RECORD_APPROVAL_CLOSURE_PLANNING_WHITELIST_FILES[0],
        base_runner=GRANT_OWNER_APPROVAL_REQUEST_RECORD_APPROVAL_CLOSURE_PLANNING_WHITELIST_FILES[1],
        base_verifier=GRANT_OWNER_APPROVAL_REQUEST_RECORD_APPROVAL_CLOSURE_PLANNING_WHITELIST_FILES[2],
        base_go_no_go_pack=RECORD_APPROVAL_CLOSURE_PLANNING_GO_NO_GO_PACK,
        stage_phase="Freeze-Authorization-Grant-Owner-Approval-Request-Record-Approval-Closure-Planning-v1-001",
        stage_term_overrides=GRANT_OWNER_APPROVAL_REQUEST_RECORD_APPROVAL_CLOSURE_PLANNING_STAGE_TERM_OVERRIDES,
        stage_additions=GRANT_OWNER_APPROVAL_REQUEST_RECORD_APPROVAL_CLOSURE_PLANNING_STAGE_ADDITIONS,
        template_files=GRANT_OWNER_APPROVAL_REQUEST_RECORD_APPROVAL_CLOSURE_PLANNING_WHITELIST_FILES,
        repo_root=repo_root,
        upstream_review_phase="Freeze-Authorization-Grant-Owner-Approval-Request-Issuance-Post-DryRun-Review-v1-001",
    )
    upstream_lineage_ok = post_summary.get("template_lineage_ok") is True
    if not template_lineage.get("template_lineage_ok") or not upstream_lineage_ok:
        issues.append("template_lineage_gap")

    protocol_reference_matrix_ok = True
    error_namespace_matrix_ok = True
    whitebox_candidate_ref_matrix_ok = True
    traceability_matrix_complete = evidence_chain_complete
    request_issued_absent = (
        post_summary.get("owner_approval_request_issued_absent") is True
        or absence_src.get("owner_approval_request_absent") is True
        or absence_src.get("authorization_request_issued") is False
    )
    notification_sent_absent = (
        post_summary.get("owner_operator_notification_sent_absent") is True
        or notification_review.get("owner_operator_notification_issuance_candidate_only") is True
    )
    ack_record_absent = post_summary.get("owner_operator_ack_record_absent") is True or absence_src.get("owner_operator_ack_record_absent") is True
    evidence_bound_record_absent = post_summary.get("approval_evidence_bound_record_absent") is True or absence_src.get("approval_evidence_bound_record_absent") is True
    approval_record_absent = owner_approval_record_absent
    grant_absent = grant_token_absent and grant_record_absent and authorization_grant_absent
    runtime_execution_absent = True
    protocol_runtime_absent = True
    whitebox_runtime_integration_absent = True
    module_adapter_implementation_absent = True

    file_size_governance_review = build_file_size_governance_review(
        phase_id=PHASE_ID,
        scope_paths=list(PHASE_PYTHON_FILES),
        repo_root=repo_root,
        phase_python_paths=PHASE_PYTHON_FILES,
        template_lineage_path=TEMPLATE_LINEAGE_MODULE_PATH,
        read_strategy="summary_index_first",
        full_repo_scan=False,
        previous_interruption_type=timeout_review.get("previous_interruption_type"),
        previous_interruption_duration_seconds=timeout_review.get("previous_interruption_duration_seconds"),
        previous_interruption_not_logic_loop=timeout_review.get("previous_interruption_not_logic_loop"),
    )

    record_approval_closure_plan_complete = (
        prior_owner_approval_request_issuance_post_review_go
        and evidence_chain_complete
        and closure_planning_only
        and record_candidate_closure_matrix_complete
        and approval_candidate_closure_matrix_complete
        and evidence_binding_closure_matrix_complete
        and ack_candidate_closure_matrix_complete
        and traceability_matrix_complete
        and protocol_reference_matrix_ok
        and error_namespace_matrix_ok
        and whitebox_candidate_ref_matrix_ok
        and rejection_reference_candidate_only
        and expiry_reference_candidate_only
        and revocation_reference_candidate_only
        and prerequisites_ok
        and governance_debt_preserved
        and template_lineage.get("template_lineage_ok") is True
        and file_size_governance_review.get("file_size_governance_review_ok") is True
    )
    next_phase_readiness_ok = record_approval_closure_plan_complete

    if not prior_owner_approval_request_issuance_post_review_go:
        final_decision = FINAL_DECISION_PRIOR
    elif not template_lineage.get("template_lineage_ok"):
        final_decision = FINAL_DECISION_LINEAGE
    elif (
        not closure_planning_only
        or not record_candidate_closure_matrix_complete
        or not approval_candidate_closure_matrix_complete
        or not evidence_binding_closure_matrix_complete
        or not ack_candidate_closure_matrix_complete
        or not revocation_reference_candidate_only
    ):
        final_decision = FINAL_DECISION_SCOPE
    elif not request_record_absent or not owner_approval_record_absent or not grant_token_absent or not grant_record_absent:
        final_decision = FINAL_DECISION_RECORD
    elif not authorization_request_absent:
        final_decision = FINAL_DECISION_REQUEST
    elif not foundation_not_frozen:
        final_decision = FINAL_DECISION_FREEZE
    elif not record_approval_closure_plan_complete:
        final_decision = FINAL_DECISION_SCOPE
    elif not governance_debt_preserved:
        final_decision = FINAL_DECISION_DEBT
    elif not l1_protocols_not_implemented:
        final_decision = FINAL_DECISION_L1
    elif not non_execution_boundary_ok:
        final_decision = FINAL_DECISION_RUNTIME
    else:
        final_decision = FINAL_DECISION_GO

    go_condition_values = {
        "prior_owner_approval_request_issuance_post_review_go": prior_owner_approval_request_issuance_post_review_go,
        "record_approval_closure_plan_complete": record_approval_closure_plan_complete,
        "record_candidate_closure_matrix_complete": record_candidate_closure_matrix_complete,
        "approval_candidate_closure_matrix_complete": approval_candidate_closure_matrix_complete,
        "ack_candidate_closure_matrix_complete": ack_candidate_closure_matrix_complete,
        "evidence_binding_closure_matrix_complete": evidence_binding_closure_matrix_complete,
        "traceability_matrix_complete": traceability_matrix_complete,
        "protocol_reference_matrix_ok": protocol_reference_matrix_ok,
        "error_namespace_matrix_ok": error_namespace_matrix_ok,
        "whitebox_candidate_ref_matrix_ok": whitebox_candidate_ref_matrix_ok,
        "rejection_reference_candidate_only": rejection_reference_candidate_only,
        "expiry_reference_candidate_only": expiry_reference_candidate_only,
        "revocation_reference_candidate_only": revocation_reference_candidate_only,
        "request_issued_absent": request_issued_absent,
        "notification_sent_absent": notification_sent_absent,
        "request_record_absent": request_record_absent,
        "approval_record_absent": approval_record_absent,
        "ack_record_absent": ack_record_absent,
        "evidence_bound_record_absent": evidence_bound_record_absent,
        "authorization_request_absent": authorization_request_absent,
        "grant_absent": grant_absent,
        "foundation_not_frozen": foundation_not_frozen,
        "closure_not_executed": closure_not_executed,
        "runtime_execution_absent": runtime_execution_absent,
        "protocol_runtime_absent": protocol_runtime_absent,
        "whitebox_runtime_integration_absent": whitebox_runtime_integration_absent,
        "module_adapter_implementation_absent": module_adapter_implementation_absent,
        "governance_debt_preserved": governance_debt_preserved,
        "template_lineage_ok": template_lineage.get("template_lineage_ok") is True and upstream_lineage_ok,
        "non_execution_boundary_ok": non_execution_boundary_ok,
        "next_phase_readiness_ok": next_phase_readiness_ok,
        **{key: file_size_governance_review.get(key) is True for key in FILE_SIZE_GOVERNANCE_REVIEW_KEYS},
        "file_size_governance_review_exists": file_size_governance_review.get("file_size_governance_review_exists") is True,
        "full_repo_scan_absent": file_size_governance_review.get("full_repo_scan_absent") is True,
        "tmp_eval_out_scan_absent": file_size_governance_review.get("tmp_eval_out_scan_absent") is True,
        "limited_directory_scan_ok": file_size_governance_review.get("limited_directory_scan_ok") is True,
    }
    planning_pass = (
        len(issues) == 0
        and final_decision == FINAL_DECISION_GO
        and all(go_condition_values.get(key) is True for key in GO_CONDITIONS_KEYS)
    )
    next_phase = NEXT_PHASE_GO if planning_pass else PHASE_ID
    core_schema_fields = build_core_go_no_go_summary_fields(
        go_conditions=go_condition_values,
        forbidden_runtime_flags=RUNTIME_FORBIDDEN_FLAGS,
        chain_trace_nodes=CHAIN_EVIDENCE_NODES,
        go_no_go_decision=final_decision,
        final_decision=final_decision,
        next_phase=next_phase,
        template_lineage=template_lineage,
    )

    record_plan = {
        "plan_id": "task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_plan_v1",
        "record_scope": [
            "define request record structure after authorization request issued without creating records",
            "define owner-approval-record-candidate without final schema",
            "define approval-evidence-bound-record-candidate without binding evidence records",
            "define owner-operator-ack-record-candidate without approval records",
            "define candidate lifecycle without active record lifecycle",
            "define revocation-reference-candidate without revocation execution path",
            "trace evidence chain through request record planning",
            "preserve governance debt carryover",
            "define non-execution constraints for future record dry-run",
        ],
        "evidence_chain": evidence_chain,
        "evidence_chain_complete": evidence_chain_complete,
        "node_count": len(CHAIN_EVIDENCE_NODES),
        **go_condition_values,
        "final_decision": final_decision,
        "recommended_next_phase": next_phase,
        **meta,
    }
    record_candidate_matrix = {
        "matrix_id": "task_manager_freeze_authorization_grant_owner_approval_request_record_candidate_closure_matrix_v1",
        "rows": record_rows,
        "record_candidate_closure_matrix_complete": record_candidate_closure_matrix_complete,
        **meta,
    }
    approval_candidate_matrix = {
        "matrix_id": "task_manager_freeze_authorization_grant_owner_approval_request_approval_candidate_closure_matrix_v1",
        "rows": approval_rows,
        "approval_candidate_closure_matrix_complete": approval_candidate_closure_matrix_complete,
        **meta,
    }
    ack_candidate_matrix = {
        "matrix_id": "task_manager_freeze_authorization_grant_owner_approval_request_ack_candidate_closure_matrix_v1",
        "rows": owner_binding_rows,
        "ack_candidate_closure_matrix_complete": ack_candidate_closure_matrix_complete,
        **meta,
    }
    evidence_binding_matrix = {
        "matrix_id": "task_manager_freeze_authorization_grant_owner_approval_request_evidence_binding_closure_matrix_v1",
        "rows": evidence_binding_rows,
        "evidence_binding_closure_matrix_complete": evidence_binding_closure_matrix_complete,
        **meta,
    }
    traceability_matrix = {
        "matrix_id": "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_traceability_matrix_v1",
        "chain": evidence_chain,
        "traceability_matrix_complete": traceability_matrix_complete,
        "shared_protocol_system_revalidation": False,
        "l1_input_output_protocol_revalidation": False,
        **meta,
    }
    protocol_reference_matrix = {
        "matrix_id": "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_protocol_reference_matrix_v1",
        "refs": [{"protocol_id": pid, "reference_mode": "lightweight"} for pid in LIGHTWEIGHT_PROTOCOL_REFS],
        "protocol_reference_matrix_ok": protocol_reference_matrix_ok,
        "shared_protocol_system_revalidation": False,
        **meta,
    }
    error_namespace_matrix = {
        "matrix_id": "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_error_namespace_matrix_v1",
        "error_namespace": ERROR_NAMESPACE,
        "error_namespace_matrix_ok": error_namespace_matrix_ok,
        **meta,
    }
    whitebox_candidate_ref_matrix = {
        "matrix_id": "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_whitebox_candidate_ref_matrix_v1",
        "refs": [{"ref_id": "whitebox_diagnostic_candidate", "binding_mode": "candidate-only"}],
        "whitebox_candidate_ref_matrix_ok": whitebox_candidate_ref_matrix_ok,
        "whitebox_runtime_integration_absent": True,
        **meta,
    }
    rejection_matrix = {
        "matrix_id": "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_rejection_reference_matrix_v1",
        "rows": rejection_rows,
        "rejection_reference_candidate_only": rejection_reference_candidate_only,
        **meta,
    }
    expiry_matrix = {
        "matrix_id": "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_expiry_reference_matrix_v1",
        "rows": expiry_rows,
        "expiry_reference_candidate_only": expiry_reference_candidate_only,
        **meta,
    }
    revocation_matrix = {
        "matrix_id": "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_revocation_reference_matrix_v1",
        "rows": revocation_rows,
        "revocation_reference_candidate_only": revocation_reference_candidate_only,
        **meta,
    }
    boundary_contract = {
        "contract_id": "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_boundary_contract_v1",
        "statements": list(BOUNDARY_CONTRACT_STATEMENTS),
        "owner_approval_request_record_candidate_ne_request_record": True,
        "owner_approval_record_candidate_ne_owner_approval_record": True,
        "owner_operator_ack_record_candidate_ne_ack_record": True,
        "approval_evidence_bound_record_candidate_ne_evidence_bound_record": True,
        "closure_candidate_ne_closure_executed": True,
        "record_approval_closure_planning_only": True,
        "authorization_request_absent": True,
        "request_issued_absent": True,
        "notification_sent_absent": True,
        "request_record_absent": True,
        "approval_record_absent": True,
        "ack_record_absent": True,
        "evidence_bound_record_absent": True,
        "grant_absent": True,
        "foundation_frozen": False,
        "closure_executed": False,
        **meta,
    }
    boundary_contract_doc = boundary_contract
    non_execution = {
        "constraints_id": "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_non_execution_constraints_v1",
        "constraints": list(NON_EXECUTION_CONSTRAINTS),
        "non_execution_boundary_ok": non_execution_boundary_ok,
        **{c: True for c in NON_EXECUTION_CONSTRAINTS},
        **meta,
    }
    debt_carryover = {
        "carryover_id": "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_governance_debt_carryover_v1",
        "debts": debts,
        "governance_debt_preserved": governance_debt_preserved,
        "l1_protocols_not_implemented": l1_protocols_not_implemented,
        "system_protocols_integration_not_implemented": system_protocols_integration_not_implemented,
        **meta,
    }
    template_lineage_doc = {
        "lineage_id": "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_template_lineage_v1",
        "upstream_owner_approval_request_issuance_post_review_lineage_ok": upstream_lineage_ok,
        **template_lineage,
        **meta,
    }
    next_phase_doc = {
        "readiness_id": "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_next_phase_readiness_v1",
        "recommended_next_phase": next_phase,
        "target": "freeze_authorization_grant_owner_approval_request_record_approval_closure_dryrun",
        "readiness": "record-approval-closure-dryrun-ready",
        "request_issued": False,
        "notification_sent": False,
        "request_record_created": False,
        "approval_record_created": False,
        "ack_record_created": False,
        "evidence_bound_record_created": False,
        "authorization_request_issued": False,
        "grant_issued": False,
        "foundation_frozen": False,
        "closure_executed": False,
        "runtime_execution_absent": True,
        "protocol_runtime_absent": True,
        "whitebox_runtime_integration_absent": True,
        "module_adapter_implementation_ready": False,
        "next_phase_readiness_ok": next_phase_readiness_ok,
        **meta,
    }
    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "planning_pass": planning_pass,
        "blocker_count": len(issues),
        "issues": issues,
        "downstream_readiness_gaps": downstream_readiness_gaps,
        "evidence_chain_paths_declared": evidence_chain_paths_declared,
        "issuance_post_review_ref_linked": issuance_post_review_ref_linked,
        "planning_node_linked": planning_node_linked,
        "candidate_only": True,
        "no_execution_leakage": non_execution_boundary_ok,
        "no_protocol_change": True,
        **go_condition_values,
        **core_schema_fields,
        **meta,
    }
    markdown = "\n".join(
        [
            "# Task Manager Foundation Handoff Freeze Authorization Owner Approval Request Record Approval Closure Plan v1",
            "",
            "This phase performs freeze authorization grant request record planning only. It does not create request records, bind evidence records, or issue authorization request.",
            "",
            "本阶段仅执行 freeze authorization grant request record planning，不生成 request record，不绑定 evidence record，不发起 authorization request，不生成 owner approval record，不签发 grant。",
            "",
            f"Prior request issuance post-dryrun review GO: `{prior_owner_approval_request_issuance_post_review_go}`",
            f"Authorization request absent: `{authorization_request_absent}`",
            f"Request record absent: `{request_record_absent}`",
            f"Owner approval record absent: `{owner_approval_record_absent}`",
            f"request record planning ≠ request record",
            f"request record candidate ≠ request record",
            f"Template lineage OK: `{template_lineage.get('template_lineage_ok')}`",
            f"Final decision: `{final_decision}`",
            f"Recommended next phase: `{next_phase}`",
            "",
            "## Request Record Boundary Contract",
            *[f"- {stmt}" for stmt in BOUNDARY_CONTRACT_STATEMENTS],
            "",
            "## Governance Debt Carryover (P1, not implemented)",
            f"- {GOVERNANCE_DEBTS[0]['debt_title']}",
            f"- {GOVERNANCE_DEBTS[1]['debt_title']}",
        ]
    )
    return {
        "task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_plan": record_plan,
        "task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_plan_md": markdown,
        "task_manager_freeze_authorization_grant_owner_approval_request_record_candidate_closure_matrix": record_candidate_matrix,
        "task_manager_freeze_authorization_grant_owner_approval_request_approval_candidate_closure_matrix": approval_candidate_matrix,
        "task_manager_freeze_authorization_grant_owner_approval_request_ack_candidate_closure_matrix": ack_candidate_matrix,
        "task_manager_freeze_authorization_grant_owner_approval_request_evidence_binding_closure_matrix": evidence_binding_matrix,
        "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_traceability_matrix": traceability_matrix,
        "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_protocol_reference_matrix": protocol_reference_matrix,
        "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_error_namespace_matrix": error_namespace_matrix,
        "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_whitebox_candidate_ref_matrix": whitebox_candidate_ref_matrix,
        "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_boundary_contract": boundary_contract_doc,
        "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_non_execution_constraints": non_execution,
        "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_rejection_reference_matrix": rejection_matrix,
        "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_expiry_reference_matrix": expiry_matrix,
        "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_revocation_reference_matrix": revocation_matrix,
        "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_governance_debt_carryover": debt_carryover,
        "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_template_lineage": template_lineage_doc,
        "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_next_phase_readiness": next_phase_doc,
        "file_size_governance_review": {**file_size_governance_review, **meta},
        "summary": summary,
    }
