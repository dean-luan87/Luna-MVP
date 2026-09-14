#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for Task Manager Contract v1."""

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
        "summary": "task_manager_contract_v1_summary.json",
        "intake": "task_manager_contract_input_intake_matrix_v1.json",
        "task_schema": "task_manager_task_object_schema_v1.json",
        "lifecycle_schema": "task_manager_lifecycle_event_schema_v1.json",
        "commit_schema": "task_manager_commit_decision_schema_v1.json",
        "state_machine": "task_manager_state_machine_contract_v1.json",
        "transition_guard": "task_manager_transition_guard_policy_v1.json",
        "confirmation_gate": "task_manager_confirmation_gate_policy_v1.json",
        "safety_gate": "task_manager_safety_gate_policy_v1.json",
        "idempotency": "task_manager_idempotency_duplicate_policy_v1.json",
        "rollback_abort": "task_manager_rollback_abort_policy_v1.json",
        "external_boundary": "task_manager_external_boundary_policy_v1.json",
        "runtime_disabled": "task_manager_runtime_disabled_policy_v1.json",
        "future_dryrun": "task_manager_future_runtime_dryrun_entrypoint_v1.json",
        "audit_trace": "task_manager_audit_trace_policy_v1.json",
        "midplatform_integration": "task_manager_midplatform_integration_contract_v1.json",
        "context_enrichment_schema": "task_manager_task_context_enrichment_schema_v1.json",
        "enrichment_source_policy": "task_manager_context_enrichment_source_policy_v1.json",
        "verification_context_policy": "task_manager_task_verification_context_policy_v1.json",
        "execution_support_policy": "task_manager_execution_support_context_policy_v1.json",
        "trace": "task_manager_contract_decision_trace_v1.json",
        "final": "task_manager_contract_final_decision_v1.json",
        "boundary": "task_manager_contract_boundary_report_v1.json",
        "metrics": "task_manager_contract_metrics_candidate_report_v1.json",
        "benchmark_link": "task_manager_contract_benchmark_link_report_v1.json",
        "health_report": "task_manager_contract_system_health_report_v1.json",
        "no_write": "task_manager_contract_no_write_boundary_report_v1.json",
        "sim_report": "task_manager_contract_simulation_context_report_v1.json",
        "non_claims": "task_manager_contract_non_claims_report_v1.json",
        "followups": "task_manager_contract_open_followups_v1.json",
        "audit": "task_manager_contract_audit_report_v1.json",
    }
    data: Dict[str, Any] = {}
    for k, f in files.items():
        p = root / f
        if not p.is_file():
            blockers.append(f"missing:{k}")
        else:
            data[k] = json.loads(p.read_text(encoding="utf-8"))

    if blockers:
        _write_json(root / "task_manager_contract_verifier_report_v1.json", {"verdict": "NO_GO", "blockers": blockers})
        print(json.dumps({"verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    s = data["summary"]
    ok(s.get("contract_scope") == "task_manager_contract_only", "scope")
    ok(s.get("based_on_midplatform_task_state_runtime") is True, "mp_state")
    ok(s.get("task_manager_contract_defined") is True, "contract_def")
    ok(s.get("task_manager_runtime_invoked") is False, "no_rt")
    ok(s.get("task_state_committed_now") is False, "no_commit")
    ok(s.get("task_context_enrichment_schema_defined") is True, "enrichment_def")

    ok(data["task_schema"].get("owner_module") == "task_manager", "owner_tm")
    ctx_fields = data["task_schema"].get("context_enrichment_fields") or []
    fd = data["task_schema"].get("field_definitions") or {}
    ok("gps_location_candidate" in ctx_fields or "gps_location_candidate" in fd, "gps_field")
    ok("spatial_anchor" in ctx_fields or "spatial_anchor" in (data["task_schema"].get("field_definitions") or {}), "spatial_anchor")
    ok("memory_reference_context" in ctx_fields, "memory_ref_field")

    ces = data["context_enrichment_schema"]
    ok(ces.get("can_override_live_observation") is False, "no_override_obs")
    ok(len(ces.get("candidates") or []) > 0, "enrich_candidates")

    vcp = data["verification_context_policy"]
    ok(vcp.get("memory_reference_cannot_complete_task_alone") is True, "mem_not_alone")
    ok(vcp.get("gps_candidate_cannot_complete_task_alone") is True, "gps_not_alone")
    ok(vcp.get("task_completed_now") is False, "not_completed")
    ok(vcp.get("write_allowed") is False, "vcp_write")

    esp = data["execution_support_policy"]
    ok(esp.get("execution_support_context_cannot_trigger_runtime_action_directly") is True, "esp_no_action")
    ok(esp.get("task_completed_now") is False, "esp_completed")

    events = data["lifecycle_schema"].get("event_types") or []
    ok("TASK_CANCEL_PENDING_CONFIRMATION" in events, "cancel_pending_event")
    ok(data["lifecycle_schema"].get("committed_now") is False, "lc_not_committed")

    ok(data["commit_schema"].get("allowed_now") is False, "commit_not_now")

    states = {st.get("state") for st in data["state_machine"].get("states") or []}
    ok("TASK_ACTIVE" in states, "task_active")
    ok("TASK_CANCELLED" in states, "task_cancelled")

    tg = data["transition_guard"]
    ok(tg.get("task_manager_owns_commit") is True, "tm_owns_commit")
    ok(tg.get("cancel_requires_confirmation") is True, "cancel_confirm")

    ok(data["confirmation_gate"].get("cancel_requires_confirmation") is True, "cg_cancel")

    ok(data["safety_gate"].get("safety_alert_can_block_task_commit") is True, "safety_block")

    ok(data["idempotency"].get("duplicate_commit_forbidden") is True, "no_dup")

    ok(data["rollback_abort"].get("corrective_event_append_only") is True, "append_only")

    eb = data["external_boundary"]
    ok(eb.get("midplatform_cannot_commit_lifecycle_directly") is True, "mp_no_commit")
    ok(eb.get("voice_cannot_commit_lifecycle_directly") is True, "voice_no_commit")
    ok(eb.get("navigation_guidance_cannot_commit_lifecycle_directly") is True, "nav_no_commit")

    ok(data["runtime_disabled"].get("task_manager_runtime_available") is False, "rt_disabled")

    fd = data["future_dryrun"]
    ok(fd.get("recommended_next_phase") == "Task-Manager-Runtime-DryRun-v1", "next_phase")

    ok(data["audit_trace"].get("source_chain_required") is True, "source_chain")

    mi = data["midplatform_integration"]
    ok(mi.get("lifecycle_candidate_required_for_commit") is True, "lc_required")
    ok(mi.get("commit_invoked_now") is False, "commit_not_now")

    final = data["final"]
    ok(final.get("final_decision") == "TASK_MANAGER_CONTRACT_READY", "final")

    ok(data["boundary"].get("contract_only") is True, "contract_only")
    ok(data["metrics"].get("no_write_boundary_pass_rate") == 1.0, "nw_rate")
    ok(data["no_write"].get("boundary_ok") is True, "nw_ok")
    ok(data["sim_report"].get("simulation_profile_id") == "developer_full", "sim")
    ok(data["audit"].get("midplatform_fact_written") is False, "audit")

    verdict = "GO" if not blockers else "NO_GO"
    report = {
        "verdict": verdict,
        "checks_passed": checks,
        "checks_expected": 79,
        "blockers": blockers,
        "final_decision": final.get("final_decision"),
        "phase": "Task-Manager-Contract-v1-001",
    }
    _write_json(root / "task_manager_contract_verifier_report_v1.json", report)
    print(json.dumps(report, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
