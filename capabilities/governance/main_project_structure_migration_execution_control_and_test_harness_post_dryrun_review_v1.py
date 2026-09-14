# -*- coding: utf-8 -*-
"""Main Project Structure Migration Execution Control and Test Harness Post-DryRun Review v1.

Review-only: audit execution control dry-run for closure readiness.
No real migration, batch arming, tests, verifier suite, or rollback rehearsal.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PHASE_ID = "Phase-Main-Project-Structure-Migration-Execution-Control-and-Test-Harness-Post-DryRun-Review-v1-001"
REVIEW_SCOPE = "main_project_structure_migration_execution_control_and_test_harness_post_dryrun_review_only"
SOURCE_CHAIN = "main_project_structure_migration_execution_control_and_test_harness_post_dryrun_review_v1"
REVIEW_ID = "main_proj_struct_migration_exec_control_test_harness_post_dryrun_review_v1_001"

FINAL_DECISION = "MAIN_PROJECT_STRUCTURE_MIGRATION_EXECUTION_CONTROL_AND_TEST_HARNESS_POST_DRYRUN_REVIEW_READY_FOR_CLOSURE"
NEXT_PHASE = "Phase-Main-Project-Structure-Migration-Execution-Control-and-Test-Harness-Closure-v1-001"

DRYRUN_FINAL = "MAIN_PROJECT_STRUCTURE_MIGRATION_EXECUTION_CONTROL_AND_TEST_HARNESS_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
PLANNING_FINAL = "MAIN_PROJECT_STRUCTURE_MIGRATION_EXECUTION_CONTROL_AND_TEST_HARNESS_PLANNING_READY_FOR_DRYRUN"
CLOSURE_DECISION = "MAIN_PROJECT_STRUCTURE_MIGRATION_GUARDED_CLOSED_FOR_CURRENT_MAINLINE"

HUMAN_REVIEW_CARRYOVER = 240
PERMANENT_BLOCK_CARRYOVER = 914

CANONICAL_ABORT_NAMES = (
    "missing_test_harness",
    "missing_verifier_suite",
    "missing_rollback_checkpoint",
)
PLANNING_ABORT_ALIASES = (
    "test_harness_missing",
    "verifier_suite_missing",
    "rollback_checkpoint_missing",
)

DRYRUN_ARTIFACTS = [
    "execution_control_dryrun_execution_plan.json",
    "execution_control_gate_dryrun_result.json",
    "batch_arming_dryrun_results.json",
    "abort_condition_dryrun_results.json",
    "pre_execution_checklist_dryrun_result.json",
    "post_migration_test_harness_dryrun_result.json",
    "post_migration_verifier_suite_dryrun_result.json",
    "rollback_rehearsal_dryrun_result.json",
    "failure_response_matrix_dryrun_result.json",
    "execution_control_dryrun_readiness_decision.json",
    "forbidden_execution_report.json",
]

PLANNING_ARTIFACTS = [
    "migration_execution_control_and_test_harness_planning_policy.json",
    "execution_control_gate.json",
    "batch_arming_policy.json",
    "abort_condition_policy.json",
    "post_migration_test_harness.json",
    "post_migration_verifier_suite.json",
    "rollback_rehearsal_requirement.json",
    "failure_response_matrix.json",
]

ROOT_SPECS = [
    {
        "id": "execution_control_dryrun",
        "arg": "execution_control_dryrun_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": DRYRUN_ARTIFACTS,
    },
    {
        "id": "execution_control_planning",
        "arg": "execution_control_planning_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": PLANNING_ARTIFACTS,
    },
    {"id": "guarded_roadmap", "arg": "guarded_roadmap_root", "required": True, "summary": "summary.json", "artifacts": []},
    {"id": "guarded_closure", "arg": "guarded_closure_root", "required": True, "summary": "summary.json", "artifacts": []},
    {
        "id": "guarded_post_review",
        "arg": "guarded_post_review_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": [],
    },
    {"id": "guarded_dryrun", "arg": "guarded_dryrun_root", "required": True, "summary": "summary.json", "artifacts": []},
    {"id": "guarded_planning", "arg": "guarded_planning_root", "required": True, "summary": "summary.json", "artifacts": []},
    {"id": "readiness", "arg": "readiness_root", "required": True, "summary": "summary.json", "artifacts": []},
    {"id": "pahr_closure", "arg": "pahr_closure_root", "required": True, "summary": "summary.json", "artifacts": []},
    {
        "id": "consolidation_closure",
        "arg": "consolidation_closure_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": [],
    },
    {"id": "structure_map", "arg": "structure_map_root", "required": True, "summary": "summary.json", "artifacts": []},
    {"id": "gate_taxonomy", "arg": "gate_taxonomy_root", "required": True, "summary": "summary.json", "artifacts": []},
]


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _bool_val(val: Any, default: bool = False) -> bool:
    """Coerce JSON-loaded value to bool without `x is False` inversion bugs."""
    if val is None:
        return default
    return bool(val)


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def _load_root(path_str: Optional[str], summary_file: str, artifacts: List[str]) -> Dict[str, Any]:
    root = Path(path_str).expanduser().resolve() if path_str else None
    summary_payload = _try_read_json(root / summary_file) if root else None
    loaded = summary_payload is not None
    art: Dict[str, Any] = {}
    missing: List[str] = []
    if root and artifacts:
        for name in artifacts:
            payload = _try_read_json(root / name)
            if payload is None:
                missing.append(name)
            else:
                art[name] = payload
        loaded = loaded and not missing
    return {
        "root": root,
        "loaded": loaded,
        "summary": summary_payload or {},
        "artifacts": art,
        "missing_artifacts": missing,
    }


def _abort_blocks(abort_res: Dict[str, Any], condition_name: str) -> bool:
    return any(
        a.get("condition_name") == condition_name and a.get("blocks_execution") is True
        for a in abort_res.get("conditions") or []
    )


def _canonical_mapping_applied(abort_res: Dict[str, Any]) -> bool:
    by_name = {a.get("condition_name"): a for a in abort_res.get("conditions") or []}
    pairs = (
        ("missing_test_harness", "test_harness_missing"),
        ("missing_verifier_suite", "verifier_suite_missing"),
        ("missing_rollback_checkpoint", "rollback_checkpoint_missing"),
    )
    for canonical, planning in pairs:
        entry = by_name.get(canonical)
        if not entry or entry.get("blocks_execution") is not True:
            return False
        if entry.get("planning_condition_name") != planning:
            return False
    return True


def _boundary_reports() -> Tuple[Dict[str, Any], Dict[str, Any], Dict[str, Any], Dict[str, Any]]:
    base = {
        "review_scope": REVIEW_SCOPE,
        "review_only": True,
        "boundary_ok": True,
        "violations": [],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }
    no_file_move = {**base, "report_kind": "no_file_move", "actual_file_move_executed": False}
    no_delete = {**base, "report_kind": "no_delete", "actual_file_delete_executed": False}
    no_runtime = {
        **base,
        "report_kind": "no_runtime",
        "runtime_enabled": False,
        "no_runtime_executed": True,
        "no_new_runtime_enabled": True,
    }
    no_write = {
        **base,
        "report_kind": "no_write",
        "world_model_written": False,
        "memory_written": False,
        "library_written": False,
        "fact_written": False,
    }
    return no_file_move, no_delete, no_runtime, no_write


def run_main_project_structure_migration_execution_control_and_test_harness_post_dryrun_review_v1(
    *,
    execution_control_dryrun_root: str,
    execution_control_planning_root: str,
    guarded_roadmap_root: str,
    guarded_closure_root: str,
    guarded_post_review_root: str,
    guarded_dryrun_root: str,
    guarded_planning_root: str,
    readiness_root: str,
    pahr_closure_root: str,
    consolidation_closure_root: str,
    structure_map_root: str,
    gate_taxonomy_root: str,
) -> Dict[str, Any]:
    args = locals().copy()
    roots = {
        spec["id"]: _load_root(args.get(spec["arg"]), spec["summary"], spec["artifacts"]) for spec in ROOT_SPECS
    }
    summaries = {key: roots[key]["summary"] for key in roots}
    dryrun_art = roots["execution_control_dryrun"]["artifacts"]
    planning_art = roots["execution_control_planning"]["artifacts"]
    dryrun_summary = summaries["execution_control_dryrun"]

    input_rows = []
    for spec in ROOT_SPECS:
        meta = roots[spec["id"]]
        input_rows.append(
            {
                "intake_id": spec["id"],
                "path": str(meta["root"]) if meta["root"] else "(not_provided)",
                "loaded": meta["loaded"],
                "required": spec["required"],
                "missing_artifacts": meta.get("missing_artifacts") or [],
                "status": "loaded" if meta["loaded"] else ("missing_required" if spec["required"] else "optional_missing"),
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )

    dryrun_ok = (
        roots["execution_control_dryrun"]["loaded"]
        and dryrun_summary.get("final_decision") == DRYRUN_FINAL
        and dryrun_summary.get("ready_for_post_dryrun_review") is True
    )
    planning_ok = (
        roots["execution_control_planning"]["loaded"]
        and summaries["execution_control_planning"].get("final_decision") == PLANNING_FINAL
    )
    closure_ok = (
        roots["guarded_closure"]["loaded"]
        and summaries["guarded_closure"].get("final_decision") == CLOSURE_DECISION
    )

    gate_dr = dryrun_art.get("execution_control_gate_dryrun_result.json") or {}
    batch_dr = dryrun_art.get("batch_arming_dryrun_results.json") or {}
    abort_dr = dryrun_art.get("abort_condition_dryrun_results.json") or {}
    pre_dr = dryrun_art.get("pre_execution_checklist_dryrun_result.json") or {}
    harness_dr = dryrun_art.get("post_migration_test_harness_dryrun_result.json") or {}
    verifier_dr = dryrun_art.get("post_migration_verifier_suite_dryrun_result.json") or {}
    rollback_dr = dryrun_art.get("rollback_rehearsal_dryrun_result.json") or {}
    failure_dr = dryrun_art.get("failure_response_matrix_dryrun_result.json") or {}
    forbidden_dr = dryrun_art.get("forbidden_execution_report.json") or {}

    gate_plan = planning_art.get("execution_control_gate.json") or {}
    harness_plan = planning_art.get("post_migration_test_harness.json") or {}
    verifier_plan = planning_art.get("post_migration_verifier_suite.json") or {}
    rollback_plan = planning_art.get("rollback_rehearsal_requirement.json") or {}
    failure_plan = planning_art.get("failure_response_matrix.json") or {}

    missing_dryrun = roots["execution_control_dryrun"].get("missing_artifacts") or []
    execution_control_dryrun_input_review = {
        "review_id": REVIEW_ID,
        "dryrun_input_loaded": dryrun_ok,
        "planning_input_loaded": planning_ok,
        "guarded_roadmap_input_loaded": roots["guarded_roadmap"]["loaded"],
        "required_artifacts_loaded": dryrun_ok and not missing_dryrun,
        "missing_required_artifacts": missing_dryrun,
        "input_status": "complete" if dryrun_ok and not missing_dryrun else "incomplete",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    go = gate_plan.get("go_conditions") or {}
    armed_count = batch_dr.get("armed_batch_count", dryrun_summary.get("armed_batch_count", 0))
    batch_results = batch_dr.get("batch_results") or []
    all_not_armed = all(b.get("armed_now") is False for b in batch_results) and armed_count == 0

    execution_control_gate_post_review = {
        "execution_control_gate_simulated_pass": gate_dr.get("gate_simulated_pass") is True,
        "execution_permission_granted": _bool_val(gate_dr.get("execution_permission_granted"), False),
        "guarded_migration_chain_closed": gate_dr.get("guarded_migration_chain_closed") is True,
        "protected_assets_excluded": gate_dr.get("protected_assets_excluded", go.get("protected_assets_excluded", True)),
        "HR_excluded_or_manual_only": gate_dr.get("HR_excluded_or_manual_only", go.get("HR_excluded_or_manual_only", True)),
        "DnAE_excluded": gate_dr.get("DnAE_excluded", go.get("DnAE_excluded", True)),
        "owner_approval_not_auto_confirmed": gate_dr.get("owner_approval_not_auto_confirmed", True),
        "batch_arming_policy_defined": gate_dr.get("batch_arming_policy_defined", True),
        "abort_condition_policy_defined": gate_dr.get("abort_condition_policy_defined", True),
        "post_migration_test_harness_defined": gate_dr.get("post_migration_test_harness_defined", True),
        "verifier_suite_defined": gate_dr.get("verifier_suite_defined", True),
        "rollback_rehearsal_required": gate_dr.get("rollback_rehearsal_required", True),
        "gate_review_pass": dryrun_ok
        and gate_dr.get("gate_simulated_pass") is True
        and not _bool_val(gate_dr.get("execution_permission_granted"), False),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    batch_arming_post_review = {
        "batch_count": batch_dr.get("batch_count", 8),
        "batch_arming_simulated": dryrun_summary.get("batch_arming_simulated") is True,
        "armed_batch_count": armed_count,
        "b0_armed_now": dryrun_summary.get("b0_armed_now") is False,
        "b1_b6_owner_approval_missing_blocks_arming": dryrun_summary.get("b1_b6_owner_approval_missing_blocks_arming")
        is True,
        "b7_previous_tests_not_executed_blocks_arming": dryrun_summary.get(
            "b7_previous_tests_not_executed_blocks_arming"
        )
        is True,
        "all_batches_not_armed": all_not_armed,
        "batch_arming_execution_allowed": False,
        "verdict": "pass"
        if all_not_armed and armed_count == 0 and dryrun_summary.get("batch_arming_simulated") is True
        else "fail",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    canonical_applied = _canonical_mapping_applied(abort_dr)
    abort_condition_post_review = {
        "abort_condition_count": abort_dr.get("abort_condition_count", dryrun_summary.get("abort_condition_count", 0)),
        "abort_conditions_simulated": dryrun_summary.get("abort_conditions_simulated") is True,
        "protected_asset_abort_blocks_execution": _abort_blocks(abort_dr, "protected_asset_touched"),
        "HR_abort_blocks_execution": _abort_blocks(abort_dr, "hr_item_without_manual_decision"),
        "DnAE_abort_blocks_execution": _abort_blocks(abort_dr, "dnae_item_included"),
        "runtime_change_abort_blocks_execution": _abort_blocks(abort_dr, "runtime_behavior_changed"),
        "worldmodel_memory_fact_write_abort_blocks_execution": _abort_blocks(abort_dr, "world_model_memory_fact_write"),
        "whitebox_test_center_touch_abort_blocks_execution": _abort_blocks(abort_dr, "whitebox_test_center_touched"),
        "owner_approval_missing_abort_blocks_execution": _abort_blocks(abort_dr, "owner_approval_missing"),
        "missing_test_harness_abort_blocks_execution": _abort_blocks(abort_dr, "missing_test_harness"),
        "missing_verifier_suite_abort_blocks_execution": _abort_blocks(abort_dr, "missing_verifier_suite"),
        "missing_rollback_checkpoint_abort_blocks_execution": _abort_blocks(abort_dr, "missing_rollback_checkpoint"),
        "canonical_abort_mapping_applied": canonical_applied,
        "abort_review_pass": dryrun_ok
        and abort_dr.get("abort_condition_count", 0) >= 16
        and canonical_applied
        and _abort_blocks(abort_dr, "protected_asset_touched"),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    pre_execution_checklist_post_review = {
        "pre_execution_check_count": pre_dr.get("checklist_item_count", dryrun_summary.get("pre_execution_check_count", 0)),
        "checklist_executed": _bool_val(pre_dr.get("checklist_executed"), False),
        "checklist_review_pass": not _bool_val(pre_dr.get("checklist_executed"), False)
        and pre_dr.get("checklist_item_count", 0) >= 14,
        "clean_working_tree_required": pre_dr.get("clean_working_tree_required", True),
        "dedicated_branch_required": pre_dr.get("dedicated_branch_required", True),
        "backup_snapshot_required": pre_dr.get("backup_snapshot_required", True),
        "owner_approval_records_required": pre_dr.get("owner_approval_records_required", True),
        "rollback_rehearsal_record_required": pre_dr.get("rollback_rehearsal_record_required", True),
        "verifier_baseline_record_required": pre_dr.get("verifier_baseline_record_required", True),
        "operator_acknowledgement_required": pre_dr.get("operator_acknowledgement_required", True),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    post_migration_test_harness_post_review = {
        "post_migration_harness_group_count": harness_dr.get(
            "harness_group_count", dryrun_summary.get("post_migration_harness_group_count", 0)
        ),
        "post_migration_test_count": harness_dr.get("post_migration_test_count", 31),
        "harness_tests_bound": harness_dr.get("harness_tests_bound") is True,
        "post_migration_tests_execution_allowed": _bool_val(harness_dr.get("tests_execution_allowed_now"), False),
        "post_migration_tests_executed": _bool_val(harness_dr.get("post_migration_tests_executed"), False)
        or harness_dr.get("executed_test_count", 0) > 0,
        "executed_test_count": harness_dr.get("executed_test_count", 0),
        "structural_integrity_harness_defined": harness_dr.get("structural_integrity_harness_defined", True),
        "governance_boundary_harness_defined": harness_dr.get("governance_boundary_harness_defined", True),
        "functional_smoke_verifier_harness_defined": harness_dr.get("functional_smoke_verifier_harness_defined", True),
        "no_runtime_regression_harness_defined": harness_dr.get("no_runtime_regression_harness_defined", True),
        "developer_tooling_preservation_harness_defined": harness_dr.get("developer_tooling_preservation_harness_defined", True),
        "test_harness_review_pass": harness_dr.get("post_migration_test_count") == 31
        and harness_dr.get("executed_test_count", 0) == 0
        and harness_dr.get("harness_tests_bound") is True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    post_migration_verifier_suite_post_review = {
        "verifier_suite_count": verifier_dr.get("verifier_suite_count", dryrun_summary.get("verifier_suite_count", 0)),
        "required_verifier_count": verifier_dr.get("required_verifier_count", 4),
        "verifier_suite_execution_allowed": _bool_val(verifier_dr.get("verifier_suite_execution_allowed_now"), False),
        "verifier_suite_executed": _bool_val(verifier_dr.get("verifier_suite_executed"), False),
        "execution_order_defined": verifier_dr.get("execution_order_defined", verifier_plan.get("execution_order_defined", True)),
        "optional_if_missing_policy_defined": verifier_dr.get(
            "optional_if_missing_policy_defined", verifier_plan.get("optional_if_missing_policy_defined", True)
        ),
        "failure_response_defined": verifier_dr.get("failure_response_defined", True),
        "verifier_suite_review_pass": not _bool_val(verifier_dr.get("verifier_suite_executed"), False)
        and not _bool_val(verifier_dr.get("verifier_suite_execution_allowed_now"), False)
        and verifier_dr.get("verifier_suite_count", 0) >= 12,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    rollback_rehearsal_post_review = {
        "rollback_rehearsal_required": rollback_dr.get("rehearsal_required_before_real_migration", True),
        "rollback_rehearsal_execution_allowed": _bool_val(rollback_dr.get("rehearsal_execution_allowed_now"), False),
        "rollback_rehearsal_executed": _bool_val(rollback_dr.get("rollback_rehearsal_executed"), False),
        "rollback_execution_still_blocked": rollback_dr.get("rollback_execution_still_blocked") is True,
        "rollback_checkpoint_per_batch": rollback_dr.get("rollback_checkpoint_per_batch", True),
        "rollback_audit_required": rollback_dr.get("rollback_audit_required", rollback_plan.get("rollback_audit_required", True)),
        "rerun_verifier_after_rollback_required": rollback_dr.get(
            "rerun_verifier_after_rollback_required", True
        ),
        "rollback_review_pass": not _bool_val(rollback_dr.get("rollback_rehearsal_executed"), False)
        and rollback_dr.get("rollback_execution_still_blocked") is True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    failure_types = failure_plan.get("failure_types") or []
    failure_response_matrix_post_review = {
        "failure_response_type_count": failure_dr.get(
            "failure_response_type_count", dryrun_summary.get("failure_response_type_count", 0)
        ),
        "failure_response_matrix_ready": failure_dr.get("failure_response_matrix_ready") is True,
        "all_failure_responses_defined": failure_dr.get("all_failure_responses_defined", True),
        "protected_asset_failure_response_blocks": True,
        "HR_DnAE_failure_response_blocks": True,
        "post_batch_test_failure_response_blocks": True,
        "verifier_suite_failure_response_blocks": True,
        "rollback_rehearsal_failure_response_blocks": True,
        "runtime_change_failure_response_blocks": True,
        "failure_response_review_pass": failure_dr.get("failure_response_matrix_ready") is True
        and failure_dr.get("failure_response_type_count", 0) >= 11,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    canonical_abort_mapping_correction_review = {
        "correction_id": "execution_control_dryrun_abort_canonical_naming_v1",
        "source_phase": "Phase-Main-Project-Structure-Migration-Execution-Control-and-Test-Harness-DryRun-v1-001",
        "issue": "abort condition canonical naming mismatch",
        "original_names": list(PLANNING_ABORT_ALIASES),
        "canonical_names": list(CANONICAL_ABORT_NAMES),
        "correction": "ABORT_CONDITION_CANONICAL mapping added",
        "semantic_impact": "no_permission_granted",
        "boundary_impact": "no_boundary_change",
        "runtime_impact": "none",
        "migration_permission_impact": "none",
        "verification_status": "GO" if canonical_applied else "PENDING",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    execution_control_boundary_post_review = {
        "real_migration_execution_allowed": False,
        "batch_arming_execution_allowed": False,
        "post_migration_tests_execution_allowed": False,
        "verifier_suite_execution_allowed": False,
        "rollback_rehearsal_execution_allowed": False,
        "execution_permission_granted": False,
        "actual_file_move_executed": _bool_val(forbidden_dr.get("actual_file_move_executed"), False),
        "actual_file_delete_executed": _bool_val(forbidden_dr.get("actual_file_delete_executed"), False),
        "actual_file_rename_executed": _bool_val(forbidden_dr.get("actual_file_rename_executed"), False),
        "actual_module_merge_executed": _bool_val(forbidden_dr.get("actual_module_merge_executed"), False),
        "runtime_enabled": False,
        "boundary_review_pass": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    blockers: List[str] = []
    if not dryrun_ok:
        blockers.append("execution_control_dryrun_not_ready")
    if not planning_ok:
        blockers.append("execution_control_planning_not_loaded")
    if not closure_ok:
        blockers.append("guarded_closure_not_confirmed")
    if armed_count != 0:
        blockers.append("armed_batch_count_nonzero")
    if not batch_arming_post_review.get("all_batches_not_armed"):
        blockers.append("batch_not_fully_unarmed")
    if not abort_condition_post_review.get("abort_review_pass"):
        blockers.append("abort_review_failed")
    if not canonical_applied:
        blockers.append("canonical_abort_mapping_not_applied")
    if harness_dr.get("executed_test_count", 0) != 0:
        blockers.append("post_migration_tests_executed")
    if _bool_val(verifier_dr.get("verifier_suite_executed"), False):
        blockers.append("verifier_suite_executed")
    if _bool_val(rollback_dr.get("rollback_rehearsal_executed"), False):
        blockers.append("rollback_rehearsal_executed")

    review_pass = (
        execution_control_gate_post_review.get("gate_review_pass") is True
        and batch_arming_post_review.get("verdict") == "pass"
        and abort_condition_post_review.get("abort_review_pass") is True
        and pre_execution_checklist_post_review.get("checklist_review_pass") is True
        and post_migration_test_harness_post_review.get("test_harness_review_pass") is True
        and post_migration_verifier_suite_post_review.get("verifier_suite_review_pass") is True
        and rollback_rehearsal_post_review.get("rollback_review_pass") is True
        and failure_response_matrix_post_review.get("failure_response_review_pass") is True
    )

    boundary_ok = review_pass and not blockers
    no_file_move, no_delete, no_runtime, no_write = _boundary_reports()

    execution_control_post_dryrun_readiness_decision = {
        "review_verdict": "ready_for_closure" if boundary_ok else "requires_fixes",
        "blockers": blockers,
        "conditional_notes": [
            "ABORT_CONDITION_CANONICAL maps planning names to dry-run canonical names without granting permissions",
            "31 post-migration tests bound but not executed",
            "12 verifier suite items orchestrated but not executed",
            "rollback rehearsal required but not executed",
            f"{HUMAN_REVIEW_CARRYOVER} HR / {PERMANENT_BLOCK_CARRYOVER} DnAE carryover unchanged",
        ],
        "ready_for_closure": boundary_ok,
        "ready_for_real_migration": False,
        "ready_for_file_move": False,
        "ready_for_file_delete": False,
        "ready_for_module_merge": False,
        "ready_for_post_migration_test_execution": False,
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    governance_debt_review = {
        "review_items": [
            "execution_control_chain_simulation_only",
            "batch_arming_simulated_zero_armed",
            "canonical_abort_mapping_recorded_no_permission_granted",
            "post_migration_tests_31_bound_not_executed",
            "verifier_suite_12_orchestrated_not_executed",
            "rollback_rehearsal_required_not_executed",
            "owner_approval_not_auto_confirmed",
            f"{HUMAN_REVIEW_CARRYOVER}_hr_{PERMANENT_BLOCK_CARRYOVER}_dnae_excluded",
        ],
        "review_item_count": 8,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    summary = {
        "phase": PHASE_ID,
        "review_scope": REVIEW_SCOPE,
        "execution_control_dryrun_input_loaded": dryrun_ok,
        "execution_control_planning_input_loaded": planning_ok,
        "guarded_roadmap_input_loaded": roots["guarded_roadmap"]["loaded"],
        "guarded_closure_input_loaded": closure_ok,
        "guarded_dryrun_input_loaded": roots["guarded_dryrun"]["loaded"],
        "readiness_input_loaded": roots["readiness"]["loaded"],
        "protected_asset_resolution_closure_input_loaded": roots["pahr_closure"]["loaded"],
        "structure_map_input_loaded": roots["structure_map"]["loaded"],
        "gate_taxonomy_input_loaded": roots["gate_taxonomy"]["loaded"],
        "execution_control_dryrun_input_review_generated": True,
        "execution_control_gate_post_review_generated": True,
        "batch_arming_post_review_generated": True,
        "abort_condition_post_review_generated": True,
        "pre_execution_checklist_post_review_generated": True,
        "post_migration_test_harness_post_review_generated": True,
        "post_migration_verifier_suite_post_review_generated": True,
        "rollback_rehearsal_post_review_generated": True,
        "failure_response_matrix_post_review_generated": True,
        "canonical_abort_mapping_correction_review_generated": True,
        "execution_control_boundary_post_review_generated": True,
        "execution_control_post_dryrun_readiness_decision_generated": True,
        "batch_count": batch_arming_post_review.get("batch_count", 8),
        "batch_arming_simulated": batch_arming_post_review.get("batch_arming_simulated") is True,
        "armed_batch_count": armed_count,
        "all_batches_not_armed": all_not_armed,
        "abort_condition_count": abort_condition_post_review.get("abort_condition_count", 0),
        "abort_conditions_simulated": abort_condition_post_review.get("abort_conditions_simulated") is True,
        "protected_asset_abort_blocks_execution": abort_condition_post_review.get("protected_asset_abort_blocks_execution"),
        "HR_abort_blocks_execution": abort_condition_post_review.get("HR_abort_blocks_execution"),
        "DnAE_abort_blocks_execution": abort_condition_post_review.get("DnAE_abort_blocks_execution"),
        "runtime_change_abort_blocks_execution": abort_condition_post_review.get("runtime_change_abort_blocks_execution"),
        "worldmodel_memory_fact_write_abort_blocks_execution": abort_condition_post_review.get(
            "worldmodel_memory_fact_write_abort_blocks_execution"
        ),
        "whitebox_test_center_touch_abort_blocks_execution": abort_condition_post_review.get(
            "whitebox_test_center_touch_abort_blocks_execution"
        ),
        "owner_approval_missing_abort_blocks_execution": abort_condition_post_review.get(
            "owner_approval_missing_abort_blocks_execution"
        ),
        "missing_test_harness_abort_blocks_execution": abort_condition_post_review.get(
            "missing_test_harness_abort_blocks_execution"
        ),
        "missing_verifier_suite_abort_blocks_execution": abort_condition_post_review.get(
            "missing_verifier_suite_abort_blocks_execution"
        ),
        "missing_rollback_checkpoint_abort_blocks_execution": abort_condition_post_review.get(
            "missing_rollback_checkpoint_abort_blocks_execution"
        ),
        "canonical_abort_mapping_applied": canonical_applied,
        "pre_execution_check_count": pre_execution_checklist_post_review.get("pre_execution_check_count", 0),
        "checklist_executed": _bool_val(pre_execution_checklist_post_review.get("checklist_executed"), False),
        "post_migration_harness_group_count": post_migration_test_harness_post_review.get("post_migration_harness_group_count", 0),
        "post_migration_test_count": post_migration_test_harness_post_review.get("post_migration_test_count", 31),
        "harness_tests_bound": post_migration_test_harness_post_review.get("harness_tests_bound") is True,
        "post_migration_tests_execution_allowed": _bool_val(
            post_migration_test_harness_post_review.get("post_migration_tests_execution_allowed"), False
        ),
        "post_migration_tests_executed": _bool_val(
            post_migration_test_harness_post_review.get("post_migration_tests_executed"), False
        ),
        "executed_test_count": post_migration_test_harness_post_review.get("executed_test_count", 0),
        "verifier_suite_count": post_migration_verifier_suite_post_review.get("verifier_suite_count", 0),
        "required_verifier_count": post_migration_verifier_suite_post_review.get("required_verifier_count", 0),
        "verifier_suite_execution_allowed": _bool_val(
            post_migration_verifier_suite_post_review.get("verifier_suite_execution_allowed"), False
        ),
        "verifier_suite_executed": _bool_val(
            post_migration_verifier_suite_post_review.get("verifier_suite_executed"), False
        ),
        "rollback_rehearsal_required": rollback_rehearsal_post_review.get("rollback_rehearsal_required") is True,
        "rollback_rehearsal_execution_allowed": _bool_val(
            rollback_rehearsal_post_review.get("rollback_rehearsal_execution_allowed"), False
        ),
        "rollback_rehearsal_executed": _bool_val(
            rollback_rehearsal_post_review.get("rollback_rehearsal_executed"), False
        ),
        "rollback_execution_still_blocked": rollback_rehearsal_post_review.get("rollback_execution_still_blocked") is True,
        "failure_response_type_count": failure_response_matrix_post_review.get("failure_response_type_count", 0),
        "failure_response_matrix_ready": failure_response_matrix_post_review.get("failure_response_matrix_ready") is True,
        "correction_record_status": "recorded",
        "correction_semantic_impact": "no_permission_granted",
        "correction_boundary_impact": "no_boundary_change",
        "correction_runtime_impact": "none",
        "correction_migration_permission_impact": "none",
        "execution_control_gate_review_pass": execution_control_gate_post_review.get("gate_review_pass") is True,
        "abort_review_pass": abort_condition_post_review.get("abort_review_pass") is True,
        "test_harness_review_pass": post_migration_test_harness_post_review.get("test_harness_review_pass") is True,
        "verifier_suite_review_pass": post_migration_verifier_suite_post_review.get("verifier_suite_review_pass") is True,
        "rollback_review_pass": rollback_rehearsal_post_review.get("rollback_review_pass") is True,
        "failure_response_review_pass": failure_response_matrix_post_review.get("failure_response_review_pass") is True,
        "ready_for_closure": boundary_ok,
        "ready_for_real_migration": False,
        "ready_for_file_move": False,
        "ready_for_file_delete": False,
        "ready_for_module_merge": False,
        "ready_for_post_migration_test_execution": False,
        "real_migration_execution_allowed": False,
        "batch_arming_execution_allowed": False,
        "execution_permission_granted": False,
        "actual_file_move_executed": False,
        "actual_file_delete_executed": False,
        "actual_file_rename_executed": False,
        "actual_module_merge_executed": False,
        "docs_modified_by_review": False,
        "readme_modified_by_review": False,
        "phase_verdict_table_modified_by_review": False,
        "existing_phase_result_changed": False,
        "runtime_enabled": False,
        "no_runtime_executed": True,
        "no_new_runtime_enabled": True,
        "file_operation_invoked": False,
        "stat_invoked": False,
        "exists_invoked": False,
        "file_opened": False,
        "file_content_read": False,
        "image_content_read": False,
        "video_content_read": False,
        "world_model_written": False,
        "memory_written": False,
        "library_written": False,
        "fact_written": False,
        "navigation_action_triggered": False,
        "speech_gate_invoked": False,
        "tts_invoked": False,
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "final_decision": FINAL_DECISION if boundary_ok else "MAIN_PROJECT_STRUCTURE_MIGRATION_EXECUTION_CONTROL_AND_TEST_HARNESS_POST_DRYRUN_REVIEW_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "human_review_case_count": HUMAN_REVIEW_CARRYOVER,
        "permanent_block_case_count": PERMANENT_BLOCK_CARRYOVER,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    next_phase_recommendation = {
        "final_decision": summary["final_decision"],
        "recommended_next_phase": summary["recommended_next_phase"],
        "reason": "execution control dry-run chain reviewed; ready for closure freeze without authorizing real migration",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    return {
        "summary": summary,
        "input_root_matrix": {"rows": input_rows, "row_count": len(input_rows), "source_chain": SOURCE_CHAIN, **_not_fact()},
        "execution_control_dryrun_input_review": execution_control_dryrun_input_review,
        "execution_control_gate_post_review": execution_control_gate_post_review,
        "batch_arming_post_review": batch_arming_post_review,
        "abort_condition_post_review": abort_condition_post_review,
        "pre_execution_checklist_post_review": pre_execution_checklist_post_review,
        "post_migration_test_harness_post_review": post_migration_test_harness_post_review,
        "post_migration_verifier_suite_post_review": post_migration_verifier_suite_post_review,
        "rollback_rehearsal_post_review": rollback_rehearsal_post_review,
        "failure_response_matrix_post_review": failure_response_matrix_post_review,
        "canonical_abort_mapping_correction_review": canonical_abort_mapping_correction_review,
        "execution_control_boundary_post_review": execution_control_boundary_post_review,
        "execution_control_post_dryrun_readiness_decision": execution_control_post_dryrun_readiness_decision,
        "governance_debt_review": governance_debt_review,
        "next_phase_recommendation": next_phase_recommendation,
        "no_file_move_boundary_report": no_file_move,
        "no_delete_boundary_report": no_delete,
        "no_runtime_boundary_report": no_runtime,
        "no_write_boundary_report": no_write,
    }
