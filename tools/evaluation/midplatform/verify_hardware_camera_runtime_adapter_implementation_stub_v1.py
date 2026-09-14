#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for Hardware Camera Runtime Adapter Implementation Stub v1."""

from __future__ import annotations

import argparse
import importlib.util
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


def _find_ws_root() -> Path:
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "capabilities" / "midplatform").is_dir():
            return parent
    return here.parents[3]


def _method_row(matrix: Dict[str, Any], name: str) -> Dict[str, Any]:
    for r in matrix.get("methods") or []:
        if isinstance(r, dict) and r.get("method_name") == name:
            return r
    return {}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke-root", required=True)
    args = ap.parse_args()

    root = _require_abs(args.smoke_root, "--smoke-root")
    ws = _find_ws_root()
    blockers: List[str] = []
    checks = 0

    def ok(c: bool, name: str) -> None:
        nonlocal checks
        if c:
            checks += 1
        else:
            blockers.append(name)

    files = {
        "summary": "hardware_camera_runtime_adapter_implementation_stub_v1_summary.json",
        "intake": "hardware_camera_adapter_stub_input_intake_matrix_v1.json",
        "method_matrix": "hardware_camera_adapter_method_stub_response_matrix_v1.json",
        "capability_stub": "hardware_camera_adapter_capability_report_stub_v1.json",
        "health_stub": "hardware_camera_adapter_health_status_stub_v1.json",
        "frame_stub": "hardware_camera_adapter_frame_capture_stub_response_v1.json",
        "error_mapping": "hardware_camera_adapter_error_mapping_stub_v1.json",
        "ocr_gate": "hardware_camera_adapter_stub_ocrrequest_gate_link_v1.json",
        "guardedtrial_link": "hardware_camera_adapter_stub_guardedtrial_readiness_link_v1.json",
        "long_term": "hardware_camera_adapter_stub_long_term_candidate_link_v1.json",
        "trace": "hardware_camera_adapter_stub_decision_trace_v1.json",
        "final": "hardware_camera_adapter_stub_final_decision_v1.json",
        "boundary": "hardware_camera_adapter_stub_boundary_report_v1.json",
        "metrics": "hardware_camera_adapter_stub_metrics_candidate_report_v1.json",
        "bench": "hardware_camera_adapter_stub_benchmark_link_report_v1.json",
        "health": "hardware_camera_adapter_stub_system_health_report_v1.json",
        "no_write": "hardware_camera_adapter_stub_no_write_boundary_report_v1.json",
        "sim": "hardware_camera_adapter_stub_simulation_context_report_v1.json",
        "non_claims": "hardware_camera_adapter_stub_non_claims_report_v1.json",
        "followups": "hardware_camera_adapter_stub_open_followups_v1.json",
        "audit": "hardware_camera_adapter_stub_audit_report_v1.json",
    }
    data: Dict[str, Any] = {}
    for k, f in files.items():
        p = root / f
        if not p.is_file():
            blockers.append(f"missing:{k}")
        else:
            data[k] = json.loads(p.read_text(encoding="utf-8"))

    stub_py = ws / "capabilities/midplatform/hardware_camera_runtime_adapter_stub_v1.py"
    if not stub_py.is_file():
        blockers.append("missing:stub_module")
    else:
        ok(True, "stub_file")

    if blockers and "stub_file" not in str(blockers):
        _write_json(
            root / "hardware_camera_adapter_stub_verifier_report_v1.json",
            {"verdict": "NO_GO", "blockers": blockers},
        )
        print(json.dumps({"verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    s = data["summary"]
    mm = data["method_matrix"]
    ok(True, "summary")
    ok(s.get("stub_scope") == "hardware_camera_runtime_adapter_stub_only", "scope")
    ok(s.get("based_on_adapter_contract") is True, "based_contract")
    ok(s.get("adapter_stub_implemented") is True, "stub_impl")
    ok(s.get("required_methods_implemented_as_stub") is True, "methods_stub")
    ok(s.get("required_method_count_observed") == 9, "count_9")
    ok(s.get("adapter_implementation_real") is False, "not_real")
    ok(s.get("real_camera_enabled") is False, "no_cam")
    ok(s.get("hardware_probe_invoked") is False, "no_probe")
    ok(s.get("runtime_camera_invoked") is False, "no_rt_cam")
    ok(s.get("runtime_frame_captured") is False, "no_frame")
    ok(s.get("hardware_action_invoked") is False, "no_hw")
    ok(s.get("ocr_invoked") is False, "no_ocr")

    methods = mm.get("methods") or []
    ok(len(methods) == 9, "nine_methods")
    ok(all(r.get("invoked_in_smoke") is True for r in methods if isinstance(r, dict)), "all_invoked")
    ok(all(r.get("real_hardware_called") is False for r in methods if isinstance(r, dict)), "no_real_hw")
    ok(_method_row(mm, "capture_frame").get("response_status") == "not_captured", "cap_not_captured")
    ok(_method_row(mm, "get_capability_report").get("response_status") == "unknown", "cap_unknown")

    ok(data["health_stub"].get("health_status_stub_generated") is True, "health_stub")
    ok(data["capability_stub"].get("capability_report_stub_generated") is True, "cap_stub")
    ok(data["frame_stub"].get("frame_ref") is None, "frame_null")
    ok("ADAPTER_STUB_ONLY" in (data["error_mapping"].get("error_codes_used") or []), "err_stub")
    ok(data["ocr_gate"].get("ocrrequest_eligible_now") is False, "ocr_not_now")
    gt = data["guardedtrial_link"]
    ok(gt.get("guardedtrial_allowed_now") is False, "gt_not_now")
    ok("real_adapter_missing" in (gt.get("current_blockers") or []), "real_adapter_blocker")
    ok(data["long_term"].get("can_feed_long_term_candidate") is True, "lt")
    ok(data["final"].get("final_decision") == "STUB_READY_SOFTWARE_BOUNDARY_CLOSED", "final")
    ok(data["boundary"].get("adapter_stub_only") is True, "boundary")
    ok(data["metrics"].get("implemented_stub_method_count") == 9, "metric_9")
    ok(data["metrics"].get("real_hardware_call_count") == 0, "real_hw_0")
    ok(data["metrics"].get("no_write_boundary_pass_rate") == 1.0, "metrics")
    ok(data["bench"].get("benchmark_score_generated") is False, "bench")
    ok(data["health"].get("failure_class_candidate") == "ADAPTER_STUB_ONLY", "health_fc")
    ok(data["no_write"].get("boundary_ok") is True, "nw_ok")
    ok(data["no_write"].get("violations") == [], "nw_violations")
    ok(data["sim"].get("simulation_profile_id") == "developer_full", "sim")
    ok(data["audit"].get("midplatform_fact_written") is False, "audit_fact")
    ok(data["audit"].get("hardware_fact_written") is False, "audit_hw")
    ok(data["audit"].get("world_model_written") is False, "audit_wm")

    if stub_py.is_file():
        spec = importlib.util.spec_from_file_location("hw_stub", stub_py)
        if spec and spec.loader:
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            for name in mod.METHOD_NAMES:
                ok(hasattr(mod, name) and callable(getattr(mod, name)), f"fn_{name}")

    verdict = "GO" if not blockers else "NO_GO"
    report = {
        "verdict": verdict,
        "checks_passed": checks,
        "checks_expected": 61,
        "blockers": blockers,
        "phase": "Hardware-Camera-Runtime-Adapter-Implementation-Stub-v1-001",
        "stub_module": str(stub_py),
    }
    _write_json(root / "hardware_camera_adapter_stub_verifier_report_v1.json", report)
    print(json.dumps(report, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
