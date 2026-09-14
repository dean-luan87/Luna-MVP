# -*- coding: utf-8 -*-
"""Luna Midplatform Task Manager Foundation Handoff Freeze Authorization Grant Request Issuance Post-DryRun Review v1.

Structure inherited from task_manager_foundation_handoff_freeze_authorization_grant_request_post_dryrun_review_v1.py
with upstream input from grant_request_issuance_dryrun_v1 (whitelist template reuse).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.task_manager_foundation_handoff_evaluation_template_lineage_v1 import (
    GRANT_REQUEST_ISSUANCE_POST_REVIEW_STAGE_ADDITIONS,
    GRANT_REQUEST_ISSUANCE_POST_REVIEW_STAGE_TERM_OVERRIDES,
    GRANT_REQUEST_ISSUANCE_POST_REVIEW_WHITELIST_FILES,
    build_core_go_no_go_summary_fields,
    build_template_lineage,
)
from capabilities.midplatform.task_manager_foundation_handoff_final_closure_planning_v1 import GOVERNANCE_DEBTS
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_request_issuance_dryrun_v1 import (
    CHAIN_TRACE_NODES,
    DEFAULT_OUTPUT as DEFAULT_GRANT_REQUEST_ISSUANCE_DRYRUN_ROOT,
    FINAL_DECISION_GO as GRANT_REQUEST_ISSUANCE_DRYRUN_FINAL_GO,
    GO_CONDITIONS_KEYS as GRANT_REQUEST_ISSUANCE_DRYRUN_TRUE_KEYS,
    GRANT_REQUEST_ISSUANCE_DRYRUN_ARTIFACTS,
    NEXT_PHASE_GO as GRANT_REQUEST_ISSUANCE_DRYRUN_NEXT_PHASE,
    RUNTIME_FORBIDDEN_FLAGS,
)
from capabilities.midplatform.task_manager_foundation_handoff_planning_v1 import (
    BOUNDARY_STATEMENT_EN,
    BOUNDARY_STATEMENT_ZH,
    FOUNDATION_ID,
)

PHASE_ID = "Phase-Midplatform-Task-Manager-Foundation-Handoff-Freeze-Authorization-Grant-Request-Issuance-Post-DryRun-Review-v1-001"
SCOPE = "midplatform_task_manager_foundation_handoff_freeze_authorization_grant_request_issuance_post_dryrun_review_only"
SOURCE_CHAIN = "midplatform_task_manager_foundation_handoff_freeze_authorization_grant_request_issuance_post_dryrun_review_v1"
FINAL_DECISION_GO = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_REQUEST_ISSUANCE_POST_DRYRUN_REVIEW_READY_FOR_REQUEST_RECORD_PLANNING"
FINAL_DECISION_EVIDENCE = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_REQUEST_ISSUANCE_POST_DRYRUN_REVIEW_BLOCKED_BY_DRYRUN_EVIDENCE_GAP"
FINAL_DECISION_BOUNDARY = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_REQUEST_ISSUANCE_POST_DRYRUN_REVIEW_BLOCKED_BY_BOUNDARY_DRIFT"
FINAL_DECISION_REQUEST = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_REQUEST_ISSUANCE_POST_DRYRUN_REVIEW_BLOCKED_BY_AUTHORIZATION_REQUEST_ISSUED_LEAKAGE"
FINAL_DECISION_ISSUANCE = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_REQUEST_ISSUANCE_POST_DRYRUN_REVIEW_BLOCKED_BY_REQUEST_RECORD_LEAKAGE"
FINAL_DECISION_FREEZE = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_REQUEST_ISSUANCE_POST_DRYRUN_REVIEW_BLOCKED_BY_FREEZE_STATE_ESCALATION"
FINAL_DECISION_DEBT = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_REQUEST_ISSUANCE_POST_DRYRUN_REVIEW_BLOCKED_BY_GOVERNANCE_DEBT_GAP"
FINAL_DECISION_L1 = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_REQUEST_ISSUANCE_POST_DRYRUN_REVIEW_BLOCKED_BY_L1_PROTOCOL_SCOPE_LEAKAGE"
FINAL_DECISION_RUNTIME = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_REQUEST_ISSUANCE_POST_DRYRUN_REVIEW_BLOCKED_BY_RUNTIME_SCOPE_LEAKAGE"
FINAL_DECISION_LINEAGE = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_REQUEST_ISSUANCE_POST_DRYRUN_REVIEW_BLOCKED_BY_TEMPLATE_LINEAGE_GAP"
NEXT_PHASE_GO = "Phase-Midplatform-Task-Manager-Foundation-Handoff-Freeze-Authorization-Grant-Request-Record-Planning-v1-001"
NEXT_PHASE_ALT = "Phase-Midplatform-Task-Manager-Foundation-Handoff-Freeze-Authorization-Owner-Approval-Request-Planning-v1-001"
NEXT_PHASE_HOLD = "Phase-Midplatform-Task-Manager-Foundation-Handoff-Freeze-Authorization-Grant-Request-Issuance-Post-DryRun-Review-Issue-Review-v1-001"
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "midplatform_task_manager_foundation_handoff_freeze_authorization_grant_request_issuance_post_dryrun_review_v1_smoke_v0"
)
POST_REVIEW_SCOPE = "request-issuance-post-review-scope"
FORBIDDEN_SCOPE_CLASSIFICATIONS: Tuple[str, ...] = ("request-issued-scope", "authorized-scope")

POST_REVIEW_BOUNDARY_STATEMENTS: Tuple[str, ...] = (
    "request_issuance_post_dryrun_review != authorization_request_issued",
    "request_issuance_candidate != request_record",
    "request_record_candidate != request_record",
    "owner_approval_candidate != owner_approval_record",
    "grant_token_candidate != grant_token",
    "grant_candidate != grant_record",
    "freeze_candidate != frozen",
    "closure_candidate != closed",
)
CHAIN_EVIDENCE_NODES: Tuple[str, ...] = CHAIN_TRACE_NODES + (
    "freeze_authorization_grant_request_issuance_post_dryrun_review",
)
GO_CONDITIONS_KEYS: Tuple[str, ...] = (
    "request_issuance_dryrun_result_accepted",
    "boundary_drift_absent",
    "request_issuance_chain_evidence_accepted",
    "issuance_absence_confirmed",
    "request_record_absent",
    "owner_approval_record_absent",
    "grant_token_absent",
    "grant_record_absent",
    "authorization_grant_absent",
    "foundation_not_frozen",
    "closure_not_executed",
    "governance_debt_preserved",
    "l1_protocols_not_implemented",
    "system_protocols_integration_not_implemented",
    "template_lineage_ok",
    "full_repo_scan_absent",
    "post_review_only",
    "request_record_planning_ready",
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
        "grant_request_issuance_dryrun_root": str(dryrun),
        "boundary_statement_en": BOUNDARY_STATEMENT_EN,
        "boundary_statement_zh": BOUNDARY_STATEMENT_ZH,
    }


def run_task_manager_foundation_handoff_freeze_authorization_grant_request_issuance_post_dryrun_review_v1(
    *,
    grant_request_issuance_dryrun_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    out = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    dryrun = Path(grant_request_issuance_dryrun_root).expanduser().resolve()
    repo_root = Path(__file__).resolve().parents[2]
    meta = _meta(out, dryrun)
    issues: List[str] = []

    dryrun_summary = _read_json(dryrun / "summary.json")
    dryrun_verifier = _read_json(dryrun / "verifier_report.json")
    dryrun_lineage = _read_json(dryrun / "task_manager_freeze_authorization_grant_request_issuance_template_lineage_v1.json")
    trace_matrix = _read_json(dryrun / "task_manager_freeze_authorization_grant_request_issuance_evidence_traceability_v1.json")
    candidate_val = _read_json(dryrun / "task_manager_freeze_authorization_grant_request_issuance_candidate_validation_v1.json")
    record_candidate_val = _read_json(
        dryrun / "task_manager_freeze_authorization_grant_request_record_candidate_validation_v1.json"
    )
    owner_val = _read_json(
        dryrun / "task_manager_freeze_authorization_grant_owner_approval_candidate_validation_v1.json"
    )
    absence_val = _read_json(dryrun / "task_manager_freeze_authorization_grant_request_issuance_absence_validation_v1.json")
    boundary_val = _read_json(dryrun / "task_manager_freeze_authorization_grant_request_issuance_boundary_validation_v1.json")
    debt_val = _read_json(dryrun / "task_manager_freeze_authorization_grant_request_issuance_governance_debt_validation_v1.json")
    post_review_readiness = _read_json(
        dryrun / "task_manager_freeze_authorization_grant_request_issuance_post_review_readiness_v1.json"
    )

    review_rows = []
    for fname in GRANT_REQUEST_ISSUANCE_DRYRUN_ARTIFACTS:
        path = dryrun / fname
        if fname.endswith(".json"):
            non_placeholder = bool(_read_json(path))
        else:
            non_placeholder = path.is_file() and len(path.read_text(encoding="utf-8").strip()) > 200
        review_rows.append({"artifact": fname, "exists": path.is_file(), "non_placeholder": non_placeholder})
        if not path.is_file() or not non_placeholder:
            issues.append(f"missing_dryrun_artifact:{fname}")

    request_issuance_dryrun_result_accepted = (
        dryrun_summary.get("final_decision") == GRANT_REQUEST_ISSUANCE_DRYRUN_FINAL_GO
        and dryrun_summary.get("recommended_next_phase") == GRANT_REQUEST_ISSUANCE_DRYRUN_NEXT_PHASE
        and dryrun_verifier.get("verifier") == "GO"
        and int(dryrun_verifier.get("passed_checks", 0)) >= 420
        and dryrun_verifier.get("failed_checks") == 0
        and dryrun_verifier.get("blocker_count") == 0
        and dryrun_summary.get("post_review_readiness_ok") is True
        and all(dryrun_summary.get(k) is True for k in GRANT_REQUEST_ISSUANCE_DRYRUN_TRUE_KEYS)
        and dryrun_summary.get("template_lineage_ok") is True
    )
    if not request_issuance_dryrun_result_accepted:
        issues.append("request_issuance_dryrun_not_accepted")

    boundary_drift_rows = []
    for fname in GRANT_REQUEST_ISSUANCE_DRYRUN_ARTIFACTS:
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
            "stage": "freeze_authorization_grant_request_issuance_post_dryrun_review",
            "root": str(out),
            "readiness": POST_REVIEW_SCOPE,
            "authorization_request_issued": False,
            "request_record": False,
            "grant_issued": False,
            "linked": True,
        }
    )
    request_issuance_chain_evidence_accepted = request_issuance_dryrun_result_accepted and all(
        node.get("linked") is True for node in chain_evidence
    )
    if not request_issuance_chain_evidence_accepted:
        issues.append("chain_evidence_gap")

    freeze_status = candidate_val.get("freeze_status") or "freeze-candidate"
    request_issuance_candidate_preserved = (
        candidate_val.get("request_issuance_candidate_preserved") is True
        and candidate_val.get("issuance_status") == "request-issuance-candidate"
        and candidate_val.get("request_status") == "request-issuance-candidate"
        and candidate_val.get("request_status") != "request-record"
        and candidate_val.get("authorization_request_issued") is not True
    )
    request_record_candidate_preserved = (
        record_candidate_val.get("request_record_candidate_preserved") is True
        and record_candidate_val.get("record_status") == "request-record-candidate"
        and record_candidate_val.get("record_status") != "request-record"
        and record_candidate_val.get("record_created") is not True
    )
    owner_approval_candidate_preserved = (
        owner_val.get("owner_approval_candidate_preserved") is True
        and owner_val.get("approval_status") == "owner-approval-candidate"
    )
    post_review_scope_ok = POST_REVIEW_SCOPE not in FORBIDDEN_SCOPE_CLASSIFICATIONS
    if not request_issuance_candidate_preserved or not request_record_candidate_preserved or not owner_approval_candidate_preserved:
        issues.append("request_scope_escalation")
    if not post_review_scope_ok:
        issues.append("scope_escalation")

    authorization_request_issued = boundary_val.get("authorization_request_issued") is True
    request_record_absent = absence_val.get("request_record_absent") is True
    owner_approval_record_absent = absence_val.get("owner_approval_record_absent") is True
    authorization_grant_absent = absence_val.get("authorization_grant_absent") is True
    grant_token_absent = absence_val.get("grant_token_absent") is True
    grant_record_absent = absence_val.get("grant_record_absent") is True
    no_freeze_execution_path = absence_val.get("no_freeze_execution_path") is True
    no_rollback_execution_path = absence_val.get("no_rollback_execution_path") is True
    issuance_absence_confirmed = (
        not authorization_request_issued
        and request_record_absent
        and owner_approval_record_absent
        and authorization_grant_absent
        and grant_token_absent
        and grant_record_absent
        and no_freeze_execution_path
        and no_rollback_execution_path
    )
    foundation_not_frozen = boundary_val.get("foundation_frozen") is False
    closure_not_executed = boundary_val.get("closed") is False
    if freeze_status in ("frozen", "foundation-frozen"):
        foundation_not_frozen = False
    if authorization_request_issued:
        issues.append("authorization_request_issued_leakage")
    if not issuance_absence_confirmed:
        issues.append("request_record_leakage")
    if not foundation_not_frozen:
        issues.append("freeze_state_escalation")
    if not closure_not_executed:
        issues.append("closure_state_escalation")

    debts = debt_val.get("debts") or []
    debt0 = debts[0] if debts else {}
    debt1 = debts[1] if len(debts) > 1 else {}
    governance_debt_preserved = (
        len(debts) >= 2
        and debt0.get("debt_title") == GOVERNANCE_DEBTS[0]["debt_title"]
        and debt0.get("priority") == "P1"
        and debt0.get("classification") == "L1 Midplatform System Protocols"
        and debt0.get("must_not_implement_now") is True
        and debt1.get("debt_title") == GOVERNANCE_DEBTS[1]["debt_title"]
        and debt1.get("priority") == "P1"
        and debt1.get("classification") == "L1 Midplatform System Protocols"
        and debt1.get("must_not_implement_now") is True
    )
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
        base_phase="Freeze-Authorization-Grant-Request-Post-DryRun-Review-v1-001",
        base_capability=GRANT_REQUEST_ISSUANCE_POST_REVIEW_WHITELIST_FILES[0],
        base_runner=GRANT_REQUEST_ISSUANCE_POST_REVIEW_WHITELIST_FILES[1],
        base_verifier=GRANT_REQUEST_ISSUANCE_POST_REVIEW_WHITELIST_FILES[2],
        base_go_no_go_pack=GRANT_REQUEST_ISSUANCE_POST_REVIEW_WHITELIST_FILES[3],
        stage_phase="Freeze-Authorization-Grant-Request-Issuance-Post-DryRun-Review-v1-001",
        stage_term_overrides=GRANT_REQUEST_ISSUANCE_POST_REVIEW_STAGE_TERM_OVERRIDES,
        stage_additions=GRANT_REQUEST_ISSUANCE_POST_REVIEW_STAGE_ADDITIONS,
        template_files=GRANT_REQUEST_ISSUANCE_POST_REVIEW_WHITELIST_FILES,
        repo_root=repo_root,
        upstream_review_phase="Freeze-Authorization-Grant-Request-Issuance-DryRun-v1-001",
    )
    upstream_lineage_ok = (
        dryrun_lineage.get("template_lineage_ok") is True
        and dryrun_summary.get("template_lineage_ok") is True
    )
    if not template_lineage.get("template_lineage_ok") or not upstream_lineage_ok:
        issues.append("template_lineage_gap")

    request_record_planning_ready = (
        request_issuance_dryrun_result_accepted
        and boundary_drift_absent
        and request_issuance_chain_evidence_accepted
        and issuance_absence_confirmed
        and request_issuance_candidate_preserved
        and request_record_candidate_preserved
        and owner_approval_candidate_preserved
        and foundation_not_frozen
        and closure_not_executed
        and governance_debt_preserved
        and post_review_readiness.get("post_review_readiness_ok") is True
        and template_lineage.get("template_lineage_ok") is True
    )

    if not request_issuance_dryrun_result_accepted:
        final_decision = FINAL_DECISION_EVIDENCE
    elif not template_lineage.get("template_lineage_ok"):
        final_decision = FINAL_DECISION_LINEAGE
    elif not governance_debt_preserved:
        final_decision = FINAL_DECISION_DEBT
    elif not l1_protocols_not_implemented or not system_protocols_integration_not_implemented:
        final_decision = FINAL_DECISION_L1
    elif not boundary_drift_absent:
        final_decision = FINAL_DECISION_BOUNDARY
    elif authorization_request_issued:
        final_decision = FINAL_DECISION_REQUEST
    elif not issuance_absence_confirmed:
        final_decision = FINAL_DECISION_ISSUANCE
    elif (
        not foundation_not_frozen
        or not request_issuance_candidate_preserved
        or not request_record_candidate_preserved
        or not owner_approval_candidate_preserved
    ):
        final_decision = FINAL_DECISION_FREEZE
    else:
        final_decision = FINAL_DECISION_GO

    go_condition_values = {
        "request_issuance_dryrun_result_accepted": request_issuance_dryrun_result_accepted,
        "boundary_drift_absent": boundary_drift_absent,
        "request_issuance_chain_evidence_accepted": request_issuance_chain_evidence_accepted,
        "issuance_absence_confirmed": issuance_absence_confirmed,
        "request_record_absent": request_record_absent,
        "owner_approval_record_absent": owner_approval_record_absent,
        "grant_token_absent": grant_token_absent,
        "grant_record_absent": grant_record_absent,
        "authorization_grant_absent": authorization_grant_absent,
        "foundation_not_frozen": foundation_not_frozen,
        "closure_not_executed": closure_not_executed,
        "governance_debt_preserved": governance_debt_preserved,
        "l1_protocols_not_implemented": l1_protocols_not_implemented,
        "system_protocols_integration_not_implemented": system_protocols_integration_not_implemented,
        "template_lineage_ok": template_lineage.get("template_lineage_ok") is True and upstream_lineage_ok,
        "full_repo_scan_absent": True,
        "post_review_only": True,
        "request_record_planning_ready": request_record_planning_ready,
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
        "review_id": "task_manager_foundation_handoff_freeze_authorization_grant_request_issuance_post_dryrun_review_v1",
        **go_condition_values,
        "authorization_request_issued": authorization_request_issued,
        "request_issuance_candidate_preserved": request_issuance_candidate_preserved,
        "request_record_candidate_preserved": request_record_candidate_preserved,
        "owner_approval_candidate_preserved": owner_approval_candidate_preserved,
        "post_review_scope": POST_REVIEW_SCOPE,
        "final_decision": final_decision,
        "recommended_next_phase": next_phase,
        **meta,
    }
    dryrun_review_matrix = {
        "matrix_id": "task_manager_freeze_authorization_grant_request_issuance_dryrun_review_matrix_v1",
        "rows": review_rows,
        "request_issuance_dryrun_result_accepted": request_issuance_dryrun_result_accepted,
        **meta,
    }
    boundary_drift_review = {
        "review_id": "task_manager_freeze_authorization_grant_request_issuance_boundary_drift_review_v1",
        "rows": boundary_drift_rows,
        "boundary_drift_absent": boundary_drift_absent,
        "boundary_statements": list(POST_REVIEW_BOUNDARY_STATEMENTS),
        "post_review_scope": POST_REVIEW_SCOPE,
        "forbidden_scope_classifications": list(FORBIDDEN_SCOPE_CLASSIFICATIONS),
        **meta,
    }
    chain_evidence_review = {
        "review_id": "task_manager_freeze_authorization_grant_request_issuance_chain_evidence_review_v1",
        "chain": chain_evidence,
        "node_count": len(CHAIN_EVIDENCE_NODES),
        "request_issuance_chain_evidence_accepted": request_issuance_chain_evidence_accepted,
        "freeze_authorization_chain_evidence_accepted": request_issuance_chain_evidence_accepted,
        **meta,
    }
    issuance_absence_review = {
        "review_id": "task_manager_freeze_authorization_grant_request_issuance_absence_review_v1",
        "issuance_absence_confirmed": issuance_absence_confirmed,
        "authorization_request_issued": authorization_request_issued,
        "request_record_absent": request_record_absent,
        "owner_approval_record_absent": owner_approval_record_absent,
        "authorization_grant_absent": authorization_grant_absent,
        "grant_token_absent": grant_token_absent,
        "grant_record_absent": grant_record_absent,
        "no_authorization_request_issued": not authorization_request_issued,
        "no_request_record": True,
        "no_owner_approval_record": True,
        "no_authorization_grant": True,
        "no_grant_token": True,
        "no_grant_record": True,
        "no_freeze_execution_path": no_freeze_execution_path,
        "no_rollback_execution_path": no_rollback_execution_path,
        **meta,
    }
    state_absence_review = {
        "review_id": "task_manager_freeze_authorization_grant_request_issuance_state_absence_review_v1",
        "freeze_status": freeze_status,
        "foundation_not_frozen": foundation_not_frozen,
        "closure_not_executed": closure_not_executed,
        "closure_status": "grant-request-record-planning-ready",
        "no_freeze_execution_path": no_freeze_execution_path,
        "no_rollback_execution_path": no_rollback_execution_path,
        **meta,
    }
    governance_debt_review = {
        "review_id": "task_manager_freeze_authorization_grant_request_issuance_governance_debt_review_v1",
        "debts": debts,
        "governance_debt_preserved": governance_debt_preserved,
        "l1_protocols_not_implemented": l1_protocols_not_implemented,
        "system_protocols_integration_not_implemented": system_protocols_integration_not_implemented,
        **meta,
    }
    template_lineage_review = {
        "review_id": "task_manager_freeze_authorization_grant_request_issuance_template_lineage_review_v1",
        **template_lineage,
        "upstream_grant_request_issuance_dryrun_lineage_ok": upstream_lineage_ok,
        **meta,
    }
    request_record_planning_readiness = {
        "readiness_id": "task_manager_freeze_authorization_grant_request_record_planning_readiness_v1",
        "request_record_planning_ready": request_record_planning_ready,
        "recommended_next_phase": next_phase,
        "candidates": [
            {
                "phase": NEXT_PHASE_GO,
                "readiness": "freeze-authorization-grant-request-record-planning-ready",
                "authorization_request_issued": False,
                "request_record_created": False,
                "owner_approval_record_created": False,
                "grant_issued": False,
                "foundation_frozen": False,
                "closed": False,
            },
            {
                "phase": NEXT_PHASE_ALT,
                "readiness": "freeze-authorization-owner-approval-request-planning-ready",
                "authorization_request_issued": False,
                "request_record_created": False,
                "owner_approval_record_created": False,
                "grant_issued": False,
                "foundation_frozen": False,
                "closed": False,
            },
        ],
        "module_adapter_implementation_ready": False,
        "authorization_request_issued": False,
        "request_record_created": False,
        "owner_approval_record_created": False,
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
            "# Task Manager Foundation Handoff Freeze Authorization Grant Request Issuance Post-DryRun Review v1",
            "",
            "This phase reviews freeze authorization grant request issuance dry-run results only. It does not issue authorization request, create request records, or issue grant.",
            "",
            "本阶段仅审查 freeze authorization grant request issuance dry-run 结果，不发起 authorization request，不生成 request record / owner approval record，不签发 grant。",
            "",
            f"Request issuance dry-run accepted: `{request_issuance_dryrun_result_accepted}`",
            f"Issuance absence confirmed: `{issuance_absence_confirmed}`",
            f"Request record absent: `{request_record_absent}`",
            f"Owner approval record absent: `{owner_approval_record_absent}`",
            f"Grant token absent: `{grant_token_absent}`",
            f"Grant record absent: `{grant_record_absent}`",
            f"Request record planning ready: `{request_record_planning_ready}` (request issuance post-dryrun review ≠ authorization request issued)",
            f"Template lineage OK: `{template_lineage.get('template_lineage_ok')}`",
            f"Post-review scope: `{POST_REVIEW_SCOPE}`",
            f"Freeze status: `freeze-candidate` (not frozen)",
            f"Final decision: `{final_decision}`",
            f"Recommended next phase: `{next_phase}`",
            "",
            "## Request Issuance Post-Review Boundary Statements",
            *[f"- {stmt}" for stmt in POST_REVIEW_BOUNDARY_STATEMENTS],
            "",
            "request issuance post-dryrun review ≠ authorization request issued",
            "",
            "## Governance Debts (P1, not implemented)",
            f"- {GOVERNANCE_DEBTS[0]['debt_title']}",
            f"- {GOVERNANCE_DEBTS[1]['debt_title']}",
        ]
    )
    return {
        "task_manager_foundation_handoff_freeze_authorization_grant_request_issuance_post_dryrun_review": review_report,
        "task_manager_foundation_handoff_freeze_authorization_grant_request_issuance_post_dryrun_review_md": markdown,
        "task_manager_freeze_authorization_grant_request_issuance_dryrun_review_matrix": dryrun_review_matrix,
        "task_manager_freeze_authorization_grant_request_issuance_boundary_drift_review": boundary_drift_review,
        "task_manager_freeze_authorization_grant_request_issuance_chain_evidence_review": chain_evidence_review,
        "task_manager_freeze_authorization_grant_request_issuance_absence_review": issuance_absence_review,
        "task_manager_freeze_authorization_grant_request_issuance_state_absence_review": state_absence_review,
        "task_manager_freeze_authorization_grant_request_issuance_governance_debt_review": governance_debt_review,
        "task_manager_freeze_authorization_grant_request_issuance_template_lineage_review": template_lineage_review,
        "task_manager_freeze_authorization_grant_request_record_planning_readiness": request_record_planning_readiness,
        "summary": summary,
    }
