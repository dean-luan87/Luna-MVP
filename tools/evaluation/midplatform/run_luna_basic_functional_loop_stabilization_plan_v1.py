#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-Luna-Basic-Functional-Loop-Stabilization-Plan-v1-001 runner."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

WRITES = [
    ("luna_basic_functional_loop_stabilization_plan_v1_summary.json", "summary"),
    ("luna_basic_loop_input_intake_matrix_v1.json", "intake"),
    ("luna_basic_loop_current_capability_status_matrix_v1.json", "capability_matrix"),
    ("luna_basic_functional_loop_definition_v1.json", "loop_definition"),
    ("luna_basic_loop_module_responsibility_boundary_v1.json", "module_boundary"),
    ("luna_basic_loop_information_source_standard_v1.json", "info_source_standard"),
    ("luna_basic_loop_task_state_stabilization_policy_v1.json", "task_state_policy"),
    ("luna_basic_loop_voice_dialogue_minimal_capability_plan_v1.json", "voice_plan"),
    ("luna_basic_loop_vision_ocr_evidence_ingest_plan_v1.json", "vision_ocr_ingest"),
    ("luna_basic_loop_isrc_handoff_policy_v1.json", "isrc_handoff"),
    ("luna_basic_loop_rrd_handoff_policy_v1.json", "rrd_handoff"),
    ("luna_basic_loop_candidate_classification_policy_v1.json", "classification"),
    ("luna_basic_loop_no_write_boundary_policy_v1.json", "no_write_policy"),
    ("luna_basic_loop_navigation_guidance_plan_v1.json", "nav_plan"),
    ("luna_basic_loop_future_segmentation_entry_policy_v1.json", "seg_policy"),
    ("luna_basic_loop_future_object_tracking_entry_policy_v1.json", "tracking_policy"),
    ("luna_basic_loop_future_navigation_map_entry_policy_v1.json", "map_policy"),
    ("luna_basic_loop_deferred_capability_matrix_v1.json", "deferred"),
    ("luna_basic_loop_stabilization_test_plan_v1.json", "test_plan"),
    ("luna_basic_loop_recommended_phase_roadmap_v1.json", "roadmap"),
    ("luna_basic_loop_stabilization_decision_trace_v1.json", "trace"),
    ("luna_basic_loop_stabilization_final_decision_v1.json", "final"),
    ("luna_basic_loop_stabilization_boundary_report_v1.json", "boundary"),
    ("luna_basic_loop_stabilization_metrics_candidate_report_v1.json", "metrics"),
    ("luna_basic_loop_stabilization_benchmark_link_report_v1.json", "benchmark_link"),
    ("luna_basic_loop_stabilization_system_health_report_v1.json", "health_report"),
    ("luna_basic_loop_stabilization_no_write_boundary_report_v1.json", "no_write"),
    ("luna_basic_loop_stabilization_simulation_context_report_v1.json", "sim_report"),
    ("luna_basic_loop_stabilization_non_claims_report_v1.json", "non_claims"),
    ("luna_basic_loop_stabilization_open_followups_v1.json", "followups"),
    ("luna_basic_loop_stabilization_audit_report_v1.json", "audit"),
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
    ap.add_argument("--ocr-mainline-closure-root", required=True)
    ap.add_argument("--worldmodel-framework-root", required=True)
    ap.add_argument("--software-closure-root", required=True)
    ap.add_argument("--ocr-activation-root", required=True)
    ap.add_argument("--stc-root", required=True)
    ap.add_argument("--vision-capture-governance-root", required=True)
    ap.add_argument("--vision-capture-runtime-root", required=True)
    ap.add_argument("--user-guidance-runtime-root", required=True)
    ap.add_argument("--voice-guidance-runtime-root", required=True)
    ap.add_argument("--vop-adapter-root", required=True)
    ap.add_argument("--hardware-adapter-stub-root", required=True)
    ap.add_argument("--realvideo-frame-sample-root", required=True)
    ap.add_argument("--regression-route-root", required=True)
    ap.add_argument("--system-health-root", required=True)
    ap.add_argument("--simulation-root", required=True)
    ap.add_argument("--benchmark-smoke-root", default="")
    ap.add_argument("--workspace-root", default="/Users/luanlei/Desktop/Luna-Workspace-Min")
    args = ap.parse_args()

    out = _require_abs(args.output_root, "--output-root")
    out.mkdir(parents=True, exist_ok=True)

    from capabilities.midplatform.luna_basic_functional_loop_stabilization_plan_v1 import (
        run_luna_basic_functional_loop_stabilization_plan_v1,
    )

    bench = args.benchmark_smoke_root.strip() or None
    result = run_luna_basic_functional_loop_stabilization_plan_v1(
        ocr_mainline_closure_root=str(_require_abs(args.ocr_mainline_closure_root, "ocr_closure")),
        worldmodel_framework_root=str(_require_abs(args.worldmodel_framework_root, "wm_fw")),
        software_closure_root=str(_require_abs(args.software_closure_root, "sw_closure")),
        ocr_activation_root=str(_require_abs(args.ocr_activation_root, "ocr_act")),
        stc_root=str(_require_abs(args.stc_root, "stc")),
        vision_capture_governance_root=str(_require_abs(args.vision_capture_governance_root, "vision_gov")),
        vision_capture_runtime_root=str(_require_abs(args.vision_capture_runtime_root, "vision_rt")),
        user_guidance_runtime_root=str(_require_abs(args.user_guidance_runtime_root, "user_guidance")),
        voice_guidance_runtime_root=str(_require_abs(args.voice_guidance_runtime_root, "voice_guidance")),
        vop_adapter_root=str(_require_abs(args.vop_adapter_root, "vop")),
        hardware_adapter_stub_root=str(_require_abs(args.hardware_adapter_stub_root, "hw_stub")),
        realvideo_frame_sample_root=str(_require_abs(args.realvideo_frame_sample_root, "rv")),
        regression_route_root=str(_require_abs(args.regression_route_root, "regression")),
        system_health_root=str(_require_abs(args.system_health_root, "health")),
        simulation_root=str(_require_abs(args.simulation_root, "sim")),
        benchmark_smoke_root=str(_require_abs(bench, "bench")) if bench else None,
        workspace_root=str(_require_abs(args.workspace_root, "workspace")),
    )

    for fname, key in WRITES:
        _write_json(out / fname, result[key])

    (out / "luna_basic_loop_stabilization_notes.md").write_text(
        "# Luna Basic Functional Loop Stabilization Plan v1\n\n"
        f"Final: `{result['final']['final_decision']}`\n"
        f"Next: `{result['final']['next_recommended_phase']}`\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "output_root": str(out),
                "final_decision": result["final"]["final_decision"],
                "next_recommended_phase": result["final"]["next_recommended_phase"],
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
