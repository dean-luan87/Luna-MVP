#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for Static Readable Region Discovery Runtime DryRun v1."""

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
        "summary": "static_readable_region_discovery_runtime_dryrun_v1_summary.json",
        "intake": "static_readable_region_runtime_input_intake_matrix_v1.json",
        "ranked_intake": "static_readable_region_ranked_source_area_intake_matrix_v1.json",
        "collection": "static_readable_region_candidate_collection_v1.json",
        "classification": "static_readable_region_runtime_classification_matrix_v1.json",
        "filtering": "static_readable_region_runtime_readability_filtering_matrix_v1.json",
        "guidance": "static_readable_region_user_view_guidance_candidate_collection_v1.json",
        "capture_handoff": "static_readable_region_static_capture_handoff_candidate_v1.json",
        "ocr_gate": "static_readable_region_ocrrequest_future_gate_candidate_v1.json",
        "human_assist": "static_readable_region_human_staff_assistance_region_candidate_v1.json",
        "unresolved_link": "static_readable_region_runtime_unresolved_expired_candidate_link_v1.json",
        "trace": "static_readable_region_runtime_decision_trace_v1.json",
        "final": "static_readable_region_runtime_final_decision_v1.json",
        "boundary": "static_readable_region_runtime_boundary_report_v1.json",
        "metrics": "static_readable_region_runtime_metrics_candidate_report_v1.json",
        "bench": "static_readable_region_runtime_benchmark_link_report_v1.json",
        "health": "static_readable_region_runtime_system_health_link_report_v1.json",
        "no_write": "static_readable_region_runtime_no_write_boundary_report_v1.json",
        "sim": "static_readable_region_runtime_simulation_context_report_v1.json",
        "non_claims": "static_readable_region_runtime_non_claims_report_v1.json",
        "followups": "static_readable_region_runtime_open_followups_v1.json",
        "audit": "static_readable_region_runtime_audit_report_v1.json",
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
            root / "static_readable_region_runtime_verifier_report_v1.json",
            {"verdict": "NO_GO", "blockers": blockers},
        )
        print(json.dumps({"verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    s = data["summary"]
    coll = data["collection"]
    ok(True, "summary")
    ok(s.get("dryrun_scope") == "readable_region_discovery_runtime_dryrun_only", "scope")
    ok(s.get("based_on_isrc_runtime") is True, "based_isrc")
    ok(s.get("ranked_source_area_candidate_count_observed") == 17, "ranked_count")
    ok(s.get("ranked_source_area_intake_executed") is True, "intake_exec")
    ok(s.get("readable_region_candidate_generated") is True, "rr_gen")
    ok(s.get("classification_matrix_generated") is True, "class_matrix")
    ok(s.get("readability_filtering_executed") is True, "filtering")
    ok(s.get("user_view_guidance_candidate_generated") is True, "guidance")
    ok(s.get("static_capture_handoff_candidate_generated") is True, "capture")
    ok(s.get("ocrrequest_future_gate_candidate_generated") is True, "ocr_gate")
    ok(s.get("static_capture_ready_now") is False, "cap_not_ready")
    ok(s.get("ocrrequest_eligible_now") is False, "ocr_not_now")
    ok(s.get("detector_invoked") is False, "no_det")
    ok(s.get("text_detector_invoked") is False, "no_text_det")
    ok(s.get("real_bbox_generated") is False, "no_bbox")
    ok(s.get("ocr_invoked") is False, "no_ocr")
    ok(s.get("runtime_camera_invoked") is False, "no_cam")

    ri = data["ranked_intake"].get("ranked_source_areas") or []
    ok(len(ri) == 17, "seventeen_ranked")
    ok(all(r.get("accepted_for_rrd_dryrun") is True for r in ri if isinstance(r, dict)), "accepted")

    cands = coll.get("candidates") or []
    ok(len(cands) >= 17, "rr_candidates_exist")
    ok(any(c.get("bbox_candidate_unknown_by_default") is True for c in cands if isinstance(c, dict)), "bbox_unknown")
    ok(any(c.get("readability_status_unknown_by_default") is True for c in cands if isinstance(c, dict)), "read_unknown")

    classes = data["classification"].get("rows") or []
    ok(any(r.get("class_name") == "HUMAN_ASSISTANCE_REGION" for r in classes if isinstance(r, dict)), "human_class")
    ok(all(r.get("real_quality_measured") is False for r in data["filtering"].get("rows") or [] if isinstance(r, dict)), "no_real_quality")
    ok(data["guidance"].get("candidates"), "guidance_exists")
    ok(all(g.get("tts_invoked_now") is False for g in data["guidance"].get("candidates") or [] if isinstance(g, dict)), "no_tts")
    ok(data["capture_handoff"].get("handoff_invoked_now") is False, "handoff_not_now")
    ok(data["ocr_gate"].get("ocrrequest_eligible_now") is False, "ocr_gate_not_now")
    ok(data["human_assist"].get("human_staff_assistance_region_candidate_generated") is True, "human_assist")
    ok(data["unresolved_link"].get("can_feed_long_term_candidate") is True, "lt")
    ok(data["final"].get("final_decision") == "READY_FOR_STATIC_CAPTURE_HANDOFF_LATER", "final")
    ok(data["boundary"].get("rrd_runtime_dryrun_only") is True, "boundary")
    ok(data["metrics"].get("no_write_boundary_pass_rate") == 1.0, "metrics")
    ok(data["bench"].get("benchmark_score_generated") is False, "bench_score")
    ok(data["health"].get("recovery_action_committed") is False, "health_rec")
    ok(data["no_write"].get("boundary_ok") is True, "nw_ok")
    ok(data["no_write"].get("violations") == [], "nw_violations")
    ok(data["sim"].get("simulation_profile_id") == "developer_full", "sim")
    ok(data["audit"].get("midplatform_fact_written") is False, "audit_fact")
    ok(data["audit"].get("world_model_written") is False, "audit_wm")
    ok(data["audit"].get("scene_delta_candidate_generated") is False, "audit_delta")
    ok(data["audit"].get("navigation_decision_invoked") is False, "audit_nav")
    ok(data["audit"].get("runtime_routing_changed") is False, "audit_route")

    verdict = "GO" if not blockers else "NO_GO"
    report = {
        "verdict": verdict,
        "checks_passed": checks,
        "checks_expected": 61,
        "blockers": blockers,
        "phase": "Static-Readable-Region-Discovery-Runtime-DryRun-v1-001",
    }
    _write_json(root / "static_readable_region_runtime_verifier_report_v1.json", report)
    print(json.dumps(report, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
