#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for Poster Layout Segmentation Governance v0."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List


FORBIDDEN_OCR_PLAN_REGIONS = frozenset(
    {"logo_area", "qr_area", "product_or_decoration_area", "background_or_decoration_area", "qr_or_logo_area"}
)


def _find_ws_root() -> Path:
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "capabilities" / "ocr_runtime").is_dir():
            if str(parent) not in sys.path:
                sys.path.insert(0, str(parent))
            return parent
    return here.parents[3]


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


def _risk_ids(doc: Dict[str, Any]) -> set:
    risks = doc.get("risks") if isinstance(doc.get("risks"), list) else []
    return {r.get("risk_id") for r in risks if isinstance(r, dict)}


def main() -> int:
    _find_ws_root()
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke-root", required=True)
    args = ap.parse_args()

    root = _require_abs(args.smoke_root, "--smoke-root")
    blockers: List[str] = []

    paths = {
        "summary": root / "poster_layout_governance_summary.json",
        "layout": root / "poster_layout_candidate.json",
        "text": root / "poster_text_region_candidates.json",
        "non_text": root / "poster_non_text_region_candidates.json",
        "visual": root / "poster_visual_symbol_candidates.json",
        "ocr_plan": root / "poster_ocr_region_plan.json",
        "reading": root / "poster_reading_order_candidate.json",
        "risks": root / "poster_layout_risk_report.json",
        "gate": root / "poster_layout_gate_policy_report.json",
        "audit": root / "poster_layout_governance_audit_report.json",
    }

    for label, p in paths.items():
        if not p.is_file():
            blockers.append(f"missing:{label}")

    if blockers:
        rep = {
            "schema": "poster_layout_governance_verifier_report_v0",
            "phase": "OCR-Poster-Layout-Segmentation-Governance-001",
            "smoke_root": str(root),
            "verdict": "NO_GO",
            "blockers": blockers,
        }
        _write_json(root / "poster_layout_governance_verifier_report.json", rep)
        print(json.dumps({"smoke_root": str(root), "verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    summary = _read_json(paths["summary"])
    layout = _read_json(paths["layout"])
    text_doc = _read_json(paths["text"])
    non_text_doc = _read_json(paths["non_text"])
    visual_doc = _read_json(paths["visual"])
    ocr_plan = _read_json(paths["ocr_plan"])
    reading = _read_json(paths["reading"])
    risks_doc = _read_json(paths["risks"])
    gate = _read_json(paths["gate"])
    aud = _read_json(paths["audit"])

    if summary.get("image_type") != "poster_like":
        blockers.append("summary_image_type")
    if summary.get("full_image_ocr_allowed") is not False:
        blockers.append("summary_full_image_ocr")
    if summary.get("ocr_strategy") != "segment_first":
        blockers.append("summary_ocr_strategy")
    if summary.get("layout_segmentation_required") is not True:
        blockers.append("layout_segmentation_not_required")

    if layout.get("full_image_ocr_allowed") is not False:
        blockers.append("layout_full_image_ocr")

    text_cands = text_doc.get("candidates") if isinstance(text_doc.get("candidates"), list) else []
    if len(text_cands) < 4:
        blockers.append("text_regions_incomplete")
    text_ids = {c.get("region_id") for c in text_cands if isinstance(c, dict)}
    if not {"title_area", "body_text_area", "price_or_promo_area", "time_location_area"} <= text_ids:
        blockers.append("text_region_ids_incomplete")

    price = next((c for c in text_cands if c.get("region_id") == "price_or_promo_area"), None)
    if price and "commercial_text_may_expire" not in (price.get("risk_flags") or []):
        blockers.append("price_missing_commercial_risk")
    time_r = next((c for c in text_cands if c.get("region_id") == "time_location_area"), None)
    if time_r and "temporal_text_requires_ttl" not in (time_r.get("risk_flags") or []):
        blockers.append("time_missing_ttl_risk")

    non_text_cands = non_text_doc.get("candidates") if isinstance(non_text_doc.get("candidates"), list) else []
    nt_ids = {c.get("region_id") for c in non_text_cands if isinstance(c, dict)}
    if "product_or_decoration_area" not in nt_ids:
        blockers.append("non_text_missing_product")
    for c in non_text_cands:
        if isinstance(c, dict) and c.get("ocr_allowed") is not False:
            blockers.append("non_text_ocr_allowed_true")

    visual_cands = visual_doc.get("candidates") if isinstance(visual_doc.get("candidates"), list) else []
    logo = next((c for c in visual_cands if c.get("region_id") == "logo_area"), None)
    qr = next((c for c in visual_cands if c.get("region_id") == "qr_area"), None)
    if not logo or logo.get("ocr_allowed") is not False:
        blockers.append("logo_ocr_allowed")
    if not qr or qr.get("ocr_allowed") is not False:
        blockers.append("qr_ocr_allowed")

    planned = ocr_plan.get("planned_regions") if isinstance(ocr_plan.get("planned_regions"), list) else []
    if not planned:
        blockers.append("ocr_plan_empty")
    for pr in planned:
        if not isinstance(pr, dict):
            continue
        rid = pr.get("region_id")
        if rid in FORBIDDEN_OCR_PLAN_REGIONS:
            blockers.append(f"ocr_plan_forbidden_region:{rid}")

    if reading.get("reading_order_confidence") != "low":
        blockers.append("reading_confidence_not_low")
    if reading.get("force_semantic_join_allowed") is not False:
        blockers.append("force_semantic_join_allowed")

    rids = _risk_ids(risks_doc)
    for req in (
        "complex_layout",
        "reading_order_uncertain",
        "commercial_text_may_expire",
        "visual_symbol_not_plain_text",
    ):
        if req not in rids:
            blockers.append(f"risk_missing_{req}")

    if gate.get("full_image_ocr_allowed_default") is not False:
        blockers.append("gate_full_image_ocr")
    if gate.get("visual_symbol_evidence_split_required") is not True:
        blockers.append("gate_visual_symbol_split")

    if summary.get("ocr_invoked") is not False:
        blockers.append("summary_ocr_invoked")
    audit_flags = (
        ("ocr_invoked", False),
        ("rapidocr_invoked", False),
        ("paddleocr_invoked", False),
        ("vision_provider_invoked", False),
        ("vlm_invoked", False),
        ("ai_interpretation_invoked", False),
        ("midplatform_fact_written", False),
        ("scene_delta_written", False),
        ("world_model_written", False),
        ("navigation_decision_invoked", False),
    )
    for key, expected in audit_flags:
        if aud.get(key) != expected:
            blockers.append(f"audit_{key}")

    verdict = "GO" if not blockers else "NO_GO"
    rep: Dict[str, Any] = {
        "schema": "poster_layout_governance_verifier_report_v0",
        "phase": "OCR-Poster-Layout-Segmentation-Governance-001",
        "smoke_root": str(root),
        "verdict": verdict,
        "blockers": blockers,
    }
    _write_json(root / "poster_layout_governance_verifier_report.json", rep)
    print(json.dumps({"smoke_root": str(root), "verdict": verdict, "blockers": blockers}, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
