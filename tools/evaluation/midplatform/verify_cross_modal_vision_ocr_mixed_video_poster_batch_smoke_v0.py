#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for CrossModal Vision OCR Mixed Video Poster Batch Smoke v0."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, List


P0_VIDEO_ID = "test_video_complex_6m42s"


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


def _is_false(v: Any) -> bool:
    return v is False


def main() -> int:
    _find_ws_root()
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke-root", required=True)
    args = ap.parse_args()

    root = _require_abs(args.smoke_root, "--smoke-root")
    blockers: List[str] = []
    checks_passed = 0

    def ok(cond: bool, name: str) -> None:
        nonlocal checks_passed
        if cond:
            checks_passed += 1
        else:
            blockers.append(name)

    paths = {
        "summary": root / "mixed_video_poster_batch_summary.json",
        "manifest": root / "mixed_video_poster_input_manifest.json",
        "scan": root / "mixed_video_candidate_scan_report.json",
        "frame_plan": root / "mixed_video_selected_text_bearing_frame_plan.json",
        "image_ocr": root / "mixed_poster_image_ocr_execution_report.json",
        "packs": root / "mixed_ocr_evidence_pack_collection.json",
        "sem": root / "mixed_ocr_semantic_candidate_collection.json",
        "readability": root / "mixed_ocr_readability_evaluation_report.json",
        "routing": root / "mixed_visual_symbol_public_facility_routing_report.json",
        "uncertainty": root / "mixed_ocr_uncertainty_guard_report.json",
        "chain": root / "mixed_ocr_source_chain_report.json",
        "metrics": root / "mixed_ocr_metrics_candidate_report.json",
        "benchmark": root / "mixed_ocr_benchmark_link_report.json",
        "health": root / "mixed_ocr_system_health_link_report.json",
        "boundary": root / "mixed_ocr_no_write_boundary_report.json",
        "sim": root / "mixed_ocr_simulation_context_report.json",
        "non_claims": root / "mixed_ocr_non_claims_report.json",
        "followups": root / "mixed_ocr_open_followups.json",
        "audit": root / "mixed_ocr_audit_report.json",
    }

    for label, p in paths.items():
        if not p.is_file():
            blockers.append(f"missing:{label}")

    if blockers:
        _write_json(root / "mixed_ocr_verifier_report.json", {"verdict": "NO_GO", "blockers": blockers, "checks_passed": 0})
        print(json.dumps({"verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    summary = _read_json(paths["summary"])
    manifest = _read_json(paths["manifest"])
    scan = _read_json(paths["scan"])
    frame_plan = _read_json(paths["frame_plan"])
    image_ocr = _read_json(paths["image_ocr"])
    packs = _read_json(paths["packs"])
    sem = _read_json(paths["sem"])
    readability = _read_json(paths["readability"])
    routing = _read_json(paths["routing"])
    uncertainty = _read_json(paths["uncertainty"])
    chain = _read_json(paths["chain"])
    metrics = _read_json(paths["metrics"])
    benchmark = _read_json(paths["benchmark"])
    health = _read_json(paths["health"])
    boundary = _read_json(paths["boundary"])
    sim = _read_json(paths["sim"])
    non_claims = _read_json(paths["non_claims"])
    followups = _read_json(paths["followups"])
    audit = _read_json(paths["audit"])

    ok(summary.get("batch_scope") == "mixed_video_poster_ocr_smoke", "batch_scope")
    ok(summary.get("video_count") == 8, "video_count")
    ok(summary.get("image_count") == 10, "image_count")
    ok(_is_false(summary.get("world_model_attach_executed")), "summary_wm")
    ok(_is_false(summary.get("scene_delta_candidate_generated")), "summary_scene_delta")
    ok(_is_false(summary.get("midplatform_fact_written")), "summary_midplatform")

    videos = manifest.get("videos") if isinstance(manifest.get("videos"), list) else []
    ok(len(videos) == 8, "manifest_videos")
    images = manifest.get("images") if isinstance(manifest.get("images"), list) else []
    ok(len(images) == 10, "manifest_images")

    scan_rows = scan.get("rows") if isinstance(scan.get("rows"), list) else []
    ok(scan.get("video_scan_count", 0) >= 1, "video_scan_count")
    p0_row = next((r for r in scan_rows if r.get("video_id") == P0_VIDEO_ID), None)
    ok(p0_row is not None and p0_row.get("recommended_for_text_bearing_framesample") is True, "p0_recommended")

    ok(frame_plan.get("selected_video_id") == P0_VIDEO_ID, "selected_video_id")
    ok(frame_plan.get("selected_frame_count", 0) >= 10, "selected_frame_count")

    ok(image_ocr.get("image_count") == 10, "image_ocr_count")
    ok(packs.get("total_pack_count", 0) > 0, "total_pack_count")
    ok(packs.get("raw_ocr_text_preserved") is True, "raw_preserved")

    sem_n = sem.get("semantic_candidate_count", 0)
    pack_n = packs.get("total_pack_count", 0)
    ok(sem_n >= pack_n, "semantic_candidate_count")

    ok(readability.get("readability_grade_distribution") is not None, "readability_dist")
    ok(routing.get("no_brand_fact_without_registry_or_review") is True, "no_brand_fact")
    ok(uncertainty.get("empty_text_is_not_no_text_fact") is True, "empty_guard")
    ok(uncertainty.get("partial_text_is_not_complete_entity_fact") is True, "partial_guard")
    ok(chain.get("lineage_status") == "traceable", "lineage")
    ok(metrics.get("benchmark_score_generated") is False, "metrics_benchmark")
    ok(benchmark.get("current_phase_updates_benchmark_values") is False, "bench_update")
    ok(health.get("provider_health_runtime_checked") is False, "health_runtime")
    ok(boundary.get("boundary_ok") is True, "boundary_ok")
    ok(boundary.get("violations") == [], "boundary_violations")
    ok(sim.get("simulation_profile_id") == "developer_full", "sim_profile")
    ok(non_claims.get("not_benchmark") is True, "non_claims_benchmark")
    ok(non_claims.get("not_world_model_attach") is True, "non_claims_wm")
    ok(isinstance(followups.get("items"), list) and len(followups.get("items", [])) >= 8, "followups")
    ok(audit.get("mixed_video_poster_batch_smoke_executed") is True, "audit_executed")
    ok(_is_false(audit.get("world_model_attach_executed")), "audit_wm")
    ok(_is_false(audit.get("scene_delta_candidate_generated")), "audit_scene_delta")
    ok(_is_false(audit.get("midplatform_fact_written")), "audit_midplatform")
    ok(_is_false(audit.get("world_model_written")), "audit_world_model")
    ok(_is_false(audit.get("navigation_decision_invoked")), "audit_navigation")
    ok(_is_false(audit.get("runtime_routing_changed")), "audit_routing")

    verdict = "GO" if not blockers else "NO_GO"
    _write_json(
        root / "mixed_ocr_verifier_report.json",
        {"schema_version": "mixed_ocr_verifier_report_v0", "verdict": verdict, "blockers": blockers, "checks_passed": checks_passed, "smoke_root": str(root)},
    )
    print(json.dumps({"verdict": verdict, "blockers": blockers, "checks_passed": checks_passed}, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
