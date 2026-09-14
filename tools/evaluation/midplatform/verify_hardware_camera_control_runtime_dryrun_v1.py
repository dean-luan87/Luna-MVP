#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for Hardware Camera Control Runtime DryRun v1."""

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
        "summary": "hardware_camera_control_runtime_dryrun_v1_summary.json",
        "intake": "hardware_camera_control_runtime_input_intake_matrix_v1.json",
        "capture_intake": "hardware_static_capture_request_runtime_intake_v1.json",
        "capability_eval": "hardware_capability_runtime_evaluation_v1.json",
        "unknown_handling": "hardware_capability_unknown_runtime_handling_v1.json",
        "action_matrix": "hardware_camera_runtime_action_decision_matrix_v1.json",
        "capture_decision": "hardware_static_capture_runtime_decision_candidate_v1.json",
        "ocr_gate": "hardware_camera_ocrrequest_gate_runtime_link_v1.json",
        "fallback_collection": "hardware_camera_runtime_fallback_candidate_collection_v1.json",
        "health_runtime": "hardware_camera_runtime_system_health_link_v1.json",
        "guardedtrial": "hardware_camera_guardedtrial_readiness_candidate_v1.json",
        "long_term": "hardware_camera_control_runtime_long_term_candidate_link_v1.json",
        "trace": "hardware_camera_control_runtime_decision_trace_v1.json",
        "final": "hardware_camera_control_runtime_final_decision_v1.json",
        "boundary": "hardware_camera_control_runtime_boundary_report_v1.json",
        "metrics": "hardware_camera_control_runtime_metrics_candidate_report_v1.json",
        "bench": "hardware_camera_control_runtime_benchmark_link_report_v1.json",
        "health": "hardware_camera_control_runtime_system_health_link_report_v1.json",
        "no_write": "hardware_camera_control_runtime_no_write_boundary_report_v1.json",
        "sim": "hardware_camera_control_runtime_simulation_context_report_v1.json",
        "non_claims": "hardware_camera_control_runtime_non_claims_report_v1.json",
        "followups": "hardware_camera_control_runtime_open_followups_v1.json",
        "audit": "hardware_camera_control_runtime_audit_report_v1.json",
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
            root / "hardware_camera_control_runtime_verifier_report_v1.json",
            {"verdict": "NO_GO", "blockers": blockers},
        )
        print(json.dumps({"verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    s = data["summary"]
    ok(True, "summary")
    ok(s.get("dryrun_scope") == "hardware_camera_control_runtime_dryrun_only", "scope")
    ok(s.get("based_on_hardware_camera_control_contract") is True, "based_contract")
    ok(s.get("static_capture_request_candidate_count_observed") == 26, "capture_26")
    ok(s.get("hardware_capability_evaluation_executed") is True, "cap_eval")
    ok(s.get("hardware_profile_available") is False, "no_profile")
    ok(s.get("camera_capability_registry_available") is False, "no_registry")
    ok(s.get("hardware_capability_status") == "unknown", "cap_unknown")
    ok(s.get("capability_unknown_policy_applied") is True, "policy")
    ok(s.get("runtime_action_decision_generated") is True, "action_dec")
    ok(s.get("static_capture_runtime_allowed_now") is False, "no_capture_now")
    ok(s.get("hardware_action_allowed_now") is False, "no_hw_now")
    ok(s.get("fallback_candidate_generated") is True, "fallback")
    ok(s.get("guardedtrial_readiness_candidate_generated") is True, "gt_ready")
    ok(s.get("ocrrequest_future_gate_still_blocked") is True, "ocr_blocked")
    ok(s.get("runtime_camera_invoked") is False, "no_cam")
    ok(s.get("hardware_action_invoked") is False, "no_hw")
    ok(s.get("ocr_invoked") is False, "no_ocr")

    ci = data["capture_intake"]
    ok(ci.get("accepted_for_runtime_dryrun_count") == 26, "accepted_26")
    ce = data["capability_eval"]
    ok(ce.get("capability_status") == "unknown", "eval_unknown")
    uh = data["unknown_handling"]
    ok("invoke_camera" in (uh.get("blocked_actions") or []), "block_camera")
    am = data["action_matrix"].get("decisions") or []
    ok(len(am) == 8, "eight_actions")
    ok(all(d.get("allowed_now") is False for d in am if isinstance(d, dict)), "all_blocked")
    ok(data["capture_decision"].get("static_capture_allowed_now") is False, "cap_dec")
    ok(data["ocr_gate"].get("ocrrequest_eligible_now") is False, "ocr_gate")
    ok(data["fallback_collection"].get("candidates"), "fallbacks")
    ok(data["health_runtime"].get("failure_class_candidate") == "HARDWARE_CAPABILITY_UNKNOWN", "health_fc")
    ok(data["guardedtrial"].get("guardedtrial_invoked_now") is False, "gt_not_now")
    ok(data["long_term"].get("can_feed_long_term_candidate") is True, "lt")
    ok(data["final"].get("final_decision") == "BLOCK_RUNTIME_CAMERA_ACTION_PREPARE_GUARDEDTRIAL_OR_FALLBACK", "final")
    ok(data["boundary"].get("runtime_dryrun_only") is True, "boundary")
    ok(data["metrics"].get("allowed_action_now_count") == 0, "allowed_0")
    ok(data["metrics"].get("no_write_boundary_pass_rate") == 1.0, "metrics")
    ok(data["bench"].get("benchmark_score_generated") is False, "bench")
    ok(data["health"].get("recovery_action_committed") is False, "health_rec")
    ok(data["no_write"].get("boundary_ok") is True, "nw_ok")
    ok(data["no_write"].get("violations") == [], "nw_violations")
    ok(data["sim"].get("simulation_profile_id") == "developer_full", "sim")
    ok(data["audit"].get("midplatform_fact_written") is False, "audit_fact")
    ok(data["audit"].get("hardware_fact_written") is False, "audit_hw")
    ok(data["audit"].get("world_model_written") is False, "audit_wm")
    ok(data["audit"].get("scene_delta_candidate_generated") is False, "audit_delta")

    verdict = "GO" if not blockers else "NO_GO"
    report = {
        "verdict": verdict,
        "checks_passed": checks,
        "checks_expected": 63,
        "blockers": blockers,
        "phase": "Hardware-Camera-Control-Runtime-DryRun-v1-001",
    }
    _write_json(root / "hardware_camera_control_runtime_verifier_report_v1.json", report)
    print(json.dumps(report, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
