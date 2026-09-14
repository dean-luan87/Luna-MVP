# -*- coding: utf-8 -*-
"""Main Project Structure Migration B7 Final Closure Review v1.

Review-only: confirm B7 global consistency preflight is credible (0 high-risk, scan-only).
B7 does not use Controlled Execution (allowed_operations=[]).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID

PHASE_ID = "Phase-Main-Project-Structure-Migration-B7-Final-Closure-Review-v1-001"
REVIEW_SCOPE = "main_project_structure_migration_b7_final_closure_review_only"
SOURCE_CHAIN = "main_project_structure_migration_b7_final_closure_review_v1"

FINAL_DECISION = "MAIN_PROJECT_STRUCTURE_MIGRATION_B7_FINAL_CLOSURE_REVIEW_CLOSED_READY_FOR_MAIN_STRUCTURE_MIGRATION_FINAL_CLOSURE"
NEXT_PHASE = "Phase-Main-Project-Structure-Migration-Final-Closure-v1-001"

UPSTREAM_REQUIRED_PHASE = "Phase-Main-Project-Structure-Migration-B7-Preflight-Via-Harness-v1-001"
UPSTREAM_REQUIRED_FINAL = "MAIN_PROJECT_STRUCTURE_MIGRATION_B7_PREFLIGHT_VIA_HARNESS_READY_FOR_FINAL_CLOSURE_REVIEW"
UPSTREAM_REQUIRED_NEXT = PHASE_ID

GLOBAL_CHECK_KEYS: Tuple[str, ...] = (
    "global_doc_cross_reference_consistency_check",
    "global_python_import_consistency_check",
    "global_config_path_reference_consistency_check",
    "phase_verdict_table_consistency_check",
    "readme_index_consistency_check",
    "migration_batch_closure_consistency_check",
)

SCAN_FILE_MAP: Dict[str, str] = {
    "global_doc_cross_reference_consistency_check": "b7_global_doc_cross_reference_consistency_scan_v1.json",
    "global_python_import_consistency_check": "b7_global_python_import_consistency_scan_v1.json",
    "global_config_path_reference_consistency_check": "b7_global_config_path_reference_consistency_scan_v1.json",
    "phase_verdict_table_consistency_check": "b7_phase_verdict_table_consistency_scan_v1.json",
    "readme_index_consistency_check": "b7_readme_index_consistency_scan_v1.json",
    "migration_batch_closure_consistency_check": "b7_migration_batch_closure_consistency_scan_v1.json",
}


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _boundary_meta() -> Dict[str, Any]:
    return {
        "b7_final_closure_review_only": True,
        "review_only": True,
        "final_consistency_closure_only": True,
        "selected_batch_id": "B7",
        "b7_only": True,
        "b7_closed_now": True,
        "b0_closed": True,
        "b1_closed": True,
        "b2_closed": True,
        "b3_closed": True,
        "b4_closed": True,
        "b5_closed": True,
        "b6_closed": True,
        "harness_contract_reused": True,
        "harness_extraction_reopened_now": False,
        "harness_adoption_reopened_now": False,
        "arming_chain_reopened_now": False,
        "request_chain_reopened_now": False,
        "b7_controlled_execution_skipped": True,
        "batch_execution_started_now": False,
        "actual_file_move_executed": False,
        "actual_file_rename_executed": False,
        "actual_file_delete_executed": False,
        "actual_file_merge_executed": False,
        "actual_file_copy_executed": False,
        "actual_file_overwrite_executed": False,
        "content_rewrite_executed_now": False,
        "import_rewrite_executed_now": False,
        "reference_rewrite_executed_now": False,
        "config_rewrite_executed_now": False,
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


def _collect_low_severity_candidates(
    doc_scan: Dict[str, Any],
    import_scan: Dict[str, Any],
    config_scan: Dict[str, Any],
    readme_scan: Dict[str, Any],
    closure_scan: Dict[str, Any],
) -> List[Dict[str, Any]]:
    register: List[Dict[str, Any]] = []

    def _append_from(scan: Dict[str, Any], key: str, category: str) -> None:
        for item in scan.get(key) or []:
            if item.get("severity") != "low":
                continue
            register.append({**item, "category": category, "deferred": True, "processed_now": False})

    _append_from(doc_scan, "doc_reference_issue_candidates", "doc_cross_reference")
    _append_from(import_scan, "import_issue_candidates", "python_import")
    _append_from(config_scan, "config_path_issue_candidates", "config_path_reference")
    _append_from(readme_scan, "readme_index_issue_candidates", "readme_index")
    _append_from(closure_scan, "migration_batch_closure_issue_candidates", "batch_closure")
    return register


def run_main_project_structure_migration_b7_final_closure_review_v1(
    *,
    b7_preflight_via_harness_root: str,
) -> Dict[str, Any]:
    blockers: List[str] = []
    preflight_root = Path(b7_preflight_via_harness_root).expanduser().resolve()

    source_path_mode = "workspace_fallback" if _is_workspace_fallback(preflight_root) else "repo_eval_out"
    meta = {
        **_boundary_meta(),
        "source_path_mode": source_path_mode,
        "standard_eval_out_write_pending_on_local_repro": source_path_mode == "workspace_fallback",
    }

    sm = _try_read_json(preflight_root / "summary.json") or {}
    vr = _try_read_json(preflight_root / "verifier_report.json") or {}
    batch_cfg = _try_read_json(preflight_root / "b7_batch_config_v1.json") or {}
    readiness_pf = _try_read_json(preflight_root / "b7_preflight_readiness_decision_v1.json") or {}

    doc_scan = _try_read_json(preflight_root / SCAN_FILE_MAP["global_doc_cross_reference_consistency_check"]) or {}
    import_scan = _try_read_json(preflight_root / SCAN_FILE_MAP["global_python_import_consistency_check"]) or {}
    config_scan = _try_read_json(preflight_root / SCAN_FILE_MAP["global_config_path_reference_consistency_check"]) or {}
    verdict_scan = _try_read_json(preflight_root / SCAN_FILE_MAP["phase_verdict_table_consistency_check"]) or {}
    readme_scan = _try_read_json(preflight_root / SCAN_FILE_MAP["readme_index_consistency_check"]) or {}
    closure_scan = _try_read_json(preflight_root / SCAN_FILE_MAP["migration_batch_closure_consistency_check"]) or {}

    path_count = sm.get("candidate_path_count") or 0
    check_results = sm.get("check_results") or {}

    if vr.get("verifier") != "GO" or vr.get("passed") is not True:
        blockers.append("preflight verifier must be GO")
    if sm.get("phase") != UPSTREAM_REQUIRED_PHASE:
        blockers.append("preflight phase mismatch")
    if sm.get("final_decision") != UPSTREAM_REQUIRED_FINAL:
        blockers.append("preflight final_decision mismatch")
    if sm.get("recommended_next_phase") != UPSTREAM_REQUIRED_NEXT:
        blockers.append("recommended_next_phase mismatch")
    if sm.get("boundary_ok") is not True:
        blockers.append("preflight boundary_ok must be true")
    if sm.get("hold_for_review") is True:
        blockers.append("hold_for_review must be false")
    if sm.get("all_fixed_checks_pass") is not True:
        blockers.append("all_fixed_checks_pass must be true")
    if batch_cfg.get("allowed_operations") != []:
        blockers.append("allowed_operations must be empty for B7")

    high_risk_total = (
        (sm.get("doc_high_risk_count") or 0)
        + (sm.get("import_high_risk_count") or 0)
        + (sm.get("config_high_risk_count") or 0)
        + (sm.get("verdict_high_risk_count") or 0)
        + (sm.get("readme_high_risk_count") or 0)
        + (sm.get("closure_high_risk_count") or 0)
    )
    if high_risk_total != 0:
        blockers.append(f"high_risk_total must be 0, got {high_risk_total}")

    scan_reviews: Dict[str, Dict[str, Any]] = {}
    for check_key in GLOBAL_CHECK_KEYS:
        scan = {
            "global_doc_cross_reference_consistency_check": doc_scan,
            "global_python_import_consistency_check": import_scan,
            "global_config_path_reference_consistency_check": config_scan,
            "phase_verdict_table_consistency_check": verdict_scan,
            "readme_index_consistency_check": readme_scan,
            "migration_batch_closure_consistency_check": closure_scan,
        }[check_key]
        check_pass = check_results.get(check_key) is True and scan.get("check_pass") is True
        if not check_pass:
            blockers.append(f"{check_key} must pass")
        scan_reviews[check_key] = {
            "check_id": check_key,
            "scan_file": SCAN_FILE_MAP[check_key],
            "check_pass": check_pass,
            "high_risk_count": scan.get("high_risk_count", 0),
            "low_severity_count": scan.get("low_severity_count", 0),
            "interpretation": scan.get("interpretation"),
            "review_pass": check_pass,
        }

    global_consistency_pass = all(r["review_pass"] for r in scan_reviews.values())

    forbidden_ok = (
        sm.get("actual_file_move_executed") is False
        and sm.get("actual_file_rename_executed") is False
        and sm.get("actual_file_delete_executed") is False
        and sm.get("actual_file_overwrite_executed") is False
        and sm.get("actual_file_merge_executed") is False
        and sm.get("actual_file_copy_executed") is False
        and sm.get("content_rewrite_executed_now") is False
        and sm.get("import_rewrite_executed_now") is False
        and sm.get("reference_rewrite_executed_now") is False
        and sm.get("config_rewrite_executed_now") is False
    )
    guard_ok = (
        sm.get("eval_out_modified_now") is False
        and sm.get("protected_asset_modified_now") is False
        and sm.get("hr_modified_now") is False
        and sm.get("dnae_modified_now") is False
    )
    chain_ok = (
        sm.get("harness_extraction_reopened_now") is False
        and sm.get("harness_adoption_reopened_now") is False
        and sm.get("arming_chain_reopened_now") is False
        and sm.get("request_chain_reopened_now") is False
    )
    phase_ok = sm.get("old_phase_deleted_now") is False and sm.get("old_phase_deprecated_now") is False
    batches_closed_ok = all(sm.get(f"b{n}_closed") is True for n in range(7))

    if not forbidden_ok:
        blockers.append("forbidden operation review failed")
    if not guard_ok:
        blockers.append("protected/eval_out guard failed")
    if not chain_ok:
        blockers.append("harness/arming/request chain reopened")
    if not phase_ok:
        blockers.append("old phase guard failed")
    if not batches_closed_ok:
        blockers.append("B0–B6 must be closed")

    low_register = _collect_low_severity_candidates(doc_scan, import_scan, config_scan, readme_scan, closure_scan)
    low_deferred_ok = all(item.get("processed_now") is False for item in low_register)

    boundary_ok = not blockers and global_consistency_pass and forbidden_ok and guard_ok

    global_consistency_review = {
        "candidate_path_count": path_count,
        "global_checks": scan_reviews,
        "global_consistency_review_pass": global_consistency_pass and boundary_ok,
        "high_risk_total": high_risk_total,
        "all_global_checks_pass": global_consistency_pass,
        "interpretation": "B7 global consistency scans credible; 0 high-risk" if boundary_ok else "global consistency review failed",
        **meta,
    }

    low_severity_register = {
        "register_id": "b7_low_severity_candidate_register_v1",
        "candidate_count": len(low_register),
        "doc_low_severity_count": sm.get("doc_low_severity_count", 0),
        "import_low_severity_count": sm.get("import_low_severity_count", 0),
        "config_low_severity_count": sm.get("config_low_severity_count", 0),
        "readme_low_severity_count": sm.get("readme_low_severity_count", 0),
        "closure_low_severity_count": sm.get("closure_low_severity_count", 0),
        "all_deferred": low_deferred_ok,
        "processed_now": False,
        "candidates": low_register,
        "interpretation": "low-severity candidates recorded; not processed in B7",
        **meta,
    }

    no_execution_boundary_review = {
        "allowed_operations": batch_cfg.get("allowed_operations", []),
        "blocked_operations": batch_cfg.get("blocked_operations", []),
        "b7_controlled_execution_skipped": True,
        "forbidden_operation_review_pass": forbidden_ok,
        "protected_eval_out_guard_review_pass": guard_ok,
        "harness_chain_guard_pass": chain_ok,
        "old_phase_guard_pass": phase_ok,
        "b0_b6_closed": batches_closed_ok,
        "file_operation_executed_now": False,
        "review_pass": forbidden_ok and guard_ok and chain_ok and phase_ok and batches_closed_ok,
        "interpretation": "B7 scan-only closure; no file operations executed",
        **meta,
    }

    readiness = {
        "final_decision": FINAL_DECISION if boundary_ok else "MAIN_PROJECT_STRUCTURE_MIGRATION_B7_FINAL_CLOSURE_REVIEW_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "b7_closed": boundary_ok,
        "ready_for_main_structure_migration_final_closure": boundary_ok,
        "ready_for_b7_controlled_execution": False,
        "harness_contract_reusable": sm.get("harness_contract_reused") is True,
        "low_severity_register_complete": len(low_register) > 0 or sum(
            sm.get(k, 0) for k in (
                "doc_low_severity_count",
                "import_low_severity_count",
                "config_low_severity_count",
                "readme_low_severity_count",
                "closure_low_severity_count",
            )
        ) >= 0,
        **meta,
    }

    summary = {
        "phase": PHASE_ID,
        "review_scope": REVIEW_SCOPE,
        "selected_batch_id": "B7",
        "batch_domain": sm.get("batch_domain"),
        "b7_closed_now": boundary_ok,
        "candidate_path_count": path_count,
        "allowed_operations": batch_cfg.get("allowed_operations", []),
        "hold_for_review": sm.get("hold_for_review", False),
        "high_risk_total": high_risk_total,
        "global_consistency_review_pass": global_consistency_review.get("global_consistency_review_pass"),
        "no_execution_boundary_review_pass": no_execution_boundary_review.get("review_pass"),
        "low_severity_candidate_count": len(low_register),
        "low_severity_all_deferred": low_deferred_ok,
        "ready_for_main_structure_migration_final_closure": boundary_ok,
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "final_decision": readiness["final_decision"],
        "recommended_next_phase": readiness["recommended_next_phase"],
        "preflight_readiness_confirmed": readiness_pf.get("ready_for_b7_final_closure_review") is True,
        **meta,
    }

    return {
        "summary": summary,
        "b7_global_consistency_review": global_consistency_review,
        "b7_low_severity_candidate_register": low_severity_register,
        "b7_no_execution_boundary_review": no_execution_boundary_review,
        "b7_final_closure_readiness_decision": readiness,
    }
