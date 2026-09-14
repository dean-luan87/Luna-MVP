#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for Phase-Vision-External-Supervision-Adapter-Experiment-001."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List


def _require_abs(p: str, label: str) -> Path:
    pp = Path(p).expanduser()
    if not pp.is_absolute():
        raise SystemExit(f"ERROR: {label} must be absolute, got: {p}")
    return pp.resolve()


def _read_json(p: Path) -> Any:
    return json.loads(p.read_text(encoding="utf-8"))


def _write_json(path: Path, obj: object) -> None:
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke-root", default="", help="Absolute path to experiment output root.")
    ap.add_argument(
        "--experiment-root",
        default="",
        help="Alias of --smoke-root (external experiment naming).",
    )
    args = ap.parse_args()

    root_raw = (args.smoke_root or args.experiment_root or "").strip()
    if not root_raw:
        raise SystemExit("ERROR: provide --smoke-root or --experiment-root (absolute).")
    root = _require_abs(root_raw, "--smoke-root/--experiment-root")
    blockers: List[str] = []
    soft: List[str] = []

    paths = {
        "probe": root / "external_supervision_availability_probe.json",
        "roi": root / "vision_roi_proposal_candidate.json",
        "audit": root / "external_supervision_audit_report.json",
        "summary": root / "external_supervision_adapter_experiment_summary.json",
        "feature_matrix": root / "external_supervision_feature_matrix.json",
        "synthetic": root / "external_supervision_synthetic_detections.json",
    }
    for label, p in paths.items():
        if not p.is_file():
            blockers.append(f"missing:{label}")

    verdict = "NO_GO"
    supervision_installed = False

    if not blockers:
        probe = _read_json(paths["probe"])
        roi = _read_json(paths["roi"])
        aud = _read_json(paths["audit"])
        summary = _read_json(paths["summary"])

        supervision_installed = bool(probe.get("supervision_installed"))

        if "supervision_import_attempted" not in aud:
            blockers.append("audit_missing_supervision_import_attempted")
        if "supervision_installed" not in probe:
            blockers.append("probe_missing_supervision_installed")

        items = roi.get("roi_items") if isinstance(roi.get("roi_items"), list) else []
        if len(items) < 1:
            blockers.append("roi_items_count_below_1")

        sfi = str(roi.get("source_frame_id") or "").strip()
        sir = str(roi.get("source_image_ref") or "").strip()
        if not sfi and not sir:
            blockers.append("roi_missing_source_frame_id_and_image_ref")

        sc = roi.get("source_chain")
        if not isinstance(sc, list) or len(sc) < 1:
            blockers.append("roi_missing_source_chain")

        for i, it in enumerate(items):
            if not isinstance(it, dict):
                blockers.append(f"roi_item_not_object:{i}")
                break
            bb = it.get("bbox_in_frame")
            if not isinstance(bb, list) or len(bb) != 4:
                blockers.append(f"roi_missing_bbox_in_frame:{i}")

        for k in (
            "real_camera_invoked",
            "yolo_invoked",
            "real_detector_invoked",
            "ocr_invoked",
            "vlm_invoked",
            "supervision_mainline_invoked",
            "vision_recognition_provider_invoked",
            "navigation_decision_invoked",
            "midplatform_fact_written",
            "scene_delta_written",
            "world_model_written",
            "ai_interpretation_invoked",
            "runtime_mainline_modified",
        ):
            if aud.get(k) is not False:
                blockers.append(f"audit_flag_not_false:{k}")

        if aud.get("supervision_import_attempted") is not True:
            blockers.append("supervision_import_attempted_not_true")

        if summary.get("supervision_marked_as_default_vision_module") is True:
            blockers.append("supervision_must_not_be_default_vision_module")

        if not supervision_installed:
            gap = summary.get("supervision_install_gap_report")
            if not isinstance(gap, dict) or gap.get("complete") is not True:
                blockers.append("missing_or_incomplete_supervision_install_gap_report")
            if not str(probe.get("import_error") or "").strip():
                blockers.append("probe_import_error_empty_when_supervision_missing")

    if blockers:
        verdict = "NO_GO"
    elif supervision_installed:
        verdict = "GO"
    else:
        verdict = "CONDITIONAL_GO"
        soft.append("supervision_not_installed:synthetic_roi_and_probe_complete")

    rep = {
        "schema": "external_supervision_adapter_verifier_report_v0",
        "phase": "Phase-Vision-External-Supervision-Adapter-Experiment-001",
        "smoke_root": str(root),
        "verdict": verdict,
        "blockers": blockers,
        "soft_notes": soft,
    }
    _write_json(root / "external_supervision_adapter_verifier_report.json", rep)
    print(json.dumps({"smoke_root": str(root), "verdict": verdict, "blockers": blockers}, ensure_ascii=False))
    if verdict == "NO_GO":
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
