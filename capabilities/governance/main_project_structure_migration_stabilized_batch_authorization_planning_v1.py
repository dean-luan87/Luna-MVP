# -*- coding: utf-8 -*-
"""Main Project Structure Migration Stabilized Batch Authorization Planning v1.

Batch authorization planning only: define future authorization request/grant mechanisms for B0–B7.
No authorization request sent, no authorization granted, no batch arming, no real migration,
no verifier rerun execution, no rollback rehearsal execution, no file operations.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.main_project_structure_migration_guarded_planning_v1 import GATE_DEFS
from capabilities.governance.main_project_structure_migration_stabilized_execution_planning_v1 import (
    STABILIZED_BATCH_DEFS,
)
from capabilities.governance.main_project_structure_migration_stabilized_execution_post_dryrun_review_v1 import (
    FINAL_DECISION as POST_REVIEW_FINAL,
    PHASE_ID as POST_REVIEW_PHASE,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID

PHASE_ID = "Phase-Main-Project-Structure-Migration-Stabilized-Batch-Authorization-Planning-v1-001"
PLANNING_SCOPE = "main_project_structure_migration_stabilized_batch_authorization_planning_only"
SOURCE_CHAIN = "main_project_structure_migration_stabilized_batch_authorization_planning_v1"

FINAL_DECISION = "MAIN_PROJECT_STRUCTURE_MIGRATION_STABILIZED_BATCH_AUTHORIZATION_PLANNING_READY_FOR_DRYRUN"
NEXT_PHASE = "Phase-Main-Project-Structure-Migration-Stabilized-Batch-Authorization-DryRun-v1-001"

POST_REVIEW_REQUIRED_PHASE = POST_REVIEW_PHASE
POST_REVIEW_REQUIRED_FINAL = POST_REVIEW_FINAL
POST_REVIEW_REQUIRED_NEXT = PHASE_ID

POST_REVIEW_REQUIRED_ARTIFACTS: Tuple[str, ...] = (
    "summary.json",
    "verifier_report.json",
    "execution_dryrun_input_review_v1.json",
    "b0_b7_batch_trace_completeness_review_v1.json",
    "batch_pre_gate_review_v1.json",
    "batch_manifest_review_v1.json",
    "batch_rollback_route_review_v1.json",
    "batch_verifier_rerun_non_execution_review_v1.json",
    "batch_protected_asset_guard_review_v1.json",
    "batch_eval_out_readonly_guard_review_v1.json",
    "batch_domain_isolation_review_v1.json",
    "batch_abort_condition_review_v1.json",
    "file_operation_non_execution_review_v1.json",
    "stabilized_execution_post_dryrun_review_readiness_decision_v1.json",
    "stabilized_execution_post_dryrun_review_policy_v1.json",
)


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _boundary_meta() -> Dict[str, Any]:
    return {
        "batch_authorization_planning_only": True,
        "batch_authorization_request_sent_now": False,
        "batch_authorization_granted_now": False,
        "batch_armed_now": False,
        "batch_execution_started_now": False,
        "actual_file_move_executed": False,
        "actual_file_delete_executed": False,
        "actual_file_rename_executed": False,
        "actual_file_merge_executed": False,
        "actual_file_copy_executed": False,
        "actual_file_overwrite_executed": False,
        "actual_archive_executed": False,
        "real_migration_execution_allowed": False,
        "real_rehearsal_execution_allowed": False,
        "rollback_rehearsal_execution_allowed": False,
        "verifier_rerun_executed_now": False,
        "eval_out_modified_now": False,
        "protected_asset_modified_now": False,
        "hr_modified_now": False,
        "dnae_modified_now": False,
        "file_operation_executed_now": False,
        "registry_generation_authorization_branch_paused": True,
        "registry_generation_authorization_continued_now": False,
        "governance_constraint_module_branch_closed": True,
        "governance_constraint_module_as_deferred_capability": True,
        "governance_constraint_module_enforced_now": False,
        "artifact_generation_planning_continued_now": False,
        "boundary_object_registry_generated_now": False,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        # mandatory non-execution freeze fields
        "runtime_invoked": False,
        "execution_committed": False,
        "authorization_granted_now": False,
        "owner_approval_granted_now": False,
        "operator_acknowledgement_granted_now": False,
        "execution_window_opened_now": False,
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


def _load_post_review_root(path_str: Optional[str]) -> Dict[str, Any]:
    root = Path(path_str).expanduser().resolve() if path_str else None
    artifacts: Dict[str, Any] = {}
    missing: List[str] = []
    if root:
        for name in POST_REVIEW_REQUIRED_ARTIFACTS:
            payload = _try_read_json(root / name)
            if payload is None:
                missing.append(name)
            else:
                artifacts[name] = payload
    loaded = bool(root) and not missing and bool(artifacts.get("summary.json")) and bool(artifacts.get("verifier_report.json"))
    return {"root": root, "loaded": loaded, "artifacts": artifacts, "missing": missing}


def run_main_project_structure_migration_stabilized_batch_authorization_planning_v1(
    *,
    stabilized_execution_post_dryrun_review_root: str,
) -> Dict[str, Any]:
    post = _load_post_review_root(stabilized_execution_post_dryrun_review_root)
    blockers: List[str] = []
    if not post["loaded"]:
        blockers.append(f"post-dryrun review input incomplete: {post['missing']}")

    sm = (post["artifacts"].get("summary.json") or {}) if post["artifacts"] else {}
    vr = (post["artifacts"].get("verifier_report.json") or {}) if post["artifacts"] else {}

    if vr.get("verifier") != "GO" or vr.get("passed") is not True:
        blockers.append("post-dryrun review verifier must be GO")
    if sm.get("boundary_ok") is not True:
        blockers.append("post-dryrun review boundary_ok must be true")
    if sm.get("final_decision") != POST_REVIEW_REQUIRED_FINAL:
        blockers.append("post-dryrun review final_decision mismatch")
    if sm.get("recommended_next_phase") != POST_REVIEW_REQUIRED_NEXT:
        blockers.append("post-dryrun review recommended_next_phase must point to this phase")
    if sm.get("review_only") is not True or sm.get("post_dryrun_review_only") is not True:
        blockers.append("post-dryrun review must be review_only=true and post_dryrun_review_only=true")

    # must be non-execution; propagate any boundary violations as blockers
    for f in (
        "actual_file_move_executed",
        "actual_file_delete_executed",
        "actual_file_rename_executed",
        "actual_file_merge_executed",
        "actual_file_copy_executed",
        "actual_file_overwrite_executed",
        "actual_archive_executed",
        "batch_armed_now",
        "verifier_rerun_executed_now",
        "eval_out_modified_now",
        "protected_asset_modified_now",
        "hr_modified_now",
        "dnae_modified_now",
    ):
        if sm.get(f) is not False:
            blockers.append(f"post-dryrun review boundary field must be false: {f}")

    input_review_rows = [
        _row(check_id="post_review.phase", expected=POST_REVIEW_REQUIRED_PHASE, observed=sm.get("phase"), review_pass=sm.get("phase") == POST_REVIEW_REQUIRED_PHASE),
        _row(check_id="post_review.verifier_go", expected="GO", observed=vr.get("verifier"), review_pass=vr.get("verifier") == "GO"),
        _row(check_id="post_review.final_decision", expected=POST_REVIEW_REQUIRED_FINAL, observed=sm.get("final_decision"), review_pass=sm.get("final_decision") == POST_REVIEW_REQUIRED_FINAL),
        _row(check_id="post_review.next_phase", expected=POST_REVIEW_REQUIRED_NEXT, observed=sm.get("recommended_next_phase"), review_pass=sm.get("recommended_next_phase") == POST_REVIEW_REQUIRED_NEXT),
    ]
    execution_post_dryrun_review_input_review = {
        "upstream_root": str(post["root"]) if post["root"] else None,
        "loaded": post["loaded"],
        "missing": post["missing"],
        "rows": input_review_rows,
        "row_count": len(input_review_rows),
        "all_pass": all(r.get("review_pass") for r in input_review_rows) and not blockers,
        "blockers": blockers,
        **_boundary_meta(),
    }

    # Authorization scope matrix per batch (frozen; no request/grant now)
    scope_rows: List[Dict[str, Any]] = []
    for idx, (bid, bname, scope_key, domain, touched_candidates, _) in enumerate(STABILIZED_BATCH_DEFS):
        scope_rows.append(
            _row(
                batch_id=bid,
                batch_name=bname,
                batch_domain=domain,
                authorized_scope_candidate=touched_candidates,
                excluded_scope=["_eval_out/", "protected_assets/", "human_review_queue/", "dnae_permanent_block/"],
                required_pre_gates=[g[0] for g in GATE_DEFS],
                required_before_manifest=True,
                required_after_manifest=True,
                required_rollback_route=True,
                required_verifier_rerun_list=True,
                required_abort_conditions=True,
                protected_path_intersection=False,
                eval_out_write_allowed=False,
                authorization_request_sent_now=False,
                authorization_granted_now=False,
                batch_armed_now=False,
                file_operation_executed_now=False,
                order_index=idx,
            )
        )

    b0_b7_batch_authorization_scope_matrix = {
        "rows": scope_rows,
        "row_count": len(scope_rows),
        "batch_count": len(scope_rows),
        "all_pass": len(scope_rows) == 8 and all(r.get("protected_path_intersection") is False for r in scope_rows),
        **_boundary_meta(),
    }

    # Request schema planning (planning only)
    batch_authorization_request_schema_planning = {
        "schema_version": "v1",
        "required_fields": [
            "request_id",
            "phase_id",
            "batch_id",
            "requester_id",
            "requested_scope_candidate",
            "excluded_scope",
            "required_pre_gates",
            "required_manifests",
            "required_rollback_route",
            "required_verifier_rerun_list",
            "required_abort_conditions",
            "acknowledge_non_execution_chain",
        ],
        "request_sent_now": False,
        "grant_expected_fields": ["grant_id", "batch_id", "granted", "conditions", "expiry", "approver_ids"],
        **_boundary_meta(),
    }

    # Grant schema planning (planning only)
    batch_authorization_grant_schema_planning = {
        "schema_version": "v1",
        "required_fields": [
            "grant_id",
            "phase_id",
            "batch_id",
            "granted",
            "conditions",
            "approver_ids",
            "operator_acknowledgement_required",
            "execution_window_required",
            "rollback_window_reserved_required",
            "verifier_rerun_allowed_only_after_execution",
        ],
        "grant_issued_now": False,
        **_boundary_meta(),
    }

    # Pre-authorization gate matrix (per batch)
    gate_rows: List[Dict[str, Any]] = []
    for bid, _, _, domain, _, _ in STABILIZED_BATCH_DEFS:
        for gid, gname, gscope in GATE_DEFS:
            gate_rows.append(
                _row(
                    batch_id=bid,
                    batch_domain=domain,
                    gate_id=gid,
                    gate_name=gname,
                    gate_scope=gscope,
                    must_pass_before_authorization_grant=True,
                    satisfied_now=False,
                )
            )
    batch_pre_authorization_gate_matrix = {
        "rows": gate_rows,
        "row_count": len(gate_rows),
        "all_pass": len(gate_rows) == 8 * len(GATE_DEFS),
        **_boundary_meta(),
    }

    # Execution window planning (planning only; window not opened)
    batch_execution_window_planning = {
        "rows": [
            _row(
                batch_id=bid,
                execution_window_opened_now=False,
                required_window_conditions=[
                    "dedicated_branch_required",
                    "clean_working_tree_required",
                    "one_batch_at_a_time",
                    "rollback_window_reserved",
                    "post_batch_verification_window_reserved",
                ],
                operator_acknowledgement_required=True,
            )
            for bid, _, _, _, _, _ in STABILIZED_BATCH_DEFS
        ],
        "row_count": 8,
        "execution_window_opened_now": False,
        **_boundary_meta(),
    }

    # Verifier rerun authorization planning (planned, never executed now)
    batch_verifier_rerun_authorization_planning = {
        "rows": [
            _row(
                batch_id=bid,
                verifier_rerun_allowed_only_after_batch_execution=True,
                verifier_rerun_executed_now=False,
                requires_separate_operator_ack=True,
            )
            for bid, _, _, _, _, _ in STABILIZED_BATCH_DEFS
        ],
        "row_count": 8,
        "all_pass": True,
        **_boundary_meta(),
    }

    # Rollback authorization planning (planned, never executed now)
    batch_rollback_authorization_planning = {
        "rows": [
            _row(
                batch_id=bid,
                rollback_route_required=True,
                rollback_rehearsal_execution_allowed=False,
                rollback_rehearsal_executed_now=False,
            )
            for bid, _, _, _, _, _ in STABILIZED_BATCH_DEFS
        ],
        "row_count": 8,
        "all_pass": True,
        **_boundary_meta(),
    }

    # File operation permission boundary
    batch_file_operation_permission_boundary = {
        "rows": [
            _row(
                batch_id=bid,
                file_move_allowed_now=False,
                file_delete_allowed_now=False,
                file_rename_allowed_now=False,
                file_merge_allowed_now=False,
                file_copy_allowed_now=False,
                file_overwrite_allowed_now=False,
                archive_allowed_now=False,
            )
            for bid, _, _, _, _, _ in STABILIZED_BATCH_DEFS
        ],
        "row_count": 8,
        "all_pass": True,
        **_boundary_meta(),
    }

    # Protected + eval_out guards as authorization conditions (must remain false intersection / no write)
    batch_protected_eval_out_guard_authorization_matrix = {
        "rows": [
            _row(
                batch_id=bid,
                protected_path_intersection_must_be_false=True,
                eval_out_write_must_be_false=True,
                protected_assets_frozen=True,
                hr_frozen=True,
                dnae_frozen=True,
                eval_out_readonly=True,
            )
            for bid, _, _, _, _, _ in STABILIZED_BATCH_DEFS
        ],
        "row_count": 8,
        "all_pass": True,
        **_boundary_meta(),
    }

    non_claims = [
        "授权规划不等于授权请求",
        "授权请求不等于授权授予",
        "授权授予不等于 batch armed",
        "batch armed 不等于执行完成",
        "verifier rerun list 可规划，但不得实际 rerun",
        "rollback route 可规划，但不得实际 rehearsal",
        "_eval_out 永久只读",
        "protected / HR / DnAE 永久冻结",
        "不允许跨域 batch",
        "不允许批量删除 / 隐式合并",
        "不允许通过迁移修改 runtime 行为",
        "不允许借工程整理继续 GC / Registry 支线",
    ]
    batch_authorization_non_claims_register = {
        "rows": [_row(non_claim_id=f"NC{i:02d}", text=t) for i, t in enumerate(non_claims, 1)],
        "row_count": len(non_claims),
        **_boundary_meta(),
    }

    stabilized_batch_authorization_planning_policy = _row(
        phase_id=PHASE_ID,
        planning_scope=PLANNING_SCOPE,
        batch_count=8,
        gate_count=len(GATE_DEFS),
        request_sent_now=False,
        grant_issued_now=False,
        **{},
    )

    boundary_ok = (
        execution_post_dryrun_review_input_review["all_pass"]
        and b0_b7_batch_authorization_scope_matrix["all_pass"]
        and batch_pre_authorization_gate_matrix["all_pass"]
        and not blockers
    )

    stabilized_batch_authorization_planning_readiness_decision = {
        "final_decision": FINAL_DECISION if boundary_ok else "MAIN_PROJECT_STRUCTURE_MIGRATION_STABILIZED_BATCH_AUTHORIZATION_PLANNING_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "ready_for_batch_authorization_dryrun": boundary_ok,
        "batch_authorization_planning_completed": boundary_ok,
        **_boundary_meta(),
    }

    summary = {
        "phase": PHASE_ID,
        "planning_scope": PLANNING_SCOPE,
        "post_dryrun_review_input_loaded": post["loaded"],
        "batch_count": 8,
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "final_decision": FINAL_DECISION if boundary_ok else "MAIN_PROJECT_STRUCTURE_MIGRATION_STABILIZED_BATCH_AUTHORIZATION_PLANNING_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        **_boundary_meta(),
    }

    return {
        "summary": summary,
        "stabilized_batch_authorization_planning_policy": stabilized_batch_authorization_planning_policy,
        "execution_post_dryrun_review_input_review": execution_post_dryrun_review_input_review,
        "b0_b7_batch_authorization_scope_matrix": b0_b7_batch_authorization_scope_matrix,
        "batch_authorization_request_schema_planning": batch_authorization_request_schema_planning,
        "batch_authorization_grant_schema_planning": batch_authorization_grant_schema_planning,
        "batch_pre_authorization_gate_matrix": batch_pre_authorization_gate_matrix,
        "batch_execution_window_planning": batch_execution_window_planning,
        "batch_verifier_rerun_authorization_planning": batch_verifier_rerun_authorization_planning,
        "batch_rollback_authorization_planning": batch_rollback_authorization_planning,
        "batch_file_operation_permission_boundary": batch_file_operation_permission_boundary,
        "batch_protected_eval_out_guard_authorization_matrix": batch_protected_eval_out_guard_authorization_matrix,
        "batch_authorization_non_claims_register": batch_authorization_non_claims_register,
        "stabilized_batch_authorization_planning_readiness_decision": stabilized_batch_authorization_planning_readiness_decision,
    }

