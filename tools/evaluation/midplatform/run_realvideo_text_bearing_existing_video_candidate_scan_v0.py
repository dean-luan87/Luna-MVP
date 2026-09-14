#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-RealVideo-Text-Bearing-Existing-Video-Candidate-Scan-001 runner."""

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


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-root", required=True)
    ap.add_argument("--video-path", required=True)
    ap.add_argument("--text-bearing-sample-planning-root", default="")
    ap.add_argument("--sample-interval-sec", type=float, default=3.0)
    ap.add_argument("--max-samples", type=int, default=250)
    ap.add_argument("--max-width", type=int, default=1280)
    ap.add_argument("--no-save-frames", action="store_true")
    args = ap.parse_args()

    out = _require_abs(args.output_root, "--output-root")
    video = _require_abs(args.video_path, "--video-path")
    planning = (
        _require_abs(args.text_bearing_sample_planning_root, "planning")
        if args.text_bearing_sample_planning_root.strip()
        else None
    )

    from capabilities.midplatform.realvideo_text_bearing_existing_video_candidate_scan_v0 import (
        run_existing_video_candidate_scan_v0,
    )

    summary, video_report, candidates, boundary, audit, errs = run_existing_video_candidate_scan_v0(
        video_path=str(video),
        output_root=str(out),
        text_bearing_sample_planning_root=str(planning) if planning else None,
        sample_interval_sec=float(args.sample_interval_sec),
        max_samples=int(args.max_samples),
        max_width=int(args.max_width),
        save_candidate_frames=not args.no_save_frames,
    )

    if errs and not summary:
        print(json.dumps({"errors": errs}, ensure_ascii=False))
        return 1

    summary["output_root"] = str(out)
    summary["input_roots"] = {"video_path": str(video)}
    if planning:
        summary["input_roots"]["text_bearing_sample_planning_root"] = str(planning)
    if errs:
        summary["errors"] = errs

    _write_json(out / "realvideo_text_bearing_existing_video_candidate_scan_summary.json", summary)
    _write_json(out / "realvideo_text_bearing_existing_video_scan_report.json", video_report)
    _write_json(out / "realvideo_text_bearing_frame_candidates.json", candidates)
    _write_json(out / "realvideo_text_bearing_existing_video_scan_no_write_boundary_report.json", boundary)
    _write_json(out / "realvideo_text_bearing_existing_video_scan_audit_report.json", audit)

    (out / "realvideo_text_bearing_existing_video_scan_notes.md").write_text(
        "\n".join(
            [
                "# RealVideo Existing Video Candidate Scan",
                "",
                f"- video: {video}",
                f"- frames_sampled: {summary.get('frames_sampled')}",
                f"- text_bearing_candidate_count: {summary.get('text_bearing_candidate_count')}",
                f"- phase_verdict_hint: {summary.get('phase_verdict_hint')}",
                "",
                "Scan-only OCR heuristic; not reference chain / not fact.",
                "",
            ]
        ),
        encoding="utf-8",
    )

    print(
        json.dumps(
            {
                "output_root": str(out),
                "phase_verdict_hint": summary.get("phase_verdict_hint"),
                "text_bearing_candidate_count": summary.get("text_bearing_candidate_count"),
                "errors": errs,
            },
            ensure_ascii=False,
        )
    )
    return 0 if summary.get("phase_verdict_hint") in ("GO", "CONDITIONAL_GO") else 1


if __name__ == "__main__":
    raise SystemExit(main())
