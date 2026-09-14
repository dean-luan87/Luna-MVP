#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for OCRRequest Gated Submission from Multiframe v1."""

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
        "summary": "ocrrequest_gated_submission_from_multiframe_v1_summary.json",
        "intake": "multiframe_ocrrequest_crop_intake_matrix_v1.json",
        "gate": "multiframe_ocrrequest_gate_policy_v1.json",
        "plan": "multiframe_ocrrequest_submission_plan_v1.json",
        "trace": "multiframe_ocrrequest_bridge_invocation_trace_v1.json",
        "bypass": "multiframe_ocrrequest_direct_provider_bypass_audit_v1.json",
        "collection": "multiframe_ocr_result_collection_v1.json",
        "matrix": "multiframe_ocr_result_matrix_v1.json",
        "grouping": "multiframe_ocr_output_grouping_report_v1.json",
        "guard": "multiframe_ocr_low_information_repeated_guard_v1.json",
        "carryover": "multiframe_ocr_same_frame_blocker_carryover_report_v1.json",
        "proj_risk": "multiframe_ocr_projection_crop_risk_report_v1.json",
        "future": "multiframe_ocr_future_ep_v4_plan.json",
        "chain": "multiframe_ocr_source_chain_report_v1.json",
        "provider": "multiframe_ocr_provider_summary_v1.json",
        "boundary": "multiframe_ocr_boundary_report_v1.json",
        "metrics": "multiframe_ocr_metrics_candidate_report_v1.json",
        "bench": "multiframe_ocr_benchmark_link_report_v1.json",
        "health": "multiframe_ocr_system_health_link_report_v1.json",
        "no_write": "multiframe_ocr_no_write_boundary_report_v1.json",
        "sim": "multiframe_ocr_simulation_context_report_v1.json",
        "non_claims": "multiframe_ocr_non_claims_report_v1.json",
        "followups": "multiframe_ocr_open_followups_v1.json",
        "audit": "multiframe_ocr_audit_report_v1.json",
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
            root / "multiframe_ocr_verifier_report_v1.json",
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
    grouping = data["grouping"]
    guard = data["guard"]
    carryover = data["carryover"]
    proj_risk = data["proj_risk"]
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
    ok(s.get("submission_scope") == "multiframe_crop_ocrrequest_gated_submission_only", "scope")
    ok(s.get("based_on_multiframe_crop_execution") is True, "based_crop")
    ok(s.get("multiframe_crop_artifact_count_observed") == 30, "crop30")
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

    intake_rows = intake.get("rows") or []
    ok(len(intake_rows) == 30, "intake_30")
    for row in intake_rows:
        if isinstance(row, dict):
            ok(row.get("projection_is_approximate") is True, "intake_approx")
            ok(row.get("detected_region") is False, "intake_not_detected")
            ok(row.get("selected_for_submission") is True, "intake_selected")
            break

    rule_ids = {r.get("rule_id") for r in gate.get("rules") or [] if isinstance(r, dict)}
    ok("direct_provider_bypass_forbidden" in rule_ids, "rule_no_bypass")
    ok("full_frame_ocr_forbidden" in rule_ids, "rule_no_full_frame")

    ok(len(plan.get("rows") or []) == 30, "plan_30")
    trace_rows = trace.get("rows") or []
    ok(len(trace_rows) > 0, "trace_rows")
    for tr in trace_rows:
        if isinstance(tr, dict):
            ok(bool(tr.get("ocrrequest_reference_multiframe_id")), "trace_has_ref")
            ok(tr.get("direct_provider_bypass") is False, "trace_no_bypass")
            break

    ok(bypass.get("capability_imports_rapidocr") is False, "no_rapid_import")
    ok(bypass.get("direct_provider_call_detected") is False, "no_direct_call")
    ok(bypass.get("bridge_invoked") is True, "bridge_invoked")

    results = coll.get("rows") or []
    ok(len(results) == 30, "result_30")
    ok(s.get("ocrrequest_submitted_count") == len(trace_rows), "submit_trace_align")
    for r in results:
        if isinstance(r, dict):
            ok(r.get("detected_region") is False, "res_not_detected")
            ok(r.get("evidence_pack_generated") is False, "res_no_ep")
            break

    ok(len(matrix.get("rows") or []) == 30, "matrix_30")
    ok(any(g.get("consensus_claimed") is False for g in grouping.get("groups") or []), "no_consensus")
    ok(guard.get("non_empty_text_is_not_accuracy") is True, "guard_no_accuracy")
    ok(guard.get("repeated_text_not_consensus") is True, "guard_no_consensus")
    ok(carryover.get("same_frame_blocker_resolved") is False, "carryover_blocker")
    ok(carryover.get("same_frame_consensus_blocker_still_active") is True, "carryover_active")
    ok(proj_risk.get("projection_not_detection") is True, "proj_not_det")
    future_phases = [p.get("future_phase") for p in future.get("phases") or [] if isinstance(p, dict)]
    ok("Evidence-Pack-Adapter-v4-Multiframe" in future_phases, "future_ep")
    chain_rows = chain.get("rows") or []
    ok(len(chain_rows) > 0, "chain_rows")
    for cr in chain_rows:
        if isinstance(cr, dict):
            ok(cr.get("traceable_to_multiframe_crop") is True, "chain_crop")
            break
    ok(provider.get("provider_comparison_claimed") is False, "prov_no_compare")
    ok(boundary.get("fact_write_allowed") is False, "boundary_no_fact")
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

    verdict = "GO" if not blockers else "NO_GO"
    report = {
        "verdict": verdict,
        "checks_passed": checks,
        "checks_expected": 68,
        "blockers": blockers,
        "phase": "OCRRequest-Gated-Submission-from-Multiframe-v1-001",
    }
    _write_json(root / "multiframe_ocr_verifier_report_v1.json", report)
    print(json.dumps(report, ensure_ascii=False))
    return 0 if verdict in ("GO", "CONDITIONAL_GO") else 2


if __name__ == "__main__":
    raise SystemExit(main())
