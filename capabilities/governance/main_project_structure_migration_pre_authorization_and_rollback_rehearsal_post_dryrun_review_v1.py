# -*- coding: utf-8 -*-
"""Main Project Structure Migration Pre-Authorization and Rollback Rehearsal Post-DryRun Review v1.

Review-only: audit pre-authorization dry-run for closure readiness.
No real migration, owner confirmation, ack, package, rehearsal, or batch arming.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PHASE_ID = "Phase-Main-Project-Structure-Migration-Pre-Authorization-and-Rollback-Rehearsal-Post-DryRun-Review-v1-001"
REVIEW_SCOPE = "main_project_structure_migration_pre_authorization_and_rollback_rehearsal_post_dryrun_review_only"
SOURCE_CHAIN = "main_project_structure_migration_pre_authorization_and_rollback_rehearsal_post_dryrun_review_v1"
REVIEW_ID = "main_proj_struct_migration_pre_auth_rollback_post_dryrun_review_v1_001"

FINAL_DECISION = "MAIN_PROJECT_STRUCTURE_MIGRATION_PRE_AUTHORIZATION_AND_ROLLBACK_REHEARSAL_POST_DRYRUN_REVIEW_READY_FOR_CLOSURE"
NEXT_PHASE = "Phase-Main-Project-Structure-Migration-Pre-Authorization-and-Rollback-Rehearsal-Closure-v1-001"

DRYRUN_FINAL = "MAIN_PROJECT_STRUCTURE_MIGRATION_PRE_AUTHORIZATION_AND_ROLLBACK_REHEARSAL_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
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

DRYRUN_ARTIFACTS = [
    "pre_authorization_rollback_dryrun_execution_plan.json",
    "owner_authorization_dryrun_result.json",
    "operator_acknowledgement_dryrun_result.json",
    "pre_execution_authorization_package_dryrun_result.json",
    "rollback_rehearsal_scope_dryrun_result.json",
    "rollback_rehearsal_plan_dryrun_result.json",
    "rollback_rehearsal_evidence_dryrun_result.json",
    "batch_arming_precondition_dryrun_result.json",
    "authorization_blocker_dryrun_result.json",
    "pre_authorization_dryrun_boundary_review.json",
    "pre_authorization_dryrun_readiness_decision.json",
]

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
        "id": "pre_authorization_dryrun",
        "arg": "pre_authorization_dryrun_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": DRYRUN_ARTIFACTS,
    },
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
        "artifacts": ["summary.json"],
    },
    {
        "id": "controlled_execution_closure",
        "arg": "controlled_execution_closure_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
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
        "file_operation_invoked": False,
        "stat_invoked": False,
        "exists_invoked": False,
        "file_opened": False,
        "file_content_read": False,
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


def run_main_project_structure_migration_pre_authorization_and_rollback_rehearsal_post_dryrun_review_v1(
    *,
    pre_authorization_dryrun_root: str,
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
    dryrun_art = roots["pre_authorization_dryrun"]["artifacts"]
    dryrun_summary = summaries["pre_authorization_dryrun"]

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
        roots["pre_authorization_dryrun"]["loaded"]
        and dryrun_summary.get("final_decision") == DRYRUN_FINAL
        and dryrun_summary.get("ready_for_post_dryrun_review") is True
    )
    planning_ok = (
        roots["pre_authorization_planning"]["loaded"]
        and summaries["pre_authorization_planning"].get("final_decision") == PLANNING_FINAL
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

    owner_dr = dryrun_art.get("owner_authorization_dryrun_result.json") or {}
    operator_dr = dryrun_art.get("operator_acknowledgement_dryrun_result.json") or {}
    package_dr = dryrun_art.get("pre_execution_authorization_package_dryrun_result.json") or {}
    rb_scope_dr = dryrun_art.get("rollback_rehearsal_scope_dryrun_result.json") or {}
    rb_plan_dr = dryrun_art.get("rollback_rehearsal_plan_dryrun_result.json") or {}
    rb_ev_dr = dryrun_art.get("rollback_rehearsal_evidence_dryrun_result.json") or {}
    arming_dr = dryrun_art.get("batch_arming_precondition_dryrun_result.json") or {}
    blocker_dr = dryrun_art.get("authorization_blocker_dryrun_result.json") or {}
    boundary_dr = dryrun_art.get("pre_authorization_dryrun_boundary_review.json") or {}
    gap_matrix = blocker_dr.get("gap_hard_block_matrix") or {}

    missing_dryrun = roots["pre_authorization_dryrun"].get("missing_artifacts") or []
    pre_authorization_dryrun_input_review = {
        "review_id": REVIEW_ID,
        "pre_authorization_dryrun_input_loaded": dryrun_ok,
        "pre_authorization_planning_input_loaded": planning_ok,
        "controlled_execution_roadmap_input_loaded": roadmap_loaded,
        "required_artifacts_loaded": dryrun_ok and not missing_dryrun,
        "missing_required_artifacts": missing_dryrun,
        "input_status": "complete" if dryrun_ok and not missing_dryrun else "incomplete",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    owner_count = dryrun_summary.get("owner_authorization_type_count", owner_dr.get("owner_authorization_type_count", 0))
    owner_authorization_post_review = {
        "owner_authorization_type_count": owner_count,
        "owner_authorization_simulated": dryrun_summary.get("owner_authorization_simulated", owner_dr.get("owner_authorization_simulated")) is True,
        "owner_confirmed_now": _bool_val(dryrun_summary.get("owner_confirmed_now", owner_dr.get("owner_confirmed_now")), False),
        "owner_approval_executed": _bool_val(dryrun_summary.get("owner_approval_executed", owner_dr.get("owner_approval_executed")), False),
        "owner_approval_execution_allowed": _bool_val(
            dryrun_summary.get("owner_approval_execution_allowed", owner_dr.get("owner_approval_execution_allowed")), False
        ),
        "auto_confirm_allowed": _bool_val(dryrun_summary.get("auto_confirm_allowed", owner_dr.get("auto_confirm_allowed")), False),
        "missing_owner_blocks_execution": owner_dr.get("missing_owner_blocks_execution", True),
        "missing_owner_blocks_batch_arming": owner_dr.get("missing_owner_blocks_batch_arming", True),
        "owner_candidate_not_owner_confirmed": owner_dr.get("owner_candidate_not_equal_owner_confirmed", True),
        "owner_authorization_review_pass": dryrun_ok
        and owner_count == 7
        and not _bool_val(owner_dr.get("owner_confirmed_now"), False)
        and owner_dr.get("owner_authorization_review_pass") is True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    operator_acknowledgement_post_review = {
        "operator_ack_required": operator_dr.get("operator_ack_required", True),
        "operator_ack_simulated": dryrun_summary.get("operator_ack_simulated", operator_dr.get("operator_ack_simulated")) is True,
        "operator_ack_executed_now": _bool_val(operator_dr.get("operator_ack_executed_now"), False),
        "operator_ack_auto_generated": _bool_val(operator_dr.get("operator_ack_auto_generated"), False),
        "missing_operator_ack_blocks_execution": operator_dr.get("missing_operator_ack_blocks_execution", True),
        "missing_operator_ack_blocks_batch_arming": operator_dr.get("missing_operator_ack_blocks_batch_arming", True),
        "operator_ack_required_scope_count": operator_dr.get("operator_ack_required_scope_count", 0),
        "operator_ack_review_pass": dryrun_ok
        and operator_dr.get("operator_ack_required_scope_count", 0) >= 8
        and not _bool_val(operator_dr.get("operator_ack_executed_now"), False)
        and operator_dr.get("operator_ack_review_pass") is True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    included_count = dryrun_summary.get("included_record_count", package_dr.get("included_record_count", 0))
    pre_execution_authorization_package_post_review = {
        "package_required_before_real_migration": package_dr.get("package_required_before_real_migration", True),
        "package_template_loaded": package_dr.get("package_template_loaded", dryrun_summary.get("package_template_loaded")) is True,
        "included_record_count": included_count,
        "package_generated_now": _bool_val(package_dr.get("package_generated_now"), False),
        "package_execution_allowed_now": _bool_val(package_dr.get("package_execution_allowed_now"), False),
        "missing_package_blocks_real_migration": package_dr.get("missing_package_blocks_real_migration", True),
        "package_review_pass": dryrun_ok
        and included_count >= 11
        and not _bool_val(package_dr.get("package_generated_now"), False)
        and package_dr.get("package_review_pass") is True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    rollback_rehearsal_scope_post_review = {
        "rollback_rehearsal_scope_batch_count": dryrun_summary.get(
            "rollback_rehearsal_scope_batch_count", rb_scope_dr.get("rollback_rehearsal_scope_batch_count", 0)
        ),
        "rollback_rehearsal_mandatory_batches_count": dryrun_summary.get(
            "rollback_rehearsal_mandatory_batches_count", rb_scope_dr.get("rollback_rehearsal_mandatory_batches_count", 0)
        ),
        "b1_b6_rehearsal_mandatory": rb_scope_dr.get("b1_b6_rehearsal_mandatory", True),
        "b0_baseline_restore_check_required": rb_scope_dr.get("b0_baseline_restore_check_required", True),
        "b7_verification_gate_restore_check_required": rb_scope_dr.get("b7_verification_gate_restore_check_required", True),
        "restore_path_map_required": rb_scope_dr.get("restore_path_map_required", True),
        "restore_docs_links_required": rb_scope_dr.get("restore_docs_links_required", True),
        "restore_phase_verdict_table_required_if_touched": rb_scope_dr.get(
            "restore_phase_verdict_table_required_if_touched", True
        ),
        "restore_eval_out_refs_required": rb_scope_dr.get("restore_eval_out_refs_required", True),
        "capability_runner_verifier_doc_linkage_restore_required": rb_scope_dr.get(
            "capability_runner_verifier_doc_linkage_restore_required", True
        ),
        "rollback_verifier_rerun_required": rb_scope_dr.get("rollback_verifier_rerun_required", True),
        "rehearsal_execution_allowed_now": _bool_val(rb_scope_dr.get("rehearsal_execution_allowed_now"), False),
        "rehearsal_executed_now": _bool_val(rb_scope_dr.get("rehearsal_executed_now"), False),
        "rehearsal_scope_review_pass": dryrun_ok
        and rb_scope_dr.get("rehearsal_scope_review_pass") is True
        and not _bool_val(rb_scope_dr.get("rehearsal_executed_now"), False),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    step_count = dryrun_summary.get("rollback_rehearsal_step_count", rb_plan_dr.get("rollback_rehearsal_step_count", 0))
    rollback_rehearsal_plan_post_review = {
        "rollback_rehearsal_step_count": step_count,
        "rehearsal_steps_simulated": dryrun_summary.get("rehearsal_steps_simulated", rb_plan_dr.get("rehearsal_steps_simulated")) is True,
        "rehearsal_execution_allowed_now": _bool_val(rb_plan_dr.get("rehearsal_execution_allowed_now"), False),
        "rehearsal_executed_now": _bool_val(rb_plan_dr.get("rehearsal_executed_now"), False),
        "every_step_required": rb_plan_dr.get("every_step_required", True),
        "failure_blocks_real_migration": rb_plan_dr.get("failure_blocks_real_migration", True),
        "rollback_rehearsal_report_required": rb_plan_dr.get("rollback_rehearsal_report_required", True),
        "rollback_rehearsal_review_pass": dryrun_ok
        and step_count >= 10
        and not _bool_val(rb_plan_dr.get("rehearsal_executed_now"), False)
        and rb_plan_dr.get("rollback_rehearsal_review_pass") is True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    rollback_success_claim_allowed = _bool_val(dryrun_summary.get("rollback_success_claim_allowed"), False)

    rollback_rehearsal_evidence_post_review = {
        "rollback_evidence_template_loaded": rb_ev_dr.get("rollback_evidence_template_loaded", True),
        "rollback_evidence_generated_now": _bool_val(rb_ev_dr.get("rollback_evidence_generated_now"), False),
        "rollback_success_claim_allowed": rollback_success_claim_allowed,
        "covered_batches_defined": rb_ev_dr.get("covered_batches_defined", True),
        "restore_path_map_result_required": rb_ev_dr.get("restore_path_map_result_required", True),
        "docs_link_restore_result_required": rb_ev_dr.get("docs_link_restore_result_required", True),
        "verdict_table_restore_result_required": rb_ev_dr.get("verdict_table_restore_result_required", True),
        "eval_out_ref_restore_result_required": rb_ev_dr.get("eval_out_ref_restore_result_required", True),
        "verifier_rerun_result_required": rb_ev_dr.get("verifier_rerun_result_required", True),
        "rollback_evidence_review_pass": dryrun_ok
        and not _bool_val(rb_ev_dr.get("rollback_evidence_generated_now"), False)
        and not rollback_success_claim_allowed
        and rb_ev_dr.get("rollback_evidence_review_pass") is True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    armed_count = arming_dr.get("armed_batch_count", dryrun_summary.get("armed_batch_count", 0))
    sim_batches = arming_dr.get("simulated_batches") or []
    all_not_armed = (
        armed_count == 0
        and arming_dr.get("all_batches_not_armed", dryrun_summary.get("all_batches_not_armed")) is True
        and not any(_bool_val(b.get("armed_now"), False) for b in sim_batches)
    )

    batch_arming_precondition_post_review = {
        "batch_arming_record_count": arming_dr.get("batch_arming_record_count", dryrun_summary.get("batch_arming_record_count", 8)),
        "batch_arming_precondition_simulated": dryrun_summary.get("batch_arming_precondition_simulated") is True,
        "required_owner_approvals_defined": arming_dr.get("required_owner_approvals_defined", True),
        "operator_ack_required": arming_dr.get("operator_ack_required", True),
        "rollback_rehearsal_required": arming_dr.get("rollback_rehearsal_required", True),
        "test_harness_ready_required": arming_dr.get("test_harness_ready_required", True),
        "verifier_suite_ready_required": arming_dr.get("verifier_suite_ready_required", True),
        "protected_asset_exclusion_required": arming_dr.get("protected_asset_exclusion_required", True),
        "HR_DnAE_exclusion_required": arming_dr.get("HR_DnAE_exclusion_required", True),
        "abort_policy_loaded_required": arming_dr.get("abort_policy_loaded_required", True),
        "arming_record_generated_now": _bool_val(arming_dr.get("arming_record_generated_now"), False),
        "arming_allowed_now": _bool_val(arming_dr.get("arming_allowed_now"), False),
        "armed_batch_count": armed_count,
        "all_batches_not_armed": all_not_armed,
        "batch_arming_precondition_review_pass": dryrun_ok
        and armed_count == 0
        and all_not_armed
        and arming_dr.get("batch_arming_precondition_review_pass") is True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    blocker_count = dryrun_summary.get("authorization_blocker_count", blocker_dr.get("authorization_blocker_count", 0))
    authorization_blocker_post_review = {
        "authorization_blocker_count": blocker_count,
        "blockers_simulated": dryrun_summary.get("blockers_simulated", blocker_dr.get("blockers_simulated")) is True,
        "missing_owner_blocks_execution": blocker_dr.get("missing_owner_blocks_execution", True),
        "missing_operator_ack_blocks_execution": blocker_dr.get("missing_operator_ack_blocks_execution", True),
        "missing_rollback_rehearsal_blocks_execution": blocker_dr.get("missing_rollback_rehearsal_blocks_execution", True),
        "missing_rollback_evidence_blocks_execution": blocker_dr.get("missing_rollback_evidence_blocks_execution", True),
        "missing_test_harness_readiness_blocks_execution": blocker_dr.get("missing_test_harness_readiness_blocks_execution", True),
        "missing_verifier_suite_readiness_blocks_execution": blocker_dr.get("missing_verifier_suite_readiness_blocks_execution", True),
        "protected_asset_inclusion_blocks_execution": blocker_dr.get("protected_asset_inclusion_blocks_execution", True),
        "HR_DnAE_inclusion_blocks_execution": blocker_dr.get("HR_DnAE_inclusion_blocks_execution", True),
        "batch_arming_record_missing_blocks_execution": blocker_dr.get("batch_arming_record_missing_blocks_execution", True),
        "abort_policy_missing_blocks_execution": blocker_dr.get("abort_policy_missing_blocks_execution", True),
        "dirty_working_tree_blocks_execution": blocker_dr.get("dirty_working_tree_blocks_execution", True),
        "missing_backup_branch_blocks_execution": blocker_dr.get("missing_backup_branch_blocks_execution", True),
        "auto_confirm_owner_blocks_execution": blocker_dr.get("auto_confirm_owner_blocks_execution", True),
        "rollback_rehearsal_bypass_blocks_execution": blocker_dr.get("rollback_rehearsal_bypass_blocks_execution", True),
        "parallel_batch_execution_blocks_execution": blocker_dr.get("parallel_batch_execution_blocks_execution", True),
        "authorization_blocker_review_pass": dryrun_ok
        and blocker_count >= 14
        and blocker_dr.get("authorization_blocker_review_pass") is True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    gap_hard_block_post_review = {
        "gap_hard_block_matrix_reviewed": bool(gap_matrix),
        "missing_owner_blocks_real_migration": gap_matrix.get("missing_owner", {}).get("blocks_real_migration") is True,
        "missing_owner_blocks_batch_arming": gap_matrix.get("missing_owner", {}).get("blocks_batch_arming") is True,
        "missing_operator_ack_blocks_real_migration": gap_matrix.get("missing_operator_ack", {}).get("blocks_real_migration") is True,
        "missing_operator_ack_blocks_batch_arming": gap_matrix.get("missing_operator_ack", {}).get("blocks_batch_arming") is True,
        "missing_rollback_rehearsal_blocks_real_migration": gap_matrix.get("missing_rollback_rehearsal", {}).get(
            "blocks_real_migration"
        )
        is True,
        "missing_rollback_rehearsal_blocks_batch_arming": gap_matrix.get("missing_rollback_rehearsal", {}).get(
            "blocks_batch_arming"
        )
        is True,
        "missing_package_blocks_real_migration": package_dr.get("missing_package_blocks_real_migration", True),
        "gap_hard_block_review_pass": dryrun_ok
        and gap_matrix.get("missing_owner", {}).get("blocks_real_migration") is True
        and gap_matrix.get("missing_operator_ack", {}).get("blocks_batch_arming") is True
        and gap_matrix.get("missing_rollback_rehearsal", {}).get("blocks_real_migration") is True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    pre_authorization_boundary_post_review = {
        "real_migration_execution_allowed": _bool_val(dryrun_summary.get("real_migration_execution_allowed"), False),
        "batch_arming_allowed_now": _bool_val(dryrun_summary.get("batch_arming_allowed_now"), False),
        "owner_confirmed_now": _bool_val(dryrun_summary.get("owner_confirmed_now"), False),
        "owner_approval_executed": _bool_val(dryrun_summary.get("owner_approval_executed"), False),
        "operator_ack_executed_now": _bool_val(dryrun_summary.get("operator_ack_executed_now"), False),
        "package_generated_now": _bool_val(dryrun_summary.get("package_generated_now"), False),
        "rehearsal_executed_now": _bool_val(dryrun_summary.get("rehearsal_executed_now"), False),
        "rollback_evidence_generated_now": _bool_val(dryrun_summary.get("rollback_evidence_generated_now"), False),
        "armed_batch_count": armed_count,
        "all_batches_not_armed": all_not_armed,
        "actual_file_move_executed": False,
        "actual_file_delete_executed": False,
        "actual_file_rename_executed": False,
        "actual_module_merge_executed": False,
        "runtime_enabled": False,
        "boundary_post_review_pass": dryrun_ok
        and boundary_dr.get("no_real_migration") is True
        and boundary_dr.get("no_batch_arming") is True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    review_passes = [
        owner_authorization_post_review.get("owner_authorization_review_pass"),
        operator_acknowledgement_post_review.get("operator_ack_review_pass"),
        pre_execution_authorization_package_post_review.get("package_review_pass"),
        rollback_rehearsal_scope_post_review.get("rehearsal_scope_review_pass"),
        rollback_rehearsal_plan_post_review.get("rollback_rehearsal_review_pass"),
        rollback_rehearsal_evidence_post_review.get("rollback_evidence_review_pass"),
        batch_arming_precondition_post_review.get("batch_arming_precondition_review_pass"),
        authorization_blocker_post_review.get("authorization_blocker_review_pass"),
        gap_hard_block_post_review.get("gap_hard_block_review_pass"),
        pre_authorization_boundary_post_review.get("boundary_post_review_pass"),
    ]

    blockers: List[str] = []
    if not dryrun_ok:
        blockers.append("pre_authorization_dryrun_not_ready")
    if not planning_ok:
        blockers.append("pre_authorization_planning_not_ready")
    if missing_dryrun:
        blockers.append("dryrun_artifacts_missing")
    if armed_count != 0:
        blockers.append("unexpected_armed_batches")
    if not all(review_passes):
        blockers.append("one_or_more_post_reviews_failed")
    if not gap_hard_block_post_review.get("gap_hard_block_review_pass"):
        blockers.append("gap_hard_block_matrix_not_confirmed")

    boundary_ok = not blockers

    pre_authorization_post_dryrun_readiness_decision = {
        "review_verdict": "GO" if boundary_ok else "NO_GO",
        "blockers": blockers,
        "conditional_notes": [
            "post-dryrun review confirms dry-run chain; no permission granted",
            "owner/ack/rehearsal/package gaps remain blocking",
            "closure next to freeze pre-authorization governance chain",
        ],
        "ready_for_closure": boundary_ok,
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

    governance_debt_review = {
        "items": [
            "post_dryrun_review_audit_only",
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
        "final_decision": FINAL_DECISION if boundary_ok else "MAIN_PROJECT_STRUCTURE_MIGRATION_PRE_AUTHORIZATION_POST_DRYRUN_REVIEW_REQUIRES_FIXES",
        "reason": "dry-run post-review confirms gap hard blocks; ready for closure freeze",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    no_file_move, no_delete, no_runtime, no_write = _boundary_reports()

    summary = {
        "phase": PHASE_ID,
        "review_scope": REVIEW_SCOPE,
        "pre_authorization_dryrun_input_loaded": dryrun_ok,
        "pre_authorization_planning_input_loaded": planning_ok,
        "controlled_execution_roadmap_input_loaded": roadmap_loaded,
        "controlled_execution_closure_input_loaded": ce_closure_loaded,
        "controlled_execution_planning_input_loaded": ce_planning_loaded,
        "execution_control_closure_input_loaded": ec_closure_loaded,
        "guarded_closure_input_loaded": guarded_closure_loaded,
        "readiness_input_loaded": readiness_loaded,
        "protected_asset_resolution_closure_input_loaded": pahr_loaded,
        "structure_map_input_loaded": structure_loaded,
        "gate_taxonomy_input_loaded": gate_loaded,
        "pre_authorization_dryrun_input_review_generated": True,
        "owner_authorization_post_review_generated": True,
        "operator_acknowledgement_post_review_generated": True,
        "pre_execution_authorization_package_post_review_generated": True,
        "rollback_rehearsal_scope_post_review_generated": True,
        "rollback_rehearsal_plan_post_review_generated": True,
        "rollback_rehearsal_evidence_post_review_generated": True,
        "batch_arming_precondition_post_review_generated": True,
        "authorization_blocker_post_review_generated": True,
        "gap_hard_block_post_review_generated": True,
        "pre_authorization_boundary_post_review_generated": True,
        "pre_authorization_post_dryrun_readiness_decision_generated": True,
        "owner_authorization_type_count": owner_count,
        "owner_authorization_simulated": owner_authorization_post_review["owner_authorization_simulated"],
        "owner_confirmed_now": owner_authorization_post_review["owner_confirmed_now"],
        "owner_approval_executed": owner_authorization_post_review["owner_approval_executed"],
        "owner_approval_execution_allowed": owner_authorization_post_review["owner_approval_execution_allowed"],
        "auto_confirm_allowed": owner_authorization_post_review["auto_confirm_allowed"],
        "missing_owner_blocks_execution": owner_authorization_post_review["missing_owner_blocks_execution"],
        "missing_owner_blocks_batch_arming": owner_authorization_post_review["missing_owner_blocks_batch_arming"],
        "owner_candidate_not_owner_confirmed": owner_authorization_post_review["owner_candidate_not_owner_confirmed"],
        "operator_ack_required": operator_acknowledgement_post_review["operator_ack_required"],
        "operator_ack_simulated": operator_acknowledgement_post_review["operator_ack_simulated"],
        "operator_ack_executed_now": operator_acknowledgement_post_review["operator_ack_executed_now"],
        "operator_ack_auto_generated": operator_acknowledgement_post_review["operator_ack_auto_generated"],
        "missing_operator_ack_blocks_execution": operator_acknowledgement_post_review["missing_operator_ack_blocks_execution"],
        "missing_operator_ack_blocks_batch_arming": operator_acknowledgement_post_review["missing_operator_ack_blocks_batch_arming"],
        "package_required_before_real_migration": pre_execution_authorization_package_post_review["package_required_before_real_migration"],
        "package_template_loaded": pre_execution_authorization_package_post_review["package_template_loaded"],
        "included_record_count": included_count,
        "package_generated_now": pre_execution_authorization_package_post_review["package_generated_now"],
        "package_execution_allowed_now": pre_execution_authorization_package_post_review["package_execution_allowed_now"],
        "missing_package_blocks_real_migration": pre_execution_authorization_package_post_review["missing_package_blocks_real_migration"],
        "rollback_rehearsal_scope_batch_count": rollback_rehearsal_scope_post_review["rollback_rehearsal_scope_batch_count"],
        "rollback_rehearsal_mandatory_batches_count": rollback_rehearsal_scope_post_review["rollback_rehearsal_mandatory_batches_count"],
        "b1_b6_rehearsal_mandatory": rollback_rehearsal_scope_post_review["b1_b6_rehearsal_mandatory"],
        "rollback_rehearsal_step_count": step_count,
        "rehearsal_steps_simulated": rollback_rehearsal_plan_post_review["rehearsal_steps_simulated"],
        "rehearsal_execution_allowed_now": rollback_rehearsal_plan_post_review["rehearsal_execution_allowed_now"],
        "rehearsal_executed_now": rollback_rehearsal_plan_post_review["rehearsal_executed_now"],
        "failure_blocks_real_migration": rollback_rehearsal_plan_post_review["failure_blocks_real_migration"],
        "rollback_evidence_template_loaded": rollback_rehearsal_evidence_post_review["rollback_evidence_template_loaded"],
        "rollback_evidence_generated_now": rollback_rehearsal_evidence_post_review["rollback_evidence_generated_now"],
        "rollback_success_claim_allowed": rollback_rehearsal_evidence_post_review["rollback_success_claim_allowed"],
        "batch_arming_record_count": batch_arming_precondition_post_review["batch_arming_record_count"],
        "batch_arming_precondition_simulated": batch_arming_precondition_post_review["batch_arming_precondition_simulated"],
        "arming_record_generated_now": batch_arming_precondition_post_review["arming_record_generated_now"],
        "arming_allowed_now": batch_arming_precondition_post_review["arming_allowed_now"],
        "armed_batch_count": armed_count,
        "all_batches_not_armed": all_not_armed,
        "authorization_blocker_count": blocker_count,
        "blockers_simulated": authorization_blocker_post_review["blockers_simulated"],
        "missing_rollback_rehearsal_blocks_execution": authorization_blocker_post_review["missing_rollback_rehearsal_blocks_execution"],
        "missing_rollback_evidence_blocks_execution": authorization_blocker_post_review["missing_rollback_evidence_blocks_execution"],
        "missing_test_harness_readiness_blocks_execution": authorization_blocker_post_review["missing_test_harness_readiness_blocks_execution"],
        "missing_verifier_suite_readiness_blocks_execution": authorization_blocker_post_review["missing_verifier_suite_readiness_blocks_execution"],
        "protected_asset_inclusion_blocks_execution": authorization_blocker_post_review["protected_asset_inclusion_blocks_execution"],
        "HR_DnAE_inclusion_blocks_execution": authorization_blocker_post_review["HR_DnAE_inclusion_blocks_execution"],
        "batch_arming_record_missing_blocks_execution": authorization_blocker_post_review["batch_arming_record_missing_blocks_execution"],
        "abort_policy_missing_blocks_execution": authorization_blocker_post_review["abort_policy_missing_blocks_execution"],
        "dirty_working_tree_blocks_execution": authorization_blocker_post_review["dirty_working_tree_blocks_execution"],
        "missing_backup_branch_blocks_execution": authorization_blocker_post_review["missing_backup_branch_blocks_execution"],
        "auto_confirm_owner_blocks_execution": authorization_blocker_post_review["auto_confirm_owner_blocks_execution"],
        "rollback_rehearsal_bypass_blocks_execution": authorization_blocker_post_review["rollback_rehearsal_bypass_blocks_execution"],
        "parallel_batch_execution_blocks_execution": authorization_blocker_post_review["parallel_batch_execution_blocks_execution"],
        "gap_hard_block_matrix_reviewed": gap_hard_block_post_review["gap_hard_block_matrix_reviewed"],
        "missing_owner_blocks_real_migration": gap_hard_block_post_review["missing_owner_blocks_real_migration"],
        "missing_owner_blocks_batch_arming": gap_hard_block_post_review["missing_owner_blocks_batch_arming"],
        "missing_operator_ack_blocks_real_migration": gap_hard_block_post_review["missing_operator_ack_blocks_real_migration"],
        "missing_operator_ack_blocks_batch_arming": gap_hard_block_post_review["missing_operator_ack_blocks_batch_arming"],
        "missing_rollback_rehearsal_blocks_real_migration": gap_hard_block_post_review["missing_rollback_rehearsal_blocks_real_migration"],
        "missing_rollback_rehearsal_blocks_batch_arming": gap_hard_block_post_review["missing_rollback_rehearsal_blocks_batch_arming"],
        "ready_for_closure": boundary_ok,
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
        "final_decision": FINAL_DECISION if boundary_ok else "MAIN_PROJECT_STRUCTURE_MIGRATION_PRE_AUTHORIZATION_POST_DRYRUN_REVIEW_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "human_review_case_count": HUMAN_REVIEW_CARRYOVER,
        "permanent_block_case_count": PERMANENT_BLOCK_CARRYOVER,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    return {
        "summary": summary,
        "input_root_matrix": {"rows": input_rows, "row_count": len(input_rows), "source_chain": SOURCE_CHAIN, **_not_fact()},
        "pre_authorization_dryrun_input_review": pre_authorization_dryrun_input_review,
        "owner_authorization_post_review": owner_authorization_post_review,
        "operator_acknowledgement_post_review": operator_acknowledgement_post_review,
        "pre_execution_authorization_package_post_review": pre_execution_authorization_package_post_review,
        "rollback_rehearsal_scope_post_review": rollback_rehearsal_scope_post_review,
        "rollback_rehearsal_plan_post_review": rollback_rehearsal_plan_post_review,
        "rollback_rehearsal_evidence_post_review": rollback_rehearsal_evidence_post_review,
        "batch_arming_precondition_post_review": batch_arming_precondition_post_review,
        "authorization_blocker_post_review": authorization_blocker_post_review,
        "gap_hard_block_post_review": gap_hard_block_post_review,
        "pre_authorization_boundary_post_review": pre_authorization_boundary_post_review,
        "pre_authorization_post_dryrun_readiness_decision": pre_authorization_post_dryrun_readiness_decision,
        "governance_debt_review": governance_debt_review,
        "next_phase_recommendation": next_phase_recommendation,
        "no_file_move_boundary_report": no_file_move,
        "no_delete_boundary_report": no_delete,
        "no_runtime_boundary_report": no_runtime,
        "no_write_boundary_report": no_write,
    }
