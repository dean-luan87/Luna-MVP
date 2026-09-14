# -*- coding: utf-8 -*-
"""Main Project Structure Migration B0 Controlled Execution v1.

Controlled execution: first real B0 small-batch migration for Documentation Index /
README / phase table alignment. Only move/rename on declared candidate_paths; no delete/
overwrite/merge/copy; no _eval_out/protected/HR/DnAE; no runtime refactor.
"""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID

PHASE_ID = "Phase-Main-Project-Structure-Migration-B0-Controlled-Execution-v1-001"
EXECUTION_SCOPE = "main_project_structure_migration_b0_controlled_execution_only"
SOURCE_CHAIN = "main_project_structure_migration_b0_controlled_execution_v1"

FINAL_DECISION = "MAIN_PROJECT_STRUCTURE_MIGRATION_B0_CONTROLLED_EXECUTION_READY_FOR_POST_MIGRATION_REVIEW"
NEXT_PHASE = "Phase-Main-Project-Structure-Migration-B0-Post-Migration-Review-v1-001"

UPSTREAM_REQUIRED_PHASE = "Phase-Main-Project-Structure-Migration-B0-Preflight-Via-Harness-v1-001"
UPSTREAM_REQUIRED_FINAL = "MAIN_PROJECT_STRUCTURE_MIGRATION_B0_PREFLIGHT_VIA_HARNESS_READY_FOR_CONTROLLED_EXECUTION"
UPSTREAM_REQUIRED_NEXT = PHASE_ID

UPSTREAM_REQUIRED_ARTIFACTS: Tuple[str, ...] = (
    "summary.json",
    "verifier_report.json",
    "b0_batch_config_instance_v1.json",
    "b0_preflight_result_v1.json",
)

REQUIRED_CANDIDATE_PATHS: Tuple[str, ...] = (
    "docs/architecture/README.md",
    "docs/architecture/evaluation/README.md",
    "docs/architecture/evaluation/LUNA_EVALUATION_OCR_PHASE_VERDICT_STATUS_TABLE_V0.md",
)

FORBIDDEN_SCOPE_TOKENS: Tuple[str, ...] = (
    "capabilities/",
    "tools/",
    "configs/",
    "scripts/",
    "tests/",
    "_eval_out",
    "protected",
    "hr/",
    "dnae",
)

BLOCKED_OPS: Tuple[str, ...] = ("delete", "overwrite", "merge", "copy")
ALLOWED_OPS: Tuple[str, ...] = ("move", "rename", "unchanged")


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _boundary_meta(
    *,
    move_executed: bool = False,
    rename_executed: bool = False,
    execution_completed: bool = False,
) -> Dict[str, Any]:
    return {
        "b0_controlled_execution_only": True,
        "selected_batch_id": "B0",
        "b0_only": True,
        "b1_b7_deferred": True,
        "harness_contract_reused": True,
        "harness_extraction_reopened_now": False,
        "harness_adoption_reopened_now": False,
        "b0_execution_started_now": True,
        "batch_execution_started_now": True,
        "b0_execution_completed_now": execution_completed,
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
        "old_phase_deleted_now": False,
        "old_phase_deprecated_now": False,
        "verifier_rerun_executed_now": False,
        "rollback_rehearsal_executed_now": False,
        "post_migration_tests_executed_now": False,
        "file_operation_executed_now": move_executed or rename_executed,
        "real_migration_execution_allowed": True,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_path_mode": "repo_eval_out",
        "standard_eval_out_write_pending_on_local_repro": False,
        "runtime_invoked": False,
        "execution_committed": execution_completed,
        "authorization_granted_now": False,
        "owner_approval_granted_now": False,
        "operator_acknowledgement_granted_now": False,
        "batch_arming_allowed": False,
        "success_claim_allowed": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _row(**kwargs: Any) -> Dict[str, Any]:
    return {**kwargs}


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


def _path_forbidden(rel: str) -> bool:
    lower = rel.lower().replace("\\", "/")
    return any(t in lower for t in FORBIDDEN_SCOPE_TOKENS)


def _file_fingerprint(repo_root: Path, rel: str) -> Dict[str, Any]:
    p = repo_root / rel
    if not p.is_file():
        return {"path": rel, "exists": False}
    st = p.stat()
    digest = hashlib.sha256(p.read_bytes()).hexdigest()
    return {
        "path": rel,
        "exists": True,
        "size_bytes": st.st_size,
        "mtime_ns": st.st_mtime_ns,
        "sha256": digest,
    }


def _stable_placement_plan(candidate_paths: List[str]) -> List[Dict[str, Any]]:
    """B0 stable placement: files already at canonical paths; confirm unchanged."""
    rows: List[Dict[str, Any]] = []
    for rel in candidate_paths:
        rows.append(
            {
                "source_path": rel,
                "target_path": rel,
                "operation": "unchanged",
                "reason": "already_at_stable_b0_placement",
                "allowed": True,
            }
        )
    return rows


def run_main_project_structure_migration_b0_controlled_execution_v1(
    *,
    b0_preflight_via_harness_root: str,
    repo_root: Optional[str] = None,
) -> Dict[str, Any]:
    up = _load_upstream(b0_preflight_via_harness_root)
    blockers: List[str] = []
    abort_reasons: List[str] = []

    preflight_root = up["root"]
    source_path_mode = "workspace_fallback" if _is_workspace_fallback(preflight_root) else "repo_eval_out"
    standard_pending = source_path_mode == "workspace_fallback"

    resolved_repo = Path(repo_root).expanduser().resolve() if repo_root else Path(__file__).resolve().parents[2]

    if not up["loaded"]:
        blockers.append(f"preflight input incomplete: {up['missing']}")

    sm = up["artifacts"].get("summary.json") or {}
    vr = up["artifacts"].get("verifier_report.json") or {}
    batch_cfg = up["artifacts"].get("b0_batch_config_instance_v1.json") or {}
    preflight_result = up["artifacts"].get("b0_preflight_result_v1.json") or {}

    if vr.get("verifier") != "GO" or vr.get("passed") is not True:
        blockers.append("preflight verifier must be GO")
    if sm.get("phase") != UPSTREAM_REQUIRED_PHASE:
        blockers.append("preflight phase mismatch")
    if sm.get("final_decision") != UPSTREAM_REQUIRED_FINAL:
        blockers.append("preflight final_decision mismatch")
    if sm.get("recommended_next_phase") != UPSTREAM_REQUIRED_NEXT:
        blockers.append("preflight recommended_next_phase must be this execution phase")
    if sm.get("boundary_ok") is not True:
        blockers.append("preflight boundary_ok must be true")
    if sm.get("all_fixed_checks_pass") is not True:
        blockers.append("preflight all_fixed_checks_pass must be true")
    if sm.get("b0_preflight_executed_now") is not True:
        blockers.append("preflight b0_preflight_executed_now must be true")
    if preflight_result.get("extract_now_allowed") is not False:
        blockers.append("extract_now_allowed must be false")

    candidate_paths = list(batch_cfg.get("candidate_paths") or [])
    if set(candidate_paths) != set(REQUIRED_CANDIDATE_PATHS):
        blockers.append("candidate_paths must match B0 locked scope")

    allowed_ops = set(batch_cfg.get("allowed_operations") or [])
    blocked_ops = set(batch_cfg.get("blocked_operations") or [])
    if not {"move", "rename"}.issubset(allowed_ops):
        blockers.append("allowed_operations must include move and rename")
    if not {"delete", "overwrite", "merge", "copy"}.issubset(blocked_ops):
        blockers.append("blocked_operations incomplete")

    for rel in candidate_paths:
        if _path_forbidden(rel):
            abort_reasons.append(f"scope_escape: {rel}")
            blockers.append(f"forbidden scope: {rel}")

    # Build operation plan (stable placement = unchanged)
    operation_plan = _stable_placement_plan(candidate_paths)

    # before_manifest (must precede execution)
    before_entries: List[Dict[str, Any]] = []
    missing_paths: List[str] = []
    for rel in candidate_paths:
        fp = _file_fingerprint(resolved_repo, rel)
        before_entries.append(fp)
        if not fp.get("exists"):
            missing_paths.append(rel)
            abort_reasons.append(f"missing_candidate: {rel}")

    if missing_paths:
        blockers.append(f"candidate paths missing: {missing_paths}")

    move_executed = False
    rename_executed = False
    trace_rows: List[Dict[str, Any]] = []

    execution_aborted = bool(blockers)
    if not execution_aborted:
        for plan_row in operation_plan:
            rel = plan_row["source_path"]
            target = plan_row["target_path"]
            op = plan_row["operation"]
            src = resolved_repo / rel
            dst = resolved_repo / target

            if op not in ALLOWED_OPS:
                abort_reasons.append(f"operation_not_allowlisted: {op}")
                execution_aborted = True
                break
            if op in BLOCKED_OPS:
                abort_reasons.append(f"blocked_operation: {op}")
                execution_aborted = True
                break
            if _path_forbidden(rel) or _path_forbidden(target):
                abort_reasons.append(f"protected_or_forbidden_path: {rel}->{target}")
                execution_aborted = True
                break
            if not src.is_file():
                abort_reasons.append(f"missing_at_execution: {rel}")
                execution_aborted = True
                break

            if op == "unchanged":
                trace_rows.append(
                    {
                        "source_path": rel,
                        "target_path": target,
                        "operation": "unchanged",
                        "status": "completed",
                        "moved": False,
                        "renamed": False,
                        "skipped": False,
                        "deferred": False,
                        "detail": "stable placement confirmed; no path change required",
                    }
                )
            elif op == "move":
                if dst.exists() and dst.resolve() != src.resolve():
                    abort_reasons.append(f"overwrite_blocked: target exists {target}")
                    execution_aborted = True
                    break
                dst.parent.mkdir(parents=True, exist_ok=True)
                os.rename(str(src), str(dst))
                move_executed = True
                trace_rows.append(
                    {
                        "source_path": rel,
                        "target_path": target,
                        "operation": "move",
                        "status": "completed",
                        "moved": True,
                        "renamed": False,
                        "skipped": False,
                        "deferred": False,
                    }
                )
            elif op == "rename":
                if dst.exists() and dst.resolve() != src.resolve():
                    abort_reasons.append(f"overwrite_blocked: target exists {target}")
                    execution_aborted = True
                    break
                os.rename(str(src), str(dst))
                rename_executed = True
                trace_rows.append(
                    {
                        "source_path": rel,
                        "target_path": target,
                        "operation": "rename",
                        "status": "completed",
                        "moved": False,
                        "renamed": True,
                        "skipped": False,
                        "deferred": False,
                    }
                )

    execution_completed = not execution_aborted and len(trace_rows) == len(candidate_paths)
    meta = {
        **_boundary_meta(
            move_executed=move_executed,
            rename_executed=rename_executed,
            execution_completed=execution_completed,
        ),
        "source_path_mode": source_path_mode,
        "standard_eval_out_write_pending_on_local_repro": standard_pending,
    }

    # after_manifest (post execution)
    after_entries: List[Dict[str, Any]] = []
    if execution_completed:
        for rel in candidate_paths:
            after_entries.append(_file_fingerprint(resolved_repo, rel))

    boundary_ok = execution_completed and not blockers

    policy = _row(
        phase_id=PHASE_ID,
        execution_scope=EXECUTION_SCOPE,
        repo_root=str(resolved_repo),
        **meta,
    )

    preflight_review = {
        "preflight_root": str(preflight_root),
        "preflight_loaded": up["loaded"],
        "preflight_summary": {
            "phase": sm.get("phase"),
            "final_decision": sm.get("final_decision"),
            "all_fixed_checks_pass": sm.get("all_fixed_checks_pass"),
            "harness_contract_reused": sm.get("harness_contract_reused"),
        },
        "preflight_verifier": {"verifier": vr.get("verifier"), "passed": vr.get("passed")},
        "all_pass": up["loaded"] and vr.get("verifier") == "GO",
        "blockers": blockers,
        **meta,
    }

    before_manifest = _row(
        manifest_id="b0_before_manifest_v1",
        batch_id="B0",
        generated_before_execution=True,
        entries=before_entries,
        entry_count=len(before_entries),
        **meta,
    )

    operation_plan_doc = _row(
        batch_id="B0",
        operations=operation_plan,
        operation_count=len(operation_plan),
        allowed_operations=list(allowed_ops),
        blocked_operations=list(blocked_ops),
        content_rewrite_allowed=False,
        **meta,
    )

    operation_trace = _row(
        batch_id="B0",
        trace_rows=trace_rows,
        execution_aborted=execution_aborted,
        abort_reasons=abort_reasons,
        all_candidates_processed=execution_completed,
        **meta,
    )

    after_manifest = _row(
        manifest_id="b0_after_manifest_v1",
        batch_id="B0",
        generated_after_execution=execution_completed,
        entries=after_entries,
        entry_count=len(after_entries),
        **meta,
    )

    path_mapping = _row(
        batch_id="B0",
        mappings=[
            {
                "source_path": t["source_path"],
                "target_path": t["target_path"],
                "operation": t["operation"],
                "final_path": t["target_path"],
            }
            for t in trace_rows
        ],
        identity_mapping_all_unchanged=not move_executed and not rename_executed and execution_completed,
        **meta,
    )

    blocked_assertion = _row(
        batch_id="B0",
        blocked_operations=list(BLOCKED_OPS),
        delete_attempted=False,
        overwrite_attempted=False,
        merge_attempted=False,
        copy_attempted=False,
        all_blocked_ops_absent=True,
        **meta,
    )

    guard_result = {
        **meta,
        "batch_id": "B0",
        "eval_out_policy": batch_cfg.get("eval_out_policy"),
        "protected_path_policy": batch_cfg.get("protected_path_policy"),
        "guard_pass": execution_completed,
    }

    refactor_block = {
        **meta,
        "batch_id": "B0",
        "content_rewrite_executed": False,
        "refactor_block_pass": True,
    }

    abort_check = _row(
        batch_id="B0",
        abort_conditions=batch_cfg.get("abort_conditions"),
        abort_reasons=abort_reasons,
        execution_aborted=execution_aborted,
        abort_check_pass=not execution_aborted,
        **meta,
    )

    post_review_readiness = _row(
        final_decision=FINAL_DECISION if boundary_ok else "MAIN_PROJECT_STRUCTURE_MIGRATION_B0_CONTROLLED_EXECUTION_REQUIRES_FIXES",
        recommended_next_phase=NEXT_PHASE if boundary_ok else PHASE_ID,
        ready_for_post_migration_review=boundary_ok,
        **meta,
    )

    summary = {
        "phase": PHASE_ID,
        "execution_scope": EXECUTION_SCOPE,
        "selected_batch_id": "B0",
        "b0_only": True,
        "b1_b7_deferred": True,
        "repo_root": str(resolved_repo),
        "source_path_mode": source_path_mode,
        "standard_eval_out_write_pending_on_local_repro": standard_pending,
        "preflight_loaded": up["loaded"],
        "candidate_paths": candidate_paths,
        "operations_executed": len(trace_rows),
        "operations_unchanged": sum(1 for t in trace_rows if t.get("operation") == "unchanged"),
        "execution_aborted": execution_aborted,
        "boundary_ok": boundary_ok,
        "violations": blockers + abort_reasons,
        "final_decision": FINAL_DECISION if boundary_ok else "MAIN_PROJECT_STRUCTURE_MIGRATION_B0_CONTROLLED_EXECUTION_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        **meta,
    }

    return {
        "summary": summary,
        "b0_controlled_execution_policy": policy,
        "b0_preflight_input_review": preflight_review,
        "b0_before_manifest": before_manifest,
        "b0_execution_operation_plan": operation_plan_doc,
        "b0_execution_operation_trace": operation_trace,
        "b0_after_manifest": after_manifest,
        "b0_path_mapping_result": path_mapping,
        "b0_blocked_operation_assertion": blocked_assertion,
        "b0_protected_eval_out_guard_execution_result": guard_result,
        "b0_runtime_refactor_block_execution_result": refactor_block,
        "b0_execution_abort_check_result": abort_check,
        "b0_execution_readiness_for_post_migration_review": post_review_readiness,
    }
