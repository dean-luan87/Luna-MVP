#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for Vision-OCR Evidence Ingest Integration Check v1."""

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
        "summary": "vision_ocr_evidence_ingest_integration_check_v1_summary.json",
        "intake": "vision_ocr_evidence_ingest_input_intake_matrix_v1.json",
        "obs_intake": "vision_ocr_observation_request_intake_matrix_v1.json",
        "vision_schema": "vision_evidence_ingest_schema_v1.json",
        "ocr_schema": "ocr_evidence_ingest_schema_v1.json",
        "lifecycle_policy": "vision_ocr_evidence_lifecycle_policy_v1.json",
        "separation_matrix": "vision_ocr_baseline_task_evidence_separation_matrix_v1.json",
        "ocr_joint_gate": "vision_ocr_ingest_ocr_joint_gate_check_v1.json",
        "vision_collection": "vision_evidence_candidate_collection_v1.json",
        "ocr_collection": "ocr_evidence_candidate_collection_v1.json",
        "action_support_collection": "vision_ocr_action_support_evidence_candidate_collection_v1.json",
        "verification_collection": "vision_ocr_verification_support_evidence_candidate_collection_v1.json",
        "feedback_contract": "vision_ocr_evidence_to_task_feedback_contract_v1.json",
        "freshness_policy": "vision_ocr_evidence_freshness_expiry_policy_v1.json",
        "bypass_audit": "vision_ocr_provider_runtime_bypass_audit_v1.json",
        "trace": "vision_ocr_evidence_ingest_decision_trace_v1.json",
        "final": "vision_ocr_evidence_ingest_final_decision_v1.json",
        "boundary": "vision_ocr_evidence_ingest_boundary_report_v1.json",
        "metrics": "vision_ocr_evidence_ingest_metrics_candidate_report_v1.json",
        "benchmark_link": "vision_ocr_evidence_ingest_benchmark_link_report_v1.json",
        "health_report": "vision_ocr_evidence_ingest_system_health_report_v1.json",
        "no_write": "vision_ocr_evidence_ingest_no_write_boundary_report_v1.json",
        "sim_report": "vision_ocr_evidence_ingest_simulation_context_report_v1.json",
        "non_claims": "vision_ocr_evidence_ingest_non_claims_report_v1.json",
        "followups": "vision_ocr_evidence_ingest_open_followups_v1.json",
        "audit": "vision_ocr_evidence_ingest_audit_report_v1.json",
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
            root / "vision_ocr_evidence_ingest_verifier_report_v1.json",
            {"verdict": "NO_GO", "blockers": blockers},
        )
        print(json.dumps({"verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    s = data["summary"]
    ok(s.get("check_scope") == "vision_ocr_evidence_ingest_integration_check_only", "scope")
    ok(s.get("based_on_task_observation_request_contract") is True, "obs_contract")
    ok(s.get("observation_request_candidate_count_observed") == 16, "obs_16")
    ok(s.get("baseline_request_candidate_count_observed") == 4, "baseline_4")
    ok(s.get("task_driven_request_candidate_count_observed") == 12, "td_12")
    ok(s.get("vision_evidence_ingest_schema_defined") is True, "vision_schema")
    ok(s.get("ocr_evidence_ingest_schema_defined") is True, "ocr_schema")
    ok(s.get("evidence_lifecycle_policy_defined") is True, "lifecycle")
    ok(s.get("ocr_joint_gate_check_applied") is True, "ocr_gate")
    ok(s.get("action_support_evidence_candidate_generated") is True, "action_gen")
    ok(s.get("verification_support_evidence_candidate_generated") is True, "verify_gen")
    ok(s.get("camera_invoked") is False, "no_camera")
    ok(s.get("ocr_provider_invoked") is False, "no_ocr_provider")
    ok(s.get("ocrrequest_submitted") is False, "no_ocrrequest")

    obs_rows = data["obs_intake"].get("rows") or []
    ok(len(obs_rows) == 16, "obs_rows_16")
    ok(all(r.get("accepted_for_ingest_check") for r in obs_rows), "all_accepted")

    ok(data["vision_schema"].get("can_write_fact_now") is False, "vision_no_fact")
    ok(data["ocr_schema"].get("empty_text_is_not_no_text_fact") is True, "empty_not_fact")

    lc = data["lifecycle_policy"]
    ok(lc.get("evidence_not_fact_by_default") is True, "not_fact_default")

    sep = data["separation_matrix"].get("rows") or []
    baseline_sep = next((r for r in sep if r.get("loop_type") == "baseline_safety"), None)
    ok(baseline_sep and baseline_sep.get("can_support_task_verification") is False, "baseline_no_complete")

    og = data["ocr_joint_gate"]
    ok(og.get("ocr_allowed_now") is False, "ocr_not_now")
    ok(all(g.get("ocr_provider_invoked_now") is False for g in og.get("gates") or []), "gate_no_provider")

    vc = data["vision_collection"]
    ok(vc.get("vision_evidence_candidate_count", 0) >= 16, "vision_16")

    oc = data["ocr_collection"]
    ok(all(c.get("raw_text_candidate") is None for c in oc.get("candidates") or []), "raw_null")

    asc = data["action_support_collection"]
    ok(all(c.get("can_trigger_action_directly") is False for c in asc.get("candidates") or []), "as_no_action")

    vsc = data["verification_collection"]
    ok(all(c.get("can_complete_task_alone") is False for c in vsc.get("candidates") or []), "vs_no_alone")
    ok(vsc.get("task_completed_now") is False, "not_completed")

    fb = data["feedback_contract"]
    ok(fb.get("feedback_invoked_now") is False, "fb_not_invoked")

    fp = data["freshness_policy"]
    ok(fp.get("stale_evidence_blocks_action_support") is True, "stale_block")

    ba = data["bypass_audit"]
    ok(ba.get("direct_provider_bypass") is False, "no_bypass")
    ok(ba.get("rapidocr_invoked") is False, "no_rapidocr")
    ok(ba.get("paddleocr_invoked") is False, "no_paddle")

    final = data["final"]
    ok(
        final.get("final_decision") == "VISION_OCR_EVIDENCE_INGEST_READY_FOR_NAVIGATION_GUIDANCE_LOOP",
        "final_decision",
    )
    ok(final.get("recommended_next_phase") == "Navigation-Guidance-to-Speech-Candidate-Adapter-v1", "next")

    ok(data["boundary"].get("integration_check_only") is True, "check_only")
    ok(data["metrics"].get("no_write_boundary_pass_rate") == 1.0, "nw_rate")
    ok(data["no_write"].get("boundary_ok") is True, "nw_ok")
    ok(data["audit"].get("midplatform_fact_written") is False, "audit")

    verdict = "GO" if not blockers else "NO_GO"
    report = {
        "verdict": verdict,
        "checks_passed": checks,
        "checks_expected": 66,
        "blockers": blockers,
        "final_decision": final.get("final_decision"),
        "phase": "Vision-OCR-Evidence-Ingest-Integration-Check-v1-001",
    }
    _write_json(root / "vision_ocr_evidence_ingest_verifier_report_v1.json", report)
    print(json.dumps(report, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
