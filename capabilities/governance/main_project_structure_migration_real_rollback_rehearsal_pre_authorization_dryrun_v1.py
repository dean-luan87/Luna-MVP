# -*- coding: utf-8 -*-
"""Main Project Structure Migration Real Rollback Rehearsal Pre-Authorization DryRun v1.

Pre-authorization dry-run only: simulate evaluation of the authorization chains defined in
Real Rollback Rehearsal Pre-Authorization Planning v1.

Hard boundaries:
- No real authorization granted (owner/operator/window/etc.)
- No sandbox/branch creation or authorization
- No restore map generation or authorization
- No restore operation or authorization
- No verifier rerun (no subprocess)
- No evidence generation or authorization
- No rollback success claim
- No release of real rehearsal execution / real migration execution / batch arming
- No file move/delete/rename/merge, no runtime invocation, no WorldModel/Memory/Fact/Library writes
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

PHASE_ID = "Phase-Main-Project-Structure-Migration-Real-Rollback-Rehearsal-Pre-Authorization-DryRun-v1-001"
DRYRUN_SCOPE = "main_project_structure_migration_real_rollback_rehearsal_pre_authorization_dryrun_only"
DRYRUN_ID = "main_proj_struct_migration_real_rollback_rehearsal_pre_authorization_dryrun_v1_001"
SOURCE_CHAIN = "main_project_structure_migration_real_rollback_rehearsal_pre_authorization_dryrun_v1"

SOURCE_PHASE = "Phase-Main-Project-Structure-Migration-Real-Rollback-Rehearsal-Pre-Authorization-Planning-v1-001"

FINAL_DECISION = (
    "MAIN_PROJECT_STRUCTURE_MIGRATION_REAL_ROLLBACK_REHEARSAL_PRE_AUTHORIZATION_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
)
NEXT_PHASE = (
    "Phase-Main-Project-Structure-Migration-Real-Rollback-Rehearsal-Pre-Authorization-Post-DryRun-Review-v1-001"
)


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
    return {"root": root, "loaded": loaded, "summary": summary_payload or {}, "artifacts": art, "missing": missing}


def _no_side_effect_report(kind: str) -> Dict[str, Any]:
    return {
        "pre_authorization_dryrun_only": True,
        "simulated": True,
        "authorization_granted_now": False,
        "owner_approval_granted_now": False,
        "operator_acknowledgement_granted_now": False,
        "execution_window_opened_now": False,
        "runtime_invoked": False,
        "execution_committed": False,
        "write_allowed": False,
        "fact_status": "not_fact",
        "real_rehearsal_execution_allowed": False,
        "real_migration_execution_allowed": False,
        "batch_arming_allowed": False,
        "sandbox_creation_authorized_now": False,
        "branch_creation_authorized_now": False,
        "sandbox_created_now": False,
        "branch_created_now": False,
        "restore_map_generation_authorized_now": False,
        "restore_map_generated_now": False,
        "restore_operation_executed_now": False,
        "verifier_rerun_executed_now": False,
        "evidence_generated_now": False,
        "rollback_success_claim_allowed": False,
        "protected_asset_modified": False,
        "human_review_queue_modified": False,
        "permanent_block_modified": False,
        "actual_file_move_executed": False,
        "actual_file_delete_executed": False,
        "actual_file_rename_executed": False,
        "actual_module_merge_executed": False,
        "subprocess_invocation": False,
        "runtime_enabled": False,
        "world_model_written": False,
        "memory_written": False,
        "library_written": False,
        "fact_written": False,
        "boundary_ok": True,
        "violations": [],
        "report_kind": kind,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def run_main_project_structure_migration_real_rollback_rehearsal_pre_authorization_dryrun_v1(
    *,
    pre_authorization_planning_root: str,
) -> Dict[str, Any]:
    planning_artifacts = [
        "real_rollback_rehearsal_pre_authorization_planning_policy_v1.json",
        "owner_operator_approval_requirement_matrix_v1.json",
        "execution_window_authorization_planning_v1.json",
        "sandbox_branch_preparation_authorization_plan_v1.json",
        "restore_map_generation_authorization_plan_v1.json",
        "restore_operation_boundary_authorization_plan_v1.json",
        "verifier_rerun_authorization_plan_v1.json",
        "evidence_generation_authorization_plan_v1.json",
        "success_claim_preservation_gate_v1.json",
        "real_rollback_rehearsal_pre_authorization_readiness_decision_v1.json",
        "summary.json",
        "verifier_report.json",
    ]
    upstream = _load_root(pre_authorization_planning_root, "summary.json", planning_artifacts)
    up_summary = upstream["summary"]
    up_art = upstream["artifacts"]

    input_root_matrix = {
        "rows": [
            {
                "intake_id": "pre_authorization_planning",
                "path": str(upstream["root"]) if upstream["root"] else "(not_provided)",
                "loaded": upstream["loaded"],
                "required": True,
                "missing_artifacts": upstream["missing"],
                "status": "loaded" if upstream["loaded"] else "missing_required",
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        ],
        "row_count": 1,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    up_verifier = up_art.get("verifier_report.json") or {}
    up_ready = up_art.get("real_rollback_rehearsal_pre_authorization_readiness_decision_v1.json") or {}

    upstream_go = up_verifier.get("verifier") == "GO" and up_verifier.get("passed") is True
    upstream_boundary_ok = up_summary.get("boundary_ok") is True
    upstream_planning_only = up_summary.get("pre_authorization_planning_only") is True
    upstream_ready_for_dryrun = up_ready.get("ready_for_pre_authorization_dryrun") is True

    upstream_flags_ok = (
        up_summary.get("authorization_granted_now") is False
        and up_summary.get("owner_approval_granted_now") is False
        and up_summary.get("operator_acknowledgement_granted_now") is False
        and up_summary.get("execution_window_opened_now") is False
        and up_summary.get("real_rehearsal_execution_allowed") is False
        and up_summary.get("real_migration_execution_allowed") is False
        and up_summary.get("batch_arming_allowed") is False
    )

    blockers: List[str] = []
    if not upstream["loaded"]:
        blockers.append("pre_authorization_planning_missing_or_incomplete")
    if not upstream_go:
        blockers.append("upstream_planning_verifier_not_go")
    if not upstream_boundary_ok:
        blockers.append("upstream_planning_boundary_not_ok")
    if not upstream_planning_only:
        blockers.append("upstream_pre_authorization_planning_only_not_true")
    if not upstream_ready_for_dryrun:
        blockers.append("upstream_ready_for_pre_authorization_dryrun_not_true")
    if not upstream_flags_ok:
        blockers.append("upstream_permission_or_authorization_flags_not_frozen")

    boundary_ok = not blockers

    # 4.1 policy
    real_rollback_rehearsal_pre_authorization_dryrun_policy = {
        "phase_name": PHASE_ID,
        "dryrun_id": DRYRUN_ID,
        "pre_authorization_dryrun_only": True,
        "simulated": True,
        "source_phase": SOURCE_PHASE,
        "source_verifier_go_observed": upstream_go,
        "source_boundary_ok_observed": upstream_boundary_ok,
        "source_ready_for_pre_authorization_dryrun_observed": upstream_ready_for_dryrun,
        "authorization_granted_now": False,
        "owner_approval_granted_now": False,
        "operator_acknowledgement_granted_now": False,
        "execution_window_opened_now": False,
        "runtime_invoked": False,
        "execution_committed": False,
        "write_allowed": False,
        "fact_status": "not_fact",
        "real_rehearsal_execution_allowed": False,
        "real_migration_execution_allowed": False,
        "batch_arming_allowed": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    # 4.2 owner/operator evaluation (consume >=8)
    oo_plan = up_art.get("owner_operator_approval_requirement_matrix_v1.json") or {}
    oo_rows: List[Dict[str, Any]] = []
    for r in (oo_plan.get("requirements") or []):
        oo_rows.append(
            {
                "requirement_id": r.get("requirement_id"),
                "requirement_name": r.get("requirement_name"),
                "required": True,
                "planned_for_future_authorization_observed": r.get("planned_for_future_authorization") is True,
                "simulated_evaluation": True,
                "satisfied_in_dryrun": False,
                "approval_granted_now": False,
                "owner_approval_granted_now": False,
                "operator_acknowledgement_granted_now": False,
                "blocks_real_rehearsal_execution": True,
                "required_future_phase": r.get("required_future_phase"),
                "dryrun_status": "blocked",
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )
    owner_operator_approval_dryrun_evaluation = {
        "items": oo_rows,
        "item_count": len(oo_rows),
        "owner_approval_granted_now": False,
        "operator_acknowledgement_granted_now": False,
        "authorization_granted_now": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    # 4.3 execution window evaluation (consume >=9)
    win_plan = up_art.get("execution_window_authorization_planning_v1.json") or {}
    win_rows: List[Dict[str, Any]] = []
    for r in (win_plan.get("requirements") or []):
        win_rows.append(
            {
                "window_requirement_id": r.get("window_requirement_id"),
                "requirement_name": r.get("requirement_name"),
                "required": True,
                "planned_now_observed": r.get("planned_now") is True,
                "simulated_evaluation": True,
                "satisfied_in_dryrun": False,
                "execution_window_opened_now": False,
                "blocks_real_rehearsal_execution": True,
                "required_future_phase": "Phase-Execution-Window-Authorization-v1-001",
                "dryrun_status": "blocked",
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )
    execution_window_dryrun_evaluation = {
        "items": win_rows,
        "item_count": len(win_rows),
        "execution_window_opened_now": False,
        "authorization_granted_now": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    # 4.4 sandbox/branch decision
    sb_plan = up_art.get("sandbox_branch_preparation_authorization_plan_v1.json") or {}
    sandbox_branch_authorization_dryrun_decision = {
        "sandbox_required": True,
        "branch_required": True,
        "sandbox_creation_authorization_planned_observed": sb_plan.get("sandbox_creation_authorization_planned") is True,
        "branch_creation_authorization_planned_observed": sb_plan.get("branch_creation_authorization_planned") is True,
        "simulated_decision": True,
        "sandbox_creation_authorized_now": False,
        "branch_creation_authorized_now": False,
        "sandbox_created_now": False,
        "branch_created_now": False,
        "candidate_sandbox_name": sb_plan.get("candidate_sandbox_name"),
        "candidate_branch_name": sb_plan.get("candidate_branch_name"),
        "candidate_names_not_credentials": True,
        "missing_preconditions": sb_plan.get("missing_preconditions") or [],
        "blocks_real_rehearsal_execution": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    # 4.5 restore map decision
    rm_plan = up_art.get("restore_map_generation_authorization_plan_v1.json") or {}
    restore_map_authorization_dryrun_decision = {
        "restore_map_required": True,
        "restore_map_generation_authorization_planned_observed": rm_plan.get("restore_map_generation_authorization_planned") is True,
        "simulated_decision": True,
        "restore_map_generation_authorized_now": False,
        "restore_map_generated_now": False,
        "restore_map_candidate_allowed_for_planning_observed": rm_plan.get("restore_map_candidate_allowed_for_planning") is True,
        "restore_map_candidate_executable": False,
        "protected_scope_rules_observed": bool(rm_plan.get("protected_scope_rules")),
        "HR_DnAE_boundary_rules_observed": bool(rm_plan.get("HR_DnAE_boundary_rules")),
        "missing_preconditions": rm_plan.get("missing_preconditions") or [],
        "blocks_real_rehearsal_execution": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    # 4.6 restore operation boundary evaluation
    rop_plan = up_art.get("restore_operation_boundary_authorization_plan_v1.json") or {}
    rop_rows: List[Dict[str, Any]] = []
    for r in (rop_plan.get("operations") or []):
        rop_rows.append(
            {
                "operation_type": r.get("operation_type"),
                "authorization_planned_observed": r.get("authorization_planned") is True,
                "simulated_evaluation": True,
                "authorization_granted_now": False,
                "operation_allowed_now": False,
                "operation_executed_now": False,
                "protected_scope": r.get("protected_scope"),
                "required_future_gate": r.get("required_future_gate"),
                "abort_condition": r.get("abort_condition"),
                "blocks_real_rehearsal_execution": True,
                "dryrun_status": "blocked",
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )
    restore_operation_boundary_dryrun_evaluation = {
        "items": rop_rows,
        "item_count": len(rop_rows),
        "restore_operation_executed_now": False,
        "authorization_granted_now": False,
        "protected_hr_dnae_boundaries_active": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    # 4.7 verifier rerun evaluation (no subprocess)
    vr_plan = up_art.get("verifier_rerun_authorization_plan_v1.json") or {}
    vr_rows: List[Dict[str, Any]] = []
    for v in (vr_plan.get("verifiers") or []):
        vr_rows.append(
            {
                "verifier_id": v.get("verifier_id"),
                "verifier_name": v.get("verifier_name"),
                "verifier_path": v.get("verifier_path"),
                "planned_for_future_rerun_observed": v.get("planned_for_future_rerun") is True,
                "simulated_evaluation": True,
                "authorized_now": False,
                "executed_now": False,
                "subprocess_invoked": False,
                "expected_input": v.get("expected_input"),
                "expected_output": v.get("expected_output"),
                "failure_response_ref": v.get("failure_response_ref"),
                "blocks_real_rehearsal_execution": True,
                "dryrun_status": "blocked",
                "rollback_specific": bool(v.get("rollback_specific")),
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )
    verifier_rerun_authorization_dryrun_evaluation = {
        "items": vr_rows,
        "item_count": len(vr_rows),
        "rollback_specific_verifier_count": int(vr_plan.get("rollback_specific_verifier_count", 0) or 0),
        "subprocess_invoked": False,
        "verifier_rerun_authorized_now": False,
        "verifier_rerun_executed_now": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    # 4.8 evidence generation evaluation (no evidence)
    ev_plan = up_art.get("evidence_generation_authorization_plan_v1.json") or {}
    ev_rows: List[Dict[str, Any]] = []
    for e in (ev_plan.get("evidence_items") or []):
        ev_rows.append(
            {
                "evidence_type": e.get("evidence_type"),
                "generation_authorization_planned_observed": e.get("generation_authorization_planned") is True,
                "simulated_evaluation": True,
                "generation_authorized_now": False,
                "evidence_generated_now": False,
                "candidate_only": True,
                "not_runtime_evidence": True,
                "not_success_claim": True,
                "required_future_phase": e.get("required_future_phase"),
                "blocks_real_rehearsal_execution": True,
                "dryrun_status": "blocked",
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )
    evidence_generation_authorization_dryrun_evaluation = {
        "items": ev_rows,
        "item_count": len(ev_rows),
        "evidence_generated_now": False,
        "generation_authorized_now": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    # 4.9 success claim gate evaluation
    sc_plan = up_art.get("success_claim_preservation_gate_v1.json") or {}
    success_claim_gate_dryrun_evaluation = {
        "success_claim_allowed": False,
        "success_claim_blocked": True,
        "real_rehearsal_executed": False,
        "authorization_granted_now": False,
        "owner_approval_granted": False,
        "operator_acknowledgement_granted": False,
        "execution_window_opened": False,
        "sandbox_branch_created": False,
        "restore_map_generated": False,
        "restore_operation_executed": False,
        "verifier_rerun_executed": False,
        "evidence_generated": False,
        "success_conditions_met": False,
        "dryrun_status": "blocked",
        "non_claim_statement": (
            "Pre-Authorization DryRun GO does not mean authorization is granted or real rollback rehearsal is executable."
        ),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }
    # preserve original statement as reference-only
    success_claim_gate_dryrun_evaluation["source_non_claim_reference"] = sc_plan.get("non_claim_statement")

    # 4.10 readiness decision
    ready_for_post_review = boundary_ok
    real_rollback_rehearsal_pre_authorization_dryrun_readiness_decision = {
        "ready_for_pre_authorization_post_dryrun_review": bool(ready_for_post_review),
        "ready_for_real_rollback_rehearsal_execution": False,
        "ready_for_real_migration_execution": False,
        "ready_for_batch_arming": False,
        "pre_authorization_dryrun_completed": bool(ready_for_post_review),
        "owner_operator_dryrun_evaluation_generated": True,
        "execution_window_dryrun_evaluation_generated": True,
        "sandbox_branch_authorization_dryrun_decision_generated": True,
        "restore_map_authorization_dryrun_decision_generated": True,
        "restore_operation_boundary_dryrun_evaluation_generated": True,
        "verifier_rerun_authorization_dryrun_evaluation_generated": True,
        "evidence_generation_authorization_dryrun_evaluation_generated": True,
        "success_claim_gate_dryrun_blocked": True,
        "authorization_granted_now": False,
        "final_decision": FINAL_DECISION if ready_for_post_review else "REAL_ROLLBACK_REHEARSAL_PRE_AUTH_DRYRUN_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if ready_for_post_review else PHASE_ID,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    # summary
    summary = {
        "phase": PHASE_ID,
        "dryrun_scope": DRYRUN_SCOPE,
        "pre_authorization_dryrun_only": True,
        "simulated": True,
        "pre_authorization_planning_input_loaded": upstream["loaded"],
        "source_verifier_go_observed": upstream_go,
        "source_boundary_ok_observed": upstream_boundary_ok,
        "source_ready_for_pre_authorization_dryrun_observed": upstream_ready_for_dryrun,
        "authorization_granted_now": False,
        "owner_approval_granted_now": False,
        "operator_acknowledgement_granted_now": False,
        "execution_window_opened_now": False,
        "runtime_invoked": False,
        "execution_committed": False,
        "write_allowed": False,
        "fact_status": "not_fact",
        "real_rehearsal_execution_allowed": False,
        "real_migration_execution_allowed": False,
        "batch_arming_allowed": False,
        "sandbox_creation_authorized_now": False,
        "branch_creation_authorized_now": False,
        "sandbox_created_now": False,
        "branch_created_now": False,
        "restore_map_generation_authorized_now": False,
        "restore_map_generated_now": False,
        "restore_operation_executed_now": False,
        "verifier_rerun_executed_now": False,
        "evidence_generated_now": False,
        "rollback_success_claim_allowed": False,
        "protected_asset_modified": False,
        "human_review_queue_modified": False,
        "permanent_block_modified": False,
        "actual_file_move_executed": False,
        "actual_file_delete_executed": False,
        "actual_file_rename_executed": False,
        "actual_module_merge_executed": False,
        "subprocess_invocation": False,
        "runtime_enabled": False,
        "world_model_written": False,
        "memory_written": False,
        "library_written": False,
        "fact_written": False,
        "owner_operator_dryrun_item_count": len(oo_rows),
        "execution_window_dryrun_item_count": len(win_rows),
        "sandbox_branch_dryrun_decision_generated": True,
        "restore_map_dryrun_decision_generated": True,
        "restore_operation_boundary_dryrun_item_count": len(rop_rows),
        "verifier_rerun_dryrun_item_count": len(vr_rows),
        "rollback_specific_verifier_count": int(vr_plan.get("rollback_specific_verifier_count", 0) or 0),
        "evidence_generation_dryrun_item_count": len(ev_rows),
        "success_claim_gate_blocked": True,
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "final_decision": FINAL_DECISION if ready_for_post_review else "REAL_ROLLBACK_REHEARSAL_PRE_AUTH_DRYRUN_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if ready_for_post_review else PHASE_ID,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    next_phase_recommendation = {
        "recommended_next_phase": NEXT_PHASE if ready_for_post_review else PHASE_ID,
        "final_decision": FINAL_DECISION if ready_for_post_review else "REAL_ROLLBACK_REHEARSAL_PRE_AUTH_DRYRUN_REQUIRES_FIXES",
        "reason": "pre-authorization dryrun only; proceed to post-dryrun review; no authorization granted now",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    return {
        "summary": summary,
        "input_root_matrix": input_root_matrix,
        "real_rollback_rehearsal_pre_authorization_dryrun_policy": real_rollback_rehearsal_pre_authorization_dryrun_policy,
        "owner_operator_approval_dryrun_evaluation": owner_operator_approval_dryrun_evaluation,
        "execution_window_dryrun_evaluation": execution_window_dryrun_evaluation,
        "sandbox_branch_authorization_dryrun_decision": sandbox_branch_authorization_dryrun_decision,
        "restore_map_authorization_dryrun_decision": restore_map_authorization_dryrun_decision,
        "restore_operation_boundary_dryrun_evaluation": restore_operation_boundary_dryrun_evaluation,
        "verifier_rerun_authorization_dryrun_evaluation": verifier_rerun_authorization_dryrun_evaluation,
        "evidence_generation_authorization_dryrun_evaluation": evidence_generation_authorization_dryrun_evaluation,
        "success_claim_gate_dryrun_evaluation": success_claim_gate_dryrun_evaluation,
        "real_rollback_rehearsal_pre_authorization_dryrun_readiness_decision": real_rollback_rehearsal_pre_authorization_dryrun_readiness_decision,
        "next_phase_recommendation": next_phase_recommendation,
        "no_file_move_boundary_report": _no_side_effect_report("no_file_move"),
        "no_delete_boundary_report": _no_side_effect_report("no_delete"),
        "no_runtime_boundary_report": _no_side_effect_report("no_runtime"),
        "no_write_boundary_report": _no_side_effect_report("no_write"),
    }

