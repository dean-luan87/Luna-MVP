#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for Task Manager Runtime DryRun v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List


def _require_abs(p: str, label: str) -> Path:
    pp = Path(p).expanduser()
    if not pp.is_absolute():
        raise SystemExit(f"ERROR: {label} must be absolute, got: {p}")
    return pp.resolve()


def _write_json(path: Path, obj: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke-root", required=True)
    args = ap.parse_args()

    root = _require_abs(args.smoke_root, "--smoke-root")
    blockers: List[str] = []
    checks = 0

    def ok(c: bool, name: str) -> None:
        nonlocal checks
        if c:
            checks += 1
        else:
            blockers.append(name)

    files = {
        "summary": "task_manager_runtime_dryrun_v1_summary.json",
        "intake": "task_manager_runtime_input_intake_matrix_v1.json",
        "candidate_intake": "task_manager_runtime_candidate_intake_matrix_v1.json",
        "task_objects": "task_manager_runtime_task_object_candidate_collection_v1.json",
        "lifecycle_events": "task_manager_runtime_lifecycle_event_candidate_collection_v1.json",
        "commit_decisions": "task_manager_runtime_commit_decision_candidate_collection_v1.json",
        "fsm_matrix": "task_manager_runtime_state_machine_application_matrix_v1.json",
        "guard_matrix": "task_manager_runtime_transition_guard_application_matrix_v1.json",
        "confirm_matrix": "task_manager_runtime_confirmation_gate_application_matrix_v1.json",
        "safety_matrix": "task_manager_runtime_safety_gate_application_matrix_v1.json",
        "idempotency_dryrun": "task_manager_runtime_idempotency_duplicate_dryrun_v1.json",
        "enrichment_collection": "task_manager_runtime_context_enrichment_candidate_collection_v1.json",
        "verification_collection": "task_manager_runtime_verification_context_candidate_collection_v1.json",
        "execution_collection": "task_manager_runtime_execution_support_context_candidate_collection_v1.json",
        "downstream_collection": "task_manager_runtime_downstream_candidate_collection_v1.json",
        "spatial_relations": "task_manager_runtime_task_spatial_relation_candidate_v1.json",
        "information_gaps": "task_manager_runtime_information_gap_analysis_v1.json",
        "observation_plans": "task_manager_runtime_task_aware_observation_plan_v1.json",
        "ocr_needs": "task_manager_runtime_ocr_activation_need_candidate_v1.json",
        "human_needs": "task_manager_runtime_human_assistance_need_candidate_v1.json",
        "action_schedules": "task_manager_runtime_action_schedule_candidate_v1.json",
        "scheduling_policy": "task_manager_runtime_action_scheduling_policy_v1.json",
        "rollback_abort": "task_manager_runtime_rollback_abort_dryrun_v1.json",
        "audit_collection": "task_manager_runtime_audit_trace_collection_v1.json",
        "boundary_check": "task_manager_runtime_boundary_check_v1.json",
        "trace": "task_manager_runtime_decision_trace_v1.json",
        "final": "task_manager_runtime_final_decision_v1.json",
        "boundary": "task_manager_runtime_boundary_report_v1.json",
        "metrics": "task_manager_runtime_metrics_candidate_report_v1.json",
        "benchmark_link": "task_manager_runtime_benchmark_link_report_v1.json",
        "health_report": "task_manager_runtime_system_health_report_v1.json",
        "no_write": "task_manager_runtime_no_write_boundary_report_v1.json",
        "sim_report": "task_manager_runtime_simulation_context_report_v1.json",
        "non_claims": "task_manager_runtime_non_claims_report_v1.json",
        "followups": "task_manager_runtime_open_followups_v1.json",
        "audit": "task_manager_runtime_audit_report_v1.json",
    }
    data: Dict[str, Any] = {}
    for k, f in files.items():
        p = root / f
        if not p.is_file():
            blockers.append(f"missing:{k}")
        else:
            data[k] = json.loads(p.read_text(encoding="utf-8"))

    if blockers:
        _write_json(
            root / "task_manager_runtime_verifier_report_v1.json",
            {"verdict": "NO_GO", "blockers": blockers},
        )
        print(json.dumps({"verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    s = data["summary"]
    ok(s.get("dryrun_scope") == "task_manager_runtime_dryrun_only", "scope")
    ok(s.get("based_on_task_manager_contract") is True, "contract")
    ok(s.get("based_on_midplatform_task_state_runtime") is True, "mp_state")
    ok(s.get("task_state_candidate_count_observed") == 12, "tsc_12")
    ok(s.get("lifecycle_candidate_count_observed") == 12, "lc_12")
    ok(s.get("task_state_machine_applied") is True, "fsm")
    ok(s.get("transition_guard_applied") is True, "guard")
    ok(s.get("confirmation_gate_applied") is True, "confirm")
    ok(s.get("safety_gate_applied") is True, "safety")
    ok(s.get("idempotency_policy_applied") is True, "idempotency")
    ok(s.get("commit_decision_candidates_generated") is True, "commit_gen")
    ok(s.get("task_object_candidates_generated") is True, "tobj_gen")
    ok(s.get("lifecycle_event_candidates_generated") is True, "le_gen")
    ok(s.get("context_enrichment_candidates_generated") is True, "enr_gen")
    ok(s.get("verification_context_candidates_generated") is True, "vctx_gen")
    ok(s.get("execution_support_context_candidates_generated") is True, "exec_gen")
    ok(s.get("task_aware_action_scheduling_candidates_generated") is True, "sched_gen")
    ok(s.get("spatial_relation_candidates_generated") is True, "spatial_gen")
    ok(s.get("information_gap_analysis_generated") is True, "gap_gen")
    ok(s.get("observation_plan_candidates_generated") is True, "obs_plan_gen")
    ok(s.get("ocr_need_candidates_generated") is True, "ocr_need_gen")
    ok(s.get("human_assistance_need_candidates_generated") is True, "human_need_gen")
    ok(s.get("action_schedule_candidates_generated") is True, "action_sched_gen")
    ok(s.get("task_manager_runtime_invoked") is False, "no_rt")
    ok(s.get("task_state_committed_now") is False, "no_commit")
    ok(s.get("task_completed_now") is False, "not_completed")

    ok(data["intake"].get("rows"), "intake_rows")
    ci = data["candidate_intake"]
    ok(ci.get("task_state_candidate_count_observed") == 12, "ci_tsc")
    ok(ci.get("lifecycle_candidate_count_observed") == 12, "ci_lc")

    tobj = data["task_objects"].get("candidates") or []
    ok(len(tobj) == 12, "tobj_12")
    ok(all(c.get("task_state_committed_now") is False for c in tobj), "tobj_not_committed")
    nav_tobj = next((c for c in tobj if c.get("distance_to_target_candidate")), None)
    ok(nav_tobj is not None, "distance_field")
    ok(nav_tobj and nav_tobj.get("route_stage_candidate"), "route_stage_field")

    le = data["lifecycle_events"].get("candidates") or []
    ok(len(le) == 12, "le_12")
    ok(all(c.get("committed_now") is False for c in le), "le_not_committed")

    cd = data["commit_decisions"].get("candidates") or []
    ok(len(cd) == 12, "cd_12")
    ok(all(c.get("allowed_now") is False for c in cd), "cd_not_now")

    ok(len(data["fsm_matrix"].get("rows") or []) == 12, "fsm_rows")

    guards = {g.get("guard_name") for g in data["guard_matrix"].get("guards") or []}
    ok("cancel_requires_confirmation" in guards, "cancel_confirm_guard")

    confirm_rows = data["confirm_matrix"].get("rows") or []
    cancel_req = next((r for r in confirm_rows if "utt_007" in r.get("source_candidate_id", "")), None)
    ok(cancel_req and cancel_req.get("confirmation_required") is True, "cancel_req_confirm")

    scenarios = data["safety_matrix"].get("scenarios") or []
    inactive = next((x for x in scenarios if x.get("safety_active") is False), None)
    active = next((x for x in scenarios if x.get("safety_active") is True), None)
    ok(inactive and inactive.get("candidate_dryrun_continues") is True, "safety_false")
    ok(active and active.get("low_priority_commit_delayed") is True, "safety_true_delay")

    idem = data["idempotency_dryrun"]
    ok(idem.get("duplicate_commit_forbidden") is True, "no_dup")

    enr = data["enrichment_collection"]
    ok(enr.get("enrichment_candidate_count", 0) > 0, "enr_count")
    ok(enr.get("can_override_live_observation") is False, "no_override")
    ok(all(c.get("can_override_live_observation") is False for c in enr.get("candidates") or []), "enr_no_override")

    vctx = data["verification_collection"].get("candidates") or []
    ok(len(vctx) > 0, "vctx_count")
    ok(all(c.get("memory_reference_cannot_complete_task_alone") is True for c in vctx), "mem_alone")
    ok(all(c.get("gps_candidate_cannot_complete_task_alone") is True for c in vctx), "gps_alone")
    ok(data["verification_collection"].get("task_completed_now") is False, "vctx_not_done")

    execs = data["execution_collection"].get("candidates") or []
    ok(len(execs) > 0, "exec_count")
    ok(all(c.get("cannot_trigger_runtime_action_directly") is True for c in execs), "exec_no_action")
    ok(data["execution_collection"].get("navigation_action_triggered") is False, "exec_no_nav")

    ds = data["downstream_collection"].get("candidates") or []
    ok(len(ds) == 12, "ds_12")
    ok(all(c.get("invoked_now") is False for c in ds), "ds_not_invoked")

    sr = data["spatial_relations"].get("candidates") or []
    ok(len(sr) > 0, "spatial_count")
    ok(all(c.get("distance_to_target_candidate") is not None for c in sr[:3]), "spatial_distance")
    ok(all(c.get("route_stage_candidate") for c in sr), "spatial_route_stage")
    ok(all(c.get("can_complete_task_alone") is False for c in sr), "spatial_not_alone")

    gaps = data["information_gaps"].get("gaps") or []
    ok(len(gaps) > 0, "gap_count")
    gap_types = {g.get("gap_type") for g in gaps}
    ok("missing_information_source" in gap_types, "gap_info_source")
    ok("missing_readable_region" in gap_types, "gap_readable")
    ok("missing_safety_clearance" in gap_types, "gap_safety")

    obs_plans = data["observation_plans"].get("candidates") or []
    ok(len(obs_plans) > 0, "obs_plan_count")
    ok(all(p.get("camera_invoked_now") is False for p in obs_plans), "plan_no_camera")
    ok(all(p.get("ocr_invoked_now") is False for p in obs_plans), "plan_no_ocr")
    ok(all(p.get("navigation_action_triggered") is False for p in obs_plans), "plan_no_nav")

    ocr_n = data["ocr_needs"].get("candidates") or []
    ok(len(ocr_n) > 0, "ocr_need_count")
    ok(all(c.get("ocr_allowed_now") is False for c in ocr_n), "ocr_not_now")

    human_n = data["human_needs"].get("candidates") or []
    ok(len(human_n) > 0, "human_need_count")
    ok(all(c.get("confirmation_required") is True for c in human_n), "human_confirm")

    sched = data["action_schedules"].get("candidates") or []
    ok(len(sched) == 12, "sched_12")
    ok(all(c.get("runtime_action_committed") is False for c in sched), "sched_not_committed")
    ok(all(c.get("invoked_now") is False for c in sched), "sched_not_invoked")
    ok(data["scheduling_policy"].get("scheduled_action_cannot_execute_directly") is True, "policy_no_direct")

    final_sched_flags = data["final"]
    ok(final_sched_flags.get("task_aware_action_scheduling_candidates_generated") is True, "final_sched")

    rb = data["rollback_abort"]
    ok(rb.get("corrective_event_append_only") is True, "append_only")

    traces = data["audit_collection"].get("traces") or []
    ok(len(traces) == 12, "audit_12")
    ok(all(t.get("source_chain") for t in traces), "source_chain")

    bc = data["boundary_check"]
    ok(bc.get("violation_detected") is False, "no_violation")

    ok(len(data["trace"].get("steps") or []) >= 18, "trace_steps")

    final = data["final"]
    ok(
        final.get("final_decision")
        == "TASK_MANAGER_RUNTIME_DRYRUN_READY_FOR_VISION_OCR_INGEST_AND_NAVIGATION_LOOP",
        "final_decision",
    )

    ok(data["boundary"].get("runtime_dryrun_only") is True, "dryrun_only")
    ok(data["metrics"].get("no_write_boundary_pass_rate") == 1.0, "nw_rate")
    ok(data["health_report"].get("no_runtime_health_claim") is True, "no_health_claim")
    ok(data["no_write"].get("boundary_ok") is True, "nw_ok")
    ok(data["no_write"].get("violations") == [], "nw_violations")
    ok(data["sim_report"].get("simulation_profile_id") == "developer_full", "sim_profile")
    ok(data["non_claims"].get("claims"), "non_claims")
    ok(len(data["followups"].get("items") or []) >= 4, "followups")

    audit = data["audit"]
    ok(audit.get("task_manager_runtime_dryrun_v1_executed") is True, "audit_exec")
    ok(audit.get("midplatform_fact_written") is False, "audit_no_fact")
    ok(audit.get("runtime_routing_changed") is False, "audit_no_route")

    verdict = "GO" if not blockers else "NO_GO"
    report = {
        "verdict": verdict,
        "checks_passed": checks,
        "checks_expected": 95,
        "blockers": blockers,
        "final_decision": final.get("final_decision"),
        "phase": "Task-Manager-Runtime-DryRun-v1-001",
    }
    _write_json(root / "task_manager_runtime_verifier_report_v1.json", report)
    print(json.dumps(report, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
