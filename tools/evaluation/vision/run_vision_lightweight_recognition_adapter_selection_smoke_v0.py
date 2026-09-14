#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-Vision-Lightweight-Recognition-Adapter-Selection-001 — adapter registry + stub selection."""

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
        "--roi-proposal-root",
        required=True,
        help="Absolute path to vision_roi_proposal_stub_smoke output root.",
    )
    ap.add_argument("--output-root", required=True, help="Absolute path to write adapter selection artifacts.")
    args = ap.parse_args()

    roi_root = _require_abs(args.roi_proposal_root, "--roi-proposal-root")
    out = _require_abs(args.output_root, "--output-root")

    for name in (
        "vision_provider_input_pack.json",
        "vision_roi_proposal_candidate.json",
        "vision_roi_proposal_audit_report.json",
    ):
        p = roi_root / name
        if not p.is_file():
            raise SystemExit(f"ERROR: missing ROI stub input: {p}")

    if args.repo_root.strip():
        repo = _require_abs(args.repo_root, "--repo-root")
        if str(repo) not in sys.path:
            sys.path.insert(0, str(repo))

    from capabilities.vision_runtime.vision_provider_selection_v0 import (
        run_vision_recognition_adapter_selection_skeleton_v0,
    )

    bundle = run_vision_recognition_adapter_selection_skeleton_v0(roi_root)

    _write_json(out / "vision_recognition_adapter_selection_summary.json", bundle["summary"])
    _write_json(out / "vision_provider_registry_snapshot.json", bundle["registry_snapshot"])
    _write_json(out / "vision_provider_selection_report.json", bundle["selection_report"])
    _write_json(out / "vision_provider_stub_result.json", bundle["stub_result"])
    _write_json(out / "vision_recognition_candidate_matrix.json", bundle["candidate_matrix"])
    _write_json(out / "vision_recognition_adapter_selection_audit_report.json", bundle["audit"])

    notes = (
        "# Phase-Vision-Lightweight-Recognition-Adapter-Selection-001\n\n"
        "Vision recognition **adapter selection skeleton**: registry + default **vision_stub** + "
        "synthetic stub results + audit. **No** YOLO, Supervision mainline, VLM, OCR, MidPlatform, "
        "Scene Delta, WorldModel, navigation. Providers must consume **vision_provider_input_pack_v0** "
        "units only; real provider env flags are **ignored** for invocation in this phase.\n"
    )
    (out / "vision_recognition_adapter_selection_notes.md").write_text(notes, encoding="utf-8")

    print(
        json.dumps(
            {
                "vision_recognition_adapter_selection_root": str(out),
                "vision_roi_proposal_root": str(roi_root),
                "input_units_count": bundle["summary"].get("input_units_count"),
                "stub_result_items_count": bundle["summary"].get("stub_result_items_count"),
                "status": "success",
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
