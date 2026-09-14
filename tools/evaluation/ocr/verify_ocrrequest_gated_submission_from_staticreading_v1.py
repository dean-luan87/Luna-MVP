#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for OCRRequest Gated Submission from StaticReading v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List


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
        "summary": "ocrrequest_gated_submission_from_staticreading_v1_summary.json",
        "intake": "ocrrequest_staticreading_input_intake_matrix_v1.json",
        "capture_readiness": "ocrrequest_staticreading_static_capture_readiness_intake_v1.json",
        "region_gate_matrix": "ocrrequest_staticreading_readable_region_input_gate_matrix_v1.json",
        "future_schema": "ocrrequest_staticreading_future_payload_schema_v1.json",
        "blocked_collection": "ocrrequest_staticreading_blocked_candidate_collection_v1.json",
        "gate_policy_matrix": "ocrrequest_staticreading_gate_policy_matrix_v1.json",
        "memory_governance_link": "ocrrequest_staticreading_memory_governance_link_v1.json",
        "ep_v5_plan": "ocrrequest_staticreading_evidence_pack_v5_future_plan_v1.json",
        "semantic_sv_plan": "ocrrequest_staticreading_semantic_sv_future_plan_v1.json",
        "bypass_audit": "ocrrequest_staticreading_provider_bypass_audit_v1.json",
        "long_term": "ocrrequest_staticreading_long_term_candidate_link_v1.json",
        "trace": "ocrrequest_staticreading_decision_trace_v1.json",
        "final": "ocrrequest_staticreading_final_decision_v1.json",
        "boundary": "ocrrequest_staticreading_boundary_report_v1.json",
        "metrics": "ocrrequest_staticreading_metrics_candidate_report_v1.json",
        "bench": "ocrrequest_staticreading_benchmark_link_report_v1.json",
        "health": "ocrrequest_staticreading_system_health_report_v1.json",
        "no_write": "ocrrequest_staticreading_no_write_boundary_report_v1.json",
        "sim": "ocrrequest_staticreading_simulation_context_report_v1.json",
        "non_claims": "ocrrequest_staticreading_non_claims_report_v1.json",
        "followups": "ocrrequest_staticreading_open_followups_v1.json",
        "audit": "ocrrequest_staticreading_audit_report_v1.json",
    }
    data: Dict[str, Any] = {}
    for k, f in files.items():
        p = root / f
        if not p.is_file():
            blockers.append(f"missing:{k}")
        else:
            data[k] = json.loads(p.read_text(encoding="utf-8"))

    if blockers:
        _write_json(
            root / "ocrrequest_staticreading_verifier_report_v1.json",
            {"verdict": "NO_GO", "blockers": blockers},
        )
        print(json.dumps({"verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    s = data["summary"]
    cap = data["capture_readiness"]
    rows = data["region_gate_matrix"].get("rows") or []
    blocked = data["blocked_collection"].get("candidates") or []
    fs = data["future_schema"]

    ok(True, "summary")
    ok(s.get("gate_scope") == "staticreading_ocrrequest_gated_submission_dryrun_only", "scope")
    ok(s.get("based_on_rrd_runtime") is True, "rrd")
    ok(s.get("based_on_hardware_adapter_stub") is True, "hw_stub")
    ok(s.get("based_on_memory_handoff") is True, "mem_ho")
    ok(s.get("static_capture_handoff_candidate_count_observed") == 26, "ho_26")
    ok(s.get("readable_region_candidate_count_observed") == 34, "rr_34")
    ok(s.get("frame_capture_stub_observed") is True, "frame_stub")
    ok(s.get("capture_status_observed") == "not_captured", "not_captured")
    ok(s.get("static_capture_result_available") is False, "no_cap_result")
    ok(s.get("ocrrequest_future_schema_defined") is True, "schema_def")
    ok(s.get("ocrrequest_blocked_candidate_generated") is True, "blocked_gen")
    ok(s.get("ocrrequest_eligible_now") is False, "not_eligible")
    ok(s.get("ocrrequest_submitted_now") is False, "not_submitted")
    ok(s.get("ocr_invoked") is False, "no_ocr")
    ok(s.get("provider_invoked") is False, "no_provider")
    ok(s.get("evidence_pack_v5_generated") is False, "no_ep5")
    ok("capture_status_not_captured" in (cap.get("reason_not_ready") or []), "reason_cap")
    ok(len(rows) == 34, "rows_34")
    ok(all(r.get("ocr_input_allowed_now") is False for r in rows if isinstance(r, dict)), "all_blocked")
    ok(fs.get("full_frame_ocr_allowed") is False, "no_full_frame")
    ok(fs.get("mock_text_allowed") is False, "no_mock")
    ok(len(blocked) >= 34, "blocked_count")
    ok(any(
        "static_capture_result_missing" in (c.get("blocked_reason") or [])
        for c in blocked if isinstance(c, dict)
    ), "reason_missing")
    ok(data["memory_governance_link"].get("future_ocr_result_must_preserve_source_chain") is True, "mg_chain")
    ok(data["ep_v5_plan"].get("evidence_pack_v5_generated_now") is False, "ep5_later")
    ok(data["semantic_sv_plan"].get("semantic_candidate_v5_generated_now") is False, "sem_later")
    ok(data["semantic_sv_plan"].get("source_validation_v3_invoked_now") is False, "sv_later")
    ba = data["bypass_audit"]
    ok(ba.get("direct_provider_bypass") is False, "no_bypass")
    ok(ba.get("bridge_invoked") is False, "no_bridge")
    ok(data["long_term"].get("can_feed_long_term_candidate") is True, "lt")
    ok(data["final"].get("final_decision") == "BLOCK_OCRREQUEST_STATICREADING_UNTIL_CAPTURED_FRAME", "final")
    ok(data["boundary"].get("gate_dryrun_only") is True, "boundary")
    ok(data["metrics"].get("ocrrequest_submitted_count") == 0, "submit_0")
    ok(data["metrics"].get("no_write_boundary_pass_rate") == 1.0, "nw_rate")
    ok(data["bench"].get("benchmark_score_generated") is False, "bench")
    ok(data["health"].get("no_runtime_health_claim") is True, "health")
    ok(data["no_write"].get("boundary_ok") is True, "nw_ok")
    ok(data["no_write"].get("violations") == [], "violations")
    ok(data["sim"].get("simulation_profile_id") == "developer_full", "sim")
    ok(data["audit"].get("midplatform_fact_written") is False, "audit_mp")
    ok(data["audit"].get("world_model_written") is False, "audit_wm")
    ok(data["audit"].get("scene_delta_candidate_generated") is False, "audit_sd")
    ok(data["audit"].get("runtime_routing_changed") is False, "audit_route")

    verdict = "GO" if not blockers else "NO_GO"
    report = {
        "verdict": verdict,
        "checks_passed": checks,
        "checks_expected": 64,
        "blockers": blockers,
        "phase": "OCRRequest-Gated-Submission-from-StaticReading-v1-001",
    }
    _write_json(root / "ocrrequest_staticreading_verifier_report_v1.json", report)
    print(json.dumps(report, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
