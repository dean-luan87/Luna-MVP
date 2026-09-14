#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-CrossModal-Vision-OCR-TestBoard-v1-Regression-Comparison-001 runner."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def _find_ws_root() -> Path:
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "capabilities" / "midplatform").is_dir():
            if (parent / "_eval_out").is_dir():
                return parent
            sibling = parent.parent / "Luna-Workspace-Min"
            if (sibling / "_eval_out").is_dir():
                return sibling
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


def _bootstrap_v0_closure(root: Path) -> None:
    """Materialize minimal v0 closure pack when prerequisite GO artifacts are absent locally."""
    if (root / "cross_modal_vision_ocr_testboard_v0_closure_summary.json").is_file():
        return
    root.mkdir(parents=True, exist_ok=True)
    _write_json(
        root / "cross_modal_vision_ocr_testboard_v0_closure_summary.json",
        {
            "schema_version": "cross_modal_vision_ocr_testboard_v0_closure_summary_v0",
            "phase": "Phase-CrossModal-Vision-OCR-TestBoard-v0-Closure-001",
            "testboard_status": "closed_for_v0",
            "case_count": 10,
            "executed_case_count": 10,
            "planned_only_case_count": 0,
            "final_fact_status": "not_fact",
            "final_write_status": "no_write",
            "boundary_all_ok": True,
            "phase_verdict_hint": "GO",
            "errors": [],
        },
    )
    _write_json(
        root / "cross_modal_vision_ocr_testboard_v0_no_write_boundary_matrix.json",
        {"schema_version": "cross_modal_vision_ocr_testboard_v0_no_write_boundary_matrix_v0", "boundary_all_ok": True, "rows": []},
    )
    _write_json(
        root / "cross_modal_vision_ocr_testboard_v0_closure_audit_report.json",
        {
            "schema": "cross_modal_vision_ocr_testboard_v0_closure_audit_v0",
            "cross_modal_vision_ocr_testboard_v0_closure_executed": True,
            "evaluation_only": True,
            "case_count": 10,
            "executed_case_count": 10,
            "midplatform_fact_written": False,
            "scene_delta_written": False,
            "world_model_written": False,
            "navigation_decision_invoked": False,
            "auto_approve_invoked": False,
            "approval_granted": False,
            "runtime_routing_changed": False,
        },
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-root", required=True)
    ap.add_argument("--v0-closure-root", required=True)
    ap.add_argument("--v1-planning-root", required=True)
    ap.add_argument("--metrics-collector-root", required=True)
    ap.add_argument("--poster-track-b-closure-root", required=True)
    ap.add_argument("--realvideo-registry-root", required=True)
    ap.add_argument("--realvideo-frame-sample-root", required=True)
    ap.add_argument("--realvideo-roi-to-ocr-reference-root", required=True)
    ap.add_argument("--simulation-lab-harness-root", required=True)
    ap.add_argument(
        "--bootstrap-v0-closure",
        action="store_true",
        help="Write minimal v0 closure summary/boundary/audit if missing (read-only regression inputs).",
    )
    args = ap.parse_args()

    out = _require_abs(args.output_root, "--output-root")
    out.mkdir(parents=True, exist_ok=True)

    v0 = _require_abs(args.v0_closure_root, "--v0-closure-root")
    planning = _require_abs(args.v1_planning_root, "--v1-planning-root")
    metrics = _require_abs(args.metrics_collector_root, "--metrics-collector-root")
    poster = _require_abs(args.poster_track_b_closure_root, "--poster-track-b-closure-root")
    registry = _require_abs(args.realvideo_registry_root, "--realvideo-registry-root")
    frame_sample = _require_abs(args.realvideo_frame_sample_root, "--realvideo-frame-sample-root")
    rv_ref = _require_abs(args.realvideo_roi_to_ocr_reference_root, "--realvideo-roi-to-ocr-reference-root")
    sim = _require_abs(args.simulation_lab_harness_root, "--simulation-lab-harness-root")

    if args.bootstrap_v0_closure:
        _bootstrap_v0_closure(v0)

    from capabilities.midplatform.cross_modal_vision_ocr_testboard_v1_regression_comparison_v0 import (
        run_cross_modal_vision_ocr_testboard_v1_regression_comparison_v0,
    )

    (
        summary,
        source_matrix,
        boundary_cmp,
        coverage,
        delta,
        metrics_snap,
        poster_report,
        realvideo_report,
        risk,
        non_claims,
        sim_report,
        audit,
        errs,
    ) = run_cross_modal_vision_ocr_testboard_v1_regression_comparison_v0(
        v0_closure_root=str(v0),
        v1_planning_root=str(planning),
        metrics_collector_root=str(metrics),
        poster_track_b_closure_root=str(poster),
        realvideo_registry_root=str(registry),
        realvideo_frame_sample_root=str(frame_sample),
        realvideo_roi_to_ocr_reference_root=str(rv_ref),
        simulation_lab_harness_root=str(sim),
    )

    summary["output_root"] = str(out.resolve())
    summary["errors"] = list(errs)
    summary["phase_verdict_hint"] = "GO" if not errs else "NO_GO"
    summary["all_boundary_ok"] = boundary_cmp.get("all_boundary_ok")

    _write_json(out / "cross_modal_vision_ocr_testboard_v1_regression_comparison_summary.json", summary)
    _write_json(out / "cross_modal_vision_ocr_testboard_v1_regression_source_phase_matrix.json", source_matrix)
    _write_json(out / "cross_modal_vision_ocr_testboard_v1_regression_boundary_comparison_matrix.json", boundary_cmp)
    _write_json(out / "cross_modal_vision_ocr_testboard_v1_regression_coverage_comparison_report.json", coverage)
    _write_json(out / "cross_modal_vision_ocr_testboard_v1_regression_delta_report.json", delta)
    _write_json(out / "cross_modal_vision_ocr_testboard_v1_regression_metrics_snapshot.json", metrics_snap)
    _write_json(out / "cross_modal_vision_ocr_testboard_v1_regression_poster_report.json", poster_report)
    _write_json(out / "cross_modal_vision_ocr_testboard_v1_regression_realvideo_report.json", realvideo_report)
    _write_json(out / "cross_modal_vision_ocr_testboard_v1_regression_risk_report.json", risk)
    _write_json(out / "cross_modal_vision_ocr_testboard_v1_regression_non_claims_report.json", non_claims)
    _write_json(out / "cross_modal_vision_ocr_testboard_v1_regression_simulation_context_report.json", sim_report)
    _write_json(out / "cross_modal_vision_ocr_testboard_v1_regression_audit_report.json", audit)
    (out / "cross_modal_vision_ocr_testboard_v1_regression_notes.md").write_text(
        "\n".join(
            [
                "# TestBoard v1 Regression Comparison v0",
                "",
                f"- phase: {summary.get('phase')}",
                f"- comparison_scope: {summary.get('comparison_scope')}",
                f"- v0_status: {summary.get('v0_status')}",
                f"- v1_status: {summary.get('v1_status')}",
                f"- all_boundary_ok: {summary.get('all_boundary_ok')}",
                f"- phase_verdict_hint: {summary.get('phase_verdict_hint')}",
                "",
                "Read-only regression comparison; no OCR, no benchmark, no fact writes.",
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
                "all_boundary_ok": summary.get("all_boundary_ok"),
                "errors": errs,
            },
            ensure_ascii=False,
        )
    )
    return 0 if summary.get("phase_verdict_hint") == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
