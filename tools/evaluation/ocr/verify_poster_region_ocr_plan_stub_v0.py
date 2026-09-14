#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for Poster Region OCR Plan Stub v0."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Set


FORBIDDEN_IN_PLAN = frozenset(
    {"logo_area", "qr_area", "product_or_decoration_area", "background_or_decoration_area"}
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


def main() -> int:
    _find_ws_root()
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke-root", required=True)
    args = ap.parse_args()

    root = _require_abs(args.smoke_root, "--smoke-root")
    blockers: List[str] = []

    paths = {
        "summary": root / "poster_region_ocr_plan_stub_summary.json",
        "plan": root / "poster_region_ocr_plan_stub.json",
        "excluded": root / "poster_region_ocr_excluded_regions_report.json",
        "risk": root / "poster_region_ocr_risk_matrix.json",
        "provider": root / "poster_region_ocr_provider_plan_matrix.json",
        "reading": root / "poster_region_ocr_reading_order_guard.json",
        "metrics": root / "poster_region_ocr_metrics_binding_report.json",
        "gate": root / "poster_region_ocr_gate_policy_report.json",
        "audit": root / "poster_region_ocr_plan_stub_audit_report.json",
    }

    for label, p in paths.items():
        if not p.is_file():
            blockers.append(f"missing:{label}")

    if blockers:
        _write_json(
            root / "poster_region_ocr_plan_stub_verifier_report.json",
            {"verdict": "NO_GO", "blockers": blockers},
        )
        print(json.dumps({"verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    summary = _read_json(paths["summary"])
    plan = _read_json(paths["plan"])
    excluded = _read_json(paths["excluded"])
    risk = _read_json(paths["risk"])
    provider = _read_json(paths["provider"])
    reading = _read_json(paths["reading"])
    gate = _read_json(paths["gate"])
    aud = _read_json(paths["audit"])

    if summary.get("plan_scope") != "ocr_plan_stub_only":
        blockers.append("plan_scope")
    if summary.get("full_image_ocr_allowed") is not False:
        blockers.append("full_image_ocr")
    if plan.get("ocr_strategy") != "segment_first":
        blockers.append("ocr_strategy")

    planned = plan.get("planned_regions") if isinstance(plan.get("planned_regions"), list) else []
    if len(planned) != 4:
        blockers.append("planned_count")
    planned_ids: Set[str] = set()
    for pr in planned:
        if not isinstance(pr, dict):
            continue
        sid = pr.get("source_region_id")
        planned_ids.add(str(sid))
        if sid in FORBIDDEN_IN_PLAN:
            blockers.append(f"forbidden_in_plan:{sid}")
        if pr.get("ocr_allowed") is not True:
            blockers.append(f"ocr_allowed:{sid}")
        if pr.get("fact_status") != "not_fact":
            blockers.append(f"fact_status:{sid}")

    required_text = {"title_area", "body_text_area", "price_or_promo_area", "time_location_area"}
    if planned_ids != required_text:
        blockers.append("planned_ids_mismatch")

    ex_rows = excluded.get("excluded_regions") if isinstance(excluded.get("excluded_regions"), list) else []
    ex_map = {r.get("region_id"): r for r in ex_rows if isinstance(r, dict)}
    logo = ex_map.get("logo_area")
    qr = ex_map.get("qr_area")
    if not logo or logo.get("routed_to") != "visual_symbol_candidate":
        blockers.append("logo_routing")
    if not qr or qr.get("routed_to") != "qr_candidate":
        blockers.append("qr_routing")
    if "product_or_decoration_area" not in ex_map:
        blockers.append("product_excluded")

    risk_rows = risk.get("rows") if isinstance(risk.get("rows"), list) else []
    price_risk = next((r for r in risk_rows if r.get("region_id") == "price_or_promo_area"), None)
    time_risk = next((r for r in risk_rows if r.get("region_id") == "time_location_area"), None)
    if not price_risk or "commercial_text_may_expire" not in (price_risk.get("risk_flags") or []):
        blockers.append("price_commercial_risk")
    if not time_risk or "temporal_text_requires_ttl" not in (time_risk.get("risk_flags") or []):
        blockers.append("time_ttl_risk")

    prov_rows = provider.get("rows") if isinstance(provider.get("rows"), list) else []
    for row in prov_rows:
        if isinstance(row, dict) and row.get("provider_invoked") is not False:
            blockers.append("provider_invoked")
        if isinstance(row, dict) and row.get("paddleocr_enabled") is not False:
            blockers.append("paddleocr_enabled")

    if reading.get("force_semantic_join_allowed") is not False:
        blockers.append("semantic_join_allowed")
    if reading.get("semantic_join_status") != "forbidden_in_this_phase":
        blockers.append("semantic_join_status")

    if gate.get("world_model_write_allowed") is not False:
        blockers.append("gate_world_model")
    if gate.get("scene_delta_write_allowed") is not False:
        blockers.append("gate_scene_delta")
    if gate.get("auto_approval_allowed") is not False:
        blockers.append("gate_auto_approve")

    for key in (
        "ocr_invoked",
        "rapidocr_invoked",
        "paddleocr_invoked",
        "vision_provider_invoked",
        "ai_interpretation_invoked",
        "midplatform_fact_written",
        "scene_delta_written",
        "world_model_written",
        "navigation_decision_invoked",
    ):
        if aud.get(key) is not False:
            blockers.append(f"audit_{key}")

    verdict = "GO" if not blockers else "NO_GO"
    _write_json(
        root / "poster_region_ocr_plan_stub_verifier_report.json",
        {
            "schema": "poster_region_ocr_plan_stub_verifier_report_v0",
            "phase": "OCR-Poster-Region-OCR-Plan-Stub-001",
            "smoke_root": str(root),
            "verdict": verdict,
            "blockers": blockers,
        },
    )
    print(json.dumps({"smoke_root": str(root), "verdict": verdict, "blockers": blockers}, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
