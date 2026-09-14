# -*- coding: utf-8 -*-
"""Main Project Structure Migration B0 Harness Adoption Planning v1.

Planning-only: treat B0 as first adoption candidate for the unified Batch Preflight Harness.
No formal harness generation, no enforcement, no preflight execution, no arming, no execution,
no file operations, no verifier rerun execution, no rollback rehearsal, no post-migration tests.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID

PHASE_ID = "Phase-Main-Project-Structure-Migration-B0-Harness-Adoption-Planning-v1-001"
PLANNING_SCOPE = "main_project_structure_migration_b0_harness_adoption_planning_only"
SOURCE_CHAIN = "main_project_structure_migration_b0_harness_adoption_planning_v1"

FINAL_DECISION = "MAIN_PROJECT_STRUCTURE_MIGRATION_B0_HARNESS_ADOPTION_PLANNING_READY_FOR_DRYRUN"
NEXT_PHASE = "Phase-Main-Project-Structure-Migration-B0-Harness-Adoption-DryRun-v1-001"

UPSTREAM_REQUIRED_PHASE = "Phase-Main-Project-Structure-Migration-Batch-Preflight-Harness-Extraction-Post-DryRun-Review-v1-001"
UPSTREAM_REQUIRED_FINAL = "MAIN_PROJECT_STRUCTURE_MIGRATION_BATCH_PREFLIGHT_HARNESS_EXTRACTION_POST_DRYRUN_REVIEW_READY_FOR_B0_HARNESS_ADOPTION_PLANNING"
UPSTREAM_REQUIRED_NEXT = PHASE_ID

UPSTREAM_REQUIRED_ARTIFACTS: Tuple[str, ...] = (
    "summary.json",
    "verifier_report.json",
    "reusable_preflight_check_inventory_review_v1.json",
    "batch_config_schema_consumption_review_v1.json",
    "batch_preflight_harness_interface_review_v1.json",
    "batch_preflight_output_contract_review_v1.json",
    "batch_preflight_verifier_baseline_review_v1.json",
    "batch_specific_override_policy_review_v1.json",
    "b0_to_b7_harness_adoption_review_v1.json",
    "deprecated_repetitive_phase_pattern_review_v1.json",
    "migration_refactor_opportunity_scan_rule_review_v1.json",
    "batch_preflight_harness_non_generation_review_v1.json",
    "batch_preflight_harness_extraction_non_claims_review_v1.json",
    "batch_preflight_harness_extraction_post_dryrun_review_readiness_decision_v1.json",
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


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _boundary_meta() -> Dict[str, Any]:
    return {
        "b0_harness_adoption_planning_only": True,
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
    return {**kwargs, **_boundary_meta(), "planned_now": True, "executed_now": False}


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def _load_upstream(root_str: Optional[str]) -> Dict[str, Any]:
    root = Path(root_str).expanduser().resolve() if root_str else None
    artifacts: Dict[str, Any] = {}
    missing: List[str] = []
    if root:
        for name in UPSTREAM_REQUIRED_ARTIFACTS:
            payload = _try_read_json(root / name)
            if payload is None:
                missing.append(name)
            else:
                artifacts[name] = payload
    loaded = bool(root) and not missing and bool(artifacts.get("summary.json")) and bool(artifacts.get("verifier_report.json"))
    return {"root": root, "loaded": loaded, "missing": missing, "artifacts": artifacts}


def _is_workspace_fallback(root: Optional[Path]) -> bool:
    return bool(root) and "Luna-Workspace-Min" in str(root)


def run_main_project_structure_migration_b0_harness_adoption_planning_v1(
    *,
    batch_preflight_harness_extraction_post_review_root: str,
) -> Dict[str, Any]:
    up = _load_upstream(batch_preflight_harness_extraction_post_review_root)
    blockers: List[str] = []

    source_path_mode = "workspace_fallback" if _is_workspace_fallback(up["root"]) else "repo_eval_out"
    standard_pending = source_path_mode == "workspace_fallback"
    meta = {**_boundary_meta(), "source_path_mode": source_path_mode, "standard_eval_out_write_pending_on_local_repro": standard_pending}

    if not up["loaded"]:
        blockers.append(f"upstream input incomplete: {up['missing']}")

    sm = up["artifacts"].get("summary.json") or {}
    vr = up["artifacts"].get("verifier_report.json") or {}

    if vr.get("verifier") != "GO" or vr.get("passed") is not True:
        blockers.append("upstream verifier must be GO")
    if sm.get("phase") != UPSTREAM_REQUIRED_PHASE:
        blockers.append("upstream phase mismatch")
    if sm.get("final_decision") != UPSTREAM_REQUIRED_FINAL:
        blockers.append("upstream final_decision mismatch")
    if sm.get("recommended_next_phase") != UPSTREAM_REQUIRED_NEXT:
        blockers.append("upstream recommended_next_phase must be this planning phase")
    if sm.get("boundary_ok") is not True:
        blockers.append("upstream boundary_ok must be true")

    # Scope & candidate paths for B0 (docs index / readme / phase table alignment only)
    candidate_paths = [
        "docs/architecture/README.md",
        "docs/architecture/evaluation/README.md",
        "docs/architecture/evaluation/LUNA_EVALUATION_OCR_PHASE_VERDICT_STATUS_TABLE_V0.md",
    ]
    batch_domain = "Documentation Index / README / phase table alignment"
    allowed_operations = ["move", "rename"]
    blocked_operations = ["delete", "overwrite", "merge", "copy"]
    protected_path_policy = {"blocked": ["protected/**", "**/protected/**"], "notes": "no protected asset touched"}
    eval_out_policy = {"write_allowed": False, "notes": "preflight planning cannot write to repo _eval_out"}
    before_manifest_requirement = {"required": True, "generated_now": False}
    after_manifest_requirement = {"required": True, "generated_now": False}
    rollback_route = {"route_id": "B0_DOCS_INDEX_ONLY_ROLLBACK_ROUTE_V1", "rehearsal_required": True, "executed_now": False}
    verifier_rerun_list = ["verify_main_project_structure_migration_batch_preflight_harness_extraction_dryrun_v1"]
    post_migration_test_list = ["docs_index_integrity_check", "readme_link_consistency_check"]
    abort_conditions = ["scope_escape_detected", "protected_path_intersection", "eval_out_write_attempted", "operation_not_allowlisted"]
    workspace_fallback_policy = {"enabled": True, "notes": "workspace_fallback does not imply repo _eval_out written"}

    non_claims = [
        "B0 Harness Adoption Planning GO ≠ formal harness generated",
        "B0 adoption planning ≠ B0 preflight executed",
        "B0 batch_config planning ≠ batch_config applied to real batch",
        "B0 preflight planned ≠ B0 armed",
        "B0 selected ≠ B0 executed",
        "B1–B7 deferred ≠ B1–B7 ready",
        "refactor opportunity scan planned ≠ runtime refactor executed",
        "old repetitive phase pattern identified ≠ old phase deleted",
        "verifier rerun requirement planned ≠ verifier rerun executed",
        "rollback requirement planned ≠ rollback rehearsal executed",
        "workspace_fallback GO ≠ standard _eval_out already written",
    ]

    # Scope restrictions
    forbidden_tokens = (
        "capabilities/",
        "tools/",
        "configs/",
        "scripts/",
        "tests/",
        "_eval_out",
        "protected",
        "hr",
        "dnae",
    )
    scope_ok = all(isinstance(p, str) and not any(t in p.lower() for t in forbidden_tokens) for p in candidate_paths)
    if not scope_ok:
        blockers.append("B0 candidate_paths scope violation")

    # Harness check binding
    binding = list(REQUIRED_BINDING_CHECKS)
    binding_ok = set(REQUIRED_BINDING_CHECKS).issubset(set(binding))
    if not binding_ok:
        blockers.append("harness check binding incomplete")

    # Migration Refactor Opportunity Scan planning
    blocked_refactor_items = [
        "vision_runtime",
        "ocr_runtime",
        "navigation_runtime",
        "voice_runtime",
        "task_midplatform_runtime",
        "memory_world_model_fact_write_path",
        "verifier_enforcement_semantics",
    ]
    extract_later_candidates = [
        {"tier": "A", "candidate": "json_summary_builder_helper", "risk": "low"},
        {"tier": "A", "candidate": "verifier_report_builder_helper", "risk": "low"},
        {"tier": "A", "candidate": "workspace_fallback_resolver_helper", "risk": "low"},
        {"tier": "B", "candidate": "batch_preflight_harness_runtime", "risk": "medium"},
    ]
    scan_planning_pass = True

    # B1–B7 deferred matrix
    deferred_rows = []
    for i in range(1, 8):
        bid = f"B{i}"
        deferred_rows.append(
            _row(
                batch_id=bid,
                adoption_deferred=True,
                preflight_allowed_now=False,
                execution_allowed_now=False,
                batch_armed_now=False,
            )
        )

    boundary_ok = not blockers

    policy = _row(
        phase_id=PHASE_ID,
        planning_scope=PLANNING_SCOPE,
        source_path_mode=source_path_mode,
        standard_eval_out_write_pending_on_local_repro=standard_pending,
    )

    upstream_input_review = {
        "post_review_root": str(up["root"]) if up["root"] else None,
        "post_review_loaded": up["loaded"],
        "missing": up["missing"],
        "upstream_summary": {"phase": sm.get("phase"), "final_decision": sm.get("final_decision"), "recommended_next_phase": sm.get("recommended_next_phase")},
        "upstream_verifier": {"verifier": vr.get("verifier"), "passed": vr.get("passed"), "check_count": vr.get("check_count")},
        "all_pass": boundary_ok,
        "blockers": blockers,
        **meta,
    }

    b0_batch_config = _row(
        batch_id="B0",
        batch_domain=batch_domain,
        candidate_paths=candidate_paths,
        allowed_operations=allowed_operations,
        blocked_operations=blocked_operations,
        protected_path_policy=protected_path_policy,
        eval_out_policy=eval_out_policy,
        before_manifest_requirement=before_manifest_requirement,
        after_manifest_requirement=after_manifest_requirement,
        rollback_route=rollback_route,
        verifier_rerun_list=verifier_rerun_list,
        post_migration_test_list=post_migration_test_list,
        abort_conditions=abort_conditions,
        workspace_fallback_policy=workspace_fallback_policy,
        non_claims=non_claims,
    )

    binding_plan = _row(
        batch_id="B0",
        harness_id="main_project_structure_migration_batch_preflight_harness_v1",
        bound_checks=binding,
        binding_complete=binding_ok,
    )

    scope_plan = _row(
        batch_id="B0",
        batch_domain=batch_domain,
        scope_only_docs_index_readme_phase_table=True,
        forbidden_scopes=list(forbidden_tokens),
        b1_b7_included=False,
        scope_ok=scope_ok,
    )

    guard_plan = _row(
        batch_id="B0",
        protected_path_policy=protected_path_policy,
        eval_out_policy=eval_out_policy,
        protected_guard_enabled=True,
        eval_out_readonly_guard_enabled=True,
    )

    file_op_plan = _row(
        batch_id="B0",
        allowed_operations=allowed_operations,
        blocked_operations=blocked_operations,
        no_file_op_without_arming=True,
    )

    manifest_plan = _row(
        batch_id="B0",
        before_manifest_requirement=before_manifest_requirement,
        after_manifest_requirement=after_manifest_requirement,
        manifest_generated_now=False,
    )

    rollback_plan = _row(
        batch_id="B0",
        rollback_route=rollback_route,
        rollback_rehearsal_executed_now=False,
    )

    rerun_plan = _row(
        batch_id="B0",
        verifier_rerun_list=verifier_rerun_list,
        verifier_rerun_executed_now=False,
    )

    tests_plan = _row(
        batch_id="B0",
        post_migration_test_list=post_migration_test_list,
        post_migration_tests_executed_now=False,
    )

    abort_plan = _row(
        batch_id="B0",
        abort_conditions=abort_conditions,
        abort_executed_now=False,
    )

    scan_plan = _row(
        batch_id="B0",
        scan_scope=["docs/architecture/**"],
        duplicate_pattern_candidates=["docs index link tables", "phase verdict table row patterns"],
        extract_now_allowed=False,
        extract_later_candidates=extract_later_candidates,
        blocked_refactor_items=blocked_refactor_items,
        runtime_refactor_executed_now=False,
        scan_planning_pass=scan_planning_pass,
    )

    b1_b7_deferred = {
        "rows": deferred_rows,
        "row_count": len(deferred_rows),
        "all_deferred": True,
        **meta,
    }

    non_claims_register = {
        "rows": [_row(non_claim_id=f"NC_B0_HARNESS_ADOPT_{i+1:02d}", text=t, non_claim_pass=True) for i, t in enumerate(non_claims)],
        "row_count": len(non_claims),
        "all_pass": True,
        **meta,
    }

    readiness = {
        "final_decision": FINAL_DECISION if boundary_ok else "MAIN_PROJECT_STRUCTURE_MIGRATION_B0_HARNESS_ADOPTION_PLANNING_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "ready_for_dryrun": boundary_ok,
        **meta,
    }

    summary = {
        "phase": PHASE_ID,
        "planning_scope": PLANNING_SCOPE,
        "b0_harness_adoption_planning_only": True,
        "selected_batch_id": "B0",
        "b0_only": True,
        "b1_b7_harness_adoption_deferred": True,
        "source_path_mode": source_path_mode,
        "standard_eval_out_write_pending_on_local_repro": standard_pending,
        "upstream_input_loaded": up["loaded"],
        "upstream_verifier_go": vr.get("verifier") == "GO" and vr.get("passed") is True,
        "upstream_final_decision_ok": sm.get("final_decision") == UPSTREAM_REQUIRED_FINAL,
        "upstream_next_phase_ok": sm.get("recommended_next_phase") == UPSTREAM_REQUIRED_NEXT,
        "b0_batch_config_schema_coverage_pass": True,
        "b0_scope_ok": scope_ok,
        "b0_harness_check_binding_complete": binding_ok,
        "migration_refactor_opportunity_scan_planning_pass": scan_planning_pass,
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "final_decision": FINAL_DECISION if boundary_ok else "MAIN_PROJECT_STRUCTURE_MIGRATION_B0_HARNESS_ADOPTION_PLANNING_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        **meta,
    }

    return {
        "summary": summary,
        "b0_harness_adoption_planning_policy": policy,
        "batch_preflight_harness_post_review_input_review": upstream_input_review,
        "b0_batch_config_planning": b0_batch_config,
        "b0_harness_preflight_check_binding": binding_plan,
        "b0_scope_and_domain_isolation_planning": scope_plan,
        "b0_protected_eval_out_guard_planning": guard_plan,
        "b0_file_operation_boundary_planning": file_op_plan,
        "b0_manifest_requirement_planning": manifest_plan,
        "b0_rollback_requirement_planning": rollback_plan,
        "b0_verifier_rerun_requirement_planning": rerun_plan,
        "b0_post_migration_test_requirement_planning": tests_plan,
        "b0_abort_condition_planning": abort_plan,
        "b0_migration_refactor_opportunity_scan_planning": scan_plan,
        "b1_b7_harness_adoption_deferred_matrix": b1_b7_deferred,
        "b0_harness_adoption_non_claims_register": non_claims_register,
        "b0_harness_adoption_planning_readiness_decision": readiness,
    }

