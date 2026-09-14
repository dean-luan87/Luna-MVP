# -*- coding: utf-8 -*-
"""Main Project Structure Migration Controlled Batch Execution Arming Planning v1.

Narrowed scope: plan arming for B0 only (lowest-risk docs index/readme/phase table alignment).
Planning-only: no arming, no execution, no file operations, no verifier rerun execution,
no rollback rehearsal execution, no post-migration tests executed.
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
from capabilities.governance.main_project_structure_migration_controlled_batch_execution_authorization_planning_v1 import (
    STABILIZED_BATCH_DEFS,
)
from capabilities.governance.main_project_structure_migration_controlled_batch_execution_authorization_post_dryrun_review_v1 import (
    FINAL_DECISION as UPSTREAM_FINAL,
    PHASE_ID as UPSTREAM_PHASE,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID

PHASE_ID = "Phase-Main-Project-Structure-Migration-Controlled-Batch-Execution-Arming-Planning-v1-001"
PLANNING_SCOPE = "main_project_structure_migration_controlled_batch_execution_arming_planning_only"
SOURCE_CHAIN = "main_project_structure_migration_controlled_batch_execution_arming_planning_v1"

FINAL_DECISION = "MAIN_PROJECT_STRUCTURE_MIGRATION_CONTROLLED_BATCH_EXECUTION_ARMING_PLANNING_READY_FOR_DRYRUN"
NEXT_PHASE = "Phase-Main-Project-Structure-Migration-Controlled-Batch-Execution-Arming-DryRun-v1-001"

UPSTREAM_REQUIRED_PHASE = UPSTREAM_PHASE
UPSTREAM_REQUIRED_FINAL = UPSTREAM_FINAL
UPSTREAM_REQUIRED_NEXT = PHASE_ID

UPSTREAM_REQUIRED_ARTIFACTS: Tuple[str, ...] = (
    "summary.json",
    "verifier_report.json",
    "controlled_batch_execution_authorization_post_dryrun_review_policy_v1.json",
    "controlled_batch_execution_authorization_dryrun_input_review_v1.json",
    "b0_b7_controlled_execution_scope_review_v1.json",
    "controlled_execution_request_non_sent_review_v1.json",
    "controlled_execution_grant_non_issued_review_v1.json",
    "controlled_execution_arming_non_execution_review_v1.json",
    "controlled_execution_window_non_open_review_v1.json",
    "controlled_execution_file_operation_non_execution_review_v1.json",
    "controlled_execution_verifier_rerun_non_execution_review_v1.json",
    "controlled_execution_rollback_non_execution_review_v1.json",
    "controlled_execution_post_migration_test_non_execution_review_v1.json",
    "controlled_execution_protected_eval_out_guard_review_v1.json",
    "controlled_execution_non_claims_review_v1.json",
    "controlled_batch_execution_authorization_post_dryrun_review_readiness_decision_v1.json",
)

SELECTED_BATCH_ID = "B0"
DEFERRED_BATCH_IDS: Tuple[str, ...] = ("B1", "B2", "B3", "B4", "B5", "B6", "B7")


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _boundary_meta() -> Dict[str, Any]:
    return {
        "controlled_batch_execution_arming_planning_only": True,
        "selected_batch_id": SELECTED_BATCH_ID,
        "b0_only": True,
        "b1_b7_arming_deferred": True,
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


def _b0_batch_def() -> Dict[str, Any]:
    # Derive from the stabilized batch defs
    # Shape: (batch_id, batch_name, batch_key, batch_domain, touched_paths_candidate, notes)
    for bid, name, _key, domain, _paths, _notes in STABILIZED_BATCH_DEFS:
        if bid == SELECTED_BATCH_ID:
            return {"batch_id": bid, "batch_name": name, "batch_domain": domain}
    return {"batch_id": SELECTED_BATCH_ID, "batch_name": "B0", "batch_domain": "docs_index_only"}


def run_main_project_structure_migration_controlled_batch_execution_arming_planning_v1(
    *,
    controlled_batch_execution_authorization_post_dryrun_review_root: str,
) -> Dict[str, Any]:
    up = _load_upstream_root(controlled_batch_execution_authorization_post_dryrun_review_root)
    blockers: List[str] = []
    if not up["loaded"]:
        blockers.append(f"upstream input incomplete: {up['missing']}")

    sm = (up["artifacts"].get("summary.json") or {}) if up["artifacts"] else {}
    vr = (up["artifacts"].get("verifier_report.json") or {}) if up["artifacts"] else {}

    source_path_mode = "workspace_fallback" if _is_workspace_fallback(up["root"]) else "repo_eval_out"
    standard_pending = source_path_mode == "workspace_fallback"

    if vr.get("verifier") != "GO" or vr.get("passed") is not True:
        blockers.append("upstream verifier must be GO")
    if sm.get("phase") != UPSTREAM_REQUIRED_PHASE:
        blockers.append("upstream phase mismatch")
    if sm.get("final_decision") != UPSTREAM_REQUIRED_FINAL:
        blockers.append("upstream final_decision mismatch")
    if sm.get("recommended_next_phase") != UPSTREAM_REQUIRED_NEXT:
        blockers.append("upstream recommended_next_phase must be this arming planning phase")
    if sm.get("review_only") is not True or sm.get("controlled_batch_execution_authorization_post_dryrun_review_only") is not True:
        blockers.append("upstream must be review_only post-dryrun review")
    if sm.get("boundary_ok") is not True:
        blockers.append("upstream boundary_ok must be true")

    for f in (
        "controlled_batch_execution_authorized_now",
        "controlled_batch_execution_authorization_request_sent_now",
        "batch_armed_now",
        "batch_execution_started_now",
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

    b0 = _b0_batch_def()

    # B0 arming scope: only docs index / README / phase table alignment candidates
    b0_scope_candidate = [
        "docs/architecture/README.md",
        "docs/architecture/evaluation/README.md",
        "docs/architecture/evaluation/LUNA_EVALUATION_OCR_PHASE_VERDICT_STATUS_TABLE_V0.md",
    ]
    forbidden_terms = ("capabilities/", "tools/", "protected", "HR", "DnAE", "_eval_out", "configs", "scripts", "tests")
    scope_ok = all(isinstance(p, str) for p in b0_scope_candidate) and all(
        not any(t.lower() in p.lower() for t in forbidden_terms) for p in b0_scope_candidate
    )
    if not scope_ok:
        blockers.append("b0 scope candidate contains forbidden paths")

    # Derived plans for B0 from earlier planning conventions
    b0_window = {
        "batch_id": "B0",
        "execution_window_planned": True,
        "execution_window_opened_now": False,
        "window_policy": "owner/operator gated; arming dryrun next; no open now",
        **_boundary_meta(),
    }
    b0_allow = {
        "batch_id": "B0",
        "allowed_file_operations_candidate": ["move", "rename", "copy", "merge", "overwrite"],
        "all_actual_file_ops_executed_now": False,
        **_boundary_meta(),
    }
    b0_block = {
        "batch_id": "B0",
        "blocked_file_operations": [
            "delete",
            "archive",
            "cross_domain",
            "touch_eval_out",
            "touch_protected",
            "touch_hr",
            "touch_dnae",
        ],
        **_boundary_meta(),
    }
    b0_manifest = {
        "batch_id": "B0",
        "required_before_manifest": True,
        "required_after_manifest": True,
        "manifest_candidate_only": True,
        **_boundary_meta(),
    }
    b0_rollback = {
        "batch_id": "B0",
        "rollback_route_planned": True,
        "rollback_rehearsal_executed_now": False,
        "rollback_principle": "revert docs index changes; no mass delete; no eval_out touch",
        **_boundary_meta(),
    }
    b0_rerun = {
        "batch_id": "B0",
        "verifier_rerun_list": VERIFIER_RERUN_BY_BATCH.get("B0", []),
        "verifier_rerun_executed_now": False,
        **_boundary_meta(),
    }
    b0_tests = {
        "batch_id": "B0",
        "post_migration_test_list": TEST_CHECKLIST_BY_BATCH.get("B0", []),
        "post_migration_tests_executed_now": False,
        **_boundary_meta(),
    }
    b0_abort = {
        "batch_id": "B0",
        "abort_conditions": list(COMMON_ABORT_CONDITIONS),
        "abort_triggered_now": False,
        **_boundary_meta(),
    }
    b0_guard = {
        "batch_id": "B0",
        "protected_path_intersection": False,
        "eval_out_write_allowed": False,
        "hr_modified_now": False,
        "dnae_modified_now": False,
        "protected_asset_modified_now": False,
        "eval_out_modified_now": False,
        **_boundary_meta(),
    }

    # B1-B7 deferred matrix
    deferred_rows = [
        _row(
            batch_id=bid,
            deferred=True,
            arming_allowed_now=False,
            batch_armed_now=False,
            batch_execution_started_now=False,
        )
        for bid in DEFERRED_BATCH_IDS
    ]

    # Non-claims register for arming planning
    non_claims = [
        "Arming Planning GO ≠ B0 armed",
        "B0 selected ≠ B0 executed",
        "B0 arming plan ≠ file operation executed",
        "B1–B7 deferred ≠ B1–B7 ready",
        "verifier rerun plan ≠ verifier rerun executed",
        "rollback route plan ≠ rollback rehearsal executed",
        "post-migration test plan ≠ tests executed",
        "workspace_fallback GO ≠ standard _eval_out already written",
    ]
    non_claim_rows = [_row(non_claim_id=f"NC_ARM_{i+1:02d}", text=t) for i, t in enumerate(non_claims)]

    boundary_ok = not blockers
    meta = {**_boundary_meta(), "source_path_mode": source_path_mode, "standard_eval_out_write_pending_on_local_repro": standard_pending}

    controlled_batch_execution_arming_planning_policy = _row(
        phase_id=PHASE_ID,
        planning_scope=PLANNING_SCOPE,
        source_path_mode=source_path_mode,
        standard_eval_out_write_pending_on_local_repro=standard_pending,
    )

    controlled_execution_authorization_post_review_input_review = {
        "upstream_root": str(up["root"]) if up["root"] else None,
        "upstream_loaded": up["loaded"],
        "missing": up["missing"],
        "source_path_mode": source_path_mode,
        "standard_eval_out_write_pending_on_local_repro": standard_pending,
        "upstream_summary": {
            "phase": sm.get("phase"),
            "boundary_ok": sm.get("boundary_ok"),
            "final_decision": sm.get("final_decision"),
            "recommended_next_phase": sm.get("recommended_next_phase"),
        },
        "upstream_verifier": {"verifier": vr.get("verifier"), "passed": vr.get("passed"), "check_count": vr.get("check_count")},
        "blockers": blockers,
        "all_pass": boundary_ok,
        **meta,
    }

    b0_single_batch_arming_scope = {
        "batch_id": "B0",
        "batch_domain": b0.get("batch_name"),
        "controlled_execution_scope_candidate": b0_scope_candidate,
        "forbidden_domains": ["capabilities", "runner", "verifier", "configs", "scripts", "tests", "protected", "hr", "dnae", "eval_out"],
        "b0_arming_allowed_later": True,
        "b0_armed_now": False,
        "b0_execution_started_now": False,
        "b0_file_operation_executed_now": False,
        "scope_ok": scope_ok,
        **meta,
    }

    b1_b7_deferred_arming_matrix = {"rows": deferred_rows, "row_count": len(deferred_rows), "all_pass": True, **meta}

    b0_execution_window_arming_plan = {**b0_window, **meta}
    b0_file_operation_allowlist_arming_plan = {**b0_allow, **meta}
    b0_file_operation_blocklist_arming_plan = {**b0_block, **meta}
    b0_before_after_manifest_arming_plan = {**b0_manifest, **meta}
    b0_rollback_route_arming_plan = {**b0_rollback, **meta}
    b0_verifier_rerun_arming_plan = {**b0_rerun, **meta}
    b0_post_migration_test_arming_plan = {**b0_tests, **meta}
    b0_abort_condition_arming_plan = {**b0_abort, **meta}
    b0_protected_eval_out_guard_arming_plan = {**b0_guard, **meta}
    controlled_batch_execution_arming_non_claims_register = {"rows": non_claim_rows, "row_count": len(non_claim_rows), "all_pass": True, **meta}

    controlled_batch_execution_arming_planning_readiness_decision = {
        "final_decision": FINAL_DECISION if boundary_ok else "MAIN_PROJECT_STRUCTURE_MIGRATION_CONTROLLED_BATCH_EXECUTION_ARMING_PLANNING_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "selected_batch_id": SELECTED_BATCH_ID,
        "ready_for_arming_dryrun": boundary_ok,
        **meta,
    }

    summary = {
        "phase": PHASE_ID,
        "planning_scope": PLANNING_SCOPE,
        "controlled_batch_execution_arming_planning_only": True,
        "selected_batch_id": SELECTED_BATCH_ID,
        "b0_only": True,
        "b1_b7_arming_deferred": True,
        "source_path_mode": source_path_mode,
        "standard_eval_out_write_pending_on_local_repro": standard_pending,
        "upstream_input_loaded": up["loaded"],
        "upstream_verifier_go": vr.get("verifier") == "GO" and vr.get("passed") is True,
        "upstream_final_decision_ok": sm.get("final_decision") == UPSTREAM_REQUIRED_FINAL,
        "upstream_next_phase_ok": sm.get("recommended_next_phase") == UPSTREAM_REQUIRED_NEXT,
        "b0_scope_ok": scope_ok,
        "b1_b7_deferred_count": len(DEFERRED_BATCH_IDS),
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "final_decision": FINAL_DECISION if boundary_ok else "MAIN_PROJECT_STRUCTURE_MIGRATION_CONTROLLED_BATCH_EXECUTION_ARMING_PLANNING_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        **meta,
    }

    return {
        "summary": summary,
        "controlled_batch_execution_arming_planning_policy": controlled_batch_execution_arming_planning_policy,
        "controlled_execution_authorization_post_review_input_review": controlled_execution_authorization_post_review_input_review,
        "b0_single_batch_arming_scope": b0_single_batch_arming_scope,
        "b1_b7_deferred_arming_matrix": b1_b7_deferred_arming_matrix,
        "b0_execution_window_arming_plan": b0_execution_window_arming_plan,
        "b0_file_operation_allowlist_arming_plan": b0_file_operation_allowlist_arming_plan,
        "b0_file_operation_blocklist_arming_plan": b0_file_operation_blocklist_arming_plan,
        "b0_before_after_manifest_arming_plan": b0_before_after_manifest_arming_plan,
        "b0_rollback_route_arming_plan": b0_rollback_route_arming_plan,
        "b0_verifier_rerun_arming_plan": b0_verifier_rerun_arming_plan,
        "b0_post_migration_test_arming_plan": b0_post_migration_test_arming_plan,
        "b0_abort_condition_arming_plan": b0_abort_condition_arming_plan,
        "b0_protected_eval_out_guard_arming_plan": b0_protected_eval_out_guard_arming_plan,
        "controlled_batch_execution_arming_non_claims_register": controlled_batch_execution_arming_non_claims_register,
        "controlled_batch_execution_arming_planning_readiness_decision": controlled_batch_execution_arming_planning_readiness_decision,
    }

