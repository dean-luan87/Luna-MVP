#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for ROI OCR coordinate lift (Phase-OCR-ROI-Evidence-Coordinate-Lift-001)."""

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
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _forbidden_audit_true(aud: Dict[str, Any]) -> List[str]:
    bad: List[str] = []
    for k in (
        "paddleocr_invoked",
        "rapidocr_replaced",
        "ocr_routing_changed",
        "midplatform_invoked",
        "world_model_written",
    ):
        if aud.get(k) is True:
            bad.append(f"audit_forbidden_true:{k}")
    return bad


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke-root", required=True)
    args = ap.parse_args()

    root = _require_abs(args.smoke_root, "--smoke-root")
    blockers: List[str] = []

    sum_p = root / "ocr_roi_coordinate_lift_summary.json"
    items_p = root / "ocr_roi_coordinate_lift_items.json"
    bp_p = root / "ocr_roi_coordinate_lift_bridge_pack.json"
    aud_p = root / "ocr_roi_coordinate_lift_audit_report.json"

    for name, p in (
        ("summary", sum_p),
        ("items", items_p),
        ("bridge_pack", bp_p),
        ("audit", aud_p),
    ):
        if not p.is_file():
            blockers.append(f"missing:{name}")

    verdict = "NO_GO"
    if blockers:
        rep = {
            "schema": "ocr_roi_coordinate_lift_verifier_report_v0",
            "phase": "Phase-OCR-ROI-Evidence-Coordinate-Lift-001",
            "smoke_root": str(root),
            "verdict": verdict,
            "blockers": blockers,
        }
        _write_json(root / "ocr_roi_coordinate_lift_verifier_report.json", rep)
        print(json.dumps({"smoke_root": str(root), "verdict": verdict, "blockers": blockers}, ensure_ascii=False))
        return 2

    summary = _read_json(sum_p)
    items = _read_json(items_p)
    bp = _read_json(bp_p)
    aud = _read_json(aud_p)

    blockers.extend(_forbidden_audit_true(aud))

    pol = summary.get("input_pack_processing_policy") if isinstance(summary.get("input_pack_processing_policy"), dict) else {}
    if str(pol.get("strategy") or "") != "roi":
        blockers.append("summary_must_record_roi_input_pack_strategy")

    tf = summary.get("coordinate_transform") if isinstance(summary.get("coordinate_transform"), dict) else {}
    for k in ("offset_x", "offset_y", "scale_x", "scale_y"):
        if k not in tf:
            blockers.append(f"missing_coordinate_transform_field:{k}")

    geom_unavail = aud.get("provider_geometry_unavailable") is True
    geom_avail = aud.get("provider_geometry_available") is True
    lift_applied = aud.get("roi_coordinate_lift_applied") is True
    orig_recorded = aud.get("original_geometry_recorded") is True

    if geom_avail and geom_unavail:
        blockers.append("inconsistent_geometry_flags")

    item_list = items if isinstance(items, list) else []
    any_lifted_item = False
    forged = False
    for it in item_list:
        if not isinstance(it, dict):
            continue
        if it.get("coordinate_lift_applied") is True:
            any_lifted_item = True
            ob = it.get("original_bbox")
            op = it.get("original_polygon")
            if ob is None and not (isinstance(op, list) and len(op) > 0):
                forged = True

    if forged:
        blockers.append("coordinate_lift_applied_without_original_geometry")

    elig = bp.get("eligible_text_evidence") if isinstance(bp.get("eligible_text_evidence"), list) else []
    if item_list and str(bp.get("schema_version") or "") == "ocr_evidence_pack_candidate_v0":
        if not elig:
            blockers.append("bridge_pack_eligible_text_evidence_required_for_roi")

    soft: List[str] = []
    if blockers:
        verdict = "NO_GO"
    elif geom_unavail and not geom_avail:
        verdict = "CONDITIONAL_GO"
        soft.append("provider_geometry_unavailable")
    elif lift_applied and orig_recorded and any_lifted_item and not geom_unavail:
        lifted = [
            it
            for it in item_list
            if isinstance(it, dict) and it.get("coordinate_lift_applied") is True
        ]
        all_have_orig = bool(lifted) and all(
            it.get("original_bbox") is not None
            or (isinstance(it.get("original_polygon"), list) and len(it.get("original_polygon") or []) > 0)
            for it in lifted
        )
        if all_have_orig and elig:
            elig_ok = True
            for e in elig:
                if not isinstance(e, dict) or e.get("coordinate_lift_applied") is not True:
                    continue
                eb = e.get("original_bbox")
                ep = e.get("original_polygon")
                if eb is None and not (isinstance(ep, list) and len(ep) > 0):
                    elig_ok = False
                    break
            verdict = "GO" if elig_ok else "CONDITIONAL_GO"
            if not elig_ok:
                soft.append("eligible_original_geometry_mismatch")
        elif all_have_orig and not elig:
            verdict = "CONDITIONAL_GO"
            soft.append("missing_eligible_text_evidence")
        else:
            verdict = "CONDITIONAL_GO"
            soft.append("lift_or_geometry_incomplete")
    else:
        verdict = "CONDITIONAL_GO"
        soft.append("audit_or_flags_incomplete")

    rep = {
        "schema": "ocr_roi_coordinate_lift_verifier_report_v0",
        "phase": "Phase-OCR-ROI-Evidence-Coordinate-Lift-001",
        "smoke_root": str(root),
        "verdict": verdict,
        "blockers": blockers,
        "soft_notes": soft,
        "audit_roi_lift": {
            "roi_coordinate_lift_applied": lift_applied,
            "provider_geometry_available": geom_avail,
            "original_geometry_recorded": orig_recorded,
            "provider_geometry_unavailable": geom_unavail,
        },
    }
    _write_json(root / "ocr_roi_coordinate_lift_verifier_report.json", rep)
    print(json.dumps({"smoke_root": str(root), "verdict": verdict, "blockers": blockers}, ensure_ascii=False))
    if verdict == "NO_GO":
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
