#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for Poster Real OCR Reference Update v0."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, List


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
        "summary": root / "poster_real_ocr_reference_update_summary.json",
        "candidate": root / "poster_real_ocr_updated_reference_candidate.json",
        "alignment": root / "poster_real_ocr_text_plan_alignment_matrix.json",
        "visual": root / "poster_real_ocr_visual_symbol_reference_preservation_report.json",
        "track": root / "poster_real_ocr_reference_update_track_separation_report.json",
        "reading": root / "poster_real_ocr_reference_update_reading_order_guard.json",
        "ttl": root / "poster_real_ocr_reference_update_ttl_risk_report.json",
        "chain": root / "poster_real_ocr_reference_update_source_chain_report.json",
        "metrics": root / "poster_real_ocr_reference_update_metrics_candidate_report.json",
        "benchmark": root / "poster_real_ocr_reference_update_benchmark_link_report.json",
        "health": root / "poster_real_ocr_reference_update_system_health_link_report.json",
        "boundary": root / "poster_real_ocr_reference_update_no_write_boundary_report.json",
        "sim": root / "poster_real_ocr_reference_update_simulation_context_report.json",
        "non_claims": root / "poster_real_ocr_reference_update_non_claims_report.json",
        "audit": root / "poster_real_ocr_reference_update_audit_report.json",
    }

    for label, p in paths.items():
        if not p.is_file():
            blockers.append(f"missing:{label}")

    if blockers:
        _write_json(
            root / "poster_real_ocr_reference_update_verifier_report.json",
            {"verdict": "NO_GO", "blockers": blockers, "checks_passed": 0},
        )
        print(json.dumps({"verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    summary = _read_json(paths["summary"])
    candidate = _read_json(paths["candidate"])
    alignment = _read_json(paths["alignment"])
    visual = _read_json(paths["visual"])
    track = _read_json(paths["track"])
    reading = _read_json(paths["reading"])
    ttl = _read_json(paths["ttl"])
    metrics = _read_json(paths["metrics"])
    benchmark = _read_json(paths["benchmark"])
    health = _read_json(paths["health"])
    boundary = _read_json(paths["boundary"])
    sim = _read_json(paths["sim"])
    non_claims = _read_json(paths["non_claims"])
    audit = _read_json(paths["audit"])

    if summary.get("reference_scope") != "reference_only_update":
        blockers.append("reference_scope")
    if summary.get("based_on_original_poster_reference") is not True:
        blockers.append("based_on_original")
    if summary.get("based_on_real_ocr_readonly_consumer") is not True:
        blockers.append("based_on_consumer")
    if summary.get("original_text_plan_ref_count") != 4:
        blockers.append("plan_ref_count")
    if summary.get("real_ocr_text_evidence_ref_count") != 4:
        blockers.append("real_ocr_ref_count")
    if summary.get("visual_symbol_ref_count") != 4:
        blockers.append("visual_ref_count")
    if summary.get("ocr_reinvoked") is not False:
        blockers.append("ocr_reinvoked")
    if summary.get("rapidocr_reinvoked") is not False:
        blockers.append("rapidocr_reinvoked")
    if summary.get("paddleocr_invoked") is not False:
        blockers.append("paddleocr")

    plan_refs = candidate.get("original_text_plan_refs") or []
    real_refs = candidate.get("real_ocr_text_evidence_refs") or []
    vis_refs = candidate.get("visual_symbol_refs") or []
    if len(plan_refs) != 4:
        blockers.append("candidate_plan_refs")
    if len(real_refs) != 4:
        blockers.append("candidate_real_refs")
    if len(vis_refs) != 4:
        blockers.append("candidate_visual_refs")

    sep = candidate.get("track_separation") if isinstance(candidate.get("track_separation"), dict) else {}
    if sep.get("fusion_status") != "not_fused":
        blockers.append("fusion_status")

    if alignment.get("aligned_region_count") != 4:
        blockers.append("aligned_region_count")

    if visual.get("visual_symbols_consumed_as_text") is not False:
        blockers.append("visual_as_text")
    if visual.get("qr_decoded") is not False:
        blockers.append("qr_decoded")
    if visual.get("brand_identity_confirmed") is not False:
        blockers.append("brand_confirmed")

    if track.get("text_visual_overlap") is not False:
        blockers.append("text_visual_overlap")
    if track.get("logo_qr_in_text_track") is not False:
        blockers.append("logo_qr_in_text")
    if track.get("semantic_join_allowed") is not False:
        blockers.append("semantic_join_track")

    if reading.get("semantic_join_invoked") is not False:
        blockers.append("semantic_join_reading")
    if reading.get("cross_region_text_joined") is not False:
        blockers.append("cross_region_joined")

    if ttl.get("ttl_required_region_count") != 2:
        blockers.append("ttl_count")

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
        "schema_version": "poster_real_ocr_reference_update_verifier_report_v0",
        "verdict": verdict,
        "blockers": blockers,
        "checks_passed": 56 - len(blockers),
        "phase_verdict_hint": summary.get("phase_verdict_hint"),
    }
    _write_json(root / "poster_real_ocr_reference_update_verifier_report.json", report)
    print(json.dumps({"verdict": verdict, "blockers": blockers}, ensure_ascii=False))
    return 0 if verdict in ("GO", "CONDITIONAL_GO") else 2


if __name__ == "__main__":
    raise SystemExit(main())
