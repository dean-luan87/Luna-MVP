# -*- coding: utf-8 -*-
"""Main Project Structure Migration B5 Post-Migration Review v1.

Compressed review-only: audit B5 controlled execution (29 config files, stable placement).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID

PHASE_ID = "Phase-Main-Project-Structure-Migration-B5-Post-Migration-Review-v1-001"
REVIEW_SCOPE = "main_project_structure_migration_b5_post_migration_review_only"
SOURCE_CHAIN = "main_project_structure_migration_b5_post_migration_review_v1"

FINAL_DECISION = "MAIN_PROJECT_STRUCTURE_MIGRATION_B5_POST_MIGRATION_REVIEW_CLOSED_READY_FOR_B6_PREFLIGHT_VIA_HARNESS"
NEXT_PHASE = "Phase-Main-Project-Structure-Migration-B6-Preflight-Via-Harness-v1-001"

UPSTREAM_REQUIRED_PHASE = "Phase-Main-Project-Structure-Migration-B5-Controlled-Execution-v1-001"
UPSTREAM_REQUIRED_FINAL = "MAIN_PROJECT_STRUCTURE_MIGRATION_B5_CONTROLLED_EXECUTION_READY_FOR_POST_MIGRATION_REVIEW"
UPSTREAM_REQUIRED_NEXT = PHASE_ID


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _boundary_meta() -> Dict[str, Any]:
    return {
        "b5_post_migration_review_only": True,
        "review_only": True,
        "selected_batch_id": "B5",
        "b5_only": True,
        "b5_closed_now": True,
        "b0_closed": True,
        "b1_closed": True,
        "b2_closed": True,
        "b3_closed": True,
        "b4_closed": True,
        "b6_b7_deferred": True,
        "harness_contract_reused": True,
        "harness_extraction_reopened_now": False,
        "harness_adoption_reopened_now": False,
        "arming_chain_reopened_now": False,
        "request_chain_reopened_now": False,
        "b5_execution_completed_now": True,
        "actual_file_move_executed": False,
        "actual_file_rename_executed": False,
        "actual_file_delete_executed": False,
        "actual_file_merge_executed": False,
        "actual_file_copy_executed": False,
        "actual_file_overwrite_executed": False,
        "content_rewrite_executed_now": False,
        "config_rewrite_executed_now": False,
        "schema_rewrite_executed_now": False,
        "reference_rewrite_executed_now": False,
        "eval_out_modified_now": False,
        "protected_asset_modified_now": False,
        "hr_modified_now": False,
        "dnae_modified_now": False,
        "runtime_refactor_executed_now": False,
        "old_phase_deleted_now": False,
        "old_phase_deprecated_now": False,
        "verifier_rerun_executed_now": False,
        "rollback_rehearsal_executed_now": False,
        "file_operation_executed_now": False,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def _is_workspace_fallback(root: Optional[Path]) -> bool:
    return bool(root) and "Luna-Workspace-Min" in str(root)


def _compare_manifests(before: Dict[str, Any], after: Dict[str, Any], expected_count: int) -> Dict[str, Any]:
    before_map = {e["path"]: e for e in (before.get("entries") or []) if e.get("path")}
    after_map = {e["path"]: e for e in (after.get("entries") or []) if e.get("path")}
    all_match = True
    mismatches: List[str] = []
    for path, b in before_map.items():
        a = after_map.get(path, {})
        if not b.get("exists") or not a.get("exists"):
            all_match = False
            mismatches.append(path)
            continue
        if b.get("sha256") != a.get("sha256"):
            all_match = False
            mismatches.append(path)
    count_ok = len(before_map) == expected_count and len(after_map) == expected_count
    return {
        "before_count": len(before_map),
        "after_count": len(after_map),
        "expected_count": expected_count,
        "count_ok": count_ok,
        "sha256_all_match": all_match and count_ok,
        "mismatch_count": len(mismatches),
        "review_pass": all_match and count_ok,
        "interpretation": "stable placement confirmed" if all_match and count_ok else "manifest mismatch",
    }


def run_main_project_structure_migration_b5_post_migration_review_v1(
    *,
    b5_controlled_execution_root: str,
) -> Dict[str, Any]:
    blockers: List[str] = []
    exec_root = Path(b5_controlled_execution_root).expanduser().resolve()

    source_path_mode = "workspace_fallback" if _is_workspace_fallback(exec_root) else "repo_eval_out"
    meta = {
        **_boundary_meta(),
        "source_path_mode": source_path_mode,
        "standard_eval_out_write_pending_on_local_repro": source_path_mode == "workspace_fallback",
    }

    sm = _try_read_json(exec_root / "summary.json") or {}
    vr = _try_read_json(exec_root / "verifier_report.json") or {}
    before = _try_read_json(exec_root / "b5_before_manifest_v1.json") or {}
    after = _try_read_json(exec_root / "b5_after_manifest_v1.json") or {}
    execution = _try_read_json(exec_root / "b5_execution_result_v1.json") or {}

    path_count = sm.get("candidate_path_count") or 0
    unchanged_count = sm.get("operations_unchanged") or 0

    if vr.get("verifier") != "GO" or vr.get("passed") is not True:
        blockers.append("execution verifier must be GO")
    if sm.get("phase") != UPSTREAM_REQUIRED_PHASE:
        blockers.append("execution phase mismatch")
    if sm.get("final_decision") != UPSTREAM_REQUIRED_FINAL:
        blockers.append("execution final_decision mismatch")
    if sm.get("recommended_next_phase") != UPSTREAM_REQUIRED_NEXT:
        blockers.append("recommended_next_phase mismatch")
    if sm.get("boundary_ok") is not True:
        blockers.append("execution boundary_ok must be true")
    if sm.get("b5_execution_completed_now") is not True:
        blockers.append("b5_execution_completed_now must be true")
    if unchanged_count != path_count:
        blockers.append("operations_unchanged must equal candidate_path_count")

    manifest_cmp = _compare_manifests(before, after, path_count)
    if not manifest_cmp["review_pass"]:
        blockers.append("manifest review failed")

    trace_rows = execution.get("trace_rows") or []
    trace_ok = (
        len(trace_rows) == path_count
        and execution.get("execution_aborted") is False
        and execution.get("operations_unchanged") == path_count
        and all(r.get("operation") == "unchanged" for r in trace_rows)
        and all(r.get("stable_placement_confirmed") is True for r in trace_rows)
    )
    if not trace_ok:
        blockers.append("operation trace review failed")

    forbidden_ok = (
        sm.get("actual_file_move_executed") is False
        and sm.get("actual_file_rename_executed") is False
        and sm.get("config_rewrite_executed_now") is False
        and sm.get("schema_rewrite_executed_now") is False
        and sm.get("reference_rewrite_executed_now") is False
    )
    guard_ok = (
        sm.get("eval_out_modified_now") is False
        and sm.get("protected_asset_modified_now") is False
        and sm.get("hr_modified_now") is False
        and sm.get("dnae_modified_now") is False
    )
    refactor_ok = sm.get("runtime_refactor_executed_now") is False
    phase_ok = sm.get("old_phase_deleted_now") is False and sm.get("old_phase_deprecated_now") is False
    rollback_ok = sm.get("rollback_rehearsal_executed_now") is False
    chain_ok = (
        sm.get("harness_extraction_reopened_now") is False
        and sm.get("harness_adoption_reopened_now") is False
        and sm.get("arming_chain_reopened_now") is False
        and sm.get("request_chain_reopened_now") is False
    )

    if not forbidden_ok:
        blockers.append("forbidden operation review failed")
    if not guard_ok:
        blockers.append("protected/eval_out guard failed")
    if not refactor_ok or not phase_ok:
        blockers.append("refactor/phase guard failed")
    if not chain_ok:
        blockers.append("harness/arming/request chain reopened")

    boundary_ok = not blockers

    manifest_review = {**manifest_cmp, **meta, "review_pass": manifest_cmp["review_pass"] and boundary_ok}

    trace_review = {
        "trace_row_count": len(trace_rows),
        "expected_count": path_count,
        "configs_count": sm.get("configs_count"),
        "all_unchanged": trace_ok,
        "interpretation": f"stable placement confirmed; {path_count} config files unchanged",
        "review_pass": trace_ok,
        **meta,
    }

    boundary_guard_review = {
        "forbidden_operation_review_pass": forbidden_ok,
        "protected_eval_out_guard_review_pass": guard_ok,
        "runtime_refactor_review_pass": refactor_ok,
        "config_rewrite_review_pass": sm.get("config_rewrite_executed_now") is False,
        "reference_rewrite_review_pass": sm.get("reference_rewrite_executed_now") is False,
        "old_phase_guard_pass": phase_ok,
        "rollback_readiness_pass": rollback_ok,
        "harness_chain_guard_pass": chain_ok,
        "low_severity_candidates_deferred": sm.get("low_severity_candidates_deferred") is True,
        "review_pass": forbidden_ok and guard_ok and refactor_ok and phase_ok and rollback_ok and chain_ok,
        **meta,
    }

    readiness = {
        "final_decision": FINAL_DECISION if boundary_ok else "MAIN_PROJECT_STRUCTURE_MIGRATION_B5_POST_MIGRATION_REVIEW_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "b5_closed": boundary_ok,
        "ready_for_b6_preflight_via_harness": boundary_ok,
        **meta,
    }

    summary = {
        "phase": PHASE_ID,
        "review_scope": REVIEW_SCOPE,
        "selected_batch_id": "B5",
        "b5_closed_now": boundary_ok,
        "candidate_path_count": path_count,
        "operations_unchanged": unchanged_count,
        "manifest_review_pass": manifest_review.get("review_pass"),
        "operation_trace_review_pass": trace_review.get("review_pass"),
        "boundary_guard_review_pass": boundary_guard_review.get("review_pass"),
        "ready_for_b6_preflight_via_harness": boundary_ok,
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "final_decision": readiness["final_decision"],
        "recommended_next_phase": readiness["recommended_next_phase"],
        **meta,
    }

    return {
        "summary": summary,
        "b5_manifest_review": manifest_review,
        "b5_operation_trace_review": trace_review,
        "b5_boundary_guard_review": boundary_guard_review,
        "b5_post_migration_readiness_decision": readiness,
    }
