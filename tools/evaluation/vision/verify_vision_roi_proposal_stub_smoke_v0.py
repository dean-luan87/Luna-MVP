#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for Phase-Vision-Frame-ROI-Proposal-And-Segmentation-Stub-001."""

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


def _collect_packs(bundle: Dict[str, Any]) -> List[Dict[str, Any]]:
    if isinstance(bundle.get("packs"), list):
        return [p for p in bundle["packs"] if isinstance(p, dict)]
    if bundle.get("schema_version") == "vision_provider_input_pack_v0" and isinstance(bundle.get("input_units"), list):
        return [bundle]
    return []


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--governance-root",
        required=True,
        help="Absolute path to vision_frame_input_governance output (must exist).",
    )
    ap.add_argument("--smoke-root", required=True, help="ROI stub output root.")
    args = ap.parse_args()

    gov = _require_abs(args.governance_root, "--governance-root")
    root = _require_abs(args.smoke_root, "--smoke-root")

    blockers: List[str] = []
    soft: List[str] = []

    if not gov.is_dir():
        blockers.append("governance_root_not_dir")

    sum_stub = root / "vision_roi_proposal_stub_summary.json"
    cand_roi = root / "vision_roi_proposal_candidate.json"
    pack_p = root / "vision_provider_input_pack.json"
    aud_p = root / "vision_roi_proposal_audit_report.json"
    sc_p = root / "vision_roi_source_chain_summary.json"

    for label, p in (
        ("stub_summary", sum_stub),
        ("roi_proposal_candidate", cand_roi),
        ("vision_provider_input_pack", pack_p),
        ("audit", aud_p),
        ("source_chain_summary", sc_p),
    ):
        if not p.is_file():
            blockers.append(f"missing:{label}")

    verdict = "NO_GO"
    roi_count = 0
    unit_count = 0
    missing_crop = False

    if not blockers:
        stub_sum = _read_json(sum_stub)
        gref = str(stub_sum.get("frame_input_governance_root") or "")
        if gref and Path(gref).resolve() != gov.resolve():
            soft.append("stub_summary_governance_root_mismatch_with_flag")

        cand = _read_json(cand_roi)
        roi_items = cand.get("roi_items") if isinstance(cand.get("roi_items"), list) else []
        roi_count = len(roi_items)
        if roi_count <= 0:
            blockers.append("roi_items_count_not_positive")

        pack_bundle = _read_json(pack_p)
        packs = _collect_packs(pack_bundle)
        if not packs:
            blockers.append("no_packs_in_vision_provider_input_pack")

        all_units: List[Dict[str, Any]] = []
        for p in packs:
            units = p.get("input_units") if isinstance(p.get("input_units"), list) else []
            all_units.extend([u for u in units if isinstance(u, dict)])
        unit_count = len(all_units)
        if unit_count <= 0:
            blockers.append("input_units_count_not_positive")

        for roi in roi_items:
            if not isinstance(roi, dict):
                blockers.append("roi_item_not_object")
                continue
            bb = roi.get("bbox_in_frame")
            if not isinstance(bb, list) or len(bb) != 4:
                blockers.append("roi_missing_bbox_in_frame")
            poly = roi.get("polygon_in_frame")
            if not isinstance(poly, list) or len(poly) < 3:
                blockers.append("roi_missing_polygon_in_frame")
            if str(roi.get("proposal_source") or "") != "rule_stub":
                blockers.append("proposal_source_not_rule_stub")
            seg = roi.get("segmentation_stub") or {}
            if seg.get("mask_available") is not False:
                blockers.append("segmentation_stub_mask_available_not_false")

        for u in all_units:
            cref = str(u.get("image_ref") or "").strip()
            if not cref:
                missing_crop = True
            elif not Path(cref).is_file():
                blockers.append("unit_crop_image_ref_not_file")
            ct = u.get("coordinate_transform")
            if not isinstance(ct, dict):
                blockers.append("unit_missing_coordinate_transform")
            else:
                for k in (
                    "mode",
                    "offset_x",
                    "offset_y",
                    "scale_x",
                    "scale_y",
                    "source_frame_width",
                    "source_frame_height",
                    "transformed_width",
                    "transformed_height",
                ):
                    if k not in ct:
                        blockers.append(f"coordinate_transform_missing:{k}")

        for p in packs:
            sc = p.get("source_chain")
            if not isinstance(sc, list) or len(sc) == 0:
                blockers.append("pack_missing_source_chain")

        aud = _read_json(aud_p)
        for k, must in (
            ("roi_proposal_stub_generated", True),
            ("vision_provider_input_pack_generated", True),
            ("yolo_invoked", False),
            ("real_detector_invoked", False),
            ("supervision_mainline_invoked", False),
            ("vlm_invoked", False),
            ("ocr_invoked", False),
            ("ai_interpretation_invoked", False),
            ("navigation_decision_invoked", False),
            ("midplatform_fact_written", False),
            ("scene_delta_written", False),
            ("world_model_written", False),
        ):
            if aud.get(k) is not must:
                blockers.append(f"audit_flag_bad:{k}")

        sc_sum = _read_json(sc_p)
        if not isinstance(sc_sum.get("per_frame"), list) or len(sc_sum.get("per_frame")) == 0:
            blockers.append("source_chain_summary_empty")

    if blockers:
        verdict = "NO_GO"
    elif missing_crop:
        verdict = "CONDITIONAL_GO"
    else:
        verdict = "GO"

    rep = {
        "schema": "vision_roi_proposal_stub_verifier_report_v0",
        "phase": "Phase-Vision-Frame-ROI-Proposal-And-Segmentation-Stub-001",
        "governance_root": str(gov),
        "smoke_root": str(root),
        "verdict": verdict,
        "blockers": blockers,
        "soft_notes": soft,
        "roi_items_count": roi_count,
        "input_units_count": unit_count,
    }
    _write_json(root / "vision_roi_proposal_stub_verifier_report.json", rep)
    print(
        json.dumps(
            {"smoke_root": str(root), "verdict": verdict, "blockers": blockers, "soft_notes": soft},
            ensure_ascii=False,
        )
    )
    if verdict == "NO_GO":
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
