# -*- coding: utf-8 -*-
"""Main Project Structure Migration Stabilized Execution DryRun v1.

Dry-run-only: simulate B0–B7 execution plan consumption and chaining.
No real file operations, no batch arming, no verifier reruns, no rollback rehearsal execution.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.main_project_structure_migration_guarded_planning_v1 import GATE_DEFS
from capabilities.governance.main_project_structure_migration_stabilized_execution_planning_v1 import (
    FINAL_DECISION as PLANNING_FINAL_DECISION,
    NEXT_PHASE as PLANNING_NEXT_PHASE,
    PAUSED_GC_ARTIFACT,
    PAUSED_REGISTRY_NEXT,
    PHASE_ID as PLANNING_PHASE_ID,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID

PHASE_ID = "Phase-Main-Project-Structure-Migration-Stabilized-Execution-DryRun-v1-001"
DRYRUN_SCOPE = "main_project_structure_migration_stabilized_execution_dryrun_only"
SOURCE_CHAIN = "main_project_structure_migration_stabilized_execution_dryrun_v1"

FINAL_DECISION = "MAIN_PROJECT_STRUCTURE_MIGRATION_STABILIZED_EXECUTION_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
NEXT_PHASE = "Phase-Main-Project-Structure-Migration-Stabilized-Execution-Post-DryRun-Review-v1-001"

PLANNING_REQUIRED_PHASE = PLANNING_PHASE_ID
PLANNING_REQUIRED_FINAL = PLANNING_FINAL_DECISION
PLANNING_REQUIRED_NEXT = PHASE_ID

PLANNING_REQUIRED_ARTIFACTS: Tuple[str, ...] = (
    "summary.json",
    "verifier_report.json",
    "stabilized_execution_planning_policy_v1.json",
    "resume_planning_input_review_v1.json",
    "b0_b7_execution_batch_plan_v1.json",
    "batch_pre_gate_matrix_v1.json",
    "batch_before_after_manifest_plan_v1.json",
    "batch_rollback_route_plan_v1.json",
    "batch_verifier_rerun_plan_v1.json",
    "batch_protected_asset_guard_matrix_v1.json",
    "batch_eval_out_readonly_guard_v1.json",
    "batch_domain_isolation_matrix_v1.json",
    "batch_abort_condition_matrix_v1.json",
    "stabilized_execution_planning_readiness_decision_v1.json",
)

BATCH_IDS: Tuple[str, ...] = ("B0", "B1", "B2", "B3", "B4", "B5", "B6", "B7")

# Must match planning's common abort list semantics (consumed only; never triggered in dry-run).
COMMON_ABORT_CONDITIONS: Tuple[str, ...] = (
    "protected_asset_intersection_detected",
    "eval_out_write_attempted",
    "cross_domain_batch_mix_detected",
    "before_manifest_missing",
    "rollback_route_missing",
    "verifier_rerun_list_missing",
    "runtime_behavior_change_detected",
    "model_ocr_voice_navigation_routing_change_detected",
    "gc_registry_recursion_attempted",
    "batch_arming_without_authorization",
)


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _dryrun_boundary_meta() -> Dict[str, Any]:
    return {
        "execution_dryrun_only": True,
        "simulated": True,
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
    return {
        **kwargs,
        **_dryrun_boundary_meta(),
        "planned_now": True,
        "executed_now": False,
        "simulated_now": True,
    }


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def _load_planning_root(path_str: Optional[str]) -> Dict[str, Any]:
    root = Path(path_str).expanduser().resolve() if path_str else None
    artifacts: Dict[str, Any] = {}
    missing: List[str] = []
    if root:
        for name in PLANNING_REQUIRED_ARTIFACTS:
            payload = _try_read_json(root / name)
            if payload is None:
                missing.append(name)
            else:
                artifacts[name] = payload
    loaded = bool(root) and not missing and bool(artifacts.get("summary.json")) and bool(artifacts.get("verifier_report.json"))
    return {"root": root, "loaded": loaded, "artifacts": artifacts, "missing": missing}


def _index_rows(rows: List[Dict[str, Any]], key: str) -> Dict[str, Dict[str, Any]]:
    out: Dict[str, Dict[str, Any]] = {}
    for r in rows:
        k = r.get(key)
        if isinstance(k, str) and k:
            out[k] = r
    return out


def run_main_project_structure_migration_stabilized_execution_dryrun_v1(
    *,
    stabilized_execution_planning_root: str,
) -> Dict[str, Any]:
    plan = _load_planning_root(stabilized_execution_planning_root)
    blockers: List[str] = []
    if not plan["loaded"]:
        blockers.append(f"planning input incomplete: {plan['missing']}")

    plan_summary = (plan["artifacts"].get("summary.json") or {}) if plan["artifacts"] else {}
    plan_verifier = (plan["artifacts"].get("verifier_report.json") or {}) if plan["artifacts"] else {}

    if plan_verifier.get("verifier") != "GO" or plan_verifier.get("passed") is not True:
        blockers.append("planning verifier must be GO")
    if plan_summary.get("boundary_ok") is not True:
        blockers.append("planning boundary_ok must be true")
    if plan_summary.get("final_decision") != PLANNING_REQUIRED_FINAL:
        blockers.append("planning final_decision mismatch")
    if plan_summary.get("recommended_next_phase") != PLANNING_REQUIRED_NEXT:
        blockers.append("planning recommended_next_phase must be dryrun phase")
    if plan_summary.get("registry_generation_authorization_continued_now") is not False:
        blockers.append("registry authorization must not continue now")
    if plan_summary.get("artifact_generation_planning_continued_now") is not False:
        blockers.append("GC artifact planning must not continue now")

    batch_plan = (plan["artifacts"].get("b0_b7_execution_batch_plan_v1.json") or {}).get("rows") or []
    gate_rows = (plan["artifacts"].get("batch_pre_gate_matrix_v1.json") or {}).get("rows") or []
    manifest_rows = (plan["artifacts"].get("batch_before_after_manifest_plan_v1.json") or {}).get("rows") or []
    rollback_rows = (plan["artifacts"].get("batch_rollback_route_plan_v1.json") or {}).get("rows") or []
    verifier_rows = (plan["artifacts"].get("batch_verifier_rerun_plan_v1.json") or {}).get("rows") or []
    protected_rows = (plan["artifacts"].get("batch_protected_asset_guard_matrix_v1.json") or {}).get("rows") or []
    eval_guard_rows = (plan["artifacts"].get("batch_eval_out_readonly_guard_v1.json") or {}).get("rows") or []
    domain_rows = (plan["artifacts"].get("batch_domain_isolation_matrix_v1.json") or {}).get("rows") or []
    abort_rows = (plan["artifacts"].get("batch_abort_condition_matrix_v1.json") or {}).get("rows") or []

    batch_by_id = _index_rows(batch_plan, "batch_id")
    manifest_by_id = _index_rows(manifest_rows, "batch_id")
    rollback_by_id = _index_rows(rollback_rows, "batch_id")
    verifier_by_id = _index_rows(verifier_rows, "batch_id")
    protected_by_id = _index_rows(protected_rows, "batch_id")
    eval_by_id = _index_rows(eval_guard_rows, "batch_id")
    domain_by_id = _index_rows(domain_rows, "batch_id")

    # per-batch consumption checks (simulate only: do not read/write any repo files)
    trace_rows: List[Dict[str, Any]] = []
    pre_gate_result_rows: List[Dict[str, Any]] = []
    manifest_result_rows: List[Dict[str, Any]] = []
    rollback_result_rows: List[Dict[str, Any]] = []
    verifier_result_rows: List[Dict[str, Any]] = []
    protected_result_rows: List[Dict[str, Any]] = []
    eval_out_result_rows: List[Dict[str, Any]] = []
    domain_result_rows: List[Dict[str, Any]] = []
    abort_result_rows: List[Dict[str, Any]] = []

    all_pass = True
    for idx, bid in enumerate(BATCH_IDS):
        b = batch_by_id.get(bid) or {}
        m = manifest_by_id.get(bid) or {}
        rr = rollback_by_id.get(bid) or {}
        vr = verifier_by_id.get(bid) or {}
        pr = protected_by_id.get(bid) or {}
        er = eval_by_id.get(bid) or {}
        dr = domain_by_id.get(bid) or {}
        ar = [r for r in abort_rows if r.get("batch_id") == bid]

        # consumption pass criteria
        pre_gates = [r for r in gate_rows if r.get("batch_id") == bid]
        pre_gate_pass = len(pre_gates) == len(GATE_DEFS)
        manifest_pass = bool(m.get("before_manifest_plan_id")) and bool(m.get("after_manifest_plan_id")) and (
            m.get("manifest_generated_now") is False
        )
        rollback_pass = bool(rr.get("rollback_route_id")) and rr.get("rollback_executed_now") is False
        verifier_pass = isinstance(vr.get("verifier_rerun_list"), list) and len(vr.get("verifier_rerun_list") or []) >= 1
        verifier_pass = verifier_pass and vr.get("verifier_rerun_executed_now") is False
        protected_pass = pr.get("guard_pass") is True and pr.get("protected_path_intersection") is False
        eval_out_pass = er.get("guard_pass") is True and er.get("eval_out_write_allowed") is False and er.get("eval_out_readonly") is True
        domain_pass = dr.get("isolation_pass") is True and dr.get("single_domain_only") is True
        abort_pass = len(ar) >= 1 and all(r.get("abort_on_trigger") is True and r.get("triggered_now") is False for r in ar)

        batch_pass = all(
            [
                pre_gate_pass,
                manifest_pass,
                rollback_pass,
                verifier_pass,
                protected_pass,
                eval_out_pass,
                domain_pass,
                abort_pass,
                b.get("protected_path_intersection") is False,
                b.get("eval_out_write_allowed") is False,
                b.get("path_actually_touched_now") is False,
                b.get("touched_now") is False,
                b.get("file_operation_executed_now") is False,
            ]
        )
        if not batch_pass:
            all_pass = False

        trace_rows.append(
            _row(
                batch_id=bid,
                execution_order_index=idx,
                simulated_trace_steps=[
                    "consume_pre_gates",
                    "consume_before_manifest_plan",
                    "consume_after_manifest_plan",
                    "consume_rollback_route",
                    "consume_verifier_rerun_list(no_execute)",
                    "consume_abort_conditions(no_trigger)",
                    "protected_asset_guard_check",
                    "eval_out_readonly_guard_check",
                    "domain_isolation_check",
                ],
                inputs_consumed={
                    "batch_plan_row_present": bool(b),
                    "gate_rows_count": len(pre_gates),
                    "manifest_row_present": bool(m),
                    "rollback_row_present": bool(rr),
                    "verifier_row_present": bool(vr),
                    "abort_rows_count": len(ar),
                    "protected_guard_row_present": bool(pr),
                    "eval_out_guard_row_present": bool(er),
                    "domain_row_present": bool(dr),
                },
                dryrun_pass=batch_pass,
                file_operation_executed_now=False,
                verifier_rerun_executed_now=False,
            )
        )

        pre_gate_result_rows.append(_row(batch_id=bid, pre_gate_dryrun_pass=pre_gate_pass, expected_gate_count=len(GATE_DEFS), observed_gate_count=len(pre_gates)))
        manifest_result_rows.append(_row(batch_id=bid, before_manifest_plan_consumed=bool(m.get("before_manifest_plan_id")), after_manifest_plan_consumed=bool(m.get("after_manifest_plan_id")), manifest_generated_now=False, dryrun_pass=manifest_pass))
        rollback_result_rows.append(_row(batch_id=bid, rollback_route_consumed=bool(rr.get("rollback_route_id")), rollback_executed_now=False, dryrun_pass=rollback_pass))
        verifier_result_rows.append(_row(batch_id=bid, verifier_rerun_list_consumed=bool(vr.get("verifier_rerun_list")), verifier_rerun_executed_now=False, dryrun_pass=verifier_pass))
        protected_result_rows.append(_row(batch_id=bid, protected_guard_pass=protected_pass, protected_path_intersection=False))
        eval_out_result_rows.append(_row(batch_id=bid, eval_out_readonly_guard_pass=eval_out_pass, eval_out_write_allowed=False))
        domain_result_rows.append(_row(batch_id=bid, domain_isolation_pass=domain_pass))
        abort_result_rows.append(_row(batch_id=bid, abort_conditions_consumed=len(ar) >= 1, abort_triggered_now=False, dryrun_pass=abort_pass))

    boundary_ok = bool(all_pass) and not blockers

    stabilized_execution_dryrun_policy = _row(
        phase_id=PHASE_ID,
        dryrun_scope=DRYRUN_SCOPE,
        planning_required_phase=PLANNING_REQUIRED_PHASE,
        planning_required_final_decision=PLANNING_REQUIRED_FINAL,
        planning_required_next_phase=PLANNING_REQUIRED_NEXT,
        batch_ids=list(BATCH_IDS),
        planning_required_artifacts=list(PLANNING_REQUIRED_ARTIFACTS),
        gc_branch_reference_only=True,
        registry_authorization_paused=True,
    )

    execution_planning_input_review = {
        "planning_root": str(plan["root"]) if plan["root"] else None,
        "planning_loaded": plan["loaded"],
        "missing": plan["missing"],
        "planning_summary": {
            "phase": plan_summary.get("phase"),
            "boundary_ok": plan_summary.get("boundary_ok"),
            "final_decision": plan_summary.get("final_decision"),
            "recommended_next_phase": plan_summary.get("recommended_next_phase"),
        },
        "planning_verifier": {
            "verifier": plan_verifier.get("verifier"),
            "passed": plan_verifier.get("passed"),
            "check_count": plan_verifier.get("check_count"),
        },
        "all_pass": not blockers,
        "blockers": blockers,
        **_dryrun_boundary_meta(),
    }

    b0_b7_batch_dryrun_trace = {
        "rows": trace_rows,
        "row_count": len(trace_rows),
        "batch_count": len(BATCH_IDS),
        "all_pass": all(r.get("dryrun_pass") is True for r in trace_rows),
        **_dryrun_boundary_meta(),
    }

    def _matrix(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
        return {"rows": rows, "row_count": len(rows), "all_pass": all(r.get("dryrun_pass", True) for r in rows), **_dryrun_boundary_meta()}

    batch_pre_gate_dryrun_result = _matrix(pre_gate_result_rows)
    batch_before_after_manifest_dryrun = _matrix(manifest_result_rows)
    batch_rollback_route_dryrun = _matrix(rollback_result_rows)
    batch_verifier_rerun_dryrun = _matrix(verifier_result_rows)
    batch_protected_asset_guard_dryrun = {"rows": protected_result_rows, "row_count": len(protected_result_rows), "all_pass": all(r.get("protected_guard_pass") for r in protected_result_rows), **_dryrun_boundary_meta()}
    batch_eval_out_readonly_guard_dryrun = {"rows": eval_out_result_rows, "row_count": len(eval_out_result_rows), "all_pass": all(r.get("eval_out_readonly_guard_pass") for r in eval_out_result_rows), **_dryrun_boundary_meta()}
    batch_domain_isolation_dryrun = {"rows": domain_result_rows, "row_count": len(domain_result_rows), "all_pass": all(r.get("domain_isolation_pass") for r in domain_result_rows), **_dryrun_boundary_meta()}
    batch_abort_condition_dryrun = _matrix(abort_result_rows)

    stabilized_execution_dryrun_readiness_decision = {
        "final_decision": FINAL_DECISION if boundary_ok else "MAIN_PROJECT_STRUCTURE_MIGRATION_STABILIZED_EXECUTION_DRYRUN_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "ready_for_post_dryrun_review": boundary_ok,
        "dryrun_completed": boundary_ok,
        "planning_inputs_consumed": bool(plan["loaded"]),
        **_dryrun_boundary_meta(),
    }

    summary = {
        "phase": PHASE_ID,
        "dryrun_scope": DRYRUN_SCOPE,
        "execution_dryrun_only": True,
        "simulated": True,
        "planning_input_loaded": plan["loaded"],
        "planning_verifier_go": plan_verifier.get("verifier") == "GO" and plan_verifier.get("passed") is True,
        "planning_final_decision_ok": plan_summary.get("final_decision") == PLANNING_REQUIRED_FINAL,
        "planning_next_phase_ok": plan_summary.get("recommended_next_phase") == PLANNING_REQUIRED_NEXT,
        "planning_artifact_count_required": len(PLANNING_REQUIRED_ARTIFACTS),
        "planning_artifacts_present": len(PLANNING_REQUIRED_ARTIFACTS) - len(plan["missing"]) if plan["root"] else 0,
        "batch_count": len(BATCH_IDS),
        "all_batches_traced": len(trace_rows) == len(BATCH_IDS),
        "pre_gate_dryrun_pass": batch_pre_gate_dryrun_result.get("all_pass") is True,
        "manifest_dryrun_pass": batch_before_after_manifest_dryrun.get("all_pass") is True,
        "rollback_dryrun_pass": batch_rollback_route_dryrun.get("all_pass") is True,
        "verifier_rerun_dryrun_pass": batch_verifier_rerun_dryrun.get("all_pass") is True,
        "protected_guard_pass": batch_protected_asset_guard_dryrun.get("all_pass") is True,
        "eval_out_readonly_guard_pass": batch_eval_out_readonly_guard_dryrun.get("all_pass") is True,
        "domain_isolation_pass": batch_domain_isolation_dryrun.get("all_pass") is True,
        "abort_condition_dryrun_pass": batch_abort_condition_dryrun.get("all_pass") is True,
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "final_decision": FINAL_DECISION if boundary_ok else "MAIN_PROJECT_STRUCTURE_MIGRATION_STABILIZED_EXECUTION_DRYRUN_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        # forbidden chain continuation sentinels
        "next_not_registry_dryrun": PAUSED_REGISTRY_NEXT not in (NEXT_PHASE or ""),
        "next_not_gc_artifact": PAUSED_GC_ARTIFACT not in (NEXT_PHASE or ""),
        **_dryrun_boundary_meta(),
    }

    return {
        "summary": summary,
        "stabilized_execution_dryrun_policy": stabilized_execution_dryrun_policy,
        "execution_planning_input_review": execution_planning_input_review,
        "b0_b7_batch_dryrun_trace": b0_b7_batch_dryrun_trace,
        "batch_pre_gate_dryrun_result": batch_pre_gate_dryrun_result,
        "batch_before_after_manifest_dryrun": batch_before_after_manifest_dryrun,
        "batch_rollback_route_dryrun": batch_rollback_route_dryrun,
        "batch_verifier_rerun_dryrun": batch_verifier_rerun_dryrun,
        "batch_protected_asset_guard_dryrun": batch_protected_asset_guard_dryrun,
        "batch_eval_out_readonly_guard_dryrun": batch_eval_out_readonly_guard_dryrun,
        "batch_domain_isolation_dryrun": batch_domain_isolation_dryrun,
        "batch_abort_condition_dryrun": batch_abort_condition_dryrun,
        "stabilized_execution_dryrun_readiness_decision": stabilized_execution_dryrun_readiness_decision,
    }
