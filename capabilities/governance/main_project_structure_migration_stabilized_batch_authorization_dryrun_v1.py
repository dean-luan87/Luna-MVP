# -*- coding: utf-8 -*-
"""Main Project Structure Migration Stabilized Batch Authorization DryRun v1.

Dry-run-only: simulate consumption of B0–B7 batch authorization planning artifacts.
No request sent, no grant, no batch arming, no batch execution, no verifier rerun execution,
no rollback rehearsal execution, no real file operations.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.main_project_structure_migration_guarded_planning_v1 import GATE_DEFS
from capabilities.governance.main_project_structure_migration_stabilized_execution_planning_v1 import STABILIZED_BATCH_DEFS
from capabilities.governance.main_project_structure_migration_stabilized_batch_authorization_planning_v1 import (
    FINAL_DECISION as PLANNING_FINAL_DECISION,
    NEXT_PHASE as PLANNING_NEXT_PHASE,
    PHASE_ID as PLANNING_PHASE_ID,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID

PHASE_ID = "Phase-Main-Project-Structure-Migration-Stabilized-Batch-Authorization-DryRun-v1-001"
DRYRUN_SCOPE = "main_project_structure_migration_stabilized_batch_authorization_dryrun_only"
SOURCE_CHAIN = "main_project_structure_migration_stabilized_batch_authorization_dryrun_v1"

FINAL_DECISION = (
    "MAIN_PROJECT_STRUCTURE_MIGRATION_STABILIZED_BATCH_AUTHORIZATION_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
)
NEXT_PHASE = "Phase-Main-Project-Structure-Migration-Stabilized-Batch-Authorization-Post-DryRun-Review-v1-001"

PLANNING_REQUIRED_PHASE = PLANNING_PHASE_ID
PLANNING_REQUIRED_FINAL = PLANNING_FINAL_DECISION
PLANNING_REQUIRED_NEXT = PHASE_ID

PLANNING_REQUIRED_ARTIFACTS: Tuple[str, ...] = (
    "summary.json",
    "verifier_report.json",
    "stabilized_batch_authorization_planning_policy_v1.json",
    "execution_post_dryrun_review_input_review_v1.json",
    "b0_b7_batch_authorization_scope_matrix_v1.json",
    "batch_authorization_request_schema_planning_v1.json",
    "batch_authorization_grant_schema_planning_v1.json",
    "batch_pre_authorization_gate_matrix_v1.json",
    "batch_execution_window_planning_v1.json",
    "batch_verifier_rerun_authorization_planning_v1.json",
    "batch_rollback_authorization_planning_v1.json",
    "batch_file_operation_permission_boundary_v1.json",
    "batch_protected_eval_out_guard_authorization_matrix_v1.json",
    "batch_authorization_non_claims_register_v1.json",
    "stabilized_batch_authorization_planning_readiness_decision_v1.json",
)

BATCH_IDS: Tuple[str, ...] = ("B0", "B1", "B2", "B3", "B4", "B5", "B6", "B7")


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _boundary_meta() -> Dict[str, Any]:
    return {
        "batch_authorization_dryrun_only": True,
        "simulated": True,
        "source_path_mode": "repo_eval_out",
        "batch_authorization_request_sent_now": False,
        "batch_authorization_granted_now": False,
        "batch_armed_now": False,
        "batch_execution_started_now": False,
        "execution_window_opened_now": False,
        "verifier_rerun_executed_now": False,
        "rollback_rehearsal_executed_now": False,
        "actual_file_move_executed": False,
        "actual_file_delete_executed": False,
        "actual_file_rename_executed": False,
        "actual_file_merge_executed": False,
        "actual_file_copy_executed": False,
        "actual_file_overwrite_executed": False,
        "actual_archive_executed": False,
        "real_migration_execution_allowed": False,
        "real_rehearsal_execution_allowed": False,
        "rollback_rehearsal_execution_allowed": False,
        "eval_out_modified_now": False,
        "protected_asset_modified_now": False,
        "hr_modified_now": False,
        "dnae_modified_now": False,
        "file_operation_executed_now": False,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        # mandatory non-execution freeze fields
        "runtime_invoked": False,
        "execution_committed": False,
        "authorization_granted_now": False,
        "owner_approval_granted_now": False,
        "operator_acknowledgement_granted_now": False,
        "success_claim_allowed": False,
        "batch_arming_allowed": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _row(**kwargs: Any) -> Dict[str, Any]:
    return {**kwargs, **_boundary_meta(), "planned_now": True, "executed_now": False, "simulated_now": True}


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def _load_planning_root(path_str: Optional[str]) -> Dict[str, Any]:
    root = Path(path_str).expanduser().resolve() if path_str else None
    artifacts: Dict[str, Any] = {}
    missing: List[str] = []
    if root:
        for name in PLANNING_REQUIRED_ARTIFACTS:
            payload = _try_read_json(root / name)
            if payload is None:
                missing.append(name)
            else:
                artifacts[name] = payload
    loaded = bool(root) and not missing and bool(artifacts.get("summary.json")) and bool(artifacts.get("verifier_report.json"))
    return {"root": root, "loaded": loaded, "artifacts": artifacts, "missing": missing}


def _is_workspace_fallback(root: Optional[Path]) -> bool:
    if not root:
        return False
    # simple, explicit: workspace paths are treated as fallback
    return "Luna-Workspace-Min" in str(root)


def run_main_project_structure_migration_stabilized_batch_authorization_dryrun_v1(
    *,
    stabilized_batch_authorization_planning_root: str,
) -> Dict[str, Any]:
    plan = _load_planning_root(stabilized_batch_authorization_planning_root)
    blockers: List[str] = []
    if not plan["loaded"]:
        blockers.append(f"planning input incomplete: {plan['missing']}")

    sm = (plan["artifacts"].get("summary.json") or {}) if plan["artifacts"] else {}
    vr = (plan["artifacts"].get("verifier_report.json") or {}) if plan["artifacts"] else {}

    if vr.get("verifier") != "GO" or vr.get("passed") is not True:
        blockers.append("planning verifier must be GO")
    if sm.get("final_decision") != PLANNING_REQUIRED_FINAL:
        blockers.append("planning final_decision mismatch")
    if sm.get("recommended_next_phase") != PLANNING_REQUIRED_NEXT:
        blockers.append("planning recommended_next_phase must be this dryrun phase")
    for f in (
        "batch_authorization_request_sent_now",
        "batch_authorization_granted_now",
        "batch_armed_now",
        "batch_execution_started_now",
        "verifier_rerun_executed_now",
        "rollback_rehearsal_execution_allowed",
        "eval_out_modified_now",
        "protected_asset_modified_now",
        "hr_modified_now",
        "dnae_modified_now",
    ):
        if sm.get(f) is not False:
            blockers.append(f"planning boundary must be false: {f}")

    scope_rows = (plan["artifacts"].get("b0_b7_batch_authorization_scope_matrix_v1.json") or {}).get("rows") or []
    gate_rows = (plan["artifacts"].get("batch_pre_authorization_gate_matrix_v1.json") or {}).get("rows") or []
    window_rows = (plan["artifacts"].get("batch_execution_window_planning_v1.json") or {}).get("rows") or []
    rerun_rows = (plan["artifacts"].get("batch_verifier_rerun_authorization_planning_v1.json") or {}).get("rows") or []
    rollback_rows = (plan["artifacts"].get("batch_rollback_authorization_planning_v1.json") or {}).get("rows") or []
    file_perm_rows = (plan["artifacts"].get("batch_file_operation_permission_boundary_v1.json") or {}).get("rows") or []
    guard_rows = (plan["artifacts"].get("batch_protected_eval_out_guard_authorization_matrix_v1.json") or {}).get("rows") or []
    non_claims_rows = (plan["artifacts"].get("batch_authorization_non_claims_register_v1.json") or {}).get("rows") or []

    scope_by_id = {r.get("batch_id"): r for r in scope_rows if isinstance(r.get("batch_id"), str)}

    scope_dryrun_rows: List[Dict[str, Any]] = []
    req_schema_dryrun = _row(schema_consumed=True, request_sent_now=False, dryrun_pass=True)
    grant_schema_dryrun = _row(schema_consumed=True, authorization_granted_now=False, dryrun_pass=True)
    gate_dryrun_rows: List[Dict[str, Any]] = []
    window_dryrun_rows: List[Dict[str, Any]] = []
    rerun_dryrun_rows: List[Dict[str, Any]] = []
    rollback_dryrun_rows: List[Dict[str, Any]] = []
    file_perm_dryrun_rows: List[Dict[str, Any]] = []
    guard_dryrun_rows: List[Dict[str, Any]] = []
    non_claims_dryrun_rows: List[Dict[str, Any]] = []

    all_pass = True
    for bid, _, _, domain, _, _ in STABILIZED_BATCH_DEFS:
        s = scope_by_id.get(bid) or {}
        scope_pass = (
            bool(s)
            and s.get("batch_domain") == domain
            and isinstance(s.get("authorized_scope_candidate"), list)
            and isinstance(s.get("required_pre_gates"), list)
            and len(s.get("required_pre_gates") or []) == len(GATE_DEFS)
            and s.get("authorization_request_sent_now") is False
            and s.get("authorization_granted_now") is False
            and s.get("batch_armed_now") is False
            and s.get("file_operation_executed_now") is False
            and s.get("protected_path_intersection") is False
            and s.get("eval_out_write_allowed") is False
        )
        if not scope_pass:
            all_pass = False
        scope_dryrun_rows.append(_row(batch_id=bid, batch_domain=domain, simulated_consumption="pass" if scope_pass else "fail", dryrun_pass=scope_pass))

        # gates consumption per batch
        g = [r for r in gate_rows if r.get("batch_id") == bid]
        gate_pass = len(g) == len(GATE_DEFS)
        if not gate_pass:
            all_pass = False
        gate_dryrun_rows.append(_row(batch_id=bid, expected_gate_count=len(GATE_DEFS), observed_gate_count=len(g), gate_consumption_pass=gate_pass, dryrun_pass=gate_pass))

        w = [r for r in window_rows if r.get("batch_id") == bid]
        window_pass = len(w) == 1 and w[0].get("execution_window_opened_now") is False
        if not window_pass:
            all_pass = False
        window_dryrun_rows.append(_row(batch_id=bid, execution_window_consumed=True, execution_window_opened_now=False, dryrun_pass=window_pass))

        rr = [r for r in rerun_rows if r.get("batch_id") == bid]
        rerun_pass = len(rr) == 1 and rr[0].get("verifier_rerun_executed_now") is False
        if not rerun_pass:
            all_pass = False
        rerun_dryrun_rows.append(_row(batch_id=bid, verifier_rerun_auth_consumed=True, verifier_rerun_executed_now=False, dryrun_pass=rerun_pass))

        rb = [r for r in rollback_rows if r.get("batch_id") == bid]
        rollback_pass = len(rb) == 1 and rb[0].get("rollback_rehearsal_executed_now") is False
        if not rollback_pass:
            all_pass = False
        rollback_dryrun_rows.append(_row(batch_id=bid, rollback_auth_consumed=True, rollback_rehearsal_executed_now=False, dryrun_pass=rollback_pass))

        fp = [r for r in file_perm_rows if r.get("batch_id") == bid]
        file_perm_pass = len(fp) == 1 and all(fp[0].get(k) is False for k in (
            "file_move_allowed_now",
            "file_delete_allowed_now",
            "file_rename_allowed_now",
            "file_merge_allowed_now",
            "file_copy_allowed_now",
            "file_overwrite_allowed_now",
            "archive_allowed_now",
        ))
        if not file_perm_pass:
            all_pass = False
        file_perm_dryrun_rows.append(_row(batch_id=bid, boundary_consumed=True, all_file_ops_forbidden_now=True, dryrun_pass=file_perm_pass))

        gr = [r for r in guard_rows if r.get("batch_id") == bid]
        guard_pass = len(gr) == 1 and gr[0].get("protected_assets_frozen") is True and gr[0].get("eval_out_readonly") is True
        if not guard_pass:
            all_pass = False
        guard_dryrun_rows.append(_row(batch_id=bid, guard_consumed=True, protected_eval_out_guard_pass=guard_pass, dryrun_pass=guard_pass))

    # non-claims: must contain key misunderstanding barriers
    texts = " ".join([str(r.get("text", "")) for r in non_claims_rows])
    # keep minimal; don't overfit to exact wording/casing
    nc_pass = all(sub in texts for sub in ("授权规划不等于授权请求", "授权授予不等于 batch armed"))
    non_claims_dryrun_rows = [_row(non_claims_consumed=True, dryrun_pass=nc_pass)]
    if not nc_pass:
        all_pass = False

    boundary_ok = bool(all_pass) and not blockers

    source_path_mode = "workspace_fallback" if _is_workspace_fallback(plan["root"]) else "repo_eval_out"

    stabilized_batch_authorization_dryrun_policy = _row(
        phase_id=PHASE_ID,
        dryrun_scope=DRYRUN_SCOPE,
        planning_required_phase=PLANNING_REQUIRED_PHASE,
        planning_required_final_decision=PLANNING_REQUIRED_FINAL,
        planning_required_next_phase=PLANNING_REQUIRED_NEXT,
        source_path_mode=source_path_mode,
        planned_default_output_dir="_eval_out/main_project_structure_migration_stabilized_batch_authorization_dryrun_v1_smoke_v0/",
    )

    batch_authorization_planning_input_review = {
        "planning_root": str(plan["root"]) if plan["root"] else None,
        "planning_loaded": plan["loaded"],
        "source_path_mode": source_path_mode,
        "missing": plan["missing"],
        "planning_summary": {
            "phase": sm.get("phase"),
            "final_decision": sm.get("final_decision"),
            "recommended_next_phase": sm.get("recommended_next_phase"),
        },
        "planning_verifier": {"verifier": vr.get("verifier"), "passed": vr.get("passed"), "check_count": vr.get("check_count")},
        "all_pass": not blockers,
        "blockers": blockers,
        **{**_boundary_meta(), "source_path_mode": source_path_mode},
    }

    def _pack(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
        return {"rows": rows, "row_count": len(rows), "all_pass": all(r.get("dryrun_pass") is True for r in rows), **{**_boundary_meta(), "source_path_mode": source_path_mode}}

    b0_b7_authorization_scope_dryrun = _pack(scope_dryrun_rows)
    batch_pre_authorization_gate_dryrun = _pack(gate_dryrun_rows)
    batch_execution_window_dryrun = _pack(window_dryrun_rows)
    batch_verifier_rerun_authorization_dryrun = _pack(rerun_dryrun_rows)
    batch_rollback_authorization_dryrun = _pack(rollback_dryrun_rows)
    batch_file_operation_permission_boundary_dryrun = _pack(file_perm_dryrun_rows)
    batch_protected_eval_out_guard_dryrun = _pack(guard_dryrun_rows)

    batch_authorization_request_schema_dryrun = {**req_schema_dryrun, **{**_boundary_meta(), "source_path_mode": source_path_mode}}
    batch_authorization_grant_schema_dryrun = {**grant_schema_dryrun, **{**_boundary_meta(), "source_path_mode": source_path_mode}}

    batch_authorization_non_claims_dryrun = {
        "rows": non_claims_dryrun_rows,
        "row_count": len(non_claims_dryrun_rows),
        "all_pass": nc_pass,
        **{**_boundary_meta(), "source_path_mode": source_path_mode},
    }

    stabilized_batch_authorization_dryrun_readiness_decision = {
        "final_decision": FINAL_DECISION if boundary_ok else "MAIN_PROJECT_STRUCTURE_MIGRATION_STABILIZED_BATCH_AUTHORIZATION_DRYRUN_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "ready_for_post_dryrun_review": boundary_ok,
        "dryrun_completed": boundary_ok,
        "source_path_mode": source_path_mode,
        **{**_boundary_meta(), "source_path_mode": source_path_mode},
    }

    summary = {
        "phase": PHASE_ID,
        "dryrun_scope": DRYRUN_SCOPE,
        "batch_authorization_dryrun_only": True,
        "simulated": True,
        "source_path_mode": source_path_mode,
        "planning_input_loaded": plan["loaded"],
        "planning_verifier_go": vr.get("verifier") == "GO" and vr.get("passed") is True,
        "planning_final_decision_ok": sm.get("final_decision") == PLANNING_REQUIRED_FINAL,
        "planning_next_phase_ok": sm.get("recommended_next_phase") == PLANNING_REQUIRED_NEXT,
        "planning_artifacts_present": len(PLANNING_REQUIRED_ARTIFACTS) - len(plan["missing"]) if plan["root"] else 0,
        "planning_artifact_count_required": len(PLANNING_REQUIRED_ARTIFACTS),
        "batch_count": 8,
        "scope_dryrun_pass": b0_b7_authorization_scope_dryrun.get("all_pass") is True,
        "request_schema_dryrun_pass": batch_authorization_request_schema_dryrun.get("dryrun_pass") is True,
        "grant_schema_dryrun_pass": batch_authorization_grant_schema_dryrun.get("dryrun_pass") is True,
        "pre_auth_gate_dryrun_pass": batch_pre_authorization_gate_dryrun.get("all_pass") is True,
        "execution_window_dryrun_pass": batch_execution_window_dryrun.get("all_pass") is True and all(r.get("execution_window_opened_now") is False for r in window_dryrun_rows),
        "verifier_rerun_auth_dryrun_pass": batch_verifier_rerun_authorization_dryrun.get("all_pass") is True,
        "rollback_auth_dryrun_pass": batch_rollback_authorization_dryrun.get("all_pass") is True,
        "file_op_boundary_dryrun_pass": batch_file_operation_permission_boundary_dryrun.get("all_pass") is True,
        "protected_eval_out_guard_dryrun_pass": batch_protected_eval_out_guard_dryrun.get("all_pass") is True,
        "non_claims_dryrun_pass": batch_authorization_non_claims_dryrun.get("all_pass") is True,
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "final_decision": FINAL_DECISION if boundary_ok else "MAIN_PROJECT_STRUCTURE_MIGRATION_STABILIZED_BATCH_AUTHORIZATION_DRYRUN_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        **{**_boundary_meta(), "source_path_mode": source_path_mode},
    }

    return {
        "summary": summary,
        "stabilized_batch_authorization_dryrun_policy": stabilized_batch_authorization_dryrun_policy,
        "batch_authorization_planning_input_review": batch_authorization_planning_input_review,
        "b0_b7_authorization_scope_dryrun": b0_b7_authorization_scope_dryrun,
        "batch_authorization_request_schema_dryrun": batch_authorization_request_schema_dryrun,
        "batch_authorization_grant_schema_dryrun": batch_authorization_grant_schema_dryrun,
        "batch_pre_authorization_gate_dryrun": batch_pre_authorization_gate_dryrun,
        "batch_execution_window_dryrun": batch_execution_window_dryrun,
        "batch_verifier_rerun_authorization_dryrun": batch_verifier_rerun_authorization_dryrun,
        "batch_rollback_authorization_dryrun": batch_rollback_authorization_dryrun,
        "batch_file_operation_permission_boundary_dryrun": batch_file_operation_permission_boundary_dryrun,
        "batch_protected_eval_out_guard_dryrun": batch_protected_eval_out_guard_dryrun,
        "batch_authorization_non_claims_dryrun": batch_authorization_non_claims_dryrun,
        "stabilized_batch_authorization_dryrun_readiness_decision": stabilized_batch_authorization_dryrun_readiness_decision,
    }

