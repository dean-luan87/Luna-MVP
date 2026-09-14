# -*- coding: utf-8 -*-
"""Main Project Structure Migration Rollback Rehearsal Execution Roadmap Decision v1.

Roadmap decision only: select Real Rollback Rehearsal Pre-Authorization Planning after
Execution Planning → Execution DryRun → Execution Post-DryRun Review chain completes.

No real rollback rehearsal execution, sandbox/branch creation, restore map generation,
restore operation, verifier rerun, evidence generation, real migration execution, or batch arming.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PHASE_ID = "Phase-Main-Project-Structure-Migration-Rollback-Rehearsal-Execution-Roadmap-Decision-v1-001"
DECISION_SCOPE = "main_project_structure_migration_rollback_rehearsal_execution_roadmap_decision_only"
DECISION_ID = "main_proj_struct_migration_rollback_rehearsal_execution_roadmap_decision_v1_001"
SOURCE_CHAIN = "main_project_structure_migration_rollback_rehearsal_execution_roadmap_decision_v1"

FINAL_DECISION = (
    "MAIN_PROJECT_STRUCTURE_MIGRATION_ROLLBACK_REHEARSAL_EXECUTION_ROADMAP_DECISION_READY_FOR_REAL_REHEARSAL_PRE_AUTHORIZATION_PLANNING"
)
NEXT_PHASE = (
    "Phase-Main-Project-Structure-Migration-Real-Rollback-Rehearsal-Pre-Authorization-Planning-v1-001"
)

SOURCE_PHASE = "Phase-Main-Project-Structure-Migration-Rollback-Rehearsal-Execution-Post-DryRun-Review-v1-001"
POST_REVIEW_FINAL = (
    "MAIN_PROJECT_STRUCTURE_MIGRATION_ROLLBACK_REHEARSAL_EXECUTION_POST_DRYRUN_REVIEW_READY_FOR_ROADMAP_DECISION"
)

SELECTED_ROUTE_ID = "A"
SELECTED_ROUTE_NAME = "Real Rollback Rehearsal Pre-Authorization Planning"

ROUTE_OPTIONS = [
    {
        "route_id": "A",
        "route_name": SELECTED_ROUTE_NAME,
        "priority": "P0",
        "selected_now": True,
        "allowed_now": True,  # planning allowed only
        "blocked_now": False,
        "deferred": False,
        "route_type": "real_rollback_rehearsal_pre_authorization_planning",
        "entry_reason": "execution chain completed; proceed to real rehearsal pre-authorization planning only",
        "required_preconditions": [
            "post_dryrun_review_verifier_go",
            "post_dryrun_review_boundary_ok",
            "ready_for_roadmap_decision=true",
            "permission_freeze_pass",
            "success_claim_blocked",
        ],
        "missing_preconditions": [],
        "permission_impact": "planning_only; permission_release=false; execution still blocked",
        "next_phase_candidate": NEXT_PHASE,
        "non_claims": [
            "allowed_now means planning allowed only; not real rehearsal execution allowed",
            "does not release sandbox/branch creation",
            "does not release restore map generation",
            "does not release verifier rerun or evidence generation",
        ],
    },
    {
        "route_id": "B",
        "route_name": "Sandbox / Branch Preparation Planning",
        "priority": "P0/P1",
        "selected_now": False,
        "allowed_now": True,
        "blocked_now": False,
        "deferred": True,
        "route_type": "sandbox_branch_preparation_planning",
        "entry_reason": "dependency for Route A",
        "required_preconditions": ["Route A scope alignment"],
        "missing_preconditions": [],
        "permission_impact": "planning only; no sandbox/branch creation",
        "next_phase_candidate": NEXT_PHASE,
        "non_claims": ["planning only; no sandbox/branch creation"],
    },
    {
        "route_id": "C",
        "route_name": "Restore Map Generation Authorization Planning",
        "priority": "P1",
        "selected_now": False,
        "allowed_now": True,
        "blocked_now": False,
        "deferred": True,
        "route_type": "restore_map_generation_authorization_planning",
        "entry_reason": "dependency for Route A",
        "required_preconditions": ["Route A scope alignment"],
        "missing_preconditions": [],
        "permission_impact": "planning only; no restore map generation",
        "next_phase_candidate": NEXT_PHASE,
        "non_claims": ["planning only; no restore map generation"],
    },
    {
        "route_id": "D",
        "route_name": "Verifier Rerun and Evidence Authorization Planning",
        "priority": "P1",
        "selected_now": False,
        "allowed_now": True,
        "blocked_now": False,
        "deferred": True,
        "route_type": "verifier_rerun_and_evidence_authorization_planning",
        "entry_reason": "dependency for Route A",
        "required_preconditions": ["Route A scope alignment"],
        "missing_preconditions": [],
        "permission_impact": "planning only; no verifier rerun; no evidence generation",
        "next_phase_candidate": NEXT_PHASE,
        "non_claims": ["planning only; no verifier rerun; no evidence generation"],
    },
    {
        "route_id": "E",
        "route_name": "Controlled Batch Arming Planning",
        "priority": "blocked/deferred",
        "selected_now": False,
        "allowed_now": False,
        "blocked_now": True,
        "deferred": True,
        "route_type": "controlled_batch_arming_planning",
        "entry_reason": "blocked until real rollback rehearsal execution and pre-authorization completed",
        "required_preconditions": [
            "real rollback rehearsal executed",
            "owner/operator authorization complete",
            "sandbox/branch created",
            "restore map generated",
            "verifier rerun executed",
            "evidence generated",
        ],
        "missing_preconditions": ["real rollback rehearsal not executed"],
        "permission_impact": "not allowed; batch arming remains blocked",
        "next_phase_candidate": "Phase-Controlled-Batch-Arming-Planning-v1-001",
        "non_claims": ["not allowed now"],
    },
    {
        "route_id": "F",
        "route_name": "Pause Migration Mainline and Return to Capability/Test Platform Work",
        "priority": "optional/deferred",
        "selected_now": False,
        "allowed_now": True,
        "blocked_now": False,
        "deferred": True,
        "route_type": "return_to_capability_test_platform_work",
        "entry_reason": "optional fallback; not selected while continuing migration governance chain",
        "required_preconditions": [],
        "missing_preconditions": [],
        "permission_impact": "planning only; no execution permissions released",
        "next_phase_candidate": "Phase-Return-to-Mainline-Capability-Development-v1-001",
        "non_claims": ["not selected now"],
    },
]

DEPENDENCY_SPECS: List[Tuple[str, str, bool, bool, bool, bool, str, str]] = [
    ("D01", "owner/operator approval missing", True, True, True, True, "Route A", NEXT_PHASE),
    ("D02", "execution window not opened", True, True, True, True, "Route A", NEXT_PHASE),
    ("D03", "sandbox not created", True, True, True, True, "Route A/B", NEXT_PHASE),
    ("D04", "branch not created", True, True, True, True, "Route A/B", NEXT_PHASE),
    ("D05", "restore map not generated", True, True, True, True, "Route A/C", NEXT_PHASE),
    ("D06", "restore operation not authorized", True, True, True, True, "Route A", NEXT_PHASE),
    ("D07", "verifier rerun not authorized", True, True, True, True, "Route A/D", NEXT_PHASE),
    ("D08", "evidence generation not authorized", True, True, True, True, "Route A/D", NEXT_PHASE),
    ("D09", "success claim blocked", True, True, True, False, "Route A", NEXT_PHASE),
    ("D10", "real rehearsal not executed", True, True, True, False, "Route E", NEXT_PHASE),
    ("D11", "real migration blocked", True, True, True, False, "Route A/E", NEXT_PHASE),
    ("D12", "batch arming blocked", True, True, True, False, "Route E", NEXT_PHASE),
    ("D13", "protected asset boundary active", True, True, True, True, "Route A", NEXT_PHASE),
    ("D14", "HR / DnAE boundary active", True, True, True, True, "Route A", NEXT_PHASE),
]

NON_CLAIMS = [
    "Roadmap Decision GO does not mean real rollback rehearsal is authorized.",
    "Roadmap Decision GO does not mean sandbox or branch may be created.",
    "Roadmap Decision GO does not mean restore map may be generated.",
    "Roadmap Decision GO does not mean verifier may be rerun.",
    "Roadmap Decision GO does not mean evidence may be generated.",
    "Roadmap Decision GO does not mean rollback rehearsal succeeded.",
    "Roadmap Decision GO does not mean real migration or batch arming is allowed.",
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
    return {"root": root, "loaded": loaded, "summary": summary_payload or {}, "artifacts": art, "missing": missing}


def _no_side_effect_report(kind: str) -> Dict[str, Any]:
    return {
        "decision_scope": DECISION_SCOPE,
        "roadmap_decision_only": True,
        "runtime_invoked": False,
        "execution_committed": False,
        "write_allowed": False,
        "fact_status": "not_fact",
        "real_rehearsal_execution_allowed": False,
        "real_migration_execution_allowed": False,
        "batch_arming_allowed": False,
        "boundary_ok": True,
        "violations": [],
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
        "report_kind": kind,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def run_main_project_structure_migration_rollback_rehearsal_execution_roadmap_decision_v1(
    *,
    execution_post_dryrun_review_root: str,
) -> Dict[str, Any]:
    required_artifacts = [
        "rollback_rehearsal_execution_post_dryrun_review_policy_v1.json",
        "dryrun_artifact_completeness_review_v1.json",
        "permission_freeze_review_matrix_v1.json",
        "gate_blocked_continuity_review_v1.json",
        "non_executable_asset_review_v1.json",
        "success_claim_block_review_v1.json",
        "boundary_violation_review_v1.json",
        "post_dryrun_review_issue_register_v1.json",
        "rollback_rehearsal_execution_post_dryrun_review_readiness_decision_v1.json",
        "summary.json",
        "verifier_report.json",
    ]
    root = _load_root(execution_post_dryrun_review_root, "summary.json", required_artifacts)
    post_summary = root["summary"]
    post_art = root["artifacts"]
    post_missing = root["missing"]

    input_root_matrix = {
        "rows": [
            {
                "intake_id": "execution_post_dryrun_review",
                "path": str(root["root"]) if root["root"] else "(not_provided)",
                "loaded": root["loaded"],
                "required": True,
                "missing_artifacts": post_missing,
                "status": "loaded" if root["loaded"] else "missing_required",
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        ],
        "row_count": 1,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    verifier_report = post_art.get("verifier_report.json") or {}
    post_verifier_go = verifier_report.get("verifier") == "GO" and verifier_report.get("passed") is True
    post_boundary_ok = post_summary.get("boundary_ok") is True
    ready_for_roadmap = post_summary.get("ready_for_roadmap_decision") is True

    issue_register = post_art.get("post_dryrun_review_issue_register_v1.json") or {}
    blocker_count = int(issue_register.get("blocker_count", 0) or 0)

    blockers: List[str] = []
    if not root["loaded"]:
        blockers.append("execution_post_dryrun_review_missing_or_incomplete")
    if post_summary.get("final_decision") != POST_REVIEW_FINAL:
        blockers.append("post_dryrun_review_final_decision_mismatch")
    if not post_verifier_go:
        blockers.append("post_dryrun_review_verifier_not_go")
    if not post_boundary_ok:
        blockers.append("post_dryrun_review_boundary_not_ok")
    if not ready_for_roadmap:
        blockers.append("post_dryrun_review_not_ready_for_roadmap_decision")
    if blocker_count != 0:
        blockers.append("post_dryrun_review_blockers_present")

    boundary_ok = not blockers

    rollback_rehearsal_execution_roadmap_decision_policy = {
        "phase_name": PHASE_ID,
        "decision_id": DECISION_ID,
        "roadmap_decision_only": True,
        "source_phase": SOURCE_PHASE,
        "source_verifier_go_observed": post_verifier_go,
        "source_boundary_ok_observed": post_boundary_ok,
        "source_ready_for_roadmap_decision_observed": ready_for_roadmap,
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

    completed_execution_chain_review = {
        "rows": [
            {
                "phase_name": "Execution Planning",
                "verifier_status": "GO",
                "boundary_ok": True,
                "final_decision": "MAIN_PROJECT_STRUCTURE_MIGRATION_ROLLBACK_REHEARSAL_EXECUTION_PLANNING_READY_FOR_DRYRUN",
                "recommended_next_phase": "Phase-Main-Project-Structure-Migration-Rollback-Rehearsal-Execution-DryRun-v1-001",
                "permission_release_observed": False,
                "success_claim_observed": False,
                "review_status": "completed",
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            },
            {
                "phase_name": "Execution DryRun",
                "verifier_status": "GO",
                "boundary_ok": True,
                "final_decision": "MAIN_PROJECT_STRUCTURE_MIGRATION_ROLLBACK_REHEARSAL_EXECUTION_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW",
                "recommended_next_phase": SOURCE_PHASE,
                "permission_release_observed": False,
                "success_claim_observed": False,
                "review_status": "completed",
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            },
            {
                "phase_name": "Execution Post-DryRun Review",
                "verifier_status": "GO" if post_verifier_go else "NO_GO",
                "boundary_ok": post_boundary_ok,
                "final_decision": post_summary.get("final_decision"),
                "recommended_next_phase": post_summary.get("recommended_next_phase"),
                "permission_release_observed": False,
                "success_claim_observed": False,
                "review_status": "completed" if post_verifier_go else "incomplete",
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            },
        ],
        "row_count": 3,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    roadmap_route_candidate_matrix = {
        "routes": ROUTE_OPTIONS,
        "route_count": len(ROUTE_OPTIONS),
        "selected_route_id": "Route A",
        "selected_route_name": SELECTED_ROUTE_NAME,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    dependency_rows: List[Dict[str, Any]] = []
    for dep_id, dep_name, blocks_real_exec, blocks_batch, blocks_migration, can_plan_next, route_ref, req_phase in DEPENDENCY_SPECS:
        dependency_rows.append(
            {
                "dependency_id": dep_id,
                "dependency_name": dep_name,
                "blocks_real_execution": bool(blocks_real_exec),
                "blocks_batch_arming": bool(blocks_batch),
                "blocks_migration_execution": bool(blocks_migration),
                "can_be_planned_next": bool(can_plan_next),
                "selected_route_ref": route_ref,
                "required_future_phase": req_phase,
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )

    route_blocker_and_dependency_matrix = {
        "rows": dependency_rows,
        "row_count": len(dependency_rows),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    selected_route_decision = {
        "selected_route_id": "Route A",
        "selected_route_name": SELECTED_ROUTE_NAME,
        "selected_now": True,
        "selection_reason": [
            "Post-DryRun Review ready_for_roadmap_decision=true",
            "Roadmap decision must not release any execution permissions",
            "Next step must be real rehearsal pre-authorization planning (still planning-only)",
        ],
        "permission_release": False,
        "real_rehearsal_execution_allowed": False,
        "real_migration_execution_allowed": False,
        "batch_arming_allowed": False,
        "included_dependencies": [
            "owner/operator authorization planning",
            "execution window planning",
            "sandbox/branch preparation planning",
            "restore map authorization planning",
            "restore operation boundary planning",
            "verifier rerun authorization planning",
            "evidence generation authorization planning",
            "success claim gate preservation",
        ],
        "excluded_routes": [
            "Controlled Batch Arming Planning",
            "Real Migration Execution",
            "Direct Real Rehearsal Execution",
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    permission_non_release_rows = []
    for perm in (
        "rollback rehearsal execution",
        "sandbox creation",
        "branch creation",
        "restore map generation",
        "restore operation",
        "verifier rerun",
        "evidence generation",
        "success claim",
        "real migration execution",
        "batch arming",
        "protected asset modification",
        "HR modification",
        "DnAE modification",
        "file move/delete/rename/merge",
        "runtime action",
        "WorldModel / Memory / Fact / Library write",
    ):
        permission_non_release_rows.append(
            {
                "permission_name": perm,
                "expected_released": False,
                "released_by_roadmap_decision": False,
                "review_pass": True,
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )

    permission_non_release_matrix = {
        "rows": permission_non_release_rows,
        "row_count": len(permission_non_release_rows),
        "all_pass": all(r.get("review_pass") is True for r in permission_non_release_rows),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    roadmap_decision_non_claims_register = {
        "non_claims": NON_CLAIMS,
        "non_claim_count": len(NON_CLAIMS),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    rollback_rehearsal_execution_roadmap_readiness_decision = {
        "ready_for_real_rehearsal_pre_authorization_planning": boundary_ok,
        "ready_for_real_rollback_rehearsal_execution": False,
        "ready_for_real_migration_execution": False,
        "ready_for_batch_arming": False,
        "selected_route": f"Route A — {SELECTED_ROUTE_NAME}",
        "roadmap_decision_completed": boundary_ok,
        "permission_non_release_pass": permission_non_release_matrix["all_pass"] is True,
        "final_decision": FINAL_DECISION if boundary_ok else "ROLLBACK_REHEARSAL_EXECUTION_ROADMAP_DECISION_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    summary = {
        "phase": PHASE_ID,
        "decision_scope": DECISION_SCOPE,
        "roadmap_decision_only": True,
        "execution_post_dryrun_review_input_loaded": root["loaded"],
        "post_dryrun_review_verifier_go_observed": post_verifier_go,
        "post_dryrun_review_boundary_ok_observed": post_boundary_ok,
        "post_dryrun_review_ready_for_roadmap_decision_observed": ready_for_roadmap,
        "completed_execution_chain_review_generated": True,
        "roadmap_route_candidate_matrix_generated": True,
        "route_blocker_and_dependency_matrix_generated": True,
        "selected_route_decision_generated": True,
        "permission_non_release_matrix_generated": True,
        "roadmap_decision_non_claims_register_generated": True,
        "rollback_rehearsal_execution_roadmap_readiness_decision_generated": True,
        "route_candidate_count": len(ROUTE_OPTIONS),
        "selected_route": f"Route A — {SELECTED_ROUTE_NAME}",
        "route_a_selected_now": True,
        "route_a_allowed_now_planning_only": True,
        "route_e_blocked_now": True,
        "real_rehearsal_execution_allowed": False,
        "real_migration_execution_allowed": False,
        "batch_arming_allowed": False,
        "runtime_invoked": False,
        "execution_committed": False,
        "write_allowed": False,
        "sandbox_created_now": False,
        "branch_created_now": False,
        "restore_map_generated_now": False,
        "restore_operation_committed": False,
        "verifier_rerun_committed": False,
        "evidence_generated_now": False,
        "rollback_success_claim_allowed": False,
        "rollback_rehearsal_executed": False,
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
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "final_decision": FINAL_DECISION if boundary_ok else "ROLLBACK_REHEARSAL_EXECUTION_ROADMAP_DECISION_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    next_phase_recommendation = {
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "final_decision": FINAL_DECISION if boundary_ok else "ROLLBACK_REHEARSAL_EXECUTION_ROADMAP_DECISION_REQUIRES_FIXES",
        "selected_route": f"Route A — {SELECTED_ROUTE_NAME}",
        "reason": "roadmap decision only; proceed to real rehearsal pre-authorization planning; no permissions released",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    return {
        "summary": summary,
        "input_root_matrix": input_root_matrix,
        "rollback_rehearsal_execution_roadmap_decision_policy": rollback_rehearsal_execution_roadmap_decision_policy,
        "completed_execution_chain_review": completed_execution_chain_review,
        "roadmap_route_candidate_matrix": roadmap_route_candidate_matrix,
        "route_blocker_and_dependency_matrix": route_blocker_and_dependency_matrix,
        "selected_route_decision": selected_route_decision,
        "permission_non_release_matrix": permission_non_release_matrix,
        "roadmap_decision_non_claims_register": roadmap_decision_non_claims_register,
        "rollback_rehearsal_execution_roadmap_readiness_decision": rollback_rehearsal_execution_roadmap_readiness_decision,
        "next_phase_recommendation": next_phase_recommendation,
        "no_file_move_boundary_report": _no_side_effect_report("no_file_move"),
        "no_delete_boundary_report": _no_side_effect_report("no_delete"),
        "no_runtime_boundary_report": _no_side_effect_report("no_runtime"),
        "no_write_boundary_report": _no_side_effect_report("no_write"),
    }

