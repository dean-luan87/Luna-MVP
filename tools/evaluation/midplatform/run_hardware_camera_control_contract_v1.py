#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-Hardware-Camera-Control-Contract-v1-001 runner."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

WRITES = [
    ("hardware_camera_control_contract_v1_summary.json", "summary"),
    ("hardware_camera_control_input_intake_matrix_v1.json", "intake"),
    ("hardware_camera_control_request_schema_v1.json", "request_schema"),
    ("hardware_capability_report_schema_v1.json", "capability_schema"),
    ("hardware_camera_control_action_matrix_v1.json", "action_matrix"),
    ("hardware_static_capture_request_candidate_collection_v1.json", "capture_collection"),
    ("hardware_capability_unknown_unsupported_policy_v1.json", "unknown_policy"),
    ("hardware_camera_failure_fallback_policy_v1.json", "fallback_policy"),
    ("hardware_camera_system_health_link_policy_v1.json", "health_link_policy"),
    ("hardware_static_capture_to_ocrrequest_future_gate_link_v1.json", "ocr_gate_link"),
    ("hardware_camera_guardedtrial_handoff_policy_v1.json", "guardedtrial"),
    ("hardware_camera_control_long_term_candidate_link_v1.json", "long_term"),
    ("hardware_camera_control_contract_decision_trace_v1.json", "trace"),
    ("hardware_camera_control_contract_final_decision_v1.json", "final"),
    ("hardware_camera_control_boundary_report_v1.json", "boundary"),
    ("hardware_camera_control_metrics_candidate_report_v1.json", "metrics"),
    ("hardware_camera_control_benchmark_link_report_v1.json", "benchmark_link"),
    ("hardware_camera_control_system_health_link_report_v1.json", "health_link_report"),
    ("hardware_camera_control_no_write_boundary_report_v1.json", "no_write"),
    ("hardware_camera_control_simulation_context_report_v1.json", "sim_report"),
    ("hardware_camera_control_non_claims_report_v1.json", "non_claims"),
    ("hardware_camera_control_open_followups_v1.json", "followups"),
    ("hardware_camera_control_audit_report_v1.json", "audit"),
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
    ap.add_argument("--rrd-runtime-root", required=True)
    ap.add_argument("--isrc-runtime-root", required=True)
    ap.add_argument("--assisted-static-reading-runtime-root", required=True)
    ap.add_argument("--assisted-static-reading-mode-root", required=True)
    ap.add_argument("--vision-capture-governance-root", required=True)
    ap.add_argument("--vision-capture-runtime-root", required=True)
    ap.add_argument("--ocr-activation-root", required=True)
    ap.add_argument("--stc-sampling-guidance-root", required=True)
    ap.add_argument("--benchmark-smoke-root", required=True)
    ap.add_argument("--system-health-root", required=True)
    ap.add_argument("--simulation-root", required=True)
    args = ap.parse_args()

    out = _require_abs(args.output_root, "--output-root")
    out.mkdir(parents=True, exist_ok=True)

    from capabilities.midplatform.hardware_camera_control_contract_v1 import (
        run_hardware_camera_control_contract_v1,
    )

    result = run_hardware_camera_control_contract_v1(
        rrd_runtime_root=str(_require_abs(args.rrd_runtime_root, "rrd")),
        isrc_runtime_root=str(_require_abs(args.isrc_runtime_root, "isrc")),
        assisted_static_reading_runtime_root=str(_require_abs(args.assisted_static_reading_runtime_root, "assisted_rt")),
        assisted_static_reading_mode_root=str(_require_abs(args.assisted_static_reading_mode_root, "assisted_mode")),
        vision_capture_governance_root=str(_require_abs(args.vision_capture_governance_root, "vision_gov")),
        vision_capture_runtime_root=str(_require_abs(args.vision_capture_runtime_root, "vision_rt")),
        ocr_activation_root=str(_require_abs(args.ocr_activation_root, "ocr_act")),
        stc_sampling_guidance_root=str(_require_abs(args.stc_sampling_guidance_root, "stc")),
        benchmark_smoke_root=str(_require_abs(args.benchmark_smoke_root, "bench")),
        system_health_root=str(_require_abs(args.system_health_root, "health")),
        simulation_root=str(_require_abs(args.simulation_root, "sim")),
        workspace_root=str(WS_ROOT),
    )

    for fname, key in WRITES:
        _write_json(out / fname, result[key])

    (out / "hardware_camera_control_notes.md").write_text(
        "# Hardware Camera Control Contract v1\n\n"
        "Contract-only: 26 static capture request candidates; no camera/zoom/autofocus/OCR.\n",
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
