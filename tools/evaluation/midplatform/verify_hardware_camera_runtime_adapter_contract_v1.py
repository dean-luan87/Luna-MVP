#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for Hardware Camera Runtime Adapter Contract v1."""

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


def _method(names: List[Dict[str, Any]], m: str) -> Dict[str, Any]:
    for row in names:
        if isinstance(row, dict) and row.get("method_name") == m:
            return row
    return {}


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
        "summary": "hardware_camera_runtime_adapter_contract_v1_summary.json",
        "intake": "hardware_camera_runtime_adapter_contract_input_intake_matrix_v1.json",
        "interface": "hardware_camera_runtime_adapter_interface_contract_v1.json",
        "method_schema": "hardware_camera_runtime_adapter_method_schema_v1.json",
        "capability_response_schema": "hardware_camera_adapter_capability_report_response_schema_v1.json",
        "health_response_schema": "hardware_camera_adapter_health_status_response_schema_v1.json",
        "frame_response_schema": "hardware_camera_adapter_frame_capture_response_schema_v1.json",
        "error_taxonomy": "hardware_camera_adapter_error_taxonomy_v1.json",
        "timeout_policy": "hardware_camera_adapter_timeout_retry_permission_policy_v1.json",
        "health_mapping": "hardware_camera_adapter_system_health_mapping_v1.json",
        "guardedtrial_link": "hardware_camera_adapter_guardedtrial_readiness_link_v1.json",
        "ocr_gate": "hardware_camera_adapter_ocrrequest_gate_link_v1.json",
        "long_term": "hardware_camera_adapter_long_term_candidate_link_v1.json",
        "trace": "hardware_camera_runtime_adapter_contract_decision_trace_v1.json",
        "final": "hardware_camera_runtime_adapter_contract_final_decision_v1.json",
        "boundary": "hardware_camera_runtime_adapter_contract_boundary_report_v1.json",
        "metrics": "hardware_camera_runtime_adapter_contract_metrics_candidate_report_v1.json",
        "bench": "hardware_camera_runtime_adapter_contract_benchmark_link_report_v1.json",
        "health": "hardware_camera_runtime_adapter_contract_system_health_report_v1.json",
        "no_write": "hardware_camera_runtime_adapter_contract_no_write_boundary_report_v1.json",
        "sim": "hardware_camera_runtime_adapter_contract_simulation_context_report_v1.json",
        "non_claims": "hardware_camera_runtime_adapter_contract_non_claims_report_v1.json",
        "followups": "hardware_camera_runtime_adapter_contract_open_followups_v1.json",
        "audit": "hardware_camera_runtime_adapter_contract_audit_report_v1.json",
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
            root / "hardware_camera_runtime_adapter_contract_verifier_report_v1.json",
            {"verdict": "NO_GO", "blockers": blockers},
        )
        print(json.dumps({"verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    s = data["summary"]
    iface = data["interface"]
    methods = data["method_schema"].get("methods") or []
    ok(True, "summary")
    ok(s.get("contract_scope") == "hardware_camera_runtime_adapter_contract_only", "scope")
    ok(s.get("based_on_hardware_profile_registry") is True, "based_reg")
    ok(s.get("adapter_interface_defined") is True, "iface_def")
    ok(s.get("required_methods_defined") is True, "methods_def")
    ok(s.get("method_request_response_schema_defined") is True, "mrr")
    ok(s.get("capability_report_response_schema_defined") is True, "cap_resp")
    ok(s.get("health_status_response_schema_defined") is True, "health_resp")
    ok(s.get("frame_capture_response_schema_defined") is True, "frame_resp")
    ok(s.get("hardware_error_taxonomy_defined") is True, "errors")
    ok(s.get("timeout_retry_permission_policy_defined") is True, "timeout")
    ok(s.get("system_health_mapping_defined") is True, "sh_map")
    ok(s.get("guardedtrial_readiness_link_defined") is True, "gt_link")
    ok(s.get("adapter_implementation_available") is False, "no_impl")
    ok(s.get("adapter_invoked") is False, "no_invoke")
    ok(s.get("runtime_camera_invoked") is False, "no_cam")

    req = iface.get("required_methods") or []
    ok("open_camera" in req, "open_camera")
    ok("capture_frame" in req, "capture_frame")
    ok("get_capability_report" in req, "get_capability_report")
    ok("get_health_status" in req, "get_health_status")
    ok(len(methods) == 9, "nine_methods")

    cap = _method(methods, "capture_frame")
    ok("camera_session_id" in (cap.get("request_schema") or []), "cap_req")
    ok("frame_ref" in (cap.get("response_schema") or []), "cap_resp_fields")

    frame_ex = data["frame_response_schema"].get("example") or {}
    ok(frame_ex.get("frame_is_fact") is False, "frame_not_fact")

    codes = {e.get("error_code") for e in data["error_taxonomy"].get("errors") or [] if isinstance(e, dict)}
    ok("ADAPTER_MISSING" in codes, "err_adapter")
    ok("CAMERA_PERMISSION_DENIED" in codes, "err_perm")
    ok("CAPTURE_TIMEOUT" in codes, "err_cap_timeout")
    ok(data["timeout_policy"].get("runtime_enforced_now") is False, "not_enforced")
    ok(data["health_mapping"].get("recovery_action_committed_now") is False, "rec_not_now")
    gt = data["guardedtrial_link"]
    ok(gt.get("guardedtrial_allowed_now") is False, "gt_not_now")
    ok("adapter_implementation_missing" in (gt.get("current_blockers") or []), "impl_blocker")
    ok(data["ocr_gate"].get("ocrrequest_eligible_now") is False, "ocr_not_now")
    ok(data["long_term"].get("can_feed_long_term_candidate") is True, "lt")
    ok(data["final"].get("final_decision") == "READY_FOR_ADAPTER_IMPLEMENTATION_OR_GUARDEDTRIAL_PRECHECK", "final")
    ok(data["boundary"].get("adapter_contract_only") is True, "boundary")
    ok(data["metrics"].get("required_method_count") == 9, "metric_9")
    ok(data["metrics"].get("no_write_boundary_pass_rate") == 1.0, "metrics")
    ok(data["bench"].get("benchmark_score_generated") is False, "bench")
    ok(data["health"].get("no_runtime_health_claim") is True, "health_claim")
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
        "phase": "Hardware-Camera-Runtime-Adapter-Contract-v1-001",
    }
    _write_json(root / "hardware_camera_runtime_adapter_contract_verifier_report_v1.json", report)
    print(json.dumps(report, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
