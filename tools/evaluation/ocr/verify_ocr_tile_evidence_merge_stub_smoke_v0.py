#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for OCR tile evidence merge stub smoke (Phase-OCR-Tile-Evidence-Merge-Stub-001)."""

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
    items_p = root / "ocr_tile_evidence_items.json"
    bp_p = root / "ocr_tile_evidence_bridge_pack.json"
    chain_p = root / "ocr_tile_evidence_source_chain.json"
    aud_p = root / "ocr_tile_evidence_audit_report.json"

    for name, p in (("result", res_p), ("items", items_p), ("bridge_pack", bp_p), ("chain", chain_p), ("audit", aud_p)):
        if not p.is_file():
            blockers.append(f"missing:{name}")

    if blockers:
        rep = {"schema": "ocr_tile_evidence_merge_stub_verifier_report_v0", "smoke_root": str(root), "verdict": "NO_GO", "blockers": blockers}
        _write_json(root / "ocr_tile_evidence_merge_stub_verifier_report.json", rep)
        print(json.dumps(rep, ensure_ascii=False))
        return 2

    res = _read_json(res_p)
    items_doc = _read_json(items_p)
    bp = _read_json(bp_p)
    chain_doc = _read_json(chain_p)
    aud = _read_json(aud_p)
    ev = res.get("ocr_evidence") if isinstance(res.get("ocr_evidence"), dict) else {}

    items = items_doc.get("tile_evidence_items") if isinstance(items_doc.get("tile_evidence_items"), list) else []
    mat = int((res.get("ocr_provider_input_pack") or {}).get("tile_coverage", {}).get("materialized_tile_count") or 0)
    if mat <= 0:
        mat = len(items)

    if not items:
        blockers.append("missing_tile_evidence_items")
    if len(items) != mat:
        blockers.append("tile_evidence_count_mismatch_materialized")

    for i, it in enumerate(items):
        if not isinstance(it, dict):
            blockers.append(f"item_{i}_not_dict")
            continue
        if not str(it.get("tile_id") or "").strip():
            blockers.append(f"item_{i}_missing_tile_id")
        if not str(it.get("source_unit_ref") or "").strip():
            blockers.append(f"item_{i}_missing_source_unit_ref")
        ob = it.get("original_bbox")
        op = it.get("original_polygon")
        if not (isinstance(ob, list) and len(ob) == 4) and not (isinstance(op, list) and len(op) >= 3):
            blockers.append(f"item_{i}_missing_original_geometry")
        if it.get("coordinate_transform_applied") is not True:
            blockers.append(f"item_{i}_coordinate_transform_applied")

    cov = (res.get("ocr_provider_input_pack") or {}).get("tile_coverage") or {}
    if cov.get("coverage_complete") is False:
        if ev.get("evidence_scope") != "partial_image":
            blockers.append("evidence_scope_must_be_partial_image")
        if ev.get("full_image_claim_allowed") is True:
            blockers.append("full_image_claim_must_be_false")
        tj = str(ev.get("text_joined") or "")
        if not tj.strip().startswith("[PARTIAL_TILE_EVIDENCE"):
            blockers.append("text_joined_must_have_partial_disclosure")

    if not isinstance(ev.get("partial_evidence_completion"), dict):
        blockers.append("ocr_evidence_missing_partial_evidence_completion_stub")
    else:
        pec = ev["partial_evidence_completion"]
        if pec.get("completion_candidates") != []:
            blockers.append("completion_candidates_must_be_empty_in_stub_v0")
        if pec.get("completion_allowed") is True:
            blockers.append("completion_allowed_must_be_false_stub_v0")

    if not isinstance(bp.get("partial_evidence_completion"), dict):
        blockers.append("bridge_pack_missing_partial_evidence_completion_stub")

    if not isinstance(bp.get("tile_evidence_summary"), dict):
        blockers.append("bridge_pack_missing_tile_evidence_summary")

    schain = chain_doc.get("source_chain") if isinstance(chain_doc.get("source_chain"), list) else []
    for tok in ("tile_evidence_merged", "coordinate_reconstruction_applied"):
        if tok not in schain:
            blockers.append(f"source_chain_missing:{tok}")

    if aud.get("coordinate_reconstruction_applied") is not True:
        blockers.append("audit_coordinate_reconstruction_applied")
    if aud.get("tile_evidence_generated") is not True:
        blockers.append("audit_tile_evidence_generated")

    blockers.extend(_forbidden_audit_true(aud))

    verdict = "GO" if not blockers else "NO_GO"
    rep = {
        "schema": "ocr_tile_evidence_merge_stub_verifier_report_v0",
        "phase": "Phase-OCR-Tile-Evidence-Merge-Stub-001",
        "smoke_root": str(root),
        "verdict": verdict,
        "blockers": blockers,
    }
    _write_json(root / "ocr_tile_evidence_merge_stub_verifier_report.json", rep)
    print(json.dumps({"smoke_root": str(root), "verdict": verdict, "blockers": blockers}, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
