# -*- coding: utf-8 -*-
"""Luna Midplatform Task Manager Foundation Handoff Freeze Authorization Grant Owner Approval Planning v1.

Structure inherited from task_manager_foundation_handoff_freeze_authorization_grant_request_record_planning_v1.py
with upstream evidence from grant_request_record_post_dryrun_review_v1 (whitelist template reuse).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.task_manager_foundation_handoff_evaluation_template_lineage_v1 import (
    GRANT_OWNER_APPROVAL_PLANNING_STAGE_ADDITIONS,
    GRANT_OWNER_APPROVAL_PLANNING_STAGE_TERM_OVERRIDES,
    GRANT_OWNER_APPROVAL_PLANNING_WHITELIST_FILES,
    build_core_go_no_go_summary_fields,
    build_template_lineage,
)
from capabilities.midplatform.task_manager_foundation_handoff_final_closure_planning_v1 import GOVERNANCE_DEBTS
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_request_record_post_dryrun_review_v1 import (
    CHAIN_EVIDENCE_NODES as UPSTREAM_CHAIN_NODES,
    DEFAULT_OUTPUT as DEFAULT_GRANT_REQUEST_RECORD_POST_REVIEW_ROOT,
    FINAL_DECISION_GO as GRANT_REQUEST_RECORD_POST_REVIEW_FINAL_GO,
    GO_CONDITIONS_KEYS as UPSTREAM_GO_KEYS,
    NEXT_PHASE_GO as GRANT_REQUEST_RECORD_POST_REVIEW_NEXT_PHASE,
    RUNTIME_FORBIDDEN_FLAGS,
)
from capabilities.midplatform.task_manager_foundation_handoff_planning_v1 import (
    BOUNDARY_STATEMENT_EN,
    BOUNDARY_STATEMENT_ZH,
    FOUNDATION_ID,
)

PHASE_ID = "Phase-Midplatform-Task-Manager-Foundation-Handoff-Freeze-Authorization-Grant-Owner-Approval-Planning-v1-001"
SCOPE = "midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_planning_only"
SOURCE_CHAIN = "midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_planning_v1"
FINAL_DECISION_GO = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_PLANNING_READY_FOR_DRYRUN"
FINAL_DECISION_PRIOR = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_PLANNING_BLOCKED_BY_PRIOR_REVIEW_GAP"
FINAL_DECISION_SCOPE = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_PLANNING_BLOCKED_BY_APPROVAL_SCOPE_ESCALATION"
FINAL_DECISION_APPROVAL = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_PLANNING_BLOCKED_BY_OWNER_APPROVAL_RECORD_LEAKAGE"
FINAL_DECISION_REQUEST = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_PLANNING_BLOCKED_BY_AUTHORIZATION_REQUEST_LEAKAGE"
FINAL_DECISION_FREEZE = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_PLANNING_BLOCKED_BY_FREEZE_STATE_ESCALATION"
FINAL_DECISION_DEBT = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_PLANNING_BLOCKED_BY_GOVERNANCE_DEBT_GAP"
FINAL_DECISION_L1 = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_PLANNING_BLOCKED_BY_L1_PROTOCOL_SCOPE_LEAKAGE"
FINAL_DECISION_RUNTIME = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_PLANNING_BLOCKED_BY_RUNTIME_SCOPE_LEAKAGE"
FINAL_DECISION_LINEAGE = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_PLANNING_BLOCKED_BY_TEMPLATE_LINEAGE_GAP"
NEXT_PHASE_GO = "Phase-Midplatform-Task-Manager-Foundation-Handoff-Freeze-Authorization-Grant-Owner-Approval-DryRun-v1-001"
NEXT_PHASE_HOLD = "Phase-Midplatform-Task-Manager-Foundation-Handoff-Freeze-Authorization-Grant-Owner-Approval-Planning-Issue-Review-v1-001"
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_planning_v1_smoke_v0"
)
GRANT_OWNER_APPROVAL_PLANNING_PACKAGE_FILES: Tuple[str, ...] = (
    "task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_plan_v1.json",
    "task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_plan_v1.md",
    "task_manager_freeze_authorization_grant_owner_approval_scope_matrix_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_candidate_matrix_v1.json",
    "task_manager_freeze_authorization_grant_owner_operator_ack_candidate_matrix_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_evidence_binding_matrix_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_record_binding_matrix_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_lifecycle_matrix_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_expiry_revocation_matrix_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_prerequisite_matrix_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_boundary_contract_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_non_execution_constraints_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_governance_debt_carryover_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_template_lineage_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_next_phase_readiness_v1.json",
    "summary.json",
    "verifier_report.json",
)
GRANT_REQUEST_RECORD_PLANNING_GO_NO_GO_PACK = (
    "docs/architecture/evaluation/"
    "LUNA_EVALUATION_MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_REQUEST_RECORD_PLANNING_V1_GO_NO_GO_PACK_V0.md"
)

BOUNDARY_CONTRACT_STATEMENTS: Tuple[str, ...] = (
    "owner_approval_planning != owner_approval",
    "owner_approval_candidate != owner_approval_record",
    "owner_operator_ack_candidate != owner_operator_ack_record",
    "approval_evidence_binding_candidate != approval_evidence_bound_record",
    "approval_scope_candidate != approval_scope_granted",
    "request_record_candidate != request_record",
    "authorization_request_candidate != authorization_request_issued",
    "grant_token_candidate != grant_token",
    "grant_candidate != grant_record",
    "freeze_candidate != frozen",
    "closure_candidate != closed",
)
APPROVAL_SCOPE_ROWS: Tuple[Dict[str, str], ...] = (
    {"scope": "owner_approval_definition_boundary", "classification": "owner-approval-planning-scope"},
    {"scope": "owner_operator_ack_candidate_boundary", "classification": "owner-approval-planning-scope"},
    {"scope": "approval_evidence_binding_candidate_boundary", "classification": "owner-approval-planning-scope"},
    {"scope": "request_record_binding_candidate_boundary", "classification": "owner-approval-planning-scope"},
    {"scope": "approval_lifecycle_candidate_boundary", "classification": "owner-approval-planning-scope"},
    {"scope": "expiry_revocation_reference_candidate_boundary", "classification": "owner-approval-planning-scope"},
    {"scope": "governance_debt_acknowledgement", "classification": "owner-approval-planning-scope"},
    {"scope": "non_execution_constraints", "classification": "owner-approval-planning-scope"},
)
PREREQUISITE_ROWS: Tuple[Dict[str, Any], ...] = (
    {"prerequisite": "request_record_post_review_go", "required": True},
    {"prerequisite": "authorization_request_absent", "required": True},
    {"prerequisite": "request_record_absent", "required": True},
    {"prerequisite": "owner_approval_record_absent", "required": True},
    {"prerequisite": "owner_operator_ack_record_absent", "required": True},
    {"prerequisite": "approval_evidence_bound_record_absent", "required": True},
    {"prerequisite": "grant_token_absent", "required": True},
    {"prerequisite": "grant_record_absent", "required": True},
    {"prerequisite": "authorization_grant_absent", "required": True},
    {"prerequisite": "foundation_not_frozen", "required": True},
    {"prerequisite": "closure_not_executed", "required": True},
    {"prerequisite": "governance_debt_preserved", "required": True},
)
NON_EXECUTION_CONSTRAINTS: Tuple[str, ...] = (
    "no_owner_approval_record",
    "no_owner_operator_ack_record",
    "no_approval_evidence_bound_record",
    "no_request_record",
    "no_authorization_request",
    "no_grant_token",
    "no_grant_record",
    "no_authorization_grant",
    "no_approval_revocation_execution_path",
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
OWNER_APPROVAL_CANDIDATE_ROWS: Tuple[Dict[str, Any], ...] = (
    {
        "role": "foundation_owner",
        "approval_status": "owner-approval-candidate",
        "approval_record": False,
        "owner_approval_record": False,
    },
    {
        "role": "operator_approver",
        "approval_status": "owner-approval-candidate",
        "approval_record": False,
        "owner_approval_record": False,
    },
)
OWNER_OPERATOR_ACK_ROWS: Tuple[Dict[str, Any], ...] = (
    {
        "role": "foundation_owner",
        "ack_status": "owner-operator-ack-candidate",
        "ack_record": False,
        "owner_operator_ack_record": False,
    },
    {
        "role": "operator_approver",
        "ack_status": "owner-operator-ack-candidate",
        "ack_record": False,
        "owner_operator_ack_record": False,
    },
)
APPROVAL_EVIDENCE_BINDING_ROWS: Tuple[Dict[str, Any], ...] = (
    {
        "binding_id": "record_post_review_evidence_ref",
        "binding_status": "approval-evidence-binding-candidate",
        "approval_evidence_bound": False,
    },
    {
        "binding_id": "handoff_chain_approval_evidence_ref",
        "binding_status": "approval-evidence-binding-candidate",
        "approval_evidence_bound": False,
    },
)
REQUEST_RECORD_BINDING_ROWS: Tuple[Dict[str, Any], ...] = (
    {
        "binding_id": "authorization_request_record_binding",
        "binding_status": "request-record-binding-candidate",
        "request_record_bound": False,
        "active_bound_request_record": False,
    },
    {
        "binding_id": "freeze_authorization_grant_request_record_binding",
        "binding_status": "request-record-binding-candidate",
        "request_record_bound": False,
        "active_bound_request_record": False,
    },
)
APPROVAL_LIFECYCLE_ROWS: Tuple[Dict[str, str], ...] = (
    {"stage": "approval_candidate_defined", "lifecycle_type": "candidate-lifecycle"},
    {"stage": "approval_candidate_audited", "lifecycle_type": "candidate-lifecycle"},
    {"stage": "approval_candidate_expiry_ref_prepared", "lifecycle_type": "candidate-lifecycle"},
)
EXPIRY_REVOCATION_ROWS: Tuple[Dict[str, Any], ...] = (
    {
        "reference_id": "approval_expiry_ref",
        "reference_status": "expiry-revocation-reference-candidate",
        "revocation_execution_path": False,
    },
    {
        "reference_id": "approval_revocation_ref",
        "reference_status": "expiry-revocation-reference-candidate",
        "revocation_execution_path": False,
    },
)
CHAIN_EVIDENCE_NODES: Tuple[str, ...] = UPSTREAM_CHAIN_NODES + (
    "freeze_authorization_grant_owner_approval_planning",
)
GO_CONDITIONS_KEYS: Tuple[str, ...] = (
    "prior_request_record_post_review_go",
    "owner_approval_plan_complete",
    "approval_scope_planning_only",
    "owner_approval_candidate_only",
    "owner_operator_ack_candidate_only",
    "approval_evidence_binding_candidate_only",
    "request_record_binding_candidate_only",
    "approval_lifecycle_candidate_only",
    "expiry_revocation_reference_candidate_only",
    "authorization_request_absent",
    "request_record_absent",
    "owner_approval_record_absent",
    "owner_operator_ack_record_absent",
    "approval_evidence_bound_record_absent",
    "grant_token_absent",
    "grant_record_absent",
    "authorization_grant_absent",
    "foundation_not_frozen",
    "closure_not_executed",
    "governance_debt_carryover_complete",
    "l1_protocols_not_implemented",
    "system_protocols_integration_not_implemented",
    "template_lineage_ok",
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
        "owner_approval_planning_only": True,
        "authorization_request_absent": True,
        "authorization_request_issued": False,
        "request_record_absent": True,
        "owner_approval_record_absent": True,
        "owner_operator_ack_record_absent": True,
        "approval_evidence_bound_record_absent": True,
        "authorization_grant_absent": True,
        "grant_token_absent": True,
        "grant_record_absent": True,
        "foundation_not_frozen": True,
        "closure_not_executed": True,
        "l1_protocols_not_implemented": True,
        "system_protocols_integration_not_implemented": True,
        "output_root": str(out),
        "grant_request_record_post_dryrun_review_root": str(post_review),
        "boundary_statement_en": BOUNDARY_STATEMENT_EN,
        "boundary_statement_zh": BOUNDARY_STATEMENT_ZH,
    }


def run_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_planning_v1(
    *,
    grant_request_record_post_dryrun_review_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    out = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    post_review = Path(grant_request_record_post_dryrun_review_root).expanduser().resolve()
    repo_root = Path(__file__).resolve().parents[2]
    meta = _meta(out, post_review)
    issues: List[str] = []

    post_summary = _read_json(post_review / "summary.json")
    post_verifier = _read_json(post_review / "verifier_report.json")
    chain_review = _read_json(
        post_review / "task_manager_freeze_authorization_grant_request_record_chain_evidence_review_v1.json"
    )
    absence_src = _read_json(
        post_review / "task_manager_freeze_authorization_grant_request_record_absence_review_v1.json"
    )

    prior_request_record_post_review_go = (
        post_summary.get("final_decision") == GRANT_REQUEST_RECORD_POST_REVIEW_FINAL_GO
        and post_summary.get("recommended_next_phase") == GRANT_REQUEST_RECORD_POST_REVIEW_NEXT_PHASE
        and post_verifier.get("verifier") == "GO"
        and int(post_verifier.get("passed_checks", 0)) >= 420
        and post_verifier.get("failed_checks") == 0
        and post_verifier.get("blocker_count") == 0
        and post_summary.get("owner_approval_planning_ready") is True
        and all(post_summary.get(k) is True for k in UPSTREAM_GO_KEYS)
    )
    if not prior_request_record_post_review_go:
        issues.append("prior_request_record_post_review_not_go")

    evidence_chain = []
    for stage in UPSTREAM_CHAIN_NODES:
        row = next((r for r in chain_review.get("chain") or [] if r.get("stage") == stage), {})
        evidence_chain.append({"stage": stage, "linked": row.get("linked") is True})
    evidence_chain.append(
        {
            "stage": "freeze_authorization_grant_owner_approval_planning",
            "root": str(out),
            "readiness": "owner-approval-planning-ready",
            "authorization_request_issued": False,
            "request_record": False,
            "owner_approval_record": False,
            "grant_issued": False,
            "linked": True,
        }
    )
    evidence_chain_complete = prior_request_record_post_review_go and all(
        node.get("linked") for node in evidence_chain
    )
    if not evidence_chain_complete:
        issues.append("evidence_chain_gap")

    scope_rows = list(APPROVAL_SCOPE_ROWS)
    approval_scope_planning_only = all(
        row["classification"] == "owner-approval-planning-scope"
        and row["classification"] not in ("approval-granted-scope", "authorized-scope")
        for row in scope_rows
    )
    if not approval_scope_planning_only:
        issues.append("approval_scope_escalation")

    owner_rows = list(OWNER_APPROVAL_CANDIDATE_ROWS)
    owner_approval_candidate_only = all(
        row.get("approval_status") == "owner-approval-candidate"
        and row.get("approval_status") != "owner-approval-record"
        and row.get("approval_record") is False
        and row.get("owner_approval_record") is False
        for row in owner_rows
    )
    if not owner_approval_candidate_only:
        issues.append("owner_approval_record_leakage")

    ack_rows = list(OWNER_OPERATOR_ACK_ROWS)
    owner_operator_ack_candidate_only = all(
        row.get("ack_status") == "owner-operator-ack-candidate"
        and row.get("ack_status") != "owner-operator-ack-record"
        and row.get("ack_record") is False
        and row.get("owner_operator_ack_record") is False
        for row in ack_rows
    )
    if not owner_operator_ack_candidate_only:
        issues.append("owner_operator_ack_record_leakage")

    evidence_binding_rows = list(APPROVAL_EVIDENCE_BINDING_ROWS)
    approval_evidence_binding_candidate_only = all(
        row.get("binding_status") == "approval-evidence-binding-candidate"
        and row.get("binding_status") != "approval-evidence-bound-record"
        and row.get("approval_evidence_bound") is False
        for row in evidence_binding_rows
    )
    if not approval_evidence_binding_candidate_only:
        issues.append("approval_evidence_binding_leakage")

    record_binding_rows = list(REQUEST_RECORD_BINDING_ROWS)
    request_record_binding_candidate_only = all(
        row.get("binding_status") == "request-record-binding-candidate"
        and row.get("request_record_bound") is False
        and row.get("active_bound_request_record") is False
        for row in record_binding_rows
    )
    if not request_record_binding_candidate_only:
        issues.append("request_record_binding_leakage")

    lifecycle_rows = list(APPROVAL_LIFECYCLE_ROWS)
    approval_lifecycle_candidate_only = all(
        row.get("lifecycle_type") == "candidate-lifecycle"
        and row.get("lifecycle_type") != "active-approval-lifecycle"
        for row in lifecycle_rows
    )
    if not approval_lifecycle_candidate_only:
        issues.append("approval_lifecycle_escalation")

    expiry_revocation_rows = list(EXPIRY_REVOCATION_ROWS)
    expiry_revocation_reference_candidate_only = all(
        row.get("reference_status") == "expiry-revocation-reference-candidate"
        and row.get("reference_status") not in ("expiry-execution-path", "revocation-execution-path")
        and row.get("revocation_execution_path") is False
        for row in expiry_revocation_rows
    )
    if not expiry_revocation_reference_candidate_only:
        issues.append("approval_revocation_execution_leakage")

    prerequisite_values = {
        "request_record_post_review_go": prior_request_record_post_review_go,
        "authorization_request_absent": post_summary.get("authorization_request_absent") is True
        or absence_src.get("authorization_request_issued") is False,
        "request_record_absent": post_summary.get("request_record_absent") is True
        or absence_src.get("request_record_absent") is True,
        "owner_approval_record_absent": post_summary.get("owner_approval_record_absent") is True
        or absence_src.get("owner_approval_record_absent") is True,
        "owner_operator_ack_record_absent": True,
        "approval_evidence_bound_record_absent": post_summary.get("evidence_bound_record_absent") is True
        or absence_src.get("evidence_bound_record_absent") is True,
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
    owner_operator_ack_record_absent = prerequisite_values["owner_operator_ack_record_absent"]
    approval_evidence_bound_record_absent = prerequisite_values["approval_evidence_bound_record_absent"]
    request_record_absent = prerequisite_values["request_record_absent"]
    foundation_not_frozen = prerequisite_values["foundation_not_frozen"]
    closure_not_executed = prerequisite_values["closure_not_executed"]

    if not authorization_request_absent:
        issues.append("authorization_request_leakage")
    if (
        not request_record_absent
        or not owner_approval_record_absent
        or not owner_operator_ack_record_absent
        or not approval_evidence_bound_record_absent
        or not grant_token_absent
        or not grant_record_absent
    ):
        issues.append("owner_approval_record_leakage")

    boundary_contract = {
        "contract_id": "task_manager_freeze_authorization_grant_owner_approval_boundary_contract_v1",
        "statements": list(BOUNDARY_CONTRACT_STATEMENTS),
        "owner_approval_planning_only": True,
        "authorization_request_absent": True,
        "authorization_request_issued": False,
        "request_record_absent": True,
        "owner_approval_record_absent": True,
        "owner_operator_ack_record_absent": True,
        "approval_evidence_bound_record_absent": True,
        "grant_issued": False,
        "freeze_status": "freeze-candidate",
        "foundation_frozen": False,
        "closure_applied": False,
        "closed": False,
    }

    debts = list(GOVERNANCE_DEBTS)
    governance_debt_carryover_complete = (
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
    if not governance_debt_carryover_complete:
        issues.append("governance_debt_gap")

    l1_protocols_not_implemented = True
    system_protocols_integration_not_implemented = True
    non_execution_boundary_ok = True

    template_lineage = build_template_lineage(
        base_phase="Freeze-Authorization-Grant-Request-Record-Planning-v1-001",
        base_capability=GRANT_OWNER_APPROVAL_PLANNING_WHITELIST_FILES[0],
        base_runner=GRANT_OWNER_APPROVAL_PLANNING_WHITELIST_FILES[1],
        base_verifier=GRANT_OWNER_APPROVAL_PLANNING_WHITELIST_FILES[2],
        base_go_no_go_pack=GRANT_REQUEST_RECORD_PLANNING_GO_NO_GO_PACK,
        stage_phase="Freeze-Authorization-Grant-Owner-Approval-Planning-v1-001",
        stage_term_overrides=GRANT_OWNER_APPROVAL_PLANNING_STAGE_TERM_OVERRIDES,
        stage_additions=GRANT_OWNER_APPROVAL_PLANNING_STAGE_ADDITIONS,
        template_files=GRANT_OWNER_APPROVAL_PLANNING_WHITELIST_FILES,
        repo_root=repo_root,
        upstream_review_phase="Freeze-Authorization-Grant-Request-Record-Post-DryRun-Review-v1-001",
    )
    upstream_lineage_ok = post_summary.get("template_lineage_ok") is True
    if not template_lineage.get("template_lineage_ok") or not upstream_lineage_ok:
        issues.append("template_lineage_gap")

    owner_approval_plan_complete = (
        prior_request_record_post_review_go
        and evidence_chain_complete
        and approval_scope_planning_only
        and owner_approval_candidate_only
        and owner_operator_ack_candidate_only
        and approval_evidence_binding_candidate_only
        and request_record_binding_candidate_only
        and approval_lifecycle_candidate_only
        and expiry_revocation_reference_candidate_only
        and prerequisites_ok
        and governance_debt_carryover_complete
        and template_lineage.get("template_lineage_ok") is True
    )
    next_phase_readiness_ok = owner_approval_plan_complete

    if not prior_request_record_post_review_go:
        final_decision = FINAL_DECISION_PRIOR
    elif not template_lineage.get("template_lineage_ok"):
        final_decision = FINAL_DECISION_LINEAGE
    elif (
        not approval_scope_planning_only
        or not owner_approval_candidate_only
        or not owner_operator_ack_candidate_only
        or not approval_evidence_binding_candidate_only
        or not request_record_binding_candidate_only
        or not approval_lifecycle_candidate_only
        or not expiry_revocation_reference_candidate_only
    ):
        final_decision = FINAL_DECISION_SCOPE
    elif (
        not request_record_absent
        or not owner_approval_record_absent
        or not owner_operator_ack_record_absent
        or not approval_evidence_bound_record_absent
        or not grant_token_absent
        or not grant_record_absent
    ):
        final_decision = FINAL_DECISION_APPROVAL
    elif not authorization_request_absent:
        final_decision = FINAL_DECISION_REQUEST
    elif not foundation_not_frozen:
        final_decision = FINAL_DECISION_FREEZE
    elif not governance_debt_carryover_complete:
        final_decision = FINAL_DECISION_DEBT
    elif not l1_protocols_not_implemented:
        final_decision = FINAL_DECISION_L1
    elif not non_execution_boundary_ok:
        final_decision = FINAL_DECISION_RUNTIME
    else:
        final_decision = FINAL_DECISION_GO

    go_condition_values = {
        "prior_request_record_post_review_go": prior_request_record_post_review_go,
        "owner_approval_plan_complete": owner_approval_plan_complete,
        "approval_scope_planning_only": approval_scope_planning_only,
        "owner_approval_candidate_only": owner_approval_candidate_only,
        "owner_operator_ack_candidate_only": owner_operator_ack_candidate_only,
        "approval_evidence_binding_candidate_only": approval_evidence_binding_candidate_only,
        "request_record_binding_candidate_only": request_record_binding_candidate_only,
        "approval_lifecycle_candidate_only": approval_lifecycle_candidate_only,
        "expiry_revocation_reference_candidate_only": expiry_revocation_reference_candidate_only,
        "authorization_request_absent": authorization_request_absent,
        "request_record_absent": request_record_absent,
        "owner_approval_record_absent": owner_approval_record_absent,
        "owner_operator_ack_record_absent": owner_operator_ack_record_absent,
        "approval_evidence_bound_record_absent": approval_evidence_bound_record_absent,
        "grant_token_absent": grant_token_absent,
        "grant_record_absent": grant_record_absent,
        "authorization_grant_absent": authorization_grant_absent,
        "foundation_not_frozen": foundation_not_frozen,
        "closure_not_executed": closure_not_executed,
        "governance_debt_carryover_complete": governance_debt_carryover_complete,
        "l1_protocols_not_implemented": l1_protocols_not_implemented,
        "system_protocols_integration_not_implemented": system_protocols_integration_not_implemented,
        "template_lineage_ok": template_lineage.get("template_lineage_ok") is True and upstream_lineage_ok,
        "non_execution_boundary_ok": non_execution_boundary_ok,
        "next_phase_readiness_ok": next_phase_readiness_ok,
    }
    planning_pass = len(issues) == 0 and final_decision == FINAL_DECISION_GO and all(go_condition_values.values())
    next_phase = NEXT_PHASE_GO if planning_pass else NEXT_PHASE_HOLD
    core_schema_fields = build_core_go_no_go_summary_fields(
        go_conditions=go_condition_values,
        forbidden_runtime_flags=RUNTIME_FORBIDDEN_FLAGS,
        chain_trace_nodes=CHAIN_EVIDENCE_NODES,
        go_no_go_decision=final_decision,
        final_decision=final_decision,
        next_phase=next_phase,
        template_lineage=template_lineage,
    )

    approval_plan = {
        "plan_id": "task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_plan_v1",
        "approval_scope": [
            "define owner/operator approval basis before request record creation without issuing approval",
            "define owner-approval-candidate without approval records",
            "define owner-operator-ack-candidate without ack records",
            "define approval-evidence-binding-candidate without binding approval evidence records",
            "define request-record-binding-candidate without active bound request records",
            "define candidate approval lifecycle without active approval lifecycle",
            "define expiry-revocation-reference-candidate without expiry/revocation execution path",
            "trace evidence chain through owner approval planning",
            "preserve governance debt carryover",
            "define non-execution constraints for future owner approval dry-run",
        ],
        "evidence_chain": evidence_chain,
        "evidence_chain_complete": evidence_chain_complete,
        "node_count": len(CHAIN_EVIDENCE_NODES),
        **go_condition_values,
        "final_decision": final_decision,
        "recommended_next_phase": next_phase,
        **meta,
    }
    scope_matrix = {
        "matrix_id": "task_manager_freeze_authorization_grant_owner_approval_scope_matrix_v1",
        "rows": scope_rows,
        "approval_scope_planning_only": approval_scope_planning_only,
        **meta,
    }
    candidate_matrix = {
        "matrix_id": "task_manager_freeze_authorization_grant_owner_approval_candidate_matrix_v1",
        "rows": owner_rows,
        "owner_approval_candidate_only": owner_approval_candidate_only,
        **meta,
    }
    ack_matrix = {
        "matrix_id": "task_manager_freeze_authorization_grant_owner_operator_ack_candidate_matrix_v1",
        "rows": ack_rows,
        "owner_operator_ack_candidate_only": owner_operator_ack_candidate_only,
        **meta,
    }
    evidence_binding_matrix = {
        "matrix_id": "task_manager_freeze_authorization_grant_owner_approval_evidence_binding_matrix_v1",
        "rows": evidence_binding_rows,
        "approval_evidence_binding_candidate_only": approval_evidence_binding_candidate_only,
        **meta,
    }
    record_binding_matrix = {
        "matrix_id": "task_manager_freeze_authorization_grant_owner_approval_request_record_binding_matrix_v1",
        "rows": record_binding_rows,
        "request_record_binding_candidate_only": request_record_binding_candidate_only,
        **meta,
    }
    lifecycle_matrix = {
        "matrix_id": "task_manager_freeze_authorization_grant_owner_approval_lifecycle_matrix_v1",
        "rows": lifecycle_rows,
        "approval_lifecycle_candidate_only": approval_lifecycle_candidate_only,
        **meta,
    }
    expiry_revocation_matrix = {
        "matrix_id": "task_manager_freeze_authorization_grant_owner_approval_expiry_revocation_matrix_v1",
        "rows": expiry_revocation_rows,
        "expiry_revocation_reference_candidate_only": expiry_revocation_reference_candidate_only,
        **meta,
    }
    prerequisite_matrix = {
        "matrix_id": "task_manager_freeze_authorization_grant_owner_approval_prerequisite_matrix_v1",
        "rows": prerequisite_rows,
        "prerequisites_ok": prerequisites_ok,
        **meta,
    }
    boundary_contract_doc = {**boundary_contract, **meta}
    non_execution = {
        "constraints_id": "task_manager_freeze_authorization_grant_owner_approval_non_execution_constraints_v1",
        "constraints": list(NON_EXECUTION_CONSTRAINTS),
        "non_execution_boundary_ok": non_execution_boundary_ok,
        **{c: True for c in NON_EXECUTION_CONSTRAINTS},
        **meta,
    }
    debt_carryover = {
        "carryover_id": "task_manager_freeze_authorization_grant_owner_approval_governance_debt_carryover_v1",
        "debts": debts,
        "governance_debt_carryover_complete": governance_debt_carryover_complete,
        "l1_protocols_not_implemented": l1_protocols_not_implemented,
        "system_protocols_integration_not_implemented": system_protocols_integration_not_implemented,
        **meta,
    }
    template_lineage_doc = {
        "lineage_id": "task_manager_freeze_authorization_grant_owner_approval_template_lineage_v1",
        "upstream_grant_request_record_post_review_lineage_ok": upstream_lineage_ok,
        **template_lineage,
        **meta,
    }
    next_phase_doc = {
        "readiness_id": "task_manager_freeze_authorization_grant_owner_approval_next_phase_readiness_v1",
        "recommended_next_phase": next_phase,
        "target": "freeze_authorization_grant_owner_approval_dryrun",
        "readiness": "freeze-authorization-grant-owner-approval-dryrun-ready",
        "authorization_request_issued": False,
        "request_record_created": False,
        "owner_approval_record_created": False,
        "owner_operator_ack_record_created": False,
        "grant_issued": False,
        "freeze_authorization_granted": False,
        "foundation_frozen": False,
        "closed": False,
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
        **go_condition_values,
        **core_schema_fields,
        **meta,
    }
    markdown = "\n".join(
        [
            "# Task Manager Foundation Handoff Freeze Authorization Grant Owner Approval Plan v1",
            "",
            "This phase performs freeze authorization grant owner approval planning only. It does not issue owner approval, create approval records, or bind approval evidence records.",
            "",
            "本阶段仅执行 freeze authorization grant owner approval planning，不生成 owner approval record，不生成 owner/operator ack record，不绑定 approval evidence record，不生成 request record，不发起 authorization request，不签发 grant。",
            "",
            f"Prior request record post-dryrun review GO: `{prior_request_record_post_review_go}`",
            f"Authorization request absent: `{authorization_request_absent}`",
            f"Request record absent: `{request_record_absent}`",
            f"Owner approval record absent: `{owner_approval_record_absent}`",
            f"Owner/operator ack record absent: `{owner_operator_ack_record_absent}`",
            f"Approval evidence bound record absent: `{approval_evidence_bound_record_absent}`",
            f"owner approval planning ≠ owner approval",
            f"owner approval candidate ≠ owner approval record",
            f"Template lineage OK: `{template_lineage.get('template_lineage_ok')}`",
            f"Final decision: `{final_decision}`",
            f"Recommended next phase: `{next_phase}`",
            "",
            "## Owner Approval Boundary Contract",
            *[f"- {stmt}" for stmt in BOUNDARY_CONTRACT_STATEMENTS],
            "",
            "## Governance Debt Carryover (P1, not implemented)",
            f"- {GOVERNANCE_DEBTS[0]['debt_title']}",
            f"- {GOVERNANCE_DEBTS[1]['debt_title']}",
        ]
    )
    return {
        "task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_plan": approval_plan,
        "task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_plan_md": markdown,
        "task_manager_freeze_authorization_grant_owner_approval_scope_matrix": scope_matrix,
        "task_manager_freeze_authorization_grant_owner_approval_candidate_matrix": candidate_matrix,
        "task_manager_freeze_authorization_grant_owner_operator_ack_candidate_matrix": ack_matrix,
        "task_manager_freeze_authorization_grant_owner_approval_evidence_binding_matrix": evidence_binding_matrix,
        "task_manager_freeze_authorization_grant_owner_approval_request_record_binding_matrix": record_binding_matrix,
        "task_manager_freeze_authorization_grant_owner_approval_lifecycle_matrix": lifecycle_matrix,
        "task_manager_freeze_authorization_grant_owner_approval_expiry_revocation_matrix": expiry_revocation_matrix,
        "task_manager_freeze_authorization_grant_owner_approval_prerequisite_matrix": prerequisite_matrix,
        "task_manager_freeze_authorization_grant_owner_approval_boundary_contract": boundary_contract_doc,
        "task_manager_freeze_authorization_grant_owner_approval_non_execution_constraints": non_execution,
        "task_manager_freeze_authorization_grant_owner_approval_governance_debt_carryover": debt_carryover,
        "task_manager_freeze_authorization_grant_owner_approval_template_lineage": template_lineage_doc,
        "task_manager_freeze_authorization_grant_owner_approval_next_phase_readiness": next_phase_doc,
        "summary": summary,
    }
