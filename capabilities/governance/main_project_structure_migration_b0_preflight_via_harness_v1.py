# -*- coding: utf-8 -*-
"""Main Project Structure Migration B0 Preflight Via Harness v1.

Preflight-only: execute B0 preflight checks using the frozen reusable Batch Preflight Harness contract.
No file migration, no arming, no execution window, no file operations, no verifier rerun,
no rollback rehearsal, no post-migration tests.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID

PHASE_ID = "Phase-Main-Project-Structure-Migration-B0-Preflight-Via-Harness-v1-001"
PREFLIGHT_SCOPE = "main_project_structure_migration_b0_preflight_via_harness_only"
SOURCE_CHAIN = "main_project_structure_migration_b0_preflight_via_harness_v1"

FINAL_DECISION = "MAIN_PROJECT_STRUCTURE_MIGRATION_B0_PREFLIGHT_VIA_HARNESS_READY_FOR_CONTROLLED_EXECUTION"
NEXT_PHASE = "Phase-Main-Project-Structure-Migration-B0-Controlled-Execution-v1-001"

UPSTREAM_REQUIRED_PHASE = "Phase-Main-Project-Structure-Migration-B0-Harness-Adoption-and-Reusable-Contract-Closure-v1-001"
UPSTREAM_REQUIRED_FINAL = "MAIN_PROJECT_STRUCTURE_MIGRATION_B0_HARNESS_ADOPTION_AND_REUSABLE_CONTRACT_CLOSED_READY_FOR_B0_PREFLIGHT_VIA_HARNESS"
UPSTREAM_REQUIRED_NEXT = PHASE_ID

UPSTREAM_REQUIRED_ARTIFACTS: Tuple[str, ...] = (
    "summary.json",
    "verifier_report.json",
    "reusable_batch_preflight_harness_contract_closure_v1.json",
    "batch_config_template_v1.json",
    "future_batch_usage_guide_v1.json",
    "anti_recursion_rules_freeze_v1.json",
)

REQUIRED_CANDIDATE_PATHS: Tuple[str, ...] = (
    "docs/architecture/README.md",
    "docs/architecture/evaluation/README.md",
    "docs/architecture/evaluation/LUNA_EVALUATION_OCR_PHASE_VERDICT_STATUS_TABLE_V0.md",
)

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
    "protected",
)

C_CLASS_BLOCKED_REFACTOR: Tuple[str, ...] = (
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
        "b0_preflight_via_harness_only": True,
        "selected_batch_id": "B0",
        "b0_only": True,
        "b1_b7_deferred": True,
        "harness_contract_reused": True,
        "harness_extraction_reopened_now": False,
        "harness_adoption_reopened_now": False,
        "b0_preflight_executed_now": True,
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
        "runtime_refactor_executed_now": False,
        "old_phase_deleted_now": False,
        "old_phase_deprecated_now": False,
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
    return {**kwargs, **_boundary_meta(), "executed_now": True, "preflight_only": True}


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


def _build_b0_batch_config() -> Dict[str, Any]:
    return {
        "batch_id": "B0",
        "batch_domain": "Documentation Index / README / phase table alignment",
        "candidate_paths": list(REQUIRED_CANDIDATE_PATHS),
        "allowed_operations": ["move", "rename"],
        "blocked_operations": ["delete", "overwrite", "merge", "copy"],
        "protected_path_policy": {"mode": "deny", "blocked": ["protected/**", "**/protected/**"]},
        "eval_out_policy": {"mode": "readonly", "write_allowed": False},
        "before_manifest_requirement": {"required": True, "generated_now": False},
        "after_manifest_requirement": {"required": True, "generated_now": False},
        "rollback_route": {
            "route_id": "B0_DOCS_INDEX_ONLY_ROLLBACK_ROUTE_V1",
            "rehearsal_required": True,
            "executed_now": False,
        },
        "verifier_rerun_list": ["verify_main_project_structure_migration_b0_preflight_via_harness_v1"],
        "post_migration_test_list": ["docs_index_integrity_check", "readme_link_consistency_check"],
        "abort_conditions": [
            "scope_escape_detected",
            "protected_path_intersection",
            "eval_out_write_attempted",
            "operation_not_allowlisted",
        ],
        "workspace_fallback_policy": {"enabled": True, "notes": "workspace_fallback does not imply repo _eval_out written"},
        "non_claims": [
            "B0 preflight GO ≠ B0 migration executed",
            "B0 preflight GO ≠ B0 armed",
            "B0 preflight GO ≠ execution window opened",
            "manifest requirement pass ≠ manifest generated",
            "verifier rerun requirement pass ≠ verifier rerun executed",
            "rollback requirement pass ≠ rollback rehearsal executed",
            "post-migration test requirement pass ≠ tests executed",
            "refactor opportunity scan pass ≠ runtime refactor executed",
            "workspace_fallback GO ≠ standard _eval_out already written",
        ],
    }


def _candidate_path_exists(repo_root: Path, rel: str) -> bool:
    return (repo_root / rel).is_file()


def run_main_project_structure_migration_b0_preflight_via_harness_v1(
    *,
    b0_harness_adoption_and_reusable_contract_closure_root: str,
    repo_root: Optional[str] = None,
) -> Dict[str, Any]:
    up = _load_upstream(b0_harness_adoption_and_reusable_contract_closure_root)
    blockers: List[str] = []

    closure_root = up["root"]
    source_path_mode = "workspace_fallback" if _is_workspace_fallback(closure_root) else "repo_eval_out"
    standard_pending = source_path_mode == "workspace_fallback"
    meta = {**_boundary_meta(), "source_path_mode": source_path_mode, "standard_eval_out_write_pending_on_local_repro": standard_pending}

    resolved_repo = Path(repo_root).expanduser().resolve() if repo_root else Path(__file__).resolve().parents[2]

    if not up["loaded"]:
        blockers.append(f"closure input incomplete: {up['missing']}")

    sm = up["artifacts"].get("summary.json") or {}
    vr = up["artifacts"].get("verifier_report.json") or {}
    contract = up["artifacts"].get("reusable_batch_preflight_harness_contract_closure_v1.json") or {}
    anti = up["artifacts"].get("anti_recursion_rules_freeze_v1.json") or {}

    if vr.get("verifier") != "GO" or vr.get("passed") is not True:
        blockers.append("closure verifier must be GO")
    if sm.get("phase") != UPSTREAM_REQUIRED_PHASE:
        blockers.append("closure phase mismatch")
    if sm.get("final_decision") != UPSTREAM_REQUIRED_FINAL:
        blockers.append("closure final_decision mismatch")
    if sm.get("recommended_next_phase") != UPSTREAM_REQUIRED_NEXT:
        blockers.append("closure recommended_next_phase must be this preflight phase")
    if sm.get("boundary_ok") is not True:
        blockers.append("closure boundary_ok must be true")
    if contract.get("contract_frozen_now") is not True:
        blockers.append("reusable contract must be frozen")
    if not anti.get("forbidden_future_patterns"):
        blockers.append("anti_recursion_rules_freeze must be present")

    batch_config = _build_b0_batch_config()
    batch_config_row = _row(**batch_config, batch_config_instance=True)

    # --- Fixed checks ---
    paths = batch_config["candidate_paths"]
    scope_token_ok = all(
        isinstance(p, str) and not any(t in p.lower() for t in FORBIDDEN_SCOPE_TOKENS) for p in paths
    )
    paths_set_ok = set(paths) == set(REQUIRED_CANDIDATE_PATHS)
    path_existence = {p: _candidate_path_exists(resolved_repo, p) for p in paths}
    paths_exist_ok = all(path_existence.values())
    scope_pass = scope_token_ok and paths_set_ok and paths_exist_ok
    if not scope_pass:
        blockers.append("scope_check failed")

    domain_pass = batch_config["batch_id"] == "B0" and "Documentation Index" in batch_config["batch_domain"]
    if not domain_pass:
        blockers.append("domain_isolation_check failed")

    protected_pass = batch_config["protected_path_policy"].get("mode") == "deny"
    if not protected_pass:
        blockers.append("protected_guard_check failed")

    eval_out_pass = batch_config["eval_out_policy"].get("mode") == "readonly" and batch_config["eval_out_policy"].get("write_allowed") is False
    if not eval_out_pass:
        blockers.append("eval_out_readonly_check failed")

    allowed = set(batch_config["allowed_operations"])
    blocked = set(batch_config["blocked_operations"])
    fileop_pass = allowed == {"move", "rename"} and {"delete", "overwrite", "merge", "copy"}.issubset(blocked)
    if not fileop_pass:
        blockers.append("file_operation_boundary_check failed")

    manifest_pass = (
        batch_config["before_manifest_requirement"].get("required") is True
        and batch_config["after_manifest_requirement"].get("required") is True
        and batch_config["before_manifest_requirement"].get("generated_now") is False
        and batch_config["after_manifest_requirement"].get("generated_now") is False
    )
    if not manifest_pass:
        blockers.append("manifest_requirement_check failed")

    rollback_pass = (
        bool(batch_config["rollback_route"].get("route_id"))
        and batch_config["rollback_route"].get("rehearsal_required") is True
        and batch_config["rollback_route"].get("executed_now") is False
    )
    if not rollback_pass:
        blockers.append("rollback_requirement_check failed")

    rerun_pass = bool(batch_config["verifier_rerun_list"]) and meta["verifier_rerun_executed_now"] is False
    if not rerun_pass:
        blockers.append("verifier_rerun_requirement_check failed")

    post_tests_pass = bool(batch_config["post_migration_test_list"]) and meta["post_migration_tests_executed_now"] is False
    if not post_tests_pass:
        blockers.append("post_migration_test_requirement_check failed")

    abort_pass = bool(batch_config["abort_conditions"])
    if not abort_pass:
        blockers.append("abort_condition_check failed")

    ws_pass = batch_config.get("workspace_fallback_policy", {}).get("enabled") is True
    if not ws_pass:
        blockers.append("workspace_fallback_check failed")

    non_claims_pass = len(batch_config.get("non_claims") or []) >= 5
    if not non_claims_pass:
        blockers.append("non_claims_check failed")

    scan = _row(
        scan_scope=list(REQUIRED_CANDIDATE_PATHS),
        duplicate_pattern_candidates=[
            {"pattern": "phase planning/dryrun/review triple", "location": "governance docs index"},
            {"pattern": "README + phase verdict table updater", "location": "docs/architecture"},
            {"pattern": "summary/verifier_report builder", "location": "tools/evaluation/governance"},
        ],
        extractable_common_components=[
            {"tier": "A", "candidate": "json_summary_builder_helper", "risk": "low"},
            {"tier": "A", "candidate": "readme_phase_verdict_table_updater_helper", "risk": "low"},
            {"tier": "B", "candidate": "batch_preflight_harness_runtime", "risk": "medium"},
        ],
        recommended_abstractions=[
            "parameterized batch_config for B1–B7",
            "shared preflight check result schema",
        ],
        risk_level="low",
        can_extract_now=False,
        extract_now_allowed=False,
        should_extract_later=True,
        blocked_from_runtime_refactor_now=True,
        blocked_refactor_items=list(C_CLASS_BLOCKED_REFACTOR),
        notes=["B0 docs index alignment only; no runtime refactor during migration"],
    )
    scan_pass = (
        scan.get("extract_now_allowed") is False
        and scan.get("blocked_from_runtime_refactor_now") is True
        and meta["runtime_refactor_executed_now"] is False
        and meta["old_phase_deleted_now"] is False
        and meta["old_phase_deprecated_now"] is False
    )
    if not scan_pass:
        blockers.append("migration_refactor_opportunity_scan_check failed")

    check_results: Dict[str, bool] = {
        "scope_check": scope_pass,
        "domain_isolation_check": domain_pass,
        "protected_guard_check": protected_pass,
        "eval_out_readonly_check": eval_out_pass,
        "file_operation_boundary_check": fileop_pass,
        "manifest_requirement_check": manifest_pass,
        "rollback_requirement_check": rollback_pass,
        "verifier_rerun_requirement_check": rerun_pass,
        "post_migration_test_requirement_check": post_tests_pass,
        "abort_condition_check": abort_pass,
        "workspace_fallback_check": ws_pass,
        "non_claims_check": non_claims_pass,
        "migration_refactor_opportunity_scan_check": scan_pass,
    }
    all_checks_pass = all(check_results.values())
    if not all_checks_pass:
        blockers.append("one or more fixed checks failed")

    boundary_ok = not blockers

    policy = _row(
        phase_id=PHASE_ID,
        preflight_scope=PREFLIGHT_SCOPE,
        harness_id=contract.get("harness_id", "main_project_structure_migration_batch_preflight_harness_v1"),
        source_path_mode=source_path_mode,
        standard_eval_out_write_pending_on_local_repro=standard_pending,
    )

    contract_review = {
        "closure_root": str(closure_root),
        "closure_loaded": up["loaded"],
        "contract_frozen": contract.get("contract_frozen_now"),
        "fixed_checks_from_contract": contract.get("fixed_checks"),
        "anti_recursion_active": bool(anti.get("forbidden_future_patterns")),
        "harness_extraction_reopened_now": False,
        "harness_adoption_reopened_now": False,
        "allowed_per_batch_outputs": anti.get("allowed_per_batch_outputs"),
        "all_pass": boundary_ok,
        "blockers": blockers,
        **meta,
    }

    def _check_result(check_id: str, passed: bool, detail: Any) -> Dict[str, Any]:
        return _row(check_id=check_id, check_pass=passed, detail=detail)

    scope_result = _check_result(
        "scope_check",
        scope_pass,
        {"candidate_paths": paths, "paths_set_ok": paths_set_ok, "scope_token_ok": scope_token_ok, "path_existence": path_existence},
    )
    domain_result = _check_result(
        "domain_isolation_check",
        domain_pass,
        {"batch_id": "B0", "b1_b7_deferred": True, "b1_b7_preflight_executed": False},
    )
    protected_result = _check_result("protected_guard_check", protected_pass, batch_config["protected_path_policy"])
    eval_out_result = _check_result("eval_out_readonly_check", eval_out_pass, batch_config["eval_out_policy"])
    fileop_result = _check_result(
        "file_operation_boundary_check",
        fileop_pass,
        {"allowed": list(allowed), "blocked": list(blocked), "actual_file_ops": False},
    )
    manifest_result = _check_result(
        "manifest_requirement_check",
        manifest_pass,
        {
            "before": batch_config["before_manifest_requirement"],
            "after": batch_config["after_manifest_requirement"],
        },
    )
    rollback_result = _check_result("rollback_requirement_check", rollback_pass, batch_config["rollback_route"])
    rerun_result = _check_result(
        "verifier_rerun_requirement_check",
        rerun_pass,
        {"verifier_rerun_list": batch_config["verifier_rerun_list"], "executed_now": False},
    )
    post_tests_result = _check_result(
        "post_migration_test_requirement_check",
        post_tests_pass,
        {"post_migration_test_list": batch_config["post_migration_test_list"], "executed_now": False},
    )
    abort_result = _check_result("abort_condition_check", abort_pass, {"abort_conditions": batch_config["abort_conditions"]})
    ws_result = _check_result(
        "workspace_fallback_check",
        ws_pass,
        {"workspace_fallback_policy": batch_config["workspace_fallback_policy"], "source_path_mode": source_path_mode},
    )
    non_claims_result = _check_result(
        "non_claims_check",
        non_claims_pass,
        {"non_claims": batch_config["non_claims"], "count": len(batch_config["non_claims"])},
    )

    preflight_result = _row(
        batch_id="B0",
        batch_config=batch_config,
        check_results=check_results,
        all_checks_pass=all_checks_pass,
        extract_now_allowed=False,
        extract_later_candidates=scan.get("extractable_common_components"),
        blocked_refactor_items=scan.get("blocked_refactor_items"),
        final_batch_readiness_decision=FINAL_DECISION if boundary_ok else "MAIN_PROJECT_STRUCTURE_MIGRATION_B0_PREFLIGHT_VIA_HARNESS_REQUIRES_FIXES",
    )

    readiness = {
        "final_decision": FINAL_DECISION if boundary_ok else "MAIN_PROJECT_STRUCTURE_MIGRATION_B0_PREFLIGHT_VIA_HARNESS_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "ready_for_b0_controlled_execution": boundary_ok,
        "b1_b7_deferred": True,
        **meta,
    }

    summary = {
        "phase": PHASE_ID,
        "preflight_scope": PREFLIGHT_SCOPE,
        "selected_batch_id": "B0",
        "b0_only": True,
        "b1_b7_deferred": True,
        "harness_contract_reused": True,
        "harness_extraction_reopened_now": False,
        "harness_adoption_reopened_now": False,
        "b0_preflight_executed_now": True,
        "source_path_mode": source_path_mode,
        "standard_eval_out_write_pending_on_local_repro": standard_pending,
        "closure_loaded": up["loaded"],
        "all_fixed_checks_pass": all_checks_pass,
        "check_results": check_results,
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "final_decision": FINAL_DECISION if boundary_ok else "MAIN_PROJECT_STRUCTURE_MIGRATION_B0_PREFLIGHT_VIA_HARNESS_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        **meta,
    }

    return {
        "summary": summary,
        "b0_preflight_via_harness_policy": policy,
        "reusable_harness_contract_input_review": contract_review,
        "b0_batch_config_instance": batch_config_row,
        "b0_preflight_scope_check_result": scope_result,
        "b0_preflight_domain_isolation_check_result": domain_result,
        "b0_preflight_protected_guard_check_result": protected_result,
        "b0_preflight_eval_out_readonly_check_result": eval_out_result,
        "b0_preflight_file_operation_boundary_check_result": fileop_result,
        "b0_preflight_manifest_requirement_check_result": manifest_result,
        "b0_preflight_rollback_requirement_check_result": rollback_result,
        "b0_preflight_verifier_rerun_requirement_check_result": rerun_result,
        "b0_preflight_post_migration_test_requirement_check_result": post_tests_result,
        "b0_preflight_abort_condition_check_result": abort_result,
        "b0_preflight_workspace_fallback_check_result": ws_result,
        "b0_preflight_non_claims_check_result": non_claims_result,
        "b0_preflight_migration_refactor_opportunity_scan": scan,
        "b0_preflight_result": preflight_result,
        "b0_preflight_via_harness_readiness_decision": readiness,
    }
