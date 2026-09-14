#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for RapidOCR on ROI provider input pack (Phase-OCR-Lightweight-Provider-ROI-Input-Smoke-001)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

WS_ROOT = Path(__file__).resolve().parents[3]


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


def _img_size(path: Path) -> Tuple[int, int]:
    if str(WS_ROOT) not in sys.path:
        sys.path.insert(0, str(WS_ROOT))
    from PIL import Image

    with Image.open(path) as im:
        return int(im.width), int(im.height)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke-root", required=True)
    args = ap.parse_args()

    root = _require_abs(args.smoke_root, "--smoke-root")
    blockers: List[str] = []

    img_p = root / "ocr_lightweight_provider_roi_input_original.png"
    roi_p = root / "ocr_lightweight_provider_roi_input_roi.png"
    req_p = root / "ocr_lightweight_provider_roi_input_request.json"
    res_p = root / "ocr_lightweight_provider_roi_input_result.json"
    pack_p = root / "ocr_lightweight_provider_roi_input_pack.json"
    bp_p = root / "ocr_lightweight_provider_roi_input_bridge_pack.json"
    aud_p = root / "ocr_lightweight_provider_roi_input_audit_report.json"
    sum_p = root / "ocr_lightweight_provider_roi_input_summary.json"

    for name, p in (
        ("original_png", img_p),
        ("roi_png", roi_p),
        ("request", req_p),
        ("result", res_p),
        ("pack", pack_p),
        ("bridge_pack", bp_p),
        ("audit", aud_p),
        ("summary", sum_p),
    ):
        if not p.is_file():
            blockers.append(f"missing:{name}")

    verdict = "NO_GO"
    if blockers:
        rep = {
            "schema": "ocr_lightweight_provider_roi_input_verifier_report_v0",
            "phase": "Phase-OCR-Lightweight-Provider-ROI-Input-Smoke-001",
            "smoke_root": str(root),
            "verdict": verdict,
            "blockers": blockers,
        }
        _write_json(root / "ocr_lightweight_provider_roi_input_verifier_report.json", rep)
        print(json.dumps({"smoke_root": str(root), "verdict": verdict, "blockers": blockers}, ensure_ascii=False))
        return 2

    res = _read_json(res_p)
    pack = _read_json(pack_p)
    aud = _read_json(aud_p)
    bp = _read_json(bp_p)
    ev = res.get("ocr_evidence") if isinstance(res.get("ocr_evidence"), dict) else {}
    rep_sel = res.get("provider_selection_report") if isinstance(res.get("provider_selection_report"), dict) else {}

    blockers.extend(_forbidden_audit_true(aud))

    units = pack.get("input_units") if isinstance(pack.get("input_units"), list) else []
    if len(units) != 1:
        blockers.append("pack_must_have_exactly_one_input_unit")
    u0 = units[0] if units and isinstance(units[0], dict) else {}
    if str(u0.get("unit_type") or "") != "roi":
        blockers.append("input_unit_type_must_be_roi")

    bb = u0.get("bbox_in_original")
    if not isinstance(bb, list) or len(bb) != 4:
        blockers.append("bbox_in_original_missing_or_invalid")

    tf = pack.get("coordinate_transform") if isinstance(pack.get("coordinate_transform"), dict) else {}
    if tf.get("offset_x") is None or tf.get("offset_y") is None:
        blockers.append("coordinate_transform_must_record_offset_x_offset_y")

    if aud.get("coordinate_transform_recorded") is not True:
        blockers.append("coordinate_transform_recorded_must_be_true")

    if aud.get("original_image_used_directly") is True:
        blockers.append("original_image_used_directly_must_not_be_true_for_roi_pack")

    sel = str(aud.get("selected_provider") or rep_sel.get("selected_provider") or "")
    codes_list = list(rep_sel.get("provider_selection_reason_codes") or aud.get("provider_selection_reason_codes") or [])

    joined = str(ev.get("text_joined") or "").strip()
    soft: List[str] = []
    verdict = "NO_GO"

    if sel == "rapidocr_candidate":
        if aud.get("real_provider_invoked") is not True:
            blockers.append("real_provider_invoked_must_be_true_when_rapid_selected")
        if not isinstance(bp, dict) or not bp.get("schema_version"):
            blockers.append("bridge_pack_missing_or_invalid_when_rapid_selected")
        if not blockers:
            if joined:
                verdict = "GO"
            else:
                verdict = "CONDITIONAL_GO"
                soft.append("rapidocr_invoked_but_text_empty")
    elif sel == "ocr_stub":
        explain = any(
            any(tok in str(c) for tok in ("unavailable", "import", "engine", "lightweight_input", "rejected_fallback_stub", "selected_stub_after"))
            for c in codes_list
        ) or bool(str(aud.get("provider_unavailable_reason") or rep_sel.get("provider_unavailable_reason") or "").strip())
        if not explain:
            blockers.append("stub_fallback_must_be_explained")
        if not blockers:
            verdict = "CONDITIONAL_GO"
            soft.append("stub_fallback_path")
    else:
        blockers.append(f"unexpected_selected_provider:{sel or 'empty'}")

    rep = {
        "schema": "ocr_lightweight_provider_roi_input_verifier_report_v0",
        "phase": "Phase-OCR-Lightweight-Provider-ROI-Input-Smoke-001",
        "smoke_root": str(root),
        "verdict": "NO_GO" if blockers else verdict,
        "blockers": blockers,
        "soft_notes": soft,
        "original_image_size": list(_img_size(img_p)),
        "roi_image_size": list(_img_size(roi_p)) if roi_p.is_file() else [],
        "unit_type": u0.get("unit_type"),
        "selected_provider": sel or None,
        "real_provider_invoked": aud.get("real_provider_invoked"),
        "text_joined_non_empty": bool(joined),
        "text_item_count": len(ev.get("text_items") or []) if isinstance(ev.get("text_items"), list) else 0,
        "coordinate_transform": {
            "offset_x": tf.get("offset_x"),
            "offset_y": tf.get("offset_y"),
            "mode": tf.get("mode"),
        },
        "provider_selection_reason_codes": codes_list,
    }
    _write_json(root / "ocr_lightweight_provider_roi_input_verifier_report.json", rep)
    final = str(rep["verdict"])
    print(json.dumps({"smoke_root": str(root), "verdict": final, "blockers": blockers}, ensure_ascii=False))
    if final == "NO_GO":
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
