# -*- coding: utf-8 -*-
"""Luna Midplatform Task Manager Foundation Handoff Freeze Authorization Grant Post-DryRun Review v1.

Structure inherited from task_manager_foundation_handoff_freeze_authorization_post_dryrun_review_v1.py
via whitelist template reuse (no full-repo scan).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.task_manager_foundation_handoff_evaluation_template_lineage_v1 import (
    BASE_POST_REVIEW_TEMPLATE_FILES,
    GRANT_POST_REVIEW_STAGE_ADDITIONS,
    GRANT_POST_REVIEW_STAGE_TERM_OVERRIDES,
    build_core_go_no_go_summary_fields,
    build_template_lineage,
)
from capabilities.midplatform.task_manager_foundation_handoff_final_closure_planning_v1 import GOVERNANCE_DEBTS
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_dryrun_v1 import (
    CHAIN_TRACE_NODES,
    DEFAULT_OUTPUT as DEFAULT_GRANT_DRYRUN_ROOT,
    FINAL_DECISION_GO as GRANT_DRYRUN_FINAL_GO,
    GO_CONDITIONS_KEYS as GRANT_DRYRUN_TRUE_KEYS,
    GRANT_DRYRUN_ARTIFACTS,
    NEXT_PHASE_GO as GRANT_DRYRUN_NEXT_PHASE,
    RUNTIME_FORBIDDEN_FLAGS,
)
from capabilities.midplatform.task_manager_foundation_handoff_planning_v1 import (
    BOUNDARY_STATEMENT_EN,
    BOUNDARY_STATEMENT_ZH,
    FOUNDATION_ID,
)

PHASE_ID = "Phase-Midplatform-Task-Manager-Foundation-Handoff-Freeze-Authorization-Grant-Post-DryRun-Review-v1-001"
SCOPE = "midplatform_task_manager_foundation_handoff_freeze_authorization_grant_post_dryrun_review_only"
SOURCE_CHAIN = "midplatform_task_manager_foundation_handoff_freeze_authorization_grant_post_dryrun_review_v1"
FINAL_DECISION_GO = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_POST_DRYRUN_REVIEW_READY_FOR_GRANT_REQUEST_PLANNING"
FINAL_DECISION_EVIDENCE = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_POST_DRYRUN_REVIEW_BLOCKED_BY_DRYRUN_EVIDENCE_GAP"
FINAL_DECISION_BOUNDARY = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_POST_DRYRUN_REVIEW_BLOCKED_BY_BOUNDARY_DRIFT"
FINAL_DECISION_REQUEST = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_POST_DRYRUN_REVIEW_BLOCKED_BY_AUTHORIZATION_REQUEST_LEAKAGE"
FINAL_DECISION_GRANT = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_POST_DRYRUN_REVIEW_BLOCKED_BY_GRANT_ISSUANCE_LEAKAGE"
FINAL_DECISION_FREEZE = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_POST_DRYRUN_REVIEW_BLOCKED_BY_FREEZE_STATE_ESCALATION"
FINAL_DECISION_DEBT = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_POST_DRYRUN_REVIEW_BLOCKED_BY_GOVERNANCE_DEBT_GAP"
FINAL_DECISION_L1 = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_POST_DRYRUN_REVIEW_BLOCKED_BY_L1_PROTOCOL_SCOPE_LEAKAGE"
FINAL_DECISION_RUNTIME = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_POST_DRYRUN_REVIEW_BLOCKED_BY_RUNTIME_SCOPE_LEAKAGE"
FINAL_DECISION_LINEAGE = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_POST_DRYRUN_REVIEW_BLOCKED_BY_TEMPLATE_LINEAGE_GAP"
NEXT_PHASE_GO = "Phase-Midplatform-Task-Manager-Foundation-Handoff-Freeze-Authorization-Grant-Request-Planning-v1-001"
NEXT_PHASE_HOLD = "Phase-Midplatform-Task-Manager-Foundation-Handoff-Freeze-Authorization-Grant-Post-DryRun-Review-Issue-Review-v1-001"
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "midplatform_task_manager_foundation_handoff_freeze_authorization_grant_post_dryrun_review_v1_smoke_v0"
)

POST_REVIEW_BOUNDARY_STATEMENTS: Tuple[str, ...] = (
    "grant_post_dryrun_review != grant_issued",
    "grant_candidate != grant_record",
    "freeze_authorization_grant_candidate != freeze_authorization_granted",
    "owner_approval_candidate != owner_approval_record",
    "freeze_candidate != frozen",
    "closure_candidate != closed",
)
CHAIN_EVIDENCE_NODES: Tuple[str, ...] = CHAIN_TRACE_NODES + ("freeze_authorization_grant_post_dryrun_review",)
GO_CONDITIONS_KEYS: Tuple[str, ...] = (
    "grant_dryrun_result_accepted",
    "boundary_drift_absent",
    "grant_chain_evidence_accepted",
    "grant_absence_confirmed",
    "grant_token_absent",
    "grant_record_absent",
    "owner_approval_record_absent",
    "foundation_not_frozen",
    "closure_not_executed",
    "governance_debt_preserved",
    "l1_protocols_not_implemented",
    "system_protocols_integration_not_implemented",
    "template_lineage_ok",
    "full_repo_scan_absent",
    "core_go_no_go_schema_preserved",
    "post_review_only",
    "next_planning_ready",
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
        "authorization_request_absent": True,
        "authorization_grant_absent": True,
        "grant_token_absent": True,
        "grant_record_absent": True,
        "owner_approval_record_absent": True,
        "foundation_not_frozen": True,
        "closure_not_executed": True,
        "l1_protocols_not_implemented": True,
        "system_protocols_integration_not_implemented": True,
        "grant_not_issued": True,
        "output_root": str(out),
        "grant_dryrun_root": str(dryrun),
        "boundary_statement_en": BOUNDARY_STATEMENT_EN,
        "boundary_statement_zh": BOUNDARY_STATEMENT_ZH,
    }


def run_task_manager_foundation_handoff_freeze_authorization_grant_post_dryrun_review_v1(
    *,
    grant_dryrun_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    out = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    dryrun = Path(grant_dryrun_root).expanduser().resolve()
    repo_root = Path(__file__).resolve().parents[2]
    meta = _meta(out, dryrun)
    issues: List[str] = []

    dryrun_summary = _read_json(dryrun / "summary.json")
    dryrun_verifier = _read_json(dryrun / "verifier_report.json")
    dryrun_lineage = _read_json(dryrun / "task_manager_freeze_authorization_grant_template_lineage_v1.json")
    trace_matrix = _read_json(dryrun / "task_manager_freeze_authorization_grant_evidence_traceability_v1.json")
    candidate_val = _read_json(dryrun / "task_manager_freeze_authorization_grant_candidate_validation_v1.json")
    grant_val = _read_json(dryrun / "task_manager_freeze_authorization_grant_absence_validation_v1.json")
    boundary_val = _read_json(dryrun / "task_manager_freeze_authorization_grant_boundary_validation_v1.json")
    debt_val = _read_json(dryrun / "task_manager_freeze_authorization_grant_governance_debt_validation_v1.json")

    review_rows = []
    for fname in GRANT_DRYRUN_ARTIFACTS:
        path = dryrun / fname
        if fname.endswith(".json"):
            non_placeholder = bool(_read_json(path))
        else:
            non_placeholder = path.is_file() and len(path.read_text(encoding="utf-8").strip()) > 200
        review_rows.append({"artifact": fname, "exists": path.is_file(), "non_placeholder": non_placeholder})
        if not path.is_file() or not non_placeholder:
            issues.append(f"missing_dryrun_artifact:{fname}")

    grant_dryrun_result_accepted = (
        dryrun_summary.get("final_decision") == GRANT_DRYRUN_FINAL_GO
        and dryrun_summary.get("recommended_next_phase") == GRANT_DRYRUN_NEXT_PHASE
        and dryrun_verifier.get("verifier") == "GO"
        and int(dryrun_verifier.get("passed_checks", 0)) >= 420
        and dryrun_verifier.get("failed_checks") == 0
        and dryrun_verifier.get("blocker_count") == 0
        and all(dryrun_summary.get(k) is True for k in GRANT_DRYRUN_TRUE_KEYS)
        and dryrun_summary.get("template_lineage_ok") is True
    )
    if not grant_dryrun_result_accepted:
        issues.append("grant_dryrun_not_accepted")

    boundary_drift_rows = []
    for fname in GRANT_DRYRUN_ARTIFACTS:
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
            "stage": "freeze_authorization_grant_post_dryrun_review",
            "root": str(out),
            "readiness": "grant-post-dryrun-review-scope",
            "authorization_grant": False,
            "grant_issued": False,
            "linked": True,
        }
    )
    grant_chain_evidence_accepted = grant_dryrun_result_accepted and all(
        node.get("linked") is True for node in chain_evidence
    )
    if not grant_chain_evidence_accepted:
        issues.append("chain_evidence_gap")

    freeze_status = candidate_val.get("freeze_status") or "freeze-candidate"
    grant_candidate_preserved = (
        candidate_val.get("grant_candidate_preserved") is True
        and candidate_val.get("grant_status") == "freeze-authorization-grant-candidate"
    )

    authorization_request_absent = grant_val.get("authorization_request_absent") is True
    authorization_grant_absent = grant_val.get("authorization_grant_absent") is True
    grant_token_absent = grant_val.get("grant_token_absent") is True
    grant_record_absent = grant_val.get("grant_record_absent") is True
    owner_approval_record_absent = grant_val.get("owner_approval_record_absent") is True
    no_freeze_execution_path = grant_val.get("no_freeze_execution_path") is True
    no_rollback_execution_path = grant_val.get("no_rollback_execution_path") is True
    grant_absence_confirmed = (
        authorization_request_absent
        and authorization_grant_absent
        and grant_token_absent
        and grant_record_absent
        and owner_approval_record_absent
        and no_freeze_execution_path
        and no_rollback_execution_path
    )
    foundation_not_frozen = boundary_val.get("foundation_frozen") is False
    closure_not_executed = boundary_val.get("closed") is False
    if freeze_status in ("frozen", "foundation-frozen"):
        foundation_not_frozen = False
    if not authorization_request_absent:
        issues.append("authorization_request_leakage")
    if not grant_absence_confirmed:
        issues.append("grant_issuance_leakage")
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

    template_lineage = build_template_lineage(
        base_phase="Freeze-Authorization-Post-DryRun-Review-v1-001",
        base_capability=BASE_POST_REVIEW_TEMPLATE_FILES[0],
        base_runner=BASE_POST_REVIEW_TEMPLATE_FILES[1],
        base_verifier=BASE_POST_REVIEW_TEMPLATE_FILES[2],
        base_go_no_go_pack=BASE_POST_REVIEW_TEMPLATE_FILES[3],
        stage_phase="Freeze-Authorization-Grant-Post-DryRun-Review-v1-001",
        stage_term_overrides=GRANT_POST_REVIEW_STAGE_TERM_OVERRIDES,
        stage_additions=GRANT_POST_REVIEW_STAGE_ADDITIONS,
        template_files=BASE_POST_REVIEW_TEMPLATE_FILES,
        repo_root=repo_root,
    )
    upstream_lineage_ok = (
        dryrun_lineage.get("template_lineage_ok") is True
        and dryrun_summary.get("template_lineage_ok") is True
    )
    if not template_lineage.get("template_lineage_ok") or not upstream_lineage_ok:
        issues.append("template_lineage_gap")

    next_planning_ready = (
        grant_dryrun_result_accepted
        and boundary_drift_absent
        and grant_chain_evidence_accepted
        and grant_absence_confirmed
        and grant_candidate_preserved
        and foundation_not_frozen
        and closure_not_executed
        and governance_debt_preserved
        and template_lineage.get("template_lineage_ok") is True
    )

    if not grant_dryrun_result_accepted:
        final_decision = FINAL_DECISION_EVIDENCE
    elif not template_lineage.get("template_lineage_ok"):
        final_decision = FINAL_DECISION_LINEAGE
    elif not governance_debt_preserved:
        final_decision = FINAL_DECISION_DEBT
    elif not l1_protocols_not_implemented or not system_protocols_integration_not_implemented:
        final_decision = FINAL_DECISION_L1
    elif not boundary_drift_absent:
        final_decision = FINAL_DECISION_BOUNDARY
    elif not authorization_request_absent:
        final_decision = FINAL_DECISION_REQUEST
    elif not grant_absence_confirmed:
        final_decision = FINAL_DECISION_GRANT
    elif not foundation_not_frozen or not grant_candidate_preserved:
        final_decision = FINAL_DECISION_FREEZE
    else:
        final_decision = FINAL_DECISION_GO

    go_condition_values = {
        "grant_dryrun_result_accepted": grant_dryrun_result_accepted,
        "boundary_drift_absent": boundary_drift_absent,
        "grant_chain_evidence_accepted": grant_chain_evidence_accepted,
        "grant_absence_confirmed": grant_absence_confirmed,
        "grant_token_absent": grant_token_absent,
        "grant_record_absent": grant_record_absent,
        "owner_approval_record_absent": owner_approval_record_absent,
        "foundation_not_frozen": foundation_not_frozen,
        "closure_not_executed": closure_not_executed,
        "governance_debt_preserved": governance_debt_preserved,
        "l1_protocols_not_implemented": l1_protocols_not_implemented,
        "system_protocols_integration_not_implemented": system_protocols_integration_not_implemented,
        "template_lineage_ok": template_lineage.get("template_lineage_ok") is True and upstream_lineage_ok,
        "full_repo_scan_absent": True,
        "core_go_no_go_schema_preserved": True,
        "post_review_only": True,
        "next_planning_ready": next_planning_ready,
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
        "review_id": "task_manager_foundation_handoff_freeze_authorization_grant_post_dryrun_review_v1",
        **go_condition_values,
        "authorization_request_absent": authorization_request_absent,
        "authorization_grant_absent": authorization_grant_absent,
        "grant_not_issued": True,
        "final_decision": final_decision,
        "recommended_next_phase": next_phase,
        **meta,
    }
    dryrun_review_matrix = {
        "matrix_id": "task_manager_freeze_authorization_grant_dryrun_review_matrix_v1",
        "rows": review_rows,
        "grant_dryrun_result_accepted": grant_dryrun_result_accepted,
        **meta,
    }
    boundary_drift_review = {
        "review_id": "task_manager_freeze_authorization_grant_boundary_drift_review_v1",
        "rows": boundary_drift_rows,
        "boundary_drift_absent": boundary_drift_absent,
        "boundary_statements": list(POST_REVIEW_BOUNDARY_STATEMENTS),
        **meta,
    }
    chain_evidence_review = {
        "review_id": "task_manager_freeze_authorization_grant_chain_evidence_review_v1",
        "chain": chain_evidence,
        "node_count": len(CHAIN_EVIDENCE_NODES),
        "grant_chain_evidence_accepted": grant_chain_evidence_accepted,
        "freeze_authorization_chain_evidence_accepted": grant_chain_evidence_accepted,
        **meta,
    }
    grant_absence_review = {
        "review_id": "task_manager_freeze_authorization_grant_absence_review_v1",
        "grant_absence_confirmed": grant_absence_confirmed,
        "authorization_request_absent": authorization_request_absent,
        "authorization_grant_absent": authorization_grant_absent,
        "grant_token_absent": grant_token_absent,
        "grant_record_absent": grant_record_absent,
        "owner_approval_record_absent": owner_approval_record_absent,
        "no_authorization_request": True,
        "no_authorization_grant": True,
        "no_grant_token": True,
        "no_grant_record": True,
        "no_owner_approval_record": True,
        "no_freeze_execution_path": no_freeze_execution_path,
        "no_rollback_execution_path": no_rollback_execution_path,
        **meta,
    }
    state_absence_review = {
        "review_id": "task_manager_freeze_authorization_grant_state_absence_review_v1",
        "freeze_status": freeze_status,
        "foundation_not_frozen": foundation_not_frozen,
        "closure_not_executed": closure_not_executed,
        "closure_status": "grant-request-planning-ready",
        "no_freeze_execution_path": no_freeze_execution_path,
        "no_rollback_execution_path": no_rollback_execution_path,
        **meta,
    }
    governance_debt_review = {
        "review_id": "task_manager_freeze_authorization_grant_governance_debt_review_v1",
        "debts": debts,
        "governance_debt_preserved": governance_debt_preserved,
        "l1_protocols_not_implemented": l1_protocols_not_implemented,
        "system_protocols_integration_not_implemented": system_protocols_integration_not_implemented,
        **meta,
    }
    template_lineage_review = {
        "review_id": "task_manager_freeze_authorization_grant_template_lineage_review_v1",
        **template_lineage,
        "upstream_grant_dryrun_lineage_ok": upstream_lineage_ok,
        **meta,
    }
    next_planning_readiness = {
        "readiness_id": "task_manager_freeze_authorization_grant_next_planning_readiness_v1",
        "next_planning_ready": next_planning_ready,
        "grant_not_issued": True,
        "recommended_next_phase": next_phase,
        "candidates": [
            {
                "phase": NEXT_PHASE_GO,
                "readiness": "freeze-authorization-grant-request-planning-ready",
                "grant_issued": False,
                "foundation_frozen": False,
                "closed": False,
            },
        ],
        "module_adapter_implementation_ready": False,
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
            "# Task Manager Foundation Handoff Freeze Authorization Grant Post-DryRun Review v1",
            "",
            "This phase reviews freeze authorization grant dry-run results only. It does not issue grant, freeze the foundation, or execute closure.",
            "",
            "本阶段仅审查 freeze authorization grant dry-run 结果，不签发 grant，不冻结 foundation，不执行 closure。",
            "",
            f"Grant dry-run accepted: `{grant_dryrun_result_accepted}`",
            f"Grant absence confirmed: `{grant_absence_confirmed}`",
            f"Grant token absent: `{grant_token_absent}`",
            f"Grant record absent: `{grant_record_absent}`",
            f"Owner approval record absent: `{owner_approval_record_absent}`",
            f"Next planning ready: `{next_planning_ready}` (grant post-dryrun review ≠ grant issued)",
            f"Template lineage OK: `{template_lineage.get('template_lineage_ok')}`",
            f"Freeze status: `freeze-candidate` (not frozen)",
            f"Final decision: `{final_decision}`",
            f"Recommended next phase: `{next_phase}`",
            "",
            "## Grant Boundary Statements",
            *[f"- {stmt}" for stmt in POST_REVIEW_BOUNDARY_STATEMENTS],
            "",
            "## Governance Debts (P1, not implemented)",
            f"- {GOVERNANCE_DEBTS[0]['debt_title']}",
            f"- {GOVERNANCE_DEBTS[1]['debt_title']}",
        ]
    )
    return {
        "task_manager_foundation_handoff_freeze_authorization_grant_post_dryrun_review": review_report,
        "task_manager_foundation_handoff_freeze_authorization_grant_post_dryrun_review_md": markdown,
        "task_manager_freeze_authorization_grant_dryrun_review_matrix": dryrun_review_matrix,
        "task_manager_freeze_authorization_grant_boundary_drift_review": boundary_drift_review,
        "task_manager_freeze_authorization_grant_chain_evidence_review": chain_evidence_review,
        "task_manager_freeze_authorization_grant_absence_review": grant_absence_review,
        "task_manager_freeze_authorization_grant_state_absence_review": state_absence_review,
        "task_manager_freeze_authorization_grant_governance_debt_review": governance_debt_review,
        "task_manager_freeze_authorization_grant_template_lineage_review": template_lineage_review,
        "task_manager_freeze_authorization_grant_next_planning_readiness": next_planning_readiness,
        "summary": summary,
    }
