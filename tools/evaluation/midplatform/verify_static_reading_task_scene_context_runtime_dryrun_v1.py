#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for Static Reading Task Scene Context Runtime DryRun v1."""

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
        "summary": "static_reading_task_scene_context_runtime_dryrun_v1_summary.json",
        "intake": "static_reading_task_scene_context_runtime_input_intake_matrix_v1.json",
        "task_intake": "static_reading_task_context_runtime_intake_v1.json",
        "scene_intake": "static_reading_scene_context_runtime_intake_v1.json",
        "missing": "static_reading_missing_context_runtime_handling_v1.json",
        "clarification": "static_reading_user_clarification_candidate_runtime_v1.json",
        "confidence": "static_reading_context_confidence_runtime_evaluation_v1.json",
        "query": "static_reading_information_source_query_runtime_candidate_v1.json",
        "rrd": "static_reading_rrd_runtime_preconditions_evaluation_v1.json",
        "trace": "static_reading_task_scene_context_runtime_decision_trace_v1.json",
        "final": "static_reading_task_scene_context_runtime_final_decision_v1.json",
        "long_term": "static_reading_task_scene_context_long_term_candidate_link_v1.json",
        "boundary": "static_reading_task_scene_context_runtime_boundary_report_v1.json",
        "metrics": "static_reading_task_scene_context_runtime_metrics_candidate_report_v1.json",
        "bench": "static_reading_task_scene_context_runtime_benchmark_link_report_v1.json",
        "health": "static_reading_task_scene_context_runtime_system_health_link_report_v1.json",
        "no_write": "static_reading_task_scene_context_runtime_no_write_boundary_report_v1.json",
        "sim": "static_reading_task_scene_context_runtime_simulation_context_report_v1.json",
        "non_claims": "static_reading_task_scene_context_runtime_non_claims_report_v1.json",
        "followups": "static_reading_task_scene_context_runtime_open_followups_v1.json",
        "audit": "static_reading_task_scene_context_runtime_audit_report_v1.json",
    }
    data: Dict[str, Any] = {}
    for k, f in files.items():
        p = root / f
        if not p.is_file():
            blockers.append(f"missing:{k}")
        else:
            data[k] = json.loads(p.read_text(encoding="utf-8"))

    if blockers:
        _write_json(root / "static_reading_task_scene_context_runtime_verifier_report_v1.json", {"verdict": "NO_GO", "blockers": blockers})
        print(json.dumps({"verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    s = data["summary"]
    ok(True, "summary")
    ok(s.get("dryrun_scope") == "task_scene_context_runtime_dryrun_only", "scope")
    ok(s.get("based_on_task_scene_context_policy") is True, "based_tsc")
    ok(s.get("current_case_loaded") is True, "case_loaded")
    ok(s.get("task_context_available") is False, "task_false")
    ok(s.get("scene_context_available") is False, "scene_false")
    ok(s.get("missing_context_status") == "missing_both_task_and_scene", "missing_both")
    ok(s.get("user_clarification_candidate_generated") is True, "clarify_gen")
    ok(s.get("task_context_candidate_generated") is False, "no_task_cand")
    ok(s.get("scene_context_candidate_generated") is False, "no_scene_cand")
    ok(s.get("information_source_query_candidate_generated") is False, "no_query")
    ok(s.get("ranked_information_source_area_generated") is False, "no_ranked")
    ok(s.get("readable_region_runtime_preconditions_met_now") is False, "rrd_unmet")
    ok(s.get("readable_region_runtime_invoked_now") is False, "rrd_not_invoked")
    ok(s.get("information_source_runtime_invoked_now") is False, "isrc_not_invoked")
    ok(s.get("scene_detector_invoked") is False, "no_detector")
    ok(s.get("ocr_invoked") is False, "no_ocr")

    ok(data["task_intake"].get("task_context_fabrication_forbidden") is True, "task_fab_forbidden")
    ok(data["scene_intake"].get("scene_context_fabrication_forbidden") is True, "scene_fab_forbidden")
    ok(data["missing"].get("readable_region_discovery_allowed_now") is False, "rrd_blocked")
    ok(data["missing"].get("information_source_localization_runtime_allowed_now") is False, "isrc_blocked")

    cands = data["clarification"].get("candidates") or []
    prompts = [c.get("prompt_candidate") for c in cands if isinstance(c, dict)]
    ok(any("你想找什么信息" in (p or "") for p in prompts), "clarify_prompt")
    ok(all(c.get("tts_invoked_now") is False for c in cands if isinstance(c, dict)), "no_tts")

    ok(data["confidence"].get("context_status") == "insufficient_context", "insufficient")
    ok(data["query"].get("query_candidate_generated") is False, "query_false")
    ok(data["rrd"].get("runtime_preconditions_met_now") is False, "precond_false")

    steps = [st.get("step_name") for st in data["trace"].get("steps") or [] if isinstance(st, dict)]
    ok("generate_final_runtime_dryrun_decision" in steps, "final_step")

    ok(data["final"].get("final_decision") == "WAIT_FOR_USER_CLARIFICATION", "final_decision")
    ok(data["final"].get("task_context_fabricated") is False, "no_task_fab")
    ok(data["final"].get("scene_context_fabricated") is False, "no_scene_fab")

    ok(data["long_term"].get("can_feed_long_term_candidate") is True, "lt_candidate")
    ok(data["boundary"].get("runtime_dryrun_only") is True, "boundary")
    ok(data["metrics"].get("no_write_boundary_pass_rate") == 1.0, "metrics")
    ok(data["bench"].get("benchmark_score_generated") is False, "bench")
    ok(data["health"].get("recovery_action_committed") is False, "health")
    ok(data["no_write"].get("boundary_ok") is True, "nw_ok")
    ok(data["no_write"].get("violations") == [], "violations")
    ok(data["sim"].get("simulation_profile_id") == "developer_full", "sim")
    ok(data["audit"].get("midplatform_fact_written") is False, "audit_fact")
    ok(data["audit"].get("world_model_written") is False, "audit_wm")
    ok(data["audit"].get("scene_delta_candidate_generated") is False, "audit_sd")
    ok(data["audit"].get("navigation_decision_invoked") is False, "audit_nav")
    ok(data["audit"].get("runtime_routing_changed") is False, "audit_route")

    verdict = "GO" if not blockers else "NO_GO"
    report = {
        "verdict": verdict,
        "checks_passed": checks,
        "checks_expected": 66,
        "blockers": blockers,
        "phase": "Static-Reading-Task-Scene-Context-Runtime-DryRun-v1-001",
    }
    _write_json(root / "static_reading_task_scene_context_runtime_verifier_report_v1.json", report)
    print(json.dumps(report, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
