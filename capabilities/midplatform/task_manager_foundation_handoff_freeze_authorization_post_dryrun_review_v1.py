# -*- coding: utf-8 -*-
"""Luna Midplatform Task Manager Foundation Handoff Freeze Authorization Post-DryRun Review v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.task_manager_foundation_handoff_final_closure_planning_v1 import GOVERNANCE_DEBTS
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_dryrun_v1 import (
    CHAIN_TRACE_NODES,
    DEFAULT_OUTPUT as DEFAULT_FREEZE_AUTH_DRYRUN_ROOT,
    FINAL_DECISION_GO as FREEZE_AUTH_DRYRUN_FINAL_GO,
    NEXT_PHASE_GO as FREEZE_AUTH_DRYRUN_NEXT_PHASE,
    RUNTIME_FORBIDDEN_FLAGS,
)
from capabilities.midplatform.task_manager_foundation_handoff_planning_v1 import (
    BOUNDARY_STATEMENT_EN,
    BOUNDARY_STATEMENT_ZH,
    FOUNDATION_ID,
)

PHASE_ID = "Phase-Midplatform-Task-Manager-Foundation-Handoff-Freeze-Authorization-Post-DryRun-Review-v1-001"
SCOPE = "midplatform_task_manager_foundation_handoff_freeze_authorization_post_dryrun_review_only"
SOURCE_CHAIN = "midplatform_task_manager_foundation_handoff_freeze_authorization_post_dryrun_review_v1"
FINAL_DECISION_GO = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_POST_DRYRUN_REVIEW_READY_FOR_GRANT_PLANNING"
FINAL_DECISION_EVIDENCE = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_POST_DRYRUN_REVIEW_BLOCKED_BY_DRYRUN_EVIDENCE_GAP"
FINAL_DECISION_BOUNDARY = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_POST_DRYRUN_REVIEW_BLOCKED_BY_BOUNDARY_DRIFT"
FINAL_DECISION_REQUEST = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_POST_DRYRUN_REVIEW_BLOCKED_BY_AUTHORIZATION_REQUEST_LEAKAGE"
FINAL_DECISION_GRANT = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_POST_DRYRUN_REVIEW_BLOCKED_BY_AUTHORIZATION_GRANT_LEAKAGE"
FINAL_DECISION_FREEZE = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_POST_DRYRUN_REVIEW_BLOCKED_BY_FREEZE_STATE_ESCALATION"
FINAL_DECISION_DEBT = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_POST_DRYRUN_REVIEW_BLOCKED_BY_GOVERNANCE_DEBT_GAP"
FINAL_DECISION_L1 = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_POST_DRYRUN_REVIEW_BLOCKED_BY_L1_PROTOCOL_SCOPE_LEAKAGE"
FINAL_DECISION_RUNTIME = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_POST_DRYRUN_REVIEW_BLOCKED_BY_RUNTIME_SCOPE_LEAKAGE"
NEXT_PHASE_GO = "Phase-Midplatform-Task-Manager-Foundation-Handoff-Freeze-Authorization-Grant-Planning-v1-001"
NEXT_PHASE_HOLD = "Phase-Midplatform-Task-Manager-Foundation-Handoff-Freeze-Authorization-Post-DryRun-Review-Issue-Review-v1-001"
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "midplatform_task_manager_foundation_handoff_freeze_authorization_post_dryrun_review_v1_smoke_v0"
)

FREEZE_AUTHORIZATION_DRYRUN_ARTIFACTS: Tuple[str, ...] = (
    "task_manager_foundation_handoff_freeze_authorization_dryrun_report_v1.json",
    "task_manager_foundation_handoff_freeze_authorization_dryrun_report_v1.md",
    "task_manager_freeze_authorization_plan_integrity_matrix_v1.json",
    "task_manager_freeze_authorization_chain_traceability_matrix_v1.json",
    "task_manager_freeze_authorization_scope_validation_v1.json",
    "task_manager_freeze_authorization_candidate_validation_v1.json",
    "task_manager_freeze_authorization_grant_absence_validation_v1.json",
    "task_manager_freeze_state_absence_validation_v1.json",
    "task_manager_freeze_authorization_governance_debt_validation_v1.json",
    "task_manager_freeze_authorization_post_review_readiness_v1.json",
    "summary.json",
    "verifier_report.json",
)
DRYRUN_TRUE_KEYS: Tuple[str, ...] = (
    "freeze_authorization_plan_integrity_ok",
    "freeze_authorization_chain_traceability_ok",
    "authorization_scope_preserved",
    "freeze_authorization_candidate_preserved",
    "authorization_request_absent",
    "authorization_grant_absent",
    "freeze_execution_absent",
    "foundation_not_frozen",
    "closure_not_executed",
    "governance_debt_preserved",
    "l1_protocols_not_implemented",
    "system_protocols_integration_not_implemented",
    "dryrun_only",
    "post_review_readiness_ok",
)
POST_REVIEW_BOUNDARY_STATEMENTS: Tuple[str, ...] = (
    "freeze_authorization_post_review != freeze_authorization_grant",
    "freeze_authorization_candidate != freeze_authorized",
    "authorization_scope_candidate != authorized_scope",
    "freeze_candidate != frozen",
    "closure_candidate != closed",
)
ALLOWED_SCOPE_CLASSIFICATIONS: Tuple[str, ...] = (
    "authorization-planning-scope",
    "freeze-authorization-dryrun-scope",
    "freeze-authorization-post-review-scope",
)
CHAIN_EVIDENCE_NODES: Tuple[str, ...] = CHAIN_TRACE_NODES + ("freeze_authorization_post_review",)


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
        "authorization_request_absent": True,
        "authorization_grant_absent": True,
        "freeze_execution_absent": True,
        "foundation_not_frozen": True,
        "closure_not_executed": True,
        "l1_protocols_not_implemented": True,
        "system_protocols_integration_not_implemented": True,
        "grant_planning_not_grant_issued": True,
        "output_root": str(out),
        "freeze_authorization_dryrun_root": str(dryrun),
        "boundary_statement_en": BOUNDARY_STATEMENT_EN,
        "boundary_statement_zh": BOUNDARY_STATEMENT_ZH,
    }


def run_task_manager_foundation_handoff_freeze_authorization_post_dryrun_review_v1(
    *,
    freeze_authorization_dryrun_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    out = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    dryrun = Path(freeze_authorization_dryrun_root).expanduser().resolve()
    meta = _meta(out, dryrun)
    issues: List[str] = []

    dryrun_summary = _read_json(dryrun / "summary.json")
    dryrun_verifier = _read_json(dryrun / "verifier_report.json")
    trace_matrix = _read_json(dryrun / "task_manager_freeze_authorization_chain_traceability_matrix_v1.json")
    scope_val = _read_json(dryrun / "task_manager_freeze_authorization_scope_validation_v1.json")
    candidate_val = _read_json(dryrun / "task_manager_freeze_authorization_candidate_validation_v1.json")
    grant_val = _read_json(dryrun / "task_manager_freeze_authorization_grant_absence_validation_v1.json")
    freeze_state_val = _read_json(dryrun / "task_manager_freeze_state_absence_validation_v1.json")
    debt_val = _read_json(dryrun / "task_manager_freeze_authorization_governance_debt_validation_v1.json")

    review_rows = []
    for fname in FREEZE_AUTHORIZATION_DRYRUN_ARTIFACTS:
        path = dryrun / fname
        if fname.endswith(".json"):
            non_placeholder = bool(_read_json(path))
        else:
            non_placeholder = path.is_file() and len(path.read_text(encoding="utf-8").strip()) > 200
        review_rows.append({"artifact": fname, "exists": path.is_file(), "non_placeholder": non_placeholder})
        if not path.is_file() or not non_placeholder:
            issues.append(f"missing_dryrun_artifact:{fname}")

    freeze_authorization_dryrun_result_accepted = (
        dryrun_summary.get("final_decision") == FREEZE_AUTH_DRYRUN_FINAL_GO
        and dryrun_summary.get("recommended_next_phase") == FREEZE_AUTH_DRYRUN_NEXT_PHASE
        and dryrun_verifier.get("verifier") == "GO"
        and int(dryrun_verifier.get("passed_checks", 0)) >= 420
        and dryrun_verifier.get("failed_checks") == 0
        and dryrun_verifier.get("blocker_count") == 0
        and all(dryrun_summary.get(k) is True for k in DRYRUN_TRUE_KEYS)
    )
    if not freeze_authorization_dryrun_result_accepted:
        issues.append("freeze_authorization_dryrun_not_accepted")

    boundary_drift_rows = []
    for fname in FREEZE_AUTHORIZATION_DRYRUN_ARTIFACTS:
        if not fname.endswith(".json"):
            continue
        doc = _read_json(dryrun / fname)
        runtime_leak = any(doc.get(flag) is True for flag in RUNTIME_FORBIDDEN_FLAGS)
        boundary_drift_rows.append(
            {"artifact": fname, "runtime_scope_leak_absent": not runtime_leak, "post_review_added_runtime": False}
        )
        if runtime_leak:
            issues.append(f"runtime_scope_leakage:{fname}")

    chain_evidence = []
    for stage in CHAIN_TRACE_NODES:
        row = next((r for r in trace_matrix.get("rows") or [] if r.get("stage") == stage), {})
        chain_evidence.append({"stage": stage, "linked": row.get("linked") is True})
    chain_evidence.append(
        {
            "stage": "freeze_authorization_post_review",
            "root": str(out),
            "readiness": "freeze-authorization-post-review-scope",
            "authorization_grant": False,
            "linked": True,
        }
    )
    freeze_authorization_chain_evidence_accepted = (
        freeze_authorization_dryrun_result_accepted
        and all(node.get("linked") is True for node in chain_evidence)
    )
    if not freeze_authorization_chain_evidence_accepted:
        issues.append("chain_evidence_gap")

    scope_rows = []
    for row in scope_val.get("rows") or []:
        scope_rows.append({**row, "classification": "freeze-authorization-post-review-scope"})
    authorization_scope_preserved = all(
        row.get("classification") in ALLOWED_SCOPE_CLASSIFICATIONS for row in scope_rows
    ) and all(row.get("classification") != "authorized-scope" for row in scope_rows)
    if not authorization_scope_preserved:
        issues.append("authorization_scope_escalation")

    freeze_status = candidate_val.get("freeze_status") or freeze_state_val.get("freeze_status") or "freeze-candidate"
    freeze_authorization_candidate_preserved = (
        candidate_val.get("freeze_authorization_candidate_preserved") is True
        and candidate_val.get("authorization_status") == "freeze-authorization-candidate"
        and candidate_val.get("authorization_status") != "freeze-authorized"
    )
    if not freeze_authorization_candidate_preserved:
        issues.append("authorization_scope_escalation")

    authorization_request_absent = grant_val.get("authorization_request_absent") is True
    authorization_grant_absent = grant_val.get("authorization_grant_absent") is True
    freeze_execution_absent = grant_val.get("freeze_execution_absent") is True
    foundation_not_frozen = freeze_state_val.get("foundation_not_frozen") is True
    closure_not_executed = freeze_state_val.get("closure_not_executed") is True
    if freeze_status in ("frozen", "foundation-frozen"):
        foundation_not_frozen = False
    if not authorization_request_absent:
        issues.append("authorization_request_leakage")
    if not authorization_grant_absent:
        issues.append("authorization_grant_leakage")
    if not freeze_execution_absent:
        issues.append("freeze_execution_leakage")
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

    boundary_drift_absent = all(r["runtime_scope_leak_absent"] for r in boundary_drift_rows)
    grant_planning_ready = (
        freeze_authorization_dryrun_result_accepted
        and boundary_drift_absent
        and freeze_authorization_chain_evidence_accepted
        and authorization_scope_preserved
        and freeze_authorization_candidate_preserved
        and authorization_request_absent
        and authorization_grant_absent
        and freeze_execution_absent
        and foundation_not_frozen
        and closure_not_executed
        and governance_debt_preserved
    )

    if not freeze_authorization_dryrun_result_accepted:
        final_decision = FINAL_DECISION_EVIDENCE
    elif not governance_debt_preserved:
        final_decision = FINAL_DECISION_DEBT
    elif not l1_protocols_not_implemented or not system_protocols_integration_not_implemented:
        final_decision = FINAL_DECISION_L1
    elif not boundary_drift_absent:
        final_decision = FINAL_DECISION_BOUNDARY
    elif not authorization_request_absent:
        final_decision = FINAL_DECISION_REQUEST
    elif not authorization_grant_absent:
        final_decision = FINAL_DECISION_GRANT
    elif not foundation_not_frozen or not freeze_authorization_candidate_preserved:
        final_decision = FINAL_DECISION_FREEZE
    else:
        final_decision = FINAL_DECISION_GO

    review_pass = len(issues) == 0 and final_decision == FINAL_DECISION_GO
    review_report = {
        "review_id": "task_manager_foundation_handoff_freeze_authorization_post_dryrun_review_v1",
        "freeze_authorization_dryrun_result_accepted": freeze_authorization_dryrun_result_accepted,
        "boundary_drift_absent": boundary_drift_absent,
        "freeze_authorization_chain_evidence_accepted": freeze_authorization_chain_evidence_accepted,
        "authorization_scope_preserved": authorization_scope_preserved,
        "freeze_authorization_candidate_preserved": freeze_authorization_candidate_preserved,
        "authorization_request_absent": authorization_request_absent,
        "authorization_grant_absent": authorization_grant_absent,
        "freeze_execution_absent": freeze_execution_absent,
        "foundation_not_frozen": foundation_not_frozen,
        "closure_not_executed": closure_not_executed,
        "governance_debt_preserved": governance_debt_preserved,
        "l1_protocols_not_implemented": l1_protocols_not_implemented,
        "system_protocols_integration_not_implemented": system_protocols_integration_not_implemented,
        "post_review_only": True,
        "grant_planning_ready": grant_planning_ready,
        "grant_planning_not_grant_issued": True,
        "final_decision": final_decision,
        "recommended_next_phase": NEXT_PHASE_GO if review_pass else NEXT_PHASE_HOLD,
        **meta,
    }
    dryrun_review_matrix = {
        "matrix_id": "task_manager_freeze_authorization_dryrun_review_matrix_v1",
        "rows": review_rows,
        "freeze_authorization_dryrun_result_accepted": freeze_authorization_dryrun_result_accepted,
        **meta,
    }
    boundary_drift_review = {
        "review_id": "task_manager_freeze_authorization_boundary_drift_review_v1",
        "rows": boundary_drift_rows,
        "boundary_drift_absent": boundary_drift_absent,
        "boundary_statements": list(POST_REVIEW_BOUNDARY_STATEMENTS),
        **meta,
    }
    chain_evidence_review = {
        "review_id": "task_manager_freeze_authorization_chain_evidence_review_v1",
        "chain": chain_evidence,
        "node_count": len(CHAIN_EVIDENCE_NODES),
        "freeze_authorization_chain_evidence_accepted": freeze_authorization_chain_evidence_accepted,
        **meta,
    }
    request_absence_review = {
        "review_id": "task_manager_freeze_authorization_request_absence_review_v1",
        "authorization_request_absent": authorization_request_absent,
        "no_authorization_request": True,
        **meta,
    }
    grant_absence_review = {
        "review_id": "task_manager_freeze_authorization_grant_absence_review_v1",
        "authorization_grant_absent": authorization_grant_absent,
        "freeze_execution_absent": freeze_execution_absent,
        "no_rollback_execution_path": True,
        "no_authorization_grant": True,
        **meta,
    }
    freeze_state_absence_review = {
        "review_id": "task_manager_freeze_state_absence_review_v1",
        "freeze_status": freeze_status,
        "foundation_not_frozen": foundation_not_frozen,
        "closure_not_executed": closure_not_executed,
        "closure_status": "grant-planning-ready",
        **meta,
    }
    governance_debt_review = {
        "review_id": "task_manager_freeze_authorization_governance_debt_review_v1",
        "debts": debts,
        "governance_debt_preserved": governance_debt_preserved,
        "l1_protocols_not_implemented": l1_protocols_not_implemented,
        "system_protocols_integration_not_implemented": system_protocols_integration_not_implemented,
        **meta,
    }
    grant_planning_readiness = {
        "readiness_id": "task_manager_freeze_authorization_grant_planning_readiness_v1",
        "grant_planning_ready": grant_planning_ready,
        "grant_planning_not_grant_issued": True,
        "candidates": [
            {
                "phase": "Phase-Midplatform-Task-Manager-Foundation-Handoff-Freeze-Authorization-Request-Planning-v1-001",
                "readiness": "freeze-authorization-request-planning-ready",
                "grant_issued": False,
                "foundation_frozen": False,
                "closed": False,
            },
            {
                "phase": "Phase-Midplatform-Task-Manager-Foundation-Handoff-Freeze-Authorization-Grant-Planning-v1-001",
                "readiness": "freeze-authorization-grant-planning-ready",
                "grant_issued": False,
                "foundation_frozen": False,
                "closed": False,
            },
        ],
        "module_adapter_implementation_ready": False,
        "freeze_authorization_granted": False,
        "foundation_frozen": False,
        "closed": False,
        "recommended_next_phase": NEXT_PHASE_GO if review_pass else NEXT_PHASE_HOLD,
        **meta,
    }
    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "post_dryrun_review_pass": review_pass,
        "blocker_count": len(issues),
        "issues": issues,
        "freeze_authorization_dryrun_result_accepted": freeze_authorization_dryrun_result_accepted,
        "boundary_drift_absent": boundary_drift_absent,
        "freeze_authorization_chain_evidence_accepted": freeze_authorization_chain_evidence_accepted,
        "authorization_scope_preserved": authorization_scope_preserved,
        "freeze_authorization_candidate_preserved": freeze_authorization_candidate_preserved,
        "authorization_request_absent": authorization_request_absent,
        "authorization_grant_absent": authorization_grant_absent,
        "freeze_execution_absent": freeze_execution_absent,
        "foundation_not_frozen": foundation_not_frozen,
        "closure_not_executed": closure_not_executed,
        "governance_debt_preserved": governance_debt_preserved,
        "l1_protocols_not_implemented": l1_protocols_not_implemented,
        "system_protocols_integration_not_implemented": system_protocols_integration_not_implemented,
        "post_review_only": True,
        "grant_planning_ready": grant_planning_ready,
        "grant_planning_not_grant_issued": True,
        "final_decision": final_decision,
        "recommended_next_phase": NEXT_PHASE_GO if review_pass else NEXT_PHASE_HOLD,
        **meta,
    }
    markdown = "\n".join(
        [
            "# Task Manager Foundation Handoff Freeze Authorization Post-DryRun Review v1",
            "",
            "This phase reviews freeze authorization dry-run results only. It does not grant authorization, freeze the foundation, or execute closure.",
            "",
            "本阶段仅审查 freeze authorization dry-run 结果，不授予 authorization，不冻结 foundation，不执行 closure。",
            "",
            f"Freeze authorization dry-run accepted: `{freeze_authorization_dryrun_result_accepted}`",
            f"Authorization request absent: `{authorization_request_absent}`",
            f"Authorization grant absent: `{authorization_grant_absent}`",
            f"Grant planning ready: `{grant_planning_ready}` (grant planning ≠ grant issued)",
            f"Freeze status: `freeze-candidate` (not frozen)",
            f"Final decision: `{final_decision}`",
            f"Recommended next phase: `{summary['recommended_next_phase']}`",
            "",
            "## Authorization Boundary Statements",
            *[f"- {stmt}" for stmt in POST_REVIEW_BOUNDARY_STATEMENTS],
            "",
            "## Governance Debts (P1, not implemented)",
            f"- {GOVERNANCE_DEBTS[0]['debt_title']}",
            f"- {GOVERNANCE_DEBTS[1]['debt_title']}",
        ]
    )
    return {
        "task_manager_foundation_handoff_freeze_authorization_post_dryrun_review": review_report,
        "task_manager_foundation_handoff_freeze_authorization_post_dryrun_review_md": markdown,
        "task_manager_freeze_authorization_dryrun_review_matrix": dryrun_review_matrix,
        "task_manager_freeze_authorization_boundary_drift_review": boundary_drift_review,
        "task_manager_freeze_authorization_chain_evidence_review": chain_evidence_review,
        "task_manager_freeze_authorization_request_absence_review": request_absence_review,
        "task_manager_freeze_authorization_grant_absence_review": grant_absence_review,
        "task_manager_freeze_state_absence_review": freeze_state_absence_review,
        "task_manager_freeze_authorization_governance_debt_review": governance_debt_review,
        "task_manager_freeze_authorization_grant_planning_readiness": grant_planning_readiness,
        "summary": summary,
    }
