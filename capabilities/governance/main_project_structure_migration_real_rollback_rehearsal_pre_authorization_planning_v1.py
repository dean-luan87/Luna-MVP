# -*- coding: utf-8 -*-
"""Main Project Structure Migration Real Rollback Rehearsal Pre-Authorization Planning v1.

Pre-authorization planning only: expand Route A into authorization requirements, preparation plans,
blockers, human confirmations, evidence requirements, and downstream dry-run path.

Hard boundaries:
- No real rollback rehearsal execution
- No sandbox/branch creation
- No real restore map generation
- No restore operation
- No verifier rerun
- No real evidence generation
- No rollback success claim
- No release of real rehearsal execution / real migration execution / batch arming
- No file move/delete/rename/merge, no runtime invocation, no WorldModel/Memory/Fact/Library writes
- Do not mark owner/operator approval as completed; do not mark execution window as opened
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PHASE_ID = "Phase-Main-Project-Structure-Migration-Real-Rollback-Rehearsal-Pre-Authorization-Planning-v1-001"
PLANNING_SCOPE = "main_project_structure_migration_real_rollback_rehearsal_pre_authorization_planning_only"
PLANNING_ID = "main_proj_struct_migration_real_rollback_rehearsal_pre_authorization_planning_v1_001"
SOURCE_CHAIN = "main_project_structure_migration_real_rollback_rehearsal_pre_authorization_planning_v1"

SOURCE_PHASE = "Phase-Main-Project-Structure-Migration-Rollback-Rehearsal-Execution-Roadmap-Decision-v1-001"
UPSTREAM_SELECTED_ROUTE = "Route A — Real Rollback Rehearsal Pre-Authorization Planning"

UPSTREAM_FINAL_DECISION = (
    "MAIN_PROJECT_STRUCTURE_MIGRATION_ROLLBACK_REHEARSAL_EXECUTION_ROADMAP_DECISION_READY_FOR_REAL_REHEARSAL_PRE_AUTHORIZATION_PLANNING"
)

FINAL_DECISION = "MAIN_PROJECT_STRUCTURE_MIGRATION_REAL_ROLLBACK_REHEARSAL_PRE_AUTHORIZATION_PLANNING_READY_FOR_DRYRUN"
NEXT_PHASE = "Phase-Main-Project-Structure-Migration-Real-Rollback-Rehearsal-Pre-Authorization-DryRun-v1-001"


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


def _candidate_name(prefix: str) -> str:
    # Candidate only: must not be treated as executable credential.
    return f"{prefix}-candidate-not-executable"


def _no_side_effect_report(kind: str) -> Dict[str, Any]:
    return {
        "pre_authorization_planning_only": True,
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
        "sandbox_created_now": False,
        "branch_created_now": False,
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


def run_main_project_structure_migration_real_rollback_rehearsal_pre_authorization_planning_v1(
    *,
    execution_roadmap_decision_root: str,
) -> Dict[str, Any]:
    upstream_artifacts = [
        "rollback_rehearsal_execution_roadmap_decision_policy_v1.json",
        "completed_execution_chain_review_v1.json",
        "roadmap_route_candidate_matrix_v1.json",
        "route_blocker_and_dependency_matrix_v1.json",
        "selected_route_decision_v1.json",
        "permission_non_release_matrix_v1.json",
        "roadmap_decision_non_claims_register_v1.json",
        "rollback_rehearsal_execution_roadmap_readiness_decision_v1.json",
        "summary.json",
        "verifier_report.json",
    ]
    upstream = _load_root(execution_roadmap_decision_root, "summary.json", upstream_artifacts)
    up_summary = upstream["summary"]
    up_art = upstream["artifacts"]

    input_root_matrix = {
        "rows": [
            {
                "intake_id": "execution_roadmap_decision",
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
    upstream_go = up_verifier.get("verifier") == "GO" and up_verifier.get("passed") is True
    upstream_boundary_ok = up_summary.get("boundary_ok") is True
    upstream_selected_route_ok = up_summary.get("selected_route") == UPSTREAM_SELECTED_ROUTE
    upstream_next_phase_ok = up_summary.get("recommended_next_phase") == PHASE_ID
    upstream_permissions_frozen = (
        up_summary.get("real_rehearsal_execution_allowed") is False
        and up_summary.get("real_migration_execution_allowed") is False
        and up_summary.get("batch_arming_allowed") is False
    )
    upstream_final_decision_ok = up_summary.get("final_decision") == UPSTREAM_FINAL_DECISION

    blockers: List[str] = []
    if not upstream["loaded"]:
        blockers.append("upstream_execution_roadmap_decision_missing_or_incomplete")
    if not upstream_go:
        blockers.append("upstream_verifier_not_go")
    if not upstream_boundary_ok:
        blockers.append("upstream_boundary_not_ok")
    if not upstream_selected_route_ok:
        blockers.append("upstream_selected_route_not_route_a")
    if not upstream_next_phase_ok:
        blockers.append("upstream_recommended_next_phase_mismatch")
    if not upstream_permissions_frozen:
        blockers.append("upstream_permission_freeze_not_observed")
    if not upstream_final_decision_ok:
        blockers.append("upstream_final_decision_mismatch")

    boundary_ok = not blockers

    # 4.1 Policy
    real_rollback_rehearsal_pre_authorization_planning_policy = {
        "phase_name": PHASE_ID,
        "planning_id": PLANNING_ID,
        "pre_authorization_planning_only": True,
        "source_phase": SOURCE_PHASE,
        "source_route_selected": "Route A",
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

    # 4.2 Owner/Operator requirements (>=8)
    owner_operator_requirements: List[Dict[str, Any]] = []
    reqs_oo: List[Tuple[str, str, str]] = [
        ("OO01", "owner explicit approval required", "Phase-Owner-Operator-Approval-Authorization-v1-001"),
        ("OO02", "operator acknowledgement required", "Phase-Owner-Operator-Approval-Authorization-v1-001"),
        ("OO03", "rehearsal scope confirmation required", "Phase-Real-Rollback-Rehearsal-Scope-Confirmation-v1-001"),
        ("OO04", "protected asset boundary acknowledgement required", "Phase-Protected-Asset-Boundary-Acknowledgement-v1-001"),
        ("OO05", "HR / DnAE boundary acknowledgement required", "Phase-HR-DnAE-Boundary-Acknowledgement-v1-001"),
        ("OO06", "abort authority confirmation required", "Phase-Abort-Authority-Confirmation-v1-001"),
        ("OO07", "rollback success claim limitation acknowledgement required", "Phase-Success-Claim-Limitation-Acknowledgement-v1-001"),
        ("OO08", "real migration / batch arming non-authorization acknowledgement", "Phase-Non-Authorization-Acknowledgement-v1-001"),
    ]
    for rid, name, future_phase in reqs_oo:
        owner_operator_requirements.append(
            {
                "requirement_id": rid,
                "requirement_name": name,
                "required": True,
                "planned_for_future_authorization": True,
                "satisfied_now": False,
                "approval_granted_now": False,
                "blocks_real_rehearsal_execution": True,
                "required_future_phase": future_phase,
                "non_claim": "planning-only; does not grant approval now",
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )
    owner_operator_approval_requirement_matrix = {
        "requirements": owner_operator_requirements,
        "requirement_count": len(owner_operator_requirements),
        "owner_approval_granted_now": False,
        "operator_acknowledgement_granted_now": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    # 4.3 Execution window requirements (>=9)
    window_requirements: List[Dict[str, Any]] = []
    reqs_win: List[Tuple[str, str]] = [
        ("W01", "execution window start/end defined"),
        ("W02", "no concurrent migration activity"),
        ("W03", "repository clean state check planned"),
        ("W04", "backup / snapshot reference planned"),
        ("W05", "abort window defined"),
        ("W06", "operator availability planned"),
        ("W07", "verifier rerun slot planned"),
        ("W08", "evidence capture slot planned"),
        ("W09", "post-execution review slot planned"),
    ]
    for wid, name in reqs_win:
        window_requirements.append(
            {
                "window_requirement_id": wid,
                "requirement_name": name,
                "required": True,
                "planned_now": True,
                "satisfied_now": False,
                "execution_window_opened_now": False,
                "blocks_real_rehearsal_execution": True,
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )
    execution_window_authorization_planning = {
        "execution_window_opened_now": False,
        "requirements": window_requirements,
        "requirement_count": len(window_requirements),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    # 4.4 Sandbox/branch prep plan (planning only)
    sandbox_branch_preparation_authorization_plan = {
        "sandbox_required": True,
        "branch_required": True,
        "sandbox_creation_authorization_planned": True,
        "branch_creation_authorization_planned": True,
        "sandbox_created_now": False,
        "branch_created_now": False,
        "candidate_sandbox_name": _candidate_name("rollback-rehearsal-sandbox"),
        "candidate_branch_name": _candidate_name("rollback-rehearsal-branch"),
        "required_preconditions": [
            "owner/operator authorization granted",
            "execution window approved",
            "protected asset boundary acknowledged",
        ],
        "missing_preconditions": [
            "owner/operator authorization not granted (planning-only)",
            "execution window not opened (planning-only)",
        ],
        "blocks_real_rehearsal_execution": True,
        "next_phase_candidate": "Phase-Main-Project-Structure-Migration-Real-Rollback-Rehearsal-Pre-Authorization-DryRun-v1-001",
        "candidate_name_non_executable_statement": "candidate names are not executable credentials; creation remains forbidden now",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    # 4.5 Restore map generation authorization plan (planning only)
    restore_map_generation_authorization_plan = {
        "restore_map_required": True,
        "restore_map_generation_authorization_planned": True,
        "restore_map_generated_now": False,
        "restore_map_candidate_allowed_for_planning": True,
        "restore_map_candidate_executable": False,
        "source_structure_map_refs": ["structure_map_ref_planned_only"],
        "protected_scope_rules": ["protected assets excluded unless explicitly authorized in future phase"],
        "HR_DnAE_boundary_rules": ["HR/DnAE excluded unless explicitly authorized in future phase"],
        "required_preconditions": [
            "sandbox/branch prepared",
            "restore map schema agreed",
            "protected/HR/DnAE boundaries reaffirmed",
        ],
        "missing_preconditions": ["sandbox/branch not created", "restore map authorization not granted"],
        "blocks_real_rehearsal_execution": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    # 4.6 Restore operation boundary authorization plan (>=10 types)
    op_types = [
        "file restore",
        "directory restore",
        "docs restore",
        "verdict table restore",
        "eval_out restore",
        "linkage restore",
        "protected asset restore",
        "HR restore",
        "DnAE restore",
        "rollback checkpoint restore",
    ]
    restore_ops: List[Dict[str, Any]] = []
    for t in op_types:
        restore_ops.append(
            {
                "operation_type": t,
                "authorization_planned": True,
                "authorization_granted_now": False,
                "operation_allowed_now": False,
                "operation_executed_now": False,
                "protected_scope": "excluded by default in planning-only",
                "required_future_gate": "pre_authorization_granted_and_execution_window_open",
                "abort_condition": "any boundary violation or missing approval triggers abort",
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )
    restore_operation_boundary_authorization_plan = {
        "operations": restore_ops,
        "operation_count": len(restore_ops),
        "restore_operation_executed_now": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    # 4.7 Verifier rerun authorization plan (>=12, >=4 rollback-specific)
    verifier_items: List[Dict[str, Any]] = []
    verifier_specs: List[Tuple[str, str, str, bool]] = [
        ("V01", "gate taxonomy verifier", "tools/evaluation/governance/verify_gate_taxonomy_v1.py", False),
        ("V02", "structure map consistency verifier", "tools/evaluation/governance/verify_structure_map_v1.py", False),
        ("V03", "protected asset boundary verifier", "tools/evaluation/governance/verify_protected_asset_boundary_v1.py", False),
        ("V04", "human review queue boundary verifier", "tools/evaluation/governance/verify_human_review_boundary_v1.py", False),
        ("V05", "dnae permanent block boundary verifier", "tools/evaluation/governance/verify_dnae_boundary_v1.py", False),
        ("V06", "no file move/delete/rename/merge verifier", "tools/evaluation/governance/verify_no_file_ops_v1.py", False),
        ("V07", "rollback restore map integrity verifier", "tools/evaluation/governance/verify_rollback_restore_map_integrity_v1.py", True),
        ("V08", "rollback restore operation boundary verifier", "tools/evaluation/governance/verify_rollback_restore_operation_boundary_v1.py", True),
        ("V09", "rollback success claim gate verifier", "tools/evaluation/governance/verify_rollback_success_claim_gate_v1.py", True),
        ("V10", "rollback evidence schema verifier", "tools/evaluation/governance/verify_rollback_evidence_schema_v1.py", True),
        ("V11", "verifier rerun plan verifier", "tools/evaluation/governance/verify_verifier_rerun_plan_v1.py", False),
        ("V12", "execution window checklist verifier", "tools/evaluation/governance/verify_execution_window_checklist_v1.py", False),
    ]
    rollback_specific_count = 0
    for vid, name, path, is_rb in verifier_specs:
        if is_rb:
            rollback_specific_count += 1
        verifier_items.append(
            {
                "verifier_id": vid,
                "verifier_name": name,
                "verifier_path": path,
                "planned_for_future_rerun": True,
                "authorized_now": False,
                "executed_now": False,
                "expected_input": "planned only; no subprocess execution now",
                "expected_output": "verifier report (future phase only)",
                "failure_response_ref": "abort_and_escalate",
                "rollback_specific": bool(is_rb),
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )
    verifier_rerun_authorization_plan = {
        "verifier_rerun_authorization_planned": True,
        "verifier_rerun_authorization_granted_now": False,
        "subprocess_invoked": False,
        "verifiers": verifier_items,
        "verifier_count": len(verifier_items),
        "rollback_specific_verifier_count": rollback_specific_count,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    # 4.8 Evidence generation authorization plan (>=7)
    evidence_types: List[Tuple[str, str]] = [
        ("E01", "owner/operator approval evidence"),
        ("E02", "execution window evidence"),
        ("E03", "sandbox/branch preparation evidence"),
        ("E04", "restore map generation evidence"),
        ("E05", "restore operation boundary evidence"),
        ("E06", "verifier rerun evidence"),
        ("E07", "success claim gate evidence"),
    ]
    evidence_items: List[Dict[str, Any]] = []
    for eid, etype in evidence_types:
        evidence_items.append(
            {
                "evidence_id": eid,
                "evidence_type": etype,
                "generation_authorization_planned": True,
                "generation_authorized_now": False,
                "evidence_generated_now": False,
                "candidate_only": True,
                "not_runtime_evidence": True,
                "not_success_claim": True,
                "required_future_phase": "Phase-Main-Project-Structure-Migration-Real-Rollback-Rehearsal-Pre-Authorization-DryRun-v1-001",
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )
    evidence_generation_authorization_plan = {
        "evidence_items": evidence_items,
        "evidence_type_count": len(evidence_items),
        "evidence_generated_now": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    # 4.9 Success claim preservation gate
    success_claim_preservation_gate = {
        "success_claim_allowed": False,
        "success_claim_blocked": True,
        "real_rehearsal_executed": False,
        "owner_approval_granted": False,
        "execution_window_opened": False,
        "sandbox_branch_created": False,
        "restore_map_generated": False,
        "restore_operation_executed": False,
        "verifier_rerun_executed": False,
        "evidence_generated": False,
        "success_conditions_met": False,
        "non_claim_statement": (
            "Pre-Authorization Planning GO does not mean real rollback rehearsal is authorized or executable."
        ),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    # 4.10 Readiness decision
    ready_for_pre_auth_dryrun = boundary_ok
    real_rollback_rehearsal_pre_authorization_readiness_decision = {
        "ready_for_pre_authorization_dryrun": bool(ready_for_pre_auth_dryrun),
        "ready_for_real_rollback_rehearsal_execution": False,
        "ready_for_real_migration_execution": False,
        "ready_for_batch_arming": False,
        "pre_authorization_planning_completed": bool(ready_for_pre_auth_dryrun),
        "owner_operator_requirement_matrix_generated": True,
        "execution_window_planning_generated": True,
        "sandbox_branch_authorization_plan_generated": True,
        "restore_map_authorization_plan_generated": True,
        "restore_operation_boundary_plan_generated": True,
        "verifier_rerun_authorization_plan_generated": True,
        "evidence_generation_authorization_plan_generated": True,
        "success_claim_gate_preserved": True,
        "final_decision": FINAL_DECISION if ready_for_pre_auth_dryrun else "REAL_ROLLBACK_REHEARSAL_PRE_AUTH_PLANNING_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if ready_for_pre_auth_dryrun else PHASE_ID,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    summary = {
        "phase": PHASE_ID,
        "planning_scope": PLANNING_SCOPE,
        "pre_authorization_planning_only": True,
        "execution_roadmap_decision_input_loaded": upstream["loaded"],
        "upstream_verifier_go_observed": upstream_go,
        "upstream_boundary_ok_observed": upstream_boundary_ok,
        "upstream_selected_route_observed": upstream_selected_route_ok,
        "upstream_permissions_frozen_observed": upstream_permissions_frozen,
        "upstream_final_decision_observed": upstream_final_decision_ok,
        "upstream_recommended_next_phase_matches_observed": upstream_next_phase_ok,
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
        "sandbox_created_now": False,
        "branch_created_now": False,
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
        "owner_operator_requirement_count": len(owner_operator_requirements),
        "execution_window_requirement_count": len(window_requirements),
        "restore_operation_boundary_count": len(restore_ops),
        "verifier_plan_count": len(verifier_items),
        "rollback_specific_verifier_count": rollback_specific_count,
        "evidence_type_count": len(evidence_items),
        "success_claim_blocked": True,
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "final_decision": FINAL_DECISION if ready_for_pre_auth_dryrun else "REAL_ROLLBACK_REHEARSAL_PRE_AUTH_PLANNING_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if ready_for_pre_auth_dryrun else PHASE_ID,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    next_phase_recommendation = {
        "recommended_next_phase": NEXT_PHASE if ready_for_pre_auth_dryrun else PHASE_ID,
        "final_decision": FINAL_DECISION if ready_for_pre_auth_dryrun else "REAL_ROLLBACK_REHEARSAL_PRE_AUTH_PLANNING_REQUIRES_FIXES",
        "reason": "pre-authorization planning only; proceed to pre-authorization dryrun simulation; no authorization granted now",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    return {
        "summary": summary,
        "input_root_matrix": input_root_matrix,
        "real_rollback_rehearsal_pre_authorization_planning_policy": real_rollback_rehearsal_pre_authorization_planning_policy,
        "owner_operator_approval_requirement_matrix": owner_operator_approval_requirement_matrix,
        "execution_window_authorization_planning": execution_window_authorization_planning,
        "sandbox_branch_preparation_authorization_plan": sandbox_branch_preparation_authorization_plan,
        "restore_map_generation_authorization_plan": restore_map_generation_authorization_plan,
        "restore_operation_boundary_authorization_plan": restore_operation_boundary_authorization_plan,
        "verifier_rerun_authorization_plan": verifier_rerun_authorization_plan,
        "evidence_generation_authorization_plan": evidence_generation_authorization_plan,
        "success_claim_preservation_gate": success_claim_preservation_gate,
        "real_rollback_rehearsal_pre_authorization_readiness_decision": real_rollback_rehearsal_pre_authorization_readiness_decision,
        "next_phase_recommendation": next_phase_recommendation,
        "no_file_move_boundary_report": _no_side_effect_report("no_file_move"),
        "no_delete_boundary_report": _no_side_effect_report("no_delete"),
        "no_runtime_boundary_report": _no_side_effect_report("no_runtime"),
        "no_write_boundary_report": _no_side_effect_report("no_write"),
    }

