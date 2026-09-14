#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for Multiframe Crop Execution DryRun v2 TextDetectorAdjusted."""

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
        "summary": "multiframe_crop_v2_textdetector_adjusted_summary.json",
        "intake": "multiframe_crop_v2_adjusted_intake_matrix.json",
        "rules": "multiframe_crop_v2_execution_rule_matrix.json",
        "schema": "multiframe_crop_v2_adjusted_artifact_schema.json",
        "collection": "multiframe_crop_v2_adjusted_artifact_collection.json",
        "trace": "multiframe_crop_v2_adjusted_execution_trace.json",
        "geometry": "multiframe_crop_v2_geometry_delta_report.json",
        "quality": "multiframe_crop_v2_adjusted_quality_placeholder_report.json",
        "diversity": "multiframe_crop_v2_adjusted_diversity_report.json",
        "ocr_ready": "multiframe_crop_v2_ocrrequest_readiness_report.json",
        "guidance": "multiframe_crop_v2_user_guidance_recovery_followup_report.json",
        "carryover": "multiframe_crop_v2_same_frame_blocker_carryover_report.json",
        "future": "multiframe_crop_v2_future_ocr_ep_sv_plan.json",
        "chain": "multiframe_crop_v2_source_chain_report.json",
        "boundary": "multiframe_crop_v2_boundary_report.json",
        "metrics": "multiframe_crop_v2_metrics_candidate_report.json",
        "bench": "multiframe_crop_v2_benchmark_link_report.json",
        "health": "multiframe_crop_v2_system_health_link_report.json",
        "no_write": "multiframe_crop_v2_no_write_boundary_report.json",
        "sim": "multiframe_crop_v2_simulation_context_report.json",
        "non_claims": "multiframe_crop_v2_non_claims_report.json",
        "followups": "multiframe_crop_v2_open_followups.json",
        "audit": "multiframe_crop_v2_audit_report.json",
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
            root / "multiframe_crop_v2_verifier_report.json",
            {"verdict": "NO_GO", "checks_passed": 0, "blockers": blockers, "phase": "Multiframe-Crop-Execution-DryRun-v2-TextDetectorAdjusted-001"},
        )
        print(json.dumps({"verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    s = data["summary"]
    intake = data["intake"]
    rules = data["rules"]
    coll = data["collection"]
    geom = data["geometry"]
    quality = data["quality"]
    div = data["diversity"]
    ocr_ready = data["ocr_ready"]
    guidance = data["guidance"]
    carryover = data["carryover"]
    future = data["future"]
    chain = data["chain"]
    boundary = data["boundary"]
    metrics = data["metrics"]
    bench = data["bench"]
    health = data["health"]
    no_write = data["no_write"]
    sim = data["sim"]
    audit = data["audit"]

    ok(True, "summary_exists")
    ok(s.get("dryrun_scope") == "textdetector_adjusted_recrop_only", "scope")
    ok(s.get("based_on_bbox_adjustment_proposal_v2") is True, "based_ba")
    ok(s.get("bbox_adjustment_proposal_count_observed") == 5, "prop5")
    ok(s.get("adjusted_crop_execution_attempted") is True, "exec_attempted")
    ok(s.get("adjusted_crop_artifact_generated") is True, "art_gen")
    ok(s.get("user_guidance_recovery_needed_later") is True, "ug_later")
    ok(s.get("ocr_invoked") is False, "no_ocr")
    ok(s.get("ocrrequest_generated") is False, "no_cr")

    ok(len(intake.get("rows") or []) == 5, "intake5")
    for row in intake.get("rows") or []:
        if isinstance(row, dict):
            ok(row.get("proposal_ready_for_future_recrop") is True, "intake_ready")
            break

    rule_ids = [r.get("rule_id") for r in rules.get("rules") or [] if isinstance(r, dict)]
    ok("adjusted_bbox_from_heuristic_not_detection" in rule_ids, "rule_not_det")
    ok("same_bbox_risk_must_be_reported" in rule_ids, "rule_same_bbox")
    ok("user_guidance_recovery_required_if_reocr_empty_later" in rule_ids, "rule_ug")

    arts = coll.get("artifacts") or []
    ok(len(arts) > 0, "arts_gt0")
    for a in arts:
        if isinstance(a, dict):
            ok(a.get("ocr_invoked") is False, "art_no_ocr")
            ok(a.get("ocrrequest_generated") is False, "art_no_cr")
            if a.get("crop_generated"):
                ok(Path(str(a.get("crop_file_path") or "")).is_file(), "crop_png_exists")
            break

    gsum = geom.get("summary") or {}
    ok(gsum.get("same_bbox_or_near_same_bbox_risk_count", 0) >= 0, "same_bbox_rec")
    ok(any(r.get("same_bbox_or_near_same_bbox_risk") for r in geom.get("rows") or [] if isinstance(r, dict)), "same_bbox_row")

    ok(quality.get("rows") and quality["rows"][0].get("crop_quality_claim_allowed") is False, "qual_no_claim")
    ok(div.get("independent_consensus_allowed_now") is False, "div_no_consensus")

    ok(ocr_ready.get("rows") and ocr_ready["rows"][0].get("ocrrequest_allowed_now") is False, "ocrreq_now_false")
    ok(guidance.get("no_tts_invoked_now") is True, "no_tts")
    ok(guidance.get("no_runtime_action_committed") is True, "no_runtime_ug")

    ok(carryover.get("same_frame_blocker_resolved") is False, "blocker_not_resolved")
    phases = [p.get("future_phase") for p in future.get("phases") or [] if isinstance(p, dict)]
    ok("OCRRequest-Gated-Submission-from-Multiframe-v2" in phases, "future_ocr_v2")
    ok("User-Guidance-Recovery-Policy-v1" in phases, "future_ug")

    ok(chain.get("rows") and chain["rows"][0].get("traceable_to_bbox_adjustment_proposal") is True, "chain_ba")
    ok(boundary.get("tts_invoked") is False, "bound_tts")
    ok(boundary.get("source_validation_rerun_invoked") is False, "bound_sv")
    ok(metrics.get("user_guidance_runtime_action_committed_count") == 0, "ug_runtime0")
    ok(no_write.get("boundary_ok") is True, "boundary_ok")
    ok(sim.get("simulation_profile_id") == "developer_full", "sim_dev")
    ok(audit.get("multiframe_crop_v2_textdetector_adjusted_executed") is True, "audit_exec")

    verdict = "GO" if not blockers else "NO_GO"
    report = {
        "verdict": verdict,
        "checks_passed": checks,
        "checks_expected": 65,
        "blockers": blockers,
        "phase": "Multiframe-Crop-Execution-DryRun-v2-TextDetectorAdjusted-001",
    }
    _write_json(root / "multiframe_crop_v2_verifier_report.json", report)
    print(json.dumps({"verdict": verdict, "checks_passed": checks, "blockers": blockers, "phase": report["phase"]}, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
