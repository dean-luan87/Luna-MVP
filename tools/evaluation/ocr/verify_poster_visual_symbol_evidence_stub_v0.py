#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for Poster VisualSymbolEvidence Stub v0."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Set


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


def main() -> int:
    _find_ws_root()
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke-root", required=True)
    args = ap.parse_args()

    root = _require_abs(args.smoke_root, "--smoke-root")
    blockers: List[str] = []

    paths = {
        "summary": root / "poster_visual_symbol_evidence_stub_summary.json",
        "schema": root / "poster_visual_symbol_evidence_schema_stub.json",
        "items": root / "poster_visual_symbol_evidence_items.json",
        "matrix": root / "poster_visual_symbol_evidence_matrix.json",
        "exclusion": root / "poster_visual_symbol_ocr_exclusion_link_report.json",
        "qr_logo": root / "poster_visual_symbol_qr_logo_policy_report.json",
        "risks": root / "poster_visual_symbol_risk_report.json",
        "metrics": root / "poster_visual_symbol_metrics_binding_report.json",
        "gate": root / "poster_visual_symbol_gate_policy_report.json",
        "audit": root / "poster_visual_symbol_evidence_stub_audit_report.json",
    }

    for label, p in paths.items():
        if not p.is_file():
            blockers.append(f"missing:{label}")

    if blockers:
        _write_json(
            root / "poster_visual_symbol_evidence_stub_verifier_report.json",
            {"verdict": "NO_GO", "blockers": blockers},
        )
        print(json.dumps({"verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    summary = _read_json(paths["summary"])
    items_doc = _read_json(paths["items"])
    exclusion = _read_json(paths["exclusion"])
    qr_logo = _read_json(paths["qr_logo"])
    risks_doc = _read_json(paths["risks"])
    gate = _read_json(paths["gate"])
    aud = _read_json(paths["audit"])

    if summary.get("evidence_scope") != "visual_symbol_stub_only":
        blockers.append("evidence_scope")
    if summary.get("ordinary_ocr_chain_excluded") is not True:
        blockers.append("ordinary_ocr_excluded")
    if summary.get("qr_decoded") is not False:
        blockers.append("qr_decoded")
    if summary.get("brand_identity_confirmed") is not False:
        blockers.append("brand_confirmed")

    item_list = items_doc.get("items") if isinstance(items_doc.get("items"), list) else []
    ids: Set[str] = set()
    for it in item_list:
        if not isinstance(it, dict):
            continue
        ids.add(str(it.get("source_region_id")))
        if it.get("ocr_chain_allowed") is not False:
            blockers.append("ocr_chain_allowed")
        if it.get("fact_status") != "not_fact":
            blockers.append("fact_status")
        if it.get("write_allowed") is not False:
            blockers.append("write_allowed")

    for req in ("logo_area", "qr_area", "product_or_decoration_area"):
        if req not in ids:
            blockers.append(f"missing_item:{req}")

    if not paths["matrix"].is_file():
        blockers.append("matrix")

    for check in exclusion.get("per_region_checks") or []:
        if isinstance(check, dict) and check.get("in_ocr_planned_regions") is True:
            blockers.append(f"in_ocr_plan:{check.get('region_id')}")

    if exclusion.get("ordinary_ocr_text_chain_excludes_logo_qr") is not True:
        blockers.append("exclusion_link")

    if qr_logo.get("qr_decoding_allowed_in_this_phase") is not False:
        blockers.append("qr_decode_allowed")
    if qr_logo.get("logo_brand_identification_allowed_in_this_phase") is not False:
        blockers.append("logo_id_allowed")
    if qr_logo.get("external_brand_database_invoked") is not False:
        blockers.append("brand_db")

    risk_ids = {r.get("risk_id") for r in (risks_doc.get("risks") or []) if isinstance(r, dict)}
    for req in ("visual_symbol_not_plain_text", "logo_not_brand_fact", "qr_not_decoded"):
        if req not in risk_ids:
            blockers.append(f"risk_{req}")

    if gate.get("world_model_write_allowed") is not False:
        blockers.append("gate_wm")
    if gate.get("scene_delta_write_allowed") is not False:
        blockers.append("gate_sd")
    if gate.get("midplatform_fact_write_allowed") is not False:
        blockers.append("gate_fact")
    if gate.get("auto_approval_allowed") is not False:
        blockers.append("gate_approve")

    for key in (
        "ocr_invoked",
        "qr_decoder_invoked",
        "brand_database_invoked",
        "visual_symbol_registry_invoked",
        "vision_provider_invoked",
        "ai_interpretation_invoked",
        "midplatform_fact_written",
        "scene_delta_written",
        "world_model_written",
    ):
        if aud.get(key) is not False:
            blockers.append(f"audit_{key}")

    verdict = "GO" if not blockers else "NO_GO"
    _write_json(
        root / "poster_visual_symbol_evidence_stub_verifier_report.json",
        {
            "schema": "poster_visual_symbol_evidence_stub_verifier_report_v0",
            "phase": "OCR-Poster-VisualSymbolEvidence-Stub-001",
            "smoke_root": str(root),
            "verdict": verdict,
            "blockers": blockers,
        },
    )
    print(json.dumps({"smoke_root": str(root), "verdict": verdict, "blockers": blockers}, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
