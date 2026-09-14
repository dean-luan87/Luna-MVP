#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for OCR tile coverage / truncation policy (Phase-OCR-Tile-Coverage-And-Truncation-Policy-001)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

WS_ROOT = Path(__file__).resolve().parents[3]
if str(WS_ROOT) not in sys.path:
    sys.path.insert(0, str(WS_ROOT))


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
        "real_provider_invoked",
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

    res_p = root / "ocr_mainline_bridge_result.json"
    plan_p = root / "ocr_tile_plan.json"
    pack_p = root / "ocr_provider_input_pack.json"
    sum_p = root / "ocr_tile_coverage_summary.json"
    unc_p = root / "ocr_tile_uncovered_regions.json"
    aud_p = root / "ocr_tile_coverage_audit_report.json"

    for name, p in (("result", res_p), ("tile_plan", plan_p), ("pack", pack_p), ("coverage_summary", sum_p), ("uncovered", unc_p), ("audit", aud_p)):
        if not p.is_file():
            blockers.append(f"missing:{name}")

    if blockers:
        rep = {"schema": "ocr_tile_coverage_verifier_report_v0", "smoke_root": str(root), "verdict": "NO_GO", "blockers": blockers}
        _write_json(root / "ocr_tile_coverage_verifier_report.json", rep)
        print(json.dumps(rep, ensure_ascii=False))
        return 2

    res = _read_json(res_p)
    plan = _read_json(plan_p)
    pack = _read_json(pack_p)
    cov = _read_json(sum_p)
    unc = _read_json(unc_p)
    aud = _read_json(aud_p)

    raw_c = int(plan.get("raw_tile_count") or cov.get("raw_tile_count") or -1)
    mat_c = int(plan.get("materialized_tile_count") or cov.get("materialized_tile_count") or -1)
    if raw_c < 0 or mat_c < 0:
        blockers.append("missing_raw_or_materialized_tile_count")

    if mat_c < raw_c:
        if plan.get("coverage_complete") is True or cov.get("coverage_complete") is True:
            blockers.append("must_not_coverage_complete_when_truncated")
        if plan.get("truncated_to_budget") is not True and cov.get("truncated_to_budget") is not True:
            blockers.append("truncated_to_budget_must_be_true_when_partial")
        pol = pack.get("processing_policy") if isinstance(pack.get("processing_policy"), dict) else {}
        if pol.get("evidence_scope") != "partial_image":
            blockers.append("evidence_scope_must_be_partial_image_when_partial")
        if pol.get("full_image_claim_allowed") is True:
            blockers.append("full_image_claim_must_be_false_when_partial")
        ev = res.get("ocr_evidence") if isinstance(res.get("ocr_evidence"), dict) else {}
        if ev.get("evidence_scope") != "partial_image":
            blockers.append("ocr_evidence_missing_partial_scope")
        bp = res.get("bridge_pack") if isinstance(res.get("bridge_pack"), dict) else {}
        if bp.get("evidence_scope") != "partial_image":
            blockers.append("bridge_pack_missing_partial_scope")
        if not str(ev.get("text_joined") or "").strip().startswith("[PARTIAL_TILE_EVIDENCE"):
            blockers.append("text_joined_must_disclose_partial_stub")
        if aud.get("tile_truncated_to_budget") is not True:
            blockers.append("audit_tile_truncated_to_budget_when_partial")

    schain = pack.get("source_chain") if isinstance(pack.get("source_chain"), list) else []
    for token in ("tile_plan_raw_count:", "tile_materialized_count:", "tile_truncated_to_budget:", "coverage_complete:"):
        if not any(isinstance(s, str) and token in s for s in schain):
            blockers.append(f"source_chain_missing:{token}")

    if aud.get("partial_evidence_scope_recorded") is not True:
        blockers.append("audit_partial_evidence_scope_recorded")
    if aud.get("tile_coverage_complete") is True and mat_c < raw_c:
        blockers.append("audit_tile_coverage_complete_inconsistent")

    blockers.extend(_forbidden_audit_true(aud))

    verdict = "GO" if not blockers else "NO_GO"
    rep = {
        "schema": "ocr_tile_coverage_verifier_report_v0",
        "phase": "Phase-OCR-Tile-Coverage-And-Truncation-Policy-001",
        "smoke_root": str(root),
        "verdict": verdict,
        "blockers": blockers,
    }
    _write_json(root / "ocr_tile_coverage_verifier_report.json", rep)
    print(json.dumps({"smoke_root": str(root), "verdict": verdict, "blockers": blockers}, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
