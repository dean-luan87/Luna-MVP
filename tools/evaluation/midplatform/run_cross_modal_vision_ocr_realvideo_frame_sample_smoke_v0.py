#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-CrossModal-Vision-OCR-TestBoard-v1-RealVideo-FrameSample-Smoke-001 runner."""

from __future__ import annotations

import argparse
import json
import subprocess
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


def _bootstrap_vision_chain(
    ws: Path,
    ingest_root: Path,
    trace_root: Path,
    gov_root: Path,
) -> None:
    """Bootstrap prerequisite vision ingest → trace → governance (not attributed to frame-sample phase)."""
    ingest_root.mkdir(parents=True, exist_ok=True)
    trace_root.mkdir(parents=True, exist_ok=True)
    gov_root.mkdir(parents=True, exist_ok=True)

    if not (ingest_root / "video_frame_envelopes.jsonl").is_file():
        subprocess.run(
            [
                sys.executable,
                str(ws / "tools/evaluation/vision/run_video_frame_minimal_ingest_smoke_v0.py"),
                "--repo-root",
                str(ws),
                "--output-root",
                str(ingest_root),
                "--generate-test-video",
                "--max-frames",
                "10",
            ],
            cwd=str(ws),
            check=True,
        )
    if not (trace_root / "vision_frame_trace.jsonl").is_file():
        subprocess.run(
            [
                sys.executable,
                str(ws / "tools/evaluation/vision/run_vision_frame_trace_stream_registry_v0.py"),
                "--video-ingest-root",
                str(ingest_root),
                "--output-root",
                str(trace_root),
            ],
            cwd=str(ws),
            check=True,
        )

    if not (gov_root / "vision_frame_input_governance_matrix.json").is_file():
        subprocess.run(
            [
                sys.executable,
                str(ws / "tools/evaluation/vision/run_vision_frame_input_governance_v0.py"),
                "--frame-trace-root",
                str(trace_root),
                "--output-root",
                str(gov_root),
            ],
            cwd=str(ws),
            check=True,
        )
def _bootstrap_registry(
    ws: Path,
    registry_root: Path,
    metrics_root: Path,
    poster_gov: Path,
    facility_root: Path,
) -> None:
    if (registry_root / "cross_modal_vision_ocr_realvideo_case_registry.json").is_file():
        return
    registry_root.mkdir(parents=True, exist_ok=True)
    facility_root.mkdir(parents=True, exist_ok=True)
    bootstrap = ws / "_eval_out" / "_realvideo_frame_sample_bootstrap"
    v1_planning = bootstrap / "v1_planning"
    v0_closure = bootstrap / "v0_closure_stub"
    v0_closure.mkdir(parents=True, exist_ok=True)
    if not (v0_closure / "cross_modal_vision_ocr_testboard_v0_closure_summary.json").is_file():
        _write_json(
            v0_closure / "cross_modal_vision_ocr_testboard_v0_closure_summary.json",
            {
                "schema_version": "cross_modal_vision_ocr_testboard_v0_closure_summary_v0",
                "phase": "bootstrap_stub_for_realvideo_frame_sample",
                "testboard_status": "closed_for_v0",
                "executed_case_count": 10,
                "planned_case_count": 10,
            },
        )
    if not (v1_planning / "cross_modal_vision_ocr_testboard_v1_planning_summary.json").is_file():
        subprocess.run(
            [
                sys.executable,
                str(ws / "tools/evaluation/midplatform/run_cross_modal_vision_ocr_testboard_v1_planning_v0.py"),
                "--output-root",
                str(v1_planning),
                "--v0-closure-root",
                str(v0_closure),
            ],
            cwd=str(ws),
            check=True,
        )
    if not (facility_root / "public_facility_semantic_correction_governance_summary.json").is_file():
        subprocess.run(
            [
                sys.executable,
                str(ws / "tools/evaluation/midplatform/run_public_facility_semantic_correction_governance_v0.py"),
                "--output-root",
                str(facility_root),
            ],
            cwd=str(ws),
            check=True,
        )
    subprocess.run(
        [
            sys.executable,
            str(ws / "tools/evaluation/midplatform/run_cross_modal_vision_ocr_realvideo_case_registry_v0.py"),
            "--output-root",
            str(registry_root),
            "--v1-planning-root",
            str(v1_planning),
            "--metrics-collector-root",
            str(metrics_root),
            "--poster-governance-root",
            str(poster_gov),
            "--public-facility-governance-root",
            str(facility_root),
        ],
        cwd=str(ws),
        check=True,
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-root", required=True)
    ap.add_argument("--realvideo-registry-root", required=True)
    ap.add_argument("--poster-track-b-closure-root", required=True)
    ap.add_argument("--metrics-collector-root", required=True)
    ap.add_argument("--simulation-lab-harness-root", required=True)
    ap.add_argument("--vision-ingest-root", required=True)
    ap.add_argument("--vision-frame-trace-root", required=True)
    ap.add_argument("--vision-frame-input-governance-root", required=True)
    ap.add_argument("--public-facility-governance-root", default="")
    ap.add_argument(
        "--bootstrap-inputs",
        action="store_true",
        help="Bootstrap missing vision ingest/trace/governance and case registry (explicit; may generate test video).",
    )
    args = ap.parse_args()

    ws = WS_ROOT
    out = _require_abs(args.output_root, "--output-root")
    out.mkdir(parents=True, exist_ok=True)

    reg = _require_abs(args.realvideo_registry_root, "--realvideo-registry-root")
    poster_closure = _require_abs(args.poster_track_b_closure_root, "--poster-track-b-closure-root")
    metrics = _require_abs(args.metrics_collector_root, "--metrics-collector-root")
    sim = _require_abs(args.simulation_lab_harness_root, "--simulation-lab-harness-root")
    ingest = _require_abs(args.vision_ingest_root, "--vision-ingest-root")
    trace = _require_abs(args.vision_frame_trace_root, "--vision-frame-trace-root")
    gov = _require_abs(args.vision_frame_input_governance_root, "--vision-frame-input-governance-root")
    facility = (
        _require_abs(args.public_facility_governance_root, "--public-facility-governance-root")
        if args.public_facility_governance_root.strip()
        else (ws / "_eval_out" / "public_facility_semantic_correction_governance_smoke_v0").resolve()
    )

    if args.bootstrap_inputs:
        _bootstrap_vision_chain(ws, ingest, trace, gov)
        poster_gov = (ws / "_eval_out" / "poster_layout_segmentation_governance_smoke_v0").resolve()
        _bootstrap_registry(ws, reg, metrics, poster_gov, facility)

    from capabilities.midplatform.cross_modal_vision_ocr_realvideo_frame_sample_smoke_v0 import (
        run_cross_modal_vision_ocr_realvideo_frame_sample_smoke_v0,
    )

    (
        summary,
        index_doc,
        quality,
        coverage,
        poster_facility,
        metrics_binding,
        boundary,
        sim_report,
        non_claims,
        audit,
        errs,
    ) = run_cross_modal_vision_ocr_realvideo_frame_sample_smoke_v0(
        realvideo_registry_root=str(reg),
        poster_track_b_closure_root=str(poster_closure),
        metrics_collector_root=str(metrics),
        simulation_lab_harness_root=str(sim),
        vision_ingest_root=str(ingest),
        vision_frame_trace_root=str(trace),
        vision_frame_input_governance_root=str(gov),
        public_facility_governance_root=str(facility),
        output_root=str(out),
        new_video_decoded=False,
    )

    summary["output_root"] = str(out.resolve())
    summary["errors"] = list(errs)
    summary["phase_verdict_hint"] = "GO" if not errs else "NO_GO"
    summary["bootstrap_inputs_used"] = bool(args.bootstrap_inputs)

    _write_json(out / "cross_modal_vision_ocr_realvideo_frame_sample_summary.json", summary)
    _write_json(out / "cross_modal_vision_ocr_realvideo_frame_sample_index.json", index_doc)
    _write_json(out / "cross_modal_vision_ocr_realvideo_frame_quality_placeholder_matrix.json", quality)
    _write_json(out / "cross_modal_vision_ocr_realvideo_case_coverage_mapping.json", coverage)
    _write_json(out / "cross_modal_vision_ocr_realvideo_poster_facility_candidate_mapping.json", poster_facility)
    _write_json(out / "cross_modal_vision_ocr_realvideo_frame_sample_metrics_binding_report.json", metrics_binding)
    _write_json(out / "cross_modal_vision_ocr_realvideo_frame_sample_no_write_boundary_report.json", boundary)
    _write_json(out / "cross_modal_vision_ocr_realvideo_frame_sample_simulation_context_report.json", sim_report)
    _write_json(out / "cross_modal_vision_ocr_realvideo_frame_sample_non_claims_report.json", non_claims)
    _write_json(out / "cross_modal_vision_ocr_realvideo_frame_sample_audit_report.json", audit)
    (out / "cross_modal_vision_ocr_realvideo_frame_sample_notes.md").write_text(
        "\n".join(
            [
                "# RealVideo FrameSample Smoke v0",
                "",
                f"- phase: {summary.get('phase')}",
                f"- sample_scope: {summary.get('sample_scope')}",
                f"- sample_count: {summary.get('sample_count')}",
                f"- new_video_decoded: {summary.get('new_video_decoded')}",
                f"- phase_verdict_hint: {summary.get('phase_verdict_hint')}",
                "",
                "Frame sample index only; no OCR, Vision provider, YOLO, VLM, OCRRequest, fusion, or fact writes.",
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
                "sample_count": summary.get("sample_count"),
                "new_video_decoded": summary.get("new_video_decoded"),
                "errors": errs,
            },
            ensure_ascii=False,
        )
    )
    return 0 if summary.get("phase_verdict_hint") == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
