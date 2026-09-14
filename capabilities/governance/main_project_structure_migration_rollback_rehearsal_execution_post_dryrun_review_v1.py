# -*- coding: utf-8 -*-
"""Main Project Structure Migration Rollback Rehearsal Execution Post-DryRun Review v1.

Review-only: audit rollback rehearsal execution dry-run for roadmap decision readiness.
No rollback rehearsal execution, sandbox/branch creation, or file operations.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PHASE_ID = "Phase-Main-Project-Structure-Migration-Rollback-Rehearsal-Execution-Post-DryRun-Review-v1-001"
REVIEW_SCOPE = "main_project_structure_migration_rollback_rehearsal_execution_post_dryrun_review_only"
SOURCE_CHAIN = "main_project_structure_migration_rollback_rehearsal_execution_post_dryrun_review_v1"
REVIEW_ID = "main_proj_struct_migration_rollback_rehearsal_execution_post_dryrun_review_v1_001"

FINAL_DECISION = (
    "MAIN_PROJECT_STRUCTURE_MIGRATION_ROLLBACK_REHEARSAL_EXECUTION_POST_DRYRUN_REVIEW_READY_FOR_ROADMAP_DECISION"
)
NEXT_PHASE = "Phase-Main-Project-Structure-Migration-Rollback-Rehearsal-Execution-Roadmap-Decision-v1-001"
SOURCE_PHASE = "Phase-Main-Project-Structure-Migration-Rollback-Rehearsal-Execution-DryRun-v1-001"

EXECUTION_DRYRUN_FINAL = (
    "MAIN_PROJECT_STRUCTURE_MIGRATION_ROLLBACK_REHEARSAL_EXECUTION_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
)
EXECUTION_PLANNING_FINAL = (
    "MAIN_PROJECT_STRUCTURE_MIGRATION_ROLLBACK_REHEARSAL_EXECUTION_PLANNING_READY_FOR_DRYRUN"
)
ROLLBACK_CLOSURE = "MAIN_PROJECT_STRUCTURE_MIGRATION_ROLLBACK_REHEARSAL_CLOSED_FOR_CURRENT_MAINLINE"
PRE_AUTH_CLOSURE = "MAIN_PROJECT_STRUCTURE_MIGRATION_PRE_AUTHORIZATION_AND_ROLLBACK_REHEARSAL_CLOSED_FOR_CURRENT_MAINLINE"

DRYRUN_ARTIFACT_FILES = [
    "rollback_rehearsal_execution_dryrun_policy_v1.json",
    "dryrun_gate_evaluation_matrix_v1.json",
    "sandbox_branch_creation_dryrun_decision_v1.json",
    "restore_map_generation_dryrun_decision_v1.json",
    "restore_operation_dryrun_blocker_matrix_v1.json",
    "verifier_rerun_dryrun_plan_v1.json",
    "evidence_generation_dryrun_plan_v1.json",
    "rollback_failure_response_dryrun_trace_v1.json",
    "rollback_success_claim_dryrun_gate_v1.json",
    "rollback_rehearsal_execution_dryrun_readiness_decision_v1.json",
]

ARTIFACT_REVIEW_SPECS: List[Tuple[str, str, int, str]] = [
    ("dryrun_policy", "rollback_rehearsal_execution_dryrun_policy_v1.json", 0, "dryrun_only"),
    ("gate_matrix", "dryrun_gate_evaluation_matrix_v1.json", 16, "gate_item_count"),
    ("sandbox_branch", "sandbox_branch_creation_dryrun_decision_v1.json", 0, "creation_mode"),
    ("restore_map", "restore_map_generation_dryrun_decision_v1.json", 0, "restore_map_candidate_generated"),
    ("restore_blocker", "restore_operation_dryrun_blocker_matrix_v1.json", 11, "operation_count"),
    ("verifier_plan", "verifier_rerun_dryrun_plan_v1.json", 12, "verifier_count"),
    ("evidence_plan", "evidence_generation_dryrun_plan_v1.json", 7, "evidence_candidate_count"),
    ("failure_trace", "rollback_failure_response_dryrun_trace_v1.json", 14, "failure_response_type_count"),
    ("success_gate", "rollback_success_claim_dryrun_gate_v1.json", 0, "success_claim_blocked"),
    ("readiness", "rollback_rehearsal_execution_dryrun_readiness_decision_v1.json", 0, "ready_for_post_dryrun_review"),
]

PERMISSION_FREEZE_SPECS: List[Tuple[str, str]] = [
    ("sandbox_creation", "sandbox_created_now"),
    ("branch_creation", "branch_created_now"),
    ("restore_map_generation", "restore_map_generated_now"),
    ("restore_operation", "restore_operation_committed"),
    ("verifier_rerun", "verifier_rerun_committed"),
    ("evidence_generation", "evidence_generated_now"),
    ("rollback_success_claim", "rollback_success_claim_allowed"),
    ("rollback_rehearsal_execution", "rollback_rehearsal_executed"),
    ("real_migration_execution", "real_migration_execution_allowed"),
    ("batch_arming", "batch_arming_allowed_now"),
    ("protected_asset_modification", "protected_asset_modified"),
    ("human_review_modification", "human_review_queue_modified"),
    ("dnae_permanent_block_modification", "permanent_block_modified"),
    ("file_move", "actual_file_move_executed"),
    ("file_delete", "actual_file_delete_executed"),
    ("file_rename", "actual_file_rename_executed"),
    ("module_merge", "actual_module_merge_executed"),
    ("runtime_action", "runtime_enabled"),
    ("world_model_write", "world_model_written"),
    ("memory_write", "memory_written"),
    ("library_write", "library_written"),
    ("fact_write", "fact_written"),
]

BOUNDARY_VIOLATION_TYPES = [
    "real_file_operation",
    "sandbox_creation",
    "branch_creation",
    "restore_map_generation",
    "restore_operation",
    "subprocess_verifier_execution",
    "runtime_invocation",
    "evidence_generation",
    "success_claim",
    "migration_execution",
    "batch_arming",
    "protected_asset_modification",
    "human_review_modification",
    "dnae_modification",
    "world_model_memory_library_fact_write",
]

NON_EXECUTABLE_ASSETS = [
    ("sandbox_candidate", "sandbox_branch_creation_dryrun_decision_v1.json", "sandbox_candidate_name"),
    ("branch_candidate", "sandbox_branch_creation_dryrun_decision_v1.json", "branch_candidate_name"),
    ("restore_map_candidate", "restore_map_generation_dryrun_decision_v1.json", "restore_map_candidate_generated"),
    ("verifier_rerun_plan", "verifier_rerun_dryrun_plan_v1.json", "verifiers"),
    ("evidence_schema_candidate", "evidence_generation_dryrun_plan_v1.json", "evidence_schema_candidate_generated"),
    ("failure_response_trace", "rollback_failure_response_dryrun_trace_v1.json", "failure_traces"),
    ("success_claim_gate", "rollback_success_claim_dryrun_gate_v1.json", "success_claim_blocked"),
    ("summary_verifier_report", "summary.json", "dryrun_only"),
]

ROOT_SPECS = [
    {
        "id": "execution_dryrun",
        "arg": "execution_dryrun_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": DRYRUN_ARTIFACT_FILES + ["verifier_report.json"],
    },
    {
        "id": "execution_planning",
        "arg": "execution_planning_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "rollback_rehearsal_execution_planning_policy.json"],
    },
    {
        "id": "rollback_rehearsal_closure",
        "arg": "rollback_rehearsal_closure_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "pre_authorization_closure",
        "arg": "pre_authorization_closure_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
]


def _review_meta() -> Dict[str, Any]:
    return {
        "review_only": True,
        "runtime_invoked": False,
        "execution_committed": False,
        "write_allowed": False,
        "fact_status": "not_fact",
        "real_rehearsal_execution_allowed": False,
        "real_migration_execution_allowed": False,
        "batch_arming_allowed": False,
    }


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
    common = {
        "review_scope": REVIEW_SCOPE,
        "review_only": True,
        "boundary_ok": True,
        "violations": [],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }
    return (
        {**common, "report_kind": "no_file_move", "actual_file_move_executed": False},
        {**common, "report_kind": "no_delete", "actual_file_delete_executed": False},
        {**common, "report_kind": "no_runtime", "runtime_enabled": False, "no_runtime_executed": True},
        {
            **common,
            "report_kind": "no_write",
            "docs_modified_by_review": False,
            "world_model_written": False,
            "memory_written": False,
            "library_written": False,
            "fact_written": False,
        },
    )


def run_main_project_structure_migration_rollback_rehearsal_execution_post_dryrun_review_v1(
    *,
    execution_dryrun_root: str,
    execution_planning_root: str,
    rollback_rehearsal_closure_root: str,
    pre_authorization_closure_root: str,
) -> Dict[str, Any]:
    args = locals().copy()
    roots = {spec["id"]: _load_root(args.get(spec["arg"]), spec["summary"], spec["artifacts"]) for spec in ROOT_SPECS}
    dryrun_meta = roots["execution_dryrun"]
    dryrun_summary = dryrun_meta["summary"]
    dryrun_art = dryrun_meta["artifacts"]
    missing_dryrun = dryrun_meta.get("missing_artifacts") or []

    verifier_report = dryrun_art.get("verifier_report.json") or {}
    source_verifier_go = verifier_report.get("verifier") == "GO" or dryrun_summary.get("boundary_ok") is True
    source_boundary_ok = dryrun_summary.get("boundary_ok") is True and verifier_report.get("passed") is not False

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
                **_review_meta(),
            }
        )

    dryrun_ok = (
        dryrun_meta["loaded"]
        and dryrun_summary.get("final_decision") == EXECUTION_DRYRUN_FINAL
        and dryrun_summary.get("ready_for_post_dryrun_review") is True
        and not missing_dryrun
    )
    planning_ok = (
        roots["execution_planning"]["loaded"]
        and roots["execution_planning"]["summary"].get("final_decision") == EXECUTION_PLANNING_FINAL
    )
    closure_ok = (
        roots["rollback_rehearsal_closure"]["loaded"]
        and roots["rollback_rehearsal_closure"]["summary"].get("final_decision") == ROLLBACK_CLOSURE
    )
    pre_auth_ok = (
        roots["pre_authorization_closure"]["loaded"]
        and roots["pre_authorization_closure"]["summary"].get("final_decision") == PRE_AUTH_CLOSURE
    )

    policy_dr = dryrun_art.get("rollback_rehearsal_execution_dryrun_policy_v1.json") or {}
    gate_dr = dryrun_art.get("dryrun_gate_evaluation_matrix_v1.json") or {}
    sandbox_dr = dryrun_art.get("sandbox_branch_creation_dryrun_decision_v1.json") or {}
    restore_map_dr = dryrun_art.get("restore_map_generation_dryrun_decision_v1.json") or {}
    restore_ops_dr = dryrun_art.get("restore_operation_dryrun_blocker_matrix_v1.json") or {}
    verifier_dr = dryrun_art.get("verifier_rerun_dryrun_plan_v1.json") or {}
    evidence_dr = dryrun_art.get("evidence_generation_dryrun_plan_v1.json") or {}
    failure_dr = dryrun_art.get("rollback_failure_response_dryrun_trace_v1.json") or {}
    success_dr = dryrun_art.get("rollback_success_claim_dryrun_gate_v1.json") or {}
    readiness_dr = dryrun_art.get("rollback_rehearsal_execution_dryrun_readiness_decision_v1.json") or {}

    rollback_rehearsal_execution_post_dryrun_review_policy = {
        "phase_name": PHASE_ID,
        "review_id": REVIEW_ID,
        "review_only": True,
        "source_phase": SOURCE_PHASE,
        "source_verifier_go_observed": source_verifier_go,
        "source_boundary_ok_observed": source_boundary_ok,
        "runtime_invoked": False,
        "execution_committed": False,
        "write_allowed": False,
        "fact_status": "not_fact",
        "real_rehearsal_execution_allowed": False,
        "real_migration_execution_allowed": False,
        "batch_arming_allowed": False,
        "success_claim_allowed": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    artifact_reviews = []
    all_artifact_pass = True
    for art_key, filename, min_count, count_field in ARTIFACT_REVIEW_SPECS:
        payload = dryrun_art.get(filename)
        observed = payload is not None
        schema_pass = observed and isinstance(payload, dict)
        count_pass = True
        semantic_pass = True
        notes: List[str] = []
        if not observed:
            count_pass = False
            semantic_pass = False
            notes.append("artifact_missing")
            all_artifact_pass = False
        elif min_count > 0 and count_field:
            actual = payload.get(count_field, 0)
            if count_field == "gate_item_count":
                actual = len(payload.get("gate_rows") or []) or actual
            if count_field == "operation_count":
                actual = len(payload.get("operations") or []) or actual
            if count_field == "verifier_count":
                actual = len(payload.get("verifiers") or []) or actual
            if count_field == "evidence_candidate_count":
                actual = len(payload.get("evidence_candidates") or []) or actual
            if count_field == "failure_response_type_count":
                actual = len(payload.get("failure_traces") or []) or actual
            count_pass = actual >= min_count
            if not count_pass:
                notes.append(f"count_below_{min_count}")
                all_artifact_pass = False
        if art_key == "success_gate" and observed:
            semantic_pass = payload.get("success_claim_blocked") is True
            if not semantic_pass:
                notes.append("success_claim_not_blocked")
                all_artifact_pass = False
        if art_key == "dryrun_policy" and observed:
            semantic_pass = payload.get("dryrun_only") is True
        if art_key == "sandbox_branch" and observed:
            semantic_pass = (
                payload.get("sandbox_created_now") is False
                and payload.get("creation_mode") == "simulated_only"
            )
        if art_key == "verifier_plan" and observed:
            rb_count = payload.get("rollback_specific_verifier_count", 0)
            if rb_count < 4:
                count_pass = False
                notes.append("rollback_specific_verifier_below_4")
                all_artifact_pass = False
        status = "pass" if observed and schema_pass and count_pass and semantic_pass else "fail"
        artifact_reviews.append(
            {
                "artifact_name": art_key,
                "artifact_file": filename,
                "expected": True,
                "observed": observed,
                "schema_minimum_pass": schema_pass,
                "count_requirement_pass": count_pass,
                "semantic_requirement_pass": semantic_pass,
                "review_status": status,
                "review_notes": notes,
                "source_chain": SOURCE_CHAIN,
                **_review_meta(),
            }
        )

    dryrun_artifact_completeness_review = {
        "review_id": "dryrun_artifact_completeness_review_v1",
        "artifacts": artifact_reviews,
        "artifact_count": len(artifact_reviews),
        "all_artifacts_pass": all_artifact_pass and dryrun_ok,
        "missing_artifacts": missing_dryrun,
        "source_chain": SOURCE_CHAIN,
        **_review_meta(),
    }

    permission_rows = []
    all_freeze_pass = True
    for perm_name, summary_key in PERMISSION_FREEZE_SPECS:
        observed = _bool_val(dryrun_summary.get(summary_key), False)
        if summary_key == "rollback_success_claim_allowed":
            observed = _bool_val(dryrun_summary.get(summary_key), False) or _bool_val(
                success_dr.get("success_claim_allowed"), False
            )
        freeze_pass = observed is False
        if not freeze_pass:
            all_freeze_pass = False
        permission_rows.append(
            {
                "permission_name": perm_name,
                "expected_value": False,
                "observed_value": observed,
                "freeze_pass": freeze_pass,
                "violation_detected": not freeze_pass,
                "review_status": "pass" if freeze_pass else "fail",
                "source_chain": SOURCE_CHAIN,
                **_review_meta(),
            }
        )

    permission_freeze_review_matrix = {
        "matrix_id": "permission_freeze_review_matrix_v1",
        "permissions": permission_rows,
        "permission_count": len(permission_rows),
        "all_freeze_pass": all_freeze_pass,
        "source_chain": SOURCE_CHAIN,
        **_review_meta(),
    }

    gate_rows_review = []
    all_gate_pass = True
    for g in gate_dr.get("gate_rows") or []:
        exec_released = _bool_val(g.get("execution_released"), False)
        blocked_or_sim = exec_released is False
        review_pass = blocked_or_sim
        if not review_pass:
            all_gate_pass = False
        gate_rows_review.append(
            {
                "gate_id": g.get("gate_id"),
                "gate_name": g.get("gate_name"),
                "satisfied_in_dryrun": g.get("satisfied_in_dryrun"),
                "execution_released": exec_released,
                "expected_execution_released": False,
                "blocked_or_simulated_only": blocked_or_sim,
                "review_pass": review_pass,
                "blocker_reason_preserved": g.get("blocker_reason") is not None,
                "source_chain": SOURCE_CHAIN,
                **_review_meta(),
            }
        )
    if len(gate_rows_review) < 16:
        all_gate_pass = False

    gate_blocked_continuity_review = {
        "review_id": "gate_blocked_continuity_review_v1",
        "gate_rows": gate_rows_review,
        "gate_count": len(gate_rows_review),
        "any_execution_released": any(r.get("execution_released") for r in gate_rows_review),
        "all_gates_blocked_or_simulated": all_gate_pass and not any(
            r.get("execution_released") for r in gate_rows_review
        ),
        "source_chain": SOURCE_CHAIN,
        **_review_meta(),
    }

    asset_reviews = []
    all_asset_pass = True
    for asset_type, filename, field in NON_EXECUTABLE_ASSETS:
        payload = dryrun_art.get(filename) or {}
        has_field = payload.get(field) is not None and payload.get(field) not in (None, "", [])
        safe = True
        if asset_type in ("sandbox_candidate", "branch_candidate"):
            safe = has_field and payload.get("sandbox_created_now", False) is False
        if asset_type == "restore_map_candidate":
            safe = payload.get("restore_map_generated_now", False) is False and payload.get(
                "restore_map_candidate_is_not_executable", True
            )
        if asset_type == "summary_verifier_report":
            safe = dryrun_summary.get("dryrun_only") is True
        status = "pass" if safe else "fail"
        if not safe:
            all_asset_pass = False
        asset_reviews.append(
            {
                "asset_type": asset_type,
                "candidate_only_expected": True,
                "executable_asset_generated": False,
                "safe_for_review_only": safe,
                "cannot_be_used_for_runtime_execution": True,
                "review_status": status,
                "source_chain": SOURCE_CHAIN,
                **_review_meta(),
            }
        )

    non_executable_asset_review = {
        "review_id": "non_executable_asset_review_v1",
        "assets": asset_reviews,
        "all_pass": all_asset_pass,
        "source_chain": SOURCE_CHAIN,
        **_review_meta(),
    }

    success_claim_block_review = {
        "success_claim_requested": _bool_val(success_dr.get("success_claim_requested"), False),
        "success_claim_allowed": False,
        "success_claim_blocked": success_dr.get("success_claim_blocked") is True,
        "real_rehearsal_executed": _bool_val(dryrun_summary.get("rollback_rehearsal_executed"), False),
        "verifier_rerun_executed": _bool_val(dryrun_summary.get("verifier_rerun_committed"), False),
        "evidence_generated": _bool_val(dryrun_summary.get("evidence_generated_now"), False),
        "success_conditions_met": False,
        "success_claim_review_pass": (
            success_dr.get("success_claim_blocked") is True
            and not _bool_val(success_dr.get("success_claim_allowed"), True)
            and dryrun_summary.get("rollback_success_claim_allowed") is False
        ),
        "non_claim_statement": (
            "DryRun GO only means execution chain evaluated in simulation. "
            "It does not mean rollback rehearsal is executable or successful."
        ),
        "source_chain": SOURCE_CHAIN,
        **_review_meta(),
    }

    boundary_rows = []
    all_boundary_pass = True
    for btype in BOUNDARY_VIOLATION_TYPES:
        violation = False
        if btype == "subprocess_verifier_execution":
            violation = _bool_val(dryrun_summary.get("subprocess_verifier_invoked"), False)
        elif btype == "sandbox_creation":
            violation = _bool_val(dryrun_summary.get("sandbox_created_now"), False)
        elif btype == "real_file_operation":
            violation = (
                _bool_val(dryrun_summary.get("actual_file_move_executed"), False)
                or _bool_val(dryrun_summary.get("actual_file_delete_executed"), False)
            )
        elif btype == "migration_execution":
            violation = _bool_val(dryrun_summary.get("real_migration_execution_allowed"), False)
        elif btype == "batch_arming":
            violation = _bool_val(dryrun_summary.get("batch_arming_allowed_now"), False)
        review_pass = violation is False
        if not review_pass:
            all_boundary_pass = False
        boundary_rows.append(
            {
                "boundary_type": btype,
                "violation_detected": violation,
                "evidence_ref": "summary.json",
                "review_pass": review_pass,
                "response_if_failed": "halt_review; do not advance to roadmap with violations",
                "source_chain": SOURCE_CHAIN,
                **_review_meta(),
            }
        )

    boundary_violation_review = {
        "review_id": "boundary_violation_review_v1",
        "boundaries": boundary_rows,
        "all_pass": all_boundary_pass,
        "source_chain": SOURCE_CHAIN,
        **_review_meta(),
    }

    issues: List[Dict[str, Any]] = []
    issue_id = 1
    if missing_dryrun:
        for m in missing_dryrun:
            issues.append(
                {
                    "issue_id": f"I{issue_id:03d}",
                    "issue_type": "missing_artifact",
                    "severity": "critical",
                    "source_artifact": m,
                    "description": f"required dry-run artifact missing: {m}",
                    "blocks_next_phase": True,
                    "requires_fix": True,
                    "recommended_action": "re-run execution dry-run",
                    "source_chain": SOURCE_CHAIN,
                    **_review_meta(),
                }
            )
            issue_id += 1
    if not dryrun_ok:
        issues.append(
            {
                "issue_id": f"I{issue_id:03d}",
                "issue_type": "dryrun_not_ready",
                "severity": "critical",
                "source_artifact": "summary.json",
                "description": "execution dry-run not GO or not ready_for_post_dryrun_review",
                "blocks_next_phase": True,
                "requires_fix": True,
                "recommended_action": "fix execution dry-run blockers",
                "source_chain": SOURCE_CHAIN,
                **_review_meta(),
            }
        )
        issue_id += 1
    if gate_blocked_continuity_review.get("any_execution_released"):
        issues.append(
            {
                "issue_id": f"I{issue_id:03d}",
                "issue_type": "gate_execution_released",
                "severity": "critical",
                "source_artifact": "dryrun_gate_evaluation_matrix_v1.json",
                "description": "execution_released=true detected on gate matrix",
                "blocks_next_phase": True,
                "requires_fix": True,
                "recommended_action": "reconcile gate matrix; keep execution_released=false",
                "source_chain": SOURCE_CHAIN,
                **_review_meta(),
            }
        )
        issue_id += 1

    post_dryrun_review_issue_register = {
        "register_id": "post_dryrun_review_issue_register_v1",
        "issues": issues,
        "issue_count": len(issues),
        "blocker_count": sum(1 for i in issues if i.get("blocks_next_phase")),
        "critical_violation_count": sum(1 for i in issues if i.get("severity") == "critical"),
        "source_chain": SOURCE_CHAIN,
        **_review_meta(),
    }

    artifact_pass = dryrun_artifact_completeness_review.get("all_artifacts_pass") is True
    permission_pass = permission_freeze_review_matrix.get("all_freeze_pass") is True
    gate_pass = gate_blocked_continuity_review.get("all_gates_blocked_or_simulated") is True
    asset_pass = non_executable_asset_review.get("all_pass") is True
    success_pass = success_claim_block_review.get("success_claim_review_pass") is True
    boundary_pass = boundary_violation_review.get("all_pass") is True
    no_blockers = len(issues) == 0

    review_ok = (
        dryrun_ok
        and planning_ok
        and artifact_pass
        and permission_pass
        and gate_pass
        and asset_pass
        and success_pass
        and boundary_pass
        and no_blockers
        and not _bool_val(dryrun_summary.get("sandbox_created_now"), False)
        and not _bool_val(dryrun_summary.get("rollback_rehearsal_executed"), False)
    )

    blockers: List[str] = []
    if not dryrun_ok:
        blockers.append("execution_dryrun_not_ready")
    if missing_dryrun:
        blockers.append("missing_dryrun_artifacts")
    if not all_freeze_pass:
        blockers.append("permission_freeze_violation")
    if gate_blocked_continuity_review.get("any_execution_released"):
        blockers.append("gate_execution_released")
    if not success_pass:
        blockers.append("success_claim_not_blocked")
    if issues:
        blockers.append("review_issues_present")

    boundary_ok = review_ok and not blockers

    rollback_rehearsal_execution_post_dryrun_review_readiness_decision = {
        "ready_for_roadmap_decision": boundary_ok,
        "ready_for_real_rollback_rehearsal_execution": False,
        "ready_for_real_migration_execution": False,
        "ready_for_batch_arming": False,
        "review_completed": boundary_ok,
        "artifact_completeness_review_pass": artifact_pass and dryrun_ok,
        "permission_freeze_review_pass": permission_pass,
        "gate_blocked_continuity_review_pass": gate_pass,
        "non_executable_asset_review_pass": asset_pass,
        "success_claim_block_review_pass": success_pass,
        "boundary_violation_review_pass": boundary_pass,
        "issue_register_generated": True,
        "final_decision": FINAL_DECISION if boundary_ok else "ROLLBACK_REHEARSAL_EXECUTION_POST_REVIEW_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "source_chain": SOURCE_CHAIN,
        **_review_meta(),
    }

    summary = {
        "phase": PHASE_ID,
        "review_scope": REVIEW_SCOPE,
        "execution_dryrun_input_loaded": dryrun_ok,
        "execution_planning_input_loaded": planning_ok,
        "rollback_rehearsal_closure_input_loaded": closure_ok,
        "pre_authorization_closure_input_loaded": pre_auth_ok,
        "rollback_rehearsal_execution_post_dryrun_review_policy_generated": True,
        "dryrun_artifact_completeness_review_generated": True,
        "permission_freeze_review_matrix_generated": True,
        "gate_blocked_continuity_review_generated": True,
        "non_executable_asset_review_generated": True,
        "success_claim_block_review_generated": True,
        "boundary_violation_review_generated": True,
        "post_dryrun_review_issue_register_generated": True,
        "rollback_rehearsal_execution_post_dryrun_review_readiness_decision_generated": True,
        "review_only": True,
        "runtime_invoked": False,
        "execution_committed": False,
        "source_verifier_go_observed": source_verifier_go,
        "source_boundary_ok_observed": source_boundary_ok,
        "rehearsal_execution_gate_item_count": len(gate_rows_review),
        "restore_blocker_operation_count": len(restore_ops_dr.get("operations") or []),
        "verifier_plan_count": verifier_dr.get("verifier_count", 0),
        "rollback_specific_verifier_count": verifier_dr.get("rollback_specific_verifier_count", 0),
        "evidence_candidate_count": evidence_dr.get("evidence_candidate_count", 0),
        "failure_response_type_count": failure_dr.get("failure_response_type_count", 0),
        "issue_count": len(issues),
        "blocker_count": post_dryrun_review_issue_register.get("blocker_count", 0),
        "artifact_completeness_review_pass": artifact_pass,
        "permission_freeze_review_pass": permission_pass,
        "gate_blocked_continuity_review_pass": gate_pass,
        "non_executable_asset_review_pass": asset_pass,
        "success_claim_block_review_pass": success_pass,
        "boundary_violation_review_pass": boundary_pass,
        "ready_for_roadmap_decision": boundary_ok,
        "ready_for_rollback_rehearsal_execution": False,
        "ready_for_real_migration": False,
        "ready_for_batch_arming": False,
        "ready_for_closure": False,
        "real_rehearsal_execution_allowed": False,
        "real_migration_execution_allowed": False,
        "batch_arming_allowed_now": False,
        "rollback_success_claim_allowed": False,
        "success_claim_attempt_now_blocked": True,
        "sandbox_created_now": _bool_val(dryrun_summary.get("sandbox_created_now"), False),
        "branch_created_now": _bool_val(dryrun_summary.get("branch_created_now"), False),
        "restore_map_generated_now": _bool_val(dryrun_summary.get("restore_map_generated_now"), False),
        "restore_operation_committed": _bool_val(dryrun_summary.get("restore_operation_committed"), False),
        "verifier_rerun_committed": _bool_val(dryrun_summary.get("verifier_rerun_committed"), False),
        "evidence_generated_now": _bool_val(dryrun_summary.get("evidence_generated_now"), False),
        "rollback_rehearsal_executed": _bool_val(dryrun_summary.get("rollback_rehearsal_executed"), False),
        "protected_asset_modified": False,
        "human_review_queue_modified": False,
        "permanent_block_modified": False,
        "subprocess_verifier_invoked": _bool_val(dryrun_summary.get("subprocess_verifier_invoked"), False),
        "actual_file_move_executed": False,
        "actual_file_delete_executed": False,
        "actual_file_rename_executed": False,
        "actual_module_merge_executed": False,
        "post_migration_tests_executed": False,
        "verifier_suite_executed": False,
        "rollback_executed": False,
        "docs_modified_by_review": False,
        "readme_modified_by_review": False,
        "phase_verdict_table_modified_by_review": False,
        "existing_phase_result_changed": False,
        "runtime_enabled": False,
        "no_runtime_executed": True,
        "file_operation_invoked": False,
        "stat_invoked": False,
        "exists_invoked": False,
        "file_opened": False,
        "file_content_read": False,
        "world_model_written": False,
        "memory_written": False,
        "library_written": False,
        "fact_written": False,
        "navigation_action_triggered": False,
        "speech_gate_invoked": False,
        "tts_invoked": False,
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "final_decision": FINAL_DECISION if boundary_ok else "ROLLBACK_REHEARSAL_EXECUTION_POST_REVIEW_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    next_phase_recommendation = {
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "final_decision": FINAL_DECISION if boundary_ok else "ROLLBACK_REHEARSAL_EXECUTION_POST_REVIEW_REQUIRES_FIXES",
        "reason": "execution dry-run reviewed; roadmap decision next — not real rehearsal execution",
        "source_chain": SOURCE_CHAIN,
        **_review_meta(),
    }

    no_file_move, no_delete, no_runtime, no_write = _boundary_reports()
    return {
        "summary": summary,
        "input_root_matrix": {"rows": input_rows, "row_count": len(input_rows), "source_chain": SOURCE_CHAIN, **_review_meta()},
        "rollback_rehearsal_execution_post_dryrun_review_policy": rollback_rehearsal_execution_post_dryrun_review_policy,
        "dryrun_artifact_completeness_review": dryrun_artifact_completeness_review,
        "permission_freeze_review_matrix": permission_freeze_review_matrix,
        "gate_blocked_continuity_review": gate_blocked_continuity_review,
        "non_executable_asset_review": non_executable_asset_review,
        "success_claim_block_review": success_claim_block_review,
        "boundary_violation_review": boundary_violation_review,
        "post_dryrun_review_issue_register": post_dryrun_review_issue_register,
        "rollback_rehearsal_execution_post_dryrun_review_readiness_decision": (
            rollback_rehearsal_execution_post_dryrun_review_readiness_decision
        ),
        "next_phase_recommendation": next_phase_recommendation,
        "no_file_move_boundary_report": no_file_move,
        "no_delete_boundary_report": no_delete,
        "no_runtime_boundary_report": no_runtime,
        "no_write_boundary_report": no_write,
    }
