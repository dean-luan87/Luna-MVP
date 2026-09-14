#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for Text Detector DryRun v1."""

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
        "summary": "text_detector_dryrun_v1_summary.json",
        "intake": "text_detector_input_intake_matrix_v1.json",
        "rules": "text_detector_rule_matrix_v1.json",
        "supervision": "text_detector_supervision_tooling_report_v1.json",
        "schema": "text_region_candidate_schema_v1.json",
        "collection": "text_region_candidate_collection_v1.json",
        "slicing": "text_detector_slicing_tiling_plan_report_v1.json",
        "results": "text_detector_result_matrix_v1.json",
        "overlap": "text_detector_projection_overlap_drift_report_v1.json",
        "adj": "text_detector_bbox_adjustment_candidate_report_v1.json",
        "quality": "text_detector_quality_confidence_report_v1.json",
        "empty_exp": "text_detector_empty_ocr_explanation_report_v1.json",
        "future": "text_detector_future_bbox_adjustment_reocr_plan_v1.json",
        "chain": "text_detector_source_chain_report_v1.json",
        "blocker": "text_detector_semantic_sv_blocker_carryover_report_v1.json",
        "boundary": "text_detector_boundary_report_v1.json",
        "metrics": "text_detector_metrics_candidate_report_v1.json",
        "bench": "text_detector_benchmark_link_report_v1.json",
        "health": "text_detector_system_health_link_report_v1.json",
        "no_write": "text_detector_no_write_boundary_report_v1.json",
        "sim": "text_detector_simulation_context_report_v1.json",
        "non_claims": "text_detector_non_claims_report_v1.json",
        "followups": "text_detector_open_followups_v1.json",
        "audit": "text_detector_audit_report_v1.json",
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
            root / "text_detector_verifier_report_v1.json",
            {"verdict": "NO_GO", "checks_passed": 0, "blockers": blockers, "phase": "Text-Detector-DryRun-v1-001"},
        )
        print(json.dumps({"verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    s = data["summary"]
    intake = data["intake"]
    rules = data["rules"]
    sup = data["supervision"]
    schema = data["schema"]
    coll = data["collection"]
    slicing = data["slicing"]
    results = data["results"]
    overlap = data["overlap"]
    adj = data["adj"]
    quality = data["quality"]
    empty_exp = data["empty_exp"]
    future = data["future"]
    chain = data["chain"]
    blocker = data["blocker"]
    boundary = data["boundary"]
    metrics = data["metrics"]
    bench = data["bench"]
    health = data["health"]
    no_write = data["no_write"]
    sim = data["sim"]
    audit = data["audit"]

    ok(True, "summary_exists")
    ok(s.get("dryrun_scope") == "text_detector_dryrun_only", "scope")
    ok(s.get("based_on_crop_quality_diagnosis_v2") is True, "based_cq")
    ok(s.get("evidence_pack_v4_count_observed") == 30, "ep30")
    ok(s.get("multiframe_crop_artifact_count_observed") == 30, "crop30")
    ok(s.get("empty_ocr_result_count_observed") == 30, "empty30")
    ok(s.get("text_detector_dryrun_executed") is True, "executed")
    ok(s.get("ocr_invoked") is False, "no_ocr")
    ok(s.get("ocrrequest_generated") is False, "no_ocrreq")
    ok(s.get("evidence_pack_generated") is False, "no_ep")
    ok(s.get("semantic_candidate_generated") is False, "no_sem")

    ok(intake.get("crop_count") == 30, "intake_crop30")
    ok(intake.get("frame_count") == 6, "intake_frame6")
    for row in intake.get("rows") or []:
        if isinstance(row, dict):
            ok(Path(str(row.get("file_path") or "")).is_file(), "intake_file_exists")
            break

    rule_ids = [r.get("rule_id") for r in rules.get("rules") or [] if isinstance(r, dict)]
    ok("text_detector_dryrun_not_ocr" in rule_ids, "rule_not_ocr")
    ok("text_like_region_not_text_content" in rule_ids, "rule_not_content")

    ok("ocr_provider" in (sup.get("forbidden_roles") or []), "sup_forbid_ocr")
    ok(schema.get("template", {}).get("detected_text_content") is None, "schema_no_text")

    cands = coll.get("candidates") or []
    ok(len(cands) >= 36, "cands36")
    for c in cands:
        if isinstance(c, dict):
            ok(c.get("detected_text_content") is None, "cand_no_text")
            ok(c.get("ocr_text") is None, "cand_no_ocr_text")
            break

    ok(slicing.get("tile_results_are_not_fact") is True, "tile_not_fact")
    ok(slicing.get("ocr_allowed") is False, "tile_no_ocr")

    for r in results.get("rows") or []:
        if isinstance(r, dict):
            ok(r.get("fact_status") == "not_fact", "res_not_fact")
            break

    ov_rows = overlap.get("rows") or []
    ok(len(ov_rows) >= 36, "overlap36")
    ok(any(r.get("bbox_adjustment_needed") for r in ov_rows if isinstance(r, dict)), "adj_needed_some")

    for arow in adj.get("rows") or []:
        if isinstance(arow, dict):
            ok(arow.get("crop_generation_allowed_now") is False, "no_crop_now")
            ok(arow.get("ocrrequest_allowed_now") is False, "no_ocrreq_now")
            break

    ok(quality.get("confidence_not_ocr_accuracy") is True, "conf_not_ocr")
    ok(empty_exp.get("no_text_fact_supported") is False, "no_text_fact_false")
    ok(empty_exp.get("provider_failure_supported") is False, "no_prov_fail")
    ok(empty_exp.get("root_cause_confirmed") is False, "no_root_confirm")

    phases = [p.get("future_phase") for p in future.get("phases") or [] if isinstance(p, dict)]
    ok("BBox-Adjustment-Proposal-v2-Multiframe" in phases, "future_bbox")

    ok(chain.get("rows") and chain["rows"][0].get("traceable_to_crop_quality_diagnosis") is True, "chain_cq")
    ok(blocker.get("semantic_v4_still_blocked") is True, "sem_block")
    ok(blocker.get("source_validation_rerun_still_blocked") is True, "sv_block")
    ok(boundary.get("source_validation_rerun_invoked") is False, "bound_sv")
    ok(metrics.get("fact_write_allowed_count") == 0, "fact0")
    ok(bench.get("benchmark_score_generated") is False, "no_bench")
    ok(health.get("provider_health_runtime_checked") is False, "no_health")
    ok(no_write.get("boundary_ok") is True, "boundary_ok")
    ok(no_write.get("violations") == [], "no_violations")
    ok(sim.get("simulation_profile_id") == "developer_full", "sim_dev")
    ok(audit.get("text_detector_dryrun_v1_executed") is True, "audit_exec")
    ok(audit.get("world_model_written") is False, "audit_no_wm")

    verdict = "GO" if not blockers else "NO_GO"
    report = {
        "verdict": verdict,
        "checks_passed": checks,
        "checks_expected": 66,
        "blockers": blockers,
        "phase": "Text-Detector-DryRun-v1-001",
    }
    _write_json(root / "text_detector_verifier_report_v1.json", report)
    print(json.dumps({"verdict": verdict, "checks_passed": checks, "blockers": blockers, "phase": report["phase"]}, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
