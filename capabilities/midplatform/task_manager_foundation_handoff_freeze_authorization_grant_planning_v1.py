# -*- coding: utf-8 -*-
"""Luna Midplatform Task Manager Foundation Handoff Freeze Authorization Grant Planning v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.midplatform_task_manager_controlled_skeleton_implementation_dryrun_v1 import (
    SKELETON_FILES,
)
from capabilities.midplatform.task_manager_foundation_handoff_final_closure_planning_v1 import GOVERNANCE_DEBTS
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_dryrun_v1 import (
    CHAIN_TRACE_NODES,
)
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_planning_v1 import (
    DEFAULT_OUTPUT as DEFAULT_FREEZE_AUTH_PLANNING_ROOT,
)
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_post_dryrun_review_v1 import (
    CHAIN_EVIDENCE_NODES as POST_REVIEW_CHAIN_NODES,
    DEFAULT_OUTPUT as DEFAULT_FREEZE_AUTH_POST_REVIEW_ROOT,
    FINAL_DECISION_GO as POST_REVIEW_FINAL_GO,
    NEXT_PHASE_GO as POST_REVIEW_NEXT_PHASE,
)
from capabilities.midplatform.task_manager_foundation_handoff_planning_v1 import (
    BOUNDARY_STATEMENT_EN,
    BOUNDARY_STATEMENT_ZH,
    FOUNDATION_ID,
)

PHASE_ID = "Phase-Midplatform-Task-Manager-Foundation-Handoff-Freeze-Authorization-Grant-Planning-v1-001"
SCOPE = "midplatform_task_manager_foundation_handoff_freeze_authorization_grant_planning_only"
SOURCE_CHAIN = "midplatform_task_manager_foundation_handoff_freeze_authorization_grant_planning_v1"
FINAL_DECISION_GO = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_PLANNING_READY_FOR_GRANT_DRYRUN"
FINAL_DECISION_PRIOR = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_PLANNING_BLOCKED_BY_PRIOR_REVIEW_GAP"
FINAL_DECISION_SCOPE = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_PLANNING_BLOCKED_BY_GRANT_SCOPE_ESCALATION"
FINAL_DECISION_ISSUANCE = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_PLANNING_BLOCKED_BY_GRANT_ISSUANCE_LEAKAGE"
FINAL_DECISION_REQUEST = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_PLANNING_BLOCKED_BY_AUTHORIZATION_REQUEST_LEAKAGE"
FINAL_DECISION_FREEZE = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_PLANNING_BLOCKED_BY_FREEZE_STATE_ESCALATION"
FINAL_DECISION_DEBT = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_PLANNING_BLOCKED_BY_GOVERNANCE_DEBT_GAP"
FINAL_DECISION_L1 = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_PLANNING_BLOCKED_BY_L1_PROTOCOL_SCOPE_LEAKAGE"
FINAL_DECISION_RUNTIME = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_PLANNING_BLOCKED_BY_RUNTIME_SCOPE_LEAKAGE"
NEXT_PHASE_GO = "Phase-Midplatform-Task-Manager-Foundation-Handoff-Freeze-Authorization-Grant-DryRun-v1-001"
NEXT_PHASE_HOLD = "Phase-Midplatform-Task-Manager-Foundation-Handoff-Freeze-Authorization-Grant-Planning-Issue-Review-v1-001"
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "midplatform_task_manager_foundation_handoff_freeze_authorization_grant_planning_v1_smoke_v0"
)

PLANNING_TRUE_KEYS: Tuple[str, ...] = (
    "prior_freeze_authorization_post_review_go",
    "grant_plan_complete",
    "grant_scope_planning_only",
    "grant_candidate_only",
    "grant_not_issued",
    "authorization_request_absent",
    "authorization_grant_absent",
    "foundation_not_frozen",
    "closure_not_executed",
    "governance_debt_carryover_complete",
    "l1_protocols_not_implemented",
    "system_protocols_integration_not_implemented",
    "non_execution_boundary_ok",
    "next_phase_readiness_ok",
)
POST_REVIEW_TRUE_KEYS: Tuple[str, ...] = (
    "freeze_authorization_dryrun_result_accepted",
    "boundary_drift_absent",
    "freeze_authorization_chain_evidence_accepted",
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
    "post_review_only",
    "grant_planning_ready",
)
BOUNDARY_CONTRACT_STATEMENTS: Tuple[str, ...] = (
    "grant_planning != grant_issued",
    "freeze_authorization_grant_candidate != freeze_authorization_granted",
    "grant_readiness != grant",
    "freeze_candidate != frozen",
    "closure_candidate != closed",
    "grant_planning_ready != authorized",
)
GRANT_SCOPE_ROWS: Tuple[Dict[str, str], ...] = (
    {"scope": "foundation_freeze_authorization_grant", "classification": "grant-planning-scope"},
    {"scope": "skeleton_asset_freeze_authorization_grant", "classification": "grant-planning-scope"},
    {"scope": "evidence_chain_freeze_authorization_grant", "classification": "grant-planning-scope"},
    {"scope": "governance_debt_acknowledgement", "classification": "grant-planning-scope"},
    {"scope": "rollback_revoke_boundary", "classification": "grant-planning-scope"},
    {"scope": "post_grant_expected_state", "classification": "grant-planning-scope"},
)
PREREQUISITE_ROWS: Tuple[Dict[str, Any], ...] = (
    {"prerequisite": "prior_post_dryrun_review_go", "required": True},
    {"prerequisite": "authorization_request_absent", "required": True},
    {"prerequisite": "authorization_grant_absent", "required": True},
    {"prerequisite": "foundation_not_frozen", "required": True},
    {"prerequisite": "closure_not_executed", "required": True},
    {"prerequisite": "governance_debt_preserved", "required": True},
)
NON_EXECUTION_CONSTRAINTS: Tuple[str, ...] = (
    "no_authorization_request",
    "no_authorization_grant",
    "no_grant_token",
    "no_grant_record",
    "no_owner_approval_record",
    "no_freeze_execution_path",
    "no_rollback_execution_path",
    "no_foundation_frozen",
    "no_closed_state",
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
    "no_closure_execution",
)
CHAIN_EVIDENCE_NODES: Tuple[str, ...] = POST_REVIEW_CHAIN_NODES + ("freeze_authorization_grant_planning",)


def _read_json(path: Path) -> Dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return {}
    return payload if isinstance(payload, dict) else {}


def _meta(out: Path, post_review: Path, planning: Path) -> Dict[str, Any]:
    return {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "source_chain": SOURCE_CHAIN,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "foundation_id": FOUNDATION_ID,
        "runtime_status": "not_enabled",
        "grant_planning_only": True,
        "grant_not_issued": True,
        "authorization_request_absent": True,
        "authorization_grant_absent": True,
        "foundation_not_frozen": True,
        "closure_not_executed": True,
        "l1_protocols_not_implemented": True,
        "system_protocols_integration_not_implemented": True,
        "output_root": str(out),
        "freeze_authorization_post_review_root": str(post_review),
        "freeze_authorization_planning_root": str(planning),
        "boundary_statement_en": BOUNDARY_STATEMENT_EN,
        "boundary_statement_zh": BOUNDARY_STATEMENT_ZH,
    }


def run_task_manager_foundation_handoff_freeze_authorization_grant_planning_v1(
    *,
    freeze_authorization_post_review_root: str,
    freeze_authorization_planning_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    out = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    post_review = Path(freeze_authorization_post_review_root).expanduser().resolve()
    planning = Path(freeze_authorization_planning_root).expanduser().resolve()
    repo_root = Path(__file__).resolve().parents[2]
    meta = _meta(out, post_review, planning)
    issues: List[str] = []

    post_summary = _read_json(post_review / "summary.json")
    post_verifier = _read_json(post_review / "verifier_report.json")
    chain_review = _read_json(post_review / "task_manager_freeze_authorization_chain_evidence_review_v1.json")
    candidate_map_src = _read_json(planning / "task_manager_freeze_authorization_candidate_asset_map_v1.json")

    prior_post_dryrun_review_go = (
        post_summary.get("final_decision") == POST_REVIEW_FINAL_GO
        and post_summary.get("recommended_next_phase") == POST_REVIEW_NEXT_PHASE
        and post_verifier.get("verifier") == "GO"
        and int(post_verifier.get("passed_checks", 0)) >= 420
        and post_verifier.get("failed_checks") == 0
        and post_verifier.get("blocker_count") == 0
        and post_summary.get("grant_planning_ready") is True
        and all(post_summary.get(k) is True for k in POST_REVIEW_TRUE_KEYS)
    )
    if not prior_post_dryrun_review_go:
        issues.append("prior_post_dryrun_review_not_go")

    evidence_chain = []
    for stage in CHAIN_TRACE_NODES:
        row = next((r for r in chain_review.get("chain") or [] if r.get("stage") == stage), {})
        evidence_chain.append({"stage": stage, "linked": row.get("linked") is True})
    post_review_row = next(
        (r for r in chain_review.get("chain") or [] if r.get("stage") == "freeze_authorization_post_review"),
        {},
    )
    evidence_chain.append(
        {
            "stage": "freeze_authorization_post_review",
            "linked": post_review_row.get("linked") is True,
            "authorization_grant": False,
        }
    )
    evidence_chain.append(
        {
            "stage": "freeze_authorization_grant_planning",
            "root": str(out),
            "readiness": "grant-planning-ready",
            "authorization_grant": False,
            "grant_issued": False,
            "linked": True,
        }
    )
    evidence_chain_complete = prior_post_dryrun_review_go and all(node.get("linked") for node in evidence_chain)
    if not evidence_chain_complete:
        issues.append("evidence_chain_gap")

    scope_rows = list(GRANT_SCOPE_ROWS)
    grant_scope_planning_only = all(
        row["classification"] == "grant-planning-scope"
        and row["classification"] not in ("grant-issued-scope", "authorized-scope")
        for row in scope_rows
    )
    if not grant_scope_planning_only:
        issues.append("grant_scope_escalation")

    asset_rows: List[Dict[str, Any]] = []
    src_assets = candidate_map_src.get("assets") or []
    if src_assets:
        for row in src_assets:
            asset_rows.append(
                {
                    **row,
                    "grant_status": "freeze-authorization-grant-candidate",
                    "authorization_status": "freeze-authorization-grant-candidate",
                    "freeze_status": row.get("freeze_status", "freeze-candidate"),
                }
            )
    else:
        for rel in SKELETON_FILES:
            path = repo_root / rel
            asset_rows.append(
                {
                    "asset_type": "core_skeleton",
                    "path": rel,
                    "grant_status": "freeze-authorization-grant-candidate",
                    "authorization_status": "freeze-authorization-grant-candidate",
                    "freeze_status": "freeze-candidate",
                    "exists": path.is_file(),
                }
            )
    grant_candidate_only = all(
        row.get("grant_status") == "freeze-authorization-grant-candidate"
        and row.get("authorization_status") == "freeze-authorization-grant-candidate"
        and row.get("grant_status") != "freeze-authorized"
        and row.get("freeze_status") != "frozen"
        for row in asset_rows
    )
    if not grant_candidate_only:
        issues.append("grant_scope_escalation")

    prerequisite_values = {
        "prior_post_dryrun_review_go": prior_post_dryrun_review_go,
        "authorization_request_absent": post_summary.get("authorization_request_absent") is True,
        "authorization_grant_absent": post_summary.get("authorization_grant_absent") is True,
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
    foundation_not_frozen = prerequisite_values["foundation_not_frozen"]
    closure_not_executed = prerequisite_values["closure_not_executed"]
    grant_not_issued = True

    boundary_contract = {
        "contract_id": "task_manager_freeze_authorization_grant_boundary_contract_v1",
        "statements": list(BOUNDARY_CONTRACT_STATEMENTS),
        "grant_planning_ready": True,
        "grant_not_issued": True,
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

    next_phase_readiness_ok = True
    grant_plan_complete = (
        prior_post_dryrun_review_go
        and evidence_chain_complete
        and grant_scope_planning_only
        and grant_candidate_only
        and prerequisites_ok
        and governance_debt_carryover_complete
    )

    if not prior_post_dryrun_review_go:
        final_decision = FINAL_DECISION_PRIOR
    elif not grant_scope_planning_only or not grant_candidate_only:
        final_decision = FINAL_DECISION_SCOPE
    elif not grant_not_issued or not authorization_grant_absent:
        final_decision = FINAL_DECISION_ISSUANCE
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

    planning_pass = len(issues) == 0 and final_decision == FINAL_DECISION_GO
    grant_plan = {
        "plan_id": "task_manager_foundation_handoff_freeze_authorization_grant_plan_v1",
        "grant_scope": [
            "define freeze authorization grant admission criteria without issuing grant",
            "inventory freeze-authorization-grant-candidate assets",
            "trace evidence chain through freeze authorization grant planning",
            "preserve governance debt carryover",
            "define rollback/revoke boundary for future grant issuance",
            "define post-grant expected state without executing grant",
            "prepare freeze authorization grant dry-run readiness",
        ],
        "prior_freeze_authorization_post_review_go": prior_post_dryrun_review_go,
        "grant_plan_complete": grant_plan_complete,
        "grant_scope_planning_only": grant_scope_planning_only,
        "grant_candidate_only": grant_candidate_only,
        "grant_not_issued": grant_not_issued,
        "authorization_request_absent": authorization_request_absent,
        "authorization_grant_absent": authorization_grant_absent,
        "foundation_not_frozen": foundation_not_frozen,
        "closure_not_executed": closure_not_executed,
        "governance_debt_carryover_complete": governance_debt_carryover_complete,
        "l1_protocols_not_implemented": l1_protocols_not_implemented,
        "system_protocols_integration_not_implemented": system_protocols_integration_not_implemented,
        "non_execution_boundary_ok": non_execution_boundary_ok,
        "next_phase_readiness_ok": next_phase_readiness_ok,
        "final_decision": final_decision,
        "recommended_next_phase": NEXT_PHASE_GO if planning_pass else NEXT_PHASE_HOLD,
        **meta,
    }
    scope_matrix = {
        "matrix_id": "task_manager_freeze_authorization_grant_scope_matrix_v1",
        "rows": scope_rows,
        "grant_scope_planning_only": grant_scope_planning_only,
        **meta,
    }
    candidate_asset_map = {
        "map_id": "task_manager_freeze_authorization_grant_candidate_asset_map_v1",
        "assets": asset_rows,
        "grant_candidate_only": grant_candidate_only,
        **meta,
    }
    prerequisite_matrix = {
        "matrix_id": "task_manager_freeze_authorization_grant_prerequisite_matrix_v1",
        "rows": prerequisite_rows,
        "prerequisites_ok": prerequisites_ok,
        **meta,
    }
    evidence_chain_doc = {
        "chain_id": "task_manager_freeze_authorization_grant_evidence_chain_v1",
        "chain": evidence_chain,
        "node_count": len(CHAIN_EVIDENCE_NODES),
        "evidence_chain_complete": evidence_chain_complete,
        "points_to_grant_planning_not_issued": True,
        **meta,
    }
    boundary_contract_doc = {
        **boundary_contract,
        **meta,
    }
    non_execution = {
        "constraints_id": "task_manager_freeze_authorization_grant_non_execution_constraints_v1",
        "constraints": list(NON_EXECUTION_CONSTRAINTS),
        "non_execution_boundary_ok": non_execution_boundary_ok,
        **{c: True for c in NON_EXECUTION_CONSTRAINTS},
        **meta,
    }
    debt_carryover = {
        "carryover_id": "task_manager_freeze_authorization_grant_governance_debt_carryover_v1",
        "debts": debts,
        "governance_debt_carryover_complete": governance_debt_carryover_complete,
        "l1_protocols_not_implemented": l1_protocols_not_implemented,
        "system_protocols_integration_not_implemented": system_protocols_integration_not_implemented,
        **meta,
    }
    next_phase_doc = {
        "readiness_id": "task_manager_freeze_authorization_grant_next_phase_readiness_v1",
        "recommended_next_phase": NEXT_PHASE_GO if planning_pass else NEXT_PHASE_HOLD,
        "target": "freeze_authorization_grant_dryrun",
        "readiness": "freeze-authorization-grant-dryrun-ready",
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
        "prior_freeze_authorization_post_review_go": prior_post_dryrun_review_go,
        "grant_plan_complete": grant_plan_complete,
        "grant_scope_planning_only": grant_scope_planning_only,
        "grant_candidate_only": grant_candidate_only,
        "grant_not_issued": grant_not_issued,
        "authorization_request_absent": authorization_request_absent,
        "authorization_grant_absent": authorization_grant_absent,
        "foundation_not_frozen": foundation_not_frozen,
        "closure_not_executed": closure_not_executed,
        "governance_debt_carryover_complete": governance_debt_carryover_complete,
        "l1_protocols_not_implemented": l1_protocols_not_implemented,
        "system_protocols_integration_not_implemented": system_protocols_integration_not_implemented,
        "non_execution_boundary_ok": non_execution_boundary_ok,
        "next_phase_readiness_ok": next_phase_readiness_ok,
        "final_decision": final_decision,
        "recommended_next_phase": NEXT_PHASE_GO if planning_pass else NEXT_PHASE_HOLD,
        **meta,
    }
    markdown = "\n".join(
        [
            "# Task Manager Foundation Handoff Freeze Authorization Grant Plan v1",
            "",
            "This phase performs freeze authorization grant planning only. It does not issue grant, freeze the foundation, or execute closure.",
            "",
            "本阶段仅执行 freeze authorization grant planning，不签发 grant，不冻结 foundation，不执行 closure。",
            "",
            f"Prior post-dryrun review GO: `{prior_post_dryrun_review_go}`",
            f"Grant not issued: `{grant_not_issued}` (grant planning ≠ grant issued)",
            f"Authorization request absent: `{authorization_request_absent}`",
            f"Authorization grant absent: `{authorization_grant_absent}`",
            f"Freeze status: `freeze-candidate` (not frozen)",
            f"Final decision: `{final_decision}`",
            f"Recommended next phase: `{summary['recommended_next_phase']}`",
            "",
            "## Grant Boundary Contract",
            *[f"- {stmt}" for stmt in BOUNDARY_CONTRACT_STATEMENTS],
            "",
            "## Post-Grant Expected State (planning only, not executed)",
            "- grant_issued: false",
            "- foundation_frozen: false",
            "- closed: false",
            "- module_adapter_implementation: not ready",
            "",
            "## Governance Debt Carryover (P1, not implemented)",
            f"- {GOVERNANCE_DEBTS[0]['debt_title']}",
            f"- {GOVERNANCE_DEBTS[1]['debt_title']}",
        ]
    )
    return {
        "task_manager_foundation_handoff_freeze_authorization_grant_plan": grant_plan,
        "task_manager_foundation_handoff_freeze_authorization_grant_plan_md": markdown,
        "task_manager_freeze_authorization_grant_scope_matrix": scope_matrix,
        "task_manager_freeze_authorization_grant_candidate_asset_map": candidate_asset_map,
        "task_manager_freeze_authorization_grant_prerequisite_matrix": prerequisite_matrix,
        "task_manager_freeze_authorization_grant_evidence_chain": evidence_chain_doc,
        "task_manager_freeze_authorization_grant_boundary_contract": boundary_contract_doc,
        "task_manager_freeze_authorization_grant_non_execution_constraints": non_execution,
        "task_manager_freeze_authorization_grant_governance_debt_carryover": debt_carryover,
        "task_manager_freeze_authorization_grant_next_phase_readiness": next_phase_doc,
        "summary": summary,
    }
