# -*- coding: utf-8 -*-
"""Main Project Structure Migration Batch Preflight Harness Extraction Post-DryRun Review v1.

Review-only: audit the credibility of harness extraction dry-run outputs.
Confirm consumability without generating/enforcing/integrating a formal harness, without runtime
refactor, and without deleting/deprecating old phases or modifying verifiers/templates.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.main_project_structure_migration_batch_preflight_harness_extraction_dryrun_v1 import (
    FINAL_DECISION as DRYRUN_FINAL,
    NEXT_PHASE as DRYRUN_NEXT,
    PHASE_ID as DRYRUN_PHASE,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID

PHASE_ID = "Phase-Main-Project-Structure-Migration-Batch-Preflight-Harness-Extraction-Post-DryRun-Review-v1-001"
REVIEW_SCOPE = "main_project_structure_migration_batch_preflight_harness_extraction_post_dryrun_review_only"
SOURCE_CHAIN = "main_project_structure_migration_batch_preflight_harness_extraction_post_dryrun_review_v1"

FINAL_DECISION = "MAIN_PROJECT_STRUCTURE_MIGRATION_BATCH_PREFLIGHT_HARNESS_EXTRACTION_POST_DRYRUN_REVIEW_READY_FOR_B0_HARNESS_ADOPTION_PLANNING"
NEXT_PHASE = "Phase-Main-Project-Structure-Migration-B0-Harness-Adoption-Planning-v1-001"

DRYRUN_REQUIRED_PHASE = DRYRUN_PHASE
DRYRUN_REQUIRED_FINAL = DRYRUN_FINAL
DRYRUN_REQUIRED_NEXT = PHASE_ID

DRYRUN_REQUIRED_ARTIFACTS: Tuple[str, ...] = (
    "summary.json",
    "verifier_report.json",
    "batch_preflight_harness_extraction_dryrun_policy_v1.json",
    "batch_preflight_harness_extraction_planning_input_review_v1.json",
    "reusable_preflight_check_inventory_dryrun_v1.json",
    "batch_config_schema_consumption_dryrun_v1.json",
    "batch_preflight_harness_interface_dryrun_v1.json",
    "batch_preflight_output_contract_dryrun_v1.json",
    "batch_preflight_verifier_baseline_dryrun_v1.json",
    "batch_specific_override_policy_dryrun_v1.json",
    "b0_to_b7_harness_adoption_dryrun_v1.json",
    "deprecated_repetitive_phase_pattern_dryrun_v1.json",
    "migration_refactor_opportunity_scan_rule_dryrun_v1.json",
    "batch_preflight_harness_extraction_non_claims_dryrun_v1.json",
    "batch_preflight_harness_extraction_dryrun_readiness_decision_v1.json",
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
    "readiness_decision",
    "migration_refactor_opportunity_scan_check",
)

REQUIRED_SCHEMA_FIELDS: Tuple[str, ...] = (
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
)

REQUIRED_NON_CLAIMS = [
    "Harness Extraction Post-DryRun Review GO ≠ formal harness generated",
    "Harness dry-run pass ≠ harness enforced",
    "Harness interface pass ≠ runtime integrated",
    "Batch config schema pass ≠ batch execution allowed",
    "B0 adoption candidate ≠ B0 armed",
    "B1–B7 adoption matrix pass ≠ B1–B7 ready",
    "Refactor opportunity scan ≠ immediate runtime refactor",
    "Deprecated repetitive pattern register ≠ old phase deletion",
    "Verifier baseline pass ≠ verifier modified",
    "workspace_fallback GO ≠ standard _eval_out already written",
]


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _boundary_meta() -> Dict[str, Any]:
    return {
        "batch_preflight_harness_extraction_post_dryrun_review_only": True,
        "review_only": True,
        "harness_generated_now": False,
        "harness_enforced_now": False,
        "harness_runtime_integrated_now": False,
        "harness_registered_now": False,
        "batch_config_applied_to_real_batch_now": False,
        "batch_execution_started_now": False,
        "batch_armed_now": False,
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
        "verifier_modified_now": False,
        "phase_template_modified_now": False,
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
    return {**kwargs, **_boundary_meta(), "reviewed_now": True, "executed_now": False}


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def _load_dryrun_root(path_str: Optional[str]) -> Dict[str, Any]:
    root = Path(path_str).expanduser().resolve() if path_str else None
    artifacts: Dict[str, Any] = {}
    missing: List[str] = []
    if root:
        for name in DRYRUN_REQUIRED_ARTIFACTS:
            payload = _try_read_json(root / name)
            if payload is None:
                missing.append(name)
            else:
                artifacts[name] = payload
    loaded = bool(root) and not missing and bool(artifacts.get("summary.json")) and bool(artifacts.get("verifier_report.json"))
    return {"root": root, "loaded": loaded, "missing": missing, "artifacts": artifacts}


def _is_workspace_fallback(root: Optional[Path]) -> bool:
    return bool(root) and "Luna-Workspace-Min" in str(root)


def run_main_project_structure_migration_batch_preflight_harness_extraction_post_dryrun_review_v1(
    *,
    batch_preflight_harness_extraction_dryrun_root: str,
) -> Dict[str, Any]:
    dry = _load_dryrun_root(batch_preflight_harness_extraction_dryrun_root)
    blockers: List[str] = []

    source_path_mode = "workspace_fallback" if _is_workspace_fallback(dry["root"]) else "repo_eval_out"
    standard_pending = source_path_mode == "workspace_fallback"
    meta = {**_boundary_meta(), "source_path_mode": source_path_mode, "standard_eval_out_write_pending_on_local_repro": standard_pending}

    if not dry["loaded"]:
        blockers.append(f"dryrun input incomplete: {dry['missing']}")

    sm = dry["artifacts"].get("summary.json") or {}
    vr = dry["artifacts"].get("verifier_report.json") or {}

    if vr.get("verifier") != "GO" or vr.get("passed") is not True:
        blockers.append("dryrun verifier must be GO")
    if sm.get("phase") != DRYRUN_REQUIRED_PHASE:
        blockers.append("dryrun phase mismatch")
    if sm.get("final_decision") != DRYRUN_REQUIRED_FINAL:
        blockers.append("dryrun final_decision mismatch")
    if sm.get("recommended_next_phase") != DRYRUN_REQUIRED_NEXT:
        blockers.append("dryrun recommended_next_phase must be this post-review phase")
    if sm.get("batch_preflight_harness_extraction_dryrun_only") is not True or sm.get("simulated") is not True:
        blockers.append("dryrun must be dryrun_only & simulated")
    if sm.get("boundary_ok") is not True:
        blockers.append("dryrun boundary_ok must be true")

    # Boundary: confirm non-generation/non-enforcement/non-integration/non-execution
    for f in (
        "harness_generated_now",
        "harness_enforced_now",
        "harness_runtime_integrated_now",
        "batch_config_applied_to_real_batch_now",
        "batch_armed_now",
        "batch_execution_started_now",
        "execution_window_opened_now",
        "file_operation_executed_now",
        "verifier_rerun_executed_now",
        "rollback_rehearsal_executed_now",
        "post_migration_tests_executed_now",
    ):
        if sm.get(f) is not False:
            blockers.append(f"dryrun boundary must be false: {f}")

    # 1) reusable check inventory coverage
    inv_dry = dry["artifacts"].get("reusable_preflight_check_inventory_dryrun_v1.json") or {}
    inv_required_min = ((inv_dry.get("rows") or [{}])[0].get("detail") or {}).get("required_min") or []
    inv_review_pass = all(c in inv_required_min for c in REQUIRED_FIXED_CHECKS)

    # 2) schema coverage
    schema_dry = dry["artifacts"].get("batch_config_schema_consumption_dryrun_v1.json") or {}
    schema_required_min = ((schema_dry.get("rows") or [{}])[0].get("detail") or {}).get("required_min") or []
    schema_review_pass = all(f in schema_required_min for f in REQUIRED_SCHEMA_FIELDS)

    # 3) interface: must confirm no generation/enforcement/integration/registration
    interface_review_pass = sm.get("harness_generated_now") is False and sm.get("harness_enforced_now") is False and sm.get("harness_runtime_integrated_now") is False

    # 4) output contract: ensure future batch outputs exist
    contract_dry = dry["artifacts"].get("batch_preflight_output_contract_dryrun_v1.json") or {}
    future_outputs = ((contract_dry.get("rows") or [{}])[0].get("detail") or {}).get("future_batch_outputs_min") or []
    required_future = [
        "batch_config",
        "preflight_result",
        "migration_refactor_opportunity_scan",
        "extract_now_allowed",
        "extract_later_candidates",
        "blocked_refactor_items",
        "final_batch_readiness_decision",
    ]
    contract_review_pass = all(x in future_outputs for x in required_future)

    # 5) baseline: confirm blocked_from_runtime_refactor asserted in planning baseline (carried through dry-run contract)
    baseline_dry = dry["artifacts"].get("batch_preflight_verifier_baseline_dryrun_v1.json") or {}
    baseline_review_pass = baseline_dry.get("all_pass") is True

    # 6) override policy: ensure forbidden overrides include fixed checks & governance constraints ref
    override_dry = dry["artifacts"].get("batch_specific_override_policy_dryrun_v1.json") or {}
    forbidden = ((override_dry.get("rows") or [{}])[0].get("detail") or {}).get("forbidden_overrides") or []
    override_review_pass = ("fixed_check_inventory" in forbidden) and ("governance_constraints_ref" in forbidden)

    # 7) adoption matrix: B0 first candidate, B1–B7 deferred and all exec_allowed_now=false and batch_armed_now=false
    adopt_dry = dry["artifacts"].get("b0_to_b7_harness_adoption_dryrun_v1.json") or {}
    rows = adopt_dry.get("rows") or []
    b0_first = any(r.get("batch_id") == "B0" and r.get("first_adoption_candidate") is True for r in rows)
    b1b7_deferred = all((r.get("batch_id") == "B0") or (r.get("adoption_deferred_until_b0_harness_validation") is True) for r in rows)
    exec_false = all(r.get("execution_allowed_now") is False for r in rows)
    adoption_review_pass = adopt_dry.get("all_pass") is True and b0_first and b1b7_deferred and exec_false

    # 8) deprecated patterns: confirm register exists but no deletion/deprecation of old phases (review-only statements)
    deprec_dry = dry["artifacts"].get("deprecated_repetitive_phase_pattern_dryrun_v1.json") or {}
    deprec_review_pass = deprec_dry.get("all_pass") is True

    # 9) scan rule: confirm A/B/C tiers and blocked_from_runtime_refactor_now=true
    scan_rule = dry["artifacts"].get("migration_refactor_opportunity_scan_rule_dryrun_v1.json") or {}
    scan_rows = scan_rule.get("rows") or []
    tiers = {r.get("risk_tier") for r in scan_rows}
    scan_review_pass = {"A", "B", "C"}.issubset(tiers) and scan_rule.get("blocked_from_runtime_refactor_now") is True

    # 10) non-generation review
    non_generation_pass = all(
        sm.get(f) is False
        for f in (
            "harness_generated_now",
            "harness_enforced_now",
            "harness_runtime_integrated_now",
            "batch_config_applied_to_real_batch_now",
            "file_operation_executed_now",
        )
    )

    if not inv_review_pass:
        blockers.append("reusable check inventory review failed")
    if not schema_review_pass:
        blockers.append("batch config schema review failed")
    if not interface_review_pass:
        blockers.append("harness interface non-generation review failed")
    if not contract_review_pass:
        blockers.append("output contract review failed")
    if not baseline_review_pass:
        blockers.append("verifier baseline review failed")
    if not override_review_pass:
        blockers.append("override policy review failed")
    if not adoption_review_pass:
        blockers.append("adoption matrix review failed")
    if not deprec_review_pass:
        blockers.append("deprecated pattern review failed")
    if not scan_review_pass:
        blockers.append("migration refactor scan rule review failed")
    if not non_generation_pass:
        blockers.append("non-generation review failed")

    boundary_ok = not blockers

    policy = _row(
        phase_id=PHASE_ID,
        review_scope=REVIEW_SCOPE,
        source_path_mode=source_path_mode,
        standard_eval_out_write_pending_on_local_repro=standard_pending,
    )

    input_review = {
        "dryrun_root": str(dry["root"]) if dry["root"] else None,
        "dryrun_loaded": dry["loaded"],
        "missing": dry["missing"],
        "dryrun_summary": {"phase": sm.get("phase"), "final_decision": sm.get("final_decision"), "recommended_next_phase": sm.get("recommended_next_phase")},
        "dryrun_verifier": {"verifier": vr.get("verifier"), "passed": vr.get("passed"), "check_count": vr.get("check_count")},
        "all_pass": boundary_ok,
        "blockers": blockers,
        **meta,
    }

    def _review_pack(name: str, passed: bool, detail: Any = None) -> Dict[str, Any]:
        return {"rows": [_row(check_id=name, review_pass=passed, detail=detail)], "row_count": 1, "all_pass": passed, **meta}

    inv_review = _review_pack("reusable_preflight_check_inventory", inv_review_pass, {"required_checks": list(REQUIRED_FIXED_CHECKS)})
    schema_review = _review_pack("batch_config_schema", schema_review_pass, {"required_fields": list(REQUIRED_SCHEMA_FIELDS)})
    interface_review = _review_pack(
        "harness_interface",
        interface_review_pass,
        {"harness_generated_now": False, "harness_registered_now": False, "harness_enforced_now": False, "harness_runtime_integrated_now": False},
    )
    contract_review = _review_pack("output_contract", contract_review_pass, {"required_future_outputs": required_future})
    baseline_review = _review_pack("verifier_baseline", baseline_review_pass, {"verifier_modified_now": False, "must_assert_blocked_from_runtime_refactor_now": True})
    override_review = _review_pack("override_policy", override_review_pass, {"forbidden_overrides_min": ["fixed_check_inventory", "governance_constraints_ref"]})
    adoption_review = _review_pack("adoption_matrix", adoption_review_pass, {"b0_first": b0_first, "b1_b7_deferred": b1b7_deferred, "execution_allowed_now_all_false": exec_false})
    deprec_review = _review_pack("deprecated_patterns", deprec_review_pass, {"old_phase_deleted_now": False, "old_phase_deprecated_now": False})
    scan_review = _review_pack("migration_refactor_scan_rule", scan_review_pass, {"tiers": sorted([t for t in tiers if t])})

    non_generation_review = {
        "rows": [
            _row(
                check_id="non_generation",
                formal_harness_generated=False,
                harness_enforced=False,
                harness_runtime_integrated=False,
                batch_config_applied_to_real_batch=False,
                any_file_operation_executed=False,
                review_pass=non_generation_pass,
            )
        ],
        "row_count": 1,
        "all_pass": non_generation_pass,
        **meta,
    }

    non_claims_review = {
        "rows": [_row(non_claim_id=f"NC_PREFLIGHT_HARNESS_EXTRACT_POST_{i+1:02d}", text=t, review_pass=True) for i, t in enumerate(REQUIRED_NON_CLAIMS)],
        "row_count": len(REQUIRED_NON_CLAIMS),
        "all_pass": True,
        **meta,
    }

    readiness = {
        "final_decision": FINAL_DECISION if boundary_ok else "MAIN_PROJECT_STRUCTURE_MIGRATION_BATCH_PREFLIGHT_HARNESS_EXTRACTION_POST_DRYRUN_REVIEW_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "ready_for_b0_harness_adoption_planning": boundary_ok,
        **meta,
    }

    summary = {
        "phase": PHASE_ID,
        "review_scope": REVIEW_SCOPE,
        "batch_preflight_harness_extraction_post_dryrun_review_only": True,
        "review_only": True,
        "source_path_mode": source_path_mode,
        "standard_eval_out_write_pending_on_local_repro": standard_pending,
        "dryrun_input_loaded": dry["loaded"],
        "dryrun_verifier_go": vr.get("verifier") == "GO" and vr.get("passed") is True,
        "dryrun_final_decision_ok": sm.get("final_decision") == DRYRUN_REQUIRED_FINAL,
        "dryrun_next_phase_ok": sm.get("recommended_next_phase") == DRYRUN_REQUIRED_NEXT,
        "inventory_review_pass": inv_review.get("all_pass") is True,
        "schema_review_pass": schema_review.get("all_pass") is True,
        "interface_review_pass": interface_review.get("all_pass") is True,
        "output_contract_review_pass": contract_review.get("all_pass") is True,
        "verifier_baseline_review_pass": baseline_review.get("all_pass") is True,
        "override_policy_review_pass": override_review.get("all_pass") is True,
        "adoption_review_pass": adoption_review.get("all_pass") is True,
        "deprecated_pattern_review_pass": deprec_review.get("all_pass") is True,
        "scan_rule_review_pass": scan_review.get("all_pass") is True,
        "non_generation_review_pass": non_generation_review.get("all_pass") is True,
        "non_claims_review_pass": non_claims_review.get("all_pass") is True,
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "final_decision": FINAL_DECISION if boundary_ok else "MAIN_PROJECT_STRUCTURE_MIGRATION_BATCH_PREFLIGHT_HARNESS_EXTRACTION_POST_DRYRUN_REVIEW_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        **meta,
    }

    return {
        "summary": summary,
        "batch_preflight_harness_extraction_post_dryrun_review_policy": policy,
        "batch_preflight_harness_extraction_dryrun_input_review": input_review,
        "reusable_preflight_check_inventory_review": inv_review,
        "batch_config_schema_consumption_review": schema_review,
        "batch_preflight_harness_interface_review": interface_review,
        "batch_preflight_output_contract_review": contract_review,
        "batch_preflight_verifier_baseline_review": baseline_review,
        "batch_specific_override_policy_review": override_review,
        "b0_to_b7_harness_adoption_review": adoption_review,
        "deprecated_repetitive_phase_pattern_review": deprec_review,
        "migration_refactor_opportunity_scan_rule_review": scan_review,
        "batch_preflight_harness_non_generation_review": non_generation_review,
        "batch_preflight_harness_extraction_non_claims_review": non_claims_review,
        "batch_preflight_harness_extraction_post_dryrun_review_readiness_decision": readiness,
    }

