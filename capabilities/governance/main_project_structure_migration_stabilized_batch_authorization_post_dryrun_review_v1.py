# -*- coding: utf-8 -*-
"""Main Project Structure Migration Stabilized Batch Authorization Post-DryRun Review v1.

Review-only: audit Batch Authorization DryRun completeness and boundary credibility.
No request/grant/arming/execution, no verifier rerun, no rollback rehearsal, no file operations.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.main_project_structure_migration_stabilized_batch_authorization_dryrun_v1 import (
    FINAL_DECISION as DRYRUN_FINAL,
    PHASE_ID as DRYRUN_PHASE,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID

PHASE_ID = "Phase-Main-Project-Structure-Migration-Stabilized-Batch-Authorization-Post-DryRun-Review-v1-001"
REVIEW_SCOPE = "main_project_structure_migration_stabilized_batch_authorization_post_dryrun_review_only"
SOURCE_CHAIN = "main_project_structure_migration_stabilized_batch_authorization_post_dryrun_review_v1"

FINAL_DECISION = (
    "MAIN_PROJECT_STRUCTURE_MIGRATION_STABILIZED_BATCH_AUTHORIZATION_POST_DRYRUN_REVIEW_READY_FOR_CONTROLLED_BATCH_EXECUTION_AUTHORIZATION_PLANNING"
)
NEXT_PHASE = "Phase-Main-Project-Structure-Migration-Controlled-Batch-Execution-Authorization-Planning-v1-001"

DRYRUN_REQUIRED_PHASE = DRYRUN_PHASE
DRYRUN_REQUIRED_FINAL = DRYRUN_FINAL
DRYRUN_REQUIRED_NEXT = PHASE_ID

DRYRUN_REQUIRED_ARTIFACTS: Tuple[str, ...] = (
    "summary.json",
    "verifier_report.json",
    "stabilized_batch_authorization_dryrun_policy_v1.json",
    "batch_authorization_planning_input_review_v1.json",
    "b0_b7_authorization_scope_dryrun_v1.json",
    "batch_authorization_request_schema_dryrun_v1.json",
    "batch_authorization_grant_schema_dryrun_v1.json",
    "batch_pre_authorization_gate_dryrun_v1.json",
    "batch_execution_window_dryrun_v1.json",
    "batch_verifier_rerun_authorization_dryrun_v1.json",
    "batch_rollback_authorization_dryrun_v1.json",
    "batch_file_operation_permission_boundary_dryrun_v1.json",
    "batch_protected_eval_out_guard_dryrun_v1.json",
    "batch_authorization_non_claims_dryrun_v1.json",
    "stabilized_batch_authorization_dryrun_readiness_decision_v1.json",
)


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _boundary_meta() -> Dict[str, Any]:
    return {
        "batch_authorization_post_dryrun_review_only": True,
        "review_only": True,
        "source_path_mode": "repo_eval_out",
        "standard_eval_out_write_pending_on_local_repro": False,
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
        "eval_out_modified_now": False,
        "protected_asset_modified_now": False,
        "hr_modified_now": False,
        "dnae_modified_now": False,
        "file_operation_executed_now": False,
        "rollback_rehearsal_execution_allowed": False,
        "real_migration_execution_allowed": False,
        "real_rehearsal_execution_allowed": False,
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
    return {**kwargs, **_boundary_meta(), "planned_now": True, "executed_now": False}


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def _load_dryrun_root(path_str: Optional[str]) -> Dict[str, Any]:
    root = Path(path_str).expanduser().resolve() if path_str else None
    artifacts: Dict[str, Any] = {}
    missing: List[str] = []
    if root:
        for name in DRYRUN_REQUIRED_ARTIFACTS:
            payload = _try_read_json(root / name)
            if payload is None:
                missing.append(name)
            else:
                artifacts[name] = payload
    loaded = bool(root) and not missing and bool(artifacts.get("summary.json")) and bool(artifacts.get("verifier_report.json"))
    return {"root": root, "loaded": loaded, "artifacts": artifacts, "missing": missing}


def _is_workspace_fallback(root: Optional[Path]) -> bool:
    return bool(root) and "Luna-Workspace-Min" in str(root)


def run_main_project_structure_migration_stabilized_batch_authorization_post_dryrun_review_v1(
    *,
    stabilized_batch_authorization_dryrun_root: str,
) -> Dict[str, Any]:
    dry = _load_dryrun_root(stabilized_batch_authorization_dryrun_root)
    blockers: List[str] = []
    if not dry["loaded"]:
        blockers.append(f"dryrun input incomplete: {dry['missing']}")

    dsm = (dry["artifacts"].get("summary.json") or {}) if dry["artifacts"] else {}
    dvr = (dry["artifacts"].get("verifier_report.json") or {}) if dry["artifacts"] else {}

    source_path_mode = "workspace_fallback" if _is_workspace_fallback(dry["root"]) else "repo_eval_out"
    standard_pending = source_path_mode == "workspace_fallback"

    if dvr.get("verifier") != "GO" or dvr.get("passed") is not True:
        blockers.append("dryrun verifier must be GO")
    if dsm.get("boundary_ok") is not True:
        blockers.append("dryrun boundary_ok must be true")
    if dsm.get("final_decision") != DRYRUN_REQUIRED_FINAL:
        blockers.append("dryrun final_decision mismatch")
    if dsm.get("recommended_next_phase") != DRYRUN_REQUIRED_NEXT:
        blockers.append("dryrun recommended_next_phase must point to this review phase")
    if dsm.get("batch_authorization_dryrun_only") is not True or dsm.get("simulated") is not True:
        blockers.append("dryrun must be dryrun_only=true and simulated=true")

    for f in (
        "batch_authorization_request_sent_now",
        "batch_authorization_granted_now",
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
        if dsm.get(f) is not False:
            blockers.append(f"dryrun boundary must be false: {f}")

    input_rows = [
        _row(check_id="dryrun.phase", expected=DRYRUN_REQUIRED_PHASE, observed=dsm.get("phase"), review_pass=dsm.get("phase") == DRYRUN_REQUIRED_PHASE),
        _row(check_id="dryrun.verifier_go", expected="GO", observed=dvr.get("verifier"), review_pass=dvr.get("verifier") == "GO"),
        _row(check_id="dryrun.final_decision", expected=DRYRUN_REQUIRED_FINAL, observed=dsm.get("final_decision"), review_pass=dsm.get("final_decision") == DRYRUN_REQUIRED_FINAL),
        _row(check_id="dryrun.next_phase", expected=DRYRUN_REQUIRED_NEXT, observed=dsm.get("recommended_next_phase"), review_pass=dsm.get("recommended_next_phase") == DRYRUN_REQUIRED_NEXT),
        _row(check_id="dryrun.source_path_mode", expected=source_path_mode, observed=dsm.get("source_path_mode"), review_pass=True),
    ]
    batch_authorization_dryrun_input_review = {
        "dryrun_root": str(dry["root"]) if dry["root"] else None,
        "loaded": dry["loaded"],
        "missing": dry["missing"],
        "source_path_mode": source_path_mode,
        "standard_eval_out_write_pending_on_local_repro": standard_pending,
        "rows": input_rows,
        "row_count": len(input_rows),
        "all_pass": all(r.get("review_pass") for r in input_rows) and not blockers,
        "blockers": blockers,
        **{**_boundary_meta(), "source_path_mode": source_path_mode, "standard_eval_out_write_pending_on_local_repro": standard_pending},
    }

    def _load(name: str) -> Dict[str, Any]:
        return dry["artifacts"].get(name) or {}

    # each table must be present and pass
    tables = {
        "b0_b7_authorization_scope_review": _load("b0_b7_authorization_scope_dryrun_v1.json"),
        "batch_authorization_request_non_sent_review": _load("batch_authorization_request_schema_dryrun_v1.json"),
        "batch_authorization_grant_non_issued_review": _load("batch_authorization_grant_schema_dryrun_v1.json"),
        "batch_execution_window_non_open_review": _load("batch_execution_window_dryrun_v1.json"),
        "batch_verifier_rerun_non_execution_review": _load("batch_verifier_rerun_authorization_dryrun_v1.json"),
        "batch_rollback_non_execution_review": _load("batch_rollback_authorization_dryrun_v1.json"),
        "batch_file_operation_non_execution_review": _load("batch_file_operation_permission_boundary_dryrun_v1.json"),
        "batch_protected_eval_out_guard_review": _load("batch_protected_eval_out_guard_dryrun_v1.json"),
        "batch_authorization_non_claims_review": _load("batch_authorization_non_claims_dryrun_v1.json"),
    }

    # wrap to review artifacts with explicit pass checks
    def _review_table(name: str, payload: Dict[str, Any], pass_key: str = "all_pass") -> Dict[str, Any]:
        observed = payload.get(pass_key)
        passed = observed is True or (payload.get("dryrun_pass") is True)
        return {
            "table_name": name,
            "observed_pass": observed,
            "review_pass": passed,
            "rows": [_row(table=name, **{"row_preview": (payload.get("rows") or [])[:1]})],
            "row_count": int(payload.get("row_count", 0) or 0),
            "all_pass": passed,
            **{**_boundary_meta(), "source_path_mode": source_path_mode, "standard_eval_out_write_pending_on_local_repro": standard_pending},
        }

    b0_b7_authorization_scope_review = _review_table("b0_b7_authorization_scope_review_v1", tables["b0_b7_authorization_scope_review"])
    batch_authorization_request_non_sent_review = _review_table("batch_authorization_request_non_sent_review_v1", tables["batch_authorization_request_non_sent_review"], pass_key="dryrun_pass")
    batch_authorization_grant_non_issued_review = _review_table("batch_authorization_grant_non_issued_review_v1", tables["batch_authorization_grant_non_issued_review"], pass_key="dryrun_pass")
    batch_execution_window_non_open_review = _review_table("batch_execution_window_non_open_review_v1", tables["batch_execution_window_non_open_review"])
    batch_verifier_rerun_non_execution_review = _review_table("batch_verifier_rerun_non_execution_review_v1", tables["batch_verifier_rerun_non_execution_review"])
    batch_rollback_non_execution_review = _review_table("batch_rollback_non_execution_review_v1", tables["batch_rollback_non_execution_review"])
    batch_file_operation_non_execution_review = _review_table("batch_file_operation_non_execution_review_v1", tables["batch_file_operation_non_execution_review"])
    batch_protected_eval_out_guard_review = _review_table("batch_protected_eval_out_guard_review_v1", tables["batch_protected_eval_out_guard_review"])
    batch_authorization_non_claims_review = _review_table("batch_authorization_non_claims_review_v1", tables["batch_authorization_non_claims_review"])

    # explicit reviews for arming + execution must remain false
    batch_arming_non_execution_review = {
        "rows": [
            _row(check_id="batch_armed_now=false", expected=False, observed=dsm.get("batch_armed_now"), review_pass=dsm.get("batch_armed_now") is False),
            _row(check_id="batch_execution_started_now=false", expected=False, observed=dsm.get("batch_execution_started_now"), review_pass=dsm.get("batch_execution_started_now") is False),
        ],
        "row_count": 2,
        "all_pass": True,
        **{**_boundary_meta(), "source_path_mode": source_path_mode, "standard_eval_out_write_pending_on_local_repro": standard_pending},
    }
    batch_arming_non_execution_review["all_pass"] = all(r.get("review_pass") for r in batch_arming_non_execution_review["rows"])

    review_ok = (
        batch_authorization_dryrun_input_review["all_pass"]
        and b0_b7_authorization_scope_review["all_pass"]
        and batch_authorization_request_non_sent_review["all_pass"]
        and batch_authorization_grant_non_issued_review["all_pass"]
        and batch_execution_window_non_open_review["all_pass"]
        and batch_verifier_rerun_non_execution_review["all_pass"]
        and batch_rollback_non_execution_review["all_pass"]
        and batch_file_operation_non_execution_review["all_pass"]
        and batch_protected_eval_out_guard_review["all_pass"]
        and batch_authorization_non_claims_review["all_pass"]
        and batch_arming_non_execution_review["all_pass"]
        and not blockers
    )

    boundary_ok = bool(review_ok)

    stabilized_batch_authorization_post_dryrun_review_policy = _row(
        phase_id=PHASE_ID,
        review_scope=REVIEW_SCOPE,
        dryrun_required_phase=DRYRUN_REQUIRED_PHASE,
        dryrun_required_final_decision=DRYRUN_REQUIRED_FINAL,
        dryrun_required_next_phase=DRYRUN_REQUIRED_NEXT,
        required_artifacts=list(DRYRUN_REQUIRED_ARTIFACTS),
        source_path_mode=source_path_mode,
        standard_eval_out_write_pending_on_local_repro=standard_pending,
    )

    stabilized_batch_authorization_post_dryrun_review_readiness_decision = {
        "final_decision": FINAL_DECISION if boundary_ok else "MAIN_PROJECT_STRUCTURE_MIGRATION_STABILIZED_BATCH_AUTHORIZATION_POST_DRYRUN_REVIEW_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "ready_for_controlled_batch_execution_authorization_planning": boundary_ok,
        "review_completed": boundary_ok,
        "source_path_mode": source_path_mode,
        "standard_eval_out_write_pending_on_local_repro": standard_pending,
        **{**_boundary_meta(), "source_path_mode": source_path_mode, "standard_eval_out_write_pending_on_local_repro": standard_pending},
    }

    summary = {
        "phase": PHASE_ID,
        "review_scope": REVIEW_SCOPE,
        "dryrun_input_loaded": dry["loaded"],
        "dryrun_source_path_mode": source_path_mode,
        "standard_eval_out_write_pending_on_local_repro": standard_pending,
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "final_decision": FINAL_DECISION if boundary_ok else "MAIN_PROJECT_STRUCTURE_MIGRATION_STABILIZED_BATCH_AUTHORIZATION_POST_DRYRUN_REVIEW_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        **{**_boundary_meta(), "source_path_mode": source_path_mode, "standard_eval_out_write_pending_on_local_repro": standard_pending},
    }

    return {
        "summary": summary,
        "stabilized_batch_authorization_post_dryrun_review_policy": stabilized_batch_authorization_post_dryrun_review_policy,
        "batch_authorization_dryrun_input_review": batch_authorization_dryrun_input_review,
        "b0_b7_authorization_scope_review": b0_b7_authorization_scope_review,
        "batch_authorization_request_non_sent_review": batch_authorization_request_non_sent_review,
        "batch_authorization_grant_non_issued_review": batch_authorization_grant_non_issued_review,
        "batch_arming_non_execution_review": batch_arming_non_execution_review,
        "batch_execution_window_non_open_review": batch_execution_window_non_open_review,
        "batch_verifier_rerun_non_execution_review": batch_verifier_rerun_non_execution_review,
        "batch_rollback_non_execution_review": batch_rollback_non_execution_review,
        "batch_file_operation_non_execution_review": batch_file_operation_non_execution_review,
        "batch_protected_eval_out_guard_review": batch_protected_eval_out_guard_review,
        "batch_authorization_non_claims_review": batch_authorization_non_claims_review,
        "stabilized_batch_authorization_post_dryrun_review_readiness_decision": stabilized_batch_authorization_post_dryrun_review_readiness_decision,
    }

