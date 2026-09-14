# -*- coding: utf-8 -*-
"""Main Project Structure Migration Controlled Batch Execution B0 Arming Request DryRun v1.

Dry-run-only: simulate consumption of B0 arming request planning artifacts.
No request artifact generation, no request sent, no authorization, no arming, no window open,
no execution, no file operations, no verifier rerun execution, no rollback rehearsal,
no post-migration tests.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.main_project_structure_migration_controlled_batch_execution_b0_arming_request_planning_v1 import (
    FINAL_DECISION as PLANNING_FINAL,
    NEXT_PHASE as PLANNING_NEXT,
    PHASE_ID as PLANNING_PHASE,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID

PHASE_ID = "Phase-Main-Project-Structure-Migration-Controlled-Batch-Execution-B0-Arming-Request-DryRun-v1-001"
DRYRUN_SCOPE = "main_project_structure_migration_controlled_batch_execution_b0_arming_request_dryrun_only"
SOURCE_CHAIN = "main_project_structure_migration_controlled_batch_execution_b0_arming_request_dryrun_v1"

FINAL_DECISION = "MAIN_PROJECT_STRUCTURE_MIGRATION_CONTROLLED_BATCH_EXECUTION_B0_ARMING_REQUEST_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
NEXT_PHASE = "Phase-Main-Project-Structure-Migration-Controlled-Batch-Execution-B0-Arming-Request-Post-DryRun-Review-v1-001"

PLANNING_REQUIRED_PHASE = PLANNING_PHASE
PLANNING_REQUIRED_FINAL = PLANNING_FINAL
PLANNING_REQUIRED_NEXT = PHASE_ID

PLANNING_REQUIRED_ARTIFACTS: Tuple[str, ...] = (
    "summary.json",
    "verifier_report.json",
    "b0_arming_request_planning_policy_v1.json",
    "b0_arming_post_dryrun_review_input_review_v1.json",
    "b0_arming_request_identity_planning_v1.json",
    "b0_arming_request_scope_planning_v1.json",
    "b0_arming_request_precondition_gate_planning_v1.json",
    "b0_arming_request_forbidden_scope_planning_v1.json",
    "b0_arming_request_manifest_requirement_planning_v1.json",
    "b0_arming_request_rollback_requirement_planning_v1.json",
    "b0_arming_request_verifier_rerun_requirement_planning_v1.json",
    "b0_arming_request_post_migration_test_requirement_planning_v1.json",
    "b0_arming_request_abort_revoke_planning_v1.json",
    "b0_arming_request_non_claims_register_v1.json",
    "b0_arming_request_planning_readiness_decision_v1.json",
)


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _boundary_meta() -> Dict[str, Any]:
    return {
        "b0_arming_request_dryrun_only": True,
        "simulated": True,
        "selected_batch_id": "B0",
        "b0_only": True,
        "b1_b7_arming_deferred": True,
        "b0_arming_request_artifact_generated_now": False,
        "b0_arming_request_sent_now": False,
        "b0_arming_authorized_now": False,
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


def run_main_project_structure_migration_controlled_batch_execution_b0_arming_request_dryrun_v1(
    *,
    b0_arming_request_planning_root: str,
) -> Dict[str, Any]:
    plan = _load_planning_root(b0_arming_request_planning_root)
    blockers: List[str] = []
    if not plan["loaded"]:
        blockers.append(f"planning input incomplete: {plan['missing']}")

    sm = (plan["artifacts"].get("summary.json") or {}) if plan["artifacts"] else {}
    vr = (plan["artifacts"].get("verifier_report.json") or {}) if plan["artifacts"] else {}

    source_path_mode = "workspace_fallback" if _is_workspace_fallback(plan["root"]) else "repo_eval_out"
    standard_pending = source_path_mode == "workspace_fallback"
    meta = {**_boundary_meta(), "source_path_mode": source_path_mode, "standard_eval_out_write_pending_on_local_repro": standard_pending}

    if vr.get("verifier") != "GO" or vr.get("passed") is not True:
        blockers.append("planning verifier must be GO")
    if sm.get("phase") != PLANNING_REQUIRED_PHASE:
        blockers.append("planning phase mismatch")
    if sm.get("final_decision") != PLANNING_REQUIRED_FINAL:
        blockers.append("planning final_decision mismatch")
    if sm.get("recommended_next_phase") != PLANNING_REQUIRED_NEXT:
        blockers.append("planning recommended_next_phase must be this dryrun phase")
    if sm.get("b0_arming_request_planning_only") is not True:
        blockers.append("planning must be b0_arming_request_planning_only")
    if sm.get("selected_batch_id") != "B0" or sm.get("b0_only") is not True or sm.get("b1_b7_arming_deferred") is not True:
        blockers.append("planning must be b0-only with b1-b7 deferred")
    if sm.get("boundary_ok") is not True:
        blockers.append("planning boundary_ok must be true")

    for f in (
        "b0_arming_request_artifact_generated_now",
        "b0_arming_request_sent_now",
        "b0_arming_authorized_now",
        "b0_armed_now",
        "execution_window_opened_now",
        "verifier_rerun_executed_now",
        "rollback_rehearsal_executed_now",
        "post_migration_tests_executed_now",
        "file_operation_executed_now",
    ):
        if sm.get(f) is not False:
            blockers.append(f"planning boundary must be false: {f}")

    # Consumption checks for each planning object
    identity = plan["artifacts"].get("b0_arming_request_identity_planning_v1.json") or {}
    scope = plan["artifacts"].get("b0_arming_request_scope_planning_v1.json") or {}
    gates = plan["artifacts"].get("b0_arming_request_precondition_gate_planning_v1.json") or {}
    forbidden = plan["artifacts"].get("b0_arming_request_forbidden_scope_planning_v1.json") or {}
    manifest = plan["artifacts"].get("b0_arming_request_manifest_requirement_planning_v1.json") or {}
    rollback = plan["artifacts"].get("b0_arming_request_rollback_requirement_planning_v1.json") or {}
    rerun = plan["artifacts"].get("b0_arming_request_verifier_rerun_requirement_planning_v1.json") or {}
    tests = plan["artifacts"].get("b0_arming_request_post_migration_test_requirement_planning_v1.json") or {}
    abort_revoke = plan["artifacts"].get("b0_arming_request_abort_revoke_planning_v1.json") or {}

    # identity: must not generate/send request
    identity_pass = identity.get("batch_id") == "B0" and identity.get("request_sent_now") is False and identity.get("request_artifact_generated_now") is False

    # scope: no B1-B7 and no forbidden tokens
    scope_paths = scope.get("requested_scope_candidate") or []
    bad_tokens = ("capabilities/", "tools/", "_eval_out", "protected", "hr", "dnae", "configs", "scripts", "tests")
    scope_pass = (
        scope.get("batch_id") == "B0"
        and scope.get("b1_b7_included") is False
        and all(isinstance(p, str) and not any(t in p.lower() for t in bad_tokens) for p in scope_paths)
    )

    # gates: consumable but no authorization release
    gates_pass = gates.get("batch_id") == "B0" and isinstance(gates.get("required_precondition_gates"), list) and sm.get("b0_arming_authorized_now") is False

    # forbidden: must include protected/hr/dnae/eval_out block
    forb_paths = " ".join([str(x) for x in (forbidden.get("forbidden_paths_and_domains") or [])]).lower()
    forbidden_pass = (
        forbidden.get("batch_id") == "B0"
        and "protected" in forb_paths
        and "hr" in forb_paths
        and "dnae" in forb_paths
        and "_eval_out" in forb_paths
    )

    # manifest: consumable but no real generation/execution
    manifest_pass = manifest.get("batch_id") == "B0" and manifest.get("manifest_execution_now") is False
    rollback_pass = rollback.get("batch_id") == "B0" and rollback.get("rollback_rehearsal_executed_now") is False
    rerun_pass = rerun.get("batch_id") == "B0" and rerun.get("verifier_rerun_executed_now") is False
    tests_pass = tests.get("batch_id") == "B0" and tests.get("post_migration_tests_executed_now") is False
    abort_pass = abort_revoke.get("batch_id") == "B0" and abort_revoke.get("request_sent_now") is False and abort_revoke.get("authorized_now") is False

    if not (identity_pass and scope_pass and gates_pass and forbidden_pass and manifest_pass and rollback_pass and rerun_pass and tests_pass and abort_pass):
        blockers.append("one or more request planning objects not consumable")

    # Non-claims: emit required set for dryrun
    required_non_claims = [
        "B0 Arming Request DryRun GO ≠ request artifact generated",
        "request artifact generated in future ≠ request sent",
        "request sent in future ≠ arming authorized",
        "arming authorized in future ≠ B0 armed",
        "B0 armed in future ≠ B0 executed",
        "B0 execution in future ≠ B1–B7 allowed",
        "manifest requirement pass ≠ manifest generated",
        "verifier rerun requirement pass ≠ verifier rerun executed",
        "rollback requirement pass ≠ rollback rehearsal executed",
        "post-migration test requirement pass ≠ tests executed",
        "workspace_fallback GO ≠ standard _eval_out already written",
    ]
    planning_nc = plan["artifacts"].get("b0_arming_request_non_claims_register_v1.json") or {}
    planning_nc_texts = [str(r.get("text", "")) for r in (planning_nc.get("rows") or [])]

    boundary_ok = not blockers

    policy = _row(
        phase_id=PHASE_ID,
        dryrun_scope=DRYRUN_SCOPE,
        source_path_mode=source_path_mode,
        standard_eval_out_write_pending_on_local_repro=standard_pending,
    )

    input_review = {
        "planning_root": str(plan["root"]) if plan["root"] else None,
        "planning_loaded": plan["loaded"],
        "missing": plan["missing"],
        "planning_summary": {"phase": sm.get("phase"), "final_decision": sm.get("final_decision"), "recommended_next_phase": sm.get("recommended_next_phase")},
        "planning_verifier": {"verifier": vr.get("verifier"), "passed": vr.get("passed"), "check_count": vr.get("check_count")},
        "source_path_mode": source_path_mode,
        "standard_eval_out_write_pending_on_local_repro": standard_pending,
        "all_pass": boundary_ok,
        "blockers": blockers,
        **meta,
    }

    def _pack(name: str, passed: bool, detail: Any = None) -> Dict[str, Any]:
        return {"rows": [_row(check_id=name, simulated_consumption="pass" if passed else "fail", dryrun_pass=passed, detail=detail)], "row_count": 1, "all_pass": passed, **meta}

    identity_dryrun = _pack("identity", identity_pass)
    scope_dryrun = _pack("scope", scope_pass, {"paths": scope_paths})
    gates_dryrun = _pack("precondition_gates", gates_pass)
    forbidden_dryrun = _pack("forbidden_scope", forbidden_pass)
    manifest_dryrun = _pack("manifest_requirement", manifest_pass)
    rollback_dryrun = _pack("rollback_requirement", rollback_pass)
    rerun_dryrun = _pack("verifier_rerun_requirement", rerun_pass)
    tests_dryrun = _pack("post_migration_test_requirement", tests_pass)
    abort_dryrun = _pack("abort_revoke", abort_pass)

    non_claims_dryrun = {
        "rows": [
            _row(
                non_claim_id=f"NC_B0_REQ_DR_{i+1:02d}",
                text=t,
                non_claims_consumed_from_planning=True,
                planning_non_claims_text_sample=planning_nc_texts[:5],
                dryrun_pass=True,
            )
            for i, t in enumerate(required_non_claims)
        ],
        "row_count": len(required_non_claims),
        "all_pass": True,
        **meta,
    }

    readiness = {
        "final_decision": FINAL_DECISION if boundary_ok else "MAIN_PROJECT_STRUCTURE_MIGRATION_CONTROLLED_BATCH_EXECUTION_B0_ARMING_REQUEST_DRYRUN_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "ready_for_post_dryrun_review": boundary_ok,
        "selected_batch_id": "B0",
        **meta,
    }

    summary = {
        "phase": PHASE_ID,
        "dryrun_scope": DRYRUN_SCOPE,
        "b0_arming_request_dryrun_only": True,
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
        "identity_dryrun_pass": identity_dryrun.get("all_pass") is True,
        "scope_dryrun_pass": scope_dryrun.get("all_pass") is True,
        "gates_dryrun_pass": gates_dryrun.get("all_pass") is True,
        "forbidden_scope_dryrun_pass": forbidden_dryrun.get("all_pass") is True,
        "manifest_dryrun_pass": manifest_dryrun.get("all_pass") is True,
        "rollback_dryrun_pass": rollback_dryrun.get("all_pass") is True,
        "rerun_dryrun_pass": rerun_dryrun.get("all_pass") is True,
        "post_tests_dryrun_pass": tests_dryrun.get("all_pass") is True,
        "abort_revoke_dryrun_pass": abort_dryrun.get("all_pass") is True,
        "non_claims_dryrun_pass": non_claims_dryrun.get("all_pass") is True,
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "final_decision": FINAL_DECISION if boundary_ok else "MAIN_PROJECT_STRUCTURE_MIGRATION_CONTROLLED_BATCH_EXECUTION_B0_ARMING_REQUEST_DRYRUN_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        **meta,
    }

    return {
        "summary": summary,
        "b0_arming_request_dryrun_policy": policy,
        "b0_arming_request_planning_input_review": input_review,
        "b0_arming_request_identity_dryrun": identity_dryrun,
        "b0_arming_request_scope_dryrun": scope_dryrun,
        "b0_arming_request_precondition_gate_dryrun": gates_dryrun,
        "b0_arming_request_forbidden_scope_dryrun": forbidden_dryrun,
        "b0_arming_request_manifest_requirement_dryrun": manifest_dryrun,
        "b0_arming_request_rollback_requirement_dryrun": rollback_dryrun,
        "b0_arming_request_verifier_rerun_requirement_dryrun": rerun_dryrun,
        "b0_arming_request_post_migration_test_requirement_dryrun": tests_dryrun,
        "b0_arming_request_abort_revoke_dryrun": abort_dryrun,
        "b0_arming_request_non_claims_dryrun": non_claims_dryrun,
        "b0_arming_request_dryrun_readiness_decision": readiness,
    }

