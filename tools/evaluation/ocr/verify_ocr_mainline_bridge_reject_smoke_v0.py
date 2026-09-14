#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for OCR mainline bridge REJECT (oversized) smoke."""

from __future__ import annotations

import argparse
import json
import sys
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


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke-root", required=True)
    args = ap.parse_args()

    root = _require_abs(args.smoke_root, "--smoke-root")
    blockers: List[str] = []

    req_p = root / "ocr_mainline_bridge_reject_request.json"
    res_p = root / "ocr_mainline_bridge_reject_result.json"
    sum_p = root / "ocr_mainline_bridge_reject_smoke_summary.json"
    aud_p = root / "ocr_mainline_bridge_reject_audit_report.json"

    for name, p in (
        ("request", req_p),
        ("result", res_p),
        ("summary", sum_p),
        ("audit", aud_p),
    ):
        if not p.is_file():
            blockers.append(f"missing:{name}")

    req: Dict[str, Any] = _read_json(req_p) if req_p.is_file() else {}
    res: Dict[str, Any] = _read_json(res_p) if res_p.is_file() else {}

    if sum_p.is_file():
        sm = _read_json(sum_p)
        if not sm.get("image_width") or not sm.get("image_height"):
            blockers.append("summary_missing_image_dimensions")

    ig = res.get("input_gate") if isinstance(res.get("input_gate"), dict) else {}
    if ig.get("gate_verdict") != "REJECT":
        blockers.append("gate_verdict_must_be_REJECT")
    if ig.get("oversized") is not True:
        blockers.append("oversized_must_be_true")
    strat = str(ig.get("recommended_input_strategy") or "")
    if strat not in ("downscale_required", "tile_required"):
        blockers.append("recommended_strategy_must_be_downscale_or_tile")

    if str(res.get("status") or "") != "rejected":
        blockers.append("bridge_status_must_be_rejected")

    prov = res.get("provider_result") if isinstance(res.get("provider_result"), dict) else {}
    if prov.get("provider") == "ocr_stub" or prov.get("text_joined") == "MOCK_TEXT":
        blockers.append("provider_must_not_be_invoked")

    ev = res.get("ocr_evidence") if isinstance(res.get("ocr_evidence"), dict) else {}
    tj = str(ev.get("text_joined") or "")
    if "MOCK_TEXT" in json.dumps(ev, ensure_ascii=False):
        blockers.append("evidence_must_not_contain_MOCK_TEXT")
    if tj.strip() == "MOCK_TEXT":
        blockers.append("evidence_text_joined_must_not_be_MOCK")

    bp = res.get("bridge_pack") if isinstance(res.get("bridge_pack"), dict) else {}
    if str(bp.get("pack_status") or "") != "rejected_no_evidence":
        blockers.append("bridge_pack_must_be_rejected_no_evidence")
    if "MOCK_TEXT" in json.dumps(bp, ensure_ascii=False):
        blockers.append("bridge_pack_must_not_contain_MOCK_TEXT")
    if str(bp.get("raw_text_joined") or "").strip() == "MOCK_TEXT":
        blockers.append("bridge_pack_raw_joined_must_not_be_MOCK")

    if req.get("allow_full_image") is True:
        blockers.append("allow_full_image_must_be_false_for_this_smoke")

    aud = res.get("audit") if isinstance(res.get("audit"), dict) else (_read_json(aud_p) if aud_p.is_file() else {})
    for k in (
        "real_provider_invoked",
        "paddleocr_invoked",
        "rapidocr_replaced",
        "ocr_routing_changed",
        "midplatform_invoked",
        "world_model_written",
    ):
        if aud.get(k) is True:
            blockers.append(f"audit_forbidden_true:{k}")

    verdict = "GO" if not blockers else "NO_GO"

    rep = {
        "schema": "ocr_mainline_bridge_reject_smoke_verifier_report_v0",
        "phase": "Phase-OCR-Mainline-InputGate-Reject-Smoke-001",
        "smoke_root": str(root),
        "verdict": verdict,
        "blockers": blockers,
    }
    _write_json(root / "ocr_mainline_bridge_reject_smoke_verifier_report.json", rep)
    print(json.dumps({"smoke_root": str(root), "verdict": verdict, "blockers": blockers}, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
