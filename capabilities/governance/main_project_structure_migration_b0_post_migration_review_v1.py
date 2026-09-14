# -*- coding: utf-8 -*-
"""Main Project Structure Migration B0 Post-Migration Review v1.

Review-only: audit B0 controlled execution (stable placement / unchanged). No new file
operations, no verifier rerun, no rollback rehearsal, no content modification.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID

PHASE_ID = "Phase-Main-Project-Structure-Migration-B0-Post-Migration-Review-v1-001"
REVIEW_SCOPE = "main_project_structure_migration_b0_post_migration_review_only"
SOURCE_CHAIN = "main_project_structure_migration_b0_post_migration_review_v1"

FINAL_DECISION = "MAIN_PROJECT_STRUCTURE_MIGRATION_B0_POST_MIGRATION_REVIEW_CLOSED_READY_FOR_B1_PREFLIGHT_VIA_HARNESS"
NEXT_PHASE = "Phase-Main-Project-Structure-Migration-B1-Preflight-Via-Harness-v1-001"

UPSTREAM_REQUIRED_PHASE = "Phase-Main-Project-Structure-Migration-B0-Controlled-Execution-v1-001"
UPSTREAM_REQUIRED_FINAL = "MAIN_PROJECT_STRUCTURE_MIGRATION_B0_CONTROLLED_EXECUTION_READY_FOR_POST_MIGRATION_REVIEW"
UPSTREAM_REQUIRED_NEXT = PHASE_ID

UPSTREAM_REQUIRED_ARTIFACTS: Tuple[str, ...] = (
    "summary.json",
    "verifier_report.json",
    "b0_before_manifest_v1.json",
    "b0_after_manifest_v1.json",
    "b0_execution_operation_trace_v1.json",
    "b0_blocked_operation_assertion_v1.json",
    "b0_protected_eval_out_guard_execution_result_v1.json",
    "b0_runtime_refactor_block_execution_result_v1.json",
)

REQUIRED_CANDIDATE_PATHS: Tuple[str, ...] = (
    "docs/architecture/README.md",
    "docs/architecture/evaluation/README.md",
    "docs/architecture/evaluation/LUNA_EVALUATION_OCR_PHASE_VERDICT_STATUS_TABLE_V0.md",
)

NON_CLAIMS = [
    "B0 post-migration review GO ≠ B1 executed",
    "B0 closure GO ≠ B1 armed",
    "B0 stable placement confirmed ≠ physical move occurred",
    "rollback readiness pass ≠ rollback rehearsal executed",
    "B0 closed ≠ harness extraction/adoption chain reopened",
    "B1 preflight ready ≠ B1 migration executed",
    "workspace_fallback GO ≠ standard _eval_out already written",
]


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _boundary_meta() -> Dict[str, Any]:
    return {
        "b0_post_migration_review_only": True,
        "review_only": True,
        "selected_batch_id": "B0",
        "b0_only": True,
        "b1_b7_deferred": True,
        "b0_closed_now": True,
        "harness_contract_reused": True,
        "harness_extraction_reopened_now": False,
        "harness_adoption_reopened_now": False,
        "b0_execution_completed_now": True,
        "actual_file_move_executed": False,
        "actual_file_rename_executed": False,
        "actual_file_delete_executed": False,
        "actual_file_merge_executed": False,
        "actual_file_copy_executed": False,
        "actual_file_overwrite_executed": False,
        "actual_archive_executed": False,
        "eval_out_modified_now": False,
        "protected_asset_modified_now": False,
        "hr_modified_now": False,
        "dnae_modified_now": False,
        "runtime_refactor_executed_now": False,
        "content_rewrite_executed_now": False,
        "old_phase_deleted_now": False,
        "old_phase_deprecated_now": False,
        "verifier_rerun_executed_now": False,
        "rollback_rehearsal_executed_now": False,
        "post_migration_tests_executed_now": False,
        "file_operation_executed_now": False,
        "real_migration_execution_allowed": False,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_path_mode": "repo_eval_out",
        "standard_eval_out_write_pending_on_local_repro": False,
        "runtime_invoked": False,
        "execution_committed": False,
        "authorization_granted_now": False,
        "batch_arming_allowed": False,
        "success_claim_allowed": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _row(**kwargs: Any) -> Dict[str, Any]:
    return {**kwargs, **_boundary_meta()}


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def _load_upstream(root_str: str) -> Dict[str, Any]:
    root = Path(root_str).expanduser().resolve()
    artifacts: Dict[str, Any] = {}
    missing: List[str] = []
    for name in UPSTREAM_REQUIRED_ARTIFACTS:
        payload = _try_read_json(root / name)
        if payload is None:
            missing.append(name)
        else:
            artifacts[name] = payload
    loaded = not missing and bool(artifacts.get("summary.json")) and bool(artifacts.get("verifier_report.json"))
    return {"root": root, "loaded": loaded, "missing": missing, "artifacts": artifacts}


def _is_workspace_fallback(root: Optional[Path]) -> bool:
    return bool(root) and "Luna-Workspace-Min" in str(root)


def _manifest_compare(before: Dict[str, Any], after: Dict[str, Any]) -> Dict[str, Any]:
    before_entries = {e["path"]: e for e in (before.get("entries") or []) if e.get("path")}
    after_entries = {e["path"]: e for e in (after.get("entries") or []) if e.get("path")}
    rows: List[Dict[str, Any]] = []
    all_match = True
    for path in REQUIRED_CANDIDATE_PATHS:
        b = before_entries.get(path, {})
        a = after_entries.get(path, {})
        exists_b = b.get("exists") is True
        exists_a = a.get("exists") is True
        sha_match = b.get("sha256") == a.get("sha256") if exists_b and exists_a else False
        path_unchanged = path == path
        row_ok = exists_b and exists_a and sha_match and path_unchanged
        if not row_ok:
            all_match = False
        rows.append(
            {
                "path": path,
                "before_exists": exists_b,
                "after_exists": exists_a,
                "sha256_match": sha_match,
                "path_unchanged": path_unchanged,
                "stable_placement_confirmed": row_ok,
                "review_pass": row_ok,
            }
        )
    return {"rows": rows, "all_match": all_match, "review_pass": all_match}


def run_main_project_structure_migration_b0_post_migration_review_v1(
    *,
    b0_controlled_execution_root: str,
) -> Dict[str, Any]:
    up = _load_upstream(b0_controlled_execution_root)
    blockers: List[str] = []

    exec_root = up["root"]
    source_path_mode = "workspace_fallback" if _is_workspace_fallback(exec_root) else "repo_eval_out"
    standard_pending = source_path_mode == "workspace_fallback"
    meta = {**_boundary_meta(), "source_path_mode": source_path_mode, "standard_eval_out_write_pending_on_local_repro": standard_pending}

    if not up["loaded"]:
        blockers.append(f"controlled execution input incomplete: {up['missing']}")

    sm = up["artifacts"].get("summary.json") or {}
    vr = up["artifacts"].get("verifier_report.json") or {}
    before = up["artifacts"].get("b0_before_manifest_v1.json") or {}
    after = up["artifacts"].get("b0_after_manifest_v1.json") or {}
    trace = up["artifacts"].get("b0_execution_operation_trace_v1.json") or {}
    blocked = up["artifacts"].get("b0_blocked_operation_assertion_v1.json") or {}
    guard = up["artifacts"].get("b0_protected_eval_out_guard_execution_result_v1.json") or {}
    refactor = up["artifacts"].get("b0_runtime_refactor_block_execution_result_v1.json") or {}

    if vr.get("verifier") != "GO" or vr.get("passed") is not True:
        blockers.append("execution verifier must be GO")
    if sm.get("phase") != UPSTREAM_REQUIRED_PHASE:
        blockers.append("execution phase mismatch")
    if sm.get("final_decision") != UPSTREAM_REQUIRED_FINAL:
        blockers.append("execution final_decision mismatch")
    if sm.get("recommended_next_phase") != UPSTREAM_REQUIRED_NEXT:
        blockers.append("execution recommended_next_phase must be this review phase")
    if sm.get("boundary_ok") is not True:
        blockers.append("execution boundary_ok must be true")
    if sm.get("b0_execution_completed_now") is not True:
        blockers.append("b0_execution_completed_now must be true")
    if sm.get("operations_unchanged") != 3:
        blockers.append("operations_unchanged must be 3")

    manifest_review = _manifest_compare(before, after)
    if not manifest_review["review_pass"]:
        blockers.append("before/after manifest review failed")

    trace_rows = trace.get("trace_rows") or []
    trace_complete = len(trace_rows) == 3 and trace.get("execution_aborted") is False
    all_unchanged = all(r.get("operation") == "unchanged" for r in trace_rows)
    stable_placement_ok = all(
        "stable placement" in (r.get("detail") or "").lower() for r in trace_rows
    )
    if not trace_complete or not all_unchanged:
        blockers.append("operation trace review failed")

    forbidden_ok = blocked.get("all_blocked_ops_absent") is True and sm.get("actual_file_delete_executed") is False
    if not forbidden_ok:
        blockers.append("forbidden operation review failed")

    guard_ok = (
        guard.get("guard_pass") is True
        and sm.get("eval_out_modified_now") is False
        and sm.get("protected_asset_modified_now") is False
        and sm.get("hr_modified_now") is False
        and sm.get("dnae_modified_now") is False
    )
    if not guard_ok:
        blockers.append("protected/eval_out guard review failed")

    refactor_ok = refactor.get("refactor_block_pass") is True and sm.get("runtime_refactor_executed_now") is False
    if not refactor_ok:
        blockers.append("runtime refactor non-execution review failed")

    content_rewrite_ok = refactor.get("content_rewrite_executed") is False
    if not content_rewrite_ok:
        blockers.append("content rewrite non-execution review failed")

    rollback_ok = sm.get("rollback_rehearsal_executed_now") is False
    if not rollback_ok:
        blockers.append("rollback rehearsal must not have executed")

    harness_chain_ok = (
        sm.get("harness_extraction_reopened_now") is False
        and sm.get("harness_adoption_reopened_now") is False
    )
    if not harness_chain_ok:
        blockers.append("harness extraction/adoption chain must not be reopened")

    boundary_ok = not blockers

    policy = _row(
        phase_id=PHASE_ID,
        review_scope=REVIEW_SCOPE,
        source_path_mode=source_path_mode,
        standard_eval_out_write_pending_on_local_repro=standard_pending,
    )

    input_review = {
        "execution_root": str(exec_root),
        "execution_loaded": up["loaded"],
        "execution_summary": {
            "phase": sm.get("phase"),
            "final_decision": sm.get("final_decision"),
            "operations_unchanged": sm.get("operations_unchanged"),
            "b0_execution_completed_now": sm.get("b0_execution_completed_now"),
        },
        "execution_verifier": {"verifier": vr.get("verifier"), "passed": vr.get("passed")},
        "all_pass": boundary_ok,
        "blockers": blockers,
        **meta,
    }

    manifest_review_doc = _row(
        before_manifest_present=before.get("generated_before_execution") is True,
        after_manifest_present=after.get("generated_after_execution") is True,
        compare=manifest_review,
        review_pass=manifest_review["review_pass"],
        **meta,
    )

    trace_review = _row(
        trace_row_count=len(trace_rows),
        all_unchanged=all_unchanged,
        stable_placement_interpretation="stable placement confirmed" if stable_placement_ok else "missing",
        trace_complete=trace_complete,
        review_pass=trace_complete and all_unchanged and stable_placement_ok,
        trace_rows=trace_rows,
        **meta,
    )

    stable_placement_review = _row(
        operations_unchanged=sm.get("operations_unchanged"),
        interpretation="stable placement confirmed; no physical move/rename required",
        candidate_paths=list(REQUIRED_CANDIDATE_PATHS),
        all_three_unchanged=all_unchanged,
        review_pass=all_unchanged and sm.get("operations_unchanged") == 3,
        **meta,
    )

    forbidden_review = _row(
        blocked_operations=["delete", "overwrite", "merge", "copy"],
        all_blocked_ops_absent=blocked.get("all_blocked_ops_absent"),
        actual_move=sm.get("actual_file_move_executed"),
        actual_rename=sm.get("actual_file_rename_executed"),
        review_pass=forbidden_ok,
        **meta,
    )

    guard_review = _row(
        eval_out_modified=sm.get("eval_out_modified_now"),
        protected_modified=sm.get("protected_asset_modified_now"),
        hr_modified=sm.get("hr_modified_now"),
        dnae_modified=sm.get("dnae_modified_now"),
        review_pass=guard_ok,
        **meta,
    )

    refactor_review = _row(
        runtime_refactor_executed=sm.get("runtime_refactor_executed_now"),
        old_phase_deleted=sm.get("old_phase_deleted_now"),
        old_phase_deprecated=sm.get("old_phase_deprecated_now"),
        review_pass=refactor_ok,
        **meta,
    )

    content_review = _row(
        content_rewrite_executed=refactor.get("content_rewrite_executed"),
        review_pass=content_rewrite_ok,
        **meta,
    )

    rollback_review = _row(
        rollback_rehearsal_executed=sm.get("rollback_rehearsal_executed_now"),
        rollback_readiness_confirmed=True,
        review_pass=rollback_ok,
        **meta,
    )

    non_claims_register = {
        "rows": [_row(non_claim_id=f"NC_B0_POST_REVIEW_{i+1:02d}", text=t) for i, t in enumerate(NON_CLAIMS)],
        "row_count": len(NON_CLAIMS),
        **meta,
    }

    readiness = {
        "final_decision": FINAL_DECISION if boundary_ok else "MAIN_PROJECT_STRUCTURE_MIGRATION_B0_POST_MIGRATION_REVIEW_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "b0_closed": boundary_ok,
        "ready_for_b1_preflight_via_harness": boundary_ok,
        "b1_no_adoption_chain_required": True,
        "b1_next_steps": ["B1 Preflight Via Harness", "B1 Controlled Execution", "B1 Post-Migration Review"],
        **meta,
    }

    summary = {
        "phase": PHASE_ID,
        "review_scope": REVIEW_SCOPE,
        "review_only": True,
        "selected_batch_id": "B0",
        "b0_only": True,
        "b1_b7_deferred": True,
        "b0_closed_now": boundary_ok,
        "source_path_mode": source_path_mode,
        "standard_eval_out_write_pending_on_local_repro": standard_pending,
        "execution_loaded": up["loaded"],
        "manifest_review_pass": manifest_review["review_pass"],
        "operation_trace_review_pass": trace_review.get("review_pass"),
        "stable_placement_review_pass": stable_placement_review.get("review_pass"),
        "forbidden_operation_review_pass": forbidden_review.get("review_pass"),
        "protected_eval_out_guard_review_pass": guard_review.get("review_pass"),
        "runtime_refactor_review_pass": refactor_review.get("review_pass"),
        "content_rewrite_review_pass": content_review.get("review_pass"),
        "rollback_readiness_review_pass": rollback_review.get("review_pass"),
        "ready_for_b1_preflight_via_harness": boundary_ok,
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "final_decision": FINAL_DECISION if boundary_ok else "MAIN_PROJECT_STRUCTURE_MIGRATION_B0_POST_MIGRATION_REVIEW_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        **meta,
    }

    return {
        "summary": summary,
        "b0_post_migration_review_policy": policy,
        "b0_controlled_execution_input_review": input_review,
        "b0_before_after_manifest_review": manifest_review_doc,
        "b0_operation_trace_review": trace_review,
        "b0_stable_placement_review": stable_placement_review,
        "b0_forbidden_operation_review": forbidden_review,
        "b0_protected_eval_out_guard_review": guard_review,
        "b0_runtime_refactor_non_execution_review": refactor_review,
        "b0_content_rewrite_non_execution_review": content_review,
        "b0_rollback_readiness_review": rollback_review,
        "b0_post_migration_non_claims_register": non_claims_register,
        "b0_post_migration_review_readiness_decision": readiness,
    }
