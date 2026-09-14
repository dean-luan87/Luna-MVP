# -*- coding: utf-8 -*-
"""Main Project Structure Migration Batch Preflight Harness Extraction DryRun v1.

Dry-run-only: simulate consumption of Batch Preflight Harness Extraction Planning artifacts and
validate they can be consumed for B0–B7 without generating/enforcing a real harness.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.main_project_structure_migration_batch_preflight_harness_extraction_planning_v1 import (
    FINAL_DECISION as PLANNING_FINAL,
    NEXT_PHASE as PLANNING_NEXT,
    PHASE_ID as PLANNING_PHASE,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID

PHASE_ID = "Phase-Main-Project-Structure-Migration-Batch-Preflight-Harness-Extraction-DryRun-v1-001"
DRYRUN_SCOPE = "main_project_structure_migration_batch_preflight_harness_extraction_dryrun_only"
SOURCE_CHAIN = "main_project_structure_migration_batch_preflight_harness_extraction_dryrun_v1"

FINAL_DECISION = "MAIN_PROJECT_STRUCTURE_MIGRATION_BATCH_PREFLIGHT_HARNESS_EXTRACTION_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
NEXT_PHASE = "Phase-Main-Project-Structure-Migration-Batch-Preflight-Harness-Extraction-Post-DryRun-Review-v1-001"

PLANNING_REQUIRED_PHASE = PLANNING_PHASE
PLANNING_REQUIRED_FINAL = PLANNING_FINAL
PLANNING_REQUIRED_NEXT = PHASE_ID

PLANNING_REQUIRED_ARTIFACTS: Tuple[str, ...] = (
    "summary.json",
    "verifier_report.json",
    "batch_preflight_harness_extraction_policy_v1.json",
    "reusable_preflight_check_inventory_v1.json",
    "batch_config_schema_planning_v1.json",
    "batch_preflight_harness_interface_planning_v1.json",
    "batch_preflight_output_contract_planning_v1.json",
    "batch_preflight_verifier_baseline_planning_v1.json",
    "batch_specific_override_policy_v1.json",
    "b0_to_b7_harness_adoption_matrix_v1.json",
    "deprecated_repetitive_phase_pattern_register_v1.json",
    "batch_preflight_harness_extraction_readiness_decision_v1.json",
)

REQUIRED_FIXED_CHECKS_MIN: Tuple[str, ...] = (
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

REQUIRED_CONFIG_FIELDS_MIN: Tuple[str, ...] = (
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


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _boundary_meta() -> Dict[str, Any]:
    return {
        "batch_preflight_harness_extraction_dryrun_only": True,
        "simulated": True,
        "harness_generated_now": False,
        "harness_enforced_now": False,
        "harness_runtime_integrated_now": False,
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


def run_main_project_structure_migration_batch_preflight_harness_extraction_dryrun_v1(
    *,
    batch_preflight_harness_extraction_planning_root: str,
) -> Dict[str, Any]:
    plan = _load_planning_root(batch_preflight_harness_extraction_planning_root)
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
    if sm.get("batch_preflight_harness_extraction_planning_only") is not True:
        blockers.append("planning must be extraction_planning_only")
    for f in ("harness_generated_now", "harness_enforced_now", "batch_armed_now"):
        if sm.get(f) is not False:
            blockers.append(f"planning boundary must be false: {f}")

    # 1) reusable_preflight_check_inventory consumption
    inv = plan["artifacts"].get("reusable_preflight_check_inventory_v1.json") or {}
    inv_ids = [str(r.get("check_id")) for r in (inv.get("rows") or [])]
    inv_pass = all(c in inv_ids for c in REQUIRED_FIXED_CHECKS_MIN)
    if not inv_pass:
        blockers.append("reusable_preflight_check_inventory missing required checks")

    # 2) batch_config_schema consumption
    schema = plan["artifacts"].get("batch_config_schema_planning_v1.json") or {}
    req_fields = [str(x) for x in (schema.get("required_fields") or [])]
    schema_pass = all(f in req_fields for f in REQUIRED_CONFIG_FIELDS_MIN) and schema.get("field_count", 0) >= 15
    if not schema_pass:
        blockers.append("batch_config_schema missing required fields or insufficient coverage")

    # 3) interface consumption (but no harness generated)
    interface = plan["artifacts"].get("batch_preflight_harness_interface_planning_v1.json") or {}
    interface_pass = (
        interface.get("harness_id") == "main_project_structure_migration_batch_preflight_harness_v1"
        and interface.get("harness_generated_now") is False
        and interface.get("harness_enforced_now") is False
    )
    if not interface_pass:
        blockers.append("harness interface not consumable")

    # 4) output contract consumption (ensure refactor scan present and future batch outputs shape)
    contract = plan["artifacts"].get("batch_preflight_output_contract_planning_v1.json") or {}
    core_outputs = [str(x) for x in (contract.get("core_outputs") or [])]
    contract_pass = all(x in core_outputs for x in ("migration_refactor_opportunity_scan", "readiness_decision", "summary", "verifier_report"))
    if not contract_pass:
        blockers.append("output contract not consumable")

    # 5) verifier baseline consumption (but no verifier modified now)
    baseline = plan["artifacts"].get("batch_preflight_verifier_baseline_planning_v1.json") or {}
    baseline_pass = baseline.get("min_checks") == 420 and baseline.get("must_assert_non_execution_freeze") is True
    if not baseline_pass:
        blockers.append("verifier baseline not consumable")

    # 6) override policy consumption (must forbid bypass of key guards)
    overrides = plan["artifacts"].get("batch_specific_override_policy_v1.json") or {}
    forbidden = [str(x) for x in (overrides.get("forbidden_overrides") or [])]
    override_pass = (
        overrides.get("override_model") == "batch_config_plus_harness_fixed_checks"
        and "fixed_check_inventory" in forbidden
        and "governance_constraints_ref" in forbidden
    )
    if not override_pass:
        blockers.append("override policy not consumable or too permissive")

    # 7) adoption matrix consumption for B0–B7; interpret B1–B7 adoption deferred until B0 validation
    adoption = plan["artifacts"].get("b0_to_b7_harness_adoption_matrix_v1.json") or {}
    adopt_rows = adoption.get("rows") or []
    batch_ids = {r.get("batch_id") for r in adopt_rows}
    adoption_pass = all(f"B{i}" in batch_ids for i in range(8))
    if not adoption_pass:
        blockers.append("adoption matrix does not cover B0–B7")

    # 8) deprecated patterns register consumption
    deprec = plan["artifacts"].get("deprecated_repetitive_phase_pattern_register_v1.json") or {}
    patterns = " ".join([str(r.get("pattern", "")) for r in (deprec.get("rows") or [])]).lower()
    deprec_pass = all(
        token in patterns
        for token in (
            "per-batch",
            "planning",
            "dry-run",
            "post-review",
            "non-claims",
            "summary",
            "verifier_report",
        )
    )
    if not deprec_pass:
        blockers.append("deprecated repetitive pattern register insufficient coverage")

    # 9) migration refactor opportunity scan rule consumption (risk tiers)
    scan_rule_pass = "migration_refactor_opportunity_scan_check" in inv_ids
    if not scan_rule_pass:
        blockers.append("migration refactor opportunity scan rule missing from fixed checks")

    # Non-claims (required set)
    required_non_claims = [
        "Harness Extraction DryRun GO ≠ formal harness generated",
        "Harness interface pass ≠ harness enforced",
        "Batch config schema pass ≠ batch execution allowed",
        "B0 adoption candidate ≠ B0 armed",
        "B1–B7 adoption matrix pass ≠ B1–B7 ready",
        "Refactor opportunity scan ≠ immediate runtime refactor",
        "Deprecated repetitive pattern register ≠ old phase deletion",
        "Verifier baseline pass ≠ verifier modified",
        "workspace_fallback GO ≠ standard _eval_out already written",
    ]

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
        "source_path_mode": source_path_mode,
        "standard_eval_out_write_pending_on_local_repro": standard_pending,
        **meta,
    }

    def _pack(name: str, passed: bool, detail: Any = None) -> Dict[str, Any]:
        return {"rows": [_row(check_id=name, simulated_consumption="pass" if passed else "fail", dryrun_pass=passed, detail=detail)], "row_count": 1, "all_pass": passed, **meta}

    inv_dry = _pack("reusable_preflight_check_inventory", inv_pass, {"required_min": list(REQUIRED_FIXED_CHECKS_MIN)})
    schema_dry = _pack("batch_config_schema", schema_pass, {"required_min": list(REQUIRED_CONFIG_FIELDS_MIN), "field_count": schema.get("field_count")})
    interface_dry = _pack("harness_interface", interface_pass)

    # future batch preflight outputs (as required by user)
    future_batch_outputs = [
        "batch_config",
        "preflight_result",
        "migration_refactor_opportunity_scan",
        "extract_now_allowed",
        "extract_later_candidates",
        "blocked_refactor_items",
        "final_batch_readiness_decision",
    ]
    contract_dry = _pack("output_contract", contract_pass, {"future_batch_outputs_min": future_batch_outputs})
    baseline_dry = _pack("verifier_baseline", baseline_pass)
    override_dry = _pack("override_policy", override_pass, {"forbidden_overrides": forbidden})

    adoption_rows_dry = []
    for i in range(8):
        bid = f"B{i}"
        adoption_rows_dry.append(
            _row(
                batch_id=bid,
                in_planning_matrix=bid in batch_ids,
                first_adoption_candidate=(bid == "B0"),
                adoption_deferred_until_b0_harness_validation=(bid != "B0"),
                execution_allowed_now=False,
                dryrun_pass=(bid in batch_ids),
            )
        )
    adoption_dry = {"rows": adoption_rows_dry, "row_count": len(adoption_rows_dry), "all_pass": adoption_pass, **meta}

    deprec_dry = _pack("deprecated_repetitive_phase_pattern_register", deprec_pass)

    scan_rule_dry = {
        "rows": [
            _row(rule_id="A_LOW_RISK_HELPERS", risk_tier="A", allowed_now=False, can_extract_now=False, should_extract_later=True, examples=["json_summary_builder", "verifier_report_builder", "workspace_fallback_resolver"]),
            _row(rule_id="B_MIGRATION_AFTER", risk_tier="B", allowed_now=False, can_extract_now=False, should_extract_later=True, examples=["common_phase_lifecycle_template", "common_dryrun_harness", "batch_preflight_harness"]),
            _row(rule_id="C_FORBIDDEN_DURING_MIGRATION", risk_tier="C", allowed_now=False, can_extract_now=False, should_extract_later=False, examples=["vision_runtime", "ocr_runtime", "navigation_runtime", "memory_worldmodel_fact_write_path"]),
        ],
        "row_count": 3,
        "all_pass": scan_rule_pass,
        "blocked_from_runtime_refactor_now": True,
        **meta,
    }

    non_claims = {
        "rows": [_row(non_claim_id=f"NC_PREFLIGHT_HARNESS_EXTRACT_DR_{i+1:02d}", text=t, dryrun_pass=True) for i, t in enumerate(required_non_claims)],
        "row_count": len(required_non_claims),
        "all_pass": True,
        **meta,
    }

    readiness = {
        "final_decision": FINAL_DECISION if boundary_ok else "MAIN_PROJECT_STRUCTURE_MIGRATION_BATCH_PREFLIGHT_HARNESS_EXTRACTION_DRYRUN_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "ready_for_post_dryrun_review": boundary_ok,
        **meta,
    }

    summary = {
        "phase": PHASE_ID,
        "dryrun_scope": DRYRUN_SCOPE,
        "batch_preflight_harness_extraction_dryrun_only": True,
        "simulated": True,
        "source_path_mode": source_path_mode,
        "standard_eval_out_write_pending_on_local_repro": standard_pending,
        "planning_input_loaded": plan["loaded"],
        "planning_verifier_go": vr.get("verifier") == "GO" and vr.get("passed") is True,
        "planning_final_decision_ok": sm.get("final_decision") == PLANNING_REQUIRED_FINAL,
        "planning_next_phase_ok": sm.get("recommended_next_phase") == PLANNING_REQUIRED_NEXT,
        "reusable_preflight_check_inventory_dryrun_pass": inv_dry.get("all_pass") is True,
        "batch_config_schema_dryrun_pass": schema_dry.get("all_pass") is True,
        "harness_interface_dryrun_pass": interface_dry.get("all_pass") is True,
        "output_contract_dryrun_pass": contract_dry.get("all_pass") is True,
        "verifier_baseline_dryrun_pass": baseline_dry.get("all_pass") is True,
        "override_policy_dryrun_pass": override_dry.get("all_pass") is True,
        "adoption_matrix_dryrun_pass": adoption_dry.get("all_pass") is True,
        "deprecated_pattern_dryrun_pass": deprec_dry.get("all_pass") is True,
        "migration_refactor_opportunity_scan_rule_dryrun_pass": scan_rule_dry.get("all_pass") is True,
        "non_claims_dryrun_pass": non_claims.get("all_pass") is True,
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "final_decision": FINAL_DECISION if boundary_ok else "MAIN_PROJECT_STRUCTURE_MIGRATION_BATCH_PREFLIGHT_HARNESS_EXTRACTION_DRYRUN_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        **meta,
    }

    return {
        "summary": summary,
        "batch_preflight_harness_extraction_dryrun_policy": policy,
        "batch_preflight_harness_extraction_planning_input_review": input_review,
        "reusable_preflight_check_inventory_dryrun": inv_dry,
        "batch_config_schema_consumption_dryrun": schema_dry,
        "batch_preflight_harness_interface_dryrun": interface_dry,
        "batch_preflight_output_contract_dryrun": contract_dry,
        "batch_preflight_verifier_baseline_dryrun": baseline_dry,
        "batch_specific_override_policy_dryrun": override_dry,
        "b0_to_b7_harness_adoption_dryrun": adoption_dry,
        "deprecated_repetitive_phase_pattern_dryrun": deprec_dry,
        "migration_refactor_opportunity_scan_rule_dryrun": scan_rule_dry,
        "batch_preflight_harness_extraction_non_claims_dryrun": non_claims,
        "batch_preflight_harness_extraction_dryrun_readiness_decision": readiness,
    }

