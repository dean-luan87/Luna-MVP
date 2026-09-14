#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for Static Reading Task Scene Context Reevaluation DryRun v1."""

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


def _find_row(matrix: Dict[str, Any], raw_substr: str) -> Dict[str, Any]:
    for r in matrix.get("rows") or []:
        if isinstance(r, dict) and raw_substr in (r.get("raw_user_response") or ""):
            return r
    return {}


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
        "summary": "static_reading_task_scene_context_reevaluation_dryrun_v1_summary.json",
        "intake": "static_reading_task_scene_reevaluation_input_intake_matrix_v1.json",
        "reeval_matrix": "static_reading_task_scene_candidate_reevaluation_matrix_v1.json",
        "completeness": "static_reading_task_scene_completeness_summary_v1.json",
        "confirmation": "static_reading_task_scene_confirmation_requirement_matrix_v1.json",
        "query_collection": "static_reading_information_source_query_candidate_collection_v1.json",
        "isrc_readiness": "static_reading_isrc_runtime_readiness_candidate_v1.json",
        "rrd_readiness": "static_reading_rrd_runtime_readiness_candidate_v1.json",
        "human_reeval": "static_reading_task_scene_human_staff_reevaluation_v1.json",
        "long_term": "static_reading_task_scene_reevaluation_long_term_candidate_link_v1.json",
        "trace": "static_reading_task_scene_reevaluation_decision_trace_v1.json",
        "final": "static_reading_task_scene_reevaluation_final_decision_v1.json",
        "boundary": "static_reading_task_scene_reevaluation_boundary_report_v1.json",
        "metrics": "static_reading_task_scene_reevaluation_metrics_candidate_report_v1.json",
        "bench": "static_reading_task_scene_reevaluation_benchmark_link_report_v1.json",
        "health": "static_reading_task_scene_reevaluation_system_health_link_report_v1.json",
        "no_write": "static_reading_task_scene_reevaluation_no_write_boundary_report_v1.json",
        "sim": "static_reading_task_scene_reevaluation_simulation_context_report_v1.json",
        "non_claims": "static_reading_task_scene_reevaluation_non_claims_report_v1.json",
        "followups": "static_reading_task_scene_reevaluation_open_followups_v1.json",
        "audit": "static_reading_task_scene_reevaluation_audit_report_v1.json",
    }
    data: Dict[str, Any] = {}
    for k, f in files.items():
        p = root / f
        if not p.is_file():
            blockers.append(f"missing:{k}")
        else:
            data[k] = json.loads(p.read_text(encoding="utf-8"))

    if blockers:
        _write_json(root / "static_reading_task_scene_reevaluation_verifier_report_v1.json", {"verdict": "NO_GO", "blockers": blockers})
        print(json.dumps({"verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    s = data["summary"]
    m = data["reeval_matrix"]
    ok(True, "summary")
    ok(s.get("dryrun_scope") == "task_scene_context_reevaluation_dryrun_only", "scope")
    ok(s.get("based_on_response_parsing") is True, "based_parsing")
    ok(s.get("candidate_reevaluation_executed") is True, "reeval")
    ok(s.get("complete_context_candidate_count_computed") is True, "complete_computed")
    ok(s.get("information_source_query_candidate_generated") is True, "query_gen")
    ok(s.get("isrc_runtime_ready_candidate_generated") is True, "isrc_ready")
    ok(s.get("rrd_runtime_ready_now") is False, "rrd_not_ready")
    ok(s.get("task_context_written_now") is False, "no_task_write")
    ok(s.get("information_source_runtime_invoked_now") is False, "no_isrc")
    ok(s.get("readable_region_runtime_invoked_now") is False, "no_rrd")
    ok(s.get("asr_invoked") is False, "no_asr")
    ok(s.get("llm_invoked") is False, "no_llm")

    ok(_find_row(m, "找出口").get("context_completeness_status") == "complete_candidate", "exit_mall_complete")
    ok(_find_row(m, "门牌").get("context_completeness_status") == "partial_task_only", "doorplate_partial")
    ok(_find_row(m, "医院里").get("context_completeness_status") == "complete_candidate", "hospital_complete")
    ok(_find_row(m, "读这段").get("context_completeness_status") == "partial_task_only", "read_partial")
    ok(_find_row(m, "不知道").get("context_completeness_status") == "insufficient_context", "insufficient")
    ok(_find_row(m, "工作人员").get("context_completeness_status") == "human_staff_assistance_requested", "human")
    ok(_find_row(m, "洗手间").get("context_completeness_status") == "complete_candidate", "restroom_complete")
    ok(_find_row(m, "几号线").get("context_completeness_status") == "complete_candidate", "transit_complete")

    ok(data["completeness"].get("complete_candidate_count", 0) >= 1, "complete_count")
    ok(data["query_collection"].get("query_candidates"), "queries_exist")
    ok(all(q.get("handoff_invoked_now") is False for q in data["query_collection"].get("query_candidates") or [] if isinstance(q, dict)), "handoff_not_now")
    ok(data["isrc_readiness"].get("information_source_runtime_invoked_now") is False, "isrc_not_invoked")
    ok(data["rrd_readiness"].get("rrd_runtime_ready_now") is False, "rrd_blocked")
    ok(data["human_reeval"].get("human_staff_assistance_candidate_present") is True, "human_present")
    ok(data["long_term"].get("can_feed_long_term_candidate") is True, "lt")
    ok(data["final"].get("final_decision") == "READY_FOR_INFORMATION_SOURCE_LOCALIZATION_RUNTIME_LATER", "final")
    ok(data["boundary"].get("reevaluation_dryrun_only") is True, "boundary")
    ok(data["metrics"].get("no_write_boundary_pass_rate") == 1.0, "metrics")
    ok(data["no_write"].get("boundary_ok") is True, "nw_ok")
    ok(data["sim"].get("simulation_profile_id") == "developer_full", "sim")
    ok(data["audit"].get("midplatform_fact_written") is False, "audit_fact")
    ok(data["audit"].get("world_model_written") is False, "audit_wm")
    ok(data["audit"].get("runtime_routing_changed") is False, "audit_route")

    verdict = "GO" if not blockers else "NO_GO"
    report = {
        "verdict": verdict,
        "checks_passed": checks,
        "checks_expected": 64,
        "blockers": blockers,
        "phase": "Static-Reading-Task-Scene-Context-Reevaluation-DryRun-v1-001",
    }
    _write_json(root / "static_reading_task_scene_reevaluation_verifier_report_v1.json", report)
    print(json.dumps(report, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
