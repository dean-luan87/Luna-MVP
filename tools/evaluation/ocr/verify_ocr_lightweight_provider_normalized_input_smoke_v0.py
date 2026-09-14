#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for RapidOCR on normalized downscaled input pack (Phase-OCR-Lightweight-Provider-Normalized-Input-Smoke-001)."""

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
    ap.add_argument("--lightweight-max-edge", type=int, default=512)
    args = ap.parse_args()

    root = _require_abs(args.smoke_root, "--smoke-root")
    cap = int(args.lightweight_max_edge)
    blockers: List[str] = []

    img_p = root / "ocr_lightweight_provider_normalized_input_original.png"
    req_p = root / "ocr_lightweight_provider_normalized_input_request.json"
    res_p = root / "ocr_lightweight_provider_normalized_input_result.json"
    pack_p = root / "ocr_lightweight_provider_normalized_input_pack.json"
    bp_p = root / "ocr_lightweight_provider_normalized_input_bridge_pack.json"
    aud_p = root / "ocr_lightweight_provider_normalized_input_audit_report.json"
    sum_p = root / "ocr_lightweight_provider_normalized_input_summary.json"

    for name, p in (
        ("original_png", img_p),
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
            "schema": "ocr_lightweight_provider_normalized_input_verifier_report_v0",
            "phase": "Phase-OCR-Lightweight-Provider-Normalized-Input-Smoke-001",
            "smoke_root": str(root),
            "verdict": verdict,
            "blockers": blockers,
        }
        _write_json(root / "ocr_lightweight_provider_normalized_input_verifier_report.json", rep)
        print(json.dumps({"smoke_root": str(root), "verdict": verdict, "blockers": blockers}, ensure_ascii=False))
        return 2

    ow, oh = _img_size(img_p)
    if max(ow, oh) <= cap:
        blockers.append(f"original_image_expected_above_lightweight_cap_{cap}_got_{ow}x{oh}")

    res = _read_json(res_p)
    pack = _read_json(pack_p)
    aud = _read_json(aud_p)
    bp = _read_json(bp_p)
    ev = res.get("ocr_evidence") if isinstance(res.get("ocr_evidence"), dict) else {}
    rep_sel = res.get("provider_selection_report") if isinstance(res.get("provider_selection_report"), dict) else {}
    reasons = "|".join(str(x) for x in (rep_sel.get("provider_selection_reason_codes") or []))

    blockers.extend(_forbidden_audit_true(aud))

    if aud.get("downscale_applied") is not True:
        blockers.append("downscale_applied_must_be_true")
    if aud.get("original_image_used_directly") is not False:
        blockers.append("original_image_used_directly_must_be_false")
    if aud.get("coordinate_transform_recorded") is not True:
        blockers.append("coordinate_transform_recorded_must_be_true")

    units = pack.get("input_units") if isinstance(pack.get("input_units"), list) else []
    if len(units) != 1:
        blockers.append("pack_must_have_exactly_one_input_unit")
    u0 = units[0] if units and isinstance(units[0], dict) else {}
    if str(u0.get("unit_type") or "") != "downscaled_full_image":
        blockers.append("unit_type_must_be_downscaled_full_image")
    uw, uh = int(u0.get("width") or 0), int(u0.get("height") or 0)
    img_ref = str(u0.get("image_ref") or "")
    if img_ref and Path(img_ref).resolve() == img_p.resolve():
        blockers.append("normalized_unit_image_ref_must_not_equal_original_oversized_image_path")
    if uw > cap or uh > cap:
        blockers.append(f"normalized_unit_exceeds_lightweight_cap_{cap}_got_{uw}x{uh}")

    sel = str(aud.get("selected_provider") or "")
    real_inv = aud.get("real_provider_invoked") is True
    joined = str(ev.get("text_joined") or "").strip()
    items = ev.get("text_items") if isinstance(ev.get("text_items"), list) else []

    if sel == "rapidocr_candidate" and real_inv:
        if str(res.get("status") or "") != "success":
            blockers.append("status_must_be_success")
        if str(bp.get("schema_version") or "") != "ocr_evidence_pack_candidate_v0":
            blockers.append("bridge_pack_invalid")
        if joined and len(items) >= 1:
            verdict = "GO" if not blockers else "NO_GO"
        else:
            verdict = "CONDITIONAL_GO" if not blockers else "NO_GO"
    elif sel == "ocr_stub":
        explain = any(
            t in reasons
            for t in (
                "provider_runtime_unavailable",
                "import",
                "engine_init",
                "lightweight_input_pack",
                "selected_stub_after_unavailable",
            )
        )
        if not explain:
            blockers.append("stub_fallback_must_be_explained")
        verdict = "CONDITIONAL_GO" if not blockers else "NO_GO"
    else:
        blockers.append(f"unexpected_selected_provider:{sel}")
        verdict = "NO_GO"

    out_rep = {
        "schema": "ocr_lightweight_provider_normalized_input_verifier_report_v0",
        "phase": "Phase-OCR-Lightweight-Provider-Normalized-Input-Smoke-001",
        "smoke_root": str(root),
        "verdict": verdict,
        "blockers": blockers,
        "original_width": ow,
        "original_height": oh,
        "normalized_unit_width": uw,
        "normalized_unit_height": uh,
        "selected_provider": sel,
        "real_provider_invoked": real_inv,
        "text_item_count": len(items),
        "text_joined_non_empty": bool(joined),
    }
    _write_json(root / "ocr_lightweight_provider_normalized_input_verifier_report.json", out_rep)
    print(json.dumps({"smoke_root": str(root), "verdict": verdict, "blockers": blockers}, ensure_ascii=False))
    if verdict == "NO_GO":
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
