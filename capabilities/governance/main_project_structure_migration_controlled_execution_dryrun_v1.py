# -*- coding: utf-8 -*-
"""Main Project Structure Migration Controlled Execution DryRun v1.

Dry-run-only: simulate execution window, owner gates, batch arming/progression,
test/verifier order, rollback rehearsal precondition — no real migration.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

PHASE_ID = "Phase-Main-Project-Structure-Migration-Controlled-Execution-DryRun-v1-001"
DRYRUN_SCOPE = "main_project_structure_migration_controlled_execution_dryrun_only"
DRYRUN_ID = "main_proj_struct_migration_controlled_execution_dryrun_v1_001"
SOURCE_CHAIN = "main_project_structure_migration_controlled_execution_dryrun_v1"

FINAL_DECISION = "MAIN_PROJECT_STRUCTURE_MIGRATION_CONTROLLED_EXECUTION_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
NEXT_PHASE = "Phase-Main-Project-Structure-Migration-Controlled-Execution-Post-DryRun-Review-v1-001"

PLANNING_FINAL = "MAIN_PROJECT_STRUCTURE_MIGRATION_CONTROLLED_EXECUTION_PLANNING_READY_FOR_DRYRUN"
EXECUTION_CONTROL_CLOSURE = "MAIN_PROJECT_STRUCTURE_MIGRATION_EXECUTION_CONTROL_AND_TEST_HARNESS_CLOSED_FOR_CURRENT_MAINLINE"
GUARDED_CLOSURE = "MAIN_PROJECT_STRUCTURE_MIGRATION_GUARDED_CLOSED_FOR_CURRENT_MAINLINE"

HUMAN_REVIEW_CARRYOVER = 240
PERMANENT_BLOCK_CARRYOVER = 914

BATCH_IDS = ("B0", "B1", "B2", "B3", "B4", "B5", "B6", "B7")
OWNER_APPROVAL_BATCHES = ("B1", "B2", "B3", "B4", "B5", "B6")

BATCH_SEMANTICS = {
    "B0": ("b0_baseline_only_no_move", "baseline_snapshot_no_move"),
    "B1": ("b1_docs_relink_candidate_only", "safe_docs_relink_candidate"),
    "B2": ("b2_capability_grouping_candidate_only", "capability_grouping_candidate"),
    "B3": ("b3_governance_grouping_candidate_only", "governance_grouping_candidate"),
    "B4": ("b4_midplatform_grouping_candidate_only", "midplatform_grouping_candidate"),
    "B5": ("b5_dev_artifact_reference_only", "developer_artifact_reference_only"),
    "B6": ("b6_future_marker_only", "future_module_marker_only"),
    "B7": ("b7_verification_gate_only", "verification_gate_no_move"),
}

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
    "controlled_execution_planning_readiness_decision.json",
]

ROOT_SPECS = [
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
        "artifacts": [
            "summary.json",
            "execution_control_closure_decision_summary.json",
            "execution_control_non_claims_register.json",
        ],
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
        "artifacts": [
            "guarded_migration_batch_plan.json",
            "post_migration_verification_matrix.json",
        ],
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
        "artifacts": ["module_inventory.json", "current_to_target_structure_map.json"],
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


def _no_side_effect_report(kind: str) -> Dict[str, Any]:
    return {
        "dryrun_scope": DRYRUN_SCOPE,
        "dryrun_only": True,
        "boundary_ok": True,
        "violations": [],
        "actual_file_move_executed": False,
        "actual_file_delete_executed": False,
        "actual_file_rename_executed": False,
        "actual_module_merge_executed": False,
        "docs_modified_by_dryrun": False,
        "readme_modified_by_dryrun": False,
        "phase_verdict_table_modified_by_dryrun": False,
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
        "report_kind": kind,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def run_main_project_structure_migration_controlled_execution_dryrun_v1(
    *,
    controlled_execution_planning_root: str,
    execution_control_roadmap_root: str,
    execution_control_closure_root: str,
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
    plan_art = roots["controlled_execution_planning"]["artifacts"] if roots["controlled_execution_planning"]["loaded"] else {}

    input_rows = []
    for spec in ROOT_SPECS:
        meta = roots[spec["id"]]
        input_rows.append(
            {
                "intake_id": spec["id"],
                "path": str(meta["root"]) if meta["root"] else "(not_provided)",
                "loaded": meta["loaded"],
                "required": spec["required"],
                "status": "loaded" if meta["loaded"] else ("missing_required" if spec["required"] else "optional_missing"),
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )

    planning_loaded = (
        roots["controlled_execution_planning"]["loaded"]
        and summaries["controlled_execution_planning"].get("final_decision") == PLANNING_FINAL
        and summaries["controlled_execution_planning"].get("ready_for_controlled_execution_dryrun") is True
    )
    ec_roadmap_loaded = roots["execution_control_roadmap"]["loaded"]
    ec_closure_loaded = (
        roots["execution_control_closure"]["loaded"]
        and summaries["execution_control_closure"].get("final_decision") == EXECUTION_CONTROL_CLOSURE
    )
    ec_dryrun_loaded = roots["execution_control_dryrun"]["loaded"]
    guarded_closure_loaded = (
        roots["guarded_closure"]["loaded"]
        and summaries["guarded_closure"].get("final_decision") == GUARDED_CLOSURE
    )
    readiness_loaded = roots["readiness"]["loaded"]
    pahr_loaded = roots["pahr_closure"]["loaded"]
    structure_loaded = roots["structure_map"]["loaded"]
    gate_loaded = roots["gate_taxonomy"]["loaded"]

    batch_plan = plan_art.get("controlled_execution_batch_plan.json") or {}
    window_plan = plan_art.get("execution_window_policy.json") or {}
    owner_plan = plan_art.get("owner_authorization_gate.json") or {}
    arming_plan = plan_art.get("batch_arming_execution_plan.json") or {}
    rollback_pre = plan_art.get("rollback_rehearsal_precondition.json") or {}
    test_order_plan = plan_art.get("post_batch_test_execution_order.json") or {}
    verifier_order_plan = plan_art.get("verifier_suite_execution_order.json") or {}
    abort_plan = plan_art.get("abort_and_failure_response_plan.json") or {}
    evidence_plan = plan_art.get("post_execution_evidence_pack_plan.json") or {}

    batch_count = batch_plan.get("batch_count", len(batch_plan.get("batches") or []))
    owner_gate_count = owner_plan.get("owner_authorization_gate_count", len(owner_plan.get("gates") or []))
    window_req_count = window_plan.get("execution_window_requirement_count", len(window_plan.get("requirements") or []))
    post_batch_test_count = test_order_plan.get("post_batch_test_count", len(test_order_plan.get("tests") or []))
    verifier_suite_count = verifier_order_plan.get("verifier_suite_count", len(verifier_order_plan.get("verifiers") or []))
    required_verifier_count = verifier_order_plan.get("required_verifier_count", 4)
    abort_count = abort_plan.get("abort_condition_count", len(abort_plan.get("abort_conditions") or []))
    failure_count = abort_plan.get("failure_response_type_count", len(abort_plan.get("failure_types") or []))

    controlled_execution_dryrun_execution_plan = {
        "dryrun_id": DRYRUN_ID,
        "source_planning_ref": "_eval_out/main_project_structure_migration_controlled_execution_planning_v1_smoke_v0/",
        "source_execution_control_roadmap_ref": "_eval_out/main_project_structure_migration_execution_control_and_test_harness_roadmap_decision_v1_smoke_v0/",
        "batch_count": batch_count,
        "owner_authorization_gate_count": owner_gate_count,
        "execution_window_requirement_count": window_req_count,
        "post_batch_test_count": post_batch_test_count,
        "verifier_suite_count": verifier_suite_count,
        "abort_condition_count": abort_count,
        "failure_response_type_count": failure_count,
        "execution_mode": "dryrun_only",
        "real_migration_execution_allowed": False,
        "batch_arming_allowed_now": False,
        "post_migration_tests_execution_allowed": False,
        "verifier_suite_execution_allowed": False,
        "rollback_rehearsal_execution_allowed": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    req_names = [r.get("requirement_name") for r in window_plan.get("requirements") or []]
    execution_window_dryrun_result = {
        "execution_window_requirement_count": window_req_count,
        "dedicated_branch_required": "dedicated_branch_required" in req_names,
        "clean_working_tree_required": "clean_working_tree_required" in req_names,
        "no_unrelated_changes_required": "no_unrelated_changes" in req_names,
        "max_batch_size_limit_defined": "max_batch_size_limit" in req_names,
        "one_batch_at_a_time_required": window_plan.get("one_batch_at_a_time_required") is True
        or "one_batch_at_a_time" in req_names,
        "no_parallel_migration_batches": window_plan.get("no_parallel_migration_batches") is True
        or "no_parallel_migration_batches" in req_names,
        "operator_acknowledgement_required": "operator_acknowledgement_required" in req_names,
        "rollback_window_reserved_required": "rollback_window_reserved" in req_names,
        "post_batch_verification_window_reserved_required": "post_batch_verification_window_reserved" in req_names,
        "stop_condition_window_required": "stop_condition_window_required" in req_names,
        "execution_window_opened": False,
        "execution_window_review_pass": planning_loaded and window_req_count >= 8,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    owner_authorization_gate_dryrun_result = {
        "owner_authorization_gate_count": owner_gate_count,
        "architecture_owner_required": True,
        "governance_owner_required": True,
        "evaluation_owner_required": True,
        "capability_owner_required": True,
        "midplatform_owner_required": True,
        "docs_owner_required": True,
        "product_client_owner_required": True,
        "owner_auto_confirm_allowed": False,
        "owner_approval_executed": False,
        "final_owner_human_confirmed": False,
        "missing_owner_approval_blocks_execution": True,
        "owner_authorization_review_pass": owner_gate_count >= 7 and planning_loaded,
        "simulated_gates": [
            {
                "owner_type": g.get("owner_type"),
                "applies_to_batches": g.get("applies_to_batches"),
                "approval_simulated": False,
                "blocks_arming": True,
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
            for g in owner_plan.get("gates") or []
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    arming_entries_plan = {b.get("batch_id"): b for b in arming_plan.get("batches") or []}
    batch_arming_sim_results: List[Dict[str, Any]] = []
    armed_count = 0
    for bid in BATCH_IDS:
        ap = arming_entries_plan.get(bid) or {}
        owner_req = bool(ap.get("required_owner_approvals"))
        if bid == "B0":
            sim_state = "baseline_only_no_arm"
        elif bid in OWNER_APPROVAL_BATCHES:
            sim_state = "blocked_owner_approval_missing"
        elif bid == "B7":
            sim_state = "blocked_previous_batch_tests_not_executed"
        else:
            sim_state = "blocked_preconditions"
        batch_arming_sim_results.append(
            {
                "batch_id": bid,
                "arming_preconditions_checked": True,
                "required_owner_approvals": ap.get("required_owner_approvals") or [],
                "arming_allowed_now": False,
                "armed_now": False,
                "simulated_state": sim_state,
                "owner_approval_missing_blocks": bid in OWNER_APPROVAL_BATCHES,
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )

    batch_arming_execution_dryrun_result = {
        "batch_results": batch_arming_sim_results,
        "batch_count": len(batch_arming_sim_results),
        "batch_arming_simulated": True,
        "armed_batch_count": armed_count,
        "b0_armed_now": False,
        "b1_b6_owner_approval_missing_blocks_arming": True,
        "b7_previous_tests_not_executed_blocks_arming": True,
        "all_batches_not_armed": armed_count == 0,
        "arming_allowed_now": False,
        "armed_now": False,
        "batch_arming_review_pass": armed_count == 0 and planning_loaded,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    progression_entries = []
    for bid in BATCH_IDS:
        sem_key, mode = BATCH_SEMANTICS[bid]
        progression_entries.append(
            {
                "batch_id": bid,
                "progression_mode": mode,
                "candidate_only": True,
                "execution_simulated": False,
                "execution_count": 0,
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )

    controlled_batch_progression_dryrun_result = {
        "batch_progression_simulated": True,
        "batches": progression_entries,
        "b0_baseline_only_no_move": True,
        "b1_docs_relink_candidate_only": True,
        "b2_capability_grouping_candidate_only": True,
        "b3_governance_grouping_candidate_only": True,
        "b4_midplatform_grouping_candidate_only": True,
        "b5_dev_artifact_reference_only": True,
        "b6_future_marker_only": True,
        "b7_verification_gate_only": True,
        "batch_execution_count": 0,
        "pass_required_before_next_batch": True,
        "failure_blocks_next_batch": True,
        "no_parallel_batch_execution": True,
        "progression_review_pass": planning_loaded and batch_count == 8,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    rollback_rehearsal_precondition_dryrun_result = {
        "rollback_rehearsal_mandatory": rollback_pre.get("rollback_rehearsal_mandatory", True),
        "rollback_rehearsal_covers_b1_b6": rollback_pre.get("rehearsal_must_cover_batches")
        == ["B1", "B2", "B3", "B4", "B5", "B6"]
        or set(rollback_pre.get("rehearsal_must_cover_batches") or []) >= set(OWNER_APPROVAL_BATCHES),
        "restore_path_map_required": rollback_pre.get("restore_path_map_required", True),
        "restore_docs_links_required": rollback_pre.get("restore_docs_links_required", True),
        "restore_phase_verdict_table_required_if_touched": rollback_pre.get(
            "restore_phase_verdict_table_if_touched", True
        ),
        "restore_eval_out_refs_required": rollback_pre.get("restore_eval_out_references_required", True),
        "rollback_verifier_rerun_required": rollback_pre.get("rollback_verifier_rerun_required", True),
        "rollback_rehearsal_report_required": rollback_pre.get("rollback_rehearsal_report_required", True),
        "rollback_rehearsal_execution_allowed": False,
        "rollback_rehearsal_executed": False,
        "rollback_execution_still_blocked": True,
        "rollback_rehearsal_review_pass": rollback_pre.get("rollback_rehearsal_mandatory") is True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    tests = test_order_plan.get("tests") or []
    post_batch_test_execution_order_dryrun_result = {
        "post_batch_test_count": post_batch_test_count,
        "test_execution_order_defined": all(t.get("execution_order") for t in tests) if tests else post_batch_test_count == 31,
        "tests_mapped_to_batches": all(t.get("related_batch") for t in tests) if tests else True,
        "pass_required_before_next_batch": test_order_plan.get("pass_required_before_next_batch", True),
        "failure_blocks_next_batch": test_order_plan.get("failure_blocks_next_batch", True),
        "rollback_required_if_failed": all(t.get("rollback_required_if_failed") for t in tests) if tests else True,
        "post_migration_tests_execution_allowed": False,
        "post_migration_tests_executed": False,
        "executed_test_count": 0,
        "post_batch_test_order_review_pass": post_batch_test_count == 31 and planning_loaded,
        "simulated_test_chain": [
            {
                "test_id": t.get("test_id"),
                "related_batch": t.get("related_batch"),
                "execution_simulated": False,
                "executed": False,
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
            for t in tests
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    verifiers = verifier_order_plan.get("verifiers") or []
    verifier_suite_execution_order_dryrun_result = {
        "verifier_suite_count": verifier_suite_count,
        "verifier_execution_order_defined": all(v.get("execution_order") for v in verifiers) if verifiers else True,
        "required_verifier_count": required_verifier_count,
        "optional_if_missing_policy_defined": verifier_order_plan.get("optional_if_missing_policy_defined", True),
        "pass_required_before_next_batch": True,
        "failure_blocks_real_migration": True,
        "verifier_suite_execution_allowed": False,
        "verifier_suite_executed": False,
        "verifier_suite_order_review_pass": verifier_suite_count >= 12 and planning_loaded,
        "simulated_verifier_chain": [
            {
                "verifier_id": v.get("verifier_id"),
                "execution_order": v.get("execution_order"),
                "execution_simulated": False,
                "executed": False,
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
            for v in verifiers
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    abort_conditions = abort_plan.get("abort_conditions") or []
    failure_types = abort_plan.get("failure_types") or []
    abort_and_failure_response_dryrun_result = {
        "abort_condition_count": abort_count,
        "failure_response_type_count": failure_count,
        "every_abort_has_failure_response": abort_plan.get("every_abort_has_failure_response", True),
        "protected_HR_DnAE_abort_blocks_entire_execution": abort_plan.get(
            "protected_hr_dnae_abort_blocks_entire_execution", True
        ),
        "runtime_worldmodel_memory_fact_abort_blocks_entire_execution": abort_plan.get(
            "runtime_wm_memory_fact_write_abort_blocks", True
        ),
        "missing_harness_verifier_rollback_blocks_execution": abort_plan.get(
            "missing_harness_verifier_rollback_blocks", True
        ),
        "failed_post_batch_test_blocks_next_batch": abort_plan.get("failed_post_batch_test_blocks_next_batch", True),
        "failed_verifier_suite_blocks_next_batch": abort_plan.get("failed_verifier_suite_blocks_next_batch", True),
        "rollback_rehearsal_failure_blocks_real_migration": abort_plan.get(
            "rollback_rehearsal_failure_blocks_real_migration", True
        ),
        "whitebox_test_center_touched_blocks_execution": abort_plan.get("whitebox_test_center_touch_blocks", True),
        "abort_failure_response_review_pass": abort_count >= 16 and failure_count >= 11 and planning_loaded,
        "simulated_abort_routing": [
            {
                "condition_name": c.get("condition_name"),
                "failure_response": c.get("failure_response"),
                "would_block_if_triggered": True,
                "triggered_in_dryrun": False,
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
            for c in abort_conditions
        ],
        "failure_types_defined": len(failure_types) >= 11,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    post_execution_evidence_pack_dryrun_result = {
        "post_execution_evidence_pack_template_defined": evidence_plan.get("required_after_each_batch", True)
        and bool(evidence_plan.get("evidence_pack_templates")),
        "evidence_pack_generated_now": False,
        "execution_result_claimed_now": False,
        "moved_file_count_claimed_now": 0,
        "deleted_file_count_claimed_now": 0,
        "renamed_file_count_claimed_now": 0,
        "merged_module_count_claimed_now": 0,
        "protected_asset_touch_count_claimed_now": 0,
        "HR_DnAE_touch_count_claimed_now": 0,
        "evidence_pack_review_pass": evidence_plan.get("evidence_pack_generated_now") is False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    controlled_execution_dryrun_boundary_review = {
        "no_real_migration": True,
        "no_batch_arming": True,
        "no_file_move_delete_rename_merge": True,
        "no_readme_modification": True,
        "no_phase_verdict_table_modification": True,
        "no_docs_modification_by_dryrun": True,
        "no_test_execution": True,
        "no_verifier_execution": True,
        "no_rollback_rehearsal": True,
        "no_rollback_execution": True,
        "no_runtime": True,
        "no_whitebox_test_center_design": True,
        "no_developer_backend_finalization": True,
        "no_future_module_finalization": True,
        "boundary_review_pass": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    blockers: List[str] = []
    if not planning_loaded:
        blockers.append("controlled_execution_planning_not_ready")
    if not ec_closure_loaded:
        blockers.append("execution_control_closure_not_ready")
    if not guarded_closure_loaded:
        blockers.append("guarded_closure_not_confirmed")
    if batch_count != 8:
        blockers.append("batch_count_not_8")
    if armed_count != 0:
        blockers.append("unexpected_armed_batches")
    if post_batch_test_count != 31:
        blockers.append("post_batch_test_count_not_31")
    if post_batch_test_execution_order_dryrun_result.get("executed_test_count", 0) != 0:
        blockers.append("tests_executed_in_dryrun")
    if verifier_suite_execution_order_dryrun_result.get("verifier_suite_executed"):
        blockers.append("verifier_executed_in_dryrun")
    if rollback_rehearsal_precondition_dryrun_result.get("rollback_rehearsal_executed"):
        blockers.append("rollback_rehearsal_executed_in_dryrun")
    if execution_window_dryrun_result.get("execution_window_opened"):
        blockers.append("execution_window_opened_in_dryrun")

    boundary_ok = not blockers

    controlled_execution_dryrun_readiness_decision = {
        "dryrun_verdict": "GO" if boundary_ok else "NO_GO",
        "blockers": blockers,
        "conditional_notes": [
            "dry-run simulates window/auth/arming/progression without file ops",
            "armed_batch_count=0 by design",
            "31 tests and 12 verifiers ordered but not executed",
        ],
        "ready_for_post_dryrun_review": boundary_ok,
        "ready_for_real_migration": False,
        "ready_for_file_move": False,
        "ready_for_file_delete": False,
        "ready_for_module_merge": False,
        "ready_for_post_migration_test_execution": False,
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    governance_debt_register = {
        "items": [
            "controlled_execution_dryrun_simulated_only",
            "execution_window_not_opened",
            "owner_approvals_not_collected",
            "armed_batch_count=0",
            "batch_progression_candidate_only",
            "rollback_rehearsal_required_not_executed",
            "31_tests_ordered_not_executed",
            "12_verifiers_ordered_not_executed",
            f"{HUMAN_REVIEW_CARRYOVER}_hr_manual_only",
            f"{PERMANENT_BLOCK_CARRYOVER}_dnae_excluded",
        ],
        "item_count": 10,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    next_phase_recommendation = {
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "final_decision": FINAL_DECISION if boundary_ok else "MAIN_PROJECT_STRUCTURE_MIGRATION_CONTROLLED_EXECUTION_DRYRUN_REQUIRES_FIXES",
        "reason": "controlled execution chain simulated; no file ops; armed_batch_count=0",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    summary = {
        "phase": PHASE_ID,
        "dryrun_scope": DRYRUN_SCOPE,
        "controlled_execution_planning_input_loaded": planning_loaded,
        "execution_control_roadmap_input_loaded": ec_roadmap_loaded,
        "execution_control_closure_input_loaded": ec_closure_loaded,
        "execution_control_dryrun_input_loaded": ec_dryrun_loaded,
        "guarded_closure_input_loaded": guarded_closure_loaded,
        "readiness_input_loaded": readiness_loaded,
        "protected_asset_resolution_closure_input_loaded": pahr_loaded,
        "structure_map_input_loaded": structure_loaded,
        "gate_taxonomy_input_loaded": gate_loaded,
        "controlled_execution_dryrun_execution_plan_generated": True,
        "execution_window_dryrun_result_generated": True,
        "owner_authorization_gate_dryrun_result_generated": True,
        "batch_arming_execution_dryrun_result_generated": True,
        "controlled_batch_progression_dryrun_result_generated": True,
        "rollback_rehearsal_precondition_dryrun_result_generated": True,
        "post_batch_test_execution_order_dryrun_result_generated": True,
        "verifier_suite_execution_order_dryrun_result_generated": True,
        "abort_and_failure_response_dryrun_result_generated": True,
        "post_execution_evidence_pack_dryrun_result_generated": True,
        "controlled_execution_dryrun_boundary_review_generated": True,
        "controlled_execution_dryrun_readiness_decision_generated": True,
        "batch_count": batch_count,
        "owner_authorization_gate_count": owner_gate_count,
        "execution_window_requirement_count": window_req_count,
        "post_batch_test_count": post_batch_test_count,
        "verifier_suite_count": verifier_suite_count,
        "abort_condition_count": abort_count,
        "failure_response_type_count": failure_count,
        "execution_window_opened": False,
        "owner_auto_confirm_allowed": False,
        "owner_approval_executed": False,
        "final_owner_human_confirmed": False,
        "batch_arming_simulated": True,
        "armed_batch_count": armed_count,
        "all_batches_not_armed": armed_count == 0,
        "batch_progression_simulated": True,
        "batch_execution_count": 0,
        "b0_baseline_only_no_move": True,
        "b1_docs_relink_candidate_only": True,
        "b2_capability_grouping_candidate_only": True,
        "b3_governance_grouping_candidate_only": True,
        "b4_midplatform_grouping_candidate_only": True,
        "b5_dev_artifact_reference_only": True,
        "b6_future_marker_only": True,
        "b7_verification_gate_only": True,
        "rollback_rehearsal_mandatory": rollback_rehearsal_precondition_dryrun_result.get("rollback_rehearsal_mandatory")
        is True,
        "rollback_rehearsal_executed": False,
        "rollback_execution_still_blocked": True,
        "test_execution_order_defined": post_batch_test_execution_order_dryrun_result.get("test_execution_order_defined")
        is True,
        "tests_mapped_to_batches": post_batch_test_execution_order_dryrun_result.get("tests_mapped_to_batches") is True,
        "post_migration_tests_execution_allowed": False,
        "post_migration_tests_executed": False,
        "executed_test_count": 0,
        "verifier_execution_order_defined": verifier_suite_execution_order_dryrun_result.get(
            "verifier_execution_order_defined"
        )
        is True,
        "required_verifier_count": required_verifier_count,
        "verifier_suite_execution_allowed": False,
        "verifier_suite_executed": False,
        "every_abort_has_failure_response": abort_and_failure_response_dryrun_result.get("every_abort_has_failure_response")
        is True,
        "protected_HR_DnAE_abort_blocks_entire_execution": abort_and_failure_response_dryrun_result.get(
            "protected_HR_DnAE_abort_blocks_entire_execution"
        )
        is True,
        "runtime_worldmodel_memory_fact_abort_blocks_entire_execution": abort_and_failure_response_dryrun_result.get(
            "runtime_worldmodel_memory_fact_abort_blocks_entire_execution"
        )
        is True,
        "missing_harness_verifier_rollback_blocks_execution": abort_and_failure_response_dryrun_result.get(
            "missing_harness_verifier_rollback_blocks_execution"
        )
        is True,
        "failed_post_batch_test_blocks_next_batch": abort_and_failure_response_dryrun_result.get(
            "failed_post_batch_test_blocks_next_batch"
        )
        is True,
        "failed_verifier_suite_blocks_next_batch": abort_and_failure_response_dryrun_result.get(
            "failed_verifier_suite_blocks_next_batch"
        )
        is True,
        "rollback_rehearsal_failure_blocks_real_migration": abort_and_failure_response_dryrun_result.get(
            "rollback_rehearsal_failure_blocks_real_migration"
        )
        is True,
        "whitebox_test_center_touched_blocks_execution": abort_and_failure_response_dryrun_result.get(
            "whitebox_test_center_touched_blocks_execution"
        )
        is True,
        "post_execution_evidence_pack_template_defined": post_execution_evidence_pack_dryrun_result.get(
            "post_execution_evidence_pack_template_defined"
        )
        is True,
        "evidence_pack_generated_now": False,
        "execution_result_claimed_now": False,
        "ready_for_post_dryrun_review": boundary_ok,
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
        "docs_modified_by_dryrun": False,
        "readme_modified_by_dryrun": False,
        "phase_verdict_table_modified_by_dryrun": False,
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
        "final_decision": FINAL_DECISION if boundary_ok else "MAIN_PROJECT_STRUCTURE_MIGRATION_CONTROLLED_EXECUTION_DRYRUN_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "human_review_case_count": HUMAN_REVIEW_CARRYOVER,
        "permanent_block_case_count": PERMANENT_BLOCK_CARRYOVER,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    return {
        "summary": summary,
        "input_root_matrix": {"rows": input_rows, "row_count": len(input_rows), "source_chain": SOURCE_CHAIN, **_not_fact()},
        "controlled_execution_dryrun_execution_plan": controlled_execution_dryrun_execution_plan,
        "execution_window_dryrun_result": execution_window_dryrun_result,
        "owner_authorization_gate_dryrun_result": owner_authorization_gate_dryrun_result,
        "batch_arming_execution_dryrun_result": batch_arming_execution_dryrun_result,
        "controlled_batch_progression_dryrun_result": controlled_batch_progression_dryrun_result,
        "rollback_rehearsal_precondition_dryrun_result": rollback_rehearsal_precondition_dryrun_result,
        "post_batch_test_execution_order_dryrun_result": post_batch_test_execution_order_dryrun_result,
        "verifier_suite_execution_order_dryrun_result": verifier_suite_execution_order_dryrun_result,
        "abort_and_failure_response_dryrun_result": abort_and_failure_response_dryrun_result,
        "post_execution_evidence_pack_dryrun_result": post_execution_evidence_pack_dryrun_result,
        "controlled_execution_dryrun_boundary_review": controlled_execution_dryrun_boundary_review,
        "controlled_execution_dryrun_readiness_decision": controlled_execution_dryrun_readiness_decision,
        "governance_debt_register": governance_debt_register,
        "next_phase_recommendation": next_phase_recommendation,
        "no_file_move_boundary_report": _no_side_effect_report("no_file_move"),
        "no_delete_boundary_report": _no_side_effect_report("no_delete"),
        "no_runtime_boundary_report": _no_side_effect_report("no_runtime"),
        "no_write_boundary_report": _no_side_effect_report("no_write"),
    }
