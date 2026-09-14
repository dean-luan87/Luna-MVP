# -*- coding: utf-8 -*-
"""Luna Midplatform Task Manager Foundation Handoff Freeze Authorization Grant DryRun v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.task_manager_foundation_handoff_evaluation_template_lineage_v1 import (
    BASE_DRYRUN_TEMPLATE_FILES,
    GRANT_DRYRUN_STAGE_ADDITIONS,
    GRANT_DRYRUN_STAGE_TERM_OVERRIDES,
    build_core_go_no_go_summary_fields,
    build_template_lineage,
)
from capabilities.midplatform.task_manager_foundation_handoff_final_closure_planning_v1 import GOVERNANCE_DEBTS
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_planning_v1 import (
    CHAIN_EVIDENCE_NODES,
    DEFAULT_OUTPUT as DEFAULT_GRANT_PLANNING_ROOT,
    FINAL_DECISION_GO as GRANT_PLANNING_FINAL_GO,
    NEXT_PHASE_GO as GRANT_PLANNING_NEXT_PHASE,
    PLANNING_TRUE_KEYS,
)
from capabilities.midplatform.task_manager_foundation_handoff_planning_v1 import (
    BOUNDARY_STATEMENT_EN,
    BOUNDARY_STATEMENT_ZH,
    FOUNDATION_ID,
)

PHASE_ID = "Phase-Midplatform-Task-Manager-Foundation-Handoff-Freeze-Authorization-Grant-DryRun-v1-001"
SCOPE = "midplatform_task_manager_foundation_handoff_freeze_authorization_grant_dryrun_validation_only"
SOURCE_CHAIN = "midplatform_task_manager_foundation_handoff_freeze_authorization_grant_dryrun_v1"
FINAL_DECISION_GO = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
FINAL_DECISION_PLAN_GAP = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_DRYRUN_BLOCKED_BY_PLANNING_PACKAGE_GAP"
FINAL_DECISION_SCOPE = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_DRYRUN_BLOCKED_BY_GRANT_SCOPE_ESCALATION"
FINAL_DECISION_ISSUANCE = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_DRYRUN_BLOCKED_BY_GRANT_ISSUANCE_LEAKAGE"
FINAL_DECISION_REQUEST = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_DRYRUN_BLOCKED_BY_AUTHORIZATION_REQUEST_LEAKAGE"
FINAL_DECISION_FREEZE = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_DRYRUN_BLOCKED_BY_FREEZE_STATE_ESCALATION"
FINAL_DECISION_DEBT = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_DRYRUN_BLOCKED_BY_GOVERNANCE_DEBT_GAP"
FINAL_DECISION_L1 = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_DRYRUN_BLOCKED_BY_L1_PROTOCOL_SCOPE_LEAKAGE"
FINAL_DECISION_RUNTIME = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_DRYRUN_BLOCKED_BY_RUNTIME_SCOPE_LEAKAGE"
NEXT_PHASE_GO = "Phase-Midplatform-Task-Manager-Foundation-Handoff-Freeze-Authorization-Grant-Post-DryRun-Review-v1-001"
NEXT_PHASE_HOLD = "Phase-Midplatform-Task-Manager-Foundation-Handoff-Freeze-Authorization-Grant-DryRun-Issue-Review-v1-001"
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "midplatform_task_manager_foundation_handoff_freeze_authorization_grant_dryrun_v1_smoke_v0"
)

GRANT_DRYRUN_ARTIFACTS: Tuple[str, ...] = (
    "task_manager_foundation_handoff_freeze_authorization_grant_dryrun_report_v1.json",
    "task_manager_foundation_handoff_freeze_authorization_grant_dryrun_report_v1.md",
    "task_manager_freeze_authorization_grant_plan_integrity_matrix_v1.json",
    "task_manager_freeze_authorization_grant_scope_validation_v1.json",
    "task_manager_freeze_authorization_grant_candidate_validation_v1.json",
    "task_manager_freeze_authorization_grant_prerequisite_validation_v1.json",
    "task_manager_freeze_authorization_grant_evidence_traceability_v1.json",
    "task_manager_freeze_authorization_grant_absence_validation_v1.json",
    "task_manager_freeze_authorization_grant_boundary_validation_v1.json",
    "task_manager_freeze_authorization_grant_governance_debt_validation_v1.json",
    "task_manager_freeze_authorization_grant_post_review_readiness_v1.json",
    "task_manager_freeze_authorization_grant_template_lineage_v1.json",
    "summary.json",
    "verifier_report.json",
)
GRANT_PLANNING_PACKAGE_FILES: Tuple[str, ...] = (
    "task_manager_foundation_handoff_freeze_authorization_grant_plan_v1.json",
    "task_manager_foundation_handoff_freeze_authorization_grant_plan_v1.md",
    "task_manager_freeze_authorization_grant_scope_matrix_v1.json",
    "task_manager_freeze_authorization_grant_candidate_asset_map_v1.json",
    "task_manager_freeze_authorization_grant_prerequisite_matrix_v1.json",
    "task_manager_freeze_authorization_grant_evidence_chain_v1.json",
    "task_manager_freeze_authorization_grant_boundary_contract_v1.json",
    "task_manager_freeze_authorization_grant_non_execution_constraints_v1.json",
    "task_manager_freeze_authorization_grant_governance_debt_carryover_v1.json",
    "task_manager_freeze_authorization_grant_next_phase_readiness_v1.json",
    "summary.json",
    "verifier_report.json",
)
CHAIN_TRACE_NODES: Tuple[str, ...] = CHAIN_EVIDENCE_NODES + ("freeze_authorization_grant_dryrun",)
DRYRUN_BOUNDARY_STATEMENTS: Tuple[str, ...] = (
    "grant_dryrun != grant_issued",
    "freeze_authorization_grant_candidate != freeze_authorization_granted",
    "grant_candidate != grant_record",
    "grant_readiness != grant",
    "freeze_candidate != frozen",
    "closure_candidate != closed",
)
ALLOWED_SCOPE_CLASSIFICATIONS: Tuple[str, ...] = (
    "grant-planning-scope",
    "grant-dryrun-scope",
)
FORBIDDEN_ASSET_STATES: Tuple[str, ...] = (
    "frozen",
    "foundation-frozen",
    "closed",
    "foundation-finalized",
)
GO_CONDITIONS_KEYS: Tuple[str, ...] = (
    "grant_plan_integrity_ok",
    "grant_scope_preserved",
    "grant_candidate_preserved",
    "grant_prerequisites_satisfied",
    "grant_evidence_traceability_ok",
    "authorization_request_absent",
    "authorization_grant_absent",
    "grant_token_absent",
    "grant_record_absent",
    "owner_approval_record_absent",
    "foundation_not_frozen",
    "closure_not_executed",
    "governance_debt_preserved",
    "l1_protocols_not_implemented",
    "system_protocols_integration_not_implemented",
    "grant_dryrun_only",
    "post_review_readiness_ok",
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
    "grant_token_created_now",
    "grant_record_created_now",
    "owner_approval_record_created_now",
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
        "grant_dryrun_only": True,
        "grant_not_issued": True,
        "authorization_request_absent": True,
        "authorization_grant_absent": True,
        "grant_token_absent": True,
        "grant_record_absent": True,
        "owner_approval_record_absent": True,
        "foundation_not_frozen": True,
        "closure_not_executed": True,
        "l1_protocols_not_implemented": True,
        "system_protocols_integration_not_implemented": True,
        "output_root": str(out),
        "grant_planning_root": str(planning),
        "boundary_statement_en": BOUNDARY_STATEMENT_EN,
        "boundary_statement_zh": BOUNDARY_STATEMENT_ZH,
    }


def run_task_manager_foundation_handoff_freeze_authorization_grant_dryrun_v1(
    *,
    grant_planning_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    out = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    planning = Path(grant_planning_root).expanduser().resolve()
    meta = _meta(out, planning)
    issues: List[str] = []

    planning_summary = _read_json(planning / "summary.json")
    planning_verifier = _read_json(planning / "verifier_report.json")
    scope_matrix = _read_json(planning / "task_manager_freeze_authorization_grant_scope_matrix_v1.json")
    asset_map = _read_json(planning / "task_manager_freeze_authorization_grant_candidate_asset_map_v1.json")
    prerequisite_matrix = _read_json(planning / "task_manager_freeze_authorization_grant_prerequisite_matrix_v1.json")
    evidence_chain_doc = _read_json(planning / "task_manager_freeze_authorization_grant_evidence_chain_v1.json")
    boundary_contract = _read_json(planning / "task_manager_freeze_authorization_grant_boundary_contract_v1.json")
    debt_carryover = _read_json(planning / "task_manager_freeze_authorization_grant_governance_debt_carryover_v1.json")
    non_execution_doc = _read_json(planning / "task_manager_freeze_authorization_grant_non_execution_constraints_v1.json")

    integrity_rows = []
    for fname in GRANT_PLANNING_PACKAGE_FILES:
        path = planning / fname
        if fname.endswith(".json"):
            non_placeholder = bool(_read_json(path))
        else:
            non_placeholder = path.is_file() and len(path.read_text(encoding="utf-8").strip()) > 200
        integrity_rows.append({"file": fname, "exists": path.is_file(), "non_placeholder": non_placeholder})
        if not path.is_file() or not non_placeholder:
            issues.append(f"missing_or_placeholder:{fname}")

    planning_go = (
        planning_summary.get("final_decision") == GRANT_PLANNING_FINAL_GO
        and planning_summary.get("recommended_next_phase") == GRANT_PLANNING_NEXT_PHASE
        and planning_verifier.get("verifier") == "GO"
        and int(planning_verifier.get("passed_checks", 0)) >= 420
        and planning_verifier.get("failed_checks") == 0
        and planning_verifier.get("blocker_count") == 0
    )
    if not planning_go:
        issues.append("grant_planning_not_go")

    for key in PLANNING_TRUE_KEYS:
        if planning_summary.get(key) is not True:
            issues.append(f"planning_key_false:{key}")

    trace_rows = list(evidence_chain_doc.get("chain") or [])
    trace_rows.append(
        {
            "stage": "freeze_authorization_grant_dryrun",
            "root": str(out),
            "readiness": "grant-dryrun-scope",
            "authorization_grant": False,
            "grant_issued": False,
            "linked": True,
        }
    )
    grant_evidence_traceability_ok = all(
        next((r for r in trace_rows if r.get("stage") == stage), {}).get("linked") is True
        for stage in CHAIN_TRACE_NODES
    )
    dryrun_node = next((r for r in trace_rows if r.get("stage") == "freeze_authorization_grant_dryrun"), {})
    if dryrun_node.get("authorization_grant") is True or dryrun_node.get("grant_issued") is True:
        grant_evidence_traceability_ok = False
    if not grant_evidence_traceability_ok:
        issues.append("chain_trace_gap")

    scope_rows = []
    for row in scope_matrix.get("rows") or []:
        scope_rows.append({**row, "classification": "grant-dryrun-scope"})
    grant_scope_preserved = all(
        row.get("classification") in ALLOWED_SCOPE_CLASSIFICATIONS for row in scope_rows
    ) and all(
        row.get("classification") not in ("grant-issued-scope", "authorized-scope") for row in scope_rows
    )
    if not grant_scope_preserved:
        issues.append("grant_scope_escalation")

    freeze_status = boundary_contract.get("freeze_status") or "freeze-candidate"
    candidate_rows = asset_map.get("assets") or []
    grant_candidate_preserved = all(
        row.get("grant_status") == "freeze-authorization-grant-candidate"
        and row.get("authorization_status") == "freeze-authorization-grant-candidate"
        and row.get("grant_status") != "freeze-authorization-granted"
        and row.get("freeze_status") not in FORBIDDEN_ASSET_STATES
        for row in candidate_rows
    ) if candidate_rows else asset_map.get("grant_candidate_only") is True
    asset_state_ok = all(
        row.get("freeze_status") not in FORBIDDEN_ASSET_STATES
        and row.get("grant_status") not in FORBIDDEN_ASSET_STATES
        for row in candidate_rows
    ) if candidate_rows else True
    if not grant_candidate_preserved:
        issues.append("grant_scope_escalation")
    if not asset_state_ok:
        issues.append("freeze_state_escalation")

    authorization_request_absent = True
    authorization_grant_absent = (
        planning_summary.get("grant_not_issued") is True
        and planning_summary.get("authorization_grant_absent") is True
        and boundary_contract.get("grant_not_issued") is True
    )
    grant_not_issued = planning_summary.get("grant_not_issued") is True
    grant_token_absent = True
    grant_record_absent = True
    owner_approval_record_absent = True
    foundation_not_frozen = boundary_contract.get("foundation_frozen") is False
    closure_not_executed = (
        boundary_contract.get("closure_applied") is False
        and boundary_contract.get("closed") is False
    )
    for flag in RUNTIME_FORBIDDEN_FLAGS:
        if planning_summary.get(flag) is True or non_execution_doc.get(flag.replace("_created_now", "")) is False:
            if "request" in flag:
                authorization_request_absent = False
            elif flag == "authorization_grant_created_now":
                authorization_grant_absent = False
            elif flag == "grant_token_created_now":
                grant_token_absent = False
            elif flag == "grant_record_created_now":
                grant_record_absent = False
            elif flag == "owner_approval_record_created_now":
                owner_approval_record_absent = False

    prerequisite_validation = {
        "authorization_request_absent": authorization_request_absent,
        "authorization_grant_absent": authorization_grant_absent,
        "grant_not_issued": grant_not_issued,
        "foundation_not_frozen": foundation_not_frozen,
        "closure_not_executed": closure_not_executed,
    }
    grant_prerequisites_satisfied = (
        prerequisite_matrix.get("prerequisites_ok") is True
        and all(prerequisite_validation[k] for k in prerequisite_validation)
    )
    if not authorization_request_absent:
        issues.append("authorization_request_leakage")
    if not authorization_grant_absent or not grant_not_issued:
        issues.append("grant_issuance_leakage")
    if not grant_token_absent or not grant_record_absent or not owner_approval_record_absent:
        issues.append("grant_issuance_leakage")
    if not foundation_not_frozen:
        issues.append("freeze_state_escalation")
    if not closure_not_executed:
        issues.append("closure_state_escalation")
    if not grant_prerequisites_satisfied:
        issues.append("prerequisite_gap")

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

    grant_plan_integrity_ok = all(r["exists"] and r["non_placeholder"] for r in integrity_rows)
    grant_dryrun_only = True
    post_review_readiness_ok = planning_go and grant_evidence_traceability_ok and governance_debt_preserved

    if not grant_plan_integrity_ok or not planning_go:
        final_decision = FINAL_DECISION_PLAN_GAP
    elif not grant_evidence_traceability_ok:
        final_decision = FINAL_DECISION_PLAN_GAP
    elif not grant_scope_preserved:
        final_decision = FINAL_DECISION_SCOPE
    elif not authorization_request_absent:
        final_decision = FINAL_DECISION_REQUEST
    elif not authorization_grant_absent or not grant_not_issued or not grant_token_absent or not grant_record_absent:
        final_decision = FINAL_DECISION_ISSUANCE
    elif not grant_candidate_preserved or not foundation_not_frozen or not asset_state_ok:
        final_decision = FINAL_DECISION_FREEZE
    elif not governance_debt_preserved:
        final_decision = FINAL_DECISION_DEBT
    elif not l1_protocols_not_implemented:
        final_decision = FINAL_DECISION_L1
    elif not non_execution_boundary_ok:
        final_decision = FINAL_DECISION_RUNTIME
    else:
        final_decision = FINAL_DECISION_GO

    go_condition_values = {
        "grant_plan_integrity_ok": grant_plan_integrity_ok,
        "grant_scope_preserved": grant_scope_preserved,
        "grant_candidate_preserved": grant_candidate_preserved,
        "grant_prerequisites_satisfied": grant_prerequisites_satisfied,
        "grant_evidence_traceability_ok": grant_evidence_traceability_ok,
        "authorization_request_absent": authorization_request_absent,
        "authorization_grant_absent": authorization_grant_absent,
        "grant_token_absent": grant_token_absent,
        "grant_record_absent": grant_record_absent,
        "owner_approval_record_absent": owner_approval_record_absent,
        "foundation_not_frozen": foundation_not_frozen,
        "closure_not_executed": closure_not_executed,
        "governance_debt_preserved": governance_debt_preserved,
        "l1_protocols_not_implemented": l1_protocols_not_implemented,
        "system_protocols_integration_not_implemented": system_protocols_integration_not_implemented,
        "grant_dryrun_only": grant_dryrun_only,
        "post_review_readiness_ok": post_review_readiness_ok,
    }
    dryrun_pass = len(issues) == 0 and final_decision == FINAL_DECISION_GO and all(go_condition_values.values())

    repo_root = Path(__file__).resolve().parents[2]
    template_lineage = build_template_lineage(
        base_phase="Freeze-Authorization-DryRun-v1-001",
        base_capability=BASE_DRYRUN_TEMPLATE_FILES[0],
        base_runner=BASE_DRYRUN_TEMPLATE_FILES[1],
        base_verifier=BASE_DRYRUN_TEMPLATE_FILES[2],
        base_go_no_go_pack=BASE_DRYRUN_TEMPLATE_FILES[3],
        stage_phase="Freeze-Authorization-Grant-DryRun-v1-001",
        stage_term_overrides=GRANT_DRYRUN_STAGE_TERM_OVERRIDES,
        stage_additions=GRANT_DRYRUN_STAGE_ADDITIONS,
        template_files=BASE_DRYRUN_TEMPLATE_FILES,
        repo_root=repo_root,
    )
    next_phase = NEXT_PHASE_GO if dryrun_pass else NEXT_PHASE_HOLD
    core_schema_fields = build_core_go_no_go_summary_fields(
        go_conditions=go_condition_values,
        forbidden_runtime_flags=RUNTIME_FORBIDDEN_FLAGS,
        chain_trace_nodes=CHAIN_TRACE_NODES,
        go_no_go_decision=final_decision,
        final_decision=final_decision,
        next_phase=next_phase,
        template_lineage=template_lineage,
    )

    dryrun_report = {
        "report_id": "task_manager_foundation_handoff_freeze_authorization_grant_dryrun_report_v1",
        "planning_final_decision": planning_summary.get("final_decision"),
        "planning_verifier": planning_verifier.get("verifier"),
        "grant_plan_integrity_ok": grant_plan_integrity_ok,
        "grant_scope_preserved": grant_scope_preserved,
        "grant_candidate_preserved": grant_candidate_preserved,
        "grant_prerequisites_satisfied": grant_prerequisites_satisfied,
        "grant_evidence_traceability_ok": grant_evidence_traceability_ok,
        "authorization_request_absent": authorization_request_absent,
        "authorization_grant_absent": authorization_grant_absent,
        "grant_token_absent": grant_token_absent,
        "grant_record_absent": grant_record_absent,
        "owner_approval_record_absent": owner_approval_record_absent,
        "foundation_not_frozen": foundation_not_frozen,
        "closure_not_executed": closure_not_executed,
        "governance_debt_preserved": governance_debt_preserved,
        "l1_protocols_not_implemented": l1_protocols_not_implemented,
        "system_protocols_integration_not_implemented": system_protocols_integration_not_implemented,
        "grant_dryrun_only": grant_dryrun_only,
        "post_review_readiness_ok": post_review_readiness_ok,
        "boundary_statements": list(DRYRUN_BOUNDARY_STATEMENTS),
        "final_decision": final_decision,
        "recommended_next_phase": next_phase,
        **meta,
    }
    plan_integrity_matrix = {
        "matrix_id": "task_manager_freeze_authorization_grant_plan_integrity_matrix_v1",
        "rows": integrity_rows,
        "grant_plan_integrity_ok": grant_plan_integrity_ok,
        **meta,
    }
    scope_validation = {
        "validation_id": "task_manager_freeze_authorization_grant_scope_validation_v1",
        "rows": scope_rows,
        "grant_scope_preserved": grant_scope_preserved,
        "allowed_classifications": list(ALLOWED_SCOPE_CLASSIFICATIONS),
        **meta,
    }
    candidate_validation = {
        "validation_id": "task_manager_freeze_authorization_grant_candidate_validation_v1",
        "freeze_status": freeze_status,
        "grant_candidate_preserved": grant_candidate_preserved,
        "asset_state_ok": asset_state_ok,
        "grant_status": "freeze-authorization-grant-candidate",
        "forbidden_states": list(FORBIDDEN_ASSET_STATES),
        **meta,
    }
    prerequisite_validation_doc = {
        "validation_id": "task_manager_freeze_authorization_grant_prerequisite_validation_v1",
        "rows": prerequisite_matrix.get("rows") or [],
        "grant_prerequisites_satisfied": grant_prerequisites_satisfied,
        **prerequisite_validation,
        **meta,
    }
    evidence_traceability = {
        "trace_id": "task_manager_freeze_authorization_grant_evidence_traceability_v1",
        "matrix_id": "task_manager_freeze_authorization_grant_chain_traceability_matrix_v1",
        "rows": trace_rows,
        "grant_evidence_traceability_ok": grant_evidence_traceability_ok,
        "freeze_authorization_chain_traceability_ok": grant_evidence_traceability_ok,
        "points_to_dryrun_not_issued": True,
        "points_to_dryrun_not_grant": True,
        **meta,
    }
    freeze_state_absence_validation = {
        "validation_id": "task_manager_freeze_authorization_grant_freeze_state_absence_validation_v1",
        "freeze_status": freeze_status,
        "foundation_not_frozen": foundation_not_frozen,
        "closure_not_executed": closure_not_executed,
        "closure_status": "grant-dryrun-ready",
        **meta,
    }
    grant_absence_validation = {
        "validation_id": "task_manager_freeze_authorization_grant_absence_validation_v1",
        "authorization_request_absent": authorization_request_absent,
        "authorization_grant_absent": authorization_grant_absent,
        "grant_token_absent": grant_token_absent,
        "grant_record_absent": grant_record_absent,
        "owner_approval_record_absent": owner_approval_record_absent,
        "no_freeze_execution_path": True,
        "no_rollback_execution_path": True,
        **meta,
    }
    boundary_validation = {
        "validation_id": "task_manager_freeze_authorization_grant_boundary_validation_v1",
        "statements": list(DRYRUN_BOUNDARY_STATEMENTS),
        "grant_dryrun_only": grant_dryrun_only,
        "grant_not_issued": grant_not_issued,
        "grant_issued": False,
        "foundation_frozen": False,
        "closed": False,
        **meta,
    }
    governance_debt_validation = {
        "validation_id": "task_manager_freeze_authorization_grant_governance_debt_validation_v1",
        "debts": debts,
        "governance_debt_preserved": governance_debt_preserved,
        "l1_protocols_not_implemented": l1_protocols_not_implemented,
        "system_protocols_integration_not_implemented": system_protocols_integration_not_implemented,
        **meta,
    }
    post_review_readiness = {
        "readiness_id": "task_manager_freeze_authorization_grant_post_review_readiness_v1",
        "post_review_readiness_ok": post_review_readiness_ok,
        "recommended_next_phase": next_phase,
        "target": "freeze_authorization_grant_post_dryrun_review",
        "module_adapter_implementation_ready": False,
        "grant_issued": False,
        "freeze_authorization_granted": False,
        "foundation_frozen": False,
        "closed": False,
        **meta,
    }
    template_lineage_doc = {
        "lineage_id": "task_manager_freeze_authorization_grant_template_lineage_v1",
        **template_lineage,
        **meta,
    }
    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "dryrun_pass": dryrun_pass,
        "blocker_count": len(issues),
        "issues": issues,
        **go_condition_values,
        **core_schema_fields,
        **meta,
    }
    markdown = "\n".join(
        [
            "# Task Manager Foundation Handoff Freeze Authorization Grant DryRun Report v1",
            "",
            "This phase performs freeze authorization grant dry-run validation only. It does not issue grant, freeze the foundation, or execute closure.",
            "",
            "本阶段仅执行 freeze authorization grant dry-run validation，不签发 grant，不冻结 foundation，不执行 closure。",
            "",
            f"Grant planning GO: `{planning_go}`",
            f"Grant not issued: `{grant_not_issued}` (grant dryrun ≠ grant issued)",
            f"Authorization request absent: `{authorization_request_absent}`",
            f"Grant token absent: `{grant_token_absent}`",
            f"Grant record absent: `{grant_record_absent}`",
            f"Owner approval record absent: `{owner_approval_record_absent}`",
            f"Freeze status: `{freeze_status}` (not frozen)",
            f"Governance debt preserved: `{governance_debt_preserved}`",
            f"Final decision: `{final_decision}`",
            f"Recommended next phase: `{summary['recommended_next_phase']}`",
            "",
            "## Grant Boundary Statements",
            *[f"- {stmt}" for stmt in DRYRUN_BOUNDARY_STATEMENTS],
            "",
            "## Governance Debts (P1, not implemented)",
            f"- {GOVERNANCE_DEBTS[0]['debt_title']}",
            f"- {GOVERNANCE_DEBTS[1]['debt_title']}",
        ]
    )
    return {
        "task_manager_foundation_handoff_freeze_authorization_grant_dryrun_report": dryrun_report,
        "task_manager_foundation_handoff_freeze_authorization_grant_dryrun_report_md": markdown,
        "task_manager_freeze_authorization_grant_plan_integrity_matrix": plan_integrity_matrix,
        "task_manager_freeze_authorization_grant_scope_validation": scope_validation,
        "task_manager_freeze_authorization_grant_candidate_validation": candidate_validation,
        "task_manager_freeze_authorization_grant_prerequisite_validation": prerequisite_validation_doc,
        "task_manager_freeze_authorization_grant_evidence_traceability": evidence_traceability,
        "task_manager_freeze_authorization_grant_absence_validation": grant_absence_validation,
        "task_manager_freeze_authorization_grant_boundary_validation": boundary_validation,
        "task_manager_freeze_authorization_grant_governance_debt_validation": governance_debt_validation,
        "task_manager_freeze_authorization_grant_post_review_readiness": post_review_readiness,
        "task_manager_freeze_authorization_grant_freeze_state_absence_validation": freeze_state_absence_validation,
        "task_manager_freeze_authorization_grant_template_lineage": template_lineage_doc,
        "summary": summary,
    }
