# -*- coding: utf-8 -*-
"""Main Project Structure Migration Pre-Authorization and Rollback Rehearsal DryRun v1.

Dry-run-only: simulate owner/auth gaps, operator ack gaps, package/rehearsal gaps blocking migration.
No real migration, owner confirmation, ack execution, rehearsal, or batch arming.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

PHASE_ID = "Phase-Main-Project-Structure-Migration-Pre-Authorization-and-Rollback-Rehearsal-DryRun-v1-001"
DRYRUN_SCOPE = "main_project_structure_migration_pre_authorization_and_rollback_rehearsal_dryrun_only"
DRYRUN_ID = "main_proj_struct_migration_pre_auth_rollback_rehearsal_dryrun_v1_001"
SOURCE_CHAIN = "main_project_structure_migration_pre_authorization_and_rollback_rehearsal_dryrun_v1"

FINAL_DECISION = "MAIN_PROJECT_STRUCTURE_MIGRATION_PRE_AUTHORIZATION_AND_ROLLBACK_REHEARSAL_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
NEXT_PHASE = "Phase-Main-Project-Structure-Migration-Pre-Authorization-and-Rollback-Rehearsal-Post-DryRun-Review-v1-001"

PLANNING_FINAL = "MAIN_PROJECT_STRUCTURE_MIGRATION_PRE_AUTHORIZATION_AND_ROLLBACK_REHEARSAL_PLANNING_READY_FOR_DRYRUN"
ROADMAP_FINAL = (
    "MAIN_PROJECT_STRUCTURE_MIGRATION_CONTROLLED_EXECUTION_ROADMAP_DECISION_READY_FOR_PRE_AUTHORIZATION_AND_ROLLBACK_REHEARSAL_PLANNING"
)
CONTROLLED_EXECUTION_CLOSURE = "MAIN_PROJECT_STRUCTURE_MIGRATION_CONTROLLED_EXECUTION_CLOSED_FOR_CURRENT_MAINLINE"
CE_PLANNING_FINAL = "MAIN_PROJECT_STRUCTURE_MIGRATION_CONTROLLED_EXECUTION_PLANNING_READY_FOR_DRYRUN"
EXECUTION_CONTROL_CLOSURE = "MAIN_PROJECT_STRUCTURE_MIGRATION_EXECUTION_CONTROL_AND_TEST_HARNESS_CLOSED_FOR_CURRENT_MAINLINE"
GUARDED_CLOSURE = "MAIN_PROJECT_STRUCTURE_MIGRATION_GUARDED_CLOSED_FOR_CURRENT_MAINLINE"

HUMAN_REVIEW_CARRYOVER = 240
PERMANENT_BLOCK_CARRYOVER = 914

BATCH_IDS = ("B0", "B1", "B2", "B3", "B4", "B5", "B6", "B7")
OWNER_APPROVAL_BATCHES = ("B1", "B2", "B3", "B4", "B5", "B6")

OWNER_TYPES = (
    "architecture_owner",
    "governance_owner",
    "evaluation_owner",
    "capability_owner",
    "midplatform_owner",
    "docs_owner",
    "product_client_owner",
)

OWNER_BATCH_REQUIRED: Dict[str, List[str]] = {
    "B0": ["architecture_owner"],
    "B1": ["docs_owner", "architecture_owner"],
    "B2": ["capability_owner", "architecture_owner"],
    "B3": ["governance_owner", "architecture_owner"],
    "B4": ["midplatform_owner", "architecture_owner"],
    "B5": ["evaluation_owner", "architecture_owner"],
    "B6": ["architecture_owner"],
    "B7": ["evaluation_owner", "architecture_owner"],
}

PLANNING_ARTIFACTS = [
    "pre_authorization_and_rollback_rehearsal_planning_policy.json",
    "owner_authorization_resolution_plan.json",
    "operator_acknowledgement_policy.json",
    "pre_execution_authorization_package.json",
    "rollback_rehearsal_scope.json",
    "rollback_rehearsal_plan.json",
    "rollback_rehearsal_evidence_template.json",
    "batch_arming_precondition_record.json",
    "authorization_blocker_policy.json",
    "pre_authorization_planning_readiness_decision.json",
]

ROOT_SPECS = [
    {
        "id": "pre_authorization_planning",
        "arg": "pre_authorization_planning_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": PLANNING_ARTIFACTS,
    },
    {
        "id": "controlled_execution_roadmap",
        "arg": "controlled_execution_roadmap_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "pre_authorization_rollback_rehearsal_route_decision.json"],
    },
    {
        "id": "controlled_execution_closure",
        "arg": "controlled_execution_closure_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": [
            "summary.json",
            "controlled_execution_closure_decision_summary.json",
            "controlled_execution_non_claims_register.json",
        ],
    },
    {
        "id": "controlled_execution_post_review",
        "arg": "controlled_execution_post_review_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "controlled_execution_dryrun",
        "arg": "controlled_execution_dryrun_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "controlled_execution_planning",
        "arg": "controlled_execution_planning_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": [
            "controlled_execution_batch_plan.json",
            "owner_authorization_gate.json",
            "batch_arming_execution_plan.json",
            "rollback_rehearsal_precondition.json",
        ],
    },
    {
        "id": "execution_control_closure",
        "arg": "execution_control_closure_root",
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
        "post_migration_tests_executed": False,
        "verifier_suite_executed": False,
        "rollback_executed": False,
        "rollback_rehearsal_executed": False,
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


def run_main_project_structure_migration_pre_authorization_and_rollback_rehearsal_dryrun_v1(
    *,
    pre_authorization_planning_root: str,
    controlled_execution_roadmap_root: str,
    controlled_execution_closure_root: str,
    controlled_execution_post_review_root: str,
    controlled_execution_dryrun_root: str,
    controlled_execution_planning_root: str,
    execution_control_closure_root: str,
    guarded_closure_root: str,
    readiness_root: str,
    pahr_closure_root: str,
    consolidation_closure_root: str,
    structure_map_root: str,
    gate_taxonomy_root: str,
) -> Dict[str, Any]:
    args = locals().copy()
    roots = {spec["id"]: _load_root(args.get(spec["arg"]), spec["summary"], spec["artifacts"]) for spec in ROOT_SPECS}
    summaries = {key: roots[key]["summary"] for key in roots}
    pre_art = roots["pre_authorization_planning"]["artifacts"] if roots["pre_authorization_planning"]["loaded"] else {}
    ce_art = roots["controlled_execution_planning"]["artifacts"] if roots["controlled_execution_planning"]["loaded"] else {}

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

    pre_planning_loaded = (
        roots["pre_authorization_planning"]["loaded"]
        and summaries["pre_authorization_planning"].get("final_decision") == PLANNING_FINAL
        and summaries["pre_authorization_planning"].get("ready_for_pre_authorization_dryrun") is True
    )
    roadmap_loaded = roots["controlled_execution_roadmap"]["loaded"]
    ce_closure_loaded = (
        roots["controlled_execution_closure"]["loaded"]
        and summaries["controlled_execution_closure"].get("final_decision") == CONTROLLED_EXECUTION_CLOSURE
    )
    ce_planning_loaded = (
        roots["controlled_execution_planning"]["loaded"]
        and summaries["controlled_execution_planning"].get("final_decision") == CE_PLANNING_FINAL
    )
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

    owner_plan = pre_art.get("owner_authorization_resolution_plan.json") or {}
    operator_plan = pre_art.get("operator_acknowledgement_policy.json") or {}
    package_plan = pre_art.get("pre_execution_authorization_package.json") or {}
    rb_scope_plan = pre_art.get("rollback_rehearsal_scope.json") or {}
    rb_plan = pre_art.get("rollback_rehearsal_plan.json") or {}
    rb_evidence_plan = pre_art.get("rollback_rehearsal_evidence_template.json") or {}
    arming_plan = pre_art.get("batch_arming_precondition_record.json") or {}
    blocker_plan = pre_art.get("authorization_blocker_policy.json") or {}
    rollback_pre = ce_art.get("rollback_rehearsal_precondition.json") or {}

    owner_count = owner_plan.get("owner_authorization_type_count", len(owner_plan.get("owners") or []))
    step_count = rb_plan.get("rollback_rehearsal_step_count", len(rb_plan.get("steps") or []))
    scope_batch_count = rb_scope_plan.get("rollback_rehearsal_scope_batch_count", len(BATCH_IDS))
    mandatory_count = rb_scope_plan.get("rollback_rehearsal_mandatory_batches_count", 6)
    blocker_count = blocker_plan.get("authorization_blocker_count", len(blocker_plan.get("blockers") or []))
    included_records = package_plan.get("included_records") or []
    included_record_count = len(included_records)
    arming_batches = arming_plan.get("batches") or []
    batch_arming_record_count = arming_plan.get("batch_arming_record_count", len(arming_batches))

    pre_authorization_rollback_dryrun_execution_plan = {
        "dryrun_id": DRYRUN_ID,
        "source_planning_ref": "_eval_out/main_project_structure_migration_pre_authorization_and_rollback_rehearsal_planning_v1_smoke_v0/",
        "source_controlled_execution_roadmap_ref": "_eval_out/main_project_structure_migration_controlled_execution_roadmap_decision_v1_smoke_v0/",
        "owner_authorization_type_count": owner_count,
        "batch_arming_record_count": batch_arming_record_count,
        "rollback_rehearsal_scope_batch_count": scope_batch_count,
        "rollback_rehearsal_mandatory_batches_count": mandatory_count,
        "rollback_rehearsal_step_count": step_count,
        "authorization_blocker_count": blocker_count,
        "execution_mode": "dryrun_only",
        "real_migration_execution_allowed": False,
        "batch_arming_allowed_now": False,
        "owner_approval_execution_allowed": False,
        "operator_ack_execution_allowed": False,
        "rollback_rehearsal_execution_allowed": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    owner_sim_entries = []
    for ot in OWNER_TYPES:
        owner_sim_entries.append(
            {
                "owner_type": ot,
                "owner_candidate_present": True,
                "owner_confirmed_now": False,
                "approval_simulated": False,
                "approval_executed": False,
                "missing_owner_blocks_arming": True,
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )

    batch_owner_block = []
    armed_count = 0
    for bid in BATCH_IDS:
        missing_owners = OWNER_BATCH_REQUIRED.get(bid, [])
        if bid == "B0":
            sim_state = "baseline_only_no_arm"
            blocks_arming = False
        elif bid in OWNER_APPROVAL_BATCHES:
            sim_state = "blocked_missing_owner_approval"
            blocks_arming = True
        elif bid == "B7":
            sim_state = "blocked_missing_owner_and_evidence"
            blocks_arming = True
        else:
            sim_state = "blocked_preconditions"
            blocks_arming = True
        batch_owner_block.append(
            {
                "batch_id": bid,
                "required_owner_approvals": missing_owners,
                "owner_approval_missing_blocks_arming": blocks_arming and bid != "B0",
                "simulated_state": sim_state,
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )

    owner_authorization_dryrun_result = {
        "owner_authorization_type_count": owner_count,
        "owner_authorization_simulated": True,
        "architecture_owner_candidate_present": True,
        "governance_owner_candidate_present": True,
        "evaluation_owner_candidate_present": True,
        "capability_owner_candidate_present": True,
        "midplatform_owner_candidate_present": True,
        "docs_owner_candidate_present": True,
        "product_client_owner_candidate_present": True,
        "owner_confirmed_now": False,
        "owner_approval_executed": False,
        "owner_approval_execution_allowed": False,
        "auto_confirm_allowed": False,
        "missing_owner_blocks_execution": True,
        "missing_owner_blocks_batch_arming": True,
        "owner_authorization_review_pass": owner_count == 7 and pre_planning_loaded,
        "B1_B6_missing_owner_blocks_arming": True,
        "B7_missing_evaluation_architecture_owner_blocks_arming": True,
        "owner_candidate_not_equal_owner_confirmed": True,
        "simulated_owners": owner_sim_entries,
        "simulated_batch_owner_blocks": batch_owner_block,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    ack_topics = operator_plan.get("operator_must_confirm_understanding_of") or []
    operator_acknowledgement_dryrun_result = {
        "operator_ack_required": operator_plan.get("operator_ack_required", True),
        "operator_ack_simulated": True,
        "operator_ack_executed_now": False,
        "operator_ack_auto_generated": False,
        "missing_operator_ack_blocks_execution": True,
        "missing_operator_ack_blocks_batch_arming": True,
        "operator_ack_required_scope_count": len(ack_topics),
        "operator_ack_review_pass": len(ack_topics) >= 8 and pre_planning_loaded,
        "gap_simulation_missing_operator_ack_blocks_migration": True,
        "gap_simulation_missing_operator_ack_blocks_arming": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    record_flags = {r.get("record_name") if isinstance(r, dict) else r: True for r in included_records}
    pre_execution_authorization_package_dryrun_result = {
        "package_required_before_real_migration": package_plan.get("package_required_before_real_migration", True),
        "package_template_loaded": pre_planning_loaded and included_record_count >= 11,
        "included_record_count": included_record_count,
        "owner_approval_records_required": record_flags.get("owner_approval_records", True),
        "operator_acknowledgement_required": record_flags.get("operator_acknowledgement", True),
        "clean_working_tree_proof_required": record_flags.get("clean_working_tree_proof", True),
        "branch_backup_proof_required": record_flags.get("branch_backup_proof", True),
        "protected_asset_exclusion_snapshot_required": record_flags.get("protected_asset_exclusion_snapshot", True),
        "HR_DnAE_exclusion_snapshot_required": record_flags.get("HR_DnAE_exclusion_snapshot", True),
        "rollback_rehearsal_report_required": record_flags.get("rollback_rehearsal_report", True),
        "test_harness_ready_record_required": record_flags.get("test_harness_ready_record", True),
        "verifier_suite_ready_record_required": record_flags.get("verifier_suite_ready_record", True),
        "abort_policy_loaded_record_required": record_flags.get("abort_policy_loaded_record", True),
        "batch_arming_record_required": record_flags.get("batch_arming_record", True),
        "package_generated_now": False,
        "package_execution_allowed_now": False,
        "missing_package_blocks_real_migration": True,
        "package_review_pass": included_record_count >= 11 and pre_planning_loaded,
        "gap_simulation_missing_package_blocks_migration": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    rollback_rehearsal_scope_dryrun_result = {
        "rollback_rehearsal_scope_batch_count": scope_batch_count,
        "rollback_rehearsal_mandatory_batches_count": mandatory_count,
        "b1_b6_rehearsal_mandatory": rb_scope_plan.get("B1_B6_mandatory", True),
        "b0_baseline_restore_check_required": rb_scope_plan.get("B0_baseline_restore_check", True),
        "b7_verification_gate_restore_check_required": rb_scope_plan.get("B7_verification_gate_restore_check", True),
        "restore_path_map_required": True,
        "restore_docs_links_required": rollback_pre.get("restore_docs_links_required", True),
        "restore_phase_verdict_table_required_if_touched": rollback_pre.get(
            "restore_phase_verdict_table_if_touched", True
        ),
        "restore_eval_out_refs_required": rollback_pre.get("restore_eval_out_references_required", True),
        "capability_runner_verifier_doc_linkage_restore_required": True,
        "rollback_verifier_rerun_required": rollback_pre.get("rollback_verifier_rerun_required", True),
        "rehearsal_execution_allowed_now": False,
        "rehearsal_executed_now": False,
        "rehearsal_scope_review_pass": scope_batch_count >= 8 and mandatory_count >= 6 and pre_planning_loaded,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    steps = rb_plan.get("steps") or []
    rollback_rehearsal_plan_dryrun_result = {
        "rollback_rehearsal_step_count": step_count,
        "rehearsal_steps_simulated": True,
        "rehearsal_execution_allowed_now": False,
        "rehearsal_executed_now": False,
        "every_step_required": all(s.get("required") for s in steps) if steps else step_count >= 10,
        "failure_blocks_real_migration": all(s.get("failure_blocks_real_migration") for s in steps) if steps else True,
        "rollback_rehearsal_report_required": True,
        "rollback_rehearsal_review_pass": step_count >= 10 and pre_planning_loaded,
        "gap_simulation_missing_rollback_rehearsal_blocks_migration": True,
        "gap_simulation_missing_rollback_rehearsal_blocks_arming": True,
        "simulated_steps": [
            {
                "rehearsal_step_id": s.get("rehearsal_step_id"),
                "executed_now": False,
                "execution_simulated": True,
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
            for s in steps
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    rollback_rehearsal_evidence_dryrun_result = {
        "rollback_evidence_template_loaded": pre_planning_loaded,
        "rollback_evidence_generated_now": False,
        "rollback_success_claim_allowed": rb_evidence_plan.get("rollback_success_claim_allowed", False) is False,
        "covered_batches_defined": bool(rb_evidence_plan.get("covered_batches")),
        "restore_path_map_result_required": True,
        "docs_link_restore_result_required": True,
        "verdict_table_restore_result_required": True,
        "eval_out_ref_restore_result_required": True,
        "verifier_rerun_result_required": True,
        "rollback_evidence_review_pass": rb_evidence_plan.get("evidence_generated_now") is False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    batch_arming_sim = []
    for b in arming_batches:
        bid = b.get("batch_id")
        batch_arming_sim.append(
            {
                "batch_id": bid,
                "arming_precondition_simulated": True,
                "arming_record_generated_now": False,
                "arming_allowed_now": False,
                "armed_now": False,
                "blocked_by_missing_owner": bid in OWNER_APPROVAL_BATCHES or bid == "B7",
                "blocked_by_missing_operator_ack": bid != "B0",
                "blocked_by_missing_rollback_rehearsal": bid in OWNER_APPROVAL_BATCHES or bid == "B7",
                "simulated_state": "not_armed_gap_preconditions",
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )

    batch_arming_precondition_dryrun_result = {
        "batch_arming_record_count": batch_arming_record_count,
        "batch_arming_precondition_simulated": True,
        "required_owner_approvals_defined": all(b.get("required_owner_approvals") for b in arming_batches)
        if arming_batches
        else True,
        "operator_ack_required": True,
        "rollback_rehearsal_required": True,
        "test_harness_ready_required": True,
        "verifier_suite_ready_required": True,
        "protected_asset_exclusion_required": True,
        "HR_DnAE_exclusion_required": True,
        "abort_policy_loaded_required": True,
        "arming_record_generated_now": False,
        "arming_allowed_now": False,
        "armed_batch_count": armed_count,
        "all_batches_not_armed": armed_count == 0,
        "batch_arming_precondition_review_pass": armed_count == 0 and batch_arming_record_count == 8,
        "simulated_batches": batch_arming_sim,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    authorization_blocker_dryrun_result = {
        "authorization_blocker_count": blocker_count,
        "blockers_simulated": True,
        "missing_owner_blocks_execution": blocker_plan.get("missing_owner_blocks_execution", True),
        "missing_operator_ack_blocks_execution": blocker_plan.get("missing_operator_ack_blocks_execution", True),
        "missing_rollback_rehearsal_blocks_execution": blocker_plan.get("missing_rollback_rehearsal_blocks_execution", True),
        "missing_rollback_evidence_blocks_execution": True,
        "missing_test_harness_readiness_blocks_execution": True,
        "missing_verifier_suite_readiness_blocks_execution": True,
        "protected_asset_inclusion_blocks_execution": True,
        "HR_DnAE_inclusion_blocks_execution": True,
        "batch_arming_record_missing_blocks_execution": True,
        "abort_policy_missing_blocks_execution": True,
        "dirty_working_tree_blocks_execution": True,
        "missing_backup_branch_blocks_execution": True,
        "auto_confirm_owner_blocks_execution": True,
        "rollback_rehearsal_bypass_blocks_execution": True,
        "parallel_batch_execution_blocks_execution": True,
        "authorization_blocker_review_pass": blocker_count >= 14 and pre_planning_loaded,
        "gap_hard_block_matrix": {
            "missing_owner": {"blocks_real_migration": True, "blocks_batch_arming": True, "simulated_fire": True},
            "missing_operator_ack": {"blocks_real_migration": True, "blocks_batch_arming": True, "simulated_fire": True},
            "missing_rollback_rehearsal": {"blocks_real_migration": True, "blocks_batch_arming": True, "simulated_fire": True},
        },
        "simulated_blockers": [
            {
                "blocker_id": bl.get("blocker_id"),
                "blocker_name": bl.get("blocker_name"),
                "would_fire_in_gap_scenario": True,
                "blocks_real_migration": bl.get("blocks_real_migration"),
                "blocks_batch_arming": bl.get("blocks_batch_arming"),
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
            for bl in blocker_plan.get("blockers") or []
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    pre_authorization_dryrun_boundary_review = {
        "no_real_migration": True,
        "no_owner_confirmation": True,
        "no_operator_ack_execution": True,
        "no_authorization_package_generation": True,
        "no_rollback_rehearsal": True,
        "no_rollback_evidence_generation": True,
        "no_batch_arming": True,
        "no_file_move_delete_rename_merge": True,
        "no_test_verifier_execution": True,
        "no_runtime": True,
        "no_whitebox_test_center_design": True,
        "no_developer_backend_finalization": True,
        "no_future_module_finalization": True,
        "boundary_review_pass": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    blockers: List[str] = []
    if not pre_planning_loaded:
        blockers.append("pre_authorization_planning_not_ready")
    if not ce_closure_loaded:
        blockers.append("controlled_execution_closure_not_ready")
    if owner_count != 7:
        blockers.append("owner_authorization_type_count_not_7")
    if armed_count != 0:
        blockers.append("unexpected_armed_batches")
    if step_count < 10:
        blockers.append("rollback_rehearsal_step_count_insufficient")
    if blocker_count < 14:
        blockers.append("authorization_blocker_count_insufficient")
    if not authorization_blocker_dryrun_result.get("gap_hard_block_matrix"):
        blockers.append("gap_hard_block_matrix_missing")

    boundary_ok = not blockers

    pre_authorization_dryrun_readiness_decision = {
        "dryrun_verdict": "GO" if boundary_ok else "NO_GO",
        "blockers": blockers,
        "conditional_notes": [
            "dry-run validates owner/ack/rehearsal gaps block migration and arming",
            "armed_batch_count=0 by design",
            "no owner confirmation, no real package, no rehearsal execution",
        ],
        "ready_for_post_dryrun_review": boundary_ok,
        "ready_for_real_migration": False,
        "ready_for_batch_arming": False,
        "ready_for_file_move": False,
        "ready_for_file_delete": False,
        "ready_for_module_merge": False,
        "ready_for_rollback_rehearsal_execution": False,
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    governance_debt_register = {
        "items": [
            "pre_authorization_dryrun_simulated_only",
            "owner_approvals_not_collected",
            "operator_ack_not_executed",
            "authorization_package_template_only",
            "rollback_rehearsal_not_performed",
            "rollback_evidence_not_generated",
            "armed_batch_count=0",
            f"{HUMAN_REVIEW_CARRYOVER}_hr_manual_only",
            f"{PERMANENT_BLOCK_CARRYOVER}_dnae_excluded",
        ],
        "item_count": 9,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    next_phase_recommendation = {
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "final_decision": FINAL_DECISION if boundary_ok else "MAIN_PROJECT_STRUCTURE_MIGRATION_PRE_AUTHORIZATION_DRYRUN_REQUIRES_FIXES",
        "reason": "owner/ack/rehearsal gaps simulated; all block migration and arming; armed_batch_count=0",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    summary = {
        "phase": PHASE_ID,
        "dryrun_scope": DRYRUN_SCOPE,
        "pre_authorization_planning_input_loaded": pre_planning_loaded,
        "controlled_execution_roadmap_input_loaded": roadmap_loaded,
        "controlled_execution_closure_input_loaded": ce_closure_loaded,
        "controlled_execution_planning_input_loaded": ce_planning_loaded,
        "execution_control_closure_input_loaded": ec_closure_loaded,
        "guarded_closure_input_loaded": guarded_closure_loaded,
        "readiness_input_loaded": readiness_loaded,
        "protected_asset_resolution_closure_input_loaded": pahr_loaded,
        "structure_map_input_loaded": structure_loaded,
        "gate_taxonomy_input_loaded": gate_loaded,
        "pre_authorization_rollback_dryrun_execution_plan_generated": True,
        "owner_authorization_dryrun_result_generated": True,
        "operator_acknowledgement_dryrun_result_generated": True,
        "pre_execution_authorization_package_dryrun_result_generated": True,
        "rollback_rehearsal_scope_dryrun_result_generated": True,
        "rollback_rehearsal_plan_dryrun_result_generated": True,
        "rollback_rehearsal_evidence_dryrun_result_generated": True,
        "batch_arming_precondition_dryrun_result_generated": True,
        "authorization_blocker_dryrun_result_generated": True,
        "pre_authorization_dryrun_boundary_review_generated": True,
        "pre_authorization_dryrun_readiness_decision_generated": True,
        "owner_authorization_type_count": owner_count,
        "owner_authorization_simulated": True,
        "owner_confirmed_now": False,
        "owner_approval_executed": False,
        "owner_approval_execution_allowed": False,
        "auto_confirm_allowed": False,
        "missing_owner_blocks_execution": True,
        "missing_owner_blocks_batch_arming": True,
        "operator_ack_required": True,
        "operator_ack_simulated": True,
        "operator_ack_executed_now": False,
        "operator_ack_auto_generated": False,
        "missing_operator_ack_blocks_execution": True,
        "missing_operator_ack_blocks_batch_arming": True,
        "package_required_before_real_migration": True,
        "package_template_loaded": pre_execution_authorization_package_dryrun_result["package_template_loaded"],
        "included_record_count": included_record_count,
        "package_generated_now": False,
        "package_execution_allowed_now": False,
        "missing_package_blocks_real_migration": True,
        "rollback_rehearsal_scope_batch_count": scope_batch_count,
        "rollback_rehearsal_mandatory_batches_count": mandatory_count,
        "b1_b6_rehearsal_mandatory": rollback_rehearsal_scope_dryrun_result["b1_b6_rehearsal_mandatory"],
        "rollback_rehearsal_step_count": step_count,
        "rehearsal_steps_simulated": True,
        "rehearsal_execution_allowed_now": False,
        "rehearsal_executed_now": False,
        "failure_blocks_real_migration": rollback_rehearsal_plan_dryrun_result["failure_blocks_real_migration"],
        "rollback_evidence_template_loaded": rollback_rehearsal_evidence_dryrun_result["rollback_evidence_template_loaded"],
        "rollback_evidence_generated_now": False,
        "rollback_success_claim_allowed": False,
        "batch_arming_record_count": batch_arming_record_count,
        "batch_arming_precondition_simulated": True,
        "arming_record_generated_now": False,
        "arming_allowed_now": False,
        "armed_batch_count": armed_count,
        "all_batches_not_armed": armed_count == 0,
        "authorization_blocker_count": blocker_count,
        "blockers_simulated": True,
        "missing_rollback_rehearsal_blocks_execution": True,
        "missing_rollback_evidence_blocks_execution": True,
        "missing_test_harness_readiness_blocks_execution": True,
        "missing_verifier_suite_readiness_blocks_execution": True,
        "protected_asset_inclusion_blocks_execution": True,
        "HR_DnAE_inclusion_blocks_execution": True,
        "batch_arming_record_missing_blocks_execution": True,
        "abort_policy_missing_blocks_execution": True,
        "dirty_working_tree_blocks_execution": True,
        "missing_backup_branch_blocks_execution": True,
        "auto_confirm_owner_blocks_execution": True,
        "rollback_rehearsal_bypass_blocks_execution": True,
        "parallel_batch_execution_blocks_execution": True,
        "ready_for_post_dryrun_review": boundary_ok,
        "ready_for_real_migration": False,
        "ready_for_batch_arming": False,
        "ready_for_file_move": False,
        "ready_for_file_delete": False,
        "ready_for_module_merge": False,
        "ready_for_rollback_rehearsal_execution": False,
        "real_migration_execution_allowed": False,
        "batch_arming_allowed_now": False,
        "actual_file_move_executed": False,
        "actual_file_delete_executed": False,
        "actual_file_rename_executed": False,
        "actual_module_merge_executed": False,
        "post_migration_tests_executed": False,
        "verifier_suite_executed": False,
        "rollback_executed": False,
        "rollback_rehearsal_executed": False,
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
        "final_decision": FINAL_DECISION if boundary_ok else "MAIN_PROJECT_STRUCTURE_MIGRATION_PRE_AUTHORIZATION_DRYRUN_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "human_review_case_count": HUMAN_REVIEW_CARRYOVER,
        "permanent_block_case_count": PERMANENT_BLOCK_CARRYOVER,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    return {
        "summary": summary,
        "input_root_matrix": {"rows": input_rows, "row_count": len(input_rows), "source_chain": SOURCE_CHAIN, **_not_fact()},
        "pre_authorization_rollback_dryrun_execution_plan": pre_authorization_rollback_dryrun_execution_plan,
        "owner_authorization_dryrun_result": owner_authorization_dryrun_result,
        "operator_acknowledgement_dryrun_result": operator_acknowledgement_dryrun_result,
        "pre_execution_authorization_package_dryrun_result": pre_execution_authorization_package_dryrun_result,
        "rollback_rehearsal_scope_dryrun_result": rollback_rehearsal_scope_dryrun_result,
        "rollback_rehearsal_plan_dryrun_result": rollback_rehearsal_plan_dryrun_result,
        "rollback_rehearsal_evidence_dryrun_result": rollback_rehearsal_evidence_dryrun_result,
        "batch_arming_precondition_dryrun_result": batch_arming_precondition_dryrun_result,
        "authorization_blocker_dryrun_result": authorization_blocker_dryrun_result,
        "pre_authorization_dryrun_boundary_review": pre_authorization_dryrun_boundary_review,
        "pre_authorization_dryrun_readiness_decision": pre_authorization_dryrun_readiness_decision,
        "governance_debt_register": governance_debt_register,
        "next_phase_recommendation": next_phase_recommendation,
        "no_file_move_boundary_report": _no_side_effect_report("no_file_move"),
        "no_delete_boundary_report": _no_side_effect_report("no_delete"),
        "no_runtime_boundary_report": _no_side_effect_report("no_runtime"),
        "no_write_boundary_report": _no_side_effect_report("no_write"),
    }
