#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-OCR-StaticReading-Poster-RealVideo-Regression-RouteCompliance-v1-001 runner."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

WRITES = [
    ("ocr_staticreading_poster_realvideo_regression_route_compliance_v1_summary.json", "summary"),
    ("ocr_regression_route_compliance_input_intake_matrix_v1.json", "intake"),
    ("ocr_regression_route_compliance_matrix_v1.json", "route_matrix"),
    ("ocr_regression_realvideo_route_check_v1.json", "realvideo_check"),
    ("ocr_regression_poster_route_check_v1.json", "poster_check"),
    ("ocr_regression_staticreading_route_check_v1.json", "staticreading_check"),
    ("ocr_regression_memory_handoff_route_check_v1.json", "memory_check"),
    ("ocr_regression_hardware_stub_route_check_v1.json", "hardware_check"),
    ("ocr_regression_boundary_matrix_v1.json", "boundary_matrix"),
    ("ocr_regression_expected_blocker_validation_v1.json", "blocker_validation"),
    ("ocr_regression_provider_bypass_audit_v1.json", "bypass_audit"),
    ("ocr_regression_worldmodel_scenedelta_no_write_v1.json", "wm_sd_check"),
    ("ocr_regression_coverage_report_v1.json", "coverage"),
    ("ocr_regression_route_compliance_decision_trace_v1.json", "trace"),
    ("ocr_regression_route_compliance_final_decision_v1.json", "final"),
    ("ocr_regression_route_compliance_boundary_report_v1.json", "boundary"),
    ("ocr_regression_route_compliance_metrics_candidate_report_v1.json", "metrics"),
    ("ocr_regression_route_compliance_benchmark_link_report_v1.json", "benchmark_link"),
    ("ocr_regression_route_compliance_system_health_report_v1.json", "health_report"),
    ("ocr_regression_route_compliance_no_write_boundary_report_v1.json", "no_write"),
    ("ocr_regression_route_compliance_simulation_context_report_v1.json", "sim_report"),
    ("ocr_regression_route_compliance_non_claims_report_v1.json", "non_claims"),
    ("ocr_regression_route_compliance_open_followups_v1.json", "followups"),
    ("ocr_regression_route_compliance_audit_report_v1.json", "audit"),
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
    ap.add_argument("--closure-root", required=True)
    ap.add_argument("--staticreading-ocrrequest-root", required=True)
    ap.add_argument("--memory-handoff-root", required=True)
    ap.add_argument("--hardware-adapter-stub-root", required=True)
    ap.add_argument("--rrd-runtime-root", required=True)
    ap.add_argument("--realvideo-frame-sample-root", required=True)
    ap.add_argument("--realvideo-ocr-consumer-root", required=True)
    ap.add_argument("--realvideo-text-bearing-planning-root", required=True)
    ap.add_argument("--poster-layout-governance-root", required=True)
    ap.add_argument("--poster-fusion-policy-gate-root", required=True)
    ap.add_argument("--benchmark-smoke-root", required=True)
    ap.add_argument("--testboard-metrics-root", required=True)
    ap.add_argument("--ocr-activation-root", required=True)
    ap.add_argument("--stc-root", required=True)
    ap.add_argument("--system-health-root", required=True)
    ap.add_argument("--simulation-root", required=True)
    args = ap.parse_args()

    out = _require_abs(args.output_root, "--output-root")
    out.mkdir(parents=True, exist_ok=True)

    from capabilities.midplatform.ocr_staticreading_poster_realvideo_regression_route_compliance_v1 import (
        run_ocr_staticreading_poster_realvideo_regression_route_compliance_v1,
    )

    result = run_ocr_staticreading_poster_realvideo_regression_route_compliance_v1(
        closure_root=str(_require_abs(args.closure_root, "closure")),
        staticreading_ocrrequest_root=str(_require_abs(args.staticreading_ocrrequest_root, "ocr_gate")),
        memory_handoff_root=str(_require_abs(args.memory_handoff_root, "mem_handoff")),
        hardware_adapter_stub_root=str(_require_abs(args.hardware_adapter_stub_root, "hw_stub")),
        rrd_runtime_root=str(_require_abs(args.rrd_runtime_root, "rrd")),
        realvideo_frame_sample_root=str(_require_abs(args.realvideo_frame_sample_root, "rv_frame")),
        realvideo_ocr_consumer_root=str(_require_abs(args.realvideo_ocr_consumer_root, "rv_consumer")),
        realvideo_text_bearing_planning_root=str(_require_abs(args.realvideo_text_bearing_planning_root, "rv_plan")),
        poster_layout_governance_root=str(_require_abs(args.poster_layout_governance_root, "poster_layout")),
        poster_fusion_policy_gate_root=str(_require_abs(args.poster_fusion_policy_gate_root, "poster_gate")),
        benchmark_smoke_root=str(_require_abs(args.benchmark_smoke_root, "bench")),
        testboard_metrics_root=str(_require_abs(args.testboard_metrics_root, "testboard")),
        ocr_activation_root=str(_require_abs(args.ocr_activation_root, "ocr_act")),
        stc_root=str(_require_abs(args.stc_root, "stc")),
        system_health_root=str(_require_abs(args.system_health_root, "health")),
        simulation_root=str(_require_abs(args.simulation_root, "sim")),
    )

    for fname, key in WRITES:
        _write_json(out / fname, result[key])

    (out / "ocr_regression_route_compliance_notes.md").write_text(
        "# OCR StaticReading Poster RealVideo Regression Route Compliance v1\n\n"
        f"Final: `{result['final']['final_decision']}`\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "output_root": str(out),
                "final_decision": result["final"]["final_decision"],
                "phase_verdict_hint": result["summary"].get("phase_verdict_hint"),
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())