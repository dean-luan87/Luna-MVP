#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for Static Readable Region Discovery Guidance Policy v1."""

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
        "summary": "static_readable_region_discovery_guidance_policy_v1_summary.json",
        "intake": "static_readable_region_input_intake_matrix_v1.json",
        "scope": "static_readable_region_discovery_scope_policy_v1.json",
        "schema": "static_readable_region_candidate_schema_v1.json",
        "filter": "static_readable_region_readability_filtering_policy_v1.json",
        "classify": "static_readable_region_classification_policy_v1.json",
        "guidance": "static_readable_region_user_view_guidance_policy_v1.json",
        "ranking": "static_readable_region_ranking_selection_policy_v1.json",
        "capture": "static_readable_region_static_capture_handoff_policy_v1.json",
        "ocr_link": "static_readable_region_ocrrequest_future_gate_link_policy_v1.json",
        "human": "static_readable_region_human_staff_assistance_preservation_policy_v1.json",
        "expired": "static_readable_region_unresolved_expired_candidate_policy_v1.json",
        "current": "static_readable_region_current_case_dryrun_v1.json",
        "boundary": "static_readable_region_boundary_report_v1.json",
        "metrics": "static_readable_region_metrics_candidate_report_v1.json",
        "bench": "static_readable_region_benchmark_link_report_v1.json",
        "health": "static_readable_region_system_health_link_report_v1.json",
        "no_write": "static_readable_region_no_write_boundary_report_v1.json",
        "sim": "static_readable_region_simulation_context_report_v1.json",
        "non_claims": "static_readable_region_non_claims_report_v1.json",
        "followups": "static_readable_region_open_followups_v1.json",
        "audit": "static_readable_region_audit_report_v1.json",
    }
    data: Dict[str, Any] = {}
    for k, f in files.items():
        p = root / f
        if not p.is_file():
            blockers.append(f"missing:{k}")
        else:
            data[k] = json.loads(p.read_text(encoding="utf-8"))

    if blockers:
        _write_json(root / "static_readable_region_verifier_report_v1.json", {"verdict": "NO_GO", "blockers": blockers})
        print(json.dumps({"verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    s = data["summary"]
    scope = data["scope"]
    schema = data["schema"]
    filt = data["filter"]
    cls = data["classify"]
    g = data["guidance"]
    cap = data["capture"]
    ocr = data["ocr_link"]
    human = data["human"]
    expired = data["expired"]
    current = data["current"]
    boundary = data["boundary"]
    metrics = data["metrics"]
    bench = data["bench"]
    health = data["health"]
    no_write = data["no_write"]
    sim = data["sim"]
    audit = data["audit"]

    ok(True, "summary")
    ok(s.get("policy_scope") == "readable_region_discovery_guidance_policy_only", "scope_field")
    ok(s.get("based_on_information_source_localization") is True, "based_isrc")
    ok(s.get("candidate_information_source_handoff_consumed") is True, "handoff")
    ok(s.get("global_text_search_forbidden_by_default") is True, "no_global")
    ok(s.get("detector_invoked") is False, "no_detector")
    ok(s.get("ocr_invoked") is False, "no_ocr")

    forbidden = [x.get("scope_type") for x in scope.get("forbidden_search_scope") or [] if isinstance(x, dict)]
    ok("full_frame_generic_text_search" in forbidden, "forbid_full_frame")
    ok(schema.get("bbox_candidate_unknown_by_default") is True, "bbox_unknown")
    ok(schema.get("readability_status_unknown_by_default") is True, "read_unknown")

    fdims = [d.get("filtering_dimension") for d in filt.get("dimensions") or [] if isinstance(d, dict)]
    for dim in ("task_relevance", "distance", "angle", "text_size"):
        ok(dim in fdims, dim)

    cnames = [c.get("class_name") for c in cls.get("classes") or [] if isinstance(c, dict)]
    for cn in ("READABLE_CANDIDATE", "UNREADABLE_BUT_REPAIRABLE", "NOT_WORTH_READING"):
        ok(cn in cnames, cn)

    acts = [a.get("guidance_action") for a in g.get("actions") or [] if isinstance(a, dict)]
    for act in ("center_region", "adjust_angle", "hold_still", "ask_external_assistance"):
        ok(act in acts, act)
    ok(all(a.get("tts_invoked_now") is False for a in g.get("actions") or [] if isinstance(a, dict)), "guidance_no_tts")

    rdims = [d.get("ranking_dimension") for d in data["ranking"].get("dimensions") or [] if isinstance(d, dict)]
    ok("task_relevance" in rdims and "safety_relevance" in rdims, "rank_safety")
    ok("privacy_sensitivity" in rdims, "rank_privacy")

    ok(cap.get("static_capture_invoked_now") is False, "cap_not_now")
    ok(ocr.get("ocrrequest_eligible_now") is False, "ocr_now_false")

    atypes = [c.get("assistance_type") for c in human.get("candidates") or [] if isinstance(c, dict)]
    ok("ask_staff_where_sign_is" in atypes, "ask_staff")

    ok(any(c.get("can_feed_long_term_candidate") is True for c in expired.get("candidates") or [] if isinstance(c, dict)), "expired_lt")

    ok(current.get("readable_region_discovery_invoked_now") is False, "rrd_not_now")
    reasons = current.get("reason_not_invoked") or []
    ok("missing_task_context" in reasons or "missing_scene_context" in reasons, "reason_missing_ctx")
    ok(boundary.get("policy_only") is True, "boundary")
    ok(metrics.get("no_write_boundary_pass_rate") == 1.0, "metrics")
    ok(bench.get("benchmark_score_generated") is False, "no_bench")
    ok(health.get("recovery_action_committed") is False, "no_recovery")
    ok(no_write.get("boundary_ok") is True, "nw_ok")
    ok(no_write.get("violations") == [], "violations")
    ok(sim.get("simulation_profile_id") == "developer_full", "sim")
    ok(audit.get("midplatform_fact_written") is False, "audit_no_fact")
    ok(audit.get("world_model_written") is False, "audit_no_wm")
    ok(audit.get("scene_delta_candidate_generated") is False, "audit_no_sd")
    ok(audit.get("navigation_decision_invoked") is False, "audit_no_nav")
    ok(audit.get("runtime_routing_changed") is False, "audit_no_route")

    verdict = "GO" if not blockers else "NO_GO"
    report = {
        "verdict": verdict,
        "checks_passed": checks,
        "checks_expected": 61,
        "blockers": blockers,
        "phase": "Static-Readable-Region-Discovery-Guidance-Policy-v1-001",
    }
    _write_json(root / "static_readable_region_verifier_report_v1.json", report)
    print(json.dumps(report, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
