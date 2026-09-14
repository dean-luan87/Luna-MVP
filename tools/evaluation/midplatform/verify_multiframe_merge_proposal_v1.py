#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for Multiframe Merge Proposal v1."""

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


def _read_json(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))


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
        "summary": "multiframe_merge_proposal_v1_summary.json",
        "intake": "multiframe_sv2_blocker_intake_matrix.json",
        "rules": "multiframe_merge_proposal_rule_matrix.json",
        "region_schema": "multiframe_candidate_region_schema_v1.json",
        "region_collection": "multiframe_candidate_region_collection_v1.json",
        "target_window": "multiframe_target_frame_window_plan_v1.json",
        "neighbor": "multiframe_neighbor_frame_selection_plan_v1.json",
        "tracklet": "multiframe_tracklet_hint_plan_v1.json",
        "merge_strategy": "multiframe_merge_strategy_matrix_v1.json",
        "evidence_gain": "multiframe_expected_evidence_gain_report_v1.json",
        "risk": "multiframe_merge_risk_report_v1.json",
        "future": "multiframe_future_extraction_plan_v1.json",
        "carryover": "multiframe_same_frame_blocker_carryover_report_v1.json",
        "source_chain": "multiframe_source_chain_report_v1.json",
        "review": "multiframe_review_unresolved_readiness_report_v1.json",
        "boundary": "multiframe_boundary_report_v1.json",
        "metrics": "multiframe_metrics_candidate_report_v1.json",
        "bench": "multiframe_benchmark_link_report_v1.json",
        "health": "multiframe_system_health_link_report_v1.json",
        "no_write": "multiframe_no_write_boundary_report_v1.json",
        "sim": "multiframe_simulation_context_report_v1.json",
        "non_claims": "multiframe_non_claims_report_v1.json",
        "followups": "multiframe_open_followups_v1.json",
        "audit": "multiframe_audit_report_v1.json",
    }
    data = {}
    for k, f in files.items():
        p = root / f
        if not p.is_file():
            blockers.append(f"missing:{k}")
        else:
            data[k] = _read_json(p)

    if blockers:
        _write_json(
            root / "multiframe_verifier_report_v1.json",
            {"verdict": "NO_GO", "checks_passed": 0, "blockers": blockers},
        )
        print(json.dumps({"verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    s = data["summary"]
    intake = data["intake"]
    rules = data["rules"]
    region_coll = data["region_collection"]
    target_window = data["target_window"]
    neighbor = data["neighbor"]
    tracklet = data["tracklet"]
    merge_strategy = data["merge_strategy"]
    evidence_gain = data["evidence_gain"]
    risk = data["risk"]
    future = data["future"]
    carryover = data["carryover"]
    source_chain = data["source_chain"]
    review = data["review"]
    boundary = data["boundary"]
    metrics = data["metrics"]
    bench = data["bench"]
    health = data["health"]
    no_write = data["no_write"]
    sim = data["sim"]
    audit = data["audit"]

    ok(True, "summary_exists")
    ok(s.get("proposal_scope") == "multiframe_merge_proposal_only", "scope")
    ok(s.get("based_on_source_validation_v2") is True, "based_sv2")
    ok(s.get("based_on_semantic_candidate_v3") is True, "based_sem")
    ok(s.get("source_validation_passed_count_observed") == 0, "passed0")
    ok(s.get("same_frame_consensus_blocked_count_observed") == 4, "same_frame4")
    ok(s.get("multiframe_proposal_generated") is True, "proposal_generated")
    ok(s.get("new_frame_extracted") is False, "no_frame")
    ok(s.get("video_decoded") is False, "no_decode")
    ok(s.get("ocr_invoked") is False, "no_ocr")

    ok(intake.get("row_count") == 4 or len(intake.get("rows") or []) == 4, "intake_4")
    for row in intake.get("rows") or []:
        if isinstance(row, dict):
            ok(row.get("validation_passed") is False, "intake_not_passed")
            ok(row.get("entity_confirmed") is False, "intake_no_entity")
            ok(row.get("eligible_for_multiframe_proposal") is True, "intake_eligible")
            break

    rule_ids = {r.get("rule_id") for r in rules.get("rules") or [] if isinstance(r, dict)}
    ok("same_frame_blocker_requires_multiframe_plan" in rule_ids, "rule_same_frame")
    ok("no_new_frame_extraction_in_this_phase" in rule_ids, "rule_no_frame")
    ok("no_ocr_execution_in_this_phase" in rule_ids, "rule_no_ocr")

    ok(data["region_schema"].get("template") or data["region_schema"].get("example_instance"), "schema")

    regions = region_coll.get("regions") or []
    ok(len(regions) >= 1, "region_count")
    ok(s.get("multiframe_candidate_region_count", 0) >= 1, "summary_region_count")

    plans = target_window.get("plans") or []
    ok(len(plans) >= 1, "window_plans")
    for plan in plans:
        if isinstance(plan, dict):
            ok(plan.get("extraction_allowed_in_this_phase") is False, "no_extract")
            ok(plan.get("video_decode_allowed_in_this_phase") is False, "no_decode_plan")
            break

    for plan in neighbor.get("plans") or []:
        if isinstance(plan, dict):
            ok(plan.get("selection_not_executed") is True, "neighbor_not_executed")
            strategies = plan.get("neighbor_selection_strategy") or []
            ok(len(strategies) >= 4, "neighbor_strategies")
            break

    for hint in tracklet.get("hints") or []:
        if isinstance(hint, dict):
            ok(hint.get("tracklet_created_now") is False, "no_tracklet_now")
            feats = hint.get("tracking_features") or []
            ok(len(feats) >= 5, "tracking_features")
            break

    strategies = merge_strategy.get("strategies") or []
    ok(len(strategies) >= 6, "merge_strategies")
    for st in strategies:
        if isinstance(st, dict):
            ok(st.get("execution_allowed_now") is False, "strategy_not_now")
            break

    for rep in evidence_gain.get("reports") or []:
        if isinstance(rep, dict):
            ok(rep.get("estimate_is_diagnostic_only") is True, "gain_diagnostic")
            ok(rep.get("fact_write_allowed") is False, "gain_no_fact")
            break

    for rep in risk.get("reports") or []:
        if isinstance(rep, dict):
            ok(rep.get("requires_future_quality_gate") is True, "risk_quality_gate")
            ok(rep.get("requires_future_source_validation_rerun") is True, "risk_sv_rerun")
            break

    future_phases = [p.get("future_phase") for p in future.get("phases") or [] if isinstance(p, dict)]
    ok("Better-Frame-Extraction-DryRun-v1" in future_phases, "future_better_frame")

    ok(carryover.get("same_frame_consensus_blocker_still_active") is True, "carryover_active")
    ok(carryover.get("independent_consensus_allowed_now") is False, "no_consensus_now")
    ok(carryover.get("blocker_not_resolved_in_this_phase") is True, "blocker_not_resolved")

    ok(source_chain.get("traceable_to_source_validation_v2") is True, "chain_sv2")
    ok(source_chain.get("traceable_to_semantic_candidate_v3") is True, "chain_sem")
    ok(source_chain.get("traceable_to_evidence_pack_v3") is True, "chain_ep")
    ok(source_chain.get("traceable_to_linebox_trace") is True, "chain_linebox")

    ok(review.get("review_policy_ready_now") is False, "review_not_ready")
    ok(review.get("unresolved_slot_ready_now") is False, "slot_not_ready")

    ok(boundary.get("multiframe_merge_proposal_only") is True, "boundary_proposal_only")
    ok(boundary.get("source_validation_rerun_invoked") is False, "boundary_no_sv_rerun")

    ok(metrics.get("new_frame_extracted_count") == 0, "metrics_no_frame")
    ok(metrics.get("ocr_invoked_count") == 0, "metrics_no_ocr")

    ok(bench.get("benchmark_score_generated") is False, "bench_no_score")

    ok(health.get("provider_health_runtime_checked") is False, "health_no_runtime")

    ok(no_write.get("boundary_ok") is True, "no_write_ok")
    ok(no_write.get("violations") == [], "no_write_violations")

    ok(sim.get("simulation_profile_id") == "developer_full", "sim_profile")

    ok(data["non_claims"].get("same_frame_blocker_not_resolved") is True, "non_claims_blocker")
    ok(len(data["followups"].get("items") or []) >= 5, "followups")

    ok(audit.get("world_model_attach_executed") is False, "audit_no_wm")
    ok(audit.get("scene_delta_candidate_generated") is False, "audit_no_sd")
    ok(audit.get("midplatform_fact_written") is False, "audit_no_fact")
    ok(audit.get("world_model_written") is False, "audit_no_wm_write")
    ok(audit.get("navigation_decision_invoked") is False, "audit_no_nav")
    ok(audit.get("runtime_routing_changed") is False, "audit_no_routing")

    verdict = "GO" if not blockers else "NO_GO"
    report = {
        "verdict": verdict,
        "checks_passed": checks,
        "checks_expected": 65,
        "blockers": blockers,
        "phase": "Multiframe-Merge-Proposal-v1-001",
    }
    _write_json(root / "multiframe_verifier_report_v1.json", report)
    print(json.dumps(report, ensure_ascii=False))
    return 0 if verdict in ("GO", "CONDITIONAL_GO") else 2


if __name__ == "__main__":
    raise SystemExit(main())
