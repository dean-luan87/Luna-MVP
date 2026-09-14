#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for Crop Quality Diagnosis v2 Multiframe."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import List


def _require_abs(p: str, label: str) -> Path:
    pp = Path(p).expanduser()
    if not pp.is_absolute():
        raise SystemExit(f"ERROR: {label} must be absolute, got: {p}")
    return pp.resolve()


def _write_json(path: Path, obj: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke-root", required=True)
    args = ap.parse_args()

    root = _require_abs(args.smoke_root, "--smoke-root")
    blockers: List[str] = []
    checks = 0

    def ok(c: bool, name: str) -> None:
        nonlocal checks
        if c:
            checks += 1
        else:
            blockers.append(name)

    files = {
        "summary": "crop_quality_diagnosis_v2_multiframe_summary.json",
        "intake": "crop_quality_diagnosis_v2_intake_matrix.json",
        "rules": "crop_quality_diagnosis_v2_rule_matrix.json",
        "geometry": "crop_quality_geometry_diagnosis_report_v2.json",
        "bbox": "crop_quality_bbox_type_comparison_report_v2.json",
        "frame": "crop_quality_frame_offset_diagnosis_report_v2.json",
        "bright": "crop_quality_brightness_blur_report_v2.json",
        "proj": "crop_quality_projection_drift_diagnosis_report_v2.json",
        "empty": "crop_quality_empty_result_pattern_report_v2.json",
        "visual": "crop_quality_visual_existence_report_v2.json",
        "root": "crop_quality_root_cause_hypothesis_report_v2.json",
        "decision": "crop_quality_diagnosis_decision_matrix_v2.json",
        "future": "crop_quality_future_fix_plan_v2.json",
        "blocker": "crop_quality_semantic_sv_blocker_carryover_report_v2.json",
        "chain": "crop_quality_source_chain_report_v2.json",
        "boundary": "crop_quality_boundary_report_v2.json",
        "metrics": "crop_quality_metrics_candidate_report_v2.json",
        "bench": "crop_quality_benchmark_link_report_v2.json",
        "health": "crop_quality_system_health_link_report_v2.json",
        "no_write": "crop_quality_no_write_boundary_report_v2.json",
        "sim": "crop_quality_simulation_context_report_v2.json",
        "non_claims": "crop_quality_non_claims_report_v2.json",
        "followups": "crop_quality_open_followups_v2.json",
        "audit": "crop_quality_audit_report_v2.json",
    }
    data = {}
    for k, f in files.items():
        p = root / f
        if not p.is_file():
            blockers.append(f"missing:{k}")
        else:
            data[k] = json.loads(p.read_text(encoding="utf-8"))

    if blockers:
        _write_json(
            root / "crop_quality_verifier_report_v2.json",
            {"verdict": "NO_GO", "checks_passed": 0, "blockers": blockers, "phase": "Crop-Quality-Diagnosis-v2-Multiframe-001"},
        )
        print(json.dumps({"verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    s = data["summary"]
    intake = data["intake"]
    rules = data["rules"]
    geom = data["geometry"]
    bbox = data["bbox"]
    frame = data["frame"]
    bright = data["bright"]
    proj = data["proj"]
    empty = data["empty"]
    visual = data["visual"]
    root_hyp = data["root"]
    decision = data["decision"]
    future = data["future"]
    blocker = data["blocker"]
    chain = data["chain"]
    boundary = data["boundary"]
    metrics = data["metrics"]
    bench = data["bench"]
    health = data["health"]
    no_write = data["no_write"]
    sim = data["sim"]
    audit = data["audit"]

    ok(True, "summary_exists")
    ok(s.get("diagnosis_scope") == "multiframe_crop_quality_diagnosis_only", "scope")
    ok(s.get("based_on_evidence_pack_v4_multiframe") is True, "based_ep")
    ok(s.get("evidence_pack_v4_count_observed") == 30, "ep30")
    ok(s.get("empty_ocr_result_count_observed") == 30, "empty30")
    ok(s.get("non_empty_ocr_result_count_observed") == 0, "nonempty0")
    ok(s.get("crop_quality_diagnosis_generated") is True, "diag_gen")
    ok(s.get("root_cause_confirmed") is False, "no_confirm")
    ok(s.get("ocr_invoked") is False, "no_ocr")
    ok(s.get("new_crop_generated") is False, "no_crop")

    intake_rows = intake.get("rows") or []
    ok(len(intake_rows) == 30, "intake30")
    for row in intake_rows:
        if isinstance(row, dict):
            ok(row.get("empty_text") is True, "intake_empty")
            ok(row.get("detected_region") is False, "intake_det")
            ok(row.get("projection_is_approximate") is True, "intake_proj")
            break

    rule_ids = [r.get("rule_id") for r in rules.get("rules") or [] if isinstance(r, dict)]
    ok("empty_ocr_not_no_text_fact" in rule_ids, "rule_no_text_fact")
    ok("root_cause_hypothesis_not_confirmed_by_default" in rule_ids, "rule_hypothesis")

    ok(geom.get("summary", {}).get("crop_count") == 30, "geom30")
    groups = bbox.get("groups") or []
    ok(any(g.get("bbox_type") == "source_bbox" for g in groups if isinstance(g, dict)), "src_bbox_grp")
    ok(any(g.get("bbox_type") == "expanded_bbox" for g in groups if isinstance(g, dict)), "exp_bbox_grp")
    ok(bbox.get("comparison_is_diagnostic_only") is True or all(
        g.get("comparison_is_diagnostic_only") is True for g in groups if isinstance(g, dict)
    ), "bbox_diag_only")

    frame_rows = frame.get("rows") or []
    ok(len(frame_rows) >= 6, "frame6")
    offsets = {r.get("frame_offset_from_source") for r in frame_rows if isinstance(r, dict)}
    for fo in [-30, -15, -5, 5, 15, 30]:
        ok(fo in offsets, f"offset_{fo}")

    ok(bright.get("lightweight_placeholder") is True, "bright_placeholder")
    ok(bright.get("quality_claim_allowed") is False, "no_quality_claim")

    ok(proj.get("summary", {}).get("detected_region_count") == 0, "det0")
    ok(proj.get("projection_crop_not_detection") is True, "proj_not_det")

    ok(empty.get("all_empty") is True, "all_empty")
    ok(empty.get("no_text_fact_written") is False, "no_text_fact_false")

    vis_rows = visual.get("rows") or []
    ok(len(vis_rows) == 30, "vis30")
    ok(all(r.get("file_exists") and r.get("image_read_success") for r in vis_rows if isinstance(r, dict)), "vis_readable")

    hyps = root_hyp.get("hypotheses") or []
    ok(len(hyps) >= 10, "hyp10")
    ok(root_hyp.get("root_cause_confirmed") is False, "hyp_not_confirmed")
    ok(all(h.get("confirmed") is False for h in hyps if isinstance(h, dict)), "all_hyp_unconfirmed")

    dec_rows = decision.get("rows") or []
    ok(len(dec_rows) == 30, "dec30")
    for drow in dec_rows:
        if isinstance(drow, dict):
            ok(drow.get("semantic_v4_allowed") is False, "sem_block")
            ok(drow.get("source_validation_rerun_allowed") is False, "sv_block")
            break

    phases = [p.get("future_phase") for p in future.get("phases") or [] if isinstance(p, dict)]
    ok("Text-Detector-DryRun-v1" in phases, "future_td")
    ok("BBox-Adjustment-Proposal-v2-Multiframe" in phases, "future_bbox")

    ok(blocker.get("semantic_v4_still_blocked") is True, "sem_still")
    ok(blocker.get("source_validation_rerun_still_blocked") is True, "sv_still")

    ok(chain.get("rows") and chain["rows"][0].get("traceable_to_ep_v4") is True, "chain_ep")

    ok(boundary.get("source_validation_rerun_invoked") is False, "bound_no_sv")
    ok(boundary.get("ocr_invoked") is False, "bound_no_ocr")

    ok(metrics.get("confirmed_root_cause_count") == 0, "confirmed0")
    ok(metrics.get("fact_write_allowed_count") == 0, "fact0")

    ok(bench.get("benchmark_score_generated") is False, "no_bench")
    ok(health.get("provider_health_runtime_checked") is False, "no_health_runtime")

    ok(no_write.get("boundary_ok") is True, "boundary_ok")
    ok(no_write.get("violations") == [], "no_violations")

    ok(sim.get("simulation_profile_id") == "developer_full", "sim_dev")

    ok(audit.get("crop_quality_diagnosis_v2_multiframe_executed") is True, "audit_exec")
    ok(audit.get("world_model_written") is False, "audit_no_wm")

    verdict = "GO" if not blockers else "NO_GO"
    report = {
        "verdict": verdict,
        "checks_passed": checks,
        "checks_expected": 69,
        "blockers": blockers,
        "phase": "Crop-Quality-Diagnosis-v2-Multiframe-001",
    }
    _write_json(root / "crop_quality_verifier_report_v2.json", report)
    print(json.dumps({"verdict": verdict, "checks_passed": checks, "blockers": blockers, "phase": report["phase"]}, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
