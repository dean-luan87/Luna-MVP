#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-CrossModal-Vision-OCR-TestBoard-v1-Track-Closures-001 runner."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def _find_ws_root() -> Path:
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "capabilities" / "midplatform").is_dir():
            sibling = parent.parent / "Luna-Workspace-Min"
            if (sibling / "_eval_out").is_dir():
                return sibling
            if (parent / "_eval_out").is_dir():
                return parent
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


def _bootstrap_metrics_schema(root: Path) -> None:
    if (root / "cross_modal_vision_ocr_testboard_metrics_schema_summary.json").is_file():
        return
    root.mkdir(parents=True, exist_ok=True)
    _write_json(
        root / "cross_modal_vision_ocr_testboard_metrics_schema_summary.json",
        {
            "schema_version": "cross_modal_vision_ocr_testboard_metrics_schema_summary_v0",
            "phase": "CrossModal-Vision-OCR-TestBoard-Metrics-Schema-001",
            "metrics_scope": "schema_definition_only",
            "phase_verdict_hint": "GO",
            "errors": [],
            "performance_metrics_available": False,
        },
    )
    _write_json(
        root / "cross_modal_vision_ocr_testboard_metrics_schema_audit_report.json",
        {
            "schema": "cross_modal_vision_ocr_testboard_metrics_schema_audit_v0",
            "ocr_invoked": False,
            "fusion_invoked": False,
            "midplatform_fact_written": False,
            "scene_delta_written": False,
            "world_model_written": False,
            "runtime_routing_changed": False,
        },
    )


def _resolve_planning_root(ws: Path, requested: Path) -> Path:
    if (requested / "cross_modal_vision_ocr_testboard_v1_planning_summary.json").is_file():
        return requested
    alt = ws / "_eval_out" / "_realvideo_frame_sample_bootstrap" / "v1_planning"
    if (alt / "cross_modal_vision_ocr_testboard_v1_planning_summary.json").is_file():
        return alt.resolve()
    return requested


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-root", required=True)
    ap.add_argument("--v1-planning-root", required=True)
    ap.add_argument("--poster-track-b-closure-root", required=True)
    ap.add_argument("--metrics-schema-root", required=True)
    ap.add_argument("--metrics-collector-root", required=True)
    ap.add_argument("--realvideo-registry-root", required=True)
    ap.add_argument("--realvideo-frame-sample-root", required=True)
    ap.add_argument("--realvideo-roi-to-ocr-reference-root", required=True)
    ap.add_argument("--regression-comparison-root", required=True)
    ap.add_argument("--simulation-lab-harness-root", required=True)
    ap.add_argument("--bootstrap-metrics-schema", action="store_true")
    args = ap.parse_args()

    ws = WS_ROOT
    out = _require_abs(args.output_root, "--output-root")
    out.mkdir(parents=True, exist_ok=True)

    planning = _resolve_planning_root(ws, _require_abs(args.v1_planning_root, "--v1-planning-root"))
    poster = _require_abs(args.poster_track_b_closure_root, "--poster-track-b-closure-root")
    metrics_schema = _require_abs(args.metrics_schema_root, "--metrics-schema-root")
    metrics_coll = _require_abs(args.metrics_collector_root, "--metrics-collector-root")
    registry = _require_abs(args.realvideo_registry_root, "--realvideo-registry-root")
    frame_sample = _require_abs(args.realvideo_frame_sample_root, "--realvideo-frame-sample-root")
    rv_ref = _require_abs(args.realvideo_roi_to_ocr_reference_root, "--realvideo-roi-to-ocr-reference-root")
    regression = _require_abs(args.regression_comparison_root, "--regression-comparison-root")
    sim = _require_abs(args.simulation_lab_harness_root, "--simulation-lab-harness-root")

    if args.bootstrap_metrics_schema:
        _bootstrap_metrics_schema(metrics_schema)

    from capabilities.midplatform.cross_modal_vision_ocr_testboard_v1_track_closures_v0 import (
        run_cross_modal_vision_ocr_testboard_v1_track_closures_v0,
    )

    (
        summary,
        track_matrix,
        source_matrix,
        boundary,
        coverage,
        capability,
        carryover,
        non_claims,
        followups,
        metrics_track,
        realvideo_track,
        poster_link,
        sim_report,
        audit,
        risk_report,
        errs,
    ) = run_cross_modal_vision_ocr_testboard_v1_track_closures_v0(
        v1_planning_root=str(planning),
        poster_track_b_closure_root=str(poster),
        metrics_schema_root=str(metrics_schema),
        metrics_collector_root=str(metrics_coll),
        realvideo_registry_root=str(registry),
        realvideo_frame_sample_root=str(frame_sample),
        realvideo_roi_to_ocr_reference_root=str(rv_ref),
        regression_comparison_root=str(regression),
        simulation_lab_harness_root=str(sim),
    )

    summary["output_root"] = str(out.resolve())
    summary["errors"] = list(errs)
    summary["phase_verdict_hint"] = "GO" if not errs else "NO_GO"

    _write_json(out / "cross_modal_vision_ocr_testboard_v1_track_closures_summary.json", summary)
    _write_json(out / "cross_modal_vision_ocr_testboard_v1_track_closure_matrix.json", track_matrix)
    _write_json(out / "cross_modal_vision_ocr_testboard_v1_track_closures_source_phase_matrix.json", source_matrix)
    _write_json(out / "cross_modal_vision_ocr_testboard_v1_track_closures_boundary_matrix.json", boundary)
    _write_json(out / "cross_modal_vision_ocr_testboard_v1_coverage_closure_report.json", coverage)
    _write_json(out / "cross_modal_vision_ocr_testboard_v1_capability_closure_report.json", capability)
    _write_json(out / "cross_modal_vision_ocr_testboard_v1_regression_carryover_report.json", carryover)
    _write_json(out / "cross_modal_vision_ocr_testboard_v1_non_claims_report.json", non_claims)
    _write_json(out / "cross_modal_vision_ocr_testboard_v1_open_followups.json", followups)
    _write_json(out / "cross_modal_vision_ocr_testboard_v1_metrics_track_c_closure_report.json", metrics_track)
    _write_json(out / "cross_modal_vision_ocr_testboard_v1_realvideo_track_a_closure_report.json", realvideo_track)
    _write_json(out / "cross_modal_vision_ocr_testboard_v1_poster_track_b_closure_link_report.json", poster_link)
    _write_json(out / "cross_modal_vision_ocr_testboard_v1_track_closures_simulation_context_report.json", sim_report)
    _write_json(out / "cross_modal_vision_ocr_testboard_v1_track_closures_audit_report.json", audit)
    _write_json(out / "cross_modal_vision_ocr_testboard_v1_regression_risk_report.json", risk_report)
    (out / "cross_modal_vision_ocr_testboard_v1_track_closures_notes.md").write_text(
        "\n".join(
            [
                "# TestBoard v1 Track Closures",
                "",
                f"- phase: {summary.get('phase')}",
                f"- v1_status: {summary.get('v1_status')}",
                f"- track_a: {summary.get('track_a_realvideo_status')}",
                f"- track_b: {summary.get('track_b_poster_status')}",
                f"- track_c: {summary.get('track_c_metrics_status')}",
                f"- phase_verdict_hint: {summary.get('phase_verdict_hint')}",
                "",
                "Evaluation closure only; not production ready.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    print(
        json.dumps(
            {
                "output_root": str(out),
                "phase_verdict_hint": summary.get("phase_verdict_hint"),
                "v1_status": summary.get("v1_status"),
                "errors": errs,
            },
            ensure_ascii=False,
        )
    )
    return 0 if summary.get("phase_verdict_hint") == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
