#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for Basic Functional Loop Runtime Logic Audit and Correction v1."""

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
        "summary": "basic_functional_loop_runtime_logic_audit_correction_v1_summary.json",
        "intake": "basic_loop_runtime_logic_input_intake_matrix_v1.json",
        "mainline": "basic_loop_runtime_mainline_sequence_matrix_v1.json",
        "baseline_policy": "basic_loop_baseline_safety_loop_policy_v1.json",
        "task_driven_policy": "basic_loop_task_driven_loop_policy_v1.json",
        "authority": "basic_loop_authority_boundary_matrix_v1.json",
        "candidate_transition": "basic_loop_candidate_to_commit_transition_matrix_v1.json",
        "observation_gap": "basic_loop_observation_request_gap_analysis_v1.json",
        "observation_stub": "basic_loop_task_observation_request_contract_stub_v1.json",
        "evidence_lifecycle": "basic_loop_vision_evidence_lifecycle_matrix_v1.json",
        "ocr_joint": "basic_loop_ocr_joint_gate_matrix_v1.json",
        "speech_path": "basic_loop_speech_output_path_matrix_v1.json",
        "arbitration": "basic_loop_safety_task_arbitration_matrix_v1.json",
        "nav_boundary": "basic_loop_navigation_guidance_action_boundary_v1.json",
        "info_lifecycle": "basic_loop_information_lifecycle_gap_registry_v1.json",
        "memory_deferred": "basic_loop_memory_system_boundary_deferred_report_v1.json",
        "missing_contracts": "basic_loop_missing_contract_registry_v1.json",
        "roadmap": "basic_loop_corrected_phase_roadmap_v1.json",
        "trace": "basic_loop_runtime_logic_audit_decision_trace_v1.json",
        "final": "basic_loop_runtime_logic_audit_final_decision_v1.json",
        "boundary": "basic_loop_runtime_logic_audit_boundary_report_v1.json",
        "metrics": "basic_loop_runtime_logic_audit_metrics_candidate_report_v1.json",
        "benchmark_link": "basic_loop_runtime_logic_audit_benchmark_link_report_v1.json",
        "health_report": "basic_loop_runtime_logic_audit_system_health_report_v1.json",
        "no_write": "basic_loop_runtime_logic_audit_no_write_boundary_report_v1.json",
        "sim_report": "basic_loop_runtime_logic_audit_simulation_context_report_v1.json",
        "non_claims": "basic_loop_runtime_logic_audit_non_claims_report_v1.json",
        "followups": "basic_loop_runtime_logic_audit_open_followups_v1.json",
        "audit": "basic_loop_runtime_logic_audit_audit_report_v1.json",
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
            root / "basic_loop_runtime_logic_audit_verifier_report_v1.json",
            {"verdict": "NO_GO", "blockers": blockers},
        )
        print(json.dumps({"verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    s = data["summary"]
    ok(s.get("audit_scope") == "runtime_logic_audit_and_correction_only", "scope")
    ok(s.get("baseline_safety_loop_defined") is True, "baseline_def")
    ok(s.get("task_driven_loop_defined") is True, "task_driven_def")
    ok(s.get("baseline_vs_task_driven_separation_defined") is True, "separation")
    ok(s.get("no_task_safety_runtime_allowed_as_baseline") is True, "no_task_safety")
    ok(s.get("task_driven_runtime_requires_task_context") is True, "task_ctx_req")
    ok(s.get("observation_request_gap_identified") is True, "obs_gap")
    ok(s.get("vision_evidence_lifecycle_defined") is True, "evidence_lc")
    ok(s.get("ocr_joint_gate_defined") is True, "ocr_gate")
    ok(s.get("speech_output_path_defined") is True, "speech_path")
    ok(s.get("safety_task_arbitration_defined") is True, "arbitration")
    ok(s.get("navigation_guidance_action_boundary_defined") is True, "nav_boundary_def")
    ok(s.get("information_lifecycle_gap_registered") is True, "info_lc_gap")
    ok(s.get("memory_system_boundary_deferred") is True, "memory_defer")
    ok(s.get("missing_contract_registry_generated") is True, "missing_contracts")
    ok(s.get("runtime_action_committed") is False, "no_runtime_commit")

    steps = data["mainline"].get("steps") or []
    baseline = [x for x in steps if x.get("loop_type") == "baseline_safety_loop"]
    task_drv = [x for x in steps if x.get("loop_type") == "task_driven_loop"]
    ok(len(baseline) >= 6, "baseline_steps")
    ok(len(task_drv) >= 9, "task_steps")
    ok(all(x.get("allowed_without_task") for x in baseline), "baseline_no_task")
    ok(all(x.get("requires_task_context") for x in task_drv), "task_requires_ctx")

    bp = data["baseline_policy"]
    ok(bp.get("baseline_safety_loop_enabled_by_default") is True, "baseline_default")
    ok(bp.get("generic_text_ocr_forbidden_without_task") is True, "no_generic_ocr")

    tdp = data["task_driven_policy"]
    ok(tdp.get("task_driven_loop_requires_task_or_goal") is True, "task_requires_goal")
    ok(tdp.get("safety_priority_above_task") is True, "safety_above_task")

    trans = data["candidate_transition"].get("candidates") or []
    ok(all(c.get("can_be_committed_now") is False for c in trans), "all_not_commit_now")

    og = data["observation_gap"]
    ok(og.get("explicit_observation_request_contract_missing") is True, "obs_contract_missing")

    stub = data["observation_stub"]
    ok(stub.get("recommended_future_phase") == "Task-Observation-Request-Contract-v1", "obs_stub_next")

    ocr = data["ocr_joint"]
    ok(ocr.get("ocr_allowed_now") is False, "ocr_not_now")
    ok(ocr.get("generic_environment_text_forbidden") is True, "no_generic_env_ocr")

    speech = data["speech_path"].get("paths") or []
    ok(all(p.get("requires_speech_gate") for p in speech), "speech_gate")
    ok(all(p.get("direct_tts_bypass_forbidden") for p in speech), "no_tts_bypass")

    arb = data["arbitration"]
    ok(arb.get("safety_priority_above_task") is True, "arb_safety")

    nav = data["nav_boundary"]
    ok(nav.get("guidance_is_not_action") is True, "guidance_not_action")
    ok(nav.get("navigation_action_triggered") is False, "no_nav_action")

    info = data["info_lifecycle"]
    ok(info.get("compression_policy_missing") is True, "compression_missing")
    ok(info.get("summarization_policy_missing") is True, "summarization_missing")

    mem = data["memory_deferred"]
    ok(mem.get("traditional_database_model_for_memory_rejected") is True, "no_db_memory")
    ok(mem.get("memory_runtime_invoked_now") is False, "mem_not_invoked")

    contracts = {c.get("contract_name") for c in data["missing_contracts"].get("contracts") or []}
    ok("Task-Observation-Request-Contract-v1" in contracts, "contract_obs")
    ok("Information-Lifecycle-Governance-v1" in contracts, "contract_info_lc")
    ok("Memory-System-Architecture-v1" in contracts, "contract_memory")

    final = data["final"]
    ok(
        final.get("final_decision")
        == "BASIC_FUNCTIONAL_LOOP_RUNTIME_LOGIC_CORRECTED_READY_FOR_OBSERVATION_REQUEST_CONTRACT",
        "final_decision",
    )
    ok(final.get("recommended_next_phase") == "Task-Observation-Request-Contract-v1", "next_phase")

    ok(data["boundary"].get("audit_only") is True, "audit_only")
    ok(data["metrics"].get("no_write_boundary_pass_rate") == 1.0, "nw_rate")
    ok(data["health_report"].get("no_runtime_health_claim") is True, "no_health_claim")
    ok(data["no_write"].get("boundary_ok") is True, "nw_ok")
    ok(data["no_write"].get("violations") == [], "nw_violations")
    ok(data["sim_report"].get("simulation_profile_id") == "developer_full", "sim_profile")
    ok(data["audit"].get("midplatform_fact_written") is False, "audit_no_fact")

    verdict = "GO" if not blockers else "NO_GO"
    report = {
        "verdict": verdict,
        "checks_passed": checks,
        "checks_expected": 74,
        "blockers": blockers,
        "final_decision": final.get("final_decision"),
        "phase": "Basic-Functional-Loop-Runtime-Logic-Audit-and-Correction-v1-001",
    }
    _write_json(root / "basic_loop_runtime_logic_audit_verifier_report_v1.json", report)
    print(json.dumps(report, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
