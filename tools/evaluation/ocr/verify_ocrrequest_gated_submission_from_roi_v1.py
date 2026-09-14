#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for OCRRequest Gated Submission from ROI v1."""

from __future__ import annotations

import argparse
import json
import sys
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
        "summary": "ocrrequest_gated_submission_from_roi_v1_summary.json",
        "intake": "ocrrequest_roi_submission_intake_matrix_v1.json",
        "gate": "ocrrequest_roi_submission_gate_policy_v1.json",
        "plan": "ocrrequest_roi_submission_plan_v1.json",
        "trace": "ocrrequest_roi_bridge_invocation_trace_v1.json",
        "bypass": "ocrrequest_roi_direct_provider_bypass_audit_v1.json",
        "collection": "roi_ocr_result_collection_v1.json",
        "matrix": "roi_ocr_result_matrix_v1.json",
        "guard": "roi_ocr_empty_nonempty_guard_report_v1.json",
        "chain": "roi_ocr_source_chain_report_v1.json",
        "provider": "roi_ocr_provider_summary_report_v1.json",
        "no_ep": "roi_ocr_no_evidence_pack_boundary_report_v1.json",
        "future": "roi_ocr_future_adapter_plan_v1.json",
        "boundary": "roi_ocr_boundary_report_v1.json",
        "metrics": "roi_ocr_metrics_candidate_report_v1.json",
        "bench": "roi_ocr_benchmark_link_report_v1.json",
        "health": "roi_ocr_system_health_link_report_v1.json",
        "no_write": "roi_ocr_no_write_boundary_report_v1.json",
        "sim": "roi_ocr_simulation_context_report_v1.json",
        "non_claims": "roi_ocr_non_claims_report_v1.json",
        "followups": "roi_ocr_open_followups_v1.json",
        "audit": "roi_ocr_audit_report_v1.json",
    }
    data = {}
    for k, f in files.items():
        p = root / f
        if not p.is_file():
            blockers.append(f"missing:{k}")
        else:
            data[k] = _read_json(p)

    if blockers:
        _write_json(root / "roi_ocr_verifier_report_v1.json", {"verdict": "NO_GO", "blockers": blockers})
        print(json.dumps({"verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    s = data["summary"]
    intake = data["intake"]
    gate = data["gate"]
    plan = data["plan"]
    trace = data["trace"]
    bypass = data["bypass"]
    collection = data["collection"]
    guard = data["guard"]
    chain = data["chain"]
    provider = data["provider"]
    no_ep = data["no_ep"]
    future = data["future"]
    boundary = data["boundary"]
    metrics = data["metrics"]
    audit = data["audit"]

    ok(s.get("submission_scope") == "roi_ocrrequest_gated_submission_only", "scope")
    ok(s.get("based_on_roi_ocrrequest_reference") is True, "based_ref")
    ok(s.get("ocrrequest_reference_count_observed") == 12, "ref_12")
    ok(s.get("ocr_invoked") is True, "ocr_invoked")
    ok(s.get("provider_invoked") is True, "provider_invoked")
    ok(s.get("direct_provider_bypass") is False, "no_bypass")
    ok(s.get("every_provider_call_has_ocrrequest_ref") is True, "has_ref")
    ok(s.get("full_frame_ocr_invoked") is False, "no_full_frame")
    ok(s.get("mock_text_used") is False, "no_mock")

    ok(intake.get("row_count") == 12, "intake_12")
    for row in intake.get("rows") or []:
        if isinstance(row, dict):
            ok(row.get("full_frame_ocr_allowed") is False, "intake_no_ff")
            ok(row.get("mock_text_allowed") is False, "intake_no_mock")
            break

    rule_ids = [r.get("rule_id") for r in (gate.get("rules") or []) if isinstance(r, dict)]
    ok("direct_provider_bypass_forbidden" in rule_ids, "rule_bypass")
    ok("full_frame_ocr_forbidden" in rule_ids, "rule_ff")
    ok(gate.get("direct_provider_bypass_forbidden") is True, "gate_bypass_flag")

    submitted = int(s.get("ocrrequest_submitted_count") or 0)
    selected = int(plan.get("selected_for_submission_count") or 0)
    ok(plan.get("row_count") == 12, "plan_12")
    ok(selected == submitted, "plan_submitted_align")

    ok(trace.get("row_count") == submitted, "trace_count")
    for row in trace.get("rows") or []:
        if isinstance(row, dict):
            ok(bool(row.get("ocrrequest_reference_id")), "trace_has_ref")
            ok(row.get("direct_provider_bypass") is False, "trace_no_bypass")
            break

    ok(bypass.get("capability_imports_rapidocr") is False, "no_rapid_import")
    ok(bypass.get("direct_provider_call_detected") is False, "no_direct_call")

    ok(collection.get("result_count") == 12, "coll_12")
    ok(collection.get("result_count") == submitted or submitted <= 12, "coll_submitted")
    for row in collection.get("rows") or []:
        if isinstance(row, dict) and row.get("result_status") not in ("skipped_not_selected",):
            ok(row.get("raw_output_preserved") is True, "raw_preserved")
            break

    ok(data["matrix"].get("row_count") == 12, "matrix_12")
    ok(guard.get("empty_text_is_not_no_text_fact") is True, "guard_empty")
    ok(guard.get("non_empty_text_is_not_accuracy") is True, "guard_accuracy")
    ok(chain.get("all_traceable_to_ocrrequest_reference") is True, "chain_ref")
    ok(provider.get("provider_comparison_claimed") is False, "no_comparison")
    ok(no_ep.get("evidence_pack_generated") is False, "no_ep")
    ok(no_ep.get("semantic_candidate_generated") is False, "no_semantic")

    phases = [p.get("future_phase") for p in (future.get("phases") or []) if isinstance(p, dict)]
    ok("Evidence-Pack-Adapter-v2-ROIRef" in phases, "future_ep")

    ok(boundary.get("world_model_attach_allowed") is False, "boundary_wm")
    ok(boundary.get("scene_delta_candidate_allowed") is False, "boundary_sd")
    ok(metrics.get("fact_write_allowed_count") == 0, "metrics_fact")
    ok(data["bench"].get("benchmark_score_generated") is False, "bench")
    ok(data["health"].get("provider_health_runtime_checked") is False, "health")
    ok(data["no_write"].get("boundary_ok") is True, "boundary_ok")
    ok(data["sim"].get("simulation_profile_id") == "developer_full", "sim")
    ok(audit.get("ocrrequest_gated_submission_from_roi_v1_executed") is True, "audit")
    ok(audit.get("world_model_attach_executed") is False, "audit_wm")
    ok(audit.get("midplatform_fact_written") is False, "audit_fact")

    verdict = "GO" if not blockers else "NO_GO"
    _write_json(
        root / "roi_ocr_verifier_report_v1.json",
        {"schema_version": "roi_ocr_verifier_report_v1", "verdict": verdict, "blockers": blockers, "checks_passed": checks},
    )
    print(json.dumps({"verdict": verdict, "blockers": blockers, "checks_passed": checks}, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
