#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-Vision-External-Supervision-Adapter-Experiment-001 — external Supervision probe + synthetic ROI candidate (not mainline)."""

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
    ap.add_argument("--repo-root", default="", help="Optional absolute repo root for PYTHONPATH.")
    ap.add_argument(
        "--video-ingest-root",
        default="",
        help="Absolute path to video_frame_minimal_ingest smoke (must contain video_frame_envelopes.jsonl).",
    )
    ap.add_argument(
        "--frame-ingest-root",
        default="",
        help="Alias of --video-ingest-root (external experiment naming).",
    )
    ap.add_argument("--output-root", required=True, help="Absolute path for experiment artifacts.")
    args = ap.parse_args()

    ingest_raw = (args.video_ingest_root or args.frame_ingest_root or "").strip()
    if not ingest_raw:
        raise SystemExit("ERROR: provide --video-ingest-root or --frame-ingest-root (absolute).")
    ingest = _require_abs(ingest_raw, "--video-ingest-root/--frame-ingest-root")
    out = _require_abs(args.output_root, "--output-root")
    out.mkdir(parents=True, exist_ok=True)

    if args.repo_root.strip():
        repo = _require_abs(args.repo_root, "--repo-root")
        if str(repo) not in sys.path:
            sys.path.insert(0, str(repo))

    env_path = ingest / "video_frame_envelopes.jsonl"
    if not env_path.is_file():
        raise SystemExit(f"ERROR: missing {env_path}")

    from capabilities.vision_runtime.external_supervision_adapter_experiment_v0 import (
        run_external_supervision_adapter_experiment_v0,
    )

    summary, probe, synthetic, roi, feature_matrix, audit, _env = run_external_supervision_adapter_experiment_v0(
        ingest, out
    )

    summary["supervision_marked_as_default_vision_module"] = False

    _write_json(out / "external_supervision_adapter_experiment_summary.json", summary)
    _write_json(out / "external_supervision_availability_probe.json", probe)
    _write_json(out / "external_supervision_synthetic_detections.json", {"detections": synthetic})
    _write_json(out / "vision_roi_proposal_candidate.json", roi)
    _write_json(out / "external_supervision_feature_matrix.json", feature_matrix)
    _write_json(out / "external_supervision_audit_report.json", audit)

    notes = (
        "# Phase-Vision-External-Supervision-Adapter-Experiment-001\n\n"
        "**External experiment only** — Roboflow Supervision as a **candidate** for ROI/tracking/mask tooling. "
        "**Not** Luna runtime mainline; **not** MidPlatform; **no** navigation; **no** YOLO invoke in this smoke "
        "(synthetic detections only). See `docs/architecture/vision/LUNA_VISION_EXTERNAL_SUPERVISION_ADAPTER_EXPERIMENT_V0.md`.\n"
    )
    (out / "external_supervision_adapter_notes.md").write_text(notes, encoding="utf-8")

    print(
        json.dumps(
            {
                "external_supervision_adapter_experiment_root": str(out),
                "video_ingest_root": str(ingest),
                "supervision_installed": summary.get("supervision_installed"),
                "status": "success",
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
