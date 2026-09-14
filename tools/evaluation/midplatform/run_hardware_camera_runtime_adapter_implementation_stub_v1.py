#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-Hardware-Camera-Runtime-Adapter-Implementation-Stub-v1-001 runner."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

WRITES = [
    ("hardware_camera_runtime_adapter_implementation_stub_v1_summary.json", "summary"),
    ("hardware_camera_adapter_stub_input_intake_matrix_v1.json", "intake"),
    ("hardware_camera_adapter_method_stub_response_matrix_v1.json", "method_matrix"),
    ("hardware_camera_adapter_capability_report_stub_v1.json", "capability_stub"),
    ("hardware_camera_adapter_health_status_stub_v1.json", "health_stub"),
    ("hardware_camera_adapter_frame_capture_stub_response_v1.json", "frame_stub"),
    ("hardware_camera_adapter_error_mapping_stub_v1.json", "error_mapping"),
    ("hardware_camera_adapter_stub_ocrrequest_gate_link_v1.json", "ocr_gate"),
    ("hardware_camera_adapter_stub_guardedtrial_readiness_link_v1.json", "guardedtrial_link"),
    ("hardware_camera_adapter_stub_long_term_candidate_link_v1.json", "long_term"),
    ("hardware_camera_adapter_stub_decision_trace_v1.json", "trace"),
    ("hardware_camera_adapter_stub_final_decision_v1.json", "final"),
    ("hardware_camera_adapter_stub_boundary_report_v1.json", "boundary"),
    ("hardware_camera_adapter_stub_metrics_candidate_report_v1.json", "metrics"),
    ("hardware_camera_adapter_stub_benchmark_link_report_v1.json", "benchmark_link"),
    ("hardware_camera_adapter_stub_system_health_report_v1.json", "health_report"),
    ("hardware_camera_adapter_stub_no_write_boundary_report_v1.json", "no_write"),
    ("hardware_camera_adapter_stub_simulation_context_report_v1.json", "sim_report"),
    ("hardware_camera_adapter_stub_non_claims_report_v1.json", "non_claims"),
    ("hardware_camera_adapter_stub_open_followups_v1.json", "followups"),
    ("hardware_camera_adapter_stub_audit_report_v1.json", "audit"),
]


def _find_ws_root() -> Path:
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "capabilities" / "midplatform").is_dir():
            return parent
    return here.parents[3]


WS_ROOT = _find_ws_root()
if str(WS_ROOT) not in sys.path:
    sys.path.insert(0, str(WS_ROOT))


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
    ap.add_argument("--output-root", required=True)
    ap.add_argument("--adapter-contract-root", required=True)
    ap.add_argument("--hardware-profile-registry-root", required=True)
    ap.add_argument("--hardware-runtime-root", required=True)
    ap.add_argument("--hardware-contract-root", required=True)
    ap.add_argument("--rrd-runtime-root", required=True)
    ap.add_argument("--benchmark-smoke-root", required=True)
    ap.add_argument("--system-health-root", required=True)
    ap.add_argument("--simulation-root", required=True)
    args = ap.parse_args()

    out = _require_abs(args.output_root, "--output-root")
    out.mkdir(parents=True, exist_ok=True)

    from capabilities.midplatform.hardware_camera_runtime_adapter_implementation_stub_v1 import (
        run_hardware_camera_runtime_adapter_implementation_stub_v1,
    )

    result = run_hardware_camera_runtime_adapter_implementation_stub_v1(
        adapter_contract_root=str(_require_abs(args.adapter_contract_root, "contract")),
        hardware_profile_registry_root=str(_require_abs(args.hardware_profile_registry_root, "registry")),
        hardware_runtime_root=str(_require_abs(args.hardware_runtime_root, "hw_rt")),
        hardware_contract_root=str(_require_abs(args.hardware_contract_root, "hw_contract")),
        rrd_runtime_root=str(_require_abs(args.rrd_runtime_root, "rrd")),
        benchmark_smoke_root=str(_require_abs(args.benchmark_smoke_root, "bench")),
        system_health_root=str(_require_abs(args.system_health_root, "health")),
        simulation_root=str(_require_abs(args.simulation_root, "sim")),
        workspace_root=str(WS_ROOT),
    )

    for fname, key in WRITES:
        _write_json(out / fname, result[key])

    stub_path = WS_ROOT / "capabilities/midplatform/hardware_camera_runtime_adapter_stub_v1.py"
    (out / "hardware_camera_adapter_stub_notes.md").write_text(
        "# Hardware Camera Runtime Adapter Stub v1\n\n"
        f"Stub module: `{stub_path}`\n\n"
        "9 methods invoked in smoke; no real camera; STUB_READY_SOFTWARE_BOUNDARY_CLOSED.\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "output_root": str(out),
                "stub_module": str(stub_path),
                "phase_verdict_hint": result["summary"].get("phase_verdict_hint"),
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
