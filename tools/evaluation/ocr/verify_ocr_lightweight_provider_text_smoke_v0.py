#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for RapidOCR lightweight text smoke (Phase-OCR-Lightweight-Provider-Text-Smoke-001)."""

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


def _input_image_size(path: Path) -> Tuple[int, int]:
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

    img_p = root / "ocr_lightweight_provider_text_input.png"
    req_p = root / "ocr_lightweight_provider_text_request.json"
    res_p = root / "ocr_lightweight_provider_text_result.json"
    bp_p = root / "ocr_lightweight_provider_text_bridge_pack.json"
    aud_p = root / "ocr_lightweight_provider_text_audit_report.json"
    sum_p = root / "ocr_lightweight_provider_text_smoke_summary.json"

    for name, p in (
        ("input_png", img_p),
        ("request", req_p),
        ("result", res_p),
        ("bridge_pack", bp_p),
        ("audit", aud_p),
        ("summary", sum_p),
    ):
        if not p.is_file():
            blockers.append(f"missing:{name}")

    verdict = "NO_GO"
    if blockers:
        rep = {
            "schema": "ocr_lightweight_provider_text_verifier_report_v0",
            "phase": "Phase-OCR-Lightweight-Provider-Text-Smoke-001",
            "smoke_root": str(root),
            "verdict": verdict,
            "blockers": blockers,
        }
        _write_json(root / "ocr_lightweight_provider_text_verifier_report.json", rep)
        print(json.dumps({"smoke_root": str(root), "verdict": verdict, "blockers": blockers}, ensure_ascii=False))
        return 2

    iw, ih = _input_image_size(img_p)
    if iw > 512 or ih > 512:
        blockers.append("input_image_must_be_at_most_512_on_each_edge_for_this_smoke")

    res = _read_json(res_p)
    aud = _read_json(aud_p) if aud_p.is_file() else {}
    bp = _read_json(bp_p) if bp_p.is_file() else {}
    ev = res.get("ocr_evidence") if isinstance(res.get("ocr_evidence"), dict) else {}
    rep_sel = res.get("provider_selection_report") if isinstance(res.get("provider_selection_report"), dict) else {}
    reasons = "|".join(str(x) for x in (rep_sel.get("provider_selection_reason_codes") or []))

    blockers.extend(_forbidden_audit_true(aud))

    sel = str(aud.get("selected_provider") or "")
    real_inv = aud.get("real_provider_invoked") is True
    joined = str(ev.get("text_joined") or "").strip()
    items = ev.get("text_items") if isinstance(ev.get("text_items"), list) else []

    if sel == "rapidocr_candidate" and real_inv:
        if str(res.get("status") or "") != "success":
            blockers.append("status_must_be_success_when_rapid_invoked")
        if not joined:
            blockers.append("text_joined_must_be_non_empty_when_rapid_succeeds")
        if len(items) < 1:
            blockers.append("text_items_count_must_be_at_least_1")
        if str(bp.get("schema_version") or "") != "ocr_evidence_pack_candidate_v0":
            blockers.append("bridge_pack_missing_or_invalid")
        pt = bp.get("provider_trace") if isinstance(bp.get("provider_trace"), dict) else {}
        if str(pt.get("provider") or "") != "rapidocr_candidate":
            blockers.append("bridge_pack_provider_trace_must_be_rapidocr_candidate")
        verdict = "GO" if not blockers else "NO_GO"
    elif sel == "rapidocr_candidate" and not real_inv:
        blockers.append("rapid_selected_but_real_provider_not_invoked")
        verdict = "NO_GO"
    elif sel == "ocr_stub":
        if real_inv:
            blockers.append("stub_path_must_not_report_real_provider_invoked")
        explain = any(
            token in reasons
            for token in (
                "provider_runtime_unavailable",
                "import_failed",
                "rapidocr_import",
                "engine_init_failed",
                "lightweight_input_pack_rejected",
                "selected_stub_after_unavailable",
                "selected_stub_after_lightweight_reject",
            )
        )
        if not explain:
            blockers.append("stub_fallback_must_have_explainable_reason_in_selection_codes")
        verdict = "CONDITIONAL_GO" if not blockers else "NO_GO"
    else:
        blockers.append(f"unexpected_selected_provider:{sel or 'empty'}")
        verdict = "NO_GO"

    out_rep = {
        "schema": "ocr_lightweight_provider_text_verifier_report_v0",
        "phase": "Phase-OCR-Lightweight-Provider-Text-Smoke-001",
        "smoke_root": str(root),
        "verdict": verdict,
        "blockers": blockers,
        "input_width": iw,
        "input_height": ih,
        "selected_provider": sel,
        "real_provider_invoked": real_inv,
        "text_item_count": len(items),
    }
    _write_json(root / "ocr_lightweight_provider_text_verifier_report.json", out_rep)
    print(json.dumps({"smoke_root": str(root), "verdict": verdict, "blockers": blockers}, ensure_ascii=False))
    if verdict == "NO_GO":
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
