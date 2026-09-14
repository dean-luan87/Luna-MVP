# -*- coding: utf-8 -*-
"""Main Project Structure Migration B1 Preflight Via Harness v1.

Compressed preflight-only: reuse frozen Batch Preflight Harness contract for B1.
No Harness Extraction/Adoption/Arming/Request chains. Outputs 4 artifacts + summary.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID

PHASE_ID = "Phase-Main-Project-Structure-Migration-B1-Preflight-Via-Harness-v1-001"
PREFLIGHT_SCOPE = "main_project_structure_migration_b1_preflight_via_harness_only"
SOURCE_CHAIN = "main_project_structure_migration_b1_preflight_via_harness_v1"

FINAL_DECISION = "MAIN_PROJECT_STRUCTURE_MIGRATION_B1_PREFLIGHT_VIA_HARNESS_READY_FOR_CONTROLLED_EXECUTION"
NEXT_PHASE = "Phase-Main-Project-Structure-Migration-B1-Controlled-Execution-v1-001"

UPSTREAM_REQUIRED_PHASE = "Phase-Main-Project-Structure-Migration-B0-Post-Migration-Review-v1-001"
UPSTREAM_REQUIRED_FINAL = "MAIN_PROJECT_STRUCTURE_MIGRATION_B0_POST_MIGRATION_REVIEW_CLOSED_READY_FOR_B1_PREFLIGHT_VIA_HARNESS"
UPSTREAM_REQUIRED_NEXT = PHASE_ID

BATCH_ID = "B1"
BATCH_DOMAIN = "Governance docs stable placement"
GOVERNANCE_ROOT = "docs/architecture/governance"

REQUIRED_FIXED_CHECKS: Tuple[str, ...] = (
    "scope_check",
    "domain_isolation_check",
    "protected_guard_check",
    "eval_out_readonly_check",
    "file_operation_boundary_check",
    "manifest_requirement_check",
    "rollback_requirement_check",
    "verifier_rerun_requirement_check",
    "post_migration_test_requirement_check",
    "abort_condition_check",
    "workspace_fallback_check",
    "non_claims_check",
    "migration_refactor_opportunity_scan_check",
    "readiness_decision",
)

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

C_CLASS_BLOCKED: Tuple[str, ...] = (
    "vision_runtime",
    "ocr_runtime",
    "navigation_runtime",
    "voice_runtime",
    "task_midplatform_runtime",
    "memory_world_model_fact_write_path",
    "verifier_enforcement_semantics",
)


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _boundary_meta() -> Dict[str, Any]:
    return {
        "b1_preflight_via_harness_only": True,
        "selected_batch_id": BATCH_ID,
        "b1_only": True,
        "b0_closed": True,
        "b2_b7_deferred": True,
        "harness_contract_reused": True,
        "harness_extraction_reopened_now": False,
        "harness_adoption_reopened_now": False,
        "arming_chain_reopened_now": False,
        "request_chain_reopened_now": False,
        "b1_preflight_executed_now": True,
        "batch_execution_started_now": False,
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
        "runtime_refactor_executed_now": False,
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


def scan_governance_candidate_paths(repo_root: Path) -> List[str]:
    gov_dir = repo_root / GOVERNANCE_ROOT
    if not gov_dir.is_dir():
        return []
    return sorted(
        str(p.relative_to(repo_root)).replace("\\", "/")
        for p in gov_dir.rglob("*.md")
        if p.is_file()
    )


def _build_batch_config(candidate_paths: List[str]) -> Dict[str, Any]:
    return {
        "batch_id": BATCH_ID,
        "batch_domain": BATCH_DOMAIN,
        "candidate_paths": candidate_paths,
        "allowed_operations": ["move", "rename"],
        "blocked_operations": ["delete", "overwrite", "merge", "copy"],
        "protected_path_policy": {"mode": "deny", "blocked": ["protected/**", "**/protected/**"]},
        "eval_out_policy": {"mode": "readonly", "write_allowed": False},
        "before_manifest_requirement": {"required": True, "generated_now": False},
        "after_manifest_requirement": {"required": True, "generated_now": False},
        "rollback_route": {"route_id": "B1_GOVERNANCE_DOCS_ROLLBACK_ROUTE_V1", "rehearsal_required": True},
        "verifier_rerun_list": ["verify_main_project_structure_migration_b1_preflight_via_harness_v1"],
        "post_migration_test_list": ["governance_doc_path_check"],
        "abort_conditions": [
            "scope_escape_detected",
            "protected_path_intersection",
            "eval_out_write_attempted",
            "operation_not_allowlisted",
        ],
        "workspace_fallback_policy": {"enabled": True},
        "non_claims": [
            "B1 preflight GO ≠ B1 migration executed",
            "B1 preflight GO ≠ arming/request chain reopened",
            "manifest requirement pass ≠ manifest generated",
            "refactor scan pass ≠ runtime refactor executed",
            "workspace_fallback GO ≠ standard _eval_out already written",
        ],
    }


def run_main_project_structure_migration_b1_preflight_via_harness_v1(
    *,
    b0_post_migration_review_root: str,
    repo_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []
    review_root = Path(b0_post_migration_review_root).expanduser().resolve()
    resolved_repo = Path(repo_root).expanduser().resolve() if repo_root else Path(__file__).resolve().parents[2]

    source_path_mode = "workspace_fallback" if _is_workspace_fallback(review_root) else "repo_eval_out"
    standard_pending = source_path_mode == "workspace_fallback"
    meta = {**_boundary_meta(), "source_path_mode": source_path_mode, "standard_eval_out_write_pending_on_local_repro": standard_pending}

    sm = _try_read_json(review_root / "summary.json") or {}
    vr = _try_read_json(review_root / "verifier_report.json") or {}

    if vr.get("verifier") != "GO" or vr.get("passed") is not True:
        blockers.append("B0 post-migration review verifier must be GO")
    if sm.get("phase") != UPSTREAM_REQUIRED_PHASE:
        blockers.append("upstream phase mismatch")
    if sm.get("final_decision") != UPSTREAM_REQUIRED_FINAL:
        blockers.append("upstream final_decision mismatch")
    if sm.get("recommended_next_phase") != UPSTREAM_REQUIRED_NEXT:
        blockers.append("upstream recommended_next_phase must be B1 preflight")
    if sm.get("boundary_ok") is not True:
        blockers.append("upstream boundary_ok must be true")
    if sm.get("b0_closed_now") is not True:
        blockers.append("b0_closed_now must be true")
    if sm.get("ready_for_b1_preflight_via_harness") is not True:
        blockers.append("ready_for_b1_preflight_via_harness must be true")

    candidate_paths = scan_governance_candidate_paths(resolved_repo)
    if not candidate_paths:
        blockers.append("no governance candidate paths found")

    batch_config = _build_batch_config(candidate_paths)

    # Fixed checks
    scope_ok = all(
        p.startswith(f"{GOVERNANCE_ROOT}/") and p.endswith(".md") and not any(t in p.lower() for t in FORBIDDEN_SCOPE_TOKENS)
        for p in candidate_paths
    )
    domain_ok = batch_config["batch_id"] == BATCH_ID and batch_config["batch_domain"] == BATCH_DOMAIN
    protected_ok = batch_config["protected_path_policy"].get("mode") == "deny"
    eval_out_ok = batch_config["eval_out_policy"].get("mode") == "readonly"
    fileop_ok = set(batch_config["allowed_operations"]) == {"move", "rename"} and {"delete", "overwrite", "merge", "copy"}.issubset(
        set(batch_config["blocked_operations"])
    )
    manifest_ok = batch_config["before_manifest_requirement"]["required"] and batch_config["after_manifest_requirement"]["required"]
    rollback_ok = bool(batch_config["rollback_route"].get("route_id"))
    rerun_ok = bool(batch_config["verifier_rerun_list"])
    post_ok = bool(batch_config["post_migration_test_list"])
    abort_ok = bool(batch_config["abort_conditions"])
    ws_ok = batch_config["workspace_fallback_policy"].get("enabled") is True
    non_claims_ok = len(batch_config["non_claims"]) >= 3

    path_existence = {p: (resolved_repo / p).is_file() for p in candidate_paths}
    exists_ok = all(path_existence.values())
    if not exists_ok:
        blockers.append("some candidate paths missing on disk")

    scan = {
        "scan_scope": [GOVERNANCE_ROOT],
        "duplicate_pattern_candidates": [
            {"pattern": "governance LUNA_* triple docs", "location": GOVERNANCE_ROOT},
            {"pattern": "README/index crosslink updater", "location": "docs/architecture"},
        ],
        "extractable_common_components": [
            {"tier": "A", "candidate": "governance_doc_index_helper", "risk": "low"},
            {"tier": "B", "candidate": "batch_preflight_harness_runtime", "risk": "medium"},
        ],
        "extract_now_allowed": False,
        "extract_later_candidates": [{"tier": "A", "candidate": "governance_doc_index_helper"}],
        "blocked_from_runtime_refactor_now": True,
        "blocked_refactor_items": list(C_CLASS_BLOCKED),
        **meta,
    }
    scan_ok = scan["extract_now_allowed"] is False and scan["blocked_from_runtime_refactor_now"] is True

    check_results = {
        "scope_check": scope_ok and exists_ok,
        "domain_isolation_check": domain_ok,
        "protected_guard_check": protected_ok,
        "eval_out_readonly_check": eval_out_ok,
        "file_operation_boundary_check": fileop_ok,
        "manifest_requirement_check": manifest_ok,
        "rollback_requirement_check": rollback_ok,
        "verifier_rerun_requirement_check": rerun_ok,
        "post_migration_test_requirement_check": post_ok,
        "abort_condition_check": abort_ok,
        "workspace_fallback_check": ws_ok,
        "non_claims_check": non_claims_ok,
        "migration_refactor_opportunity_scan_check": scan_ok,
    }
    all_checks_pass = all(check_results.values()) and not blockers
    if not all_checks_pass and not blockers:
        blockers.append("one or more fixed checks failed")

    boundary_ok = not blockers

    preflight_result = {
        "batch_id": BATCH_ID,
        "batch_config": batch_config,
        "check_results": check_results,
        "all_checks_pass": all_checks_pass,
        "candidate_path_count": len(candidate_paths),
        "path_existence": path_existence,
        "final_batch_readiness_decision": FINAL_DECISION if boundary_ok else "MAIN_PROJECT_STRUCTURE_MIGRATION_B1_PREFLIGHT_REQUIRES_FIXES",
        **meta,
    }

    readiness = {
        "final_decision": FINAL_DECISION if boundary_ok else "MAIN_PROJECT_STRUCTURE_MIGRATION_B1_PREFLIGHT_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "ready_for_b1_controlled_execution": boundary_ok,
        **meta,
    }

    summary = {
        "phase": PHASE_ID,
        "preflight_scope": PREFLIGHT_SCOPE,
        "selected_batch_id": BATCH_ID,
        "batch_domain": BATCH_DOMAIN,
        "candidate_path_count": len(candidate_paths),
        "all_fixed_checks_pass": all_checks_pass,
        "check_results": check_results,
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "final_decision": readiness["final_decision"],
        "recommended_next_phase": readiness["recommended_next_phase"],
        **meta,
    }

    return {
        "summary": summary,
        "b1_batch_config": batch_config,
        "b1_preflight_result": preflight_result,
        "b1_migration_refactor_opportunity_scan": scan,
        "b1_preflight_readiness_decision": readiness,
    }
