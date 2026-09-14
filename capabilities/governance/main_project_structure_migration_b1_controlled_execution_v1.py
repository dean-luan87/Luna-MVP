# -*- coding: utf-8 -*-
"""Main Project Structure Migration B1 Controlled Execution v1.

Compressed controlled execution for Governance docs stable placement.
Only move/rename; stable placement unchanged when already at target path.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.main_project_structure_migration_b1_preflight_via_harness_v1 import (
    GOVERNANCE_ROOT,
    scan_governance_candidate_paths,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID

PHASE_ID = "Phase-Main-Project-Structure-Migration-B1-Controlled-Execution-v1-001"
EXECUTION_SCOPE = "main_project_structure_migration_b1_controlled_execution_only"
SOURCE_CHAIN = "main_project_structure_migration_b1_controlled_execution_v1"

FINAL_DECISION = "MAIN_PROJECT_STRUCTURE_MIGRATION_B1_CONTROLLED_EXECUTION_READY_FOR_POST_MIGRATION_REVIEW"
NEXT_PHASE = "Phase-Main-Project-Structure-Migration-B1-Post-Migration-Review-v1-001"

UPSTREAM_REQUIRED_PHASE = "Phase-Main-Project-Structure-Migration-B1-Preflight-Via-Harness-v1-001"
UPSTREAM_REQUIRED_FINAL = "MAIN_PROJECT_STRUCTURE_MIGRATION_B1_PREFLIGHT_VIA_HARNESS_READY_FOR_CONTROLLED_EXECUTION"
UPSTREAM_REQUIRED_NEXT = PHASE_ID

FORBIDDEN_SCOPE_TOKENS: Tuple[str, ...] = (
    "capabilities/",
    "tools/",
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
        "b1_controlled_execution_only": True,
        "selected_batch_id": "B1",
        "b1_only": True,
        "b0_closed": True,
        "b2_b7_deferred": True,
        "harness_contract_reused": True,
        "harness_extraction_reopened_now": False,
        "harness_adoption_reopened_now": False,
        "arming_chain_reopened_now": False,
        "request_chain_reopened_now": False,
        "b1_execution_started_now": True,
        "batch_execution_started_now": True,
        "b1_execution_completed_now": execution_completed,
        "actual_file_move_executed": move_executed,
        "actual_file_rename_executed": rename_executed,
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


def run_main_project_structure_migration_b1_controlled_execution_v1(
    *,
    b1_preflight_via_harness_root: str,
    repo_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []
    abort_reasons: List[str] = []

    preflight_root = Path(b1_preflight_via_harness_root).expanduser().resolve()
    resolved_repo = Path(repo_root).expanduser().resolve() if repo_root else Path(__file__).resolve().parents[2]

    source_path_mode = "workspace_fallback" if _is_workspace_fallback(preflight_root) else "repo_eval_out"
    standard_pending = source_path_mode == "workspace_fallback"

    sm = _try_read_json(preflight_root / "summary.json") or {}
    vr = _try_read_json(preflight_root / "verifier_report.json") or {}
    batch_cfg = _try_read_json(preflight_root / "b1_batch_config_v1.json") or {}

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
    if sm.get("arming_chain_reopened_now") is not False:
        blockers.append("arming chain must not be reopened")
    if sm.get("request_chain_reopened_now") is not False:
        blockers.append("request chain must not be reopened")

    candidate_paths = list(batch_cfg.get("candidate_paths") or [])
    if not candidate_paths:
        candidate_paths = scan_governance_candidate_paths(resolved_repo)
    if len(candidate_paths) == 0:
        blockers.append("no candidate paths")

    for rel in candidate_paths:
        if _path_forbidden(rel) or not rel.startswith(f"{GOVERNANCE_ROOT}/"):
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
            target = rel  # stable placement: source == target
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
    }

    after_entries = [_file_fingerprint(resolved_repo, rel) for rel in candidate_paths] if execution_completed else []

    unchanged_count = sum(1 for t in trace_rows if t.get("operation") == "unchanged")
    boundary_ok = execution_completed and not blockers

    before_manifest = {
        "manifest_id": "b1_before_manifest_v1",
        "batch_id": "B1",
        "entry_count": len(before_entries),
        "entries": before_entries,
        **meta,
    }

    execution_result = {
        "batch_id": "B1",
        "batch_domain": batch_cfg.get("batch_domain", "Governance docs stable placement"),
        "trace_rows": trace_rows,
        "operations_total": len(trace_rows),
        "operations_unchanged": unchanged_count,
        "operations_moved": 0,
        "operations_renamed": 0,
        "execution_aborted": execution_aborted,
        "abort_reasons": abort_reasons,
        "all_scoped_paths_pass": execution_completed,
        **meta,
    }

    after_manifest = {
        "manifest_id": "b1_after_manifest_v1",
        "batch_id": "B1",
        "entry_count": len(after_entries),
        "entries": after_entries,
        "generated_after_execution": execution_completed,
        **meta,
    }

    refactor_scan = {
        "scan_scope": [GOVERNANCE_ROOT],
        "extract_now_allowed": False,
        "extract_later_candidates": [{"tier": "A", "candidate": "governance_doc_index_helper"}],
        "blocked_from_runtime_refactor_now": True,
        "runtime_refactor_executed_now": False,
        "old_phase_deleted_now": False,
        "old_phase_deprecated_now": False,
        **meta,
    }

    summary = {
        "phase": PHASE_ID,
        "execution_scope": EXECUTION_SCOPE,
        "selected_batch_id": "B1",
        "batch_domain": batch_cfg.get("batch_domain"),
        "candidate_path_count": len(candidate_paths),
        "operations_unchanged": unchanged_count,
        "execution_aborted": execution_aborted,
        "boundary_ok": boundary_ok,
        "violations": blockers + abort_reasons,
        "final_decision": FINAL_DECISION if boundary_ok else "MAIN_PROJECT_STRUCTURE_MIGRATION_B1_CONTROLLED_EXECUTION_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        **meta,
    }

    return {
        "summary": summary,
        "b1_before_manifest": before_manifest,
        "b1_execution_result": execution_result,
        "b1_after_manifest": after_manifest,
        "b1_migration_refactor_opportunity_scan": refactor_scan,
    }
