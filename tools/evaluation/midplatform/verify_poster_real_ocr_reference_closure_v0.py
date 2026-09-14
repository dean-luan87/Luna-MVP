#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for Poster Real OCR Reference Closure v0."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, List


TEXT_REGIONS = ("title_area", "body_text_area", "price_or_promo_area", "time_location_area")
VISUAL_REGIONS = ("logo_area", "qr_area", "product_or_decoration_area", "background_or_decoration_area")
REQUIRED_PHASE_KEYS = (
    "poster_layout_governance",
    "poster_region_ocr_plan",
    "poster_visual_symbol_evidence",
    "original_poster_reference_only",
    "poster_real_ocr_gated_execution",
    "poster_real_ocr_readonly_consumer",
    "poster_real_ocr_reference_update",
)


def _find_ws_root() -> Path:
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "capabilities" / "midplatform").is_dir():
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
        "summary": root / "poster_real_ocr_reference_closure_summary.json",
        "phase_matrix": root / "poster_real_ocr_reference_closure_phase_matrix.json",
        "lineage": root / "poster_real_ocr_reference_lineage_closure_report.json",
        "track": root / "poster_real_ocr_reference_track_closure_matrix.json",
        "alignment": root / "poster_real_ocr_reference_alignment_closure_report.json",
        "visual": root / "poster_real_ocr_reference_visual_symbol_closure_report.json",
        "reading": root / "poster_real_ocr_reference_reading_order_closure_report.json",
        "ttl": root / "poster_real_ocr_reference_ttl_risk_closure_report.json",
        "metrics": root / "poster_real_ocr_reference_metrics_closure_candidate_report.json",
        "benchmark": root / "poster_real_ocr_reference_closure_benchmark_link_report.json",
        "health": root / "poster_real_ocr_reference_closure_system_health_link_report.json",
        "boundary": root / "poster_real_ocr_reference_closure_no_write_boundary_report.json",
        "sim": root / "poster_real_ocr_reference_closure_simulation_context_report.json",
        "non_claims": root / "poster_real_ocr_reference_closure_non_claims_report.json",
        "followups": root / "poster_real_ocr_reference_closure_open_followups.json",
        "audit": root / "poster_real_ocr_reference_closure_audit_report.json",
    }

    for label, p in paths.items():
        if not p.is_file():
            blockers.append(f"missing:{label}")

    if blockers:
        _write_json(
            root / "poster_real_ocr_reference_closure_verifier_report.json",
            {"verdict": "NO_GO", "blockers": blockers, "checks_passed": 0},
        )
        print(json.dumps({"verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    summary = _read_json(paths["summary"])
    phase_matrix = _read_json(paths["phase_matrix"])
    lineage = _read_json(paths["lineage"])
    track = _read_json(paths["track"])
    alignment = _read_json(paths["alignment"])
    visual = _read_json(paths["visual"])
    reading = _read_json(paths["reading"])
    ttl = _read_json(paths["ttl"])
    metrics = _read_json(paths["metrics"])
    benchmark = _read_json(paths["benchmark"])
    health = _read_json(paths["health"])
    boundary = _read_json(paths["boundary"])
    sim = _read_json(paths["sim"])
    non_claims = _read_json(paths["non_claims"])
    followups = _read_json(paths["followups"])
    audit = _read_json(paths["audit"])

    if summary.get("closure_scope") != "reference_chain_closure_only":
        blockers.append("closure_scope")
    if summary.get("poster_real_ocr_reference_status") != "closed_for_reference_evaluation":
        blockers.append("reference_status")
    if summary.get("based_on_real_ocr_execution") is not True:
        blockers.append("based_on_execution")
    if summary.get("based_on_readonly_consumer") is not True:
        blockers.append("based_on_consumer")
    if summary.get("based_on_reference_update") is not True:
        blockers.append("based_on_update")
    if summary.get("original_text_plan_ref_count") != 4:
        blockers.append("plan_ref_count")
    if summary.get("real_ocr_text_evidence_ref_count") != 4:
        blockers.append("real_ocr_ref_count")
    if summary.get("visual_symbol_ref_count") != 4:
        blockers.append("visual_ref_count")
    if summary.get("aligned_region_count") != 4:
        blockers.append("aligned_count")
    if summary.get("semantic_join_invoked") is not False:
        blockers.append("semantic_join")
    if summary.get("fusion_invoked") is not False:
        blockers.append("fusion")
    if summary.get("scene_delta_candidate_generated") is not False:
        blockers.append("scene_delta")

    rows = phase_matrix.get("rows") if isinstance(phase_matrix.get("rows"), list) else []
    if len(rows) < 7:
        blockers.append("phase_matrix_row_count")
    for row in rows:
        if not isinstance(row, dict):
            continue
        if row.get("source_status") != "ok":
            blockers.append(f"phase_not_ok:{row.get('phase_key')}")
        if row.get("blockers"):
            blockers.append(f"phase_blockers:{row.get('phase_key')}")
        if row.get("write_status") != "no_write":
            blockers.append(f"write_status:{row.get('phase_key')}")
        if row.get("routing_changed") is not False:
            blockers.append(f"routing:{row.get('phase_key')}")

    text_lin = lineage.get("text_region_lineage") if isinstance(lineage.get("text_region_lineage"), list) else []
    vis_lin = lineage.get("visual_region_lineage") if isinstance(lineage.get("visual_region_lineage"), list) else []
    if len(text_lin) != 4:
        blockers.append("text_lineage_count")
    for rid in TEXT_REGIONS:
        if not any(isinstance(t, dict) and t.get("source_region_id") == rid for t in text_lin):
            blockers.append(f"text_lineage_missing:{rid}")
        else:
            t = next(x for x in text_lin if x.get("source_region_id") == rid)
            for key in (
                "layout_region_ref",
                "ocr_plan_ref",
                "real_ocr_execution_ref",
                "readonly_consumer_ref",
                "reference_update_ref",
                "final_closure_ref",
            ):
                if not t.get(key):
                    blockers.append(f"text_lineage_field:{rid}:{key}")

    if len(vis_lin) != 4:
        blockers.append("visual_lineage_count")
    for rid in VISUAL_REGIONS:
        if not any(isinstance(v, dict) and v.get("source_region_id") == rid for v in vis_lin):
            blockers.append(f"visual_lineage_missing:{rid}")

    tracks = track.get("tracks") if isinstance(track.get("tracks"), list) else []
    if len(tracks) != 3:
        blockers.append("track_count")
    vis_track = next((t for t in tracks if isinstance(t, dict) and t.get("track_name") == "visual_symbol_track"), {})
    if vis_track.get("status") != "preserved_not_text":
        blockers.append("visual_track_status")

    if alignment.get("all_text_regions_aligned") is not True:
        blockers.append("all_aligned")
    if alignment.get("accuracy_computed") is not False:
        blockers.append("accuracy")

    if visual.get("visual_symbols_consumed_as_text") is not False:
        blockers.append("visual_as_text")
    if visual.get("qr_decoded") is not False:
        blockers.append("qr_decoded")
    if visual.get("brand_identity_confirmed") is not False:
        blockers.append("brand")

    if reading.get("semantic_join_invoked") is not False:
        blockers.append("reading_semantic_join")
    if reading.get("cross_region_text_joined") is not False:
        blockers.append("cross_region")

    if ttl.get("ttl_required_region_count") != 2:
        blockers.append("ttl_count")

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

    if non_claims.get("not_fusion") is not True:
        blockers.append("non_claims_fusion")
    if non_claims.get("not_benchmark") is not True:
        blockers.append("non_claims_benchmark")

    items = followups.get("items") if isinstance(followups.get("items"), list) else []
    if len(items) < 1:
        blockers.append("followups_empty")

    audit_checks = [
        ("ocr_reinvoked", False),
        ("rapidocr_reinvoked", False),
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
        "schema_version": "poster_real_ocr_reference_closure_verifier_report_v0",
        "verdict": verdict,
        "blockers": blockers,
        "checks_passed": 59 - len(blockers),
        "phase_verdict_hint": summary.get("phase_verdict_hint"),
    }
    _write_json(root / "poster_real_ocr_reference_closure_verifier_report.json", report)
    print(json.dumps({"verdict": verdict, "blockers": blockers}, ensure_ascii=False))
    return 0 if verdict in ("GO", "CONDITIONAL_GO") else 2


if __name__ == "__main__":
    raise SystemExit(main())
