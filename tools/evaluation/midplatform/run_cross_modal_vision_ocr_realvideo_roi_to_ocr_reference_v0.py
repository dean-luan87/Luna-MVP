#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-CrossModal-Vision-OCR-TestBoard-v1-RealVideo-ROI-to-OCR-Reference-001 runner."""

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


def _bootstrap_prerequisites(
    ws: Path,
    *,
    governance_root: Path,
    roi_root: Path,
    bridge_root: Path,
    rapidocr_root: Path,
) -> None:
    roi_root.mkdir(parents=True, exist_ok=True)
    bridge_root.mkdir(parents=True, exist_ok=True)

    if not (roi_root / "vision_roi_proposal_candidate.json").is_file():
        subprocess.run(
            [
                sys.executable,
                str(ws / "tools/evaluation/vision/run_vision_roi_proposal_stub_smoke_v0.py"),
                "--governance-root",
                str(governance_root),
                "--output-root",
                str(roi_root),
            ],
            cwd=str(ws),
            check=True,
        )

    if not (bridge_root / "vision_roi_to_ocr_request_candidates.json").is_file():
        subprocess.run(
            [
                sys.executable,
                str(ws / "tools/evaluation/vision/run_vision_roi_to_ocr_request_bridge_v0.py"),
                "--vision-roi-proposal-root",
                str(roi_root),
                "--output-root",
                str(bridge_root),
            ],
            cwd=str(ws),
            check=True,
        )

    if rapidocr_root.is_dir() and not (rapidocr_root / "cross_modal_vision_ocr_reference_only_rapidocr_summary.json").is_file():
        vis_cons = ws / "_eval_out" / "vision_recognition_evidence_readonly_consumer_smoke_v0"
        ocr_cons = ws / "_eval_out" / "vision_triggered_ocr_evidence_readonly_consumer_smoke_v0"
        if vis_cons.is_dir() and ocr_cons.is_dir():
            subprocess.run(
                [
                    sys.executable,
                    str(ws / "tools/evaluation/midplatform/run_cross_modal_vision_ocr_reference_only_rapidocr_v0.py"),
                    "--output-root",
                    str(rapidocr_root),
                    "--vision-roi-proposal-root",
                    str(roi_root),
                    "--vision-roi-to-ocr-bridge-root",
                    str(bridge_root),
                    "--vision-recognition-readonly-consumer-root",
                    str(vis_cons),
                    "--vision-triggered-ocr-readonly-consumer-root",
                    str(ocr_cons),
                ],
                cwd=str(ws),
                check=True,
            )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-root", required=True)
    ap.add_argument("--frame-sample-root", required=True)
    ap.add_argument("--realvideo-registry-root", required=True)
    ap.add_argument("--vision-roi-proposal-root", required=True)
    ap.add_argument("--vision-roi-to-ocr-bridge-root", required=True)
    ap.add_argument("--cross-modal-rapidocr-reference-root", required=True)
    ap.add_argument("--poster-track-b-closure-root", required=True)
    ap.add_argument("--metrics-collector-root", required=True)
    ap.add_argument("--simulation-lab-harness-root", required=True)
    ap.add_argument("--public-facility-governance-root", default="")
    ap.add_argument(
        "--bootstrap-inputs",
        action="store_true",
        help="Bootstrap ROI proposal / OCR bridge if missing (prerequisite phases only).",
    )
    args = ap.parse_args()

    ws = WS_ROOT
    out = _require_abs(args.output_root, "--output-root")
    out.mkdir(parents=True, exist_ok=True)

    fs_root = _require_abs(args.frame_sample_root, "--frame-sample-root")
    reg = _require_abs(args.realvideo_registry_root, "--realvideo-registry-root")
    roi = _require_abs(args.vision_roi_proposal_root, "--vision-roi-proposal-root")
    bridge = _require_abs(args.vision_roi_to_ocr_bridge_root, "--vision-roi-to-ocr-bridge-root")
    rapidocr = _require_abs(args.cross_modal_rapidocr_reference_root, "--cross-modal-rapidocr-reference-root")
    poster = _require_abs(args.poster_track_b_closure_root, "--poster-track-b-closure-root")
    metrics = _require_abs(args.metrics_collector_root, "--metrics-collector-root")
    sim = _require_abs(args.simulation_lab_harness_root, "--simulation-lab-harness-root")
    facility = (
        _require_abs(args.public_facility_governance_root, "--public-facility-governance-root")
        if args.public_facility_governance_root.strip()
        else (ws / "_eval_out/public_facility_semantic_correction_governance_smoke_v0").resolve()
    )

    if args.bootstrap_inputs:
        gov = (ws / "_eval_out/vision_frame_input_governance_smoke_v0").resolve()
        idx_p = fs_root / "cross_modal_vision_ocr_realvideo_frame_sample_index.json"
        if idx_p.is_file():
            idx = json.loads(idx_p.read_text(encoding="utf-8"))
            if isinstance(idx, dict) and idx.get("governance_root"):
                gov = Path(str(idx["governance_root"])).resolve()
        _bootstrap_prerequisites(ws, governance_root=gov, roi_root=roi, bridge_root=bridge, rapidocr_root=rapidocr)

    from capabilities.midplatform.cross_modal_vision_ocr_realvideo_roi_to_ocr_reference_v0 import (
        run_cross_modal_vision_ocr_realvideo_roi_to_ocr_reference_v0,
    )

    (
        summary,
        candidate,
        frame_roi,
        ocr_matrix,
        case_map,
        gov_report,
        risk,
        metrics_binding,
        boundary,
        sim_report,
        non_claims,
        audit,
        errs,
    ) = run_cross_modal_vision_ocr_realvideo_roi_to_ocr_reference_v0(
        frame_sample_root=str(fs_root),
        realvideo_registry_root=str(reg),
        vision_roi_proposal_root=str(roi),
        vision_roi_to_ocr_bridge_root=str(bridge),
        cross_modal_rapidocr_reference_root=str(rapidocr),
        poster_track_b_closure_root=str(poster),
        metrics_collector_root=str(metrics),
        simulation_lab_harness_root=str(sim),
        public_facility_governance_root=str(facility),
        output_root=str(out),
    )

    summary["output_root"] = str(out.resolve())
    summary["errors"] = list(errs)
    summary["phase_verdict_hint"] = "GO" if not errs else "NO_GO"
    summary["frame_to_roi_row_count"] = frame_roi.get("row_count")
    summary["ocr_request_reference_count"] = ocr_matrix.get("row_count")

    _write_json(out / "cross_modal_vision_ocr_realvideo_roi_to_ocr_reference_summary.json", summary)
    _write_json(out / "cross_modal_vision_ocr_realvideo_roi_to_ocr_reference_candidate.json", candidate)
    _write_json(out / "cross_modal_vision_ocr_realvideo_frame_to_roi_reference_matrix.json", frame_roi)
    _write_json(out / "cross_modal_vision_ocr_realvideo_ocr_request_reference_matrix.json", ocr_matrix)
    _write_json(out / "cross_modal_vision_ocr_realvideo_case_to_reference_mapping.json", case_map)
    _write_json(out / "cross_modal_vision_ocr_realvideo_poster_facility_governance_reference_report.json", gov_report)
    _write_json(out / "cross_modal_vision_ocr_realvideo_roi_to_ocr_reference_risk_report.json", risk)
    _write_json(out / "cross_modal_vision_ocr_realvideo_roi_to_ocr_reference_metrics_binding_report.json", metrics_binding)
    _write_json(out / "cross_modal_vision_ocr_realvideo_roi_to_ocr_reference_no_write_boundary_report.json", boundary)
    _write_json(out / "cross_modal_vision_ocr_realvideo_roi_to_ocr_reference_simulation_context_report.json", sim_report)
    _write_json(out / "cross_modal_vision_ocr_realvideo_roi_to_ocr_reference_non_claims_report.json", non_claims)
    _write_json(out / "cross_modal_vision_ocr_realvideo_roi_to_ocr_reference_audit_report.json", audit)
    (out / "cross_modal_vision_ocr_realvideo_roi_to_ocr_reference_notes.md").write_text(
        "\n".join(
            [
                "# RealVideo ROI-to-OCR Reference v0",
                "",
                f"- phase: {summary.get('phase')}",
                f"- reference_scope: {summary.get('reference_scope')}",
                f"- frame_to_roi_row_count: {summary.get('frame_to_roi_row_count')}",
                f"- ocr_request_reference_count: {summary.get('ocr_request_reference_count')}",
                f"- phase_verdict_hint: {summary.get('phase_verdict_hint')}",
                "",
                "Reference-only: no OCRRequest submit, no OCR invoke, no evidence, no fusion.",
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
                "frame_to_roi_row_count": summary.get("frame_to_roi_row_count"),
                "ocr_request_reference_count": summary.get("ocr_request_reference_count"),
                "errors": errs,
            },
            ensure_ascii=False,
        )
    )
    return 0 if summary.get("phase_verdict_hint") == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
