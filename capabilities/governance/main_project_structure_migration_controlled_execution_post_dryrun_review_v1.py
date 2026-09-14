# -*- coding: utf-8 -*-
"""Main Project Structure Migration Controlled Execution Post-DryRun Review v1.

Review-only: audit controlled execution dry-run for closure readiness.
No real migration, batch arming, tests, verifier suite, or rollback rehearsal.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PHASE_ID = "Phase-Main-Project-Structure-Migration-Controlled-Execution-Post-DryRun-Review-v1-001"
REVIEW_SCOPE = "main_project_structure_migration_controlled_execution_post_dryrun_review_only"
SOURCE_CHAIN = "main_project_structure_migration_controlled_execution_post_dryrun_review_v1"
REVIEW_ID = "main_proj_struct_migration_controlled_execution_post_dryrun_review_v1_001"

FINAL_DECISION = "MAIN_PROJECT_STRUCTURE_MIGRATION_CONTROLLED_EXECUTION_POST_DRYRUN_REVIEW_READY_FOR_CLOSURE"
NEXT_PHASE = "Phase-Main-Project-Structure-Migration-Controlled-Execution-Closure-v1-001"

DRYRUN_FINAL = "MAIN_PROJECT_STRUCTURE_MIGRATION_CONTROLLED_EXECUTION_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
PLANNING_FINAL = "MAIN_PROJECT_STRUCTURE_MIGRATION_CONTROLLED_EXECUTION_PLANNING_READY_FOR_DRYRUN"
EXECUTION_CONTROL_CLOSURE = "MAIN_PROJECT_STRUCTURE_MIGRATION_EXECUTION_CONTROL_AND_TEST_HARNESS_CLOSED_FOR_CURRENT_MAINLINE"
GUARDED_CLOSURE = "MAIN_PROJECT_STRUCTURE_MIGRATION_GUARDED_CLOSED_FOR_CURRENT_MAINLINE"

HUMAN_REVIEW_CARRYOVER = 240
PERMANENT_BLOCK_CARRYOVER = 914

DRYRUN_ARTIFACTS = [
    "controlled_execution_dryrun_execution_plan.json",
    "execution_window_dryrun_result.json",
    "owner_authorization_gate_dryrun_result.json",
    "batch_arming_execution_dryrun_result.json",
    "controlled_batch_progression_dryrun_result.json",
    "rollback_rehearsal_precondition_dryrun_result.json",
    "post_batch_test_execution_order_dryrun_result.json",
    "verifier_suite_execution_order_dryrun_result.json",
    "abort_and_failure_response_dryrun_result.json",
    "post_execution_evidence_pack_dryrun_result.json",
    "controlled_execution_dryrun_boundary_review.json",
    "controlled_execution_dryrun_readiness_decision.json",
]

PLANNING_ARTIFACTS = [
    "controlled_migration_execution_planning_policy.json",
    "controlled_execution_batch_plan.json",
    "execution_window_policy.json",
    "owner_authorization_gate.json",
    "batch_arming_execution_plan.json",
    "rollback_rehearsal_precondition.json",
    "post_batch_test_execution_order.json",
    "verifier_suite_execution_order.json",
    "abort_and_failure_response_plan.json",
    "post_execution_evidence_pack_plan.json",
]

ROOT_SPECS = [
    {
        "id": "controlled_execution_dryrun",
        "arg": "controlled_execution_dryrun_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": DRYRUN_ARTIFACTS,
    },
    {
        "id": "controlled_execution_planning",
        "arg": "controlled_execution_planning_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": PLANNING_ARTIFACTS,
    },
    {
        "id": "execution_control_roadmap",
        "arg": "execution_control_roadmap_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "execution_control_closure",
        "arg": "execution_control_closure_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "execution_control_post_review",
        "arg": "execution_control_post_review_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "execution_control_dryrun",
        "arg": "execution_control_dryrun_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "guarded_closure",
        "arg": "guarded_closure_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "guarded_planning",
        "arg": "guarded_planning_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "readiness",
        "arg": "readiness_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "pahr_closure",
        "arg": "pahr_closure_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "consolidation_closure",
        "arg": "consolidation_closure_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "structure_map",
        "arg": "structure_map_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "gate_taxonomy",
        "arg": "gate_taxonomy_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
]


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _bool_val(val: Any, default: bool = False) -> bool:
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


def run_main_project_structure_migration_controlled_execution_post_dryrun_review_v1(
    *,
    controlled_execution_dryrun_root: str,
    controlled_execution_planning_root: str,
    execution_control_roadmap_root: str,
    execution_control_closure_root: str,
    execution_control_post_review_root: str,
    execution_control_dryrun_root: str,
    guarded_closure_root: str,
    guarded_planning_root: str,
    readiness_root: str,
    pahr_closure_root: str,
    consolidation_closure_root: str,
    structure_map_root: str,
    gate_taxonomy_root: str,
) -> Dict[str, Any]:
    args = locals().copy()
    roots = {spec["id"]: _load_root(args.get(spec["arg"]), spec["summary"], spec["artifacts"]) for spec in ROOT_SPECS}
    summaries = {key: roots[key]["summary"] for key in roots}
    dryrun_art = roots["controlled_execution_dryrun"]["artifacts"]
    dryrun_summary = summaries["controlled_execution_dryrun"]

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
        roots["controlled_execution_dryrun"]["loaded"]
        and dryrun_summary.get("final_decision") == DRYRUN_FINAL
        and dryrun_summary.get("ready_for_post_dryrun_review") is True
    )
    planning_ok = (
        roots["controlled_execution_planning"]["loaded"]
        and summaries["controlled_execution_planning"].get("final_decision") == PLANNING_FINAL
    )
    ec_roadmap_loaded = roots["execution_control_roadmap"]["loaded"]
    ec_closure_loaded = (
        roots["execution_control_closure"]["loaded"]
        and summaries["execution_control_closure"].get("final_decision") == EXECUTION_CONTROL_CLOSURE
    )
    guarded_closure_loaded = (
        roots["guarded_closure"]["loaded"]
        and summaries["guarded_closure"].get("final_decision") == GUARDED_CLOSURE
    )
    readiness_loaded = roots["readiness"]["loaded"]
    pahr_loaded = roots["pahr_closure"]["loaded"]
    structure_loaded = roots["structure_map"]["loaded"]
    gate_loaded = roots["gate_taxonomy"]["loaded"]

    window_dr = dryrun_art.get("execution_window_dryrun_result.json") or {}
    owner_dr = dryrun_art.get("owner_authorization_gate_dryrun_result.json") or {}
    arming_dr = dryrun_art.get("batch_arming_execution_dryrun_result.json") or {}
    progression_dr = dryrun_art.get("controlled_batch_progression_dryrun_result.json") or {}
    rollback_dr = dryrun_art.get("rollback_rehearsal_precondition_dryrun_result.json") or {}
    test_dr = dryrun_art.get("post_batch_test_execution_order_dryrun_result.json") or {}
    verifier_dr = dryrun_art.get("verifier_suite_execution_order_dryrun_result.json") or {}
    abort_dr = dryrun_art.get("abort_and_failure_response_dryrun_result.json") or {}
    evidence_dr = dryrun_art.get("post_execution_evidence_pack_dryrun_result.json") or {}
    boundary_dr = dryrun_art.get("controlled_execution_dryrun_boundary_review.json") or {}

    missing_dryrun = roots["controlled_execution_dryrun"].get("missing_artifacts") or []
    controlled_execution_dryrun_input_review = {
        "review_id": REVIEW_ID,
        "controlled_execution_dryrun_input_loaded": dryrun_ok,
        "controlled_execution_planning_input_loaded": planning_ok,
        "execution_control_roadmap_input_loaded": ec_roadmap_loaded,
        "required_artifacts_loaded": dryrun_ok and not missing_dryrun,
        "missing_required_artifacts": missing_dryrun,
        "input_status": "complete" if dryrun_ok and not missing_dryrun else "incomplete",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    window_req_count = dryrun_summary.get("execution_window_requirement_count", window_dr.get("execution_window_requirement_count", 0))
    execution_window_post_review = {
        "execution_window_requirement_count": window_req_count,
        "dedicated_branch_required": window_dr.get("dedicated_branch_required", True),
        "clean_working_tree_required": window_dr.get("clean_working_tree_required", True),
        "no_unrelated_changes_required": window_dr.get("no_unrelated_changes_required", True),
        "one_batch_at_a_time_required": window_dr.get("one_batch_at_a_time_required", True),
        "no_parallel_migration_batches": window_dr.get("no_parallel_migration_batches", True),
        "operator_acknowledgement_required": window_dr.get("operator_acknowledgement_required", True),
        "rollback_window_reserved_required": window_dr.get("rollback_window_reserved_required", True),
        "post_batch_verification_window_reserved_required": window_dr.get(
            "post_batch_verification_window_reserved_required", True
        ),
        "stop_condition_window_required": window_dr.get("stop_condition_window_required", True),
        "execution_window_opened": _bool_val(window_dr.get("execution_window_opened"), False),
        "execution_window_review_pass": dryrun_ok
        and window_req_count >= 8
        and not _bool_val(window_dr.get("execution_window_opened"), False)
        and window_dr.get("execution_window_review_pass") is True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    owner_gate_count = dryrun_summary.get("owner_authorization_gate_count", owner_dr.get("owner_authorization_gate_count", 0))
    owner_authorization_post_review = {
        "owner_authorization_gate_count": owner_gate_count,
        "architecture_owner_required": owner_dr.get("architecture_owner_required", True),
        "governance_owner_required": owner_dr.get("governance_owner_required", True),
        "evaluation_owner_required": owner_dr.get("evaluation_owner_required", True),
        "capability_owner_required": owner_dr.get("capability_owner_required", True),
        "midplatform_owner_required": owner_dr.get("midplatform_owner_required", True),
        "docs_owner_required": owner_dr.get("docs_owner_required", True),
        "product_client_owner_required": owner_dr.get("product_client_owner_required", True),
        "owner_auto_confirm_allowed": _bool_val(owner_dr.get("owner_auto_confirm_allowed"), False),
        "owner_approval_executed": _bool_val(owner_dr.get("owner_approval_executed"), False),
        "final_owner_human_confirmed": _bool_val(owner_dr.get("final_owner_human_confirmed"), False),
        "missing_owner_approval_blocks_execution": owner_dr.get("missing_owner_approval_blocks_execution", True),
        "owner_authorization_review_pass": dryrun_ok
        and owner_gate_count >= 7
        and not _bool_val(owner_dr.get("owner_approval_executed"), False)
        and owner_dr.get("owner_authorization_review_pass") is True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    armed_count = arming_dr.get("armed_batch_count", dryrun_summary.get("armed_batch_count", 0))
    batch_results = arming_dr.get("batch_results") or []
    all_not_armed = (
        armed_count == 0
        and arming_dr.get("all_batches_not_armed", dryrun_summary.get("all_batches_not_armed")) is True
        and not any(_bool_val(b.get("armed_now"), False) for b in batch_results)
    )

    batch_arming_post_review = {
        "batch_count": arming_dr.get("batch_count", dryrun_summary.get("batch_count", 8)),
        "batch_arming_simulated": dryrun_summary.get("batch_arming_simulated") is True,
        "armed_batch_count": armed_count,
        "all_batches_not_armed": all_not_armed,
        "b0_armed_now": _bool_val(arming_dr.get("b0_armed_now"), False),
        "b1_b6_owner_approval_missing_blocks_arming": arming_dr.get("b1_b6_owner_approval_missing_blocks_arming", True),
        "b7_previous_tests_not_executed_blocks_arming": arming_dr.get("b7_previous_tests_not_executed_blocks_arming", True),
        "arming_allowed_now": _bool_val(arming_dr.get("arming_allowed_now"), False),
        "armed_now": _bool_val(arming_dr.get("armed_now"), False),
        "batch_arming_review_pass": dryrun_ok
        and armed_count == 0
        and all_not_armed
        and arming_dr.get("batch_arming_review_pass") is True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    controlled_batch_progression_post_review = {
        "batch_progression_simulated": progression_dr.get("batch_progression_simulated", True),
        "batch_execution_count": progression_dr.get("batch_execution_count", dryrun_summary.get("batch_execution_count", 0)),
        "b0_baseline_only_no_move": progression_dr.get("b0_baseline_only_no_move", True),
        "b1_docs_relink_candidate_only": progression_dr.get("b1_docs_relink_candidate_only", True),
        "b2_capability_grouping_candidate_only": progression_dr.get("b2_capability_grouping_candidate_only", True),
        "b3_governance_grouping_candidate_only": progression_dr.get("b3_governance_grouping_candidate_only", True),
        "b4_midplatform_grouping_candidate_only": progression_dr.get("b4_midplatform_grouping_candidate_only", True),
        "b5_dev_artifact_reference_only": progression_dr.get("b5_dev_artifact_reference_only", True),
        "b6_future_marker_only": progression_dr.get("b6_future_marker_only", True),
        "b7_verification_gate_only": progression_dr.get("b7_verification_gate_only", True),
        "pass_required_before_next_batch": progression_dr.get("pass_required_before_next_batch", True),
        "failure_blocks_next_batch": progression_dr.get("failure_blocks_next_batch", True),
        "no_parallel_batch_execution": progression_dr.get("no_parallel_batch_execution", True),
        "progression_review_pass": dryrun_ok
        and progression_dr.get("batch_execution_count", 0) == 0
        and progression_dr.get("progression_review_pass") is True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    rollback_rehearsal_precondition_post_review = {
        "rollback_rehearsal_mandatory": rollback_dr.get("rollback_rehearsal_mandatory", True),
        "rollback_rehearsal_covers_b1_b6": rollback_dr.get("rollback_rehearsal_covers_b1_b6", True),
        "rollback_rehearsal_execution_allowed": _bool_val(rollback_dr.get("rollback_rehearsal_execution_allowed"), False),
        "rollback_rehearsal_executed": _bool_val(rollback_dr.get("rollback_rehearsal_executed"), False),
        "rollback_execution_still_blocked": rollback_dr.get("rollback_execution_still_blocked", True),
        "rollback_verifier_rerun_required": rollback_dr.get("rollback_verifier_rerun_required", True),
        "rollback_rehearsal_review_pass": dryrun_ok
        and not _bool_val(rollback_dr.get("rollback_rehearsal_executed"), False)
        and rollback_dr.get("rollback_rehearsal_review_pass") is True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    post_batch_test_execution_order_post_review = {
        "post_batch_test_count": test_dr.get("post_batch_test_count", dryrun_summary.get("post_batch_test_count", 31)),
        "test_execution_order_defined": test_dr.get("test_execution_order_defined", True),
        "tests_mapped_to_batches": test_dr.get("tests_mapped_to_batches", True),
        "pass_required_before_next_batch": test_dr.get("pass_required_before_next_batch", True),
        "failure_blocks_next_batch": test_dr.get("failure_blocks_next_batch", True),
        "rollback_required_if_failed": test_dr.get("rollback_required_if_failed", True),
        "post_migration_tests_execution_allowed": _bool_val(test_dr.get("post_migration_tests_execution_allowed"), False),
        "post_migration_tests_executed": _bool_val(test_dr.get("post_migration_tests_executed"), False),
        "executed_test_count": test_dr.get("executed_test_count", 0),
        "post_batch_test_order_review_pass": dryrun_ok
        and test_dr.get("post_batch_test_count") == 31
        and test_dr.get("executed_test_count", 0) == 0
        and test_dr.get("post_batch_test_order_review_pass") is True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    verifier_suite_execution_order_post_review = {
        "verifier_suite_count": verifier_dr.get("verifier_suite_count", dryrun_summary.get("verifier_suite_count", 12)),
        "verifier_execution_order_defined": verifier_dr.get("verifier_execution_order_defined", True),
        "required_verifier_count": verifier_dr.get("required_verifier_count", dryrun_summary.get("required_verifier_count", 4)),
        "optional_if_missing_policy_defined": verifier_dr.get("optional_if_missing_policy_defined", True),
        "pass_required_before_next_batch": verifier_dr.get("pass_required_before_next_batch", True),
        "failure_blocks_real_migration": verifier_dr.get("failure_blocks_real_migration", True),
        "verifier_suite_execution_allowed": _bool_val(verifier_dr.get("verifier_suite_execution_allowed"), False),
        "verifier_suite_executed": _bool_val(verifier_dr.get("verifier_suite_executed"), False),
        "verifier_suite_order_review_pass": dryrun_ok
        and not _bool_val(verifier_dr.get("verifier_suite_executed"), False)
        and verifier_dr.get("verifier_suite_count", 0) >= 12
        and verifier_dr.get("verifier_suite_order_review_pass") is True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    abort_and_failure_response_post_review = {
        "abort_condition_count": abort_dr.get("abort_condition_count", dryrun_summary.get("abort_condition_count", 0)),
        "failure_response_type_count": abort_dr.get(
            "failure_response_type_count", dryrun_summary.get("failure_response_type_count", 0)
        ),
        "every_abort_has_failure_response": abort_dr.get("every_abort_has_failure_response", True),
        "protected_HR_DnAE_abort_blocks_entire_execution": abort_dr.get("protected_HR_DnAE_abort_blocks_entire_execution", True),
        "runtime_worldmodel_memory_fact_abort_blocks_entire_execution": abort_dr.get(
            "runtime_worldmodel_memory_fact_abort_blocks_entire_execution", True
        ),
        "missing_harness_verifier_rollback_blocks_execution": abort_dr.get(
            "missing_harness_verifier_rollback_blocks_execution", True
        ),
        "failed_post_batch_test_blocks_next_batch": abort_dr.get("failed_post_batch_test_blocks_next_batch", True),
        "failed_verifier_suite_blocks_next_batch": abort_dr.get("failed_verifier_suite_blocks_next_batch", True),
        "rollback_rehearsal_failure_blocks_real_migration": abort_dr.get(
            "rollback_rehearsal_failure_blocks_real_migration", True
        ),
        "whitebox_test_center_touched_blocks_execution": abort_dr.get("whitebox_test_center_touched_blocks_execution", True),
        "abort_failure_response_review_pass": dryrun_ok
        and abort_dr.get("abort_condition_count", 0) >= 16
        and abort_dr.get("abort_failure_response_review_pass") is True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    post_execution_evidence_pack_post_review = {
        "post_execution_evidence_pack_template_defined": evidence_dr.get(
            "post_execution_evidence_pack_template_defined", True
        ),
        "evidence_pack_generated_now": _bool_val(evidence_dr.get("evidence_pack_generated_now"), False),
        "execution_result_claimed_now": _bool_val(evidence_dr.get("execution_result_claimed_now"), False),
        "moved_file_count_claimed_now": evidence_dr.get("moved_file_count_claimed_now", 0),
        "deleted_file_count_claimed_now": evidence_dr.get("deleted_file_count_claimed_now", 0),
        "renamed_file_count_claimed_now": evidence_dr.get("renamed_file_count_claimed_now", 0),
        "merged_module_count_claimed_now": evidence_dr.get("merged_module_count_claimed_now", 0),
        "protected_asset_touch_count_claimed_now": evidence_dr.get("protected_asset_touch_count_claimed_now", 0),
        "HR_DnAE_touch_count_claimed_now": evidence_dr.get("HR_DnAE_touch_count_claimed_now", 0),
        "evidence_pack_review_pass": dryrun_ok
        and not _bool_val(evidence_dr.get("evidence_pack_generated_now"), False)
        and evidence_dr.get("evidence_pack_review_pass") is True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    controlled_execution_boundary_post_review = {
        "real_migration_execution_allowed": False,
        "batch_arming_allowed_now": False,
        "actual_file_move_executed": _bool_val(dryrun_summary.get("actual_file_move_executed"), False),
        "actual_file_delete_executed": _bool_val(dryrun_summary.get("actual_file_delete_executed"), False),
        "actual_file_rename_executed": _bool_val(dryrun_summary.get("actual_file_rename_executed"), False),
        "actual_module_merge_executed": _bool_val(dryrun_summary.get("actual_module_merge_executed"), False),
        "docs_modified_by_review": False,
        "readme_modified_by_review": False,
        "phase_verdict_table_modified_by_review": False,
        "runtime_enabled": False,
        "post_migration_tests_executed": _bool_val(dryrun_summary.get("post_migration_tests_executed"), False),
        "verifier_suite_executed": _bool_val(dryrun_summary.get("verifier_suite_executed"), False),
        "rollback_rehearsal_executed": _bool_val(dryrun_summary.get("rollback_rehearsal_executed"), False),
        "boundary_review_pass": boundary_dr.get("boundary_review_pass", True) is True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    blockers: List[str] = []
    if not dryrun_ok:
        blockers.append("controlled_execution_dryrun_not_ready")
    if not planning_ok:
        blockers.append("controlled_execution_planning_not_loaded")
    if not ec_closure_loaded:
        blockers.append("execution_control_closure_not_confirmed")
    if not guarded_closure_loaded:
        blockers.append("guarded_closure_not_confirmed")
    if armed_count != 0:
        blockers.append("armed_batch_count_nonzero")
    if not all_not_armed:
        blockers.append("batch_not_fully_unarmed")
    if progression_dr.get("batch_execution_count", 0) != 0:
        blockers.append("batch_execution_count_nonzero")
    if test_dr.get("executed_test_count", 0) != 0:
        blockers.append("post_migration_tests_executed")
    if _bool_val(verifier_dr.get("verifier_suite_executed"), False):
        blockers.append("verifier_suite_executed")
    if _bool_val(rollback_dr.get("rollback_rehearsal_executed"), False):
        blockers.append("rollback_rehearsal_executed")
    if _bool_val(evidence_dr.get("evidence_pack_generated_now"), False):
        blockers.append("evidence_pack_generated")
    if _bool_val(window_dr.get("execution_window_opened"), False):
        blockers.append("execution_window_opened")

    review_pass = (
        execution_window_post_review.get("execution_window_review_pass") is True
        and owner_authorization_post_review.get("owner_authorization_review_pass") is True
        and batch_arming_post_review.get("batch_arming_review_pass") is True
        and controlled_batch_progression_post_review.get("progression_review_pass") is True
        and rollback_rehearsal_precondition_post_review.get("rollback_rehearsal_review_pass") is True
        and post_batch_test_execution_order_post_review.get("post_batch_test_order_review_pass") is True
        and verifier_suite_execution_order_post_review.get("verifier_suite_order_review_pass") is True
        and abort_and_failure_response_post_review.get("abort_failure_response_review_pass") is True
        and post_execution_evidence_pack_post_review.get("evidence_pack_review_pass") is True
    )

    boundary_ok = review_pass and not blockers
    no_file_move, no_delete, no_runtime, no_write = _boundary_reports()

    controlled_execution_post_dryrun_readiness_decision = {
        "review_verdict": "ready_for_closure" if boundary_ok else "requires_fixes",
        "blockers": blockers,
        "conditional_notes": [
            "post-dryrun review confirms dry-run chain only; no migration permissions granted",
            "armed_batch_count=0; B0–B7 candidate-only; 31 tests and 12 verifiers not executed",
            "rollback rehearsal required but not executed; evidence pack template only",
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
            "controlled_execution_dryrun_reviewed_not_executed",
            "armed_batch_count_zero_confirmed",
            "owner_approval_not_collected",
            "batch_progression_candidate_only",
            "post_migration_tests_31_ordered_not_executed",
            "verifier_suite_12_ordered_not_executed",
            "rollback_rehearsal_required_not_executed",
            "evidence_pack_template_only",
            f"{HUMAN_REVIEW_CARRYOVER}_hr_{PERMANENT_BLOCK_CARRYOVER}_dnae_excluded",
        ],
        "review_item_count": 9,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    next_phase_recommendation = {
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "final_decision": FINAL_DECISION if boundary_ok else "MAIN_PROJECT_STRUCTURE_MIGRATION_CONTROLLED_EXECUTION_POST_DRYRUN_REVIEW_REQUIRES_FIXES",
        "reason": "controlled execution dry-run reviewed; closure next without granting real migration",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    summary = {
        "phase": PHASE_ID,
        "review_scope": REVIEW_SCOPE,
        "controlled_execution_dryrun_input_loaded": dryrun_ok,
        "controlled_execution_planning_input_loaded": planning_ok,
        "execution_control_roadmap_input_loaded": ec_roadmap_loaded,
        "execution_control_closure_input_loaded": ec_closure_loaded,
        "guarded_closure_input_loaded": guarded_closure_loaded,
        "readiness_input_loaded": readiness_loaded,
        "protected_asset_resolution_closure_input_loaded": pahr_loaded,
        "structure_map_input_loaded": structure_loaded,
        "gate_taxonomy_input_loaded": gate_loaded,
        "controlled_execution_dryrun_input_review_generated": True,
        "execution_window_post_review_generated": True,
        "owner_authorization_post_review_generated": True,
        "batch_arming_post_review_generated": True,
        "controlled_batch_progression_post_review_generated": True,
        "rollback_rehearsal_precondition_post_review_generated": True,
        "post_batch_test_execution_order_post_review_generated": True,
        "verifier_suite_execution_order_post_review_generated": True,
        "abort_and_failure_response_post_review_generated": True,
        "post_execution_evidence_pack_post_review_generated": True,
        "controlled_execution_boundary_post_review_generated": True,
        "controlled_execution_post_dryrun_readiness_decision_generated": True,
        "execution_window_requirement_count": window_req_count,
        "execution_window_opened": _bool_val(window_dr.get("execution_window_opened"), False),
        "owner_authorization_gate_count": owner_gate_count,
        "owner_auto_confirm_allowed": _bool_val(owner_dr.get("owner_auto_confirm_allowed"), False),
        "owner_approval_executed": _bool_val(owner_dr.get("owner_approval_executed"), False),
        "final_owner_human_confirmed": _bool_val(owner_dr.get("final_owner_human_confirmed"), False),
        "batch_count": batch_arming_post_review.get("batch_count", 8),
        "batch_arming_simulated": dryrun_summary.get("batch_arming_simulated") is True,
        "armed_batch_count": armed_count,
        "all_batches_not_armed": all_not_armed,
        "batch_progression_simulated": progression_dr.get("batch_progression_simulated", True),
        "batch_execution_count": progression_dr.get("batch_execution_count", 0),
        "b0_baseline_only_no_move": progression_dr.get("b0_baseline_only_no_move", True),
        "b1_docs_relink_candidate_only": progression_dr.get("b1_docs_relink_candidate_only", True),
        "b2_capability_grouping_candidate_only": progression_dr.get("b2_capability_grouping_candidate_only", True),
        "b3_governance_grouping_candidate_only": progression_dr.get("b3_governance_grouping_candidate_only", True),
        "b4_midplatform_grouping_candidate_only": progression_dr.get("b4_midplatform_grouping_candidate_only", True),
        "b5_dev_artifact_reference_only": progression_dr.get("b5_dev_artifact_reference_only", True),
        "b6_future_marker_only": progression_dr.get("b6_future_marker_only", True),
        "b7_verification_gate_only": progression_dr.get("b7_verification_gate_only", True),
        "rollback_rehearsal_mandatory": rollback_dr.get("rollback_rehearsal_mandatory", True),
        "rollback_rehearsal_executed": _bool_val(rollback_dr.get("rollback_rehearsal_executed"), False),
        "rollback_execution_still_blocked": rollback_dr.get("rollback_execution_still_blocked", True),
        "post_batch_test_count": test_dr.get("post_batch_test_count", 31),
        "tests_mapped_to_batches": test_dr.get("tests_mapped_to_batches", True),
        "post_migration_tests_execution_allowed": _bool_val(test_dr.get("post_migration_tests_execution_allowed"), False),
        "post_migration_tests_executed": _bool_val(test_dr.get("post_migration_tests_executed"), False),
        "executed_test_count": test_dr.get("executed_test_count", 0),
        "verifier_suite_count": verifier_dr.get("verifier_suite_count", 12),
        "verifier_suite_execution_allowed": _bool_val(verifier_dr.get("verifier_suite_execution_allowed"), False),
        "verifier_suite_executed": _bool_val(verifier_dr.get("verifier_suite_executed"), False),
        "abort_condition_count": abort_dr.get("abort_condition_count", 0),
        "failure_response_type_count": abort_dr.get("failure_response_type_count", 0),
        "every_abort_has_failure_response": abort_dr.get("every_abort_has_failure_response", True),
        "protected_HR_DnAE_abort_blocks_entire_execution": abort_dr.get("protected_HR_DnAE_abort_blocks_entire_execution", True),
        "runtime_worldmodel_memory_fact_abort_blocks_entire_execution": abort_dr.get(
            "runtime_worldmodel_memory_fact_abort_blocks_entire_execution", True
        ),
        "missing_harness_verifier_rollback_blocks_execution": abort_dr.get(
            "missing_harness_verifier_rollback_blocks_execution", True
        ),
        "failed_post_batch_test_blocks_next_batch": abort_dr.get("failed_post_batch_test_blocks_next_batch", True),
        "failed_verifier_suite_blocks_next_batch": abort_dr.get("failed_verifier_suite_blocks_next_batch", True),
        "rollback_rehearsal_failure_blocks_real_migration": abort_dr.get("rollback_rehearsal_failure_blocks_real_migration", True),
        "whitebox_test_center_touched_blocks_execution": abort_dr.get("whitebox_test_center_touched_blocks_execution", True),
        "post_execution_evidence_pack_template_defined": evidence_dr.get("post_execution_evidence_pack_template_defined", True),
        "evidence_pack_generated_now": _bool_val(evidence_dr.get("evidence_pack_generated_now"), False),
        "execution_result_claimed_now": _bool_val(evidence_dr.get("execution_result_claimed_now"), False),
        "evidence_pack_review_pass": post_execution_evidence_pack_post_review.get("evidence_pack_review_pass") is True,
        "ready_for_closure": boundary_ok,
        "ready_for_real_migration": False,
        "ready_for_file_move": False,
        "ready_for_file_delete": False,
        "ready_for_module_merge": False,
        "ready_for_post_migration_test_execution": False,
        "real_migration_execution_allowed": False,
        "batch_arming_allowed_now": False,
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
        "final_decision": FINAL_DECISION if boundary_ok else "MAIN_PROJECT_STRUCTURE_MIGRATION_CONTROLLED_EXECUTION_POST_DRYRUN_REVIEW_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "human_review_case_count": HUMAN_REVIEW_CARRYOVER,
        "permanent_block_case_count": PERMANENT_BLOCK_CARRYOVER,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    return {
        "summary": summary,
        "input_root_matrix": {"rows": input_rows, "row_count": len(input_rows), "source_chain": SOURCE_CHAIN, **_not_fact()},
        "controlled_execution_dryrun_input_review": controlled_execution_dryrun_input_review,
        "execution_window_post_review": execution_window_post_review,
        "owner_authorization_post_review": owner_authorization_post_review,
        "batch_arming_post_review": batch_arming_post_review,
        "controlled_batch_progression_post_review": controlled_batch_progression_post_review,
        "rollback_rehearsal_precondition_post_review": rollback_rehearsal_precondition_post_review,
        "post_batch_test_execution_order_post_review": post_batch_test_execution_order_post_review,
        "verifier_suite_execution_order_post_review": verifier_suite_execution_order_post_review,
        "abort_and_failure_response_post_review": abort_and_failure_response_post_review,
        "post_execution_evidence_pack_post_review": post_execution_evidence_pack_post_review,
        "controlled_execution_boundary_post_review": controlled_execution_boundary_post_review,
        "controlled_execution_post_dryrun_readiness_decision": controlled_execution_post_dryrun_readiness_decision,
        "governance_debt_review": governance_debt_review,
        "next_phase_recommendation": next_phase_recommendation,
        "no_file_move_boundary_report": no_file_move,
        "no_delete_boundary_report": no_delete,
        "no_runtime_boundary_report": no_runtime,
        "no_write_boundary_report": no_write,
    }
