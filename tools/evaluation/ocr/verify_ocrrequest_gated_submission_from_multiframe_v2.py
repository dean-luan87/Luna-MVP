#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for OCRRequest Gated Submission from Multiframe v2."""

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
        "summary": "ocrrequest_gated_submission_from_multiframe_v2_summary.json",
        "intake": "multiframe_v2_ocrrequest_adjusted_crop_intake_matrix.json",
        "gate": "multiframe_v2_ocrrequest_gate_policy.json",
        "plan": "multiframe_v2_ocrrequest_submission_plan.json",
        "trace": "multiframe_v2_ocrrequest_bridge_invocation_trace.json",
        "bypass": "multiframe_v2_ocrrequest_direct_provider_bypass_audit.json",
        "collection": "multiframe_ocr_result_v2_collection.json",
        "matrix": "multiframe_ocr_result_v2_matrix.json",
        "comparison": "multiframe_ocr_v1_v2_comparison_report.json",
        "guard": "multiframe_ocr_v2_low_information_empty_guard.json",
        "guidance": "multiframe_ocr_v2_user_guidance_recovery_recommendation_report.json",
        "carryover": "multiframe_ocr_v2_same_frame_blocker_carryover_report.json",
        "future": "multiframe_ocr_v2_future_ep_guidance_plan.json",
        "chain": "multiframe_ocr_v2_source_chain_report.json",
        "provider": "multiframe_ocr_v2_provider_summary.json",
        "boundary": "multiframe_ocr_v2_boundary_report.json",
        "metrics": "multiframe_ocr_v2_metrics_candidate_report.json",
        "bench": "multiframe_ocr_v2_benchmark_link_report.json",
        "health": "multiframe_ocr_v2_system_health_link_report.json",
        "no_write": "multiframe_ocr_v2_no_write_boundary_report.json",
        "sim": "multiframe_ocr_v2_simulation_context_report.json",
        "non_claims": "multiframe_ocr_v2_non_claims_report.json",
        "followups": "multiframe_ocr_v2_open_followups.json",
        "audit": "multiframe_ocr_v2_audit_report.json",
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
            root / "multiframe_ocr_v2_verifier_report.json",
            {"verdict": "NO_GO", "checks_passed": 0, "blockers": blockers},
        )
        print(json.dumps({"verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    s = data["summary"]
    intake = data["intake"]
    gate = data["gate"]
    plan = data["plan"]
    trace = data["trace"]
    bypass = data["bypass"]
    coll = data["collection"]
    matrix = data["matrix"]
    comparison = data["comparison"]
    guard = data["guard"]
    guidance = data["guidance"]
    carryover = data["carryover"]
    future = data["future"]
    chain = data["chain"]
    provider = data["provider"]
    boundary = data["boundary"]
    metrics = data["metrics"]
    bench = data["bench"]
    health = data["health"]
    no_write = data["no_write"]
    sim = data["sim"]
    audit = data["audit"]

    ok(True, "summary_exists")
    ok(
        s.get("submission_scope") == "textdetector_adjusted_crop_ocrrequest_gated_submission_only",
        "scope",
    )
    ok(s.get("based_on_textdetector_adjusted_crop") is True, "based_adjusted")
    ok(s.get("adjusted_crop_artifact_count_observed") == 5, "crop5")
    ok(s.get("same_bbox_risk_count_observed") == 5, "same_bbox5")
    ok(s.get("geometry_change_significant_count_observed") == 0, "geom0")
    ok(s.get("ocrrequest_reference_generated") is True, "ref_gen")
    ok(s.get("ocr_invoked") is True, "ocr_invoked")
    ok(s.get("provider_invoked") is True, "provider_invoked")
    ok(s.get("direct_provider_bypass") is False, "no_bypass")
    ok(s.get("every_provider_call_has_ocrrequest_ref") is True, "every_ref")
    ok(s.get("full_frame_ocr_invoked") is False, "no_full_frame")
    ok(s.get("mock_text_used") is False, "no_mock")
    ok(s.get("evidence_pack_generated") is False, "no_ep")
    ok(s.get("semantic_candidate_generated") is False, "no_sem")
    ok(s.get("source_validation_rerun_invoked") is False, "no_sv")
    ok(s.get("same_frame_blocker_resolved") is False, "blocker_not_resolved")
    ok(s.get("tts_invoked") is False, "no_tts")
    ok(s.get("user_guidance_runtime_action_committed") is False, "no_ug_action")

    intake_rows = intake.get("rows") or []
    ok(len(intake_rows) == 5, "intake_5")
    for row in intake_rows:
        if isinstance(row, dict):
            ok(row.get("same_bbox_or_near_same_bbox_risk") is True, "intake_same_bbox")
            ok(row.get("selected_for_submission") is True, "intake_selected")
            break

    rule_ids = {r.get("rule_id") for r in gate.get("rules") or [] if isinstance(r, dict)}
    ok("same_bbox_risk_must_be_preserved" in rule_ids, "rule_same_bbox")
    ok(
        "user_guidance_recovery_recommended_if_v2_empty_or_low_confidence" in rule_ids,
        "rule_ug_recovery",
    )

    ok(len(plan.get("rows") or []) == 5, "plan_5")
    trace_rows = trace.get("rows") or []
    ok(len(trace_rows) > 0, "trace_rows")
    for tr in trace_rows:
        if isinstance(tr, dict):
            ok(bool(tr.get("ocrrequest_reference_multiframe_v2_id")), "trace_has_ref")
            ok(tr.get("direct_provider_bypass") is False, "trace_no_bypass")
            break

    ok(bypass.get("capability_imports_rapidocr") is False, "no_rapid_import")
    ok(bypass.get("direct_provider_call_detected") is False, "no_direct_call")
    ok(bypass.get("bridge_invoked") is True, "bridge_invoked")

    results = coll.get("rows") or []
    ok(len(results) == 5, "result_5")
    ok(s.get("ocrrequest_submitted_count") == len(trace_rows), "submit_trace_align")
    for r in results:
        if isinstance(r, dict):
            ok(r.get("evidence_pack_generated") is False, "res_no_ep")
            ok(r.get("semantic_candidate_generated") is False, "res_no_sem")
            break

    ok(len(matrix.get("rows") or []) == 5, "matrix_5")
    ok(comparison.get("improvement_claim_allowed") is False, "no_improve_claim")
    ok(comparison.get("same_bbox_risk_limits_interpretation") is True, "same_bbox_limits")
    ok(guard.get("empty_text_is_not_no_text_fact") is True, "guard_empty_not_fact")
    ok(guidance.get("no_tts_invoked_now") is True, "guidance_no_tts")
    ok(guidance.get("no_runtime_action_committed") is True, "guidance_no_action")
    ok(carryover.get("same_frame_blocker_resolved") is False, "carryover_blocker")
    ok(carryover.get("same_frame_consensus_blocker_still_active") is True, "carryover_active")
    future_phases = [p.get("future_phase") for p in future.get("phases") or [] if isinstance(p, dict)]
    ok("User-Guidance-Recovery-Policy-v1" in future_phases, "future_ug")
    chain_rows = chain.get("rows") or []
    ok(len(chain_rows) > 0, "chain_rows")
    for cr in chain_rows:
        if isinstance(cr, dict):
            ok(cr.get("traceable_to_textdetector_adjusted_crop") is True, "chain_crop_v2")
            break
    ok(provider.get("provider_comparison_claimed") is False, "prov_no_compare")
    ok(boundary.get("fact_write_allowed") is False, "boundary_no_fact")
    ok(boundary.get("tts_invoked") is False, "boundary_no_tts")
    ok(metrics.get("fact_write_allowed_count") == 0, "metrics_no_fact")
    ok(bench.get("benchmark_score_generated") is False, "bench_no_score")
    ok(health.get("provider_health_runtime_checked") is False, "health_no_runtime")
    ok(no_write.get("boundary_ok") is True, "no_write_ok")
    ok(no_write.get("violations") == [], "no_write_violations")
    ok(sim.get("simulation_profile_id") == "developer_full", "sim_profile")
    ok(len(data["followups"].get("items") or []) >= 5, "followups")
    ok(audit.get("world_model_attach_executed") is False, "audit_no_wm")
    ok(audit.get("midplatform_fact_written") is False, "audit_no_fact")
    ok(audit.get("runtime_routing_changed") is False, "audit_no_routing")
    ok(audit.get("scene_delta_candidate_generated") is False, "audit_no_scene_delta")
    ok(audit.get("navigation_decision_invoked") is False, "audit_no_nav")

    verdict = "GO" if not blockers else "NO_GO"
    report = {
        "verdict": verdict,
        "checks_passed": checks,
        "checks_expected": 73,
        "blockers": blockers,
        "phase": "OCRRequest-Gated-Submission-from-Multiframe-v2-001",
    }
    _write_json(root / "multiframe_ocr_v2_verifier_report.json", report)
    print(json.dumps(report, ensure_ascii=False))
    return 0 if verdict in ("GO", "CONDITIONAL_GO") else 2


if __name__ == "__main__":
    raise SystemExit(main())
