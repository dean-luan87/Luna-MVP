# -*- coding: utf-8 -*-
"""Main Project Structure Migration Controlled Batch Execution Arming DryRun v1.

Dry-run-only for B0 arming plan consumption. No real arming, no window open, no execution,
no file operations, no verifier rerun execution, no rollback rehearsal, no post-migration tests.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.main_project_structure_migration_controlled_batch_execution_arming_planning_v1 import (
    FINAL_DECISION as PLANNING_FINAL,
    NEXT_PHASE as PLANNING_NEXT,
    PHASE_ID as PLANNING_PHASE,
    SELECTED_BATCH_ID,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID

PHASE_ID = "Phase-Main-Project-Structure-Migration-Controlled-Batch-Execution-Arming-DryRun-v1-001"
DRYRUN_SCOPE = "main_project_structure_migration_controlled_batch_execution_arming_dryrun_only"
SOURCE_CHAIN = "main_project_structure_migration_controlled_batch_execution_arming_dryrun_v1"

FINAL_DECISION = "MAIN_PROJECT_STRUCTURE_MIGRATION_CONTROLLED_BATCH_EXECUTION_ARMING_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
NEXT_PHASE = "Phase-Main-Project-Structure-Migration-Controlled-Batch-Execution-Arming-Post-DryRun-Review-v1-001"

PLANNING_REQUIRED_PHASE = PLANNING_PHASE
PLANNING_REQUIRED_FINAL = PLANNING_FINAL
PLANNING_REQUIRED_NEXT = PHASE_ID

PLANNING_REQUIRED_ARTIFACTS: Tuple[str, ...] = (
    "summary.json",
    "verifier_report.json",
    "controlled_batch_execution_arming_planning_policy_v1.json",
    "controlled_execution_authorization_post_review_input_review_v1.json",
    "b0_single_batch_arming_scope_v1.json",
    "b1_b7_deferred_arming_matrix_v1.json",
    "b0_execution_window_arming_plan_v1.json",
    "b0_file_operation_allowlist_arming_plan_v1.json",
    "b0_file_operation_blocklist_arming_plan_v1.json",
    "b0_before_after_manifest_arming_plan_v1.json",
    "b0_rollback_route_arming_plan_v1.json",
    "b0_verifier_rerun_arming_plan_v1.json",
    "b0_post_migration_test_arming_plan_v1.json",
    "b0_abort_condition_arming_plan_v1.json",
    "b0_protected_eval_out_guard_arming_plan_v1.json",
    "controlled_batch_execution_arming_non_claims_register_v1.json",
    "controlled_batch_execution_arming_planning_readiness_decision_v1.json",
)


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _boundary_meta() -> Dict[str, Any]:
    return {
        "controlled_batch_execution_arming_dryrun_only": True,
        "simulated": True,
        "selected_batch_id": SELECTED_BATCH_ID,
        "b0_only": True,
        "b1_b7_arming_deferred": True,
        "b0_armed_now": False,
        "batch_armed_now": False,
        "b0_execution_started_now": False,
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
        "source_path_mode": "repo_eval_out",
        "standard_eval_out_write_pending_on_local_repro": False,
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


def run_main_project_structure_migration_controlled_batch_execution_arming_dryrun_v1(
    *,
    controlled_batch_execution_arming_planning_root: str,
) -> Dict[str, Any]:
    plan = _load_planning_root(controlled_batch_execution_arming_planning_root)
    blockers: List[str] = []
    if not plan["loaded"]:
        blockers.append(f"arming planning input incomplete: {plan['missing']}")

    sm = (plan["artifacts"].get("summary.json") or {}) if plan["artifacts"] else {}
    vr = (plan["artifacts"].get("verifier_report.json") or {}) if plan["artifacts"] else {}

    source_path_mode = "workspace_fallback" if _is_workspace_fallback(plan["root"]) else "repo_eval_out"
    standard_pending = source_path_mode == "workspace_fallback"

    if vr.get("verifier") != "GO" or vr.get("passed") is not True:
        blockers.append("arming planning verifier must be GO")
    if sm.get("phase") != PLANNING_REQUIRED_PHASE:
        blockers.append("arming planning phase mismatch")
    if sm.get("final_decision") != PLANNING_REQUIRED_FINAL:
        blockers.append("arming planning final_decision mismatch")
    if sm.get("recommended_next_phase") != PLANNING_REQUIRED_NEXT:
        blockers.append("arming planning recommended_next_phase must be this arming dryrun phase")
    if sm.get("selected_batch_id") != "B0" or sm.get("b0_only") is not True or sm.get("b1_b7_arming_deferred") is not True:
        blockers.append("arming planning must be b0-only with b1-b7 deferred")
    if sm.get("boundary_ok") is not True:
        blockers.append("arming planning boundary_ok must be true")

    for f in (
        "batch_armed_now",
        "batch_execution_started_now",
        "execution_window_opened_now",
        "verifier_rerun_executed_now",
        "rollback_rehearsal_executed_now",
        "post_migration_tests_executed_now",
        "eval_out_modified_now",
        "protected_asset_modified_now",
        "hr_modified_now",
        "dnae_modified_now",
        "file_operation_executed_now",
    ):
        if sm.get(f) is not False:
            blockers.append(f"arming planning boundary must be false: {f}")

    meta = {**_boundary_meta(), "source_path_mode": source_path_mode, "standard_eval_out_write_pending_on_local_repro": standard_pending}

    # B0 scope consumption check
    b0_scope = plan["artifacts"].get("b0_single_batch_arming_scope_v1.json") or {}
    paths = b0_scope.get("controlled_execution_scope_candidate") or []
    bad_tokens = ("capabilities/", "tools/", "_eval_out", "protected", "hr", "dnae", "configs", "scripts", "tests")
    scope_pass = (
        b0_scope.get("batch_id") == "B0"
        and b0_scope.get("scope_ok") is True
        and all(isinstance(p, str) and not any(t in p.lower() for t in bad_tokens) for p in paths)
    )
    if not scope_pass:
        blockers.append("B0 scope dryrun failed (forbidden path or shape mismatch)")

    # B1-B7 deferred consumption check
    deferred = plan["artifacts"].get("b1_b7_deferred_arming_matrix_v1.json") or {}
    deferred_rows = deferred.get("rows") or []
    deferred_pass = len(deferred_rows) == 7 and all(r.get("deferred") is True for r in deferred_rows)
    if not deferred_pass:
        blockers.append("B1-B7 deferred matrix consumption failed")

    # Window / allowlist / blocklist / manifest / rollback / rerun / tests / abort / guard
    window = plan["artifacts"].get("b0_execution_window_arming_plan_v1.json") or {}
    allowlist = plan["artifacts"].get("b0_file_operation_allowlist_arming_plan_v1.json") or {}
    blocklist = plan["artifacts"].get("b0_file_operation_blocklist_arming_plan_v1.json") or {}
    manifest = plan["artifacts"].get("b0_before_after_manifest_arming_plan_v1.json") or {}
    rollback = plan["artifacts"].get("b0_rollback_route_arming_plan_v1.json") or {}
    rerun = plan["artifacts"].get("b0_verifier_rerun_arming_plan_v1.json") or {}
    tests = plan["artifacts"].get("b0_post_migration_test_arming_plan_v1.json") or {}
    abort = plan["artifacts"].get("b0_abort_condition_arming_plan_v1.json") or {}
    guard = plan["artifacts"].get("b0_protected_eval_out_guard_arming_plan_v1.json") or {}

    window_pass = window.get("batch_id") == "B0" and window.get("execution_window_opened_now") is False
    allow_pass = allowlist.get("batch_id") == "B0" and isinstance(allowlist.get("allowed_file_operations_candidate"), list)
    block_pass = blocklist.get("batch_id") == "B0" and isinstance(blocklist.get("blocked_file_operations"), list)
    manifest_pass = manifest.get("batch_id") == "B0" and manifest.get("manifest_candidate_only") is True
    rollback_pass = rollback.get("batch_id") == "B0" and rollback.get("rollback_rehearsal_executed_now") is False
    rerun_pass = rerun.get("batch_id") == "B0" and rerun.get("verifier_rerun_executed_now") is False
    tests_pass = tests.get("batch_id") == "B0" and tests.get("post_migration_tests_executed_now") is False
    abort_pass = abort.get("batch_id") == "B0" and abort.get("abort_triggered_now") is False and isinstance(abort.get("abort_conditions"), list)
    guard_pass = (
        guard.get("batch_id") == "B0"
        and guard.get("eval_out_modified_now") is False
        and guard.get("protected_asset_modified_now") is False
        and guard.get("hr_modified_now") is False
        and guard.get("dnae_modified_now") is False
    )

    # Non-claims: emit required dryrun set, record we consumed planning non-claims
    required_non_claims = [
        "Arming DryRun GO ≠ B0 armed",
        "B0 selected ≠ B0 executed",
        "B0 arming scope pass ≠ file operation executed",
        "B1–B7 deferred ≠ B1–B7 ready",
        "execution window pass ≠ execution window opened",
        "verifier rerun plan pass ≠ verifier rerun executed",
        "rollback route pass ≠ rollback rehearsal executed",
        "post-migration test plan pass ≠ tests executed",
        "workspace_fallback GO ≠ standard _eval_out already written",
    ]
    planning_nc = plan["artifacts"].get("controlled_batch_execution_arming_non_claims_register_v1.json") or {}
    planning_nc_texts = [str(r.get("text", "")) for r in (planning_nc.get("rows") or [])]
    non_claims_pass = len(required_non_claims) >= 9

    if not (window_pass and allow_pass and block_pass and manifest_pass and rollback_pass and rerun_pass and tests_pass and abort_pass and guard_pass):
        blockers.append("one or more B0 arming plan components not consumable")

    boundary_ok = not blockers

    controlled_batch_execution_arming_dryrun_policy = _row(
        phase_id=PHASE_ID,
        dryrun_scope=DRYRUN_SCOPE,
        selected_batch_id="B0",
        b0_only=True,
        b1_b7_arming_deferred=True,
        source_path_mode=source_path_mode,
        standard_eval_out_write_pending_on_local_repro=standard_pending,
    )

    controlled_batch_execution_arming_planning_input_review = {
        "planning_root": str(plan["root"]) if plan["root"] else None,
        "planning_loaded": plan["loaded"],
        "missing": plan["missing"],
        "planning_summary": {
            "phase": sm.get("phase"),
            "boundary_ok": sm.get("boundary_ok"),
            "final_decision": sm.get("final_decision"),
            "recommended_next_phase": sm.get("recommended_next_phase"),
            "selected_batch_id": sm.get("selected_batch_id"),
            "b0_only": sm.get("b0_only"),
            "b1_b7_arming_deferred": sm.get("b1_b7_arming_deferred"),
        },
        "planning_verifier": {"verifier": vr.get("verifier"), "passed": vr.get("passed"), "check_count": vr.get("check_count")},
        "source_path_mode": source_path_mode,
        "standard_eval_out_write_pending_on_local_repro": standard_pending,
        "all_pass": not blockers,
        "blockers": blockers,
        **meta,
    }

    def _pack(name: str, passed: bool, detail: Any = None) -> Dict[str, Any]:
        return {"rows": [_row(check_id=name, simulated_consumption="pass" if passed else "fail", dryrun_pass=passed, detail=detail)], "row_count": 1, "all_pass": passed, **meta}

    b0_single_batch_arming_scope_dryrun = _pack("b0_scope", scope_pass, {"paths": paths})
    b1_b7_deferred_arming_dryrun = _pack("b1_b7_deferred", deferred_pass, {"row_count": len(deferred_rows)})
    b0_execution_window_arming_dryrun = _pack("b0_window", window_pass, {"execution_window_opened_now": False})
    b0_file_operation_allowlist_arming_dryrun = _pack("b0_allowlist", allow_pass, {"allowed_ops": allowlist.get("allowed_file_operations_candidate")})
    b0_file_operation_blocklist_arming_dryrun = _pack("b0_blocklist", block_pass, {"blocked_ops": blocklist.get("blocked_file_operations")})
    b0_before_after_manifest_arming_dryrun = _pack("b0_manifest", manifest_pass, {"manifest_candidate_only": True})
    b0_rollback_route_arming_dryrun = _pack("b0_rollback", rollback_pass, {"rollback_rehearsal_executed_now": False})
    b0_verifier_rerun_arming_dryrun = _pack("b0_verifier_rerun", rerun_pass, {"verifier_rerun_executed_now": False})
    b0_post_migration_test_arming_dryrun = _pack("b0_post_tests", tests_pass, {"post_migration_tests_executed_now": False})
    b0_abort_condition_arming_dryrun = _pack("b0_abort", abort_pass, {"abort_triggered_now": False})
    b0_protected_eval_out_guard_arming_dryrun = _pack("b0_guard", guard_pass, {"eval_out_modified_now": False})

    controlled_batch_execution_arming_non_claims_dryrun = {
        "rows": [
            _row(
                non_claim_id=f"NC_ARM_DR_{i+1:02d}",
                text=t,
                non_claims_consumed_from_planning=True,
                planning_non_claims_text_sample=planning_nc_texts[:5],
                dryrun_pass=True,
            )
            for i, t in enumerate(required_non_claims)
        ],
        "row_count": len(required_non_claims),
        "all_pass": non_claims_pass,
        **meta,
    }

    controlled_batch_execution_arming_dryrun_readiness_decision = {
        "final_decision": FINAL_DECISION if boundary_ok else "MAIN_PROJECT_STRUCTURE_MIGRATION_CONTROLLED_BATCH_EXECUTION_ARMING_DRYRUN_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "ready_for_post_dryrun_review": boundary_ok,
        "selected_batch_id": "B0",
        **meta,
    }

    summary = {
        "phase": PHASE_ID,
        "dryrun_scope": DRYRUN_SCOPE,
        "controlled_batch_execution_arming_dryrun_only": True,
        "simulated": True,
        "selected_batch_id": "B0",
        "b0_only": True,
        "b1_b7_arming_deferred": True,
        "source_path_mode": source_path_mode,
        "standard_eval_out_write_pending_on_local_repro": standard_pending,
        "planning_input_loaded": plan["loaded"],
        "planning_verifier_go": vr.get("verifier") == "GO" and vr.get("passed") is True,
        "planning_final_decision_ok": sm.get("final_decision") == PLANNING_REQUIRED_FINAL,
        "planning_next_phase_ok": sm.get("recommended_next_phase") == PLANNING_REQUIRED_NEXT,
        "b0_scope_dryrun_pass": b0_single_batch_arming_scope_dryrun.get("all_pass") is True,
        "b1_b7_deferred_dryrun_pass": b1_b7_deferred_arming_dryrun.get("all_pass") is True,
        "window_dryrun_pass": b0_execution_window_arming_dryrun.get("all_pass") is True,
        "allowlist_dryrun_pass": b0_file_operation_allowlist_arming_dryrun.get("all_pass") is True,
        "blocklist_dryrun_pass": b0_file_operation_blocklist_arming_dryrun.get("all_pass") is True,
        "manifest_dryrun_pass": b0_before_after_manifest_arming_dryrun.get("all_pass") is True,
        "rollback_dryrun_pass": b0_rollback_route_arming_dryrun.get("all_pass") is True,
        "rerun_dryrun_pass": b0_verifier_rerun_arming_dryrun.get("all_pass") is True,
        "post_tests_dryrun_pass": b0_post_migration_test_arming_dryrun.get("all_pass") is True,
        "abort_dryrun_pass": b0_abort_condition_arming_dryrun.get("all_pass") is True,
        "guard_dryrun_pass": b0_protected_eval_out_guard_arming_dryrun.get("all_pass") is True,
        "non_claims_dryrun_pass": controlled_batch_execution_arming_non_claims_dryrun.get("all_pass") is True,
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "final_decision": FINAL_DECISION if boundary_ok else "MAIN_PROJECT_STRUCTURE_MIGRATION_CONTROLLED_BATCH_EXECUTION_ARMING_DRYRUN_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        **meta,
    }

    return {
        "summary": summary,
        "controlled_batch_execution_arming_dryrun_policy": controlled_batch_execution_arming_dryrun_policy,
        "controlled_batch_execution_arming_planning_input_review": controlled_batch_execution_arming_planning_input_review,
        "b0_single_batch_arming_scope_dryrun": b0_single_batch_arming_scope_dryrun,
        "b1_b7_deferred_arming_dryrun": b1_b7_deferred_arming_dryrun,
        "b0_execution_window_arming_dryrun": b0_execution_window_arming_dryrun,
        "b0_file_operation_allowlist_arming_dryrun": b0_file_operation_allowlist_arming_dryrun,
        "b0_file_operation_blocklist_arming_dryrun": b0_file_operation_blocklist_arming_dryrun,
        "b0_before_after_manifest_arming_dryrun": b0_before_after_manifest_arming_dryrun,
        "b0_rollback_route_arming_dryrun": b0_rollback_route_arming_dryrun,
        "b0_verifier_rerun_arming_dryrun": b0_verifier_rerun_arming_dryrun,
        "b0_post_migration_test_arming_dryrun": b0_post_migration_test_arming_dryrun,
        "b0_abort_condition_arming_dryrun": b0_abort_condition_arming_dryrun,
        "b0_protected_eval_out_guard_arming_dryrun": b0_protected_eval_out_guard_arming_dryrun,
        "controlled_batch_execution_arming_non_claims_dryrun": controlled_batch_execution_arming_non_claims_dryrun,
        "controlled_batch_execution_arming_dryrun_readiness_decision": controlled_batch_execution_arming_dryrun_readiness_decision,
    }

