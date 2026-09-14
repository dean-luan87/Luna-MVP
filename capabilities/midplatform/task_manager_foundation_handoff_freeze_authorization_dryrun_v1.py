# -*- coding: utf-8 -*-
"""Luna Midplatform Task Manager Foundation Handoff Freeze Authorization DryRun v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.task_manager_foundation_handoff_final_closure_post_dryrun_review_v1 import (
    CHAIN_EVIDENCE_NODES,
)
from capabilities.midplatform.task_manager_foundation_handoff_final_closure_planning_v1 import GOVERNANCE_DEBTS
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_planning_v1 import (
    DEFAULT_OUTPUT as DEFAULT_FREEZE_AUTH_PLANNING_ROOT,
    FINAL_DECISION_GO as FREEZE_AUTH_PLANNING_FINAL_GO,
    NEXT_PHASE_GO as FREEZE_AUTH_PLANNING_NEXT_PHASE,
)
from capabilities.midplatform.task_manager_foundation_handoff_planning_v1 import (
    BOUNDARY_STATEMENT_EN,
    BOUNDARY_STATEMENT_ZH,
    FOUNDATION_ID,
)

PHASE_ID = "Phase-Midplatform-Task-Manager-Foundation-Handoff-Freeze-Authorization-DryRun-v1-001"
SCOPE = "midplatform_task_manager_foundation_handoff_freeze_authorization_dryrun_validation_only"
SOURCE_CHAIN = "midplatform_task_manager_foundation_handoff_freeze_authorization_dryrun_v1"
FINAL_DECISION_GO = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
FINAL_DECISION_PLAN_GAP = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_DRYRUN_BLOCKED_BY_PLANNING_PACKAGE_GAP"
FINAL_DECISION_SCOPE = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_DRYRUN_BLOCKED_BY_AUTHORIZATION_SCOPE_ESCALATION"
FINAL_DECISION_REQUEST = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_DRYRUN_BLOCKED_BY_AUTHORIZATION_REQUEST_LEAKAGE"
FINAL_DECISION_GRANT = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_DRYRUN_BLOCKED_BY_AUTHORIZATION_GRANT_LEAKAGE"
FINAL_DECISION_FREEZE_EXEC = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_DRYRUN_BLOCKED_BY_FREEZE_EXECUTION_LEAKAGE"
FINAL_DECISION_FREEZE = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_DRYRUN_BLOCKED_BY_FREEZE_STATE_ESCALATION"
FINAL_DECISION_DEBT = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_DRYRUN_BLOCKED_BY_GOVERNANCE_DEBT_GAP"
FINAL_DECISION_L1 = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_DRYRUN_BLOCKED_BY_L1_PROTOCOL_SCOPE_LEAKAGE"
NEXT_PHASE_GO = "Phase-Midplatform-Task-Manager-Foundation-Handoff-Freeze-Authorization-Post-DryRun-Review-v1-001"
NEXT_PHASE_HOLD = "Phase-Midplatform-Task-Manager-Foundation-Handoff-Freeze-Authorization-DryRun-Issue-Review-v1-001"
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "midplatform_task_manager_foundation_handoff_freeze_authorization_dryrun_v1_smoke_v0"
)

FREEZE_AUTHORIZATION_PLANNING_PACKAGE_FILES: Tuple[str, ...] = (
    "task_manager_foundation_handoff_freeze_authorization_plan_v1.json",
    "task_manager_foundation_handoff_freeze_authorization_plan_v1.md",
    "task_manager_freeze_authorization_scope_matrix_v1.json",
    "task_manager_freeze_authorization_candidate_asset_map_v1.json",
    "task_manager_freeze_authorization_evidence_chain_v1.json",
    "task_manager_freeze_authorization_boundary_contract_v1.json",
    "task_manager_freeze_authorization_readiness_matrix_v1.json",
    "task_manager_freeze_authorization_governance_debt_carryover_v1.json",
    "task_manager_freeze_authorization_non_execution_constraints_v1.json",
    "task_manager_freeze_authorization_next_phase_readiness_v1.json",
    "summary.json",
    "verifier_report.json",
)
PLANNING_TRUE_KEYS: Tuple[str, ...] = (
    "prior_final_review_go",
    "freeze_authorization_plan_complete",
    "authorization_scope_planning_only",
    "freeze_authorization_candidate_only",
    "freeze_candidate_preserved",
    "authorization_not_granted",
    "foundation_not_frozen",
    "closure_not_executed",
    "governance_debt_carryover_complete",
    "l1_protocols_not_implemented",
    "system_protocols_integration_not_implemented",
    "non_execution_boundary_ok",
    "next_phase_readiness_ok",
)
CHAIN_TRACE_NODES: Tuple[str, ...] = CHAIN_EVIDENCE_NODES + ("freeze_authorization_planning", "freeze_authorization_dryrun")
DRYRUN_BOUNDARY_STATEMENTS: Tuple[str, ...] = (
    "freeze_authorization_dryrun != freeze_authorization_grant",
    "freeze_authorization_candidate != freeze_authorized",
    "authorization_scope_candidate != authorized_scope",
    "freeze_candidate != frozen",
    "closure_candidate != closed",
)
ALLOWED_SCOPE_CLASSIFICATIONS: Tuple[str, ...] = (
    "authorization-planning-scope",
    "freeze-authorization-dryrun-scope",
)
RUNTIME_FORBIDDEN_FLAGS: Tuple[str, ...] = (
    "runtime_executor_created_now",
    "scheduler_binding_created_now",
    "task_execution_authority_granted_now",
    "output_authorization_granted_now",
    "module_adapter_integration_created_now",
    "information_channel_governance_implemented_now",
    "protocol_governance_implemented_now",
    "closure_channel_governance_implemented_now",
    "system_protocols_integration_implemented_now",
    "authorization_request_created_now",
    "authorization_grant_created_now",
    "freeze_execution_path_created_now",
    "rollback_execution_path_created_now",
)


def _read_json(path: Path) -> Dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return {}
    return payload if isinstance(payload, dict) else {}


def _meta(out: Path, planning: Path) -> Dict[str, Any]:
    return {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "source_chain": SOURCE_CHAIN,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "foundation_id": FOUNDATION_ID,
        "runtime_status": "not_enabled",
        "dryrun_only": True,
        "authorization_request_absent": True,
        "authorization_grant_absent": True,
        "freeze_execution_absent": True,
        "foundation_not_frozen": True,
        "closure_not_executed": True,
        "l1_protocols_not_implemented": True,
        "system_protocols_integration_not_implemented": True,
        "output_root": str(out),
        "freeze_authorization_planning_root": str(planning),
        "boundary_statement_en": BOUNDARY_STATEMENT_EN,
        "boundary_statement_zh": BOUNDARY_STATEMENT_ZH,
    }


def run_task_manager_foundation_handoff_freeze_authorization_dryrun_v1(
    *,
    freeze_authorization_planning_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    out = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    planning = Path(freeze_authorization_planning_root).expanduser().resolve()
    meta = _meta(out, planning)
    issues: List[str] = []

    planning_summary = _read_json(planning / "summary.json")
    planning_verifier = _read_json(planning / "verifier_report.json")
    scope_matrix = _read_json(planning / "task_manager_freeze_authorization_scope_matrix_v1.json")
    asset_map = _read_json(planning / "task_manager_freeze_authorization_candidate_asset_map_v1.json")
    evidence_chain_doc = _read_json(planning / "task_manager_freeze_authorization_evidence_chain_v1.json")
    boundary_contract = _read_json(planning / "task_manager_freeze_authorization_boundary_contract_v1.json")
    debt_carryover = _read_json(planning / "task_manager_freeze_authorization_governance_debt_carryover_v1.json")
    non_execution_doc = _read_json(planning / "task_manager_freeze_authorization_non_execution_constraints_v1.json")

    integrity_rows = []
    for fname in FREEZE_AUTHORIZATION_PLANNING_PACKAGE_FILES:
        path = planning / fname
        if fname.endswith(".json"):
            non_placeholder = bool(_read_json(path))
        else:
            non_placeholder = path.is_file() and len(path.read_text(encoding="utf-8").strip()) > 200
        integrity_rows.append({"file": fname, "exists": path.is_file(), "non_placeholder": non_placeholder})
        if not path.is_file() or not non_placeholder:
            issues.append(f"missing_or_placeholder:{fname}")

    planning_go = (
        planning_summary.get("final_decision") == FREEZE_AUTH_PLANNING_FINAL_GO
        and planning_summary.get("recommended_next_phase") == FREEZE_AUTH_PLANNING_NEXT_PHASE
        and planning_verifier.get("verifier") == "GO"
        and int(planning_verifier.get("passed_checks", 0)) >= 420
        and planning_verifier.get("failed_checks") == 0
        and planning_verifier.get("blocker_count") == 0
    )
    if not planning_go:
        issues.append("freeze_authorization_planning_not_go")

    for key in PLANNING_TRUE_KEYS:
        if planning_summary.get(key) is not True:
            issues.append(f"planning_key_false:{key}")

    trace_rows = list(evidence_chain_doc.get("chain") or [])
    trace_rows.append(
        {
            "stage": "freeze_authorization_dryrun",
            "root": str(out),
            "readiness": "freeze-authorization-dryrun-scope",
            "authorization_grant": False,
            "linked": True,
        }
    )
    freeze_authorization_chain_traceability_ok = all(
        next((r for r in trace_rows if r.get("stage") == stage), {}).get("linked") is True
        for stage in CHAIN_TRACE_NODES
    )
    dryrun_node = next((r for r in trace_rows if r.get("stage") == "freeze_authorization_dryrun"), {})
    if dryrun_node.get("authorization_grant") is True:
        freeze_authorization_chain_traceability_ok = False
    if not freeze_authorization_chain_traceability_ok:
        issues.append("chain_trace_gap")

    scope_rows = []
    for row in scope_matrix.get("rows") or []:
        scope_rows.append({**row, "classification": "freeze-authorization-dryrun-scope"})
    authorization_scope_preserved = all(
        row.get("classification") in ALLOWED_SCOPE_CLASSIFICATIONS for row in scope_rows
    ) and all(row.get("classification") != "authorized-scope" for row in scope_rows)
    if not authorization_scope_preserved:
        issues.append("authorization_scope_escalation")

    freeze_status = boundary_contract.get("freeze_status") or "freeze-candidate"
    candidate_rows = asset_map.get("assets") or []
    freeze_authorization_candidate_preserved = all(
        row.get("authorization_status") == "freeze-authorization-candidate"
        and row.get("authorization_status") != "freeze-authorized"
        for row in candidate_rows
    ) if candidate_rows else asset_map.get("freeze_authorization_candidate_only") is True
    freeze_candidate_preserved = (
        freeze_status == "freeze-candidate"
        and asset_map.get("freeze_candidate_preserved") is True
        and freeze_status not in ("frozen", "foundation-frozen")
    )
    if not freeze_authorization_candidate_preserved:
        issues.append("authorization_scope_escalation")
    if not freeze_candidate_preserved:
        issues.append("freeze_state_escalation")

    closure_status = "authorization-planning-ready"
    closure_not_executed = (
        boundary_contract.get("closure_applied") is False
        and boundary_contract.get("closed") is False
        and closure_status not in ("closed", "foundation-finalized")
    )
    if not closure_not_executed:
        issues.append("closure_state_escalation")

    authorization_request_absent = True
    authorization_grant_absent = (
        planning_summary.get("authorization_not_granted") is True
        and boundary_contract.get("authorization_not_granted") is True
    )
    freeze_execution_absent = True
    foundation_not_frozen = boundary_contract.get("foundation_frozen") is False
    for flag in RUNTIME_FORBIDDEN_FLAGS:
        if planning_summary.get(flag) is True:
            if "request" in flag:
                authorization_request_absent = False
            elif "grant" in flag:
                authorization_grant_absent = False
            elif "freeze_execution" in flag or "rollback_execution" in flag:
                freeze_execution_absent = False
    if not authorization_request_absent:
        issues.append("authorization_request_leakage")
    if not authorization_grant_absent:
        issues.append("authorization_grant_leakage")
    if not freeze_execution_absent:
        issues.append("freeze_execution_leakage")
    if not foundation_not_frozen:
        issues.append("freeze_state_escalation")

    non_execution_boundary_ok = non_execution_doc.get("non_execution_boundary_ok") is True
    if not non_execution_boundary_ok:
        issues.append("runtime_scope_leakage")

    debts = debt_carryover.get("debts") or []
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

    l1_protocols_not_implemented = debt_carryover.get("l1_protocols_not_implemented") is True
    system_protocols_integration_not_implemented = debt_carryover.get("system_protocols_integration_not_implemented") is True
    if not l1_protocols_not_implemented or not system_protocols_integration_not_implemented:
        issues.append("l1_protocol_scope_leakage")

    freeze_authorization_plan_integrity_ok = all(r["exists"] and r["non_placeholder"] for r in integrity_rows)
    dryrun_only = True
    post_review_readiness_ok = planning_go and freeze_authorization_chain_traceability_ok and governance_debt_preserved

    if not freeze_authorization_plan_integrity_ok or not planning_go:
        final_decision = FINAL_DECISION_PLAN_GAP
    elif not freeze_authorization_chain_traceability_ok:
        final_decision = FINAL_DECISION_PLAN_GAP
    elif not authorization_scope_preserved:
        final_decision = FINAL_DECISION_SCOPE
    elif not authorization_request_absent:
        final_decision = FINAL_DECISION_REQUEST
    elif not authorization_grant_absent:
        final_decision = FINAL_DECISION_GRANT
    elif not freeze_execution_absent:
        final_decision = FINAL_DECISION_FREEZE_EXEC
    elif not freeze_candidate_preserved or not foundation_not_frozen:
        final_decision = FINAL_DECISION_FREEZE
    elif not governance_debt_preserved:
        final_decision = FINAL_DECISION_DEBT
    elif not l1_protocols_not_implemented:
        final_decision = FINAL_DECISION_L1
    else:
        final_decision = FINAL_DECISION_GO

    dryrun_pass = (
        len(issues) == 0
        and final_decision == FINAL_DECISION_GO
        and freeze_authorization_plan_integrity_ok
        and freeze_authorization_chain_traceability_ok
        and authorization_scope_preserved
        and freeze_authorization_candidate_preserved
        and authorization_request_absent
        and authorization_grant_absent
        and freeze_execution_absent
        and foundation_not_frozen
        and closure_not_executed
        and governance_debt_preserved
        and l1_protocols_not_implemented
        and system_protocols_integration_not_implemented
        and dryrun_only
        and post_review_readiness_ok
    )

    dryrun_report = {
        "report_id": "task_manager_foundation_handoff_freeze_authorization_dryrun_report_v1",
        "planning_final_decision": planning_summary.get("final_decision"),
        "planning_verifier": planning_verifier.get("verifier"),
        "freeze_authorization_plan_integrity_ok": freeze_authorization_plan_integrity_ok,
        "freeze_authorization_chain_traceability_ok": freeze_authorization_chain_traceability_ok,
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
        "dryrun_only": dryrun_only,
        "post_review_readiness_ok": post_review_readiness_ok,
        "boundary_statements": list(DRYRUN_BOUNDARY_STATEMENTS),
        "final_decision": final_decision,
        "recommended_next_phase": NEXT_PHASE_GO if dryrun_pass else NEXT_PHASE_HOLD,
        **meta,
    }
    plan_integrity_matrix = {
        "matrix_id": "task_manager_freeze_authorization_plan_integrity_matrix_v1",
        "rows": integrity_rows,
        "freeze_authorization_plan_integrity_ok": freeze_authorization_plan_integrity_ok,
        **meta,
    }
    chain_traceability_matrix = {
        "matrix_id": "task_manager_freeze_authorization_chain_traceability_matrix_v1",
        "rows": trace_rows,
        "freeze_authorization_chain_traceability_ok": freeze_authorization_chain_traceability_ok,
        "points_to_dryrun_not_grant": True,
        **meta,
    }
    scope_validation = {
        "validation_id": "task_manager_freeze_authorization_scope_validation_v1",
        "rows": scope_rows,
        "authorization_scope_preserved": authorization_scope_preserved,
        "allowed_classifications": list(ALLOWED_SCOPE_CLASSIFICATIONS),
        **meta,
    }
    candidate_validation = {
        "validation_id": "task_manager_freeze_authorization_candidate_validation_v1",
        "freeze_status": freeze_status,
        "freeze_authorization_candidate_preserved": freeze_authorization_candidate_preserved,
        "freeze_candidate_preserved": freeze_candidate_preserved,
        "authorization_status": "freeze-authorization-candidate",
        **meta,
    }
    grant_absence_validation = {
        "validation_id": "task_manager_freeze_authorization_grant_absence_validation_v1",
        "authorization_request_absent": authorization_request_absent,
        "authorization_grant_absent": authorization_grant_absent,
        "freeze_execution_absent": freeze_execution_absent,
        "no_rollback_execution_path": True,
        **meta,
    }
    freeze_state_absence_validation = {
        "validation_id": "task_manager_freeze_state_absence_validation_v1",
        "freeze_status": freeze_status,
        "foundation_not_frozen": foundation_not_frozen,
        "closure_not_executed": closure_not_executed,
        "closure_status": closure_status,
        **meta,
    }
    governance_debt_validation = {
        "validation_id": "task_manager_freeze_authorization_governance_debt_validation_v1",
        "debts": debts,
        "governance_debt_preserved": governance_debt_preserved,
        "l1_protocols_not_implemented": l1_protocols_not_implemented,
        "system_protocols_integration_not_implemented": system_protocols_integration_not_implemented,
        **meta,
    }
    post_review_readiness = {
        "readiness_id": "task_manager_freeze_authorization_post_review_readiness_v1",
        "post_review_readiness_ok": post_review_readiness_ok,
        "recommended_next_phase": NEXT_PHASE_GO if dryrun_pass else NEXT_PHASE_HOLD,
        "module_adapter_implementation_ready": False,
        "freeze_authorization_granted": False,
        "foundation_frozen": False,
        "closed": False,
        **meta,
    }
    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "dryrun_pass": dryrun_pass,
        "blocker_count": len(issues),
        "issues": issues,
        "freeze_authorization_plan_integrity_ok": freeze_authorization_plan_integrity_ok,
        "freeze_authorization_chain_traceability_ok": freeze_authorization_chain_traceability_ok,
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
        "dryrun_only": dryrun_only,
        "post_review_readiness_ok": post_review_readiness_ok,
        "final_decision": final_decision,
        "recommended_next_phase": NEXT_PHASE_GO if dryrun_pass else NEXT_PHASE_HOLD,
        **meta,
    }
    markdown = "\n".join(
        [
            "# Task Manager Foundation Handoff Freeze Authorization DryRun Report v1",
            "",
            "This phase performs freeze authorization dry-run validation only. It does not grant authorization, freeze the foundation, or execute closure.",
            "",
            "本阶段仅执行 freeze authorization dry-run validation，不授予 authorization，不冻结 foundation，不执行 closure。",
            "",
            f"Planning GO: `{planning_go}`",
            f"Authorization request absent: `{authorization_request_absent}`",
            f"Authorization grant absent: `{authorization_grant_absent}`",
            f"Freeze status: `{freeze_status}` (not frozen)",
            f"Governance debt preserved: `{governance_debt_preserved}`",
            f"Final decision: `{final_decision}`",
            f"Recommended next phase: `{summary['recommended_next_phase']}`",
            "",
            "## Authorization Boundary Statements",
            *[f"- {stmt}" for stmt in DRYRUN_BOUNDARY_STATEMENTS],
            "",
            "## Governance Debts (P1, not implemented)",
            f"- {GOVERNANCE_DEBTS[0]['debt_title']}",
            f"- {GOVERNANCE_DEBTS[1]['debt_title']}",
        ]
    )
    return {
        "task_manager_foundation_handoff_freeze_authorization_dryrun_report": dryrun_report,
        "task_manager_foundation_handoff_freeze_authorization_dryrun_report_md": markdown,
        "task_manager_freeze_authorization_plan_integrity_matrix": plan_integrity_matrix,
        "task_manager_freeze_authorization_chain_traceability_matrix": chain_traceability_matrix,
        "task_manager_freeze_authorization_scope_validation": scope_validation,
        "task_manager_freeze_authorization_candidate_validation": candidate_validation,
        "task_manager_freeze_authorization_grant_absence_validation": grant_absence_validation,
        "task_manager_freeze_state_absence_validation": freeze_state_absence_validation,
        "task_manager_freeze_authorization_governance_debt_validation": governance_debt_validation,
        "task_manager_freeze_authorization_post_review_readiness": post_review_readiness,
        "summary": summary,
    }
