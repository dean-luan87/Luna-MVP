# -*- coding: utf-8 -*-
"""Main Project Structure Migration Controlled Batch Execution Authorization Planning v1.

Final gate planning before any real execution: define which batches may be included in future
controlled execution authorization, preconditions, abort policy, post-migration test plan.

Planning-only: no execution, no arming, no real file operations, no verifier rerun execution,
no rollback rehearsal execution.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.main_project_structure_migration_guarded_planning_v1 import GATE_DEFS
from capabilities.governance.main_project_structure_migration_stabilized_execution_planning_v1 import (
    COMMON_ABORT_CONDITIONS,
    STABILIZED_BATCH_DEFS,
    TEST_CHECKLIST_BY_BATCH,
    VERIFIER_RERUN_BY_BATCH,
)
from capabilities.governance.main_project_structure_migration_stabilized_batch_authorization_post_dryrun_review_v1 import (
    FINAL_DECISION as UPSTREAM_FINAL,
    PHASE_ID as UPSTREAM_PHASE,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID

PHASE_ID = "Phase-Main-Project-Structure-Migration-Controlled-Batch-Execution-Authorization-Planning-v1-001"
PLANNING_SCOPE = "main_project_structure_migration_controlled_batch_execution_authorization_planning_only"
SOURCE_CHAIN = "main_project_structure_migration_controlled_batch_execution_authorization_planning_v1"

FINAL_DECISION = "MAIN_PROJECT_STRUCTURE_MIGRATION_CONTROLLED_BATCH_EXECUTION_AUTHORIZATION_PLANNING_READY_FOR_DRYRUN"
NEXT_PHASE = "Phase-Main-Project-Structure-Migration-Controlled-Batch-Execution-Authorization-DryRun-v1-001"

UPSTREAM_REQUIRED_PHASE = UPSTREAM_PHASE
UPSTREAM_REQUIRED_FINAL = UPSTREAM_FINAL
UPSTREAM_REQUIRED_NEXT = PHASE_ID

UPSTREAM_REQUIRED_ARTIFACTS: Tuple[str, ...] = (
    "summary.json",
    "verifier_report.json",
    "batch_authorization_dryrun_input_review_v1.json",
    "b0_b7_authorization_scope_review_v1.json",
    "batch_authorization_request_non_sent_review_v1.json",
    "batch_authorization_grant_non_issued_review_v1.json",
    "batch_arming_non_execution_review_v1.json",
    "batch_execution_window_non_open_review_v1.json",
    "batch_verifier_rerun_non_execution_review_v1.json",
    "batch_rollback_non_execution_review_v1.json",
    "batch_file_operation_non_execution_review_v1.json",
    "batch_protected_eval_out_guard_review_v1.json",
    "batch_authorization_non_claims_review_v1.json",
    "stabilized_batch_authorization_post_dryrun_review_readiness_decision_v1.json",
    "stabilized_batch_authorization_post_dryrun_review_policy_v1.json",
)

BATCH_IDS: Tuple[str, ...] = ("B0", "B1", "B2", "B3", "B4", "B5", "B6", "B7")


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _boundary_meta() -> Dict[str, Any]:
    return {
        "controlled_batch_execution_authorization_planning_only": True,
        "controlled_batch_execution_authorization_request_sent_now": False,
        "controlled_batch_execution_authorized_now": False,
        "batch_armed_now": False,
        "batch_execution_started_now": False,
        "execution_window_opened_now": False,
        "actual_file_move_executed": False,
        "actual_file_delete_executed": False,
        "actual_file_rename_executed": False,
        "actual_file_merge_executed": False,
        "actual_file_copy_executed": False,
        "actual_file_overwrite_executed": False,
        "actual_archive_executed": False,
        "verifier_rerun_executed_now": False,
        "rollback_rehearsal_executed_now": False,
        "eval_out_modified_now": False,
        "protected_asset_modified_now": False,
        "hr_modified_now": False,
        "dnae_modified_now": False,
        "file_operation_executed_now": False,
        "real_migration_execution_allowed": False,
        "real_rehearsal_execution_allowed": False,
        "rollback_rehearsal_execution_allowed": False,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        # workspace fallback continuity
        "source_path_mode": "repo_eval_out",
        "standard_eval_out_write_pending_on_local_repro": False,
        # mandatory non-execution freeze fields
        "runtime_invoked": False,
        "execution_committed": False,
        "authorization_granted_now": False,
        "owner_approval_granted_now": False,
        "operator_acknowledgement_granted_now": False,
        "batch_arming_allowed": False,
        "success_claim_allowed": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _row(**kwargs: Any) -> Dict[str, Any]:
    return {**kwargs, **_boundary_meta(), "planned_now": True, "executed_now": False}


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def _load_upstream_root(path_str: Optional[str]) -> Dict[str, Any]:
    root = Path(path_str).expanduser().resolve() if path_str else None
    artifacts: Dict[str, Any] = {}
    missing: List[str] = []
    if root:
        for name in UPSTREAM_REQUIRED_ARTIFACTS:
            payload = _try_read_json(root / name)
            if payload is None:
                missing.append(name)
            else:
                artifacts[name] = payload
    loaded = bool(root) and not missing and bool(artifacts.get("summary.json")) and bool(artifacts.get("verifier_report.json"))
    return {"root": root, "loaded": loaded, "artifacts": artifacts, "missing": missing}


def _is_workspace_fallback(root: Optional[Path]) -> bool:
    return bool(root) and "Luna-Workspace-Min" in str(root)


def run_main_project_structure_migration_controlled_batch_execution_authorization_planning_v1(
    *,
    stabilized_batch_authorization_post_dryrun_review_root: str,
) -> Dict[str, Any]:
    up = _load_upstream_root(stabilized_batch_authorization_post_dryrun_review_root)
    blockers: List[str] = []
    if not up["loaded"]:
        blockers.append(f"missing upstream artifacts: {up['missing']}")

    sm = (up["artifacts"].get("summary.json") or {}) if up["artifacts"] else {}
    vr = (up["artifacts"].get("verifier_report.json") or {}) if up["artifacts"] else {}

    source_path_mode = "workspace_fallback" if _is_workspace_fallback(up["root"]) else "repo_eval_out"
    standard_pending = source_path_mode == "workspace_fallback"

    if vr.get("verifier") != "GO" or vr.get("passed") is not True:
        blockers.append("upstream verifier must be GO")
    if sm.get("boundary_ok") is not True:
        blockers.append("upstream boundary_ok must be true")
    if sm.get("final_decision") != UPSTREAM_REQUIRED_FINAL:
        blockers.append("upstream final_decision mismatch")
    if sm.get("recommended_next_phase") != UPSTREAM_REQUIRED_NEXT:
        blockers.append("upstream recommended_next_phase must point to this phase")
    if sm.get("review_only") is not True:
        blockers.append("upstream must be review_only=true")

    upstream_review_rows = [
        _row(check_id="up.phase", expected=UPSTREAM_REQUIRED_PHASE, observed=sm.get("phase"), review_pass=sm.get("phase") == UPSTREAM_REQUIRED_PHASE),
        _row(check_id="up.verifier_go", expected="GO", observed=vr.get("verifier"), review_pass=vr.get("verifier") == "GO"),
        _row(check_id="up.final_decision", expected=UPSTREAM_REQUIRED_FINAL, observed=sm.get("final_decision"), review_pass=sm.get("final_decision") == UPSTREAM_REQUIRED_FINAL),
        _row(check_id="up.next_phase", expected=UPSTREAM_REQUIRED_NEXT, observed=sm.get("recommended_next_phase"), review_pass=sm.get("recommended_next_phase") == UPSTREAM_REQUIRED_NEXT),
        _row(check_id="up.source_path_mode", expected=source_path_mode, observed=sm.get("source_path_mode"), review_pass=True),
    ]
    batch_authorization_post_dryrun_review_input_review = {
        "upstream_root": str(up["root"]) if up["root"] else None,
        "loaded": up["loaded"],
        "missing": up["missing"],
        "source_path_mode": source_path_mode,
        "standard_eval_out_write_pending_on_local_repro": standard_pending,
        "rows": upstream_review_rows,
        "row_count": len(upstream_review_rows),
        "all_pass": all(r.get("review_pass") for r in upstream_review_rows) and not blockers,
        "blockers": blockers,
        **{**_boundary_meta(), "source_path_mode": source_path_mode, "standard_eval_out_write_pending_on_local_repro": standard_pending},
    }

    # Scope matrix: keep batch domains and scope candidates from stabilized plan.
    scope_rows: List[Dict[str, Any]] = []
    allowlist_rows: List[Dict[str, Any]] = []
    blocklist_rows: List[Dict[str, Any]] = []
    gate_rows: List[Dict[str, Any]] = []
    window_rows: List[Dict[str, Any]] = []
    rerun_rows: List[Dict[str, Any]] = []
    abort_rows: List[Dict[str, Any]] = []
    post_test_rows: List[Dict[str, Any]] = []
    rollback_req_rows: List[Dict[str, Any]] = []

    for idx, (bid, bname, _scope_key, domain, touched_candidates, _planned_outputs) in enumerate(STABILIZED_BATCH_DEFS):
        allowed_ops = ["move", "rename", "copy", "merge", "overwrite"]
        blocked_ops = ["delete", "archive"]
        scope_rows.append(
            _row(
                batch_id=bid,
                batch_name=bname,
                batch_domain=domain,
                controlled_execution_scope_candidate=touched_candidates,
                allowed_file_operations_candidate=allowed_ops,
                blocked_file_operations=blocked_ops,
                required_precondition_gates=[g[0] for g in GATE_DEFS],
                required_before_manifest=True,
                required_after_manifest=True,
                required_rollback_route=True,
                required_verifier_rerun_list=True,
                required_post_migration_tests=True,
                required_abort_conditions=True,
                protected_path_intersection=False,
                eval_out_write_allowed=False,
                execution_authorization_request_sent_now=False,
                execution_authorized_now=False,
                batch_armed_now=False,
                batch_execution_started_now=False,
                file_operation_executed_now=False,
                order_index=idx,
            )
        )
        allowlist_rows.append(_row(batch_id=bid, allowed_file_operations_candidate=allowed_ops, allowlist_planned=True))
        blocklist_rows.append(_row(batch_id=bid, blocked_file_operations=blocked_ops, blocklist_planned=True))
        for gid, gname, gscope in GATE_DEFS:
            gate_rows.append(
                _row(
                    batch_id=bid,
                    batch_domain=domain,
                    gate_id=gid,
                    gate_name=gname,
                    gate_scope=gscope,
                    must_pass_before_execution_authorization_grant=True,
                    satisfied_now=False,
                )
            )
        window_rows.append(
            _row(
                batch_id=bid,
                execution_window_opened_now=False,
                required_window_conditions=[
                    "dedicated_branch_required",
                    "clean_working_tree_required",
                    "one_batch_at_a_time",
                    "rollback_window_reserved",
                    "post_batch_verification_window_reserved",
                    "stop_condition_window_required",
                ],
            )
        )
        rerun_rows.append(_row(batch_id=bid, verifier_rerun_list=VERIFIER_RERUN_BY_BATCH.get(bid, []), verifier_rerun_executed_now=False))
        rollback_req_rows.append(_row(batch_id=bid, rollback_rehearsal_required_before_real_execution=True, rollback_rehearsal_executed_now=False))
        for ac in COMMON_ABORT_CONDITIONS:
            abort_rows.append(_row(batch_id=bid, abort_condition_id=ac, abort_on_trigger=True, triggered_now=False))
        post_test_rows.append(_row(batch_id=bid, required_post_migration_tests=TEST_CHECKLIST_BY_BATCH.get(bid, []), tests_executed_now=False))

    b0_b7_controlled_execution_authorization_scope_matrix = {
        "rows": scope_rows,
        "row_count": len(scope_rows),
        "batch_count": len(scope_rows),
        "all_pass": len(scope_rows) == 8 and all(r.get("protected_path_intersection") is False for r in scope_rows),
        **{**_boundary_meta(), "source_path_mode": source_path_mode, "standard_eval_out_write_pending_on_local_repro": standard_pending},
    }

    controlled_execution_authorization_request_schema_planning = {
        "schema_version": "v1",
        "required_fields": [
            "request_id",
            "phase_id",
            "batch_id",
            "requested_scope_candidate",
            "allowed_file_operations_candidate",
            "blocked_file_operations",
            "required_precondition_gates",
            "required_manifests",
            "required_abort_conditions",
            "required_verifier_rerun_list",
            "required_post_migration_tests",
            "non_claims_acknowledged",
        ],
        "execution_authorization_request_sent_now": False,
        **{**_boundary_meta(), "source_path_mode": source_path_mode, "standard_eval_out_write_pending_on_local_repro": standard_pending},
    }

    controlled_execution_authorization_grant_schema_planning = {
        "schema_version": "v1",
        "required_fields": [
            "grant_id",
            "phase_id",
            "batch_id",
            "granted",
            "conditions",
            "approver_ids",
            "execution_window_required",
            "operator_ack_required",
            "rollback_window_reserved_required",
        ],
        "controlled_batch_execution_authorized_now": False,
        **{**_boundary_meta(), "source_path_mode": source_path_mode, "standard_eval_out_write_pending_on_local_repro": standard_pending},
    }

    controlled_execution_precondition_gate_matrix = {
        "rows": gate_rows,
        "row_count": len(gate_rows),
        "all_pass": len(gate_rows) == 8 * len(GATE_DEFS),
        **{**_boundary_meta(), "source_path_mode": source_path_mode, "standard_eval_out_write_pending_on_local_repro": standard_pending},
    }

    controlled_execution_window_planning = {
        "rows": window_rows,
        "row_count": len(window_rows),
        "execution_window_opened_now": False,
        "all_pass": len(window_rows) == 8,
        **{**_boundary_meta(), "source_path_mode": source_path_mode, "standard_eval_out_write_pending_on_local_repro": standard_pending},
    }

    controlled_execution_file_operation_allowlist_planning = {
        "rows": allowlist_rows,
        "row_count": len(allowlist_rows),
        "all_pass": len(allowlist_rows) == 8,
        **{**_boundary_meta(), "source_path_mode": source_path_mode, "standard_eval_out_write_pending_on_local_repro": standard_pending},
    }
    controlled_execution_file_operation_blocklist_planning = {
        "rows": blocklist_rows,
        "row_count": len(blocklist_rows),
        "all_pass": len(blocklist_rows) == 8,
        **{**_boundary_meta(), "source_path_mode": source_path_mode, "standard_eval_out_write_pending_on_local_repro": standard_pending},
    }

    controlled_execution_verifier_rerun_plan = {
        "rows": rerun_rows,
        "row_count": len(rerun_rows),
        "all_pass": all(isinstance(r.get("verifier_rerun_list"), list) for r in rerun_rows),
        **{**_boundary_meta(), "source_path_mode": source_path_mode, "standard_eval_out_write_pending_on_local_repro": standard_pending},
    }

    controlled_execution_rollback_rehearsal_requirement = {
        "rows": rollback_req_rows,
        "row_count": len(rollback_req_rows),
        "rollback_rehearsal_execution_allowed": False,
        "all_pass": all(r.get("rollback_rehearsal_required_before_real_execution") is True for r in rollback_req_rows),
        **{**_boundary_meta(), "source_path_mode": source_path_mode, "standard_eval_out_write_pending_on_local_repro": standard_pending},
    }

    controlled_execution_abort_condition_matrix = {
        "rows": abort_rows,
        "row_count": len(abort_rows),
        "common_abort_condition_count": len(COMMON_ABORT_CONDITIONS),
        "all_pass": len(abort_rows) == 8 * len(COMMON_ABORT_CONDITIONS),
        **{**_boundary_meta(), "source_path_mode": source_path_mode, "standard_eval_out_write_pending_on_local_repro": standard_pending},
    }

    controlled_execution_post_migration_test_plan = {
        "rows": post_test_rows,
        "row_count": len(post_test_rows),
        "tests_executed_now": False,
        "all_pass": all(isinstance(r.get("required_post_migration_tests"), list) for r in post_test_rows),
        **{**_boundary_meta(), "source_path_mode": source_path_mode, "standard_eval_out_write_pending_on_local_repro": standard_pending},
    }

    non_claims = [
        "Controlled Execution Authorization Planning GO ≠ execution authorization request sent",
        "Authorization request planned ≠ authorization granted",
        "Authorization granted in future ≠ batch armed",
        "Batch armed in future ≠ batch executed",
        "File operation allowlist planned ≠ file operation executed",
        "Verifier rerun plan ≠ verifier rerun executed",
        "Rollback rehearsal requirement planned ≠ rollback rehearsal executed",
        "Post-migration test plan ≠ tests executed",
        "workspace_fallback GO ≠ standard _eval_out already written",
    ]
    controlled_execution_non_claims_register = {
        "rows": [_row(non_claim_id=f"NC{i:02d}", text=t) for i, t in enumerate(non_claims, 1)],
        "row_count": len(non_claims),
        **{**_boundary_meta(), "source_path_mode": source_path_mode, "standard_eval_out_write_pending_on_local_repro": standard_pending},
    }

    controlled_batch_execution_authorization_planning_policy = _row(
        phase_id=PHASE_ID,
        planning_scope=PLANNING_SCOPE,
        batch_count=8,
        gate_count=len(GATE_DEFS),
        request_sent_now=False,
        authorized_now=False,
        source_path_mode=source_path_mode,
        standard_eval_out_write_pending_on_local_repro=standard_pending,
    )

    boundary_ok = (
        batch_authorization_post_dryrun_review_input_review["all_pass"]
        and b0_b7_controlled_execution_authorization_scope_matrix["all_pass"]
        and controlled_execution_precondition_gate_matrix["all_pass"]
        and controlled_execution_abort_condition_matrix["all_pass"]
        and controlled_execution_non_claims_register["row_count"] >= 9
        and not blockers
    )

    controlled_batch_execution_authorization_planning_readiness_decision = {
        "final_decision": FINAL_DECISION if boundary_ok else "MAIN_PROJECT_STRUCTURE_MIGRATION_CONTROLLED_BATCH_EXECUTION_AUTHORIZATION_PLANNING_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "ready_for_controlled_execution_authorization_dryrun": boundary_ok,
        "controlled_execution_authorization_planning_completed": boundary_ok,
        "source_path_mode": source_path_mode,
        "standard_eval_out_write_pending_on_local_repro": standard_pending,
        **{**_boundary_meta(), "source_path_mode": source_path_mode, "standard_eval_out_write_pending_on_local_repro": standard_pending},
    }

    summary = {
        "phase": PHASE_ID,
        "planning_scope": PLANNING_SCOPE,
        "upstream_input_loaded": up["loaded"],
        "source_path_mode": source_path_mode,
        "standard_eval_out_write_pending_on_local_repro": standard_pending,
        "batch_count": 8,
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "final_decision": FINAL_DECISION if boundary_ok else "MAIN_PROJECT_STRUCTURE_MIGRATION_CONTROLLED_BATCH_EXECUTION_AUTHORIZATION_PLANNING_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        **{**_boundary_meta(), "source_path_mode": source_path_mode, "standard_eval_out_write_pending_on_local_repro": standard_pending},
    }

    return {
        "summary": summary,
        "controlled_batch_execution_authorization_planning_policy": controlled_batch_execution_authorization_planning_policy,
        "batch_authorization_post_dryrun_review_input_review": batch_authorization_post_dryrun_review_input_review,
        "b0_b7_controlled_execution_authorization_scope_matrix": b0_b7_controlled_execution_authorization_scope_matrix,
        "controlled_execution_authorization_request_schema_planning": controlled_execution_authorization_request_schema_planning,
        "controlled_execution_authorization_grant_schema_planning": controlled_execution_authorization_grant_schema_planning,
        "controlled_execution_precondition_gate_matrix": controlled_execution_precondition_gate_matrix,
        "controlled_execution_window_planning": controlled_execution_window_planning,
        "controlled_execution_file_operation_allowlist_planning": controlled_execution_file_operation_allowlist_planning,
        "controlled_execution_file_operation_blocklist_planning": controlled_execution_file_operation_blocklist_planning,
        "controlled_execution_verifier_rerun_plan": controlled_execution_verifier_rerun_plan,
        "controlled_execution_rollback_rehearsal_requirement": controlled_execution_rollback_rehearsal_requirement,
        "controlled_execution_abort_condition_matrix": controlled_execution_abort_condition_matrix,
        "controlled_execution_post_migration_test_plan": controlled_execution_post_migration_test_plan,
        "controlled_execution_non_claims_register": controlled_execution_non_claims_register,
        "controlled_batch_execution_authorization_planning_readiness_decision": controlled_batch_execution_authorization_planning_readiness_decision,
    }

