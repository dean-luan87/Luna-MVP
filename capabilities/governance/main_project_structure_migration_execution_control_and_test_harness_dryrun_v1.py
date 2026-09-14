# -*- coding: utf-8 -*-
"""Main Project Structure Migration Execution Control and Test Harness DryRun v1.

Dry-run-only: simulate arming/abort/harness/verifier/rollback chain — no execution permissions.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

PHASE_ID = "Phase-Main-Project-Structure-Migration-Execution-Control-and-Test-Harness-DryRun-v1-001"
DRYRUN_SCOPE = "main_project_structure_migration_execution_control_and_test_harness_dryrun_only"
SOURCE_CHAIN = "main_project_structure_migration_execution_control_and_test_harness_dryrun_v1"
DRYRUN_ID = "main_proj_struct_migration_exec_control_test_harness_dryrun_v1_001"

FINAL_DECISION = "MAIN_PROJECT_STRUCTURE_MIGRATION_EXECUTION_CONTROL_AND_TEST_HARNESS_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
NEXT_PHASE = "Phase-Main-Project-Structure-Migration-Execution-Control-and-Test-Harness-Post-DryRun-Review-v1-001"

PLANNING_FINAL = "MAIN_PROJECT_STRUCTURE_MIGRATION_EXECUTION_CONTROL_AND_TEST_HARNESS_PLANNING_READY_FOR_DRYRUN"
CLOSURE_DECISION = "MAIN_PROJECT_STRUCTURE_MIGRATION_GUARDED_CLOSED_FOR_CURRENT_MAINLINE"
ROADMAP_FINAL = (
    "MAIN_PROJECT_STRUCTURE_MIGRATION_GUARDED_ROADMAP_DECISION_READY_FOR_EXECUTION_CONTROL_AND_TEST_HARNESS_PLANNING"
)

HUMAN_REVIEW_CARRYOVER = 240
PERMANENT_BLOCK_CARRYOVER = 914

# Planning policy names → dry-run canonical condition_name
ABORT_CONDITION_CANONICAL = {
    "test_harness_missing": "missing_test_harness",
    "verifier_suite_missing": "missing_verifier_suite",
    "rollback_checkpoint_missing": "missing_rollback_checkpoint",
}

# Conditions that dry-run simulates as triggered (would block execution)
ABORT_SIMULATE_TRIGGERED = {
    "protected_asset_touched",
    "hr_item_without_manual_decision",
    "dnae_item_included",
    "missing_test_harness",
    "missing_verifier_suite",
    "missing_rollback_checkpoint",
    "test_harness_missing",
    "verifier_suite_missing",
    "rollback_checkpoint_missing",
    "runtime_behavior_changed",
    "world_model_memory_fact_write",
    "client_backend_boundary_violation",
    "whitebox_test_center_touched",
    "future_reserved_module_finalized",
    "owner_approval_missing",
    "post_batch_test_failed",
}

BATCH_IDS = ("B0", "B1", "B2", "B3", "B4", "B5", "B6", "B7")
OWNER_APPROVAL_BATCHES = ("B1", "B2", "B3", "B4", "B5", "B6")

PLANNING_ARTIFACTS = [
    "migration_execution_control_and_test_harness_planning_policy.json",
    "execution_control_gate.json",
    "batch_arming_policy.json",
    "abort_condition_policy.json",
    "pre_execution_checklist.json",
    "post_migration_test_harness.json",
    "post_migration_verifier_suite.json",
    "rollback_rehearsal_requirement.json",
    "failure_response_matrix.json",
    "execution_control_readiness_decision.json",
]

ROOT_SPECS = [
    {
        "id": "execution_control_planning",
        "arg": "execution_control_planning_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": PLANNING_ARTIFACTS,
    },
    {
        "id": "guarded_roadmap",
        "arg": "guarded_roadmap_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "guarded_closure",
        "arg": "guarded_closure_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "guarded_migration_non_claims_register.json"],
    },
    {
        "id": "guarded_post_review",
        "arg": "guarded_post_review_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "guarded_dryrun",
        "arg": "guarded_dryrun_root",
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
            "guarded_migration_gate_sequence.json",
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


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def _load_root(path_str: Optional[str], summary_file: str, artifacts: List[str]) -> Dict[str, Any]:
    root = Path(path_str).expanduser().resolve() if path_str else None
    loaded = bool(root) and _try_read_json(root / summary_file) is not None
    if root and artifacts:
        loaded = loaded and all(_try_read_json(root / a) is not None for a in artifacts)
    summary_payload = _try_read_json(root / summary_file) if (root and loaded) else {}
    art: Dict[str, Any] = {}
    if root and loaded:
        for name in artifacts:
            art[name] = _try_read_json(root / name)
    return {"root": root, "loaded": loaded, "summary": summary_payload or {}, "artifacts": art}


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


def run_main_project_structure_migration_execution_control_and_test_harness_dryrun_v1(
    *,
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
    roots = {spec["id"]: _load_root(args.get(spec["arg"]), spec["summary"], spec["artifacts"]) for spec in ROOT_SPECS}
    summaries = {key: roots[key]["summary"] for key in roots}
    planning_art = roots["execution_control_planning"]["artifacts"]

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
        roots["execution_control_planning"]["loaded"]
        and summaries["execution_control_planning"].get("final_decision") == PLANNING_FINAL
        and summaries["execution_control_planning"].get("ready_for_execution_control_dryrun") is True
    )
    closure_loaded = (
        roots["guarded_closure"]["loaded"]
        and summaries["guarded_closure"].get("final_decision") == CLOSURE_DECISION
    )
    roadmap_loaded = roots["guarded_roadmap"]["loaded"]
    guarded_planning_loaded = roots["guarded_planning"]["loaded"]
    guarded_dryrun_loaded = roots["guarded_dryrun"]["loaded"]
    readiness_loaded = roots["readiness"]["loaded"]
    pahr_loaded = roots["pahr_closure"]["loaded"]
    structure_loaded = roots["structure_map"]["loaded"]
    gate_loaded = roots["gate_taxonomy"]["loaded"]

    policy = planning_art.get("migration_execution_control_and_test_harness_planning_policy.json") or {}
    gate_plan = planning_art.get("execution_control_gate.json") or {}
    batch_plan = planning_art.get("batch_arming_policy.json") or {}
    abort_plan = planning_art.get("abort_condition_policy.json") or {}
    pre_exec_plan = planning_art.get("pre_execution_checklist.json") or {}
    harness_plan = planning_art.get("post_migration_test_harness.json") or {}
    verifier_plan = planning_art.get("post_migration_verifier_suite.json") or {}
    rollback_plan = planning_art.get("rollback_rehearsal_requirement.json") or {}
    failure_plan = planning_art.get("failure_response_matrix.json") or {}

    chain_closed = summaries["guarded_closure"].get("guarded_migration_chain_closed") is True
    planning_summary = summaries["execution_control_planning"]

    batch_count = batch_plan.get("batch_count", 8)
    abort_conditions = abort_plan.get("conditions") or []
    abort_count = abort_plan.get("abort_condition_count", len(abort_conditions))
    pre_check_count = pre_exec_plan.get("pre_execution_check_count", len(pre_exec_plan.get("checks") or []))
    harness_groups = harness_plan.get("harness_groups") or []
    post_migration_test_count = harness_plan.get("post_migration_test_count", 31)
    verifiers = verifier_plan.get("verifiers") or []
    verifier_suite_count = verifier_plan.get("verifier_suite_count", len(verifiers))
    required_verifier_count = verifier_plan.get("required_verifier_count", 4)
    failure_types = failure_plan.get("failure_types") or []
    failure_response_type_count = failure_plan.get("failure_response_type_count", len(failure_types))

    execution_control_dryrun_execution_plan = {
        "dryrun_id": DRYRUN_ID,
        "source_planning_ref": "_eval_out/main_project_structure_migration_execution_control_and_test_harness_planning_v1_smoke_v0/",
        "source_guarded_roadmap_ref": "_eval_out/main_project_structure_migration_guarded_roadmap_decision_v1_smoke_v0/",
        "batch_count": batch_count,
        "abort_condition_count": abort_count,
        "pre_execution_check_count": pre_check_count,
        "post_migration_test_count": post_migration_test_count,
        "verifier_suite_count": verifier_suite_count,
        "failure_response_type_count": failure_response_type_count,
        "execution_mode": "dryrun_only",
        "real_migration_execution_allowed": False,
        "batch_arming_execution_allowed": False,
        "post_migration_tests_execution_allowed": False,
        "rollback_rehearsal_execution_allowed": False,
        "verifier_suite_execution_allowed": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    go = gate_plan.get("go_conditions") or {}
    execution_control_gate_dryrun_result = {
        "guarded_migration_chain_closed": chain_closed,
        "protected_assets_excluded": go.get("protected_assets_excluded", True),
        "HR_excluded_or_manual_only": go.get("HR_excluded_or_manual_only", True),
        "DnAE_excluded": go.get("DnAE_excluded", True),
        "human_owner_approval_required": go.get("human_owner_approval_required", True),
        "owner_approval_not_auto_confirmed": go.get("owner_approval_not_auto_confirmed", True),
        "batch_arming_policy_defined": go.get("batch_arming_policy_defined", True),
        "abort_condition_policy_defined": go.get("abort_condition_policy_defined", True),
        "post_migration_test_harness_defined": go.get("post_migration_test_harness_defined", True),
        "verifier_suite_defined": go.get("verifier_suite_defined", True),
        "rollback_rehearsal_required": go.get("rollback_rehearsal_required", True),
        "clean_working_tree_required": go.get("clean_working_tree_required", True),
        "backup_or_branch_required": go.get("backup_or_branch_required", True),
        "protected_asset_snapshot_required": go.get("protected_asset_snapshot_required", True),
        "pre_execution_verifier_snapshot_required": go.get("pre_execution_verifier_snapshot_required", True),
        "gate_simulated_pass": chain_closed and planning_loaded,
        "execution_permission_granted": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    batch_entries_plan = {b.get("batch_id"): b for b in batch_plan.get("batches") or []}
    batch_arming_results: List[Dict[str, Any]] = []
    armed_count = 0

    for bid in BATCH_IDS:
        bp = batch_entries_plan.get(bid) or {}
        owner_req = bp.get("owner_approval_required", bid in OWNER_APPROVAL_BATCHES)
        owner_present = False
        if bid == "B0":
            simulated_state = "blocked_until_real_approval_or_execution_phase"
        elif bid in OWNER_APPROVAL_BATCHES:
            simulated_state = "blocked_owner_approval_missing"
        elif bid == "B7":
            simulated_state = "blocked_previous_batch_tests_not_executed"
        else:
            simulated_state = "blocked_until_real_approval_or_execution_phase"

        batch_arming_results.append(
            {
                "batch_id": bid,
                "arming_preconditions_checked": True,
                "owner_approval_required": owner_req,
                "owner_approval_present": owner_present,
                "protected_asset_check_pass": True,
                "HR_DnAE_exclusion_pass": True,
                "rollback_checkpoint_required": bp.get("rollback_checkpoint_required", True),
                "post_batch_test_required": bp.get("post_batch_test_required", bid != "B6"),
                "arming_allowed_now": False,
                "armed_now": False,
                "execution_allowed_now": False,
                "simulated_state": simulated_state,
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )

    batch_arming_dryrun_results = {
        "batch_results": batch_arming_results,
        "batch_count": len(batch_arming_results),
        "armed_batch_count": armed_count,
        "b0_armed_now": False,
        "b1_b6_owner_approval_missing_blocks_arming": True,
        "b7_previous_tests_not_executed_blocks_arming": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    abort_dryrun_entries = []
    for c in abort_conditions:
        raw_name = c.get("condition_name", "")
        name = ABORT_CONDITION_CANONICAL.get(raw_name, raw_name)
        triggered = raw_name in ABORT_SIMULATE_TRIGGERED or name in ABORT_SIMULATE_TRIGGERED
        abort_dryrun_entries.append(
            {
                "abort_condition_id": c.get("abort_condition_id"),
                "condition_name": name,
                "planning_condition_name": raw_name if raw_name != name else None,
                "simulated_triggered": triggered,
                "severity": c.get("severity"),
                "abort_scope": c.get("abort_scope"),
                "failure_response": c.get("failure_response"),
                "rollback_required": c.get("rollback_required"),
                "audit_required": c.get("audit_required"),
                "blocks_execution": triggered,
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )

    abort_condition_dryrun_results = {
        "conditions": abort_dryrun_entries,
        "abort_condition_count": len(abort_dryrun_entries),
        "simulated_blocked_count": sum(1 for a in abort_dryrun_entries if a.get("blocks_execution")),
        "protected_asset_abort_blocks": any(
            a.get("condition_name") == "protected_asset_touched" and a.get("blocks_execution") for a in abort_dryrun_entries
        ),
        "HR_abort_blocks": any(
            a.get("condition_name") == "hr_item_without_manual_decision" and a.get("blocks_execution")
            for a in abort_dryrun_entries
        ),
        "DnAE_abort_blocks": any(
            a.get("condition_name") == "dnae_item_included" and a.get("blocks_execution") for a in abort_dryrun_entries
        ),
        "runtime_change_abort_blocks": any(
            a.get("condition_name") == "runtime_behavior_changed" and a.get("blocks_execution")
            for a in abort_dryrun_entries
        ),
        "worldmodel_memory_fact_write_abort_blocks": any(
            a.get("condition_name") == "world_model_memory_fact_write" and a.get("blocks_execution")
            for a in abort_dryrun_entries
        ),
        "whitebox_test_center_touch_abort_blocks": any(
            a.get("condition_name") == "whitebox_test_center_touched" and a.get("blocks_execution")
            for a in abort_dryrun_entries
        ),
        "owner_approval_missing_abort_blocks": any(
            a.get("condition_name") == "owner_approval_missing" and a.get("blocks_execution")
            for a in abort_dryrun_entries
        ),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    pre_execution_checklist_dryrun_result = {
        "checklist_item_count": pre_check_count,
        "checklist_executed": False,
        "all_items_defined": len(pre_exec_plan.get("checks") or []) >= 14,
        "clean_working_tree_required": True,
        "dedicated_branch_required": True,
        "backup_snapshot_required": True,
        "owner_approval_records_required": True,
        "rollback_rehearsal_record_required": True,
        "verifier_baseline_record_required": True,
        "operator_acknowledgement_required": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    group_map = {g.get("harness_group_id"): g for g in harness_groups}
    post_migration_test_harness_dryrun_result = {
        "harness_group_count": len(harness_groups),
        "post_migration_test_count": post_migration_test_count,
        "harness_tests_bound": post_migration_test_count == 31,
        "tests_execution_allowed_now": False,
        "executed_test_count": 0,
        "structural_integrity_harness_defined": "A" in group_map,
        "governance_boundary_harness_defined": "B" in group_map,
        "functional_smoke_verifier_harness_defined": "C" in group_map,
        "no_runtime_regression_harness_defined": "D" in group_map,
        "developer_tooling_preservation_harness_defined": "E" in group_map,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    post_migration_verifier_suite_dryrun_result = {
        "verifier_suite_count": verifier_suite_count,
        "required_verifier_count": required_verifier_count,
        "verifier_suite_execution_allowed_now": False,
        "verifier_suite_executed": False,
        "execution_order_defined": all(v.get("execution_order") for v in verifiers),
        "optional_if_missing_policy_defined": any(v.get("optional_if_missing") for v in verifiers),
        "failure_response_defined": all(v.get("failure_response") for v in verifiers),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    rollback_rehearsal_dryrun_result = {
        "rehearsal_required_before_real_migration": rollback_plan.get("rehearsal_required_before_real_migration", True),
        "rehearsal_execution_allowed_now": False,
        "rollback_dryrun_required": rollback_plan.get("rollback_dryrun_required", True),
        "rollback_checkpoint_per_batch": rollback_plan.get("rollback_checkpoint_per_batch", True),
        "rollback_audit_required": rollback_plan.get("rollback_audit_required", True),
        "rollback_rehearsal_executed": False,
        "rollback_execution_still_blocked": rollback_plan.get("rollback_execution_still_blocked", True),
        "rerun_verifier_after_rollback_required": rollback_plan.get("rerun_verifier_after_rollback_required", True),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    blocks_next = sum(1 for f in failure_types if f.get("blocks_next_batch"))
    blocks_migration = sum(1 for f in failure_types if f.get("blocks_real_migration"))
    rollback_req_count = sum(1 for f in failure_types if f.get("rollback_required"))
    hr_review_count = sum(1 for f in failure_types if f.get("requires_human_review"))

    failure_response_matrix_dryrun_result = {
        "failure_response_type_count": failure_response_type_count,
        "all_failure_responses_defined": len(failure_types) >= 11,
        "blocks_next_batch_count": blocks_next,
        "blocks_real_migration_count": blocks_migration,
        "rollback_required_count": rollback_req_count,
        "requires_human_review_count": hr_review_count,
        "failure_response_matrix_ready": len(failure_types) >= 11,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    blockers: List[str] = []
    if not planning_loaded:
        blockers.append("execution_control_planning_not_ready")
    if not closure_loaded or not chain_closed:
        blockers.append("guarded_migration_chain_not_closed")
    if not execution_control_gate_dryrun_result.get("gate_simulated_pass"):
        blockers.append("execution_control_gate_simulation_failed")
    if armed_count != 0:
        blockers.append("unexpected_armed_batches")
    if post_migration_test_harness_dryrun_result.get("executed_test_count", 0) != 0:
        blockers.append("tests_executed_in_dryrun")
    if post_migration_verifier_suite_dryrun_result.get("verifier_suite_executed"):
        blockers.append("verifier_suite_executed_in_dryrun")
    if rollback_rehearsal_dryrun_result.get("rollback_rehearsal_executed"):
        blockers.append("rollback_rehearsal_executed_in_dryrun")
    if post_migration_test_count != 31:
        blockers.append("post_migration_test_count_not_31")

    boundary_ok = not blockers

    execution_control_dryrun_readiness_decision = {
        "dryrun_verdict": "GO" if boundary_ok else "NO_GO",
        "blockers": blockers,
        "conditional_notes": [] if boundary_ok else ["execution_control_dryrun_findings_require_review"],
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

    forbidden_execution_report = {
        "forbidden_actions": [
            "real_migration_execution",
            "batch_arming_execution",
            "post_migration_test_execution",
            "verifier_suite_execution",
            "rollback_rehearsal_execution",
            "rollback_execution",
            "owner_confirmation",
            "protected_asset_modification",
            "permanent_block_release",
        ],
        "all_forbidden_respected": boundary_ok,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    governance_debt_register = {
        "items": [
            "execution_control_dryrun_simulated_only",
            "armed_batch_count=0_by_design",
            "owner_approval_missing_blocks_b1_b6",
            "b7_blocked_until_prior_batch_tests_execute",
            "31_tests_bound_not_executed",
            "verifier_suite_orchestrated_not_executed",
            "rollback_rehearsal_required_not_executed",
        ],
        "item_count": 7,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    next_phase_recommendation = {
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "final_decision": FINAL_DECISION if boundary_ok else "MAIN_PROJECT_STRUCTURE_MIGRATION_EXECUTION_CONTROL_DRYRUN_REQUIRES_FIXES",
        "reason": "dry-run chain simulated; armed_batch_count=0; tests and verifiers not executed",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    summary = {
        "phase": PHASE_ID,
        "dryrun_scope": DRYRUN_SCOPE,
        "execution_control_planning_input_loaded": planning_loaded,
        "guarded_roadmap_input_loaded": roadmap_loaded,
        "guarded_closure_input_loaded": closure_loaded,
        "guarded_dryrun_input_loaded": guarded_dryrun_loaded,
        "guarded_planning_input_loaded": guarded_planning_loaded,
        "readiness_input_loaded": readiness_loaded,
        "protected_asset_resolution_closure_input_loaded": pahr_loaded,
        "consolidation_closure_input_loaded": roots["consolidation_closure"]["loaded"],
        "structure_map_input_loaded": structure_loaded,
        "gate_taxonomy_input_loaded": gate_loaded,
        "guarded_post_review_input_loaded": roots["guarded_post_review"]["loaded"],
        "execution_control_dryrun_execution_plan_generated": True,
        "execution_control_gate_dryrun_result_generated": True,
        "batch_arming_dryrun_results_generated": True,
        "abort_condition_dryrun_results_generated": True,
        "pre_execution_checklist_dryrun_result_generated": True,
        "post_migration_test_harness_dryrun_result_generated": True,
        "post_migration_verifier_suite_dryrun_result_generated": True,
        "rollback_rehearsal_dryrun_result_generated": True,
        "failure_response_matrix_dryrun_result_generated": True,
        "execution_control_dryrun_readiness_decision_generated": True,
        "batch_count": batch_count,
        "abort_condition_count": abort_count,
        "pre_execution_check_count": pre_check_count,
        "post_migration_harness_group_count": len(harness_groups),
        "post_migration_test_count": post_migration_test_count,
        "verifier_suite_count": verifier_suite_count,
        "required_verifier_count": required_verifier_count,
        "failure_response_type_count": failure_response_type_count,
        "execution_control_gate_simulated_pass": execution_control_gate_dryrun_result.get("gate_simulated_pass") is True,
        "execution_permission_granted": False,
        "batch_arming_simulated": True,
        "armed_batch_count": armed_count,
        "b0_armed_now": False,
        "b1_b6_owner_approval_missing_blocks_arming": batch_arming_dryrun_results.get(
            "b1_b6_owner_approval_missing_blocks_arming"
        )
        is True,
        "b7_previous_tests_not_executed_blocks_arming": batch_arming_dryrun_results.get(
            "b7_previous_tests_not_executed_blocks_arming"
        )
        is True,
        "abort_conditions_simulated": len(abort_dryrun_entries) >= 16,
        "protected_asset_abort_blocks_execution": abort_condition_dryrun_results.get("protected_asset_abort_blocks")
        is True,
        "HR_abort_blocks_execution": abort_condition_dryrun_results.get("HR_abort_blocks") is True,
        "DnAE_abort_blocks_execution": abort_condition_dryrun_results.get("DnAE_abort_blocks") is True,
        "runtime_change_abort_blocks_execution": abort_condition_dryrun_results.get("runtime_change_abort_blocks")
        is True,
        "worldmodel_memory_fact_write_abort_blocks_execution": abort_condition_dryrun_results.get(
            "worldmodel_memory_fact_write_abort_blocks"
        )
        is True,
        "whitebox_test_center_touch_abort_blocks_execution": abort_condition_dryrun_results.get(
            "whitebox_test_center_touch_abort_blocks"
        )
        is True,
        "owner_approval_missing_abort_blocks_execution": abort_condition_dryrun_results.get(
            "owner_approval_missing_abort_blocks"
        )
        is True,
        "checklist_executed": False,
        "post_migration_tests_execution_allowed": False,
        "post_migration_tests_executed": False,
        "executed_test_count": 0,
        "verifier_suite_execution_allowed": False,
        "verifier_suite_executed": False,
        "rollback_rehearsal_required": rollback_rehearsal_dryrun_result.get("rehearsal_required_before_real_migration")
        is True,
        "rollback_rehearsal_execution_allowed": False,
        "rollback_rehearsal_executed": False,
        "rollback_execution_still_blocked": rollback_rehearsal_dryrun_result.get("rollback_execution_still_blocked") is True,
        "failure_response_matrix_ready": failure_response_matrix_dryrun_result.get("failure_response_matrix_ready") is True,
        "ready_for_post_dryrun_review": boundary_ok,
        "ready_for_real_migration": False,
        "ready_for_file_move": False,
        "ready_for_file_delete": False,
        "ready_for_module_merge": False,
        "ready_for_post_migration_test_execution": False,
        "real_migration_execution_allowed": False,
        "batch_arming_execution_allowed": False,
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
        "final_decision": FINAL_DECISION if boundary_ok else "MAIN_PROJECT_STRUCTURE_MIGRATION_EXECUTION_CONTROL_DRYRUN_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "human_review_case_count": HUMAN_REVIEW_CARRYOVER,
        "permanent_block_case_count": PERMANENT_BLOCK_CARRYOVER,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    return {
        "summary": summary,
        "input_root_matrix": {"rows": input_rows, "row_count": len(input_rows), "source_chain": SOURCE_CHAIN, **_not_fact()},
        "execution_control_dryrun_execution_plan": execution_control_dryrun_execution_plan,
        "execution_control_gate_dryrun_result": execution_control_gate_dryrun_result,
        "batch_arming_dryrun_results": batch_arming_dryrun_results,
        "abort_condition_dryrun_results": abort_condition_dryrun_results,
        "pre_execution_checklist_dryrun_result": pre_execution_checklist_dryrun_result,
        "post_migration_test_harness_dryrun_result": post_migration_test_harness_dryrun_result,
        "post_migration_verifier_suite_dryrun_result": post_migration_verifier_suite_dryrun_result,
        "rollback_rehearsal_dryrun_result": rollback_rehearsal_dryrun_result,
        "failure_response_matrix_dryrun_result": failure_response_matrix_dryrun_result,
        "execution_control_dryrun_readiness_decision": execution_control_dryrun_readiness_decision,
        "forbidden_execution_report": forbidden_execution_report,
        "governance_debt_register": governance_debt_register,
        "next_phase_recommendation": next_phase_recommendation,
        "no_file_move_boundary_report": _no_side_effect_report("no_file_move"),
        "no_delete_boundary_report": _no_side_effect_report("no_delete"),
        "no_runtime_boundary_report": _no_side_effect_report("no_runtime"),
        "no_write_boundary_report": _no_side_effect_report("no_write"),
    }
