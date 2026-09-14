# -*- coding: utf-8 -*-
"""Main Project Structure Migration Batch Preflight Harness Extraction Planning v1.

Planning-only: extract common preflight validation logic from existing controlled batch execution
authorization/arming/request-planning chains and define a reusable Batch Preflight Harness contract.

No harness generated now, no enforcement, no arming, no requests, no execution, no file operations.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID

PHASE_ID = "Phase-Main-Project-Structure-Migration-Batch-Preflight-Harness-Extraction-Planning-v1-001"
PLANNING_SCOPE = "main_project_structure_migration_batch_preflight_harness_extraction_planning_only"
SOURCE_CHAIN = "main_project_structure_migration_batch_preflight_harness_extraction_planning_v1"

FINAL_DECISION = "MAIN_PROJECT_STRUCTURE_MIGRATION_BATCH_PREFLIGHT_HARNESS_EXTRACTION_PLANNING_READY_FOR_DRYRUN"
NEXT_PHASE = "Phase-Main-Project-Structure-Migration-Batch-Preflight-Harness-Extraction-DryRun-v1-001"

UPSTREAM_PHASES: Tuple[Tuple[str, str], ...] = (
    (
        "controlled_batch_exec_auth_post_review_root",
        "Phase-Main-Project-Structure-Migration-Controlled-Batch-Execution-Authorization-Post-DryRun-Review-v1-001",
    ),
    (
        "controlled_batch_exec_arming_post_review_root",
        "Phase-Main-Project-Structure-Migration-Controlled-Batch-Execution-Arming-Post-DryRun-Review-v1-001",
    ),
    (
        "b0_arming_request_planning_root",
        "Phase-Main-Project-Structure-Migration-Controlled-Batch-Execution-B0-Arming-Request-Planning-v1-001",
    ),
)

UPSTREAM_REQUIRED_FINAL_DECISIONS: Dict[str, str] = {
    "controlled_batch_exec_auth_post_review_root": "MAIN_PROJECT_STRUCTURE_MIGRATION_CONTROLLED_BATCH_EXECUTION_AUTHORIZATION_POST_DRYRUN_REVIEW_READY_FOR_CONTROLLED_BATCH_EXECUTION_ARMING_PLANNING",
    "controlled_batch_exec_arming_post_review_root": "MAIN_PROJECT_STRUCTURE_MIGRATION_CONTROLLED_BATCH_EXECUTION_ARMING_POST_DRYRUN_REVIEW_READY_FOR_B0_ARMING_REQUEST_PLANNING",
    "b0_arming_request_planning_root": "MAIN_PROJECT_STRUCTURE_MIGRATION_CONTROLLED_BATCH_EXECUTION_B0_ARMING_REQUEST_PLANNING_READY_FOR_DRYRUN",
}


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _boundary_meta() -> Dict[str, Any]:
    return {
        "batch_preflight_harness_extraction_planning_only": True,
        "selected_batch_id": "B0",  # planning anchored on B0 patterns; harness applies to B0–B7
        "b0_only": False,
        "b1_b7_arming_deferred": True,
        "harness_generated_now": False,
        "harness_enforced_now": False,
        "batch_armed_now": False,
        "batch_execution_started_now": False,
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
        "execution_window_opened_now": False,
        "eval_out_modified_now": False,
        "protected_asset_modified_now": False,
        "hr_modified_now": False,
        "dnae_modified_now": False,
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
    return {
        **kwargs,
        **_boundary_meta(),
        "planned_now": True,
        "executed_now": False,
        "simulated_now": False,
    }


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def _is_workspace_fallback(root: Optional[Path]) -> bool:
    return bool(root) and "Luna-Workspace-Min" in str(root)


def _load_upstream(root_str: Optional[str], phase_required: str) -> Dict[str, Any]:
    root = Path(root_str).expanduser().resolve() if root_str else None
    if not root:
        return {"root": None, "loaded": False, "summary": None, "verifier_report": None, "missing": ["root_not_provided"]}
    sm = _try_read_json(root / "summary.json")
    vr = _try_read_json(root / "verifier_report.json")
    missing: List[str] = []
    if sm is None:
        missing.append("summary.json")
    if vr is None:
        missing.append("verifier_report.json")
    loaded = not missing and sm.get("phase") == phase_required and vr.get("verifier") == "GO" and vr.get("passed") is True
    return {"root": root, "loaded": loaded, "summary": sm, "verifier_report": vr, "missing": missing}


def run_main_project_structure_migration_batch_preflight_harness_extraction_planning_v1(
    *,
    controlled_batch_exec_auth_post_review_root: str,
    controlled_batch_exec_arming_post_review_root: str,
    b0_arming_request_planning_root: str,
) -> Dict[str, Any]:
    upstream: Dict[str, Dict[str, Any]] = {}
    blockers: List[str] = []

    source_path_mode = "workspace_fallback" if any(
        _is_workspace_fallback(Path(p).expanduser().resolve())
        for p in (controlled_batch_exec_auth_post_review_root, controlled_batch_exec_arming_post_review_root, b0_arming_request_planning_root)
        if p
    ) else "repo_eval_out"
    standard_pending = source_path_mode == "workspace_fallback"
    meta = {**_boundary_meta(), "source_path_mode": source_path_mode, "standard_eval_out_write_pending_on_local_repro": standard_pending}

    for key, required_phase in UPSTREAM_PHASES:
        root_value = {
            "controlled_batch_exec_auth_post_review_root": controlled_batch_exec_auth_post_review_root,
            "controlled_batch_exec_arming_post_review_root": controlled_batch_exec_arming_post_review_root,
            "b0_arming_request_planning_root": b0_arming_request_planning_root,
        }[key]
        up = _load_upstream(root_value, required_phase)
        upstream[key] = up
        if not up["loaded"]:
            blockers.append(f"upstream not loaded: {key} missing={up['missing']}")
        else:
            sm = up["summary"] or {}
            required_final = UPSTREAM_REQUIRED_FINAL_DECISIONS.get(key)
            if required_final and sm.get("final_decision") != required_final:
                blockers.append(f"upstream final_decision mismatch: {key}")
            if sm.get("boundary_ok") is not True:
                blockers.append(f"upstream boundary_ok must be true: {key}")

    # Fixed check list of harness
    fixed_checks = [
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
    ]

    # Batch config schema planning (required by user)
    config_schema_fields = [
        "batch_id",
        "batch_domain",
        "candidate_paths",
        "allowed_operations",
        "blocked_operations",
        "protected_path_policy",
        "eval_out_policy",
        "before_manifest_requirement",
        "after_manifest_requirement",
        "rollback_route",
        "verifier_rerun_list",
        "post_migration_test_list",
        "abort_conditions",
        "workspace_fallback_policy",
        "non_claims",
    ]

    # Adoption matrix: B0–B7 will use harness (no repetitive phase chain)
    adoption_rows = []
    for i in range(8):
        bid = f"B{i}"
        adoption_rows.append(
            _row(
                batch_id=bid,
                adopt_harness=True,
                repetitive_phase_chain_deprecated=True,
                notes="use batch config + harness; do not fork per-batch planning/dryrun/review chains",
            )
        )

    deprecated_patterns = [
        "per-batch planning chain duplication (preflight)",
        "per-batch dry-run chain duplication (preflight)",
        "per-batch post-review chain duplication (preflight)",
        "repeated non-claims register generation",
        "repeated guard matrix generation (protected/HR/DnAE/_eval_out/file-op)",
        "repeated summary / verifier_report boilerplate",
        "duplicating scope/protected/_eval_out/file-op boundary checks in separate batch-specific phase code",
        "copy-paste verifier inflation loops across batch phases",
        "document three-pack boilerplate duplication (governance/evaluation/go-no-go)",
        "phase verdict table / README update boilerplate duplication",
        "treating workspace_fallback as standard _eval_out already written",
    ]

    # Overrides: allow batch-specific lists/paths but forbid changing the fixed check list
    override_policy = {
        "allowed_overrides": [
            "batch_domain",
            "candidate_paths",
            "allowed_operations",
            "blocked_operations",
            "protected_path_policy",
            "eval_out_policy",
            "before_manifest_requirement",
            "after_manifest_requirement",
            "rollback_route",
            "verifier_rerun_list",
            "post_migration_test_list",
            "abort_conditions",
            "non_claims",
        ],
        "forbidden_overrides": [
            "fixed_check_inventory",
            "non_execution_freeze_fields",
            "mandatory_boundary_fields",
            "governance_constraints_ref",
        ],
        "override_model": "batch_config_plus_harness_fixed_checks",
    }

    boundary_ok = not blockers

    policy = _row(
        phase_id=PHASE_ID,
        planning_scope=PLANNING_SCOPE,
        source_path_mode=source_path_mode,
        standard_eval_out_write_pending_on_local_repro=standard_pending,
    )

    check_inventory = {
        "rows": [_row(check_id=c, required=True, description="fixed harness check") for c in fixed_checks],
        "row_count": len(fixed_checks),
        "all_fixed": True,
        "all_required": True,
        **meta,
    }

    schema_planning = {
        "schema_id": "batch_preflight_config_schema_v1",
        "required_fields": config_schema_fields,
        "field_count": len(config_schema_fields),
        "supported_batch_ids": [f"B{i}" for i in range(8)],
        "allows_future_extension": True,
        "extension_rule": "additive_only; no change to fixed check inventory without harness version bump",
        **meta,
    }

    interface_planning = {
        "harness_id": "main_project_structure_migration_batch_preflight_harness_v1",
        "entrypoint_cli_candidate": "Phase-Main-Project-Structure-Migration-<BATCH>-Preflight-v1",
        "input_config_schema_id": "batch_preflight_config_schema_v1",
        "fixed_checks": fixed_checks,
        "execution_mode": "planning/dryrun/review supported; real execution not in harness scope",
        "harness_generated_now": False,
        "harness_enforced_now": False,
        **meta,
    }

    output_contract = {
        "output_contract_id": "batch_preflight_output_contract_v1",
        "core_outputs": [
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
            "migration_refactor_opportunity_scan",
            "readiness_decision",
            "summary",
            "verifier_report",
        ],
        "contract_frozen": True,
        "requires_summary_freeze_fields": True,
        **meta,
    }

    verifier_baseline = {
        "verifier_baseline_id": "batch_preflight_verifier_baseline_v1",
        "min_checks": 420,
        "baseline_requirement": 340,
        "must_assert_upstream_go": True,
        "must_assert_non_execution_freeze": True,
        "must_assert_scope_no_cross_batch": True,
        "must_assert_no_protected_hr_dnae_eval_out": True,
        "must_assert_workspace_fallback_semantics": True,
        "must_assert_blocked_from_runtime_refactor_now": True,
        **meta,
    }

    adoption_matrix = {
        "rows": adoption_rows,
        "row_count": len(adoption_rows),
        "all_adopt": True,
        "deprecates_repetitive_phase_pattern": True,
        **meta,
    }

    deprecated_register = {
        "rows": [_row(pattern_id=f"DEPR_{i+1:02d}", pattern=p, forbidden_later=True) for i, p in enumerate(deprecated_patterns)],
        "row_count": len(deprecated_patterns),
        "all_forbidden_later": True,
        **meta,
    }

    readiness = {
        "final_decision": FINAL_DECISION if boundary_ok else "MAIN_PROJECT_STRUCTURE_MIGRATION_BATCH_PREFLIGHT_HARNESS_EXTRACTION_PLANNING_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "ready_for_dryrun": boundary_ok,
        "harness_generated_now": False,
        "harness_enforced_now": False,
        "check_inventory_defined": True,
        "config_schema_defined": True,
        "output_contract_defined": True,
        **meta,
    }

    summary = {
        "phase": PHASE_ID,
        "planning_scope": PLANNING_SCOPE,
        "batch_preflight_harness_extraction_planning_only": True,
        "source_path_mode": source_path_mode,
        "standard_eval_out_write_pending_on_local_repro": standard_pending,
        "upstream_loaded": {k: upstream[k]["loaded"] for k in upstream},
        "upstream_boundary_ok": {k: bool((upstream[k]["summary"] or {}).get("boundary_ok") is True) for k in upstream},
        "harness_generated_now": False,
        "harness_enforced_now": False,
        "fixed_check_inventory_count": len(fixed_checks),
        "batch_config_required_field_count": len(config_schema_fields),
        "b0_to_b7_adoption_rows": len(adoption_rows),
        "deprecated_patterns_registered": len(deprecated_patterns),
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "final_decision": FINAL_DECISION if boundary_ok else "MAIN_PROJECT_STRUCTURE_MIGRATION_BATCH_PREFLIGHT_HARNESS_EXTRACTION_PLANNING_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        **meta,
    }

    return {
        "summary": summary,
        "batch_preflight_harness_extraction_policy": policy,
        "reusable_preflight_check_inventory": check_inventory,
        "batch_config_schema_planning": schema_planning,
        "batch_preflight_harness_interface_planning": interface_planning,
        "batch_preflight_output_contract_planning": output_contract,
        "batch_preflight_verifier_baseline_planning": verifier_baseline,
        "batch_specific_override_policy": {**override_policy, **meta},
        "b0_to_b7_harness_adoption_matrix": adoption_matrix,
        "deprecated_repetitive_phase_pattern_register": deprecated_register,
        "batch_preflight_harness_extraction_readiness_decision": readiness,
    }

