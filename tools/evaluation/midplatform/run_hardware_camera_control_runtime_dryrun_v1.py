#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-Hardware-Camera-Control-Runtime-DryRun-v1-001 runner."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

WRITES = [
    ("hardware_camera_control_runtime_dryrun_v1_summary.json", "summary"),
    ("hardware_camera_control_runtime_input_intake_matrix_v1.json", "intake"),
    ("hardware_static_capture_request_runtime_intake_v1.json", "capture_intake"),
    ("hardware_capability_runtime_evaluation_v1.json", "capability_eval"),
    ("hardware_capability_unknown_runtime_handling_v1.json", "unknown_handling"),
    ("hardware_camera_runtime_action_decision_matrix_v1.json", "action_matrix"),
    ("hardware_static_capture_runtime_decision_candidate_v1.json", "capture_decision"),
    ("hardware_camera_ocrrequest_gate_runtime_link_v1.json", "ocr_gate"),
    ("hardware_camera_runtime_fallback_candidate_collection_v1.json", "fallback_collection"),
    ("hardware_camera_runtime_system_health_link_v1.json", "health_runtime"),
    ("hardware_camera_guardedtrial_readiness_candidate_v1.json", "guardedtrial"),
    ("hardware_camera_control_runtime_long_term_candidate_link_v1.json", "long_term"),
    ("hardware_camera_control_runtime_decision_trace_v1.json", "trace"),
    ("hardware_camera_control_runtime_final_decision_v1.json", "final"),
    ("hardware_camera_control_runtime_boundary_report_v1.json", "boundary"),
    ("hardware_camera_control_runtime_metrics_candidate_report_v1.json", "metrics"),
    ("hardware_camera_control_runtime_benchmark_link_report_v1.json", "benchmark_link"),
    ("hardware_camera_control_runtime_system_health_link_report_v1.json", "health_link_report"),
    ("hardware_camera_control_runtime_no_write_boundary_report_v1.json", "no_write"),
    ("hardware_camera_control_runtime_simulation_context_report_v1.json", "sim_report"),
    ("hardware_camera_control_runtime_non_claims_report_v1.json", "non_claims"),
    ("hardware_camera_control_runtime_open_followups_v1.json", "followups"),
    ("hardware_camera_control_runtime_audit_report_v1.json", "audit"),
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
    ap.add_argument("--hardware-contract-root", required=True)
    ap.add_argument("--rrd-runtime-root", required=True)
    ap.add_argument("--vision-capture-governance-root", required=True)
    ap.add_argument("--vision-capture-runtime-root", required=True)
    ap.add_argument("--assisted-static-reading-runtime-root", required=True)
    ap.add_argument("--benchmark-smoke-root", required=True)
    ap.add_argument("--system-health-root", required=True)
    ap.add_argument("--simulation-root", required=True)
    args = ap.parse_args()

    out = _require_abs(args.output_root, "--output-root")
    out.mkdir(parents=True, exist_ok=True)

    from capabilities.midplatform.hardware_camera_control_runtime_dryrun_v1 import (
        run_hardware_camera_control_runtime_dryrun_v1,
    )

    result = run_hardware_camera_control_runtime_dryrun_v1(
        hardware_contract_root=str(_require_abs(args.hardware_contract_root, "contract")),
        rrd_runtime_root=str(_require_abs(args.rrd_runtime_root, "rrd")),
        vision_capture_governance_root=str(_require_abs(args.vision_capture_governance_root, "vision_gov")),
        vision_capture_runtime_root=str(_require_abs(args.vision_capture_runtime_root, "vision_rt")),
        assisted_static_reading_runtime_root=str(_require_abs(args.assisted_static_reading_runtime_root, "assisted_rt")),
        benchmark_smoke_root=str(_require_abs(args.benchmark_smoke_root, "bench")),
        system_health_root=str(_require_abs(args.system_health_root, "health")),
        simulation_root=str(_require_abs(args.simulation_root, "sim")),
        workspace_root=str(WS_ROOT),
    )

    for fname, key in WRITES:
        _write_json(out / fname, result[key])

    (out / "hardware_camera_control_runtime_notes.md").write_text(
        "# Hardware Camera Control Runtime DryRun v1\n\n"
        "Hardware unknown: block all actions; 26 requests preserved; fallback + guardedtrial later.\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {"output_root": str(out), "phase_verdict_hint": result["summary"].get("phase_verdict_hint")},
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
