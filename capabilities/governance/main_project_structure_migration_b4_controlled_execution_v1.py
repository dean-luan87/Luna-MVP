# -*- coding: utf-8 -*-
"""Main Project Structure Migration B4 Controlled Execution v1.

Compressed controlled execution for Runner / verifier stable placement.
Only move/rename; no content/import/PHASE_ID rewrite or module rename.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.main_project_structure_migration_b4_preflight_via_harness_v1 import (
    GOVERNANCE_TOOLS_ROOT,
    scan_runner_verifier_candidate_paths,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID

PHASE_ID = "Phase-Main-Project-Structure-Migration-B4-Controlled-Execution-v1-001"
EXECUTION_SCOPE = "main_project_structure_migration_b4_controlled_execution_only"
SOURCE_CHAIN = "main_project_structure_migration_b4_controlled_execution_v1"

FINAL_DECISION = "MAIN_PROJECT_STRUCTURE_MIGRATION_B4_CONTROLLED_EXECUTION_READY_FOR_POST_MIGRATION_REVIEW"
NEXT_PHASE = "Phase-Main-Project-Structure-Migration-B4-Post-Migration-Review-v1-001"

UPSTREAM_REQUIRED_PHASE = "Phase-Main-Project-Structure-Migration-B4-Preflight-Via-Harness-v1-001"
UPSTREAM_REQUIRED_FINAL = "MAIN_PROJECT_STRUCTURE_MIGRATION_B4_PREFLIGHT_VIA_HARNESS_READY_FOR_CONTROLLED_EXECUTION"
UPSTREAM_REQUIRED_NEXT = PHASE_ID

FORBIDDEN_SCOPE_TOKENS: Tuple[str, ...] = (
    "capabilities/",
    "docs/architecture/",
    "configs/",
    "scripts/",
    "tests/",
    "_eval_out",
    "protected/",
    "/hr/",
    "dnae",
)


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _boundary_meta(*, move_executed: bool = False, rename_executed: bool = False, execution_completed: bool = False) -> Dict[str, Any]:
    return {
        "b4_controlled_execution_only": True,
        "selected_batch_id": "B4",
        "b4_only": True,
        "b0_closed": True,
        "b1_closed": True,
        "b2_closed": True,
        "b3_closed": True,
        "b5_b7_deferred": True,
        "harness_contract_reused": True,
        "harness_extraction_reopened_now": False,
        "harness_adoption_reopened_now": False,
        "arming_chain_reopened_now": False,
        "request_chain_reopened_now": False,
        "b4_execution_started_now": True,
        "batch_execution_started_now": True,
        "b4_execution_completed_now": execution_completed,
        "actual_file_move_executed": move_executed,
        "actual_file_rename_executed": rename_executed,
        "actual_file_delete_executed": False,
        "actual_file_merge_executed": False,
        "actual_file_copy_executed": False,
        "actual_file_overwrite_executed": False,
        "content_rewrite_executed_now": False,
        "import_rewrite_executed_now": False,
        "phase_id_modified_now": False,
        "module_rename_executed_now": False,
        "eval_out_modified_now": False,
        "protected_asset_modified_now": False,
        "hr_modified_now": False,
        "dnae_modified_now": False,
        "runtime_refactor_executed_now": False,
        "old_phase_deleted_now": False,
        "old_phase_deprecated_now": False,
        "verifier_rerun_executed_now": False,
        "rollback_rehearsal_executed_now": False,
        "post_migration_tests_executed_now": False,
        "file_operation_executed_now": move_executed or rename_executed,
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


def _path_forbidden(rel: str) -> bool:
    lower = rel.lower().replace("\\", "/")
    return any(t in lower for t in FORBIDDEN_SCOPE_TOKENS)


def _file_fingerprint(repo_root: Path, rel: str) -> Dict[str, Any]:
    p = repo_root / rel
    if not p.is_file():
        return {"path": rel, "exists": False}
    st = p.stat()
    return {
        "path": rel,
        "exists": True,
        "size_bytes": st.st_size,
        "mtime_ns": st.st_mtime_ns,
        "sha256": hashlib.sha256(p.read_bytes()).hexdigest(),
    }


def run_main_project_structure_migration_b4_controlled_execution_v1(
    *,
    b4_preflight_via_harness_root: str,
    repo_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []
    abort_reasons: List[str] = []

    preflight_root = Path(b4_preflight_via_harness_root).expanduser().resolve()
    resolved_repo = Path(repo_root).expanduser().resolve() if repo_root else Path(__file__).resolve().parents[2]

    source_path_mode = "workspace_fallback" if _is_workspace_fallback(preflight_root) else "repo_eval_out"
    standard_pending = source_path_mode == "workspace_fallback"

    sm = _try_read_json(preflight_root / "summary.json") or {}
    vr = _try_read_json(preflight_root / "verifier_report.json") or {}
    batch_cfg = _try_read_json(preflight_root / "b4_batch_config_v1.json") or {}
    check_results = sm.get("check_results") or {}

    if vr.get("verifier") != "GO" or vr.get("passed") is not True:
        blockers.append("preflight verifier must be GO")
    if sm.get("phase") != UPSTREAM_REQUIRED_PHASE:
        blockers.append("preflight phase mismatch")
    if sm.get("final_decision") != UPSTREAM_REQUIRED_FINAL:
        blockers.append("preflight final_decision mismatch")
    if sm.get("recommended_next_phase") != UPSTREAM_REQUIRED_NEXT:
        blockers.append("preflight recommended_next_phase mismatch")
    if sm.get("boundary_ok") is not True:
        blockers.append("preflight boundary_ok must be true")
    if sm.get("harness_contract_reused") is not True:
        blockers.append("harness_contract_reused must be true")
    if sm.get("all_fixed_checks_pass") is not True:
        blockers.append("preflight all_fixed_checks_pass must be true")
    if sm.get("hold_for_review") is True:
        blockers.append("preflight hold_for_review must be false")
    if check_results.get("runner_verifier_pairing_consistency_check") is not True:
        blockers.append("runner_verifier_pairing_consistency_check must pass")
    if check_results.get("phase_reference_consistency_check") is not True:
        blockers.append("phase_reference_consistency_check must pass")
    if check_results.get("runner_module_import_consistency_check") is not True:
        blockers.append("runner_module_import_consistency_check must pass")
    if (sm.get("pairing_high_risk_count") or 0) != 0:
        blockers.append("pairing_high_risk_count must be 0")
    if (sm.get("phase_reference_high_risk_count") or 0) != 0:
        blockers.append("phase_reference_high_risk_count must be 0")
    if (sm.get("import_high_risk_count") or 0) != 0:
        blockers.append("import_high_risk_count must be 0")
    paired = sm.get("paired_count") or 0
    run_count = sm.get("run_script_count") or 0
    verify_count = sm.get("verify_script_count") or 0
    if run_count <= 0 or verify_count <= 0 or paired != run_count or paired != verify_count:
        blockers.append("run/verify pairing counts invalid")
    if sm.get("arming_chain_reopened_now") is not False:
        blockers.append("arming chain must not be reopened")
    if sm.get("request_chain_reopened_now") is not False:
        blockers.append("request chain must not be reopened")
    if sm.get("harness_extraction_reopened_now") is not False:
        blockers.append("harness extraction must not be reopened")
    if sm.get("harness_adoption_reopened_now") is not False:
        blockers.append("harness adoption must not be reopened")

    allowed = set(batch_cfg.get("allowed_operations") or [])
    blocked = set(batch_cfg.get("blocked_operations") or [])
    if allowed != {"move", "rename"}:
        blockers.append("allowed_operations must be move/rename only")
    if not {"delete", "overwrite", "merge", "copy", "content_rewrite", "import_rewrite"}.issubset(blocked):
        blockers.append("blocked_operations must include delete/overwrite/merge/copy/content_rewrite/import_rewrite")

    candidate_paths = list(batch_cfg.get("candidate_paths") or [])
    if not candidate_paths:
        candidate_paths = scan_runner_verifier_candidate_paths(resolved_repo)
    if len(candidate_paths) == 0:
        blockers.append("no candidate paths")

    preflight_count = sm.get("candidate_path_count")
    if preflight_count is not None and len(candidate_paths) != preflight_count:
        blockers.append(f"candidate_path_count mismatch: preflight={preflight_count} batch={len(candidate_paths)}")

    for rel in candidate_paths:
        if _path_forbidden(rel) or not rel.startswith(f"{GOVERNANCE_TOOLS_ROOT}/") or not rel.endswith(".py"):
            abort_reasons.append(f"scope_escape: {rel}")
            blockers.append(f"forbidden scope: {rel}")

    before_entries = [_file_fingerprint(resolved_repo, rel) for rel in candidate_paths]
    missing = [e["path"] for e in before_entries if not e.get("exists")]
    if missing:
        blockers.append(f"missing paths: {len(missing)}")
        abort_reasons.extend([f"missing: {p}" for p in missing[:5]])

    move_executed = False
    rename_executed = False
    trace_rows: List[Dict[str, Any]] = []
    execution_aborted = bool(blockers)

    if not execution_aborted:
        for rel in candidate_paths:
            target = rel
            src = resolved_repo / rel
            if not src.is_file():
                execution_aborted = True
                abort_reasons.append(f"missing_at_execution: {rel}")
                break
            trace_rows.append(
                {
                    "source_path": rel,
                    "target_path": target,
                    "operation": "unchanged",
                    "status": "completed",
                    "stable_placement_confirmed": True,
                    "moved": False,
                    "renamed": False,
                    "skipped": False,
                    "aborted": False,
                    "detail": "stable placement confirmed; no path change required",
                }
            )

    execution_completed = not execution_aborted and len(trace_rows) == len(candidate_paths)
    meta = {
        **_boundary_meta(move_executed=move_executed, rename_executed=rename_executed, execution_completed=execution_completed),
        "source_path_mode": source_path_mode,
        "standard_eval_out_write_pending_on_local_repro": standard_pending,
        "run_script_count": run_count,
        "verify_script_count": verify_count,
        "paired_count": paired,
        "phase_reference_low_severity_count": sm.get("phase_reference_low_severity_count", 0),
        "low_severity_candidates_deferred": True,
    }

    after_entries = [_file_fingerprint(resolved_repo, rel) for rel in candidate_paths] if execution_completed else []

    unchanged_count = sum(1 for t in trace_rows if t.get("operation") == "unchanged")
    boundary_ok = execution_completed and not blockers

    before_manifest = {
        "manifest_id": "b4_before_manifest_v1",
        "batch_id": "B4",
        "entry_count": len(before_entries),
        "entries": before_entries,
        **meta,
    }

    execution_result = {
        "batch_id": "B4",
        "batch_domain": batch_cfg.get("batch_domain", "Runner / verifier stable placement"),
        "trace_rows": trace_rows,
        "operations_total": len(trace_rows),
        "operations_unchanged": unchanged_count,
        "operations_moved": 0,
        "operations_renamed": 0,
        "operations_skipped": 0,
        "operations_aborted": 0,
        "execution_aborted": execution_aborted,
        "abort_reasons": abort_reasons,
        "all_scoped_paths_pass": execution_completed,
        **meta,
    }

    after_manifest = {
        "manifest_id": "b4_after_manifest_v1",
        "batch_id": "B4",
        "entry_count": len(after_entries),
        "entries": after_entries,
        "generated_after_execution": execution_completed,
        **meta,
    }

    refactor_scan = {
        "scan_scope": [GOVERNANCE_TOOLS_ROOT],
        "duplicate_pattern_candidates": [
            {"pattern": "run/verify argparse + OUTPUT_FILES boilerplate", "location": GOVERNANCE_TOOLS_ROOT},
            {"pattern": "verifier meta inflation loop", "location": GOVERNANCE_TOOLS_ROOT},
        ],
        "extract_now_allowed": False,
        "extract_later_candidates": [{"tier": "A", "candidate": "shared_run_verify_output_writer"}],
        "blocked_from_runtime_refactor_now": True,
        "runtime_refactor_executed_now": False,
        "old_phase_deleted_now": False,
        "old_phase_deprecated_now": False,
        **meta,
    }

    summary = {
        "phase": PHASE_ID,
        "execution_scope": EXECUTION_SCOPE,
        "selected_batch_id": "B4",
        "batch_domain": batch_cfg.get("batch_domain"),
        "candidate_path_count": len(candidate_paths),
        "operations_unchanged": unchanged_count,
        "operations_moved": 0,
        "operations_renamed": 0,
        "execution_aborted": execution_aborted,
        "boundary_ok": boundary_ok,
        "violations": blockers + abort_reasons,
        "final_decision": FINAL_DECISION if boundary_ok else "MAIN_PROJECT_STRUCTURE_MIGRATION_B4_CONTROLLED_EXECUTION_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        **meta,
    }

    return {
        "summary": summary,
        "b4_before_manifest": before_manifest,
        "b4_execution_result": execution_result,
        "b4_after_manifest": after_manifest,
        "b4_migration_refactor_opportunity_scan": refactor_scan,
    }
