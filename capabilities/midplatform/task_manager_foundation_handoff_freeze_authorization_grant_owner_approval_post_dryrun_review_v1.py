# -*- coding: utf-8 -*-
"""Luna Midplatform Task Manager Foundation Handoff Freeze Authorization Grant Owner Approval Post-DryRun Review v1.

Structure inherited from task_manager_foundation_handoff_freeze_authorization_grant_request_record_post_dryrun_review_v1.py
with upstream input from grant_owner_approval_dryrun_v1 (whitelist template reuse).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.protocol_canonical_standard_planning_v1 import GOVERNANCE_DEBTS
from capabilities.midplatform.protocols.protocol_separation_rule_v1 import FAILURE_CLASSIFICATION
from capabilities.midplatform.task_manager_foundation_handoff_evaluation_template_lineage_v1 import (
    GRANT_OWNER_APPROVAL_POST_REVIEW_STAGE_ADDITIONS,
    GRANT_OWNER_APPROVAL_POST_REVIEW_STAGE_TERM_OVERRIDES,
    GRANT_OWNER_APPROVAL_POST_REVIEW_WHITELIST_FILES,
    build_core_go_no_go_summary_fields,
    build_template_lineage,
)
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_dryrun_v1 import (
    CHAIN_TRACE_NODES,
    DEFAULT_OUTPUT as DEFAULT_DRYRUN_ROOT,
    DRYRUN_BOUNDARY_STATEMENTS,
    ERROR_NAMESPACE,
    FINAL_DECISION_GO as DRYRUN_FINAL_GO,
    GO_CONDITIONS_KEYS as DRYRUN_TRUE_KEYS,
    GRANT_OWNER_APPROVAL_DRYRUN_ARTIFACTS,
    NEXT_PHASE_GO as DRYRUN_NEXT_PHASE,
    PROTOCOL_EXECUTION_RESULT_SCHEMA_REF,
    PROTOCOL_ID,
    PROTOCOL_STANDARD_REF,
    RELATED_PROTOCOL_IDS,
    RUNTIME_FORBIDDEN_FLAGS,
    SEPARATION_RULE_REF,
)
from capabilities.midplatform.task_manager_foundation_handoff_planning_v1 import (
    BOUNDARY_STATEMENT_EN,
    BOUNDARY_STATEMENT_ZH,
    FOUNDATION_ID,
)

PHASE_ID = "Phase-Midplatform-Task-Manager-Foundation-Handoff-Freeze-Authorization-Grant-Owner-Approval-Post-DryRun-Review-v1-001"
SCOPE = "midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_post_dryrun_review_only"
SOURCE_CHAIN = "midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_post_dryrun_review_v1"
FINAL_DECISION_GO = (
    "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_POST_DRYRUN_REVIEW_READY_FOR_OWNER_APPROVAL_REQUEST_PLANNING"
)
FINAL_DECISION_EVIDENCE = (
    "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_POST_DRYRUN_REVIEW_BLOCKED_BY_DRYRUN_EVIDENCE_GAP"
)
FINAL_DECISION_BOUNDARY = (
    "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_POST_DRYRUN_REVIEW_BLOCKED_BY_BOUNDARY_DRIFT"
)
FINAL_DECISION_PROTOCOL = (
    "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_POST_DRYRUN_REVIEW_BLOCKED_BY_PROTOCOL_REFERENCE_GAP"
)
FINAL_DECISION_APPROVAL = (
    "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_POST_DRYRUN_REVIEW_BLOCKED_BY_OWNER_APPROVAL_RECORD_LEAKAGE"
)
FINAL_DECISION_REQUEST = (
    "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_POST_DRYRUN_REVIEW_BLOCKED_BY_AUTHORIZATION_REQUEST_LEAKAGE"
)
FINAL_DECISION_FREEZE = (
    "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_POST_DRYRUN_REVIEW_BLOCKED_BY_FREEZE_STATE_ESCALATION"
)
FINAL_DECISION_DEBT = (
    "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_POST_DRYRUN_REVIEW_BLOCKED_BY_GOVERNANCE_DEBT_GAP"
)
FINAL_DECISION_L1 = (
    "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_POST_DRYRUN_REVIEW_BLOCKED_BY_L1_PROTOCOL_SCOPE_LEAKAGE"
)
FINAL_DECISION_RUNTIME = (
    "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_POST_DRYRUN_REVIEW_BLOCKED_BY_RUNTIME_SCOPE_LEAKAGE"
)
FINAL_DECISION_LINEAGE = (
    "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_POST_DRYRUN_REVIEW_BLOCKED_BY_TEMPLATE_LINEAGE_GAP"
)
NEXT_PHASE_GO = "Phase-Midplatform-Task-Manager-Foundation-Handoff-Freeze-Authorization-Grant-Owner-Approval-Request-Planning-v1-001"
NEXT_PHASE_ALT = "Phase-Midplatform-Task-Manager-Foundation-Handoff-Freeze-Authorization-Grant-Owner-Approval-Issuance-Planning-v1-001"
NEXT_PHASE_HOLD = (
    "Phase-Midplatform-Task-Manager-Foundation-Handoff-Freeze-Authorization-Grant-Owner-Approval-Post-DryRun-Review-Issue-Review-v1-001"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_post_dryrun_review_v1_smoke_v0"
)
POST_REVIEW_SCOPE = "owner-approval-post-review-scope"
FORBIDDEN_SCOPE_CLASSIFICATIONS: Tuple[str, ...] = ("approval-granted-scope", "authorized-scope")

POST_REVIEW_BOUNDARY_STATEMENTS: Tuple[str, ...] = (
    "owner_approval_post_dryrun_review != owner_approval",
    "owner_approval_candidate != owner_approval_record",
    "owner_operator_ack_candidate != owner_operator_ack_record",
    "approval_evidence_binding_candidate != approval_evidence_bound_record",
    "request_record_binding_candidate != request_record",
    "approval_lifecycle_candidate != active-approval-lifecycle",
    "expiry_revocation_reference_candidate != revocation-execution-path",
    "authorization_request_candidate != authorization_request_issued",
    "grant_token_candidate != grant_token",
    "grant_candidate != grant_record",
    "freeze_candidate != frozen",
    "closure_candidate != closed",
)
CHAIN_EVIDENCE_NODES: Tuple[str, ...] = CHAIN_TRACE_NODES + (
    "freeze_authorization_grant_owner_approval_post_dryrun_review",
)
GO_CONDITIONS_KEYS: Tuple[str, ...] = (
    "prior_owner_approval_dryrun_go",
    "owner_approval_dryrun_result_accepted",
    "protocol_reference_review_ok",
    "separation_rule_review_ok",
    "candidate_state_preserved",
    "owner_operator_ack_candidate_preserved",
    "approval_evidence_binding_candidate_preserved",
    "request_record_binding_candidate_preserved",
    "approval_lifecycle_candidate_preserved",
    "expiry_revocation_reference_candidate_preserved",
    "absence_review_ok",
    "boundary_drift_absent",
    "evidence_chain_review_ok",
    "governance_debt_preserved",
    "template_lineage_ok",
    "post_review_only",
    "non_execution_boundary_ok",
    "next_phase_readiness_ok",
)


def _read_json(path: Path) -> Dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return {}
    return payload if isinstance(payload, dict) else {}


def _meta(out: Path, dryrun: Path) -> Dict[str, Any]:
    return {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "source_chain": SOURCE_CHAIN,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "foundation_id": FOUNDATION_ID,
        "runtime_status": "not_enabled",
        "post_review_only": True,
        "post_review_scope": POST_REVIEW_SCOPE,
        "shared_protocol_system_revalidation": False,
        "protocol_standard_ref": PROTOCOL_STANDARD_REF,
        "protocol_id": PROTOCOL_ID,
        "related_protocol_ids": list(RELATED_PROTOCOL_IDS),
        "error_namespace": ERROR_NAMESPACE,
        "protocol_execution_result_schema_ref": PROTOCOL_EXECUTION_RESULT_SCHEMA_REF,
        "separation_rule_ref": SEPARATION_RULE_REF,
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
        "grant_owner_approval_dryrun_root": str(dryrun),
        "boundary_statement_en": BOUNDARY_STATEMENT_EN,
        "boundary_statement_zh": BOUNDARY_STATEMENT_ZH,
    }


def run_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_post_dryrun_review_v1(
    *,
    grant_owner_approval_dryrun_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    out = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    dryrun = Path(grant_owner_approval_dryrun_root or DEFAULT_DRYRUN_ROOT).expanduser().resolve()
    repo_root = Path(__file__).resolve().parents[2]
    meta = _meta(out, dryrun)
    issues: List[str] = []

    dryrun_summary = _read_json(dryrun / "summary.json")
    dryrun_verifier = _read_json(dryrun / "verifier_report.json")
    dryrun_lineage = _read_json(dryrun / "task_manager_freeze_authorization_grant_owner_approval_template_lineage_v1.json")
    trace_matrix = _read_json(dryrun / "task_manager_freeze_authorization_grant_owner_approval_evidence_traceability_v1.json")
    candidate_val = _read_json(dryrun / "task_manager_freeze_authorization_grant_owner_approval_candidate_validation_v1.json")
    ack_val = _read_json(dryrun / "task_manager_freeze_authorization_grant_owner_operator_ack_candidate_validation_v1.json")
    evidence_val = _read_json(
        dryrun / "task_manager_freeze_authorization_grant_owner_approval_evidence_binding_validation_v1.json"
    )
    record_binding_val = _read_json(
        dryrun / "task_manager_freeze_authorization_grant_owner_approval_request_record_binding_validation_v1.json"
    )
    lifecycle_val = _read_json(dryrun / "task_manager_freeze_authorization_grant_owner_approval_lifecycle_validation_v1.json")
    expiry_revocation_val = _read_json(
        dryrun / "task_manager_freeze_authorization_grant_owner_approval_expiry_revocation_validation_v1.json"
    )
    absence_val = _read_json(dryrun / "task_manager_freeze_authorization_grant_owner_approval_absence_validation_v1.json")
    boundary_val = _read_json(dryrun / "task_manager_freeze_authorization_grant_owner_approval_boundary_validation_v1.json")
    protocol_val = _read_json(
        dryrun / "task_manager_freeze_authorization_grant_owner_approval_protocol_reference_validation_v1.json"
    )
    debt_val = _read_json(dryrun / "task_manager_freeze_authorization_grant_owner_approval_governance_debt_validation_v1.json")
    post_review_readiness = _read_json(
        dryrun / "task_manager_freeze_authorization_grant_owner_approval_post_review_readiness_v1.json"
    )

    review_rows = []
    for fname in GRANT_OWNER_APPROVAL_DRYRUN_ARTIFACTS:
        path = dryrun / fname
        if fname.endswith(".json"):
            non_placeholder = bool(_read_json(path))
        else:
            non_placeholder = path.is_file() and len(path.read_text(encoding="utf-8").strip()) > 200
        review_rows.append({"artifact": fname, "exists": path.is_file(), "non_placeholder": non_placeholder})
        if not path.is_file() or not non_placeholder:
            issues.append(f"missing_dryrun_artifact:{fname}")

    prior_owner_approval_dryrun_go = (
        dryrun_summary.get("final_decision") == DRYRUN_FINAL_GO
        and dryrun_summary.get("recommended_next_phase") == DRYRUN_NEXT_PHASE
        and dryrun_verifier.get("verifier") == "GO"
        and int(dryrun_verifier.get("passed_checks", 0)) >= 420
        and dryrun_verifier.get("failed_checks") == 0
        and dryrun_verifier.get("blocker_count") == 0
        and dryrun_summary.get("post_review_readiness_ok") is True
    )
    if not prior_owner_approval_dryrun_go:
        issues.append("owner_approval_dryrun_not_go")

    owner_approval_dryrun_result_accepted = (
        prior_owner_approval_dryrun_go
        and all(dryrun_summary.get(k) is True for k in DRYRUN_TRUE_KEYS)
        and dryrun_summary.get("template_lineage_ok") is True
    )
    if not owner_approval_dryrun_result_accepted:
        issues.append("owner_approval_dryrun_not_accepted")

    protocol_reference_review_ok = (
        protocol_val.get("shared_protocol_system_revalidation") is False
        and protocol_val.get("protocol_standard_ref") == PROTOCOL_STANDARD_REF
        and protocol_val.get("protocol_id") == PROTOCOL_ID
        and protocol_val.get("error_namespace") == ERROR_NAMESPACE
        and protocol_val.get("protocol_execution_result_schema_ref") == PROTOCOL_EXECUTION_RESULT_SCHEMA_REF
        and protocol_val.get("separation_rule_ref") == SEPARATION_RULE_REF
        and protocol_val.get("protocol_standard_reference_ok") is True
        and protocol_val.get("protocol_id_reference_ok") is True
        and protocol_val.get("error_namespace_reference_ok") is True
        and protocol_val.get("protocol_execution_result_schema_ref_ok") is True
        and protocol_val.get("separation_rule_ref_ok") is True
        and protocol_val.get("protocol_error_code_light_check_ok") is True
        and protocol_val.get("whitebox_candidate_ref_ok") is True
    )
    if not protocol_reference_review_ok:
        issues.append("protocol_reference_review_gap")

    separation_rule_review_ok = (
        protocol_val.get("separation_rule_ref_ok") is True
        and protocol_val.get("module_local_failure_not_protocol_failure_by_default") is True
        and list(protocol_val.get("error_classification_rules") or []) == list(FAILURE_CLASSIFICATION)
    )
    if not separation_rule_review_ok:
        issues.append("separation_rule_review_gap")

    boundary_drift_rows = []
    for fname in GRANT_OWNER_APPROVAL_DRYRUN_ARTIFACTS:
        if not fname.endswith(".json"):
            continue
        doc = _read_json(dryrun / fname)
        runtime_leak = any(doc.get(flag) is True for flag in RUNTIME_FORBIDDEN_FLAGS)
        scope_leak = doc.get("scope") in FORBIDDEN_SCOPE_CLASSIFICATIONS or doc.get("classification") in FORBIDDEN_SCOPE_CLASSIFICATIONS
        boundary_drift_rows.append(
            {
                "artifact": fname,
                "runtime_scope_leak_absent": not runtime_leak,
                "post_review_added_runtime": False,
                "scope_classification": POST_REVIEW_SCOPE,
                "scope_escalation_absent": not scope_leak,
            }
        )
        if runtime_leak:
            issues.append(f"runtime_scope_leakage:{fname}")
        if scope_leak:
            issues.append(f"scope_escalation:{fname}")

    chain_evidence = []
    for stage in CHAIN_TRACE_NODES:
        row = next((r for r in trace_matrix.get("rows") or [] if r.get("stage") == stage), {})
        chain_evidence.append({"stage": stage, "linked": row.get("linked") is True})
    chain_evidence.append(
        {
            "stage": "freeze_authorization_grant_owner_approval_post_dryrun_review",
            "root": str(out),
            "readiness": POST_REVIEW_SCOPE,
            "authorization_request_issued": False,
            "request_record": False,
            "owner_approval_record": False,
            "owner_operator_ack_record": False,
            "grant_issued": False,
            "linked": True,
        }
    )
    evidence_chain_review_ok = owner_approval_dryrun_result_accepted and all(
        node.get("linked") is True for node in chain_evidence
    )
    if not evidence_chain_review_ok:
        issues.append("evidence_chain_gap")

    freeze_status = candidate_val.get("freeze_status") or "freeze-candidate"
    candidate_state_preserved = (
        candidate_val.get("owner_approval_candidate_preserved") is True
        and candidate_val.get("approval_status") == "owner-approval-candidate"
        and candidate_val.get("approval_status") != "owner-approval-record"
    )
    owner_operator_ack_candidate_preserved = ack_val.get("owner_operator_ack_candidate_preserved") is True
    approval_evidence_binding_candidate_preserved = (
        evidence_val.get("approval_evidence_binding_candidate_preserved") is True
        and evidence_val.get("binding_status") == "approval-evidence-binding-candidate"
        and evidence_val.get("binding_status") != "approval-evidence-bound-record"
    )
    request_record_binding_candidate_preserved = (
        record_binding_val.get("request_record_binding_candidate_preserved") is True
        and record_binding_val.get("binding_status") == "request-record-binding-candidate"
    )
    approval_lifecycle_candidate_preserved = (
        lifecycle_val.get("approval_lifecycle_candidate_preserved") is True
        and lifecycle_val.get("lifecycle_type") == "candidate-lifecycle"
        and lifecycle_val.get("lifecycle_type") != "active-approval-lifecycle"
    )
    expiry_revocation_reference_candidate_preserved = (
        expiry_revocation_val.get("expiry_revocation_reference_candidate_preserved") is True
        and expiry_revocation_val.get("reference_status") == "expiry-revocation-reference-candidate"
        and expiry_revocation_val.get("reference_status") not in ("expiry-execution-path", "revocation-execution-path")
    )
    post_review_scope_ok = POST_REVIEW_SCOPE not in FORBIDDEN_SCOPE_CLASSIFICATIONS
    if (
        not candidate_state_preserved
        or not owner_operator_ack_candidate_preserved
        or not approval_evidence_binding_candidate_preserved
        or not request_record_binding_candidate_preserved
        or not approval_lifecycle_candidate_preserved
        or not expiry_revocation_reference_candidate_preserved
    ):
        issues.append("approval_scope_escalation")
    if not post_review_scope_ok:
        issues.append("scope_escalation")

    authorization_request_issued = boundary_val.get("authorization_request_issued") is True
    authorization_request_absent = absence_val.get("authorization_request_absent") is True
    request_record_absent = absence_val.get("request_record_absent") is True
    owner_approval_record_absent = absence_val.get("owner_approval_record_absent") is True
    owner_operator_ack_record_absent = absence_val.get("owner_operator_ack_record_absent") is True
    approval_evidence_bound_record_absent = absence_val.get("approval_evidence_bound_record_absent") is True
    authorization_grant_absent = absence_val.get("authorization_grant_absent") is True
    grant_token_absent = absence_val.get("grant_token_absent") is True
    grant_record_absent = absence_val.get("grant_record_absent") is True
    no_freeze_execution_path = absence_val.get("no_freeze_execution_path") is True
    no_rollback_execution_path = absence_val.get("no_rollback_execution_path") is True
    no_revocation_execution_path = absence_val.get("no_approval_revocation_execution_path") is True
    absence_review_ok = (
        not authorization_request_issued
        and authorization_request_absent
        and request_record_absent
        and owner_approval_record_absent
        and owner_operator_ack_record_absent
        and approval_evidence_bound_record_absent
        and authorization_grant_absent
        and grant_token_absent
        and grant_record_absent
        and no_freeze_execution_path
        and no_rollback_execution_path
        and no_revocation_execution_path
    )
    foundation_not_frozen = boundary_val.get("foundation_frozen") is False
    closure_not_executed = boundary_val.get("closed") is False
    non_execution_boundary_ok = boundary_val.get("owner_approval_dryrun_only") is True
    if freeze_status in ("frozen", "foundation-frozen"):
        foundation_not_frozen = False
    if authorization_request_issued:
        issues.append("authorization_request_issued_leakage")
    if not absence_review_ok:
        issues.append("owner_approval_record_leakage")
    if not foundation_not_frozen:
        issues.append("freeze_state_escalation")
    if not closure_not_executed:
        issues.append("closure_state_escalation")
    if not non_execution_boundary_ok:
        issues.append("runtime_scope_leakage")

    dryrun_debts = debt_val.get("debts") or []
    debts = list(GOVERNANCE_DEBTS)
    for dd in dryrun_debts:
        for i, cd in enumerate(debts):
            if cd.get("debt_title") == dd.get("debt_title"):
                debts[i] = {**cd, **dd}
    required_titles = [d["debt_title"] for d in GOVERNANCE_DEBTS]
    debt_rows: List[Dict[str, Any]] = []
    governance_debt_preserved = len(debts) >= len(GOVERNANCE_DEBTS)
    for title in required_titles:
        match = next((d for d in debts if d.get("debt_title") == title), {})
        ok = (
            bool(match)
            and match.get("priority") == "P1"
            and match.get("classification") == "L1 Midplatform System Protocols"
            and match.get("must_not_implement_now") is True
        )
        debt_rows.append(
            {
                "debt_title": title,
                "preserved": ok,
                "priority": match.get("priority"),
                "must_not_implement_now": match.get("must_not_implement_now"),
            }
        )
        if not ok:
            governance_debt_preserved = False
    if not governance_debt_preserved:
        issues.append("governance_debt_gap")

    l1_protocols_not_implemented = debt_val.get("l1_protocols_not_implemented") is True
    system_protocols_integration_not_implemented = debt_val.get("system_protocols_integration_not_implemented") is True
    if not l1_protocols_not_implemented or not system_protocols_integration_not_implemented:
        issues.append("l1_protocol_scope_leakage")

    boundary_drift_absent = all(
        r["runtime_scope_leak_absent"] and r.get("scope_escalation_absent", True) for r in boundary_drift_rows
    )

    template_lineage = build_template_lineage(
        base_phase="Freeze-Authorization-Grant-Request-Record-Post-DryRun-Review-v1-001",
        base_capability=GRANT_OWNER_APPROVAL_POST_REVIEW_WHITELIST_FILES[0],
        base_runner=GRANT_OWNER_APPROVAL_POST_REVIEW_WHITELIST_FILES[1],
        base_verifier=GRANT_OWNER_APPROVAL_POST_REVIEW_WHITELIST_FILES[2],
        base_go_no_go_pack=GRANT_OWNER_APPROVAL_POST_REVIEW_WHITELIST_FILES[3],
        stage_phase="Freeze-Authorization-Grant-Owner-Approval-Post-DryRun-Review-v1-001",
        stage_term_overrides=GRANT_OWNER_APPROVAL_POST_REVIEW_STAGE_TERM_OVERRIDES,
        stage_additions=GRANT_OWNER_APPROVAL_POST_REVIEW_STAGE_ADDITIONS,
        template_files=GRANT_OWNER_APPROVAL_POST_REVIEW_WHITELIST_FILES,
        repo_root=repo_root,
        upstream_review_phase="Freeze-Authorization-Grant-Owner-Approval-DryRun-v1-001",
    )
    upstream_lineage_ok = (
        dryrun_lineage.get("template_lineage_ok") is True
        and dryrun_summary.get("template_lineage_ok") is True
    )
    template_lineage_ok = template_lineage.get("template_lineage_ok") is True and upstream_lineage_ok
    if not template_lineage_ok:
        issues.append("template_lineage_gap")

    owner_approval_request_planning_ready = (
        owner_approval_dryrun_result_accepted
        and protocol_reference_review_ok
        and separation_rule_review_ok
        and boundary_drift_absent
        and evidence_chain_review_ok
        and absence_review_ok
        and candidate_state_preserved
        and owner_operator_ack_candidate_preserved
        and approval_evidence_binding_candidate_preserved
        and request_record_binding_candidate_preserved
        and approval_lifecycle_candidate_preserved
        and expiry_revocation_reference_candidate_preserved
        and foundation_not_frozen
        and closure_not_executed
        and governance_debt_preserved
        and non_execution_boundary_ok
        and post_review_readiness.get("post_review_readiness_ok") is True
        and template_lineage_ok
    )
    next_phase_readiness_ok = owner_approval_request_planning_ready

    if not owner_approval_dryrun_result_accepted:
        final_decision = FINAL_DECISION_EVIDENCE
    elif not template_lineage_ok:
        final_decision = FINAL_DECISION_LINEAGE
    elif not protocol_reference_review_ok:
        final_decision = FINAL_DECISION_PROTOCOL
    elif not governance_debt_preserved:
        final_decision = FINAL_DECISION_DEBT
    elif not l1_protocols_not_implemented or not system_protocols_integration_not_implemented:
        final_decision = FINAL_DECISION_L1
    elif not boundary_drift_absent or not non_execution_boundary_ok:
        final_decision = FINAL_DECISION_BOUNDARY if not boundary_drift_absent else FINAL_DECISION_RUNTIME
    elif authorization_request_issued:
        final_decision = FINAL_DECISION_REQUEST
    elif not absence_review_ok:
        final_decision = FINAL_DECISION_APPROVAL
    elif (
        not foundation_not_frozen
        or not candidate_state_preserved
        or not owner_operator_ack_candidate_preserved
        or not approval_evidence_binding_candidate_preserved
        or not request_record_binding_candidate_preserved
        or not approval_lifecycle_candidate_preserved
        or not expiry_revocation_reference_candidate_preserved
    ):
        final_decision = FINAL_DECISION_FREEZE
    else:
        final_decision = FINAL_DECISION_GO

    go_condition_values = {
        "prior_owner_approval_dryrun_go": prior_owner_approval_dryrun_go,
        "owner_approval_dryrun_result_accepted": owner_approval_dryrun_result_accepted,
        "protocol_reference_review_ok": protocol_reference_review_ok,
        "separation_rule_review_ok": separation_rule_review_ok,
        "candidate_state_preserved": candidate_state_preserved,
        "owner_operator_ack_candidate_preserved": owner_operator_ack_candidate_preserved,
        "approval_evidence_binding_candidate_preserved": approval_evidence_binding_candidate_preserved,
        "request_record_binding_candidate_preserved": request_record_binding_candidate_preserved,
        "approval_lifecycle_candidate_preserved": approval_lifecycle_candidate_preserved,
        "expiry_revocation_reference_candidate_preserved": expiry_revocation_reference_candidate_preserved,
        "absence_review_ok": absence_review_ok,
        "boundary_drift_absent": boundary_drift_absent,
        "evidence_chain_review_ok": evidence_chain_review_ok,
        "governance_debt_preserved": governance_debt_preserved,
        "template_lineage_ok": template_lineage_ok,
        "post_review_only": True,
        "non_execution_boundary_ok": non_execution_boundary_ok,
        "next_phase_readiness_ok": next_phase_readiness_ok,
    }
    review_pass = len(issues) == 0 and final_decision == FINAL_DECISION_GO and all(go_condition_values.values())
    next_phase = NEXT_PHASE_GO if review_pass else NEXT_PHASE_HOLD
    core_schema_fields = build_core_go_no_go_summary_fields(
        go_conditions=go_condition_values,
        forbidden_runtime_flags=RUNTIME_FORBIDDEN_FLAGS,
        chain_trace_nodes=CHAIN_EVIDENCE_NODES,
        go_no_go_decision=final_decision,
        final_decision=final_decision,
        next_phase=next_phase,
        template_lineage=template_lineage,
    )

    review_report = {
        "review_id": "task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_post_dryrun_review_v1",
        **go_condition_values,
        "authorization_request_issued": authorization_request_issued,
        "owner_approval_request_planning_ready": owner_approval_request_planning_ready,
        "post_review_scope": POST_REVIEW_SCOPE,
        "final_decision": final_decision,
        "recommended_next_phase": next_phase,
        **meta,
    }
    dryrun_result_review = {
        "review_id": "task_manager_freeze_authorization_grant_owner_approval_dryrun_result_review_v1",
        "rows": review_rows,
        "prior_owner_approval_dryrun_go": prior_owner_approval_dryrun_go,
        "owner_approval_dryrun_result_accepted": owner_approval_dryrun_result_accepted,
        "dryrun_final_decision": dryrun_summary.get("final_decision"),
        "dryrun_recommended_next_phase": dryrun_summary.get("recommended_next_phase"),
        **meta,
    }
    protocol_reference_review = {
        "review_id": "task_manager_freeze_authorization_grant_owner_approval_protocol_reference_review_v1",
        "source_validation_id": protocol_val.get("validation_id"),
        "protocol_standard_ref": PROTOCOL_STANDARD_REF,
        "protocol_id": PROTOCOL_ID,
        "related_protocol_ids": list(RELATED_PROTOCOL_IDS),
        "error_namespace": ERROR_NAMESPACE,
        "protocol_execution_result_schema_ref": PROTOCOL_EXECUTION_RESULT_SCHEMA_REF,
        "separation_rule_ref": SEPARATION_RULE_REF,
        "shared_protocol_system_revalidation": False,
        "protocol_reference_review_ok": protocol_reference_review_ok,
        "protocol_standard_reference_ok": protocol_val.get("protocol_standard_reference_ok") is True,
        "protocol_id_reference_ok": protocol_val.get("protocol_id_reference_ok") is True,
        "error_namespace_reference_ok": protocol_val.get("error_namespace_reference_ok") is True,
        "protocol_execution_result_schema_ref_ok": protocol_val.get("protocol_execution_result_schema_ref_ok") is True,
        "separation_rule_ref_ok": protocol_val.get("separation_rule_ref_ok") is True,
        "protocol_error_code_light_check_ok": protocol_val.get("protocol_error_code_light_check_ok") is True,
        "whitebox_candidate_ref_ok": protocol_val.get("whitebox_candidate_ref_ok") is True,
        "sample_protocol_error_code": protocol_val.get("sample_protocol_error_code"),
        "whitebox_candidate_ref": protocol_val.get("whitebox_candidate_ref"),
        "protocol_violation_examples": protocol_val.get("protocol_violation_examples") or [],
        **meta,
    }
    separation_rule_review = {
        "review_id": "task_manager_freeze_authorization_grant_owner_approval_separation_rule_review_v1",
        "separation_rule_ref": SEPARATION_RULE_REF,
        "separation_rule_review_ok": separation_rule_review_ok,
        "error_classification_rules": list(FAILURE_CLASSIFICATION),
        "upstream_error_classification_rules": protocol_val.get("error_classification_rules") or [],
        "module_local_failure_not_protocol_failure_by_default": (
            protocol_val.get("module_local_failure_not_protocol_failure_by_default") is True
        ),
        **meta,
    }
    candidate_state_review = {
        "review_id": "task_manager_freeze_authorization_grant_owner_approval_candidate_state_review_v1",
        "rows": candidate_val.get("rows") or [],
        "freeze_status": freeze_status,
        "candidate_state_preserved": candidate_state_preserved,
        "approval_status": "owner-approval-candidate",
        **meta,
    }
    owner_operator_ack_candidate_state_review = {
        "review_id": "task_manager_freeze_authorization_grant_owner_operator_ack_candidate_state_review_v1",
        "rows": ack_val.get("rows") or [],
        "owner_operator_ack_candidate_preserved": owner_operator_ack_candidate_preserved,
        "ack_status": "owner-operator-ack-candidate",
        **meta,
    }
    evidence_binding_review = {
        "review_id": "task_manager_freeze_authorization_grant_owner_approval_evidence_binding_review_v1",
        "rows": evidence_val.get("rows") or [],
        "approval_evidence_binding_candidate_preserved": approval_evidence_binding_candidate_preserved,
        "binding_status": "approval-evidence-binding-candidate",
        "approval_evidence_bound_record_absent": approval_evidence_bound_record_absent,
        **meta,
    }
    request_record_binding_review = {
        "review_id": "task_manager_freeze_authorization_grant_owner_approval_request_record_binding_review_v1",
        "rows": record_binding_val.get("rows") or [],
        "request_record_binding_candidate_preserved": request_record_binding_candidate_preserved,
        "binding_status": "request-record-binding-candidate",
        "request_record_absent": request_record_absent,
        **meta,
    }
    lifecycle_review = {
        "review_id": "task_manager_freeze_authorization_grant_owner_approval_lifecycle_review_v1",
        "rows": lifecycle_val.get("rows") or [],
        "approval_lifecycle_candidate_preserved": approval_lifecycle_candidate_preserved,
        "lifecycle_type": "candidate-lifecycle",
        **meta,
    }
    expiry_revocation_review = {
        "review_id": "task_manager_freeze_authorization_grant_owner_approval_expiry_revocation_review_v1",
        "rows": expiry_revocation_val.get("rows") or [],
        "expiry_revocation_reference_candidate_preserved": expiry_revocation_reference_candidate_preserved,
        "reference_status": "expiry-revocation-reference-candidate",
        "no_revocation_execution_path": no_revocation_execution_path,
        **meta,
    }
    absence_review = {
        "review_id": "task_manager_freeze_authorization_grant_owner_approval_absence_review_v1",
        "absence_review_ok": absence_review_ok,
        "authorization_request_issued": authorization_request_issued,
        "authorization_request_absent": authorization_request_absent,
        "request_record_absent": request_record_absent,
        "owner_approval_record_absent": owner_approval_record_absent,
        "owner_operator_ack_record_absent": owner_operator_ack_record_absent,
        "approval_evidence_bound_record_absent": approval_evidence_bound_record_absent,
        "authorization_grant_absent": authorization_grant_absent,
        "grant_token_absent": grant_token_absent,
        "grant_record_absent": grant_record_absent,
        "no_freeze_execution_path": no_freeze_execution_path,
        "no_rollback_execution_path": no_rollback_execution_path,
        "no_revocation_execution_path": no_revocation_execution_path,
        **meta,
    }
    boundary_drift_review = {
        "review_id": "task_manager_freeze_authorization_grant_owner_approval_boundary_drift_review_v1",
        "rows": boundary_drift_rows,
        "boundary_drift_absent": boundary_drift_absent,
        "boundary_statements": list(POST_REVIEW_BOUNDARY_STATEMENTS),
        "upstream_boundary_statements": list(DRYRUN_BOUNDARY_STATEMENTS),
        "post_review_scope": POST_REVIEW_SCOPE,
        "forbidden_scope_classifications": list(FORBIDDEN_SCOPE_CLASSIFICATIONS),
        **meta,
    }
    evidence_chain_review = {
        "review_id": "task_manager_freeze_authorization_grant_owner_approval_evidence_chain_review_v1",
        "chain": chain_evidence,
        "node_count": len(CHAIN_EVIDENCE_NODES),
        "evidence_chain_review_ok": evidence_chain_review_ok,
        "freeze_authorization_chain_evidence_accepted": evidence_chain_review_ok,
        **meta,
    }
    governance_debt_review = {
        "review_id": "task_manager_freeze_authorization_grant_owner_approval_governance_debt_review_v1",
        "debts": debts,
        "debt_rows": debt_rows,
        "required_debt_count": len(GOVERNANCE_DEBTS),
        "governance_debt_preserved": governance_debt_preserved,
        "l1_protocols_not_implemented": l1_protocols_not_implemented,
        "system_protocols_integration_not_implemented": system_protocols_integration_not_implemented,
        **meta,
    }
    template_lineage_doc = {
        "lineage_id": "task_manager_freeze_authorization_grant_owner_approval_template_lineage_v1",
        "upstream_owner_approval_dryrun_lineage_ok": upstream_lineage_ok,
        **template_lineage,
        **meta,
    }
    next_phase_readiness = {
        "readiness_id": "task_manager_freeze_authorization_grant_owner_approval_next_phase_readiness_v1",
        "next_phase_readiness_ok": next_phase_readiness_ok,
        "owner_approval_request_planning_ready": owner_approval_request_planning_ready,
        "recommended_next_phase": next_phase,
        "candidates": [
            {
                "phase": NEXT_PHASE_GO,
                "readiness": "freeze-authorization-grant-owner-approval-request-planning-ready",
                "authorization_request_issued": False,
                "request_record_created": False,
                "owner_approval_record_created": False,
                "owner_operator_ack_record_created": False,
                "approval_evidence_bound_record_created": False,
                "grant_issued": False,
                "foundation_frozen": False,
                "closed": False,
            },
            {
                "phase": NEXT_PHASE_ALT,
                "readiness": "freeze-authorization-grant-owner-approval-issuance-planning-ready",
                "authorization_request_issued": False,
                "request_record_created": False,
                "owner_approval_record_created": False,
                "owner_operator_ack_record_created": False,
                "approval_evidence_bound_record_created": False,
                "grant_issued": False,
                "foundation_frozen": False,
                "closed": False,
            },
        ],
        "module_adapter_implementation_ready": False,
        "authorization_request_issued": False,
        "request_record_created": False,
        "owner_approval_record_created": False,
        "owner_operator_ack_record_created": False,
        "approval_evidence_bound_record_created": False,
        "grant_issued": False,
        "freeze_authorization_granted": False,
        "foundation_frozen": False,
        "closed": False,
        **meta,
    }
    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "post_dryrun_review_pass": review_pass,
        "blocker_count": len(issues),
        "issues": issues,
        **go_condition_values,
        **core_schema_fields,
        **meta,
    }
    markdown = "\n".join(
        [
            "# Task Manager Foundation Handoff Freeze Authorization Grant Owner Approval Post-DryRun Review v1",
            "",
            "This phase reviews freeze authorization grant owner approval dry-run results only. "
            "It does not create owner approval records, owner/operator ack records, bind approval evidence records, "
            "create request records, or issue authorization requests.",
            "",
            "本阶段仅审查 freeze authorization grant owner approval dry-run 结果，"
            "不生成 owner approval record，不生成 owner/operator ack record，"
            "不绑定 approval evidence record，不生成 request record，不发起 authorization request，不签发 grant。",
            "",
            f"Prior owner approval dry-run GO: `{prior_owner_approval_dryrun_go}`",
            f"Owner approval dry-run accepted: `{owner_approval_dryrun_result_accepted}`",
            f"Protocol reference review OK: `{protocol_reference_review_ok}`",
            f"Separation rule review OK: `{separation_rule_review_ok}`",
            f"Absence review OK: `{absence_review_ok}`",
            f"Owner approval record absent: `{owner_approval_record_absent}`",
            f"Owner/operator ack record absent: `{owner_operator_ack_record_absent}`",
            f"Approval evidence bound record absent: `{approval_evidence_bound_record_absent}`",
            f"Request record absent: `{request_record_absent}`",
            f"Grant token absent: `{grant_token_absent}`",
            f"Grant record absent: `{grant_record_absent}`",
            f"Owner approval request planning ready: `{owner_approval_request_planning_ready}` "
            "(owner approval post-dryrun review ≠ owner approval)",
            f"Template lineage OK: `{template_lineage_ok}`",
            f"Post-review scope: `{POST_REVIEW_SCOPE}`",
            f"Shared protocol system revalidation: `false`",
            f"Freeze status: `freeze-candidate` (not frozen)",
            f"Final decision: `{final_decision}`",
            f"Recommended next phase: `{next_phase}`",
            "",
            "## Owner Approval Post-Review Boundary Statements",
            *[f"- {stmt}" for stmt in POST_REVIEW_BOUNDARY_STATEMENTS],
            "",
            "owner approval post-dryrun review ≠ owner approval",
            "",
            "## Governance Debts (P1, not implemented)",
            *[f"- {d['debt_title']}" for d in GOVERNANCE_DEBTS],
        ]
    )
    return {
        "task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_post_dryrun_review_report": review_report,
        "task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_post_dryrun_review_md": markdown,
        "task_manager_freeze_authorization_grant_owner_approval_dryrun_result_review": dryrun_result_review,
        "task_manager_freeze_authorization_grant_owner_approval_protocol_reference_review": protocol_reference_review,
        "task_manager_freeze_authorization_grant_owner_approval_separation_rule_review": separation_rule_review,
        "task_manager_freeze_authorization_grant_owner_approval_candidate_state_review": candidate_state_review,
        "task_manager_freeze_authorization_grant_owner_operator_ack_candidate_state_review": owner_operator_ack_candidate_state_review,
        "task_manager_freeze_authorization_grant_owner_approval_evidence_binding_review": evidence_binding_review,
        "task_manager_freeze_authorization_grant_owner_approval_request_record_binding_review": request_record_binding_review,
        "task_manager_freeze_authorization_grant_owner_approval_lifecycle_review": lifecycle_review,
        "task_manager_freeze_authorization_grant_owner_approval_expiry_revocation_review": expiry_revocation_review,
        "task_manager_freeze_authorization_grant_owner_approval_absence_review": absence_review,
        "task_manager_freeze_authorization_grant_owner_approval_boundary_drift_review": boundary_drift_review,
        "task_manager_freeze_authorization_grant_owner_approval_evidence_chain_review": evidence_chain_review,
        "task_manager_freeze_authorization_grant_owner_approval_governance_debt_review": governance_debt_review,
        "task_manager_freeze_authorization_grant_owner_approval_template_lineage": template_lineage_doc,
        "task_manager_freeze_authorization_grant_owner_approval_next_phase_readiness": next_phase_readiness,
        "summary": summary,
    }
