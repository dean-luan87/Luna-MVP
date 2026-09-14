#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-Vision-Frame-ROI-Proposal-And-Segmentation-Stub-001 — rule ROI + vision_provider_input_pack_v0."""

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
        "--governance-root",
        required=True,
        help="Absolute path to vision_frame_input_governance smoke output root.",
    )
    ap.add_argument("--output-root", required=True, help="Absolute path to write ROI stub artifacts.")
    args = ap.parse_args()

    gov = _require_abs(args.governance_root, "--governance-root")
    out = _require_abs(args.output_root, "--output-root")

    for name in (
        "vision_provider_input_candidate.json",
        "vision_frame_input_governance_matrix.json",
        "vision_frame_input_governance_summary.json",
        "vision_frame_input_governance_audit_report.json",
    ):
        p = gov / name
        if not p.is_file():
            raise SystemExit(f"ERROR: missing governance input: {p}")

    if args.repo_root.strip():
        repo = _require_abs(args.repo_root, "--repo-root")
        if str(repo) not in sys.path:
            sys.path.insert(0, str(repo))

    from capabilities.vision_runtime.vision_roi_proposal_stub_v0 import run_vision_roi_proposal_stub_from_governance_v0

    bundle = run_vision_roi_proposal_stub_from_governance_v0(gov, out)

    _write_json(out / "vision_roi_proposal_stub_summary.json", bundle["summary"])
    _write_json(out / "vision_roi_proposal_candidate.json", bundle["proposal_candidate"])
    _write_json(out / "vision_provider_input_pack.json", bundle["provider_input_pack_bundle"])
    _write_json(out / "vision_roi_proposal_matrix.json", bundle["proposal_matrix"])
    _write_json(out / "vision_provider_input_unit_matrix.json", bundle["unit_matrix"])
    _write_json(out / "vision_roi_source_chain_summary.json", bundle["source_chain_summary"])
    _write_json(out / "vision_roi_proposal_audit_report.json", bundle["audit"])

    notes = (
        "# Phase-Vision-Frame-ROI-Proposal-And-Segmentation-Stub-001\n\n"
        "Rule / stub **ROI proposal** and **vision_provider_input_pack_v0** only: fixed layout ROIs, "
        "bbox-derived polygon stub, ROI **crops** on disk, coordinate transforms recorded. "
        "**No** YOLO, real detector, Supervision mainline, VLM, OCR, AI interpretation, navigation, "
        "MidPlatform fact, Scene Delta, WorldModel, or camera capture.\n"
    )
    (out / "vision_roi_proposal_stub_notes.md").write_text(notes, encoding="utf-8")

    print(
        json.dumps(
            {
                "vision_roi_proposal_stub_root": str(out),
                "frame_input_governance_root": str(gov),
                "roi_items_count": bundle["summary"].get("roi_items_count"),
                "input_units_count": bundle["summary"].get("input_units_count"),
                "status": "success",
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
