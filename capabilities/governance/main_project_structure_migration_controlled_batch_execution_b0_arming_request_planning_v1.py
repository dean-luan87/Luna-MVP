# -*- coding: utf-8 -*-
"""Main Project Structure Migration Controlled Batch Execution B0 Arming Request Planning v1.

Scope: plan the minimal arming request structure for B0 only.
Planning-only: no request artifact generated, no request sent, no authorization granted,
no arming, no execution window open, no file operations, no verifier rerun execution,
no rollback rehearsal, no post-migration tests.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.main_project_structure_migration_guarded_planning_v1 import GATE_DEFS
from capabilities.governance.main_project_structure_migration_stabilized_execution_planning_v1 import (
    COMMON_ABORT_CONDITIONS,
    TEST_CHECKLIST_BY_BATCH,
    VERIFIER_RERUN_BY_BATCH,
)
from capabilities.governance.main_project_structure_migration_controlled_batch_execution_arming_planning_v1 import (
    SELECTED_BATCH_ID,
)
from capabilities.governance.main_project_structure_migration_controlled_batch_execution_arming_post_dryrun_review_v1 import (
    FINAL_DECISION as UPSTREAM_FINAL,
    PHASE_ID as UPSTREAM_PHASE,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID

PHASE_ID = "Phase-Main-Project-Structure-Migration-Controlled-Batch-Execution-B0-Arming-Request-Planning-v1-001"
PLANNING_SCOPE = "main_project_structure_migration_controlled_batch_execution_b0_arming_request_planning_only"
SOURCE_CHAIN = "main_project_structure_migration_controlled_batch_execution_b0_arming_request_planning_v1"

FINAL_DECISION = "MAIN_PROJECT_STRUCTURE_MIGRATION_CONTROLLED_BATCH_EXECUTION_B0_ARMING_REQUEST_PLANNING_READY_FOR_DRYRUN"
NEXT_PHASE = "Phase-Main-Project-Structure-Migration-Controlled-Batch-Execution-B0-Arming-Request-DryRun-v1-001"

UPSTREAM_REQUIRED_PHASE = UPSTREAM_PHASE
UPSTREAM_REQUIRED_FINAL = UPSTREAM_FINAL
UPSTREAM_REQUIRED_NEXT = PHASE_ID

UPSTREAM_REQUIRED_ARTIFACTS: Tuple[str, ...] = (
    "summary.json",
    "verifier_report.json",
    "controlled_batch_execution_arming_post_dryrun_review_policy_v1.json",
    "controlled_batch_execution_arming_dryrun_input_review_v1.json",
    "b0_single_batch_arming_scope_review_v1.json",
    "b1_b7_deferred_arming_review_v1.json",
    "b0_execution_window_non_open_review_v1.json",
    "b0_file_operation_non_execution_review_v1.json",
    "b0_manifest_non_execution_review_v1.json",
    "b0_rollback_non_execution_review_v1.json",
    "b0_verifier_rerun_non_execution_review_v1.json",
    "b0_post_migration_test_non_execution_review_v1.json",
    "b0_abort_condition_review_v1.json",
    "b0_protected_eval_out_guard_review_v1.json",
    "controlled_batch_execution_arming_non_claims_review_v1.json",
    "controlled_batch_execution_arming_post_dryrun_review_readiness_decision_v1.json",
)


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _boundary_meta() -> Dict[str, Any]:
    return {
        "b0_arming_request_planning_only": True,
        "selected_batch_id": "B0",
        "b0_only": True,
        "b1_b7_arming_deferred": True,
        "b0_arming_request_artifact_generated_now": False,
        "b0_arming_request_sent_now": False,
        "b0_arming_authorized_now": False,
        "b0_armed_now": False,
        "batch_armed_now": False,
        "b0_execution_started_now": False,
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
        "post_migration_tests_executed_now": False,
        "eval_out_modified_now": False,
        "protected_asset_modified_now": False,
        "hr_modified_now": False,
        "dnae_modified_now": False,
        "file_operation_executed_now": False,
        "real_migration_execution_allowed": False,
        "real_rehearsal_execution_allowed": False,
        "rollback_rehearsal_execution_allowed": False,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_path_mode": "repo_eval_out",
        "standard_eval_out_write_pending_on_local_repro": False,
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


def run_main_project_structure_migration_controlled_batch_execution_b0_arming_request_planning_v1(
    *,
    controlled_batch_execution_arming_post_dryrun_review_root: str,
) -> Dict[str, Any]:
    up = _load_upstream_root(controlled_batch_execution_arming_post_dryrun_review_root)
    blockers: List[str] = []
    if not up["loaded"]:
        blockers.append(f"upstream input incomplete: {up['missing']}")

    sm = (up["artifacts"].get("summary.json") or {}) if up["artifacts"] else {}
    vr = (up["artifacts"].get("verifier_report.json") or {}) if up["artifacts"] else {}

    source_path_mode = "workspace_fallback" if _is_workspace_fallback(up["root"]) else "repo_eval_out"
    standard_pending = source_path_mode == "workspace_fallback"
    meta = {**_boundary_meta(), "source_path_mode": source_path_mode, "standard_eval_out_write_pending_on_local_repro": standard_pending}

    if vr.get("verifier") != "GO" or vr.get("passed") is not True:
        blockers.append("upstream verifier must be GO")
    if sm.get("phase") != UPSTREAM_REQUIRED_PHASE:
        blockers.append("upstream phase mismatch")
    if sm.get("final_decision") != UPSTREAM_REQUIRED_FINAL:
        blockers.append("upstream final_decision mismatch")
    if sm.get("recommended_next_phase") != UPSTREAM_REQUIRED_NEXT:
        blockers.append("upstream recommended_next_phase must be this phase")
    if sm.get("selected_batch_id") != "B0" or sm.get("b0_only") is not True or sm.get("b1_b7_arming_deferred") is not True:
        blockers.append("upstream must be b0-only with b1-b7 deferred")
    if sm.get("boundary_ok") is not True:
        blockers.append("upstream boundary_ok must be true")

    for f in (
        "batch_armed_now",
        "b0_armed_now",
        "batch_execution_started_now",
        "b0_execution_started_now",
        "execution_window_opened_now",
        "verifier_rerun_executed_now",
        "rollback_rehearsal_executed_now",
        "post_migration_tests_executed_now",
        "eval_out_modified_now",
        "protected_asset_modified_now",
        "hr_modified_now",
        "dnae_modified_now",
        "file_operation_executed_now",
    ):
        if sm.get(f) is not False:
            blockers.append(f"upstream boundary must be false: {f}")

    # Minimal identity plan
    identity = _row(
        batch_id="B0",
        requester_role_candidate="operator",
        approver_role_candidate="owner",
        request_type="controlled_batch_execution_b0_arming_request_planning",
        request_sent_now=False,
        request_artifact_generated_now=False,
    )

    # Scope plan (B0 only)
    scope_candidate = [
        "docs/architecture/README.md",
        "docs/architecture/evaluation/README.md",
        "docs/architecture/evaluation/LUNA_EVALUATION_OCR_PHASE_VERDICT_STATUS_TABLE_V0.md",
    ]
    bad_tokens = ("capabilities/", "tools/", "_eval_out", "protected", "hr", "dnae", "configs", "scripts", "tests")
    scope_ok = all(isinstance(p, str) and not any(t in p.lower() for t in bad_tokens) for p in scope_candidate)
    if not scope_ok:
        blockers.append("B0 request scope contains forbidden tokens")

    scope = _row(
        batch_id="B0",
        batch_domain="Documentation Index / README / phase table alignment",
        requested_scope_candidate=scope_candidate,
        b1_b7_included=False,
        scope_ok=scope_ok,
        request_does_not_include_execution=True,
    )

    # Preconditions: gate list required, but no window open
    pre_gates = _row(
        batch_id="B0",
        required_precondition_gates=[gid for gid, _name, _topic in GATE_DEFS],
        execution_window_opened_now=False,
        preconditions_defined=True,
    )

    forbidden_scope = _row(
        batch_id="B0",
        forbidden_paths_and_domains=[
            "_eval_out/**",
            "capabilities/**",
            "tools/**",
            "protected/**",
            "HR/**",
            "DnAE/**",
            "configs/**",
            "scripts/**",
            "tests/**",
        ],
        forbidden_operations=["delete", "archive", "cross_domain", "touch_eval_out", "touch_protected", "touch_hr", "touch_dnae"],
    )

    manifest_req = _row(batch_id="B0", before_manifest_required=True, after_manifest_required=True, manifest_execution_now=False)
    rollback_req = _row(batch_id="B0", rollback_required=True, rollback_rehearsal_executed_now=False)
    rerun_req = _row(batch_id="B0", verifier_rerun_required=True, verifier_rerun_list=VERIFIER_RERUN_BY_BATCH.get("B0", []), verifier_rerun_executed_now=False)
    tests_req = _row(batch_id="B0", post_migration_tests_required=True, post_migration_test_list=TEST_CHECKLIST_BY_BATCH.get("B0", []), post_migration_tests_executed_now=False)

    abort_revoke = _row(
        batch_id="B0",
        abort_conditions=list(COMMON_ABORT_CONDITIONS),
        revoke_conditions=[
            "scope_violation_detected",
            "protected_eval_out_intersection_detected",
            "unexpected_file_op_detected",
            "window_opened_without_authorization",
        ],
        request_sent_now=False,
        authorized_now=False,
    )

    non_claim_texts = [
        "Request Planning GO ≠ request artifact generated",
        "request artifact generated in future ≠ request sent",
        "request sent in future ≠ arming authorized",
        "arming authorized in future ≠ B0 armed",
        "B0 armed in future ≠ B0 executed",
        "B0 execution in future ≠ B1–B7 allowed",
        "workspace_fallback GO ≠ standard _eval_out already written",
    ]
    non_claims = {"rows": [_row(non_claim_id=f"NC_B0_REQ_{i+1:02d}", text=t) for i, t in enumerate(non_claim_texts)], "row_count": len(non_claim_texts), "all_pass": True, **meta}

    boundary_ok = not blockers

    policy = _row(
        phase_id=PHASE_ID,
        planning_scope=PLANNING_SCOPE,
        request_artifact_generated_now=False,
        request_sent_now=False,
        authorized_now=False,
        source_path_mode=source_path_mode,
        standard_eval_out_write_pending_on_local_repro=standard_pending,
    )

    input_review = {
        "upstream_root": str(up["root"]) if up["root"] else None,
        "upstream_loaded": up["loaded"],
        "missing": up["missing"],
        "source_path_mode": source_path_mode,
        "standard_eval_out_write_pending_on_local_repro": standard_pending,
        "upstream_summary": {"phase": sm.get("phase"), "final_decision": sm.get("final_decision"), "recommended_next_phase": sm.get("recommended_next_phase")},
        "upstream_verifier": {"verifier": vr.get("verifier"), "passed": vr.get("passed"), "check_count": vr.get("check_count")},
        "blockers": blockers,
        "all_pass": boundary_ok,
        **meta,
    }

    readiness = {
        "final_decision": FINAL_DECISION if boundary_ok else "MAIN_PROJECT_STRUCTURE_MIGRATION_CONTROLLED_BATCH_EXECUTION_B0_ARMING_REQUEST_PLANNING_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "ready_for_dryrun": boundary_ok,
        "selected_batch_id": "B0",
        **meta,
    }

    summary = {
        "phase": PHASE_ID,
        "planning_scope": PLANNING_SCOPE,
        "b0_arming_request_planning_only": True,
        "selected_batch_id": "B0",
        "b0_only": True,
        "b1_b7_arming_deferred": True,
        "source_path_mode": source_path_mode,
        "standard_eval_out_write_pending_on_local_repro": standard_pending,
        "upstream_input_loaded": up["loaded"],
        "upstream_verifier_go": vr.get("verifier") == "GO" and vr.get("passed") is True,
        "upstream_final_decision_ok": sm.get("final_decision") == UPSTREAM_REQUIRED_FINAL,
        "upstream_next_phase_ok": sm.get("recommended_next_phase") == UPSTREAM_REQUIRED_NEXT,
        "b0_scope_ok": scope_ok,
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "final_decision": FINAL_DECISION if boundary_ok else "MAIN_PROJECT_STRUCTURE_MIGRATION_CONTROLLED_BATCH_EXECUTION_B0_ARMING_REQUEST_PLANNING_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        **meta,
    }

    return {
        "summary": summary,
        "b0_arming_request_planning_policy": policy,
        "b0_arming_post_dryrun_review_input_review": input_review,
        "b0_arming_request_identity_planning": {**identity, **meta},
        "b0_arming_request_scope_planning": {**scope, **meta},
        "b0_arming_request_precondition_gate_planning": {**pre_gates, **meta},
        "b0_arming_request_forbidden_scope_planning": {**forbidden_scope, **meta},
        "b0_arming_request_manifest_requirement_planning": {**manifest_req, **meta},
        "b0_arming_request_rollback_requirement_planning": {**rollback_req, **meta},
        "b0_arming_request_verifier_rerun_requirement_planning": {**rerun_req, **meta},
        "b0_arming_request_post_migration_test_requirement_planning": {**tests_req, **meta},
        "b0_arming_request_abort_revoke_planning": {**abort_revoke, **meta},
        "b0_arming_request_non_claims_register": non_claims,
        "b0_arming_request_planning_readiness_decision": readiness,
    }

