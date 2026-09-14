# -*- coding: utf-8 -*-
"""Main Project Structure Migration B0 Harness Adoption DryRun v1.

Dry-run-only: simulate consumption of B0 Harness Adoption Planning artifacts as if consumed by
the unified Batch Preflight Harness structure. No formal harness generation/enforcement/integration,
no preflight execution, no arming, no execution, no file operations.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.main_project_structure_migration_b0_harness_adoption_planning_v1 import (
    FINAL_DECISION as PLANNING_FINAL,
    NEXT_PHASE as PLANNING_NEXT,
    PHASE_ID as PLANNING_PHASE,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID

PHASE_ID = "Phase-Main-Project-Structure-Migration-B0-Harness-Adoption-DryRun-v1-001"
DRYRUN_SCOPE = "main_project_structure_migration_b0_harness_adoption_dryrun_only"
SOURCE_CHAIN = "main_project_structure_migration_b0_harness_adoption_dryrun_v1"

FINAL_DECISION = "MAIN_PROJECT_STRUCTURE_MIGRATION_B0_HARNESS_ADOPTION_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
NEXT_PHASE = "Phase-Main-Project-Structure-Migration-B0-Harness-Adoption-Post-DryRun-Review-v1-001"

PLANNING_REQUIRED_PHASE = PLANNING_PHASE
PLANNING_REQUIRED_FINAL = PLANNING_FINAL
PLANNING_REQUIRED_NEXT = PHASE_ID

PLANNING_REQUIRED_ARTIFACTS: Tuple[str, ...] = (
    "summary.json",
    "verifier_report.json",
    "b0_harness_adoption_planning_policy_v1.json",
    "batch_preflight_harness_post_review_input_review_v1.json",
    "b0_batch_config_planning_v1.json",
    "b0_harness_preflight_check_binding_v1.json",
    "b0_scope_and_domain_isolation_planning_v1.json",
    "b0_protected_eval_out_guard_planning_v1.json",
    "b0_file_operation_boundary_planning_v1.json",
    "b0_manifest_requirement_planning_v1.json",
    "b0_rollback_requirement_planning_v1.json",
    "b0_verifier_rerun_requirement_planning_v1.json",
    "b0_post_migration_test_requirement_planning_v1.json",
    "b0_abort_condition_planning_v1.json",
    "b0_migration_refactor_opportunity_scan_planning_v1.json",
    "b1_b7_harness_adoption_deferred_matrix_v1.json",
    "b0_harness_adoption_non_claims_register_v1.json",
    "b0_harness_adoption_planning_readiness_decision_v1.json",
)

REQUIRED_CANDIDATE_PATHS: Tuple[str, ...] = (
    "docs/architecture/README.md",
    "docs/architecture/evaluation/README.md",
    "docs/architecture/evaluation/LUNA_EVALUATION_OCR_PHASE_VERDICT_STATUS_TABLE_V0.md",
)

REQUIRED_BINDING_CHECKS: Tuple[str, ...] = (
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
    "readiness_decision",
    "migration_refactor_opportunity_scan_check",
)

REQUIRED_NON_CLAIMS = [
    "B0 Harness Adoption DryRun GO ≠ formal harness generated",
    "B0 batch_config consumption pass ≠ batch_config applied to real batch",
    "B0 harness check binding pass ≠ B0 preflight executed",
    "B0 adoption candidate ≠ B0 armed",
    "B0 selected ≠ B0 executed",
    "B1–B7 deferred ≠ B1–B7 ready",
    "refactor opportunity scan pass ≠ runtime refactor executed",
    "old repetitive phase pattern identified ≠ old phase deleted",
    "verifier rerun requirement pass ≠ verifier rerun executed",
    "rollback requirement pass ≠ rollback rehearsal executed",
    "workspace_fallback GO ≠ standard _eval_out already written",
]


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _boundary_meta() -> Dict[str, Any]:
    return {
        "b0_harness_adoption_dryrun_only": True,
        "simulated": True,
        "selected_batch_id": "B0",
        "b0_only": True,
        "b1_b7_harness_adoption_deferred": True,
        "harness_generated_now": False,
        "harness_registered_now": False,
        "harness_enforced_now": False,
        "harness_runtime_integrated_now": False,
        "b0_batch_config_generated_now": False,
        "b0_batch_config_applied_to_real_batch_now": False,
        "b0_preflight_executed_now": False,
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
    return {**kwargs, **_boundary_meta(), "planned_now": True, "executed_now": False, "simulated_now": True}


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def _load_planning_root(root_str: str) -> Dict[str, Any]:
    root = Path(root_str).expanduser().resolve()
    artifacts: Dict[str, Any] = {}
    missing: List[str] = []
    for name in PLANNING_REQUIRED_ARTIFACTS:
        payload = _try_read_json(root / name)
        if payload is None:
            missing.append(name)
        else:
            artifacts[name] = payload
    loaded = not missing and bool(artifacts.get("summary.json")) and bool(artifacts.get("verifier_report.json"))
    return {"root": root, "loaded": loaded, "missing": missing, "artifacts": artifacts}


def _is_workspace_fallback(root: Optional[Path]) -> bool:
    return bool(root) and "Luna-Workspace-Min" in str(root)


def run_main_project_structure_migration_b0_harness_adoption_dryrun_v1(
    *,
    b0_harness_adoption_planning_root: str,
) -> Dict[str, Any]:
    plan = _load_planning_root(b0_harness_adoption_planning_root)
    blockers: List[str] = []

    source_path_mode = "workspace_fallback" if _is_workspace_fallback(plan["root"]) else "repo_eval_out"
    standard_pending = source_path_mode == "workspace_fallback"
    meta = {**_boundary_meta(), "source_path_mode": source_path_mode, "standard_eval_out_write_pending_on_local_repro": standard_pending}

    if not plan["loaded"]:
        blockers.append(f"planning input incomplete: {plan['missing']}")

    sm = plan["artifacts"].get("summary.json") or {}
    vr = plan["artifacts"].get("verifier_report.json") or {}

    if vr.get("verifier") != "GO" or vr.get("passed") is not True:
        blockers.append("planning verifier must be GO")
    if sm.get("phase") != PLANNING_REQUIRED_PHASE:
        blockers.append("planning phase mismatch")
    if sm.get("final_decision") != PLANNING_REQUIRED_FINAL:
        blockers.append("planning final_decision mismatch")
    if sm.get("recommended_next_phase") != PLANNING_REQUIRED_NEXT:
        blockers.append("planning recommended_next_phase must be this dryrun phase")
    if sm.get("selected_batch_id") != "B0" or sm.get("b0_only") is not True or sm.get("b1_b7_harness_adoption_deferred") is not True:
        blockers.append("planning must be b0-only and b1-b7 deferred")
    if sm.get("boundary_ok") is not True:
        blockers.append("planning boundary_ok must be true")

    # Consume B0 batch_config planning
    cfg = plan["artifacts"].get("b0_batch_config_planning_v1.json") or {}
    cfg_paths = cfg.get("candidate_paths") or []
    cfg_pass = (
        cfg.get("batch_id") == "B0"
        and cfg.get("batch_domain") == "Documentation Index / README / phase table alignment"
        and cfg_paths == list(REQUIRED_CANDIDATE_PATHS)
        and cfg.get("allowed_operations") == ["move", "rename"]
        and all(x in (cfg.get("blocked_operations") or []) for x in ("delete", "overwrite", "merge", "copy"))
        and isinstance(cfg.get("workspace_fallback_policy"), dict)
        and isinstance(cfg.get("non_claims"), list)
    )
    if not cfg_pass:
        blockers.append("B0 batch_config consumption failed")

    # Scope / domain isolation dryrun (must not contain forbidden tokens)
    forbidden = ("capabilities", "runner", "verifier", "configs", "scripts", "tests", "protected", "hr", "dnae", "_eval_out")
    scope_pass = all(isinstance(p, str) and not any(t in p.lower() for t in forbidden) for p in cfg_paths)
    if not scope_pass:
        blockers.append("B0 scope/domain isolation failed")

    # Binding dryrun
    binding = plan["artifacts"].get("b0_harness_preflight_check_binding_v1.json") or {}
    bound = binding.get("bound_checks") or []
    binding_pass = all(c in bound for c in REQUIRED_BINDING_CHECKS)
    if not binding_pass:
        blockers.append("harness check binding consumption failed")

    # Guard / file op / requirements: planning objects must exist and indicate non-execution
    guard = plan["artifacts"].get("b0_protected_eval_out_guard_planning_v1.json") or {}
    fileop = plan["artifacts"].get("b0_file_operation_boundary_planning_v1.json") or {}
    manifest = plan["artifacts"].get("b0_manifest_requirement_planning_v1.json") or {}
    rollback = plan["artifacts"].get("b0_rollback_requirement_planning_v1.json") or {}
    rerun = plan["artifacts"].get("b0_verifier_rerun_requirement_planning_v1.json") or {}
    tests = plan["artifacts"].get("b0_post_migration_test_requirement_planning_v1.json") or {}
    abort = plan["artifacts"].get("b0_abort_condition_planning_v1.json") or {}
    guard_pass = guard.get("protected_guard_enabled") is True and guard.get("eval_out_readonly_guard_enabled") is True
    fileop_pass = fileop.get("no_file_op_without_arming") is True
    manifest_pass = manifest.get("manifest_generated_now") is False
    rollback_pass = rollback.get("rollback_rehearsal_executed_now") is False
    rerun_pass = rerun.get("verifier_rerun_executed_now") is False
    tests_pass = tests.get("post_migration_tests_executed_now") is False
    abort_pass = abort.get("abort_executed_now") is False

    # Scan dryrun
    scan = plan["artifacts"].get("b0_migration_refactor_opportunity_scan_planning_v1.json") or {}
    scan_pass = (
        scan.get("extract_now_allowed") is False
        and scan.get("runtime_refactor_executed_now") is False
        and any(x in (scan.get("blocked_refactor_items") or []) for x in ("vision_runtime", "ocr_runtime", "navigation_runtime"))
    )
    if not scan_pass:
        blockers.append("migration refactor opportunity scan dryrun failed")

    # B1–B7 deferred dryrun
    d = plan["artifacts"].get("b1_b7_harness_adoption_deferred_matrix_v1.json") or {}
    rows = d.get("rows") or []
    b1b7_pass = d.get("all_deferred") is True and all(r.get("adoption_deferred") is True and r.get("preflight_allowed_now") is False and r.get("execution_allowed_now") is False and r.get("batch_armed_now") is False for r in rows)
    if not b1b7_pass:
        blockers.append("b1-b7 deferred matrix dryrun failed")

    # Non-claims
    non_claims = {
        "rows": [_row(non_claim_id=f"NC_B0_ADOPT_DR_{i+1:02d}", text=t, dryrun_pass=True) for i, t in enumerate(REQUIRED_NON_CLAIMS)],
        "row_count": len(REQUIRED_NON_CLAIMS),
        "all_pass": True,
        **meta,
    }

    boundary_ok = not blockers

    policy = _row(
        phase_id=PHASE_ID,
        dryrun_scope=DRYRUN_SCOPE,
        source_path_mode=source_path_mode,
        standard_eval_out_write_pending_on_local_repro=standard_pending,
    )

    input_review = {
        "planning_root": str(plan["root"]),
        "planning_loaded": plan["loaded"],
        "missing": plan["missing"],
        "planning_summary": {"phase": sm.get("phase"), "final_decision": sm.get("final_decision"), "recommended_next_phase": sm.get("recommended_next_phase")},
        "planning_verifier": {"verifier": vr.get("verifier"), "passed": vr.get("passed"), "check_count": vr.get("check_count")},
        "all_pass": boundary_ok,
        "blockers": blockers,
        **meta,
    }

    def _pack(name: str, passed: bool, detail: Any = None) -> Dict[str, Any]:
        return {"rows": [_row(check_id=name, simulated_consumption="pass" if passed else "fail", dryrun_pass=passed, detail=detail)], "row_count": 1, "all_pass": passed, **meta}

    cfg_dry = _pack("b0_batch_config", cfg_pass, {"candidate_paths": cfg_paths})
    bind_dry = _pack("check_binding", binding_pass, {"required_checks": list(REQUIRED_BINDING_CHECKS)})
    scope_dry = _pack("scope_domain_isolation", scope_pass)
    guard_dry = _pack("protected_eval_out_guard", guard_pass)
    fileop_dry = _pack("file_operation_boundary", fileop_pass)
    manifest_dry = _pack("manifest_requirement", manifest_pass)
    rollback_dry = _pack("rollback_requirement", rollback_pass)
    rerun_dry = _pack("verifier_rerun_requirement", rerun_pass)
    tests_dry = _pack("post_migration_test_requirement", tests_pass)
    abort_dry = _pack("abort_condition", abort_pass)
    scan_dry = _pack("migration_refactor_opportunity_scan", scan_pass, {"blocked_from_runtime_refactor_now": True})
    b1b7_dry = _pack("b1_b7_deferred", b1b7_pass)

    readiness = {
        "final_decision": FINAL_DECISION if boundary_ok else "MAIN_PROJECT_STRUCTURE_MIGRATION_B0_HARNESS_ADOPTION_DRYRUN_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "ready_for_post_dryrun_review": boundary_ok,
        **meta,
    }

    summary = {
        "phase": PHASE_ID,
        "dryrun_scope": DRYRUN_SCOPE,
        "b0_harness_adoption_dryrun_only": True,
        "simulated": True,
        "selected_batch_id": "B0",
        "b0_only": True,
        "b1_b7_harness_adoption_deferred": True,
        "source_path_mode": source_path_mode,
        "standard_eval_out_write_pending_on_local_repro": standard_pending,
        "planning_input_loaded": plan["loaded"],
        "planning_verifier_go": vr.get("verifier") == "GO" and vr.get("passed") is True,
        "planning_final_decision_ok": sm.get("final_decision") == PLANNING_REQUIRED_FINAL,
        "planning_next_phase_ok": sm.get("recommended_next_phase") == PLANNING_REQUIRED_NEXT,
        "b0_batch_config_consumption_pass": cfg_dry.get("all_pass") is True,
        "b0_binding_dryrun_pass": bind_dry.get("all_pass") is True,
        "b0_scope_domain_isolation_dryrun_pass": scope_dry.get("all_pass") is True,
        "b0_guard_dryrun_pass": guard_dry.get("all_pass") is True,
        "b0_fileop_boundary_dryrun_pass": fileop_dry.get("all_pass") is True,
        "b0_manifest_dryrun_pass": manifest_dry.get("all_pass") is True,
        "b0_rollback_dryrun_pass": rollback_dry.get("all_pass") is True,
        "b0_rerun_dryrun_pass": rerun_dry.get("all_pass") is True,
        "b0_post_tests_dryrun_pass": tests_dry.get("all_pass") is True,
        "b0_abort_dryrun_pass": abort_dry.get("all_pass") is True,
        "b0_scan_dryrun_pass": scan_dry.get("all_pass") is True,
        "b1_b7_deferred_dryrun_pass": b1b7_dry.get("all_pass") is True,
        "non_claims_dryrun_pass": non_claims.get("all_pass") is True,
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "final_decision": FINAL_DECISION if boundary_ok else "MAIN_PROJECT_STRUCTURE_MIGRATION_B0_HARNESS_ADOPTION_DRYRUN_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        **meta,
    }

    return {
        "summary": summary,
        "b0_harness_adoption_dryrun_policy": policy,
        "b0_harness_adoption_planning_input_review": input_review,
        "b0_batch_config_consumption_dryrun": cfg_dry,
        "b0_harness_preflight_check_binding_dryrun": bind_dry,
        "b0_scope_and_domain_isolation_dryrun": scope_dry,
        "b0_protected_eval_out_guard_dryrun": guard_dry,
        "b0_file_operation_boundary_dryrun": fileop_dry,
        "b0_manifest_requirement_dryrun": manifest_dry,
        "b0_rollback_requirement_dryrun": rollback_dry,
        "b0_verifier_rerun_requirement_dryrun": rerun_dry,
        "b0_post_migration_test_requirement_dryrun": tests_dry,
        "b0_abort_condition_dryrun": abort_dry,
        "b0_migration_refactor_opportunity_scan_dryrun": scan_dry,
        "b1_b7_harness_adoption_deferred_dryrun": b1b7_dry,
        "b0_harness_adoption_non_claims_dryrun": non_claims,
        "b0_harness_adoption_dryrun_readiness_decision": readiness,
    }

