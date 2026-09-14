#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for OCR mainline bridge smoke outputs (Phase-OCR-Mainline-Minimal-Bridge-001)."""

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
    ap.add_argument("--request-json", default="", help="Path to ocr_mainline_bridge_request.json for allow_full_image cross-check")
    args = ap.parse_args()

    root = _require_abs(args.smoke_root, "--smoke-root")
    blockers: List[str] = []

    req_p = root / "ocr_mainline_bridge_request.json"
    res_p = root / "ocr_mainline_bridge_result.json"
    sum_p = root / "ocr_mainline_bridge_smoke_summary.json"
    aud_p = root / "ocr_mainline_bridge_audit_report.json"

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

    if not str(req.get("request_id") or "").strip():
        blockers.append("missing_request_id")
    if not str(req.get("trace_id") or "").strip():
        blockers.append("missing_trace_id")

    ig = res.get("input_gate") if isinstance(res.get("input_gate"), dict) else {}
    if not ig:
        blockers.append("missing_input_gate_output")

    st = str(res.get("status") or "")
    if st not in ("success", "rejected", "timeout", "error"):
        blockers.append("invalid_status")

    if st == "success":
        ev = res.get("ocr_evidence") if isinstance(res.get("ocr_evidence"), dict) else {}
        if not ev:
            blockers.append("missing_ocr_evidence_on_success")
        bp = res.get("bridge_pack") if isinstance(res.get("bridge_pack"), dict) else {}
        if not bp or str(bp.get("schema_version") or "") != "ocr_evidence_pack_candidate_v0":
            blockers.append("missing_or_invalid_bridge_pack")

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

    allow_full = bool(req.get("allow_full_image"))
    oversized = bool(ig.get("oversized"))
    strat = str(ig.get("recommended_input_strategy") or "")
    if oversized and not allow_full and strat == "full_image_allowed":
        blockers.append("oversized_must_not_recommend_full_image_when_disallowed")

    verdict = "GO" if not blockers else "NO_GO"

    rep = {
        "schema": "ocr_mainline_bridge_smoke_verifier_report_v0",
        "phase": "Phase-OCR-Mainline-Minimal-Bridge-001",
        "smoke_root": str(root),
        "verdict": verdict,
        "blockers": blockers,
    }
    _write_json(root / "ocr_mainline_bridge_smoke_verifier_report.json", rep)
    print(json.dumps({"smoke_root": str(root), "verdict": verdict, "blockers": blockers}, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
