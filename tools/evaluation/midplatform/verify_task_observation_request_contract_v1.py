#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for Task Observation Request Contract v1."""

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
        "summary": "task_observation_request_contract_v1_summary.json",
        "intake": "task_observation_request_input_intake_matrix_v1.json",
        "schema": "task_observation_request_schema_v1.json",
        "source_policy": "task_observation_request_source_policy_v1.json",
        "baseline_policy": "task_observation_baseline_safety_request_policy_v1.json",
        "task_driven_policy": "task_observation_task_driven_request_policy_v1.json",
        "routing_policy": "task_observation_target_module_routing_policy_v1.json",
        "gate_policy": "task_observation_request_gate_policy_v1.json",
        "ptf_policy": "task_observation_priority_timing_freshness_policy_v1.json",
        "candidates": "task_observation_request_candidate_collection_v1.json",
        "ocr_subpolicy": "task_observation_ocr_request_subpolicy_v1.json",
        "guidance_subpolicy": "task_observation_user_guidance_request_subpolicy_v1.json",
        "human_subpolicy": "task_observation_human_assistance_request_subpolicy_v1.json",
        "handoff": "task_observation_vision_ocr_ingest_handoff_contract_v1.json",
        "lifecycle_policy": "task_observation_request_lifecycle_policy_v1.json",
        "separation_matrix": "task_observation_safety_task_request_separation_matrix_v1.json",
        "trace": "task_observation_request_contract_decision_trace_v1.json",
        "final": "task_observation_request_contract_final_decision_v1.json",
        "boundary": "task_observation_request_boundary_report_v1.json",
        "metrics": "task_observation_request_metrics_candidate_report_v1.json",
        "benchmark_link": "task_observation_request_benchmark_link_report_v1.json",
        "health_report": "task_observation_request_system_health_report_v1.json",
        "no_write": "task_observation_request_no_write_boundary_report_v1.json",
        "sim_report": "task_observation_request_simulation_context_report_v1.json",
        "non_claims": "task_observation_request_non_claims_report_v1.json",
        "followups": "task_observation_request_open_followups_v1.json",
        "audit": "task_observation_request_audit_report_v1.json",
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
            root / "task_observation_request_verifier_report_v1.json",
            {"verdict": "NO_GO", "blockers": blockers},
        )
        print(json.dumps({"verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    s = data["summary"]
    ok(s.get("contract_scope") == "task_observation_request_contract_only", "scope")
    ok(s.get("based_on_basic_loop_audit_correction") is True, "audit")
    ok(s.get("observation_request_contract_defined") is True, "contract_def")
    ok(s.get("observation_request_schema_defined") is True, "schema_def")
    ok(s.get("baseline_safety_request_policy_defined") is True, "baseline_pol")
    ok(s.get("task_driven_request_policy_defined") is True, "td_pol")
    ok(s.get("target_module_routing_policy_defined") is True, "routing_pol")
    ok(s.get("request_gate_policy_defined") is True, "gate_pol")
    ok(s.get("priority_timing_policy_defined") is True, "ptf_pol")
    ok(s.get("vision_ocr_ingest_handoff_defined") is True, "handoff_def")
    ok(s.get("camera_invoked") is False, "no_camera")
    ok(s.get("ocr_invoked") is False, "no_ocr")
    ok(s.get("detector_invoked") is False, "no_detector")

    schema = data["schema"]
    fields = schema.get("field_definitions") or {}
    sources = (fields.get("request_source") or {}).get("values") or []
    types = (fields.get("request_type") or {}).get("values") or []
    ok("baseline_safety_loop" in sources, "src_baseline")
    ok("task_manager_action_schedule" in sources, "src_tm")
    ok("observe_forward_path" in types, "type_forward")
    ok("observe_readable_region" in types, "type_readable")

    sp = data["source_policy"]
    ok(sp.get("baseline_safety_loop_can_generate_request_without_task") is True, "baseline_no_task")
    ok(sp.get("voice_cannot_generate_observation_request_directly") is True, "voice_no_req")

    bp = data["baseline_policy"]
    ok(bp.get("baseline_safety_request_allowed_without_task") is True, "baseline_allowed")
    ok(bp.get("generic_text_observation_forbidden_without_task") is True, "no_generic_text")

    tdp = data["task_driven_policy"]
    ok(tdp.get("task_driven_request_requires_task_context") is True, "td_ctx")
    ok(tdp.get("ocr_target_requires_ocr_activation_gate") is True, "ocr_gate_req")

    routes = data["routing_policy"].get("routes") or []
    mods = {r.get("target_module") for r in routes}
    ok("vision" in mods, "route_vision")
    ok("ocr_if_task_required" in mods, "route_ocr")

    ok(data["gate_policy"].get("request_allowed_now") is False, "gate_not_now")

    ptf = data["ptf_policy"]
    ok(ptf.get("safety_priority_above_task") is True, "ptf_safety")

    coll = data["candidates"]
    ok(coll.get("observation_request_candidate_count", 0) >= 16, "count_16")
    ok(coll.get("baseline_request_candidate_count", 0) >= 4, "baseline_4")
    ok(coll.get("task_driven_request_candidate_count", 0) >= 12, "td_12")
    ok(coll.get("request_allowed_now_count") == 0, "allowed_now_0")
    cands = coll.get("candidates") or []
    ok(all(c.get("request_allowed_now") is False for c in cands), "cand_not_now")
    ok(all(c.get("camera_invoked_now") is False for c in cands), "cand_no_camera")
    ok(all(c.get("ocr_invoked_now") is False for c in cands), "cand_no_ocr")

    ocr_sp = data["ocr_subpolicy"]
    ok(ocr_sp.get("generic_environment_ocr_forbidden") is True, "ocr_no_generic")
    ok(ocr_sp.get("ocr_invoked_now") is False, "ocr_sp_not_invoked")

    guid = data["guidance_subpolicy"]
    ok(guid.get("direct_tts_bypass_forbidden") is True, "no_tts_bypass")

    human = data["human_subpolicy"]
    ok(human.get("confirmation_required") is True, "human_confirm")

    handoff = data["handoff"]
    ok(handoff.get("handoff_target_phase") == "Vision-OCR-Evidence-Ingest-Integration-Check-v1", "handoff_phase")

    lc = data["lifecycle_policy"]
    ok(lc.get("request_not_executed_in_this_phase") is True, "lc_not_exec")

    sep = data["separation_matrix"]
    ok(sep.get("safety_priority_above_task") is True, "sep_safety")

    final = data["final"]
    ok(
        final.get("final_decision") == "TASK_OBSERVATION_REQUEST_CONTRACT_READY_FOR_VISION_OCR_INGEST",
        "final_decision",
    )
    ok(final.get("recommended_next_phase") == "Vision-OCR-Evidence-Ingest-Integration-Check-v1", "next_phase")

    ok(data["boundary"].get("contract_only") is True, "contract_only")
    ok(data["metrics"].get("no_write_boundary_pass_rate") == 1.0, "nw_rate")
    ok(data["health_report"].get("no_runtime_health_claim") is True, "no_health")
    ok(data["no_write"].get("boundary_ok") is True, "nw_ok")
    ok(data["no_write"].get("violations") == [], "nw_violations")
    ok(data["sim_report"].get("simulation_profile_id") == "developer_full", "sim")
    ok(data["audit"].get("midplatform_fact_written") is False, "audit_no_fact")

    verdict = "GO" if not blockers else "NO_GO"
    report = {
        "verdict": verdict,
        "checks_passed": checks,
        "checks_expected": 74,
        "blockers": blockers,
        "final_decision": final.get("final_decision"),
        "phase": "Task-Observation-Request-Contract-v1-001",
    }
    _write_json(root / "task_observation_request_verifier_report_v1.json", report)
    print(json.dumps(report, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
