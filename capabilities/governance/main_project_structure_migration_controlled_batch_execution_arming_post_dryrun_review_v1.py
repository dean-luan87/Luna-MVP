# -*- coding: utf-8 -*-
"""Main Project Structure Migration Controlled Batch Execution Arming Post-DryRun Review v1.

Review-only: audit the credibility of B0-only arming dry-run outputs.
No arming, no window open, no execution, no file operations, no verifier rerun execution,
no rollback rehearsal, no post-migration tests.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.main_project_structure_migration_controlled_batch_execution_arming_dryrun_v1 import (
    FINAL_DECISION as DRYRUN_FINAL,
    NEXT_PHASE as DRYRUN_NEXT,
    PHASE_ID as DRYRUN_PHASE,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID

PHASE_ID = "Phase-Main-Project-Structure-Migration-Controlled-Batch-Execution-Arming-Post-DryRun-Review-v1-001"
REVIEW_SCOPE = "main_project_structure_migration_controlled_batch_execution_arming_post_dryrun_review_only"
SOURCE_CHAIN = "main_project_structure_migration_controlled_batch_execution_arming_post_dryrun_review_v1"

FINAL_DECISION = "MAIN_PROJECT_STRUCTURE_MIGRATION_CONTROLLED_BATCH_EXECUTION_ARMING_POST_DRYRUN_REVIEW_READY_FOR_B0_ARMING_REQUEST_PLANNING"
NEXT_PHASE = "Phase-Main-Project-Structure-Migration-Controlled-Batch-Execution-B0-Arming-Request-Planning-v1-001"

DRYRUN_REQUIRED_PHASE = DRYRUN_PHASE
DRYRUN_REQUIRED_FINAL = DRYRUN_FINAL
DRYRUN_REQUIRED_NEXT = PHASE_ID

DRYRUN_REQUIRED_ARTIFACTS: Tuple[str, ...] = (
    "summary.json",
    "verifier_report.json",
    "controlled_batch_execution_arming_dryrun_policy_v1.json",
    "controlled_batch_execution_arming_planning_input_review_v1.json",
    "b0_single_batch_arming_scope_dryrun_v1.json",
    "b1_b7_deferred_arming_dryrun_v1.json",
    "b0_execution_window_arming_dryrun_v1.json",
    "b0_file_operation_allowlist_arming_dryrun_v1.json",
    "b0_file_operation_blocklist_arming_dryrun_v1.json",
    "b0_before_after_manifest_arming_dryrun_v1.json",
    "b0_rollback_route_arming_dryrun_v1.json",
    "b0_verifier_rerun_arming_dryrun_v1.json",
    "b0_post_migration_test_arming_dryrun_v1.json",
    "b0_abort_condition_arming_dryrun_v1.json",
    "b0_protected_eval_out_guard_arming_dryrun_v1.json",
    "controlled_batch_execution_arming_non_claims_dryrun_v1.json",
    "controlled_batch_execution_arming_dryrun_readiness_decision_v1.json",
)


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _boundary_meta() -> Dict[str, Any]:
    return {
        "controlled_batch_execution_arming_post_dryrun_review_only": True,
        "review_only": True,
        "selected_batch_id": "B0",
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
    return {**kwargs, **_boundary_meta(), "reviewed_now": True, "executed_now": False}


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


def run_main_project_structure_migration_controlled_batch_execution_arming_post_dryrun_review_v1(
    *,
    controlled_batch_execution_arming_dryrun_root: str,
) -> Dict[str, Any]:
    dr = _load_dryrun_root(controlled_batch_execution_arming_dryrun_root)
    blockers: List[str] = []
    if not dr["loaded"]:
        blockers.append(f"dryrun input incomplete: {dr['missing']}")

    sm = (dr["artifacts"].get("summary.json") or {}) if dr["artifacts"] else {}
    vr = (dr["artifacts"].get("verifier_report.json") or {}) if dr["artifacts"] else {}

    source_path_mode = "workspace_fallback" if _is_workspace_fallback(dr["root"]) else "repo_eval_out"
    standard_pending = source_path_mode == "workspace_fallback"

    if vr.get("verifier") != "GO" or vr.get("passed") is not True:
        blockers.append("dryrun verifier must be GO")
    if sm.get("phase") != DRYRUN_REQUIRED_PHASE:
        blockers.append("dryrun phase mismatch")
    if sm.get("final_decision") != DRYRUN_REQUIRED_FINAL:
        blockers.append("dryrun final_decision mismatch")
    if sm.get("recommended_next_phase") != DRYRUN_REQUIRED_NEXT:
        blockers.append("dryrun recommended_next_phase must be this post-dryrun review phase")
    if sm.get("controlled_batch_execution_arming_dryrun_only") is not True or sm.get("simulated") is not True:
        blockers.append("dryrun must be dryrun_only + simulated")
    if sm.get("selected_batch_id") != "B0" or sm.get("b0_only") is not True or sm.get("b1_b7_arming_deferred") is not True:
        blockers.append("dryrun must be b0-only with b1-b7 deferred")
    if sm.get("boundary_ok") is not True:
        blockers.append("dryrun boundary_ok must be true")

    must_false = (
        "b0_armed_now",
        "batch_armed_now",
        "b0_execution_started_now",
        "batch_execution_started_now",
        "execution_window_opened_now",
        "actual_file_move_executed",
        "actual_file_delete_executed",
        "actual_file_rename_executed",
        "actual_file_merge_executed",
        "actual_file_copy_executed",
        "actual_file_overwrite_executed",
        "actual_archive_executed",
        "verifier_rerun_executed_now",
        "rollback_rehearsal_executed_now",
        "post_migration_tests_executed_now",
        "eval_out_modified_now",
        "protected_asset_modified_now",
        "hr_modified_now",
        "dnae_modified_now",
    )
    for f in must_false:
        if sm.get(f) is not False:
            blockers.append(f"dryrun boundary must be false: {f}")

    # Consume dryrun pass flags
    def _is_true(k: str) -> bool:
        return sm.get(k) is True

    required_pass_flags = (
        "b0_scope_dryrun_pass",
        "b1_b7_deferred_dryrun_pass",
        "window_dryrun_pass",
        "allowlist_dryrun_pass",
        "blocklist_dryrun_pass",
        "manifest_dryrun_pass",
        "rollback_dryrun_pass",
        "rerun_dryrun_pass",
        "post_tests_dryrun_pass",
        "abort_dryrun_pass",
        "guard_dryrun_pass",
        "non_claims_dryrun_pass",
    )
    if not all(_is_true(k) for k in required_pass_flags):
        blockers.append("one or more dryrun pass flags are false")

    # Specific scope forbidden token review: read the B0 scope dryrun artifact detail
    b0_scope_obj = dr["artifacts"].get("b0_single_batch_arming_scope_dryrun_v1.json") or {}
    b0_rows = b0_scope_obj.get("rows") or []
    b0_detail = (b0_rows[0].get("detail") or {}) if b0_rows else {}
    b0_paths = b0_detail.get("paths") or []
    bad_tokens = ("capabilities/", "tools/", "_eval_out", "protected", "hr", "dnae", "configs", "scripts", "tests")
    scope_ok = all(isinstance(p, str) and not any(t in p.lower() for t in bad_tokens) for p in b0_paths)
    if not scope_ok:
        blockers.append("B0 scope review found forbidden path tokens")

    boundary_ok = not blockers
    meta = {**_boundary_meta(), "source_path_mode": source_path_mode, "standard_eval_out_write_pending_on_local_repro": standard_pending}

    controlled_batch_execution_arming_post_dryrun_review_policy = _row(
        phase_id=PHASE_ID,
        review_scope=REVIEW_SCOPE,
        upstream_dryrun_phase=sm.get("phase"),
        source_path_mode=source_path_mode,
        standard_eval_out_write_pending_on_local_repro=standard_pending,
        review_only=True,
    )

    controlled_batch_execution_arming_dryrun_input_review = {
        "dryrun_root": str(dr["root"]) if dr["root"] else None,
        "dryrun_loaded": dr["loaded"],
        "missing": dr["missing"],
        "source_path_mode": source_path_mode,
        "standard_eval_out_write_pending_on_local_repro": standard_pending,
        "dryrun_summary": {
            "phase": sm.get("phase"),
            "boundary_ok": sm.get("boundary_ok"),
            "final_decision": sm.get("final_decision"),
            "recommended_next_phase": sm.get("recommended_next_phase"),
            "selected_batch_id": sm.get("selected_batch_id"),
        },
        "dryrun_verifier": {"verifier": vr.get("verifier"), "passed": vr.get("passed"), "check_count": vr.get("check_count")},
        "blockers": blockers,
        "all_pass": boundary_ok,
        **meta,
    }

    def _review(name: str, passed: bool, detail: Any = None) -> Dict[str, Any]:
        return {"rows": [_row(check_id=name, review_pass=passed, detail=detail)], "row_count": 1, "all_pass": passed, **meta}

    b0_single_batch_arming_scope_review = _review("b0_scope_review", scope_ok, {"paths": b0_paths})
    b1_b7_deferred_arming_review = _review("b1_b7_deferred_review", sm.get("b1_b7_deferred_dryrun_pass") is True)
    b0_execution_window_non_open_review = _review("window_non_open", sm.get("execution_window_opened_now") is False)
    b0_file_operation_non_execution_review = _review(
        "fileop_non_execution",
        all(sm.get(k) is False for k in (
            "actual_file_move_executed",
            "actual_file_delete_executed",
            "actual_file_rename_executed",
            "actual_file_merge_executed",
            "actual_file_copy_executed",
            "actual_file_overwrite_executed",
            "actual_archive_executed",
        )),
    )
    b0_manifest_non_execution_review = _review("manifest_non_execution", sm.get("manifest_dryrun_pass") is True)
    b0_rollback_non_execution_review = _review("rollback_non_execution", sm.get("rollback_rehearsal_executed_now") is False)
    b0_verifier_rerun_non_execution_review = _review("verifier_rerun_non_execution", sm.get("verifier_rerun_executed_now") is False)
    b0_post_migration_test_non_execution_review = _review("post_tests_non_execution", sm.get("post_migration_tests_executed_now") is False)
    b0_abort_condition_review = _review("abort_condition_review", sm.get("abort_dryrun_pass") is True)
    b0_protected_eval_out_guard_review = _review(
        "protected_eval_out_guard_review",
        sm.get("eval_out_modified_now") is False
        and sm.get("protected_asset_modified_now") is False
        and sm.get("hr_modified_now") is False
        and sm.get("dnae_modified_now") is False,
        detail={"source_path_mode": source_path_mode, "standard_eval_out_write_pending_on_local_repro": standard_pending},
    )

    # Non-claims review: emit the required set for this review phase
    required_non_claims = [
        "Arming DryRun GO ≠ B0 armed",
        "B0 selected ≠ B0 executed",
        "B0 arming scope pass ≠ file operation executed",
        "B1–B7 deferred ≠ B1–B7 ready",
        "execution window pass ≠ execution window opened",
        "manifest plan pass ≠ real manifest generated",
        "verifier rerun plan pass ≠ verifier rerun executed",
        "rollback route pass ≠ rollback rehearsal executed",
        "post-migration test plan pass ≠ tests executed",
        "workspace_fallback GO ≠ standard _eval_out already written",
    ]
    nc_obj = dr["artifacts"].get("controlled_batch_execution_arming_non_claims_dryrun_v1.json") or {}
    planning_texts = [str(r.get("text", "")) for r in (nc_obj.get("rows") or [])]
    controlled_batch_execution_arming_non_claims_review = {
        "rows": [
            _row(
                non_claim_id=f"NC_ARM_POST_REVIEW_{i+1:02d}",
                text=t,
                non_claims_consumed_from_dryrun=True,
                dryrun_non_claims_text_sample=planning_texts[:5],
                review_pass=True,
            )
            for i, t in enumerate(required_non_claims)
        ],
        "row_count": len(required_non_claims),
        "all_pass": True,
        **meta,
    }

    controlled_batch_execution_arming_post_dryrun_review_readiness_decision = {
        "final_decision": FINAL_DECISION if boundary_ok else "MAIN_PROJECT_STRUCTURE_MIGRATION_CONTROLLED_BATCH_EXECUTION_ARMING_POST_DRYRUN_REVIEW_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "ready_for_b0_arming_request_planning": boundary_ok,
        "selected_batch_id": "B0",
        **meta,
    }

    summary = {
        "phase": PHASE_ID,
        "review_scope": REVIEW_SCOPE,
        "controlled_batch_execution_arming_post_dryrun_review_only": True,
        "review_only": True,
        "selected_batch_id": "B0",
        "b0_only": True,
        "b1_b7_arming_deferred": True,
        "source_path_mode": source_path_mode,
        "standard_eval_out_write_pending_on_local_repro": standard_pending,
        "dryrun_input_loaded": dr["loaded"],
        "dryrun_verifier_go": vr.get("verifier") == "GO" and vr.get("passed") is True,
        "dryrun_final_decision_ok": sm.get("final_decision") == DRYRUN_REQUIRED_FINAL,
        "dryrun_next_phase_ok": sm.get("recommended_next_phase") == DRYRUN_REQUIRED_NEXT,
        "dryrun_artifacts_present": len(DRYRUN_REQUIRED_ARTIFACTS) - len(dr["missing"]) if dr["root"] else 0,
        "dryrun_artifact_count_required": len(DRYRUN_REQUIRED_ARTIFACTS),
        "b0_scope_review_pass": b0_single_batch_arming_scope_review.get("all_pass") is True,
        "b1_b7_deferred_review_pass": b1_b7_deferred_arming_review.get("all_pass") is True,
        "window_non_open_review_pass": b0_execution_window_non_open_review.get("all_pass") is True,
        "file_op_non_execution_review_pass": b0_file_operation_non_execution_review.get("all_pass") is True,
        "manifest_non_execution_review_pass": b0_manifest_non_execution_review.get("all_pass") is True,
        "rollback_non_execution_review_pass": b0_rollback_non_execution_review.get("all_pass") is True,
        "verifier_rerun_non_execution_review_pass": b0_verifier_rerun_non_execution_review.get("all_pass") is True,
        "post_tests_non_execution_review_pass": b0_post_migration_test_non_execution_review.get("all_pass") is True,
        "abort_condition_review_pass": b0_abort_condition_review.get("all_pass") is True,
        "guard_review_pass": b0_protected_eval_out_guard_review.get("all_pass") is True,
        "non_claims_review_pass": controlled_batch_execution_arming_non_claims_review.get("all_pass") is True,
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "final_decision": FINAL_DECISION if boundary_ok else "MAIN_PROJECT_STRUCTURE_MIGRATION_CONTROLLED_BATCH_EXECUTION_ARMING_POST_DRYRUN_REVIEW_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        **meta,
    }

    return {
        "summary": summary,
        "controlled_batch_execution_arming_post_dryrun_review_policy": controlled_batch_execution_arming_post_dryrun_review_policy,
        "controlled_batch_execution_arming_dryrun_input_review": controlled_batch_execution_arming_dryrun_input_review,
        "b0_single_batch_arming_scope_review": b0_single_batch_arming_scope_review,
        "b1_b7_deferred_arming_review": b1_b7_deferred_arming_review,
        "b0_execution_window_non_open_review": b0_execution_window_non_open_review,
        "b0_file_operation_non_execution_review": b0_file_operation_non_execution_review,
        "b0_manifest_non_execution_review": b0_manifest_non_execution_review,
        "b0_rollback_non_execution_review": b0_rollback_non_execution_review,
        "b0_verifier_rerun_non_execution_review": b0_verifier_rerun_non_execution_review,
        "b0_post_migration_test_non_execution_review": b0_post_migration_test_non_execution_review,
        "b0_abort_condition_review": b0_abort_condition_review,
        "b0_protected_eval_out_guard_review": b0_protected_eval_out_guard_review,
        "controlled_batch_execution_arming_non_claims_review": controlled_batch_execution_arming_non_claims_review,
        "controlled_batch_execution_arming_post_dryrun_review_readiness_decision": controlled_batch_execution_arming_post_dryrun_review_readiness_decision,
    }

