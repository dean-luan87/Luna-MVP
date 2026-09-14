# -*- coding: utf-8 -*-
"""Main Project Structure Migration Stabilized Execution Post-DryRun Review v1.

Post-dryrun-review-only: audit dryrun credibility and boundary compliance.
No real file operations, no verifier rerun execution, no rollback rehearsal, no batch arming.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.main_project_structure_migration_stabilized_execution_dryrun_v1 import (
    FINAL_DECISION as DRYRUN_FINAL_DECISION,
    NEXT_PHASE as DRYRUN_NEXT_PHASE,
    PHASE_ID as DRYRUN_PHASE_ID,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID

PHASE_ID = "Phase-Main-Project-Structure-Migration-Stabilized-Execution-Post-DryRun-Review-v1-001"
REVIEW_SCOPE = "main_project_structure_migration_stabilized_execution_post_dryrun_review_only"
SOURCE_CHAIN = "main_project_structure_migration_stabilized_execution_post_dryrun_review_v1"

FINAL_DECISION = (
    "MAIN_PROJECT_STRUCTURE_MIGRATION_STABILIZED_EXECUTION_POST_DRYRUN_REVIEW_READY_FOR_BATCH_AUTHORIZATION_PLANNING"
)
NEXT_PHASE = "Phase-Main-Project-Structure-Migration-Stabilized-Batch-Authorization-Planning-v1-001"

DRYRUN_REQUIRED_PHASE = DRYRUN_PHASE_ID
DRYRUN_REQUIRED_FINAL = DRYRUN_FINAL_DECISION
DRYRUN_REQUIRED_NEXT = PHASE_ID

DRYRUN_REQUIRED_ARTIFACTS: Tuple[str, ...] = (
    "summary.json",
    "verifier_report.json",
    "stabilized_execution_dryrun_policy_v1.json",
    "execution_planning_input_review_v1.json",
    "b0_b7_batch_dryrun_trace_v1.json",
    "batch_pre_gate_dryrun_result_v1.json",
    "batch_before_after_manifest_dryrun_v1.json",
    "batch_rollback_route_dryrun_v1.json",
    "batch_verifier_rerun_dryrun_v1.json",
    "batch_protected_asset_guard_dryrun_v1.json",
    "batch_eval_out_readonly_guard_dryrun_v1.json",
    "batch_domain_isolation_dryrun_v1.json",
    "batch_abort_condition_dryrun_v1.json",
    "stabilized_execution_dryrun_readiness_decision_v1.json",
)

BATCH_IDS: Tuple[str, ...] = ("B0", "B1", "B2", "B3", "B4", "B5", "B6", "B7")


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _review_boundary_meta() -> Dict[str, Any]:
    return {
        "post_dryrun_review_only": True,
        "review_only": True,
        "actual_file_move_executed": False,
        "actual_file_delete_executed": False,
        "actual_file_rename_executed": False,
        "actual_file_merge_executed": False,
        "actual_file_copy_executed": False,
        "actual_file_overwrite_executed": False,
        "actual_archive_executed": False,
        "batch_arming_allowed": False,
        "batch_armed_now": False,
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
        "real_rehearsal_execution_allowed": False,
        "real_migration_execution_allowed": False,
        "batch_arming_allowed": False,
        "success_claim_allowed": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _row(**kwargs: Any) -> Dict[str, Any]:
    return {**kwargs, **_review_boundary_meta(), "planned_now": True, "executed_now": False}


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def _load_dryrun_root(path_str: Optional[str]) -> Dict[str, Any]:
    root = Path(path_str).expanduser().resolve() if path_str else None
    artifacts: Dict[str, Any] = {}
    missing: List[str] = []
    if root:
        for name in DRYRUN_REQUIRED_ARTIFACTS:
            payload = _try_read_json(root / name)
            if payload is None:
                missing.append(name)
            else:
                artifacts[name] = payload
    loaded = bool(root) and not missing and bool(artifacts.get("summary.json")) and bool(artifacts.get("verifier_report.json"))
    return {"root": root, "loaded": loaded, "artifacts": artifacts, "missing": missing}


def run_main_project_structure_migration_stabilized_execution_post_dryrun_review_v1(
    *,
    stabilized_execution_dryrun_root: str,
) -> Dict[str, Any]:
    dry = _load_dryrun_root(stabilized_execution_dryrun_root)
    blockers: List[str] = []
    if not dry["loaded"]:
        blockers.append(f"dryrun input incomplete: {dry['missing']}")

    dsm = (dry["artifacts"].get("summary.json") or {}) if dry["artifacts"] else {}
    dvr = (dry["artifacts"].get("verifier_report.json") or {}) if dry["artifacts"] else {}
    trace = (dry["artifacts"].get("b0_b7_batch_dryrun_trace_v1.json") or {}) if dry["artifacts"] else {}

    if dvr.get("verifier") != "GO" or dvr.get("passed") is not True:
        blockers.append("dryrun verifier must be GO")
    if dsm.get("boundary_ok") is not True:
        blockers.append("dryrun boundary_ok must be true")
    if dsm.get("final_decision") != DRYRUN_REQUIRED_FINAL:
        blockers.append("dryrun final_decision mismatch")
    if dsm.get("recommended_next_phase") != DRYRUN_REQUIRED_NEXT:
        blockers.append("dryrun recommended_next_phase must point to this review phase")
    if dsm.get("execution_dryrun_only") is not True or dsm.get("simulated") is not True:
        blockers.append("dryrun must be execution_dryrun_only=true and simulated=true")

    # boundary re-check (critical)
    boundary_fields_false = (
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
        "file_operation_executed_now",
        "rollback_rehearsal_execution_allowed",
    )
    for f in boundary_fields_false:
        if dsm.get(f) is not False:
            blockers.append(f"dryrun boundary field must be false: {f}")

    # trace completeness
    trace_rows = trace.get("rows") or []
    trace_by_id = {r.get("batch_id"): r for r in trace_rows if isinstance(r.get("batch_id"), str)}
    missing_trace = [bid for bid in BATCH_IDS if bid not in trace_by_id]
    if missing_trace:
        blockers.append(f"missing dryrun trace rows: {missing_trace}")

    completeness_rows: List[Dict[str, Any]] = []
    for bid in BATCH_IDS:
        r = trace_by_id.get(bid) or {}
        pass_ok = r.get("dryrun_pass") is True
        no_fileop_ok = r.get("file_operation_executed_now") is False
        no_rerun_ok = r.get("verifier_rerun_executed_now") is False
        completeness_rows.append(
            _row(
                batch_id=bid,
                trace_present=bool(r),
                trace_pass=pass_ok,
                no_file_operation=no_fileop_ok,
                no_verifier_rerun_execution=no_rerun_ok,
                review_pass=bool(r) and pass_ok and no_fileop_ok and no_rerun_ok,
            )
        )

    trace_completeness_pass = all(x.get("review_pass") for x in completeness_rows) and (len(trace_rows) == 8)

    # Consume dry-run matrices as review inputs (do not execute anything)
    def _load_rows(name: str) -> List[Dict[str, Any]]:
        return (dry["artifacts"].get(name) or {}).get("rows") or []

    pre_gate_rows = _load_rows("batch_pre_gate_dryrun_result_v1.json")
    manifest_rows = _load_rows("batch_before_after_manifest_dryrun_v1.json")
    rollback_rows = _load_rows("batch_rollback_route_dryrun_v1.json")
    verifier_rows = _load_rows("batch_verifier_rerun_dryrun_v1.json")
    protected_rows = _load_rows("batch_protected_asset_guard_dryrun_v1.json")
    eval_rows = _load_rows("batch_eval_out_readonly_guard_dryrun_v1.json")
    domain_rows = _load_rows("batch_domain_isolation_dryrun_v1.json")
    abort_rows = _load_rows("batch_abort_condition_dryrun_v1.json")

    batch_matrix_review = [
        ("batch_pre_gate_review_v1.json", pre_gate_rows, "pre_gate_dryrun_pass", True),
        ("batch_manifest_review_v1.json", manifest_rows, "dryrun_pass", True),
        ("batch_rollback_route_review_v1.json", rollback_rows, "dryrun_pass", True),
        ("batch_verifier_rerun_non_execution_review_v1.json", verifier_rows, "dryrun_pass", True),
        ("batch_protected_asset_guard_review_v1.json", protected_rows, "protected_guard_pass", True),
        ("batch_eval_out_readonly_guard_review_v1.json", eval_rows, "eval_out_readonly_guard_pass", True),
        ("batch_domain_isolation_review_v1.json", domain_rows, "domain_isolation_pass", True),
        ("batch_abort_condition_review_v1.json", abort_rows, "dryrun_pass", True),
    ]

    review_tables: Dict[str, Dict[str, Any]] = {}
    table_pass_flags: List[bool] = []
    for out_name, rows, key, expected in batch_matrix_review:
        # accept either direct pass field or dryrun_pass on row
        def _row_pass(row: Dict[str, Any]) -> bool:
            if key in row:
                return row.get(key) is expected
            return row.get("dryrun_pass") is True

        ok_all = len(rows) == 8 and all(_row_pass(r) for r in rows)
        table_pass_flags.append(ok_all)
        review_tables[out_name] = {
            "rows": [
                _row(batch_id=r.get("batch_id"), review_key=key, expected=expected, observed=r.get(key, r.get("dryrun_pass")), review_pass=_row_pass(r))
                for r in rows
            ],
            "row_count": len(rows),
            "all_pass": ok_all,
            **_review_boundary_meta(),
        }

    # explicit non-execution reviews
    file_operation_non_execution_review = {
        "rows": [
            _row(
                check_id="no_real_file_operation",
                expected=False,
                observed=dsm.get("file_operation_executed_now"),
                review_pass=dsm.get("file_operation_executed_now") is False,
            ),
            _row(
                check_id="no_batch_arming",
                expected=False,
                observed=dsm.get("batch_armed_now"),
                review_pass=dsm.get("batch_armed_now") is False,
            ),
            _row(
                check_id="no_verifier_rerun_execution",
                expected=False,
                observed=dsm.get("verifier_rerun_executed_now"),
                review_pass=dsm.get("verifier_rerun_executed_now") is False,
            ),
            _row(
                check_id="no_eval_out_write",
                expected=False,
                observed=dsm.get("eval_out_modified_now"),
                review_pass=dsm.get("eval_out_modified_now") is False,
            ),
            _row(
                check_id="no_protected_hr_dnae_mod",
                expected=False,
                observed=bool(dsm.get("protected_asset_modified_now") or dsm.get("hr_modified_now") or dsm.get("dnae_modified_now")),
                review_pass=dsm.get("protected_asset_modified_now") is False and dsm.get("hr_modified_now") is False and dsm.get("dnae_modified_now") is False,
            ),
        ],
        "row_count": 5,
        "all_pass": True,
        **_review_boundary_meta(),
    }
    file_operation_non_execution_review["all_pass"] = all(r.get("review_pass") for r in file_operation_non_execution_review["rows"])

    input_review_rows = [
        _row(check_id="dryrun.phase", expected=DRYRUN_REQUIRED_PHASE, observed=dsm.get("phase"), review_pass=dsm.get("phase") == DRYRUN_REQUIRED_PHASE),
        _row(check_id="dryrun.verifier_go", expected="GO", observed=dvr.get("verifier"), review_pass=dvr.get("verifier") == "GO"),
        _row(check_id="dryrun.final_decision", expected=DRYRUN_REQUIRED_FINAL, observed=dsm.get("final_decision"), review_pass=dsm.get("final_decision") == DRYRUN_REQUIRED_FINAL),
        _row(check_id="dryrun.next_phase", expected=DRYRUN_REQUIRED_NEXT, observed=dsm.get("recommended_next_phase"), review_pass=dsm.get("recommended_next_phase") == DRYRUN_REQUIRED_NEXT),
    ]
    execution_dryrun_input_review = {
        "dryrun_root": str(dry["root"]) if dry["root"] else None,
        "dryrun_loaded": dry["loaded"],
        "missing": dry["missing"],
        "rows": input_review_rows,
        "row_count": len(input_review_rows),
        "all_pass": all(r.get("review_pass") for r in input_review_rows) and not blockers,
        "blockers": blockers,
        **_review_boundary_meta(),
    }

    b0_b7_batch_trace_completeness_review = {
        "rows": completeness_rows,
        "row_count": len(completeness_rows),
        "all_pass": trace_completeness_pass,
        **_review_boundary_meta(),
    }

    stabilized_execution_post_dryrun_review_policy = _row(
        phase_id=PHASE_ID,
        review_scope=REVIEW_SCOPE,
        dryrun_required_phase=DRYRUN_REQUIRED_PHASE,
        dryrun_required_final_decision=DRYRUN_REQUIRED_FINAL,
        dryrun_required_next_phase=DRYRUN_REQUIRED_NEXT,
        required_dryrun_artifacts=list(DRYRUN_REQUIRED_ARTIFACTS),
        batch_count=8,
    )

    # readiness: can proceed to authorization planning only if all reviews pass.
    all_reviews_pass = (
        not blockers
        and execution_dryrun_input_review["all_pass"]
        and b0_b7_batch_trace_completeness_review["all_pass"]
        and all(table_pass_flags)
        and file_operation_non_execution_review["all_pass"]
    )
    boundary_ok = all_reviews_pass

    stabilized_execution_post_dryrun_review_readiness_decision = {
        "final_decision": FINAL_DECISION if boundary_ok else "MAIN_PROJECT_STRUCTURE_MIGRATION_STABILIZED_EXECUTION_POST_DRYRUN_REVIEW_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "ready_for_batch_authorization_planning": boundary_ok,
        "review_completed": boundary_ok,
        **_review_boundary_meta(),
    }

    summary = {
        "phase": PHASE_ID,
        "review_scope": REVIEW_SCOPE,
        "dryrun_input_loaded": dry["loaded"],
        "dryrun_verifier_go": dvr.get("verifier") == "GO" and dvr.get("passed") is True,
        "dryrun_boundary_ok": dsm.get("boundary_ok") is True,
        "dryrun_final_decision_ok": dsm.get("final_decision") == DRYRUN_REQUIRED_FINAL,
        "dryrun_next_phase_ok": dsm.get("recommended_next_phase") == DRYRUN_REQUIRED_NEXT,
        "dryrun_artifact_count_required": len(DRYRUN_REQUIRED_ARTIFACTS),
        "dryrun_artifacts_present": len(DRYRUN_REQUIRED_ARTIFACTS) - len(dry["missing"]) if dry["root"] else 0,
        "trace_completeness_review_pass": trace_completeness_pass,
        "matrix_reviews_pass": all(table_pass_flags),
        "file_operation_non_execution_review_pass": file_operation_non_execution_review["all_pass"],
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "final_decision": FINAL_DECISION if boundary_ok else "MAIN_PROJECT_STRUCTURE_MIGRATION_STABILIZED_EXECUTION_POST_DRYRUN_REVIEW_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        **_review_boundary_meta(),
    }

    return {
        "summary": summary,
        "stabilized_execution_post_dryrun_review_policy": stabilized_execution_post_dryrun_review_policy,
        "execution_dryrun_input_review": execution_dryrun_input_review,
        "b0_b7_batch_trace_completeness_review": b0_b7_batch_trace_completeness_review,
        "batch_pre_gate_review": review_tables["batch_pre_gate_review_v1.json"],
        "batch_manifest_review": review_tables["batch_manifest_review_v1.json"],
        "batch_rollback_route_review": review_tables["batch_rollback_route_review_v1.json"],
        "batch_verifier_rerun_non_execution_review": review_tables["batch_verifier_rerun_non_execution_review_v1.json"],
        "batch_protected_asset_guard_review": review_tables["batch_protected_asset_guard_review_v1.json"],
        "batch_eval_out_readonly_guard_review": review_tables["batch_eval_out_readonly_guard_review_v1.json"],
        "batch_domain_isolation_review": review_tables["batch_domain_isolation_review_v1.json"],
        "batch_abort_condition_review": review_tables["batch_abort_condition_review_v1.json"],
        "file_operation_non_execution_review": file_operation_non_execution_review,
        "stabilized_execution_post_dryrun_review_readiness_decision": stabilized_execution_post_dryrun_review_readiness_decision,
    }

