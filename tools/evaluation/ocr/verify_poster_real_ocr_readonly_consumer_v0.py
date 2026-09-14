#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for Poster Real OCR ReadOnly Consumer v0."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, List, Set


REGION_ORDER = ("title_area", "body_text_area", "price_or_promo_area", "time_location_area")


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
        "summary": root / "poster_real_ocr_readonly_consumer_summary.json",
        "view": root / "poster_real_ocr_region_text_consumer_view.json",
        "matrix": root / "poster_real_ocr_region_text_matrix.json",
        "indexes": root / "poster_real_ocr_readonly_consumer_indexes.json",
        "ttl": root / "poster_real_ocr_readonly_ttl_risk_report.json",
        "reading": root / "poster_real_ocr_readonly_reading_order_guard.json",
        "visual": root / "poster_real_ocr_readonly_visual_track_separation_check.json",
        "metrics": root / "poster_real_ocr_readonly_metrics_update_candidate_report.json",
        "benchmark": root / "poster_real_ocr_readonly_benchmark_link_report.json",
        "health": root / "poster_real_ocr_readonly_system_health_link_report.json",
        "boundary": root / "poster_real_ocr_readonly_no_write_boundary_report.json",
        "sim": root / "poster_real_ocr_readonly_simulation_context_report.json",
        "non_claims": root / "poster_real_ocr_readonly_non_claims_report.json",
        "audit": root / "poster_real_ocr_readonly_audit_report.json",
    }

    for label, p in paths.items():
        if not p.is_file():
            blockers.append(f"missing:{label}")

    if blockers:
        _write_json(
            root / "poster_real_ocr_readonly_verifier_report.json",
            {"verdict": "NO_GO", "blockers": blockers, "checks_passed": 0},
        )
        print(json.dumps({"verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    summary = _read_json(paths["summary"])
    view = _read_json(paths["view"])
    matrix = _read_json(paths["matrix"])
    ttl = _read_json(paths["ttl"])
    reading = _read_json(paths["reading"])
    visual = _read_json(paths["visual"])
    metrics = _read_json(paths["metrics"])
    benchmark = _read_json(paths["benchmark"])
    health = _read_json(paths["health"])
    boundary = _read_json(paths["boundary"])
    sim = _read_json(paths["sim"])
    non_claims = _read_json(paths["non_claims"])
    audit = _read_json(paths["audit"])

    if summary.get("consumer_scope") != "readonly_consumer":
        blockers.append("consumer_scope")
    if summary.get("based_on_poster_real_ocr") is not True:
        blockers.append("based_on_poster_real_ocr")
    if summary.get("evidence_count_observed") != 4:
        blockers.append("evidence_count")
    if summary.get("region_count_observed") != 4:
        blockers.append("region_count")
    if summary.get("ocr_reinvoked") is not False:
        blockers.append("ocr_reinvoked")
    if summary.get("rapidocr_reinvoked") is not False:
        blockers.append("rapidocr_reinvoked")
    if summary.get("paddleocr_invoked") is not False:
        blockers.append("paddleocr")
    if summary.get("semantic_join_invoked") is not False:
        blockers.append("semantic_join_summary")

    items = view.get("items") if isinstance(view.get("items"), list) else []
    if len(items) != 4:
        blockers.append("view_item_count")
    view_ids: Set[str] = set()
    for it in items:
        if isinstance(it, dict):
            view_ids.add(str(it.get("source_region_id") or ""))
    for rid in REGION_ORDER:
        if rid not in view_ids:
            blockers.append(f"view_missing:{rid}")

    mrows = matrix.get("rows") if isinstance(matrix.get("rows"), list) else []
    ttl_by_region = {str(r.get("region_id")): r.get("ttl_required") for r in mrows if isinstance(r, dict)}
    if ttl_by_region.get("price_or_promo_area") is not True:
        blockers.append("promo_ttl")
    if ttl_by_region.get("time_location_area") is not True:
        blockers.append("time_ttl")
    if ttl_by_region.get("title_area") is not False:
        blockers.append("title_ttl")
    if ttl_by_region.get("body_text_area") is not False:
        blockers.append("body_ttl")

    if ttl.get("ttl_required_region_count") != 2:
        blockers.append("ttl_count")

    if reading.get("semantic_join_allowed") is not False:
        blockers.append("reading_semantic_join")
    if reading.get("cross_region_text_joined") is not False:
        blockers.append("cross_region_joined")

    if visual.get("visual_regions_consumed_by_this_phase") is not False:
        blockers.append("visual_consumed")
    for flag in ("logo_ocr_invoked", "qr_ocr_invoked", "qr_decoded", "brand_identity_confirmed"):
        if visual.get(flag) is not False:
            blockers.append(flag)

    if metrics.get("ocr_accuracy_computed") is not False:
        blockers.append("ocr_accuracy")
    if metrics.get("benchmark_score_generated") is not False:
        blockers.append("benchmark_score")

    if benchmark.get("current_phase_updates_benchmark_values") is not False:
        blockers.append("benchmark_update")

    if health.get("provider_health_runtime_checked") is not False:
        blockers.append("health_runtime")

    if boundary.get("boundary_ok") is not True:
        blockers.append("boundary_ok")
    if boundary.get("violations") != []:
        blockers.append("violations")

    if sim.get("simulation_profile_id") != "developer_full":
        blockers.append("sim_profile")

    if non_claims.get("not_benchmark") is not True:
        blockers.append("non_claims_benchmark")
    if non_claims.get("not_provider_superiority") is not True:
        blockers.append("non_claims_provider")

    audit_checks = [
        ("full_image_ocr_invoked", False),
        ("visual_region_ocr_invoked", False),
        ("semantic_join_invoked", False),
        ("fusion_invoked", False),
        ("scene_delta_candidate_generated", False),
        ("midplatform_fact_written", False),
        ("scene_delta_written", False),
        ("world_model_written", False),
        ("navigation_decision_invoked", False),
        ("runtime_routing_changed", False),
    ]
    for key, expected in audit_checks:
        if audit.get(key) != expected:
            blockers.append(f"audit:{key}")

    if blockers:
        verdict = "NO_GO"
    elif summary.get("phase_verdict_hint") == "CONDITIONAL_GO":
        verdict = "CONDITIONAL_GO"
    else:
        verdict = str(summary.get("phase_verdict_hint") or "GO")

    report = {
        "schema_version": "poster_real_ocr_readonly_verifier_report_v0",
        "verdict": verdict,
        "blockers": blockers,
        "checks_passed": 53 - len(blockers),
        "phase_verdict_hint": summary.get("phase_verdict_hint"),
    }
    _write_json(root / "poster_real_ocr_readonly_verifier_report.json", report)
    print(json.dumps({"verdict": verdict, "blockers": blockers}, ensure_ascii=False))
    return 0 if verdict in ("GO", "CONDITIONAL_GO") else 2


if __name__ == "__main__":
    raise SystemExit(main())
