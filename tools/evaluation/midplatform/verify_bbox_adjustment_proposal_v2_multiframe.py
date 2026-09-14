#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for BBox Adjustment Proposal v2 Multiframe."""

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
        "summary": "bbox_adjustment_proposal_v2_multiframe_summary.json",
        "intake": "bbox_adjustment_candidate_intake_matrix_v2.json",
        "rules": "bbox_adjustment_rule_matrix_v2.json",
        "schema": "bbox_adjustment_proposal_schema_v2.json",
        "collection": "bbox_adjustment_proposal_collection_v2.json",
        "bounds": "bbox_adjustment_bounds_check_report_v2.json",
        "dedup": "bbox_adjustment_dedup_grouping_report_v2.json",
        "delta": "bbox_adjustment_delta_report_v2.json",
        "risk": "bbox_adjustment_risk_report_v2.json",
        "recrop": "bbox_adjustment_future_recrop_readiness_report_v2.json",
        "future": "bbox_adjustment_future_reocr_plan_v2.json",
        "chain": "bbox_adjustment_source_chain_report_v2.json",
        "blocker": "bbox_adjustment_semantic_sv_blocker_carryover_report_v2.json",
        "boundary": "bbox_adjustment_boundary_report_v2.json",
        "metrics": "bbox_adjustment_metrics_candidate_report_v2.json",
        "bench": "bbox_adjustment_benchmark_link_report_v2.json",
        "health": "bbox_adjustment_system_health_link_report_v2.json",
        "no_write": "bbox_adjustment_no_write_boundary_report_v2.json",
        "sim": "bbox_adjustment_simulation_context_report_v2.json",
        "non_claims": "bbox_adjustment_non_claims_report_v2.json",
        "followups": "bbox_adjustment_open_followups_v2.json",
        "audit": "bbox_adjustment_audit_report_v2.json",
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
            root / "bbox_adjustment_verifier_report_v2.json",
            {"verdict": "NO_GO", "checks_passed": 0, "blockers": blockers, "phase": "BBox-Adjustment-Proposal-v2-Multiframe-001"},
        )
        print(json.dumps({"verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    s = data["summary"]
    intake = data["intake"]
    rules = data["rules"]
    schema = data["schema"]
    coll = data["collection"]
    bounds = data["bounds"]
    dedup = data["dedup"]
    delta = data["delta"]
    risk = data["risk"]
    recrop = data["recrop"]
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
    ok(s.get("proposal_scope") == "bbox_adjustment_proposal_only", "scope")
    ok(s.get("based_on_text_detector_dryrun") is True, "based_td")
    ok(s.get("bbox_adjustment_candidate_count_observed") == 5, "cand5")
    ok(s.get("bbox_adjustment_proposal_generated") is True, "prop_gen")
    ok(s.get("bounds_check_executed") is True, "bounds_exec")
    ok(s.get("ocr_invoked") is False, "no_ocr")
    ok(s.get("new_crop_generated") is False, "no_crop")
    ok(s.get("ocrrequest_generated") is False, "no_cr")
    ok(s.get("evidence_pack_generated") is False, "no_ep")
    ok(s.get("semantic_candidate_generated") is False, "no_sem")

    ok(len(intake.get("rows") or []) == 5, "intake5")
    for row in intake.get("rows") or []:
        if isinstance(row, dict):
            ok(row.get("crop_generation_allowed_now") is False, "intake_no_crop")
            ok(row.get("ocrrequest_allowed_now") is False, "intake_no_ocrreq")
            break

    rule_ids = [r.get("rule_id") for r in rules.get("rules") or [] if isinstance(r, dict)]
    ok("heuristic_adjustment_not_fact" in rule_ids, "rule_not_fact")
    ok("adjustment_bbox_not_detected_text_region" in rule_ids, "rule_not_det")
    ok("no_new_crop_generation_in_this_phase" in rule_ids, "rule_no_crop")

    ok(schema.get("template", {}).get("risk_flags", {}).get("heuristic_candidate_not_fact") is True, "schema_risk")

    props = coll.get("proposals") or []
    ok(len(props) > 0, "props_gt0")
    ok(coll.get("proposal_count") > 0, "prop_count")
    for p in props:
        if isinstance(p, dict):
            ok(p.get("crop_generation_allowed_now") is False, "prop_no_crop")
            ok(p.get("ocrrequest_allowed_now") is False, "prop_no_ocrreq")
            break

    ok(any(b.get("bbox_valid_for_future_recrop") for b in bounds.get("rows") or [] if isinstance(b, dict)), "bounds_valid")
    ok(dedup.get("deduplicated_proposal_count") is not None, "dedup_count")
    ok(delta.get("rows") and delta["rows"][0].get("adjustment_is_diagnostic_only") is True, "delta_diag")
    ok(risk.get("rows") and risk["rows"][0].get("heuristic_candidate_not_fact") is True, "risk_heur")
    ok(recrop.get("rows") and recrop["rows"][0].get("crop_generation_allowed_now") is False, "recrop_no_crop")

    phases = [p.get("future_phase") for p in future.get("phases") or [] if isinstance(p, dict)]
    ok("Multiframe-Crop-Execution-DryRun-v2-TextDetectorAdjusted" in phases, "future_crop_v2")

    ok(chain.get("rows") and chain["rows"][0].get("traceable_to_text_detector_dryrun") is True, "chain_td")
    ok(blocker.get("semantic_v4_still_blocked") is True, "sem_block")
    ok(blocker.get("source_validation_rerun_still_blocked") is True, "sv_block")
    ok(boundary.get("source_validation_rerun_invoked") is False, "bound_sv")
    ok(metrics.get("fact_write_allowed_count") == 0, "fact0")
    ok(bench.get("benchmark_score_generated") is False, "no_bench")
    ok(health.get("provider_health_runtime_checked") is False, "no_health")
    ok(no_write.get("boundary_ok") is True, "boundary_ok")
    ok(no_write.get("violations") == [], "no_violations")
    ok(sim.get("simulation_profile_id") == "developer_full", "sim_dev")
    ok(audit.get("bbox_adjustment_proposal_v2_multiframe_executed") is True, "audit_exec")
    ok(audit.get("world_model_written") is False, "audit_no_wm")

    verdict = "GO" if not blockers else "NO_GO"
    report = {
        "verdict": verdict,
        "checks_passed": checks,
        "checks_expected": 63,
        "blockers": blockers,
        "phase": "BBox-Adjustment-Proposal-v2-Multiframe-001",
    }
    _write_json(root / "bbox_adjustment_verifier_report_v2.json", report)
    print(json.dumps({"verdict": verdict, "checks_passed": checks, "blockers": blockers, "phase": report["phase"]}, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
