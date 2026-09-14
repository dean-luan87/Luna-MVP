# -*- coding: utf-8 -*-
"""Luna Midplatform Task Manager Foundation Handoff Freeze Authorization Planning v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.midplatform_task_manager_controlled_skeleton_implementation_dryrun_v1 import (
    SKELETON_FILES,
)
from capabilities.midplatform.task_manager_foundation_handoff_final_closure_planning_v1 import (
    DEFAULT_OUTPUT as DEFAULT_FINAL_CLOSURE_PLANNING_ROOT,
    GOVERNANCE_DEBTS,
)
from capabilities.midplatform.task_manager_foundation_handoff_final_closure_post_dryrun_review_v1 import (
    CHAIN_EVIDENCE_NODES,
    DEFAULT_OUTPUT as DEFAULT_FINAL_CLOSURE_POST_REVIEW_ROOT,
    FINAL_DECISION_GO as FINAL_POST_REVIEW_FINAL_GO,
    NEXT_PHASE_GO as FINAL_POST_REVIEW_NEXT_PHASE,
)
from capabilities.midplatform.task_manager_foundation_handoff_planning_v1 import (
    BOUNDARY_STATEMENT_EN,
    BOUNDARY_STATEMENT_ZH,
    FOUNDATION_ID,
)

PHASE_ID = "Phase-Midplatform-Task-Manager-Foundation-Handoff-Freeze-Authorization-Planning-v1-001"
SCOPE = "midplatform_task_manager_foundation_handoff_freeze_authorization_planning_only"
SOURCE_CHAIN = "midplatform_task_manager_foundation_handoff_freeze_authorization_planning_v1"
FINAL_DECISION_GO = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_PLANNING_READY_FOR_DRYRUN"
FINAL_DECISION_PRIOR = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_PLANNING_BLOCKED_BY_PRIOR_REVIEW_GAP"
FINAL_DECISION_SCOPE = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_PLANNING_BLOCKED_BY_AUTHORIZATION_SCOPE_LEAKAGE"
FINAL_DECISION_GRANT = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_PLANNING_BLOCKED_BY_AUTHORIZATION_GRANT_LEAKAGE"
FINAL_DECISION_FREEZE = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_PLANNING_BLOCKED_BY_FREEZE_STATE_ESCALATION"
FINAL_DECISION_DEBT = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_PLANNING_BLOCKED_BY_GOVERNANCE_DEBT_GAP"
FINAL_DECISION_L1 = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_PLANNING_BLOCKED_BY_L1_PROTOCOL_SCOPE_LEAKAGE"
FINAL_DECISION_RUNTIME = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_PLANNING_BLOCKED_BY_RUNTIME_SCOPE_LEAKAGE"
NEXT_PHASE_GO = "Phase-Midplatform-Task-Manager-Foundation-Handoff-Freeze-Authorization-DryRun-v1-001"
NEXT_PHASE_HOLD = "Phase-Midplatform-Task-Manager-Foundation-Handoff-Freeze-Authorization-Planning-Issue-Review-v1-001"
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "midplatform_task_manager_foundation_handoff_freeze_authorization_planning_v1_smoke_v0"
)

POST_REVIEW_TRUE_KEYS: Tuple[str, ...] = (
    "final_closure_dryrun_result_accepted",
    "boundary_drift_absent",
    "final_chain_evidence_accepted",
    "freeze_candidate_preserved",
    "closure_candidate_preserved",
    "candidate_semantics_preserved",
    "non_execution_boundary_ok",
    "downstream_reference_scope_ok",
    "governance_debt_preserved",
    "l1_protocols_not_implemented",
    "system_protocols_integration_not_implemented",
    "post_review_only",
    "authorization_planning_ready",
)
BOUNDARY_CONTRACT_STATEMENTS: Tuple[str, ...] = (
    "freeze_authorization_planning != freeze_authorization_grant",
    "freeze_authorization_candidate != freeze_authorized",
    "freeze_candidate != frozen",
    "closure_candidate != closed",
    "authorization-planning-ready != authorized",
)
AUTHORIZATION_SCOPE_ROWS: Tuple[Dict[str, str], ...] = (
    {"scope": "foundation_freeze_authorization", "classification": "authorization-planning-scope"},
    {"scope": "skeleton_asset_freeze_authorization", "classification": "authorization-planning-scope"},
    {"scope": "evidence_chain_freeze_authorization", "classification": "authorization-planning-scope"},
    {"scope": "governance_debt_acknowledgement", "classification": "authorization-planning-scope"},
    {"scope": "rollback_revocation_boundary", "classification": "authorization-planning-scope"},
)
READINESS_ROWS: Tuple[Dict[str, Any], ...] = (
    {"target": "freeze_authorization_dryrun", "readiness": "freeze-authorization-dryrun-ready", "freeze_authorized": False},
    {"target": "module_adapter_implementation", "readiness": "not-ready", "freeze_authorized": False},
)
NON_EXECUTION_CONSTRAINTS: Tuple[str, ...] = (
    "no_authorization_request",
    "no_authorization_grant",
    "no_freeze_execution_path",
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


def _read_json(path: Path) -> Dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return {}
    return payload if isinstance(payload, dict) else {}


def _meta(out: Path, post_review: Path, final_planning: Path) -> Dict[str, Any]:
    return {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "source_chain": SOURCE_CHAIN,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "foundation_id": FOUNDATION_ID,
        "runtime_status": "not_enabled",
        "freeze_authorization_planning_only": True,
        "authorization_not_granted": True,
        "foundation_not_frozen": True,
        "closure_not_executed": True,
        "l1_protocols_not_implemented": True,
        "system_protocols_integration_not_implemented": True,
        "output_root": str(out),
        "final_closure_post_review_root": str(post_review),
        "final_closure_planning_root": str(final_planning),
        "boundary_statement_en": BOUNDARY_STATEMENT_EN,
        "boundary_statement_zh": BOUNDARY_STATEMENT_ZH,
    }


def run_task_manager_foundation_handoff_freeze_authorization_planning_v1(
    *,
    final_closure_post_review_root: str,
    final_closure_planning_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    out = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    post_review = Path(final_closure_post_review_root).expanduser().resolve()
    final_planning = Path(final_closure_planning_root).expanduser().resolve()
    repo_root = Path(__file__).resolve().parents[2]
    meta = _meta(out, post_review, final_planning)
    issues: List[str] = []

    post_summary = _read_json(post_review / "summary.json")
    post_verifier = _read_json(post_review / "verifier_report.json")
    chain_review = _read_json(post_review / "task_manager_final_closure_chain_evidence_review_v1.json")
    freeze_map_src = _read_json(final_planning / "task_manager_final_freeze_candidate_asset_map_v1.json")

    prior_final_review_go = (
        post_summary.get("final_decision") == FINAL_POST_REVIEW_FINAL_GO
        and post_summary.get("recommended_next_phase") == FINAL_POST_REVIEW_NEXT_PHASE
        and post_verifier.get("verifier") == "GO"
        and int(post_verifier.get("passed_checks", 0)) >= 420
        and post_verifier.get("failed_checks") == 0
        and post_verifier.get("blocker_count") == 0
        and all(post_summary.get(k) is True for k in POST_REVIEW_TRUE_KEYS)
    )
    downstream_readiness_gaps: List[str] = []
    if not prior_final_review_go:
        downstream_readiness_gaps.append("prior_final_closure_post_review_not_go")

    evidence_chain = []
    for stage in CHAIN_EVIDENCE_NODES:
        row = next((r for r in chain_review.get("chain") or [] if r.get("stage") == stage), {})
        evidence_chain.append({"stage": stage, "linked": row.get("linked") is True})
    evidence_chain.append(
        {
            "stage": "freeze_authorization_planning",
            "root": str(out),
            "readiness": "authorization-planning-ready",
            "authorization_grant": False,
            "linked": True,
        }
    )
    evidence_chain_paths_declared = len(evidence_chain) >= len(CHAIN_EVIDENCE_NODES) + 1
    planning_node_linked = any(
        node.get("stage") == "freeze_authorization_planning" and node.get("linked") is True
        for node in evidence_chain
    )
    closure_chain_linked = all(
        node.get("linked") is True
        for node in evidence_chain
        if node.get("stage") in CHAIN_EVIDENCE_NODES
    )
    if not closure_chain_linked:
        downstream_readiness_gaps.append("final_closure_evidence_chain_not_linked")
    evidence_chain_complete = planning_node_linked and evidence_chain_paths_declared
    if not evidence_chain_complete:
        issues.append("evidence_chain_gap")

    scope_rows = list(AUTHORIZATION_SCOPE_ROWS)
    authorization_scope_planning_only = all(row["classification"] == "authorization-planning-scope" for row in scope_rows)
    if not authorization_scope_planning_only:
        issues.append("authorization_scope_leakage")

    asset_rows: List[Dict[str, Any]] = []
    src_assets = freeze_map_src.get("assets") or []
    if src_assets:
        for row in src_assets:
            asset_rows.append(
                {
                    **row,
                    "authorization_status": "freeze-authorization-candidate",
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
                    "authorization_status": "freeze-authorization-candidate",
                    "freeze_status": "freeze-candidate",
                    "exists": path.is_file(),
                }
            )
    freeze_authorization_candidate_only = all(
        row.get("authorization_status") in ("freeze-authorization-candidate", "freeze-candidate")
        and row.get("freeze_status") != "frozen"
        for row in asset_rows
    )
    freeze_candidate_preserved = all(row.get("freeze_status") == "freeze-candidate" for row in asset_rows)
    if not freeze_authorization_candidate_only:
        issues.append("authorization_scope_leakage")
    if not freeze_candidate_preserved:
        issues.append("freeze_state_escalation")

    readiness_rows = list(READINESS_ROWS)
    next_phase_readiness_ok = all(
        row.get("readiness") == "freeze-authorization-dryrun-ready" or row.get("readiness") == "not-ready"
        for row in readiness_rows
        if row.get("target") != "module_adapter_implementation"
    ) and all(row.get("freeze_authorized") is False for row in readiness_rows)
    if any(row.get("readiness") == "freeze-authorized" for row in readiness_rows):
        issues.append("authorization_grant_leakage")

    boundary_contract = {
        "contract_id": "task_manager_freeze_authorization_boundary_contract_v1",
        "statements": list(BOUNDARY_CONTRACT_STATEMENTS),
        "authorization_planning_ready": True,
        "authorization_not_granted": True,
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
    authorization_not_granted = True
    foundation_not_frozen = True
    closure_not_executed = True

    freeze_authorization_plan_complete = (
        evidence_chain_complete
        and authorization_scope_planning_only
        and freeze_authorization_candidate_only
        and governance_debt_carryover_complete
    )

    if not authorization_scope_planning_only or not freeze_authorization_candidate_only:
        final_decision = FINAL_DECISION_SCOPE
    elif not authorization_not_granted or any(row.get("readiness") == "freeze-authorized" for row in readiness_rows):
        final_decision = FINAL_DECISION_GRANT
    elif not freeze_candidate_preserved or not foundation_not_frozen:
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
    freeze_auth_plan = {
        "plan_id": "task_manager_foundation_handoff_freeze_authorization_plan_v1",
        "authorization_scope": [
            "define freeze authorization admission criteria without granting authorization",
            "inventory freeze-authorization-candidate assets",
            "trace evidence chain through freeze authorization planning",
            "preserve governance debt carryover",
            "define rollback/revocation boundary for future authorization",
            "prepare freeze authorization dry-run readiness",
        ],
        "candidate_only": True,
        "freeze_authorization_planning_complete": planning_pass,
        "authorization_boundary_declared": True,
        "evidence_chain_paths_declared": evidence_chain_paths_declared,
        "no_execution_performed": True,
        "no_protocol_change": True,
        "prior_final_review_go": prior_final_review_go,
        "freeze_authorization_plan_complete": freeze_authorization_plan_complete,
        "authorization_scope_planning_only": authorization_scope_planning_only,
        "freeze_authorization_candidate_only": freeze_authorization_candidate_only,
        "freeze_candidate_preserved": freeze_candidate_preserved,
        "authorization_not_granted": authorization_not_granted,
        "foundation_not_frozen": foundation_not_frozen,
        "closure_not_executed": closure_not_executed,
        "governance_debt_carryover_complete": governance_debt_carryover_complete,
        "l1_protocols_not_implemented": l1_protocols_not_implemented,
        "system_protocols_integration_not_implemented": system_protocols_integration_not_implemented,
        "non_execution_boundary_ok": non_execution_boundary_ok,
        "next_phase_readiness_ok": next_phase_readiness_ok,
        "final_decision": final_decision,
        "recommended_next_phase": NEXT_PHASE_GO if planning_pass else PHASE_ID,
        **meta,
    }
    scope_matrix = {
        "matrix_id": "task_manager_freeze_authorization_scope_matrix_v1",
        "rows": scope_rows,
        "authorization_scope_planning_only": authorization_scope_planning_only,
        **meta,
    }
    candidate_asset_map = {
        "map_id": "task_manager_freeze_authorization_candidate_asset_map_v1",
        "assets": asset_rows,
        "freeze_authorization_candidate_only": freeze_authorization_candidate_only,
        "freeze_candidate_preserved": freeze_candidate_preserved,
        **meta,
    }
    evidence_chain_doc = {
        "chain_id": "task_manager_freeze_authorization_evidence_chain_v1",
        "chain": evidence_chain,
        "evidence_chain_complete": evidence_chain_complete,
        "evidence_chain_paths_declared": evidence_chain_paths_declared,
        "points_to_planning_not_grant": True,
        **meta,
    }
    boundary_contract_doc = {
        **boundary_contract,
        **meta,
    }
    readiness_matrix = {
        "matrix_id": "task_manager_freeze_authorization_readiness_matrix_v1",
        "rows": readiness_rows,
        "next_phase_readiness_ok": next_phase_readiness_ok,
        **meta,
    }
    debt_carryover = {
        "carryover_id": "task_manager_freeze_authorization_governance_debt_carryover_v1",
        "debts": debts,
        "governance_debt_carryover_complete": governance_debt_carryover_complete,
        "l1_protocols_not_implemented": l1_protocols_not_implemented,
        "system_protocols_integration_not_implemented": system_protocols_integration_not_implemented,
        **meta,
    }
    non_execution = {
        "constraints_id": "task_manager_freeze_authorization_non_execution_constraints_v1",
        "constraints": list(NON_EXECUTION_CONSTRAINTS),
        "non_execution_boundary_ok": non_execution_boundary_ok,
        **{c: True for c in NON_EXECUTION_CONSTRAINTS},
        **meta,
    }
    next_phase_doc = {
        "readiness_id": "task_manager_freeze_authorization_next_phase_readiness_v1",
        "recommended_next_phase": NEXT_PHASE_GO if planning_pass else PHASE_ID,
        "module_adapter_implementation_ready": False,
        "freeze_authorization_granted": False,
        "foundation_frozen": False,
        "closed": False,
        "next_phase_readiness_ok": next_phase_readiness_ok,
        **meta,
    }
    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "candidate_only": True,
        "planning_pass": planning_pass,
        "freeze_authorization_planning_complete": planning_pass,
        "blocker_count": len(issues),
        "issues": issues,
        "downstream_readiness_gaps": downstream_readiness_gaps,
        "downstream_readiness_refs": {
            "final_closure_post_review_root": str(post_review),
            "final_closure_planning_root": str(final_planning),
            "prior_final_review_go": prior_final_review_go,
            "final_closure_post_review_final_decision": post_summary.get("final_decision"),
        },
        "downstream_chain_refs": {
            "closure_evidence_nodes": list(CHAIN_EVIDENCE_NODES),
            "closure_chain_linked": closure_chain_linked,
        },
        "expected_next_phase_refs": {
            "next_phase_on_go": NEXT_PHASE_GO,
            "dryrun_readiness": "freeze-authorization-dryrun-ready",
        },
        "authorization_boundary_declared": True,
        "evidence_chain_paths_declared": evidence_chain_paths_declared,
        "no_execution_performed": True,
        "no_protocol_change": True,
        "prior_final_review_go": prior_final_review_go,
        "freeze_authorization_plan_complete": freeze_authorization_plan_complete,
        "authorization_scope_planning_only": authorization_scope_planning_only,
        "freeze_authorization_candidate_only": freeze_authorization_candidate_only,
        "freeze_candidate_preserved": freeze_candidate_preserved,
        "authorization_not_granted": authorization_not_granted,
        "foundation_not_frozen": foundation_not_frozen,
        "closure_not_executed": closure_not_executed,
        "governance_debt_carryover_complete": governance_debt_carryover_complete,
        "l1_protocols_not_implemented": l1_protocols_not_implemented,
        "system_protocols_integration_not_implemented": system_protocols_integration_not_implemented,
        "non_execution_boundary_ok": non_execution_boundary_ok,
        "next_phase_readiness_ok": next_phase_readiness_ok,
        "final_decision": final_decision,
        "recommended_next_phase": NEXT_PHASE_GO if planning_pass else PHASE_ID,
        **meta,
    }
    markdown = "\n".join(
        [
            "# Task Manager Foundation Handoff Freeze Authorization Plan v1",
            "",
            "This phase performs freeze authorization planning only. It does not grant authorization, freeze the foundation, or execute closure.",
            "",
            "本阶段仅执行 freeze authorization planning，不授予 authorization，不冻结 foundation，不执行 closure。",
            "",
            f"Prior final review GO: `{prior_final_review_go}`",
            f"Authorization not granted: `{authorization_not_granted}`",
            f"Freeze status: `freeze-candidate` (not frozen)",
            f"Final decision: `{final_decision}`",
            f"Recommended next phase: `{summary['recommended_next_phase']}`",
            "",
            "## Authorization Boundary Contract",
            *[f"- {stmt}" for stmt in BOUNDARY_CONTRACT_STATEMENTS],
            "",
            "## Governance Debt Carryover (P1, not implemented)",
            f"- {GOVERNANCE_DEBTS[0]['debt_title']}",
            f"- {GOVERNANCE_DEBTS[1]['debt_title']}",
        ]
    )
    return {
        "task_manager_foundation_handoff_freeze_authorization_plan": freeze_auth_plan,
        "task_manager_foundation_handoff_freeze_authorization_plan_md": markdown,
        "task_manager_freeze_authorization_scope_matrix": scope_matrix,
        "task_manager_freeze_authorization_candidate_asset_map": candidate_asset_map,
        "task_manager_freeze_authorization_evidence_chain": evidence_chain_doc,
        "task_manager_freeze_authorization_boundary_contract": boundary_contract_doc,
        "task_manager_freeze_authorization_readiness_matrix": readiness_matrix,
        "task_manager_freeze_authorization_governance_debt_carryover": debt_carryover,
        "task_manager_freeze_authorization_non_execution_constraints": non_execution,
        "task_manager_freeze_authorization_next_phase_readiness": next_phase_doc,
        "summary": summary,
    }
