#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for MixedVideo OCR Scan LineBox Trace + Source Quality Gate v0."""

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
        "summary": root / "mixedvideo_ocr_scan_linebox_trace_quality_gate_summary.json",
        "trace": root / "mixedvideo_ocr_scan_linebox_trace_report.json",
        "plan": root / "mixedvideo_selected_frame_linebox_plan_update.json",
        "policy": root / "mixedvideo_ocr_source_quality_gate_policy.json",
        "matrix": root / "mixedvideo_ocr_source_quality_evaluation_matrix.json",
        "consistency": root / "mixedvideo_scan_vs_pack_consistency_report.json",
        "risk": root / "mixedvideo_full_frame_ocr_risk_report.json",
        "roi": root / "mixedvideo_ocr_roi_crop_requirement_plan.json",
        "scan_obs": root / "mixedvideo_scan_observation_vs_evidence_policy.json",
        "ep_rec": root / "mixedvideo_ocr_evidence_pack_update_recommendation.json",
        "sem": root / "mixedvideo_semantic_candidate_guard_update_plan.json",
        "metrics": root / "mixedvideo_ocr_scan_linebox_quality_metrics_candidate_report.json",
        "benchmark": root / "mixedvideo_ocr_scan_linebox_quality_benchmark_link_report.json",
        "health": root / "mixedvideo_ocr_scan_linebox_quality_system_health_link_report.json",
        "boundary": root / "mixedvideo_ocr_scan_linebox_quality_no_write_boundary_report.json",
        "sim": root / "mixedvideo_ocr_scan_linebox_quality_simulation_context_report.json",
        "non_claims": root / "mixedvideo_ocr_scan_linebox_quality_non_claims_report.json",
        "followups": root / "mixedvideo_ocr_scan_linebox_quality_open_followups.json",
        "audit": root / "mixedvideo_ocr_scan_linebox_quality_audit_report.json",
    }

    for label, p in paths.items():
        if not p.is_file():
            blockers.append(f"missing:{label}")

    if blockers:
        _write_json(root / "mixedvideo_ocr_scan_linebox_quality_verifier_report.json", {"verdict": "NO_GO", "blockers": blockers})
        print(json.dumps({"verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    summary = _read_json(paths["summary"])
    trace = _read_json(paths["trace"])
    plan = _read_json(paths["plan"])
    policy = _read_json(paths["policy"])
    matrix = _read_json(paths["matrix"])
    consistency = _read_json(paths["consistency"])
    risk = _read_json(paths["risk"])
    roi = _read_json(paths["roi"])
    scan_obs = _read_json(paths["scan_obs"])
    ep_rec = _read_json(paths["ep_rec"])
    sem = _read_json(paths["sem"])
    metrics = _read_json(paths["metrics"])
    benchmark = _read_json(paths["benchmark"])
    health = _read_json(paths["health"])
    boundary = _read_json(paths["boundary"])
    sim = _read_json(paths["sim"])
    non_claims = _read_json(paths["non_claims"])
    followups = _read_json(paths["followups"])
    audit = _read_json(paths["audit"])

    ok(summary.get("phase_scope") == "scan_trace_and_source_quality_gate_only", "phase_scope")
    ok(summary.get("linebox_trace_defined") is True, "linebox_trace_defined")
    ok(summary.get("source_quality_gate_defined") is True, "source_quality_gate")
    ok(summary.get("scan_vs_pack_consistency_defined") is True, "scan_vs_pack_consistency")
    ok(_is_false(summary.get("world_model_attach_executed")), "summary_wm")
    ok(_is_false(summary.get("midplatform_fact_written")), "summary_fact")

    frames = trace.get("frames") if isinstance(trace.get("frames"), list) else []
    ok(len(frames) >= 10, "trace_frame_count")
    for fr in frames:
        if "linebox_available" not in fr:
            blockers.append("missing_linebox_available")
            break
        if not fr.get("linebox_available") and not fr.get("missing_reason"):
            blockers.append(f"missing_reason:{fr.get('frame_id')}")
            break
        if fr.get("linebox_available"):
            items = fr.get("text_items") or []
            if not items:
                blockers.append(f"no_text_items:{fr.get('frame_id')}")
                break
            it0 = items[0]
            for k in ("line_index", "text", "bbox_xyxy"):
                if k not in it0:
                    blockers.append(f"text_item_field:{k}")
                    break
        else:
            pass
    else:
        checks_passed += 1

    ok(plan.get("selected_frame_count", 0) >= 10, "plan_count")
    plan_frames = plan.get("frames") if isinstance(plan.get("frames"), list) else []
    ok(any("possible_mixed_regions" in f for f in plan_frames if isinstance(f, dict)), "possible_mixed_regions")

    grades = policy.get("grades") if isinstance(policy.get("grades"), dict) else {}
    for g in ("SQ_A", "SQ_B", "SQ_C", "SQ_D", "SQ_E"):
        if g not in grades:
            blockers.append(f"missing_grade:{g}")
    else:
        checks_passed += 1
    ok(grades.get("SQ_C", {}).get("requires_roi_crop") is True or grades.get("SQ_C", {}).get("requires_multiframe") is True, "sq_c_roi")
    ok(grades.get("SQ_D", {}).get("route_to_visual_symbol") is True, "sq_d_visual")
    ok(grades.get("SQ_E", {}).get("ocr_evidence_allowed") is False, "sq_e_no_evidence")

    rows = matrix.get("rows") if isinstance(matrix.get("rows"), list) else []
    ok(len(rows) >= 10, "matrix_rows")
    ok(all(isinstance(r, dict) and r.get("gate_decision") for r in rows), "gate_decision_all")

    ok(consistency.get("row_count", 0) >= 10, "consistency_rows")
    c_rows = consistency.get("rows") or []
    pack_mismatch_statuses = {
        "scan_has_text_pack_empty",
        "scan_has_text_pack_missing",
        "scan_mixed_regions_pack_empty",
    }
    ok(
        any(r.get("consistency_status") in pack_mismatch_statuses for r in c_rows)
        or consistency.get("scan_has_text_pack_empty_count", 0) > 0
        or consistency.get("scan_has_text_pack_missing_count", 0) > 0
        or consistency.get("scan_mixed_regions_pack_empty_count", 0) > 0,
        "pack_empty_recorded",
    )

    ok(risk.get("full_frame_ocr_allowed_for_fact") is False, "ff_fact_false")
    ok(risk.get("roi_crop_required_before_evidence") is True, "roi_required")

    roi_items = roi.get("items") if isinstance(roi.get("items"), list) else []
    ok(len(roi_items) >= 6, "roi_types")

    ok(scan_obs.get("scan_observation_fact_status") == "not_fact", "scan_obs_not_fact")
    ok(scan_obs.get("roi_ocr_required_for_evidence_pack") is True, "roi_required_policy")

    recs = ep_rec.get("recommendations") if isinstance(ep_rec.get("recommendations"), list) else []
    ok(any(r.get("field_to_add") == "scan_observation_ref" for r in recs if isinstance(r, dict)), "scan_obs_ref_rec")

    ok(sem.get("no_strong_entity_when_mixed_regions") is True, "sem_guard_mixed")
    ok("possible_mixed_regions" in str(sem.get("rules", [])), "sem_rules_mixed")

    ok("require_roi_crop_count" in metrics, "require_roi_crop_count")
    ok(metrics.get("benchmark_score_generated") is False, "metrics_benchmark")
    ok(benchmark.get("benchmark_score_generated") is False, "bench_score")
    ok(health.get("provider_health_runtime_checked") is False, "health_runtime")
    ok(boundary.get("boundary_ok") is True, "boundary_ok")
    ok(boundary.get("violations") == [], "violations")
    ok(sim.get("simulation_profile_id") == "developer_full", "sim_profile")
    ok(non_claims.get("not_benchmark") is True, "non_claims")
    ok(isinstance(followups.get("items"), list), "followups")
    ok(audit.get("mixedvideo_ocr_scan_linebox_trace_quality_gate_executed") is True, "audit")
    ok(_is_false(audit.get("world_model_attach_executed")), "audit_wm")
    ok(_is_false(audit.get("midplatform_fact_written")), "audit_fact")
    ok(_is_false(audit.get("runtime_routing_changed")), "audit_routing")

    verdict = "GO" if not blockers else "NO_GO"
    _write_json(
        root / "mixedvideo_ocr_scan_linebox_quality_verifier_report.json",
        {"schema_version": "mixedvideo_ocr_scan_linebox_quality_verifier_report_v0", "verdict": verdict, "blockers": blockers, "checks_passed": checks_passed},
    )
    print(json.dumps({"verdict": verdict, "blockers": blockers, "checks_passed": checks_passed}, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
