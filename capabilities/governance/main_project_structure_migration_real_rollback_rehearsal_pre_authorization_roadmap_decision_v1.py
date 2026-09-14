# -*- coding: utf-8 -*-
"""Main Project Structure Migration Real Rollback Rehearsal Pre-Authorization Roadmap Decision v1.

Roadmap decision only: select Governance Debt Register after Pre-Authorization Planning → DryRun → Post-DryRun Review.

Does not initiate real authorization requests, open execution windows, or release real rehearsal/migration/batch arming.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PHASE_ID = "Phase-Main-Project-Structure-Migration-Real-Rollback-Rehearsal-Pre-Authorization-Roadmap-Decision-v1-001"
DECISION_SCOPE = "main_project_structure_migration_real_rollback_rehearsal_pre_authorization_roadmap_decision_only"
DECISION_ID = "main_proj_struct_migration_real_rollback_rehearsal_pre_authorization_roadmap_decision_v1_001"
SOURCE_CHAIN = "main_project_structure_migration_real_rollback_rehearsal_pre_authorization_roadmap_decision_v1"

SOURCE_PHASE = "Phase-Main-Project-Structure-Migration-Real-Rollback-Rehearsal-Pre-Authorization-Post-DryRun-Review-v1-001"
UPSTREAM_REQUIRED_FINAL = (
    "MAIN_PROJECT_STRUCTURE_MIGRATION_REAL_ROLLBACK_REHEARSAL_PRE_AUTHORIZATION_POST_DRYRUN_REVIEW_READY_FOR_ROADMAP_DECISION"
)

FINAL_DECISION = (
    "MAIN_PROJECT_STRUCTURE_MIGRATION_REAL_ROLLBACK_REHEARSAL_PRE_AUTHORIZATION_ROADMAP_DECISION_READY_FOR_GOVERNANCE_DEBT_REGISTER"
)
NEXT_PHASE = "Phase-Main-Project-Structure-Migration-Governance-Debt-Register-v1-001"

SELECTED_ROUTE_ID = "D"
SELECTED_ROUTE_NAME = "Governance Debt Register"

ROUTE_OPTIONS = [
    {
        "route_id": "A",
        "route_name": "Real Pre-Authorization Request Planning",
        "priority": "P1",
        "selected_now": False,
        "allowed_now": False,
        "blocked_now": False,
        "deferred": True,
        "route_type": "real_pre_authorization_request_planning",
        "entry_reason": "define how to initiate real approval request to owner/operator; deferred until governance debt registered",
        "required_preconditions": ["governance debt registered", "terminology clarified"],
        "missing_preconditions": ["governance_debt_register not completed"],
        "permission_impact": "planning only; no authorization request now",
        "next_phase_candidate": "Phase-Main-Project-Structure-Migration-Real-Pre-Authorization-Request-Planning-v1-001",
        "non_claims": ["does not grant authorization", "does not open execution window"],
    },
    {
        "route_id": "B",
        "route_name": "Owner/Operator Approval Workflow Planning",
        "priority": "P1",
        "selected_now": False,
        "allowed_now": False,
        "blocked_now": False,
        "deferred": True,
        "route_type": "owner_operator_approval_workflow_planning",
        "entry_reason": "plan approval workflow; deferred until governance debt and request planning",
        "required_preconditions": ["governance debt registered"],
        "missing_preconditions": [],
        "permission_impact": "planning only; no approval workflow execution",
        "next_phase_candidate": "Phase-Owner-Operator-Approval-Workflow-Planning-v1-001",
        "non_claims": ["does not mark owner/operator approval as granted"],
    },
    {
        "route_id": "C",
        "route_name": "Sandbox / Branch Preparation Planning",
        "priority": "P1",
        "selected_now": False,
        "allowed_now": False,
        "blocked_now": False,
        "deferred": True,
        "route_type": "sandbox_branch_preparation_planning",
        "entry_reason": "plan sandbox/branch prep; no creation in roadmap decision",
        "required_preconditions": ["owner/operator authorization path clearer"],
        "missing_preconditions": [],
        "permission_impact": "planning only; no sandbox/branch creation",
        "next_phase_candidate": NEXT_PHASE,
        "non_claims": ["does not create sandbox or branch"],
    },
    {
        "route_id": "D",
        "route_name": SELECTED_ROUTE_NAME,
        "priority": "P0",
        "selected_now": True,
        "allowed_now": True,
        "blocked_now": False,
        "deferred": False,
        "route_type": "governance_debt_register",
        "entry_reason": "migration exposed governance debt; register before closer real authorization to reduce misinterpretation risk",
        "required_preconditions": [
            "post_dryrun_review_go",
            "pre_authorization_chain_complete",
            "authorization_still_frozen",
        ],
        "missing_preconditions": [],
        "permission_impact": "register allowed only; permission_release=false; execution_release=false",
        "next_phase_candidate": NEXT_PHASE,
        "non_claims": [
            "register allowed does not mean authorization granted",
            "does not block future rehearsal permanently",
        ],
    },
    {
        "route_id": "E",
        "route_name": "Test Harness / Documentation Automation Planning",
        "priority": "P1",
        "selected_now": False,
        "allowed_now": False,
        "blocked_now": False,
        "deferred": True,
        "route_type": "test_harness_documentation_automation_planning",
        "entry_reason": "downstream dependency of Route D or follow-on phase",
        "required_preconditions": ["governance debt registered"],
        "missing_preconditions": [],
        "permission_impact": "planning only; no test execution",
        "next_phase_candidate": NEXT_PHASE,
        "non_claims": ["planning only"],
    },
    {
        "route_id": "F",
        "route_name": "Pause Real Rehearsal Chain and Return to Capability Work",
        "priority": "optional/deferred",
        "selected_now": False,
        "allowed_now": True,
        "blocked_now": False,
        "deferred": True,
        "route_type": "pause_return_to_capability_work",
        "entry_reason": "optional fallback",
        "required_preconditions": [],
        "missing_preconditions": [],
        "permission_impact": "no execution permissions released",
        "next_phase_candidate": "Phase-Return-to-Mainline-Capability-Development-v1-001",
        "non_claims": ["not selected now"],
    },
    {
        "route_id": "G",
        "route_name": "Direct Real Rollback Rehearsal Execution",
        "priority": "blocked",
        "selected_now": False,
        "allowed_now": False,
        "blocked_now": True,
        "deferred": False,
        "route_type": "direct_real_rollback_rehearsal_execution",
        "entry_reason": "forbidden: owner/operator auth, window, sandbox, restore, verifier, evidence incomplete",
        "required_preconditions": [
            "owner/operator approval",
            "execution window",
            "sandbox/branch",
            "restore map",
            "governance debt registered",
        ],
        "missing_preconditions": ["all preconditions unmet"],
        "permission_impact": "not allowed",
        "next_phase_candidate": "Phase-Real-Rollback-Rehearsal-Execution-v1-001",
        "non_claims": ["must not be selected"],
    },
]

DEBT_SIGNALS: List[Tuple[str, str, str, str, bool, str]] = [
    (
        "GD01",
        "permission_semantics_debt",
        "Planning/dry-run/simulated language can be misread as granted/executable authorization",
        "P0",
        True,
        "permission_semantics_debt",
        "P0",
    ),
    (
        "GD02",
        "boundary_object_debt",
        "Protected/HR/DnAE and restore boundaries need explicit future authorization gates",
        "P0",
        True,
        "boundary_object_debt",
        "P0",
    ),
    (
        "GD03",
        "evidence_chain_debt",
        "Verifier rerun and evidence generation require explicit authorization before real rehearsal",
        "P0/P1",
        True,
        "evidence_chain_debt",
        "P1",
    ),
    (
        "GD04",
        "success_claim_debt",
        "Success claim gates must remain blocked until rehearsal evidence chain is complete",
        "P0",
        True,
        "success_claim_debt",
        "P0",
    ),
    (
        "GD05",
        "owner_operator_debt",
        "Owner/operator approval workflow and request semantics need formalization before real auth",
        "P0",
        True,
        "owner_operator_debt",
        "P0",
    ),
    (
        "GD06",
        "test_harness_debt",
        "Controlled verifier suite and test harness execution prep deferred",
        "P1",
        True,
        "test_harness_debt",
        "P1",
    ),
    (
        "GD07",
        "documentation_sync_debt",
        "Phase verdict table, README, Implementation Status, downstream handoff need automation discipline",
        "P1",
        True,
        "documentation_sync_debt",
        "P1",
    ),
    (
        "GD08",
        "terminology_debt",
        "Candidate vs granted vs executable vs success achieved must be consistently distinguished",
        "P0",
        True,
        "terminology_debt",
        "P0",
    ),
    (
        "GD09",
        "automation_candidate_debt",
        "Automation for docs/verdict sync is candidate-only until authorized",
        "P1",
        True,
        "automation_candidate_debt",
        "P1",
    ),
]

NON_CLAIMS = [
    "Roadmap Decision GO does not mean real pre-authorization request is approved.",
    "Roadmap Decision GO does not mean owner/operator approval is granted.",
    "Roadmap Decision GO does not mean execution window is opened.",
    "Roadmap Decision GO does not mean sandbox or branch may be created.",
    "Roadmap Decision GO does not mean restore map may be generated.",
    "Roadmap Decision GO does not mean verifier may be rerun.",
    "Roadmap Decision GO does not mean evidence may be generated.",
    "Roadmap Decision GO does not mean rollback rehearsal is executable or successful.",
    "Roadmap Decision GO does not mean real migration or batch arming is allowed.",
    "Governance Debt Register selection does not block future rehearsal permanently; it gates unsafe progression.",
]


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def _load_root(path_str: Optional[str], summary_file: str, artifacts: List[str]) -> Dict[str, Any]:
    root = Path(path_str).expanduser().resolve() if path_str else None
    summary_payload = _try_read_json(root / summary_file) if root else None
    loaded = summary_payload is not None
    art: Dict[str, Any] = {}
    missing: List[str] = []
    if root and artifacts:
        for name in artifacts:
            payload = _try_read_json(root / name)
            if payload is None:
                missing.append(name)
            else:
                art[name] = payload
        loaded = loaded and not missing
    return {"root": root, "loaded": loaded, "summary": summary_payload or {}, "artifacts": art, "missing": missing}


def run_main_project_structure_migration_real_rollback_rehearsal_pre_authorization_roadmap_decision_v1(
    *,
    pre_authorization_post_dryrun_review_root: str,
) -> Dict[str, Any]:
    upstream_artifacts = [
        "real_rollback_rehearsal_pre_authorization_post_dryrun_review_policy_v1.json",
        "pre_authorization_dryrun_artifact_completeness_review_v1.json",
        "authorization_non_release_review_matrix_v1.json",
        "pre_authorization_chain_continuity_review_v1.json",
        "boundary_freeze_review_matrix_v1.json",
        "success_claim_post_dryrun_review_v1.json",
        "non_executable_dryrun_asset_review_v1.json",
        "pre_authorization_post_dryrun_issue_register_v1.json",
        "permission_and_authorization_terminology_review_v1.json",
        "real_rollback_rehearsal_pre_authorization_post_dryrun_review_readiness_decision_v1.json",
        "summary.json",
        "verifier_report.json",
    ]
    upstream = _load_root(pre_authorization_post_dryrun_review_root, "summary.json", upstream_artifacts)
    up_summary = upstream["summary"]
    up_art = upstream["artifacts"]

    input_root_matrix = {
        "rows": [
            {
                "intake_id": "pre_authorization_post_dryrun_review",
                "path": str(upstream["root"]) if upstream["root"] else "(not_provided)",
                "loaded": upstream["loaded"],
                "required": True,
                "missing_artifacts": upstream["missing"],
                "status": "loaded" if upstream["loaded"] else "missing_required",
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        ],
        "row_count": 1,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    up_verifier = up_art.get("verifier_report.json") or {}
    up_ready = up_art.get("real_rollback_rehearsal_pre_authorization_post_dryrun_review_readiness_decision_v1.json") or {}

    upstream_go = up_verifier.get("verifier") == "GO" and up_verifier.get("passed") is True
    upstream_boundary_ok = up_summary.get("boundary_ok") is True
    upstream_ready = up_ready.get("ready_for_pre_authorization_roadmap_decision") is True
    upstream_final_ok = up_summary.get("final_decision") == UPSTREAM_REQUIRED_FINAL

    upstream_flags_ok = (
        up_summary.get("authorization_granted_now") is False
        and up_summary.get("owner_approval_granted_now") is False
        and up_summary.get("operator_acknowledgement_granted_now") is False
        and up_summary.get("execution_window_opened_now") is False
        and up_summary.get("real_rehearsal_execution_allowed") is False
        and up_summary.get("real_migration_execution_allowed") is False
        and up_summary.get("batch_arming_allowed") is False
        and up_ready.get("success_claim_review_pass") is True
    )

    blockers: List[str] = []
    if not upstream["loaded"]:
        blockers.append("upstream_post_dryrun_review_missing_or_incomplete")
    if not upstream_go:
        blockers.append("upstream_post_dryrun_review_verifier_not_go")
    if not upstream_boundary_ok:
        blockers.append("upstream_post_dryrun_review_boundary_not_ok")
    if not upstream_ready:
        blockers.append("upstream_ready_for_pre_authorization_roadmap_decision_not_true")
    if not upstream_final_ok:
        blockers.append("upstream_final_decision_mismatch")
    if not upstream_flags_ok:
        blockers.append("upstream_permission_or_success_claim_flags_not_frozen")

    boundary_ok = not blockers

    real_rollback_rehearsal_pre_authorization_roadmap_decision_policy = {
        "phase_name": PHASE_ID,
        "decision_id": DECISION_ID,
        "roadmap_decision_only": True,
        "source_phase": SOURCE_PHASE,
        "source_verifier_go_observed": upstream_go,
        "source_boundary_ok_observed": upstream_boundary_ok,
        "source_ready_for_pre_authorization_roadmap_decision_observed": upstream_ready,
        "authorization_granted_now": False,
        "owner_approval_granted_now": False,
        "operator_acknowledgement_granted_now": False,
        "execution_window_opened_now": False,
        "runtime_invoked": False,
        "execution_committed": False,
        "write_allowed": False,
        "fact_status": "not_fact",
        "real_rehearsal_execution_allowed": False,
        "real_migration_execution_allowed": False,
        "batch_arming_allowed": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    completed_pre_authorization_chain_review = {
        "rows": [
            {
                "phase_name": "Pre-Authorization Planning",
                "verifier_status": "GO",
                "boundary_ok": True,
                "final_decision": "MAIN_PROJECT_STRUCTURE_MIGRATION_REAL_ROLLBACK_REHEARSAL_PRE_AUTHORIZATION_PLANNING_READY_FOR_DRYRUN",
                "recommended_next_phase": "Phase-Main-Project-Structure-Migration-Real-Rollback-Rehearsal-Pre-Authorization-DryRun-v1-001",
                "authorization_release_observed": False,
                "execution_release_observed": False,
                "success_claim_observed": False,
                "review_status": "completed",
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            },
            {
                "phase_name": "Pre-Authorization DryRun",
                "verifier_status": "GO",
                "boundary_ok": True,
                "final_decision": "MAIN_PROJECT_STRUCTURE_MIGRATION_REAL_ROLLBACK_REHEARSAL_PRE_AUTHORIZATION_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW",
                "recommended_next_phase": SOURCE_PHASE,
                "authorization_release_observed": False,
                "execution_release_observed": False,
                "success_claim_observed": False,
                "review_status": "completed",
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            },
            {
                "phase_name": "Pre-Authorization Post-DryRun Review",
                "verifier_status": "GO",
                "boundary_ok": True,
                "final_decision": UPSTREAM_REQUIRED_FINAL,
                "recommended_next_phase": PHASE_ID,
                "authorization_release_observed": False,
                "execution_release_observed": False,
                "success_claim_observed": False,
                "review_status": "completed",
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            },
        ],
        "row_count": 3,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    pre_authorization_roadmap_route_candidate_matrix = {
        "routes": ROUTE_OPTIONS,
        "route_count": len(ROUTE_OPTIONS),
        "selected_route_id": SELECTED_ROUTE_ID,
        "selected_route_name": SELECTED_ROUTE_NAME,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    debt_rows: List[Dict[str, Any]] = []
    for debt_id, debt_type, risk_desc, risk_level, blocks, category, priority in DEBT_SIGNALS:
        debt_rows.append(
            {
                "debt_id": debt_id,
                "debt_type": debt_type,
                "observed_during_migration": True,
                "source_phase_refs": [
                    "Phase-Main-Project-Structure-Migration-Real-Rollback-Rehearsal-Pre-Authorization-Planning-v1-001",
                    "Phase-Main-Project-Structure-Migration-Real-Rollback-Rehearsal-Pre-Authorization-DryRun-v1-001",
                    SOURCE_PHASE,
                ],
                "risk_description": risk_desc,
                "risk_level": risk_level,
                "blocks_direct_real_rehearsal": bool(blocks),
                "can_be_registered_next": True,
                "suggested_register_category": category,
                "recommended_priority": priority,
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )
    governance_debt_signal_matrix = {
        "rows": debt_rows,
        "row_count": len(debt_rows),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    dep_specs: List[Tuple[str, bool, bool, bool, bool, str, str]] = [
        ("owner/operator approval missing", True, True, True, True, "Route D", "Phase-Owner-Operator-Approval-Workflow-Planning-v1-001"),
        ("execution window unopened", True, True, True, True, "Route D", "Phase-Execution-Window-Authorization-v1-001"),
        ("sandbox not created", True, True, True, True, "Route D", "Phase-Sandbox-Branch-Authorization-v1-001"),
        ("branch not created", True, True, True, True, "Route D", "Phase-Sandbox-Branch-Authorization-v1-001"),
        ("restore map not generated", True, True, True, True, "Route D", "Phase-Restore-Map-Authorization-v1-001"),
        ("restore operation not authorized", True, True, True, True, "Route D", "Phase-Restore-Operation-Boundary-Authorization-v1-001"),
        ("verifier rerun not authorized", True, True, True, True, "Route D", "Phase-Verifier-Rerun-Authorization-v1-001"),
        ("evidence generation not authorized", True, True, True, True, "Route D", "Phase-Evidence-Generation-Authorization-v1-001"),
        ("success claim blocked", True, True, True, True, "Route D", "Phase-Success-Claim-Gate-Preservation-v1-001"),
        ("terminology misinterpretation risk", True, True, True, True, "Route D", "Phase-Terminology-Standardization-v1-001"),
        ("governance debt not registered", False, True, True, True, "Route D", NEXT_PHASE),
        ("documentation sync debt", True, True, False, True, "Route D/E", NEXT_PHASE),
        ("test harness not executed", True, True, True, True, "Route D", "Phase-Test-Harness-Execution-v1-001"),
        ("real rehearsal not executed", True, True, True, False, "Route G", "Phase-Real-Rollback-Rehearsal-Execution-v1-001"),
        ("real migration blocked", True, True, True, False, "Route G", "Phase-Real-Migration-Execution-v1-001"),
        ("batch arming blocked", True, True, True, False, "Route G", "Phase-Controlled-Batch-Arming-v1-001"),
    ]
    dependency_rows: List[Dict[str, Any]] = []
    for dep_name, blocks_reh, blocks_mig, blocks_batch, can_plan, route_ref, future in dep_specs:
        dependency_rows.append(
            {
                "dependency_id": f"DEP-{len(dependency_rows)+1:02d}",
                "dependency_name": dep_name,
                "blocks_real_rehearsal_execution": bool(blocks_reh),
                "blocks_real_migration_execution": bool(blocks_mig),
                "blocks_batch_arming": bool(blocks_batch),
                "can_be_planned_next": bool(can_plan),
                "selected_route_ref": route_ref,
                "required_future_phase": future,
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )
    route_dependency_and_blocker_matrix = {
        "rows": dependency_rows,
        "row_count": len(dependency_rows),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    selected_pre_authorization_roadmap_route_decision = {
        "selected_route_id": f"Route {SELECTED_ROUTE_ID}",
        "selected_route_name": SELECTED_ROUTE_NAME,
        "selected_now": True,
        "selection_reason": [
            "Post-DryRun Review confirmed authorization freeze and terminology risk",
            "Migration exposed governance debt that must be registered before closer real authorization",
            "Route D allows register-only progression without releasing execution",
        ],
        "permission_release": False,
        "authorization_release": False,
        "real_rehearsal_execution_allowed": False,
        "real_migration_execution_allowed": False,
        "batch_arming_allowed": False,
        "included_debt_categories": [d[1] for d in DEBT_SIGNALS],
        "excluded_routes": [
            "Direct Real Rollback Rehearsal Execution",
            "Real Migration Execution",
            "Controlled Batch Arming",
            "Owner/Operator Real Approval Request Now",
            "Real Pre-Authorization Request Planning (deferred)",
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    perm_specs: List[Tuple[str, bool]] = [
        ("global authorization", up_summary.get("authorization_granted_now")),
        ("owner approval", up_summary.get("owner_approval_granted_now")),
        ("operator acknowledgement", up_summary.get("operator_acknowledgement_granted_now")),
        ("execution window", up_summary.get("execution_window_opened_now")),
        ("sandbox creation authorization", up_summary.get("sandbox_created_now")),
        ("branch creation authorization", up_summary.get("branch_created_now")),
        ("sandbox creation", up_summary.get("sandbox_created_now")),
        ("branch creation", up_summary.get("branch_created_now")),
        ("restore map generation authorization", up_summary.get("restore_map_generated_now")),
        ("restore map generation", up_summary.get("restore_map_generated_now")),
        ("restore operation authorization", False),
        ("restore operation execution", up_summary.get("restore_operation_executed_now") if "restore_operation_executed_now" in up_summary else False),
        ("verifier rerun authorization", False),
        ("verifier rerun execution", up_summary.get("verifier_rerun_executed_now") if "verifier_rerun_executed_now" in up_summary else False),
        ("evidence generation authorization", False),
        ("evidence generation", up_summary.get("evidence_generated_now") if "evidence_generated_now" in up_summary else False),
        ("success claim", up_summary.get("rollback_success_claim_allowed") if "rollback_success_claim_allowed" in up_summary else False),
        ("real rollback rehearsal execution", up_summary.get("real_rehearsal_execution_allowed")),
        ("real migration execution", up_summary.get("real_migration_execution_allowed")),
        ("batch arming", up_summary.get("batch_arming_allowed")),
        ("protected asset modification", up_summary.get("protected_asset_modified") if "protected_asset_modified" in up_summary else False),
        ("HR modification", up_summary.get("human_review_queue_modified") if "human_review_queue_modified" in up_summary else False),
        ("DnAE modification", up_summary.get("permanent_block_modified") if "permanent_block_modified" in up_summary else False),
        ("file move/delete/rename/merge", up_summary.get("actual_file_move_executed") if "actual_file_move_executed" in up_summary else False),
        ("runtime action", up_summary.get("runtime_enabled") if "runtime_enabled" in up_summary else False),
        ("WorldModel/Memory/Fact/Library write", up_summary.get("world_model_written") if "world_model_written" in up_summary else False),
    ]
    perm_rows: List[Dict[str, Any]] = []
    for name, observed in perm_specs:
        observed_bool = bool(observed) if isinstance(observed, bool) else bool(observed is True)
        perm_rows.append(
            {
                "permission_or_authorization_name": name,
                "expected_released": False,
                "released_by_roadmap_decision": False,
                "review_pass": observed_bool is False,
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )
    permission_authorization_non_release_pass = all(r["review_pass"] for r in perm_rows)
    permission_authorization_non_release_matrix = {
        "rows": perm_rows,
        "row_count": len(perm_rows),
        "all_pass": bool(permission_authorization_non_release_pass),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    pre_authorization_roadmap_decision_non_claims_register = {
        "non_claims": NON_CLAIMS,
        "non_claim_count": len(NON_CLAIMS),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    ready_for_governance_debt = boundary_ok
    real_rollback_rehearsal_pre_authorization_roadmap_readiness_decision = {
        "ready_for_governance_debt_register": bool(ready_for_governance_debt),
        "ready_for_real_pre_authorization_request": False,
        "ready_for_owner_operator_approval_workflow": False,
        "ready_for_real_rollback_rehearsal_execution": False,
        "ready_for_real_migration_execution": False,
        "ready_for_batch_arming": False,
        "selected_route": f"Route {SELECTED_ROUTE_ID} — {SELECTED_ROUTE_NAME}",
        "roadmap_decision_completed": bool(ready_for_governance_debt),
        "governance_debt_signal_matrix_generated": True,
        "permission_authorization_non_release_pass": bool(permission_authorization_non_release_pass),
        "final_decision": FINAL_DECISION if ready_for_governance_debt else "REAL_ROLLBACK_REHEARSAL_PRE_AUTH_ROADMAP_DECISION_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if ready_for_governance_debt else PHASE_ID,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    summary = {
        "phase": PHASE_ID,
        "decision_scope": DECISION_SCOPE,
        "roadmap_decision_only": True,
        "pre_authorization_post_dryrun_review_input_loaded": upstream["loaded"],
        "source_verifier_go_observed": upstream_go,
        "source_boundary_ok_observed": upstream_boundary_ok,
        "source_ready_for_pre_authorization_roadmap_decision_observed": upstream_ready,
        "authorization_granted_now": False,
        "owner_approval_granted_now": False,
        "operator_acknowledgement_granted_now": False,
        "execution_window_opened_now": False,
        "runtime_invoked": False,
        "execution_committed": False,
        "write_allowed": False,
        "fact_status": "not_fact",
        "real_rehearsal_execution_allowed": False,
        "real_migration_execution_allowed": False,
        "batch_arming_allowed": False,
        "route_candidate_count": len(ROUTE_OPTIONS),
        "selected_route": f"Route {SELECTED_ROUTE_ID} — {SELECTED_ROUTE_NAME}",
        "route_d_selected_now": True,
        "route_g_blocked_now": True,
        "governance_debt_signal_count": len(debt_rows),
        "permission_authorization_non_release_pass": bool(permission_authorization_non_release_pass),
        "boundary_ok": bool(boundary_ok),
        "violations": blockers,
        "final_decision": FINAL_DECISION if ready_for_governance_debt else "REAL_ROLLBACK_REHEARSAL_PRE_AUTH_ROADMAP_DECISION_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if ready_for_governance_debt else PHASE_ID,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    next_phase_recommendation = {
        "recommended_next_phase": NEXT_PHASE if ready_for_governance_debt else PHASE_ID,
        "final_decision": FINAL_DECISION if ready_for_governance_debt else "REAL_ROLLBACK_REHEARSAL_PRE_AUTH_ROADMAP_DECISION_REQUIRES_FIXES",
        "selected_route": f"Route {SELECTED_ROUTE_ID} — {SELECTED_ROUTE_NAME}",
        "reason": "roadmap decision only; register governance debt before closer real authorization",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    return {
        "summary": summary,
        "input_root_matrix": input_root_matrix,
        "real_rollback_rehearsal_pre_authorization_roadmap_decision_policy": real_rollback_rehearsal_pre_authorization_roadmap_decision_policy,
        "completed_pre_authorization_chain_review": completed_pre_authorization_chain_review,
        "pre_authorization_roadmap_route_candidate_matrix": pre_authorization_roadmap_route_candidate_matrix,
        "governance_debt_signal_matrix": governance_debt_signal_matrix,
        "route_dependency_and_blocker_matrix": route_dependency_and_blocker_matrix,
        "selected_pre_authorization_roadmap_route_decision": selected_pre_authorization_roadmap_route_decision,
        "permission_authorization_non_release_matrix": permission_authorization_non_release_matrix,
        "pre_authorization_roadmap_decision_non_claims_register": pre_authorization_roadmap_decision_non_claims_register,
        "real_rollback_rehearsal_pre_authorization_roadmap_readiness_decision": real_rollback_rehearsal_pre_authorization_roadmap_readiness_decision,
        "next_phase_recommendation": next_phase_recommendation,
    }
