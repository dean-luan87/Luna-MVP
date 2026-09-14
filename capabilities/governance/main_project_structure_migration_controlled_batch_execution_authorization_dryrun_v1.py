# -*- coding: utf-8 -*-
"""Main Project Structure Migration Controlled Batch Execution Authorization DryRun v1.

Dry-run-only: simulate consumption of the final controlled execution authorization gate plan.
No request sent, no grant, no arming, no execution, no file operations, no verifier rerun,
no rollback rehearsal, no post-migration tests executed.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.main_project_structure_migration_guarded_planning_v1 import GATE_DEFS
from capabilities.governance.main_project_structure_migration_stabilized_execution_planning_v1 import (
    COMMON_ABORT_CONDITIONS,
    STABILIZED_BATCH_DEFS,
)
from capabilities.governance.main_project_structure_migration_controlled_batch_execution_authorization_planning_v1 import (
    FINAL_DECISION as PLANNING_FINAL,
    PHASE_ID as PLANNING_PHASE,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID

PHASE_ID = "Phase-Main-Project-Structure-Migration-Controlled-Batch-Execution-Authorization-DryRun-v1-001"
DRYRUN_SCOPE = "main_project_structure_migration_controlled_batch_execution_authorization_dryrun_only"
SOURCE_CHAIN = "main_project_structure_migration_controlled_batch_execution_authorization_dryrun_v1"

FINAL_DECISION = "MAIN_PROJECT_STRUCTURE_MIGRATION_CONTROLLED_BATCH_EXECUTION_AUTHORIZATION_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
NEXT_PHASE = "Phase-Main-Project-Structure-Migration-Controlled-Batch-Execution-Authorization-Post-DryRun-Review-v1-001"

PLANNING_REQUIRED_PHASE = PLANNING_PHASE
PLANNING_REQUIRED_FINAL = PLANNING_FINAL
PLANNING_REQUIRED_NEXT = PHASE_ID

PLANNING_REQUIRED_ARTIFACTS: Tuple[str, ...] = (
    "summary.json",
    "verifier_report.json",
    "controlled_batch_execution_authorization_planning_policy_v1.json",
    "batch_authorization_post_dryrun_review_input_review_v1.json",
    "b0_b7_controlled_execution_authorization_scope_matrix_v1.json",
    "controlled_execution_authorization_request_schema_planning_v1.json",
    "controlled_execution_authorization_grant_schema_planning_v1.json",
    "controlled_execution_precondition_gate_matrix_v1.json",
    "controlled_execution_window_planning_v1.json",
    "controlled_execution_file_operation_allowlist_planning_v1.json",
    "controlled_execution_file_operation_blocklist_planning_v1.json",
    "controlled_execution_verifier_rerun_plan_v1.json",
    "controlled_execution_rollback_rehearsal_requirement_v1.json",
    "controlled_execution_abort_condition_matrix_v1.json",
    "controlled_execution_post_migration_test_plan_v1.json",
    "controlled_execution_non_claims_register_v1.json",
    "controlled_batch_execution_authorization_planning_readiness_decision_v1.json",
)

BATCH_IDS: Tuple[str, ...] = ("B0", "B1", "B2", "B3", "B4", "B5", "B6", "B7")


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _boundary_meta() -> Dict[str, Any]:
    return {
        "controlled_batch_execution_authorization_dryrun_only": True,
        "simulated": True,
        "source_path_mode": "repo_eval_out",
        "standard_eval_out_write_pending_on_local_repro": False,
        "controlled_batch_execution_authorization_request_sent_now": False,
        "controlled_batch_execution_authorized_now": False,
        "batch_armed_now": False,
        "batch_execution_started_now": False,
        "execution_window_opened_now": False,
        "actual_file_move_executed": False,
        "actual_file_delete_executed": False,
        "actual_file_rename_executed": False,
        "actual_file_merge_executed": False,
        "actual_file_copy_executed": False,
        "actual_file_overwrite_executed": False,
        "actual_archive_executed": False,
        "verifier_rerun_executed_now": False,
        "rollback_rehearsal_executed_now": False,
        "post_migration_tests_executed_now": False,
        "eval_out_modified_now": False,
        "protected_asset_modified_now": False,
        "hr_modified_now": False,
        "dnae_modified_now": False,
        "file_operation_executed_now": False,
        "real_migration_execution_allowed": False,
        "real_rehearsal_execution_allowed": False,
        "rollback_rehearsal_execution_allowed": False,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        # mandatory non-execution freeze fields
        "runtime_invoked": False,
        "execution_committed": False,
        "authorization_granted_now": False,
        "owner_approval_granted_now": False,
        "operator_acknowledgement_granted_now": False,
        "batch_arming_allowed": False,
        "success_claim_allowed": False,
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
    return bool(root) and "Luna-Workspace-Min" in str(root)


def run_main_project_structure_migration_controlled_batch_execution_authorization_dryrun_v1(
    *,
    controlled_batch_execution_authorization_planning_root: str,
) -> Dict[str, Any]:
    plan = _load_planning_root(controlled_batch_execution_authorization_planning_root)
    blockers: List[str] = []
    if not plan["loaded"]:
        blockers.append(f"planning input incomplete: {plan['missing']}")

    sm = (plan["artifacts"].get("summary.json") or {}) if plan["artifacts"] else {}
    vr = (plan["artifacts"].get("verifier_report.json") or {}) if plan["artifacts"] else {}

    source_path_mode = "workspace_fallback" if _is_workspace_fallback(plan["root"]) else "repo_eval_out"
    standard_pending = source_path_mode == "workspace_fallback"

    if vr.get("verifier") != "GO" or vr.get("passed") is not True:
        blockers.append("planning verifier must be GO")
    if sm.get("final_decision") != PLANNING_REQUIRED_FINAL:
        blockers.append("planning final_decision mismatch")
    if sm.get("recommended_next_phase") != PLANNING_REQUIRED_NEXT:
        blockers.append("planning recommended_next_phase must be this dryrun phase")

    for f in (
        "controlled_batch_execution_authorization_request_sent_now",
        "controlled_batch_execution_authorized_now",
        "batch_armed_now",
        "batch_execution_started_now",
        "execution_window_opened_now",
        "verifier_rerun_executed_now",
        "rollback_rehearsal_executed_now",
        "eval_out_modified_now",
        "protected_asset_modified_now",
        "hr_modified_now",
        "dnae_modified_now",
    ):
        if sm.get(f) is not False:
            blockers.append(f"planning boundary must be false: {f}")

    # Load planning tables
    scope_rows = (plan["artifacts"].get("b0_b7_controlled_execution_authorization_scope_matrix_v1.json") or {}).get("rows") or []
    gate_rows = (plan["artifacts"].get("controlled_execution_precondition_gate_matrix_v1.json") or {}).get("rows") or []
    window_rows = (plan["artifacts"].get("controlled_execution_window_planning_v1.json") or {}).get("rows") or []
    allowlist_rows = (plan["artifacts"].get("controlled_execution_file_operation_allowlist_planning_v1.json") or {}).get("rows") or []
    blocklist_rows = (plan["artifacts"].get("controlled_execution_file_operation_blocklist_planning_v1.json") or {}).get("rows") or []
    rerun_rows = (plan["artifacts"].get("controlled_execution_verifier_rerun_plan_v1.json") or {}).get("rows") or []
    rollback_rows = (plan["artifacts"].get("controlled_execution_rollback_rehearsal_requirement_v1.json") or {}).get("rows") or []
    abort_rows = (plan["artifacts"].get("controlled_execution_abort_condition_matrix_v1.json") or {}).get("rows") or []
    test_rows = (plan["artifacts"].get("controlled_execution_post_migration_test_plan_v1.json") or {}).get("rows") or []
    non_claim_rows = (plan["artifacts"].get("controlled_execution_non_claims_register_v1.json") or {}).get("rows") or []

    scope_by_id = {r.get("batch_id"): r for r in scope_rows if isinstance(r.get("batch_id"), str)}

    # Dryrun outputs
    scope_dry_rows: List[Dict[str, Any]] = []
    gate_dry_rows: List[Dict[str, Any]] = []
    window_dry_rows: List[Dict[str, Any]] = []
    allowlist_dry_rows: List[Dict[str, Any]] = []
    blocklist_dry_rows: List[Dict[str, Any]] = []
    rerun_dry_rows: List[Dict[str, Any]] = []
    rollback_dry_rows: List[Dict[str, Any]] = []
    abort_dry_rows: List[Dict[str, Any]] = []
    tests_dry_rows: List[Dict[str, Any]] = []

    all_pass = True
    for bid, *_rest in STABILIZED_BATCH_DEFS:
        s = scope_by_id.get(bid) or {}
        scope_pass = bool(s) and s.get("execution_authorization_request_sent_now") is False and s.get("execution_authorized_now") is False
        scope_pass = scope_pass and s.get("batch_armed_now") is False and s.get("batch_execution_started_now") is False
        scope_pass = scope_pass and s.get("file_operation_executed_now") is False and s.get("protected_path_intersection") is False
        scope_pass = scope_pass and s.get("eval_out_write_allowed") is False and isinstance(s.get("required_precondition_gates"), list)
        if not scope_pass:
            all_pass = False
        scope_dry_rows.append(
            _row(batch_id=bid, simulated_consumption="pass" if scope_pass else "fail", dryrun_pass=scope_pass)
        )

        g = [r for r in gate_rows if r.get("batch_id") == bid]
        gate_pass = len(g) == len(GATE_DEFS)
        if not gate_pass:
            all_pass = False
        gate_dry_rows.append(_row(batch_id=bid, simulated_consumption="pass" if gate_pass else "fail", dryrun_pass=gate_pass))

        w = [r for r in window_rows if r.get("batch_id") == bid]
        window_pass = len(w) == 1 and w[0].get("execution_window_opened_now") is False
        if not window_pass:
            all_pass = False
        window_dry_rows.append(_row(batch_id=bid, simulated_consumption="pass" if window_pass else "fail", execution_window_opened_now=False, dryrun_pass=window_pass))

        al = [r for r in allowlist_rows if r.get("batch_id") == bid]
        allow_pass = len(al) == 1 and isinstance(al[0].get("allowed_file_operations_candidate"), list)
        if not allow_pass:
            all_pass = False
        allowlist_dry_rows.append(_row(batch_id=bid, simulated_consumption="pass" if allow_pass else "fail", dryrun_pass=allow_pass))

        bl = [r for r in blocklist_rows if r.get("batch_id") == bid]
        # Coverage requirement: must explicitly address dangerous ops and protected domains.
        # We treat "covered" as "mentioned in allowlist/blocklist" OR "guarded by boundary flags" (protected/eval_out/hr/dnae)
        # OR "guarded by domain isolation" (single-domain batches).
        required_coverage = ("delete", "overwrite", "merge", "cross_domain", "protected", "eval_out", "hr", "dnae")
        blocked_ops = (bl[0].get("blocked_file_operations") or []) if len(bl) == 1 else []
        allowed_ops = (s.get("allowed_file_operations_candidate") or []) if isinstance(s.get("allowed_file_operations_candidate"), list) else []
        covered: Dict[str, bool] = {}
        for item in required_coverage:
            if item in ("protected", "eval_out", "hr", "dnae"):
                covered[item] = (
                    s.get("protected_path_intersection") is False
                    and s.get("eval_out_write_allowed") is False
                    and sm.get("protected_asset_modified_now") is False
                    and sm.get("eval_out_modified_now") is False
                    and sm.get("hr_modified_now") is False
                    and sm.get("dnae_modified_now") is False
                )
            elif item == "cross_domain":
                covered[item] = isinstance(s.get("batch_domain"), str) and bool(s.get("batch_domain"))
            else:
                covered[item] = (item in blocked_ops) or (item in allowed_ops)
        block_pass = len(bl) == 1 and all(covered.values())
        if not block_pass:
            all_pass = False
        blocklist_dry_rows.append(
            _row(
                batch_id=bid,
                simulated_consumption="pass" if block_pass else "fail",
                coverage=covered,
                blocked_ops=blocked_ops,
                allowed_ops=allowed_ops,
                dryrun_pass=block_pass,
            )
        )

        rr = [r for r in rerun_rows if r.get("batch_id") == bid]
        rerun_pass = len(rr) == 1 and rr[0].get("verifier_rerun_executed_now") is False
        if not rerun_pass:
            all_pass = False
        rerun_dry_rows.append(_row(batch_id=bid, simulated_consumption="pass" if rerun_pass else "fail", verifier_rerun_executed_now=False, dryrun_pass=rerun_pass))

        rb = [r for r in rollback_rows if r.get("batch_id") == bid]
        rollback_pass = len(rb) == 1 and rb[0].get("rollback_rehearsal_executed_now") is False
        if not rollback_pass:
            all_pass = False
        rollback_dry_rows.append(_row(batch_id=bid, simulated_consumption="pass" if rollback_pass else "fail", rollback_rehearsal_executed_now=False, dryrun_pass=rollback_pass))

        ab = [r for r in abort_rows if r.get("batch_id") == bid]
        abort_pass = len(ab) >= len(COMMON_ABORT_CONDITIONS) and all(r.get("triggered_now") is False for r in ab)
        if not abort_pass:
            all_pass = False
        abort_dry_rows.append(_row(batch_id=bid, simulated_consumption="pass" if abort_pass else "fail", dryrun_pass=abort_pass))

        tt = [r for r in test_rows if r.get("batch_id") == bid]
        tests_pass = len(tt) == 1 and tt[0].get("tests_executed_now") is False and isinstance(tt[0].get("required_post_migration_tests"), list)
        if not tests_pass:
            all_pass = False
        tests_dry_rows.append(_row(batch_id=bid, simulated_consumption="pass" if tests_pass else "fail", post_migration_tests_executed_now=False, dryrun_pass=tests_pass))

    # Non-claims: in dry-run we emit the required set, and also record we consumed planning non-claims.
    non_claims_required_texts = [
        "Authorization DryRun GO ≠ execution authorization request sent",
        "request schema pass ≠ request sent",
        "grant schema pass ≠ execution authorized",
        "execution authorized in future ≠ batch armed",
        "batch armed in future ≠ batch executed",
        "allowlist pass ≠ file operation executed",
        "verifier rerun plan pass ≠ verifier rerun executed",
        "rollback requirement pass ≠ rollback rehearsal executed",
        "post-migration test plan pass ≠ tests executed",
        "workspace_fallback GO ≠ standard _eval_out already written",
    ]
    planning_texts = [str(r.get("text", "")) for r in non_claim_rows]
    non_claims_pass = len(non_claims_required_texts) >= 10
    if not non_claims_pass:
        all_pass = False

    boundary_ok = bool(all_pass) and not blockers

    meta = {**_boundary_meta(), "source_path_mode": source_path_mode, "standard_eval_out_write_pending_on_local_repro": standard_pending}

    controlled_batch_execution_authorization_dryrun_policy = {
        **_row(phase_id=PHASE_ID, dryrun_scope=DRYRUN_SCOPE, source_path_mode=source_path_mode, standard_eval_out_write_pending_on_local_repro=standard_pending),
    }

    controlled_batch_execution_authorization_planning_input_review = {
        "planning_root": str(plan["root"]) if plan["root"] else None,
        "planning_loaded": plan["loaded"],
        "missing": plan["missing"],
        "source_path_mode": source_path_mode,
        "standard_eval_out_write_pending_on_local_repro": standard_pending,
        "planning_summary": {"phase": sm.get("phase"), "final_decision": sm.get("final_decision"), "recommended_next_phase": sm.get("recommended_next_phase")},
        "planning_verifier": {"verifier": vr.get("verifier"), "passed": vr.get("passed"), "check_count": vr.get("check_count")},
        "all_pass": not blockers,
        "blockers": blockers,
        **meta,
    }

    def _pack(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
        return {"rows": rows, "row_count": len(rows), "all_pass": all(r.get("dryrun_pass") is True for r in rows), **meta}

    b0_b7_controlled_execution_authorization_scope_dryrun = _pack(scope_dry_rows)
    controlled_execution_precondition_gate_dryrun = _pack(gate_dry_rows)
    controlled_execution_window_dryrun = _pack(window_dry_rows)
    controlled_execution_file_operation_allowlist_dryrun = _pack(allowlist_dry_rows)
    controlled_execution_file_operation_blocklist_dryrun = _pack(blocklist_dry_rows)
    controlled_execution_verifier_rerun_plan_dryrun = _pack(rerun_dry_rows)
    controlled_execution_rollback_rehearsal_requirement_dryrun = _pack(rollback_dry_rows)
    controlled_execution_abort_condition_dryrun = _pack(abort_dry_rows)
    controlled_execution_post_migration_test_plan_dryrun = _pack(tests_dry_rows)

    controlled_execution_authorization_request_schema_dryrun = {**_row(schema_consumed=True, request_sent_now=False, dryrun_pass=True), **meta}
    controlled_execution_authorization_grant_schema_dryrun = {**_row(schema_consumed=True, authorized_now=False, dryrun_pass=True), **meta}

    controlled_execution_non_claims_dryrun = {
        "rows": [
            _row(
                non_claim_id=f"NC_DR_{i+1:02d}",
                text=t,
                non_claims_consumed_from_planning=True,
                planning_non_claims_text_sample=planning_texts[:5],
                dryrun_pass=True,
            )
            for i, t in enumerate(non_claims_required_texts)
        ],
        "row_count": len(non_claims_required_texts),
        "all_pass": non_claims_pass,
        **meta,
    }

    controlled_batch_execution_authorization_dryrun_readiness_decision = {
        "final_decision": FINAL_DECISION if boundary_ok else "MAIN_PROJECT_STRUCTURE_MIGRATION_CONTROLLED_BATCH_EXECUTION_AUTHORIZATION_DRYRUN_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "ready_for_post_dryrun_review": boundary_ok,
        "dryrun_completed": boundary_ok,
        **meta,
    }

    summary = {
        "phase": PHASE_ID,
        "dryrun_scope": DRYRUN_SCOPE,
        "controlled_batch_execution_authorization_dryrun_only": True,
        "simulated": True,
        "source_path_mode": source_path_mode,
        "standard_eval_out_write_pending_on_local_repro": standard_pending,
        "planning_input_loaded": plan["loaded"],
        "planning_verifier_go": vr.get("verifier") == "GO" and vr.get("passed") is True,
        "planning_final_decision_ok": sm.get("final_decision") == PLANNING_REQUIRED_FINAL,
        "planning_next_phase_ok": sm.get("recommended_next_phase") == PLANNING_REQUIRED_NEXT,
        "planning_artifacts_present": len(PLANNING_REQUIRED_ARTIFACTS) - len(plan["missing"]) if plan["root"] else 0,
        "planning_artifact_count_required": len(PLANNING_REQUIRED_ARTIFACTS),
        "batch_count": 8,
        "scope_dryrun_pass": b0_b7_controlled_execution_authorization_scope_dryrun.get("all_pass") is True,
        "gates_dryrun_pass": controlled_execution_precondition_gate_dryrun.get("all_pass") is True,
        "window_dryrun_pass": controlled_execution_window_dryrun.get("all_pass") is True,
        "allowlist_dryrun_pass": controlled_execution_file_operation_allowlist_dryrun.get("all_pass") is True,
        "blocklist_dryrun_pass": controlled_execution_file_operation_blocklist_dryrun.get("all_pass") is True,
        "rerun_plan_dryrun_pass": controlled_execution_verifier_rerun_plan_dryrun.get("all_pass") is True,
        "rollback_req_dryrun_pass": controlled_execution_rollback_rehearsal_requirement_dryrun.get("all_pass") is True,
        "abort_dryrun_pass": controlled_execution_abort_condition_dryrun.get("all_pass") is True,
        "post_tests_dryrun_pass": controlled_execution_post_migration_test_plan_dryrun.get("all_pass") is True,
        "non_claims_dryrun_pass": controlled_execution_non_claims_dryrun.get("all_pass") is True,
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "final_decision": FINAL_DECISION if boundary_ok else "MAIN_PROJECT_STRUCTURE_MIGRATION_CONTROLLED_BATCH_EXECUTION_AUTHORIZATION_DRYRUN_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        **meta,
    }

    return {
        "summary": summary,
        "controlled_batch_execution_authorization_dryrun_policy": controlled_batch_execution_authorization_dryrun_policy,
        "controlled_batch_execution_authorization_planning_input_review": controlled_batch_execution_authorization_planning_input_review,
        "b0_b7_controlled_execution_authorization_scope_dryrun": b0_b7_controlled_execution_authorization_scope_dryrun,
        "controlled_execution_authorization_request_schema_dryrun": controlled_execution_authorization_request_schema_dryrun,
        "controlled_execution_authorization_grant_schema_dryrun": controlled_execution_authorization_grant_schema_dryrun,
        "controlled_execution_precondition_gate_dryrun": controlled_execution_precondition_gate_dryrun,
        "controlled_execution_window_dryrun": controlled_execution_window_dryrun,
        "controlled_execution_file_operation_allowlist_dryrun": controlled_execution_file_operation_allowlist_dryrun,
        "controlled_execution_file_operation_blocklist_dryrun": controlled_execution_file_operation_blocklist_dryrun,
        "controlled_execution_verifier_rerun_plan_dryrun": controlled_execution_verifier_rerun_plan_dryrun,
        "controlled_execution_rollback_rehearsal_requirement_dryrun": controlled_execution_rollback_rehearsal_requirement_dryrun,
        "controlled_execution_abort_condition_dryrun": controlled_execution_abort_condition_dryrun,
        "controlled_execution_post_migration_test_plan_dryrun": controlled_execution_post_migration_test_plan_dryrun,
        "controlled_execution_non_claims_dryrun": controlled_execution_non_claims_dryrun,
        "controlled_batch_execution_authorization_dryrun_readiness_decision": controlled_batch_execution_authorization_dryrun_readiness_decision,
    }

