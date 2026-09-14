#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for multi-ROI OCR smoke (Phase-OCR-Lightweight-Provider-Multi-ROI-Smoke-001)."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List, Set


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

    pack_p = root / "ocr_lightweight_provider_multi_roi_input_pack.json"
    res_p = root / "ocr_lightweight_provider_multi_roi_result.json"
    sum_p = root / "ocr_lightweight_provider_multi_roi_smoke_summary.json"
    bp_p = root / "ocr_lightweight_provider_multi_roi_bridge_pack.json"
    aud_p = root / "ocr_lightweight_provider_multi_roi_audit_report.json"

    for name, p in (
        ("pack", pack_p),
        ("result", res_p),
        ("summary", sum_p),
        ("bridge_pack", bp_p),
        ("audit", aud_p),
    ):
        if not p.is_file():
            blockers.append(f"missing:{name}")

    verdict = "NO_GO"
    if blockers:
        rep = {
            "schema": "ocr_lightweight_provider_multi_roi_verifier_report_v0",
            "phase": "Phase-OCR-Lightweight-Provider-Multi-ROI-Smoke-001",
            "smoke_root": str(root),
            "verdict": verdict,
            "blockers": blockers,
        }
        _write_json(root / "ocr_lightweight_provider_multi_roi_verifier_report.json", rep)
        print(json.dumps({"smoke_root": str(root), "verdict": verdict, "blockers": blockers}, ensure_ascii=False))
        return 2

    pack = _read_json(pack_p)
    res = _read_json(res_p)
    aud = _read_json(aud_p)
    bp = _read_json(bp_p)
    ev = res.get("ocr_evidence") if isinstance(res.get("ocr_evidence"), dict) else {}

    blockers.extend(_forbidden_audit_true(aud))

    units = pack.get("input_units") if isinstance(pack.get("input_units"), list) else []
    if len(units) < 2:
        blockers.append("input_units_count_must_be_at_least_2")
    for i, u in enumerate(units):
        if not isinstance(u, dict) or str(u.get("unit_type") or "") != "roi":
            blockers.append(f"unit_{i}_must_be_roi")
            continue
        bb = u.get("bbox_in_original")
        if not isinstance(bb, list) or len(bb) != 4:
            blockers.append(f"unit_{i}_missing_bbox_in_original")
        if not str(u.get("roi_id") or "").strip():
            blockers.append(f"unit_{i}_missing_roi_id")
        if not str(u.get("unit_id") or "").strip():
            blockers.append(f"unit_{i}_missing_unit_id")

    pol = pack.get("processing_policy") if isinstance(pack.get("processing_policy"), dict) else {}
    if str(pol.get("strategy") or "") != "roi_list":
        blockers.append("pack_strategy_must_be_roi_list")

    items = ev.get("text_items") if isinstance(ev.get("text_items"), list) else []
    refs: Set[str] = set()
    for it in items:
        if not isinstance(it, dict):
            continue
        ref = str(it.get("source_unit_ref") or "")
        if not ref.startswith("/"):
            blockers.append("text_item_missing_source_unit_ref")
        refs.add(ref)
    unit_refs = {str(u.get("image_ref") or "") for u in units if isinstance(u, dict)}
    for r in refs:
        if r and r not in unit_refs:
            blockers.append(f"orphan_source_unit_ref:{r}")

    geom_ok = True
    for it in items:
        if not isinstance(it, dict):
            continue
        has_local = it.get("local_bbox") is not None or (
            isinstance(it.get("local_polygon"), list) and len(it.get("local_polygon") or []) > 0
        )
        has_orig = it.get("original_bbox") is not None or (
            isinstance(it.get("original_polygon"), list) and len(it.get("original_polygon") or []) > 0
        )
        if has_local and not (it.get("coordinate_lift_applied") is True and has_orig):
            geom_ok = False
            break

    if items and not geom_ok:
        blockers.append("geometry_lift_incomplete_when_local_geometry_present")

    joined = str(ev.get("text_joined") or "").strip()
    per_roi = ev.get("per_roi_provider_status") if isinstance(ev.get("per_roi_provider_status"), list) else []
    if not per_roi:
        pr = res.get("provider_result") if isinstance(res.get("provider_result"), dict) else {}
        per_roi = (pr.get("provider_raw_ref") or {}).get("per_roi_provider_status") or []

    soft: List[str] = []
    if blockers:
        verdict = "NO_GO"
    elif not joined:
        verdict = "CONDITIONAL_GO"
        soft.append("text_joined_empty")
    elif not per_roi:
        verdict = "CONDITIONAL_GO"
        soft.append("missing_per_roi_provider_status")
    elif len({str(x.get("source_unit_ref") or "") for x in per_roi if isinstance(x, dict)}) < 2:
        verdict = "CONDITIONAL_GO"
        soft.append("per_roi_status_missing_distinct_refs")
    else:
        verdict = "GO"
        if str(bp.get("schema_version") or "") != "ocr_evidence_pack_candidate_v0":
            verdict = "CONDITIONAL_GO"
            soft.append("bridge_pack_schema_unexpected")
        elig = bp.get("eligible_text_evidence") if isinstance(bp.get("eligible_text_evidence"), list) else []
        if not elig:
            verdict = "CONDITIONAL_GO"
            soft.append("eligible_text_evidence_empty")

    rep = {
        "schema": "ocr_lightweight_provider_multi_roi_verifier_report_v0",
        "phase": "Phase-OCR-Lightweight-Provider-Multi-ROI-Smoke-001",
        "smoke_root": str(root),
        "verdict": verdict,
        "blockers": blockers,
        "soft_notes": soft,
        "input_units_count": len(units),
        "text_item_count": len(items),
        "text_joined_non_empty": bool(joined),
        "selected_provider": aud.get("selected_provider"),
        "multi_roi_processed": aud.get("multi_roi_processed"),
        "roi_unit_count": aud.get("roi_unit_count"),
    }
    _write_json(root / "ocr_lightweight_provider_multi_roi_verifier_report.json", rep)
    print(json.dumps({"smoke_root": str(root), "verdict": verdict, "blockers": blockers}, ensure_ascii=False))
    if verdict == "NO_GO":
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
