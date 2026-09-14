#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-Vision-Frame-Input-Governance-001 — frame input gate before ROI / recognition."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

WS_ROOT = Path(__file__).resolve().parents[3]
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
    ap.add_argument("--repo-root", default="")
    ap.add_argument(
        "--frame-trace-root",
        required=True,
        help="Absolute path to vision_frame_trace_stream_registry smoke output root.",
    )
    ap.add_argument("--output-root", required=True)
    args = ap.parse_args()

    trace_root = _require_abs(args.frame_trace_root, "--frame-trace-root")
    out = _require_abs(args.output_root, "--output-root")

    for name in (
        "vision_stream_registry.json",
        "vision_frame_trace.jsonl",
        "vision_frame_lineage_matrix.json",
        "vision_sampling_consistency_report.json",
        "vision_frame_trace_audit_report.json",
    ):
        p = trace_root / name
        if not p.is_file():
            raise SystemExit(f"ERROR: missing input: {p}")

    if args.repo_root.strip():
        repo = _require_abs(args.repo_root, "--repo-root")
        if str(repo) not in sys.path:
            sys.path.insert(0, str(repo))

    from capabilities.vision_runtime.vision_frame_input_governance_v0 import run_vision_frame_input_governance_v0

    bundle = run_vision_frame_input_governance_v0(trace_root, out)

    _write_json(out / "vision_frame_input_governance_summary.json", bundle["summary"])
    _write_json(out / "vision_frame_input_governance_matrix.json", bundle["matrix"])
    _write_json(out / "vision_provider_input_candidate.json", bundle["candidate"])
    _write_json(out / "vision_frame_input_governance_audit_report.json", bundle["audit"])

    notes = (
        "# Phase-Vision-Frame-Input-Governance-001\n\n"
        "Frame **input governance** only: accept/reject, resize hints, ROI eligibility — **no** YOLO/OCR/VLM/"
        "recognition provider/Supervision mainline/MidPlatform/Scene Delta/navigation. "
        "`eligible_for_recognition` stays **false**; next stage is **roi_proposal_stub** only.\n"
    )
    (out / "vision_frame_input_governance_notes.md").write_text(notes, encoding="utf-8")

    print(
        json.dumps(
            {
                "vision_frame_input_governance_root": str(out),
                "frame_trace_root": str(trace_root),
                "accepted_frames": bundle["summary"].get("accepted_frames"),
                "status": "success",
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
