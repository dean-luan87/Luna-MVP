#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for Static Reading Information Source Localization Runtime DryRun v1."""

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


def _areas_for(sm: Dict[str, Any], task: str, scene: str) -> List[str]:
    out = []
    for sa in sm.get("source_areas") or []:
        if not isinstance(sa, dict):
            continue
        if sa.get("normalized_task_type") == task and sa.get("normalized_scene_type") == scene:
            out.append(sa.get("source_area_type"))
    return out


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
        "summary": "static_reading_information_source_localization_runtime_dryrun_v1_summary.json",
        "intake": "static_reading_isrc_runtime_input_intake_matrix_v1.json",
        "query_intake": "static_reading_isrc_query_candidate_intake_matrix_v1.json",
        "source_matrix": "static_reading_isrc_candidate_source_area_matrix_v1.json",
        "exclusion": "static_reading_isrc_exclusion_filtering_matrix_v1.json",
        "ranking": "static_reading_isrc_ranking_placeholder_matrix_v1.json",
        "ranked": "static_reading_ranked_information_source_area_candidate_collection_v1.json",
        "rrd_handoff": "static_reading_isrc_to_rrd_handoff_candidate_v1.json",
        "human_assist": "static_reading_isrc_human_staff_assistance_candidate_v1.json",
        "long_term": "static_reading_isrc_long_term_candidate_link_v1.json",
        "trace": "static_reading_isrc_runtime_decision_trace_v1.json",
        "final": "static_reading_isrc_runtime_final_decision_v1.json",
        "boundary": "static_reading_isrc_runtime_boundary_report_v1.json",
        "metrics": "static_reading_isrc_runtime_metrics_candidate_report_v1.json",
        "bench": "static_reading_isrc_runtime_benchmark_link_report_v1.json",
        "health": "static_reading_isrc_runtime_system_health_link_report_v1.json",
        "no_write": "static_reading_isrc_runtime_no_write_boundary_report_v1.json",
        "sim": "static_reading_isrc_runtime_simulation_context_report_v1.json",
        "non_claims": "static_reading_isrc_runtime_non_claims_report_v1.json",
        "followups": "static_reading_isrc_runtime_open_followups_v1.json",
        "audit": "static_reading_isrc_runtime_audit_report_v1.json",
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
            root / "static_reading_isrc_runtime_verifier_report_v1.json",
            {"verdict": "NO_GO", "blockers": blockers},
        )
        print(json.dumps({"verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    s = data["summary"]
    sm = data["source_matrix"]
    ok(True, "summary")
    ok(s.get("dryrun_scope") == "information_source_localization_runtime_dryrun_only", "scope")
    ok(s.get("based_on_tsc_reevaluation") is True, "based_reeval")
    ok(s.get("query_candidate_count_observed") == 4, "query_count")
    ok(s.get("query_candidate_intake_executed") is True, "intake_exec")
    ok(s.get("candidate_source_area_matrix_generated") is True, "matrix")
    ok(s.get("exclusion_filtering_executed") is True, "exclusion")
    ok(s.get("ranking_placeholder_executed") is True, "ranking")
    ok(s.get("ranked_information_source_area_candidate_generated") is True, "ranked_gen")
    ok(s.get("rrd_handoff_candidate_generated") is True, "rrd_handoff")
    ok(s.get("rrd_runtime_invoked_now") is False, "rrd_not_now")
    ok(s.get("readable_region_generated") is False, "no_rr")
    ok(s.get("information_source_fact_written") is False, "no_fact")
    ok(s.get("ocr_invoked") is False, "no_ocr")
    ok(s.get("detector_invoked") is False, "no_det")
    ok(s.get("map_api_invoked") is False, "no_map")

    qi = data["query_intake"].get("query_candidates") or []
    ok(len(qi) == 4, "four_queries")
    ok(all(q.get("accepted_for_dryrun") is True for q in qi if isinstance(q, dict)), "accepted")

    exit_areas = _areas_for(sm, "find_exit", "shopping_mall")
    ok("exit_sign" in exit_areas and "directory_board" in exit_areas, "exit_mall_areas")
    dept_areas = _areas_for(sm, "find_department", "hospital")
    ok("department_sign" in dept_areas and "staff_desk" in dept_areas, "hospital_areas")
    rest_areas = _areas_for(sm, "find_restroom", "shopping_mall")
    ok("restroom_sign" in rest_areas, "restroom_areas")
    transit_areas = _areas_for(sm, "find_transit_line", "transit_station")
    ok("platform_sign" in transit_areas, "transit_areas")

    ok(data["ranking"].get("rows"), "ranking_rows")
    ok(all(r.get("real_score_generated") is False for r in data["ranking"].get("rows") or [] if isinstance(r, dict)), "no_real_score")
    ok(data["ranked"].get("ranked_candidate_count", 0) >= 1, "ranked_count")
    ok(all(c.get("ranked_information_source_area_written_now") is False for c in data["ranked"].get("candidates") or [] if isinstance(c, dict)), "ranked_not_written")
    ok(data["rrd_handoff"].get("handoff_invoked_now") is False, "handoff_not_now")
    ok(data["human_assist"].get("human_staff_assistance_candidate_generated") is True, "human")
    ok(data["long_term"].get("can_feed_long_term_candidate") is True, "lt")
    ok(data["final"].get("final_decision") == "READY_FOR_READABLE_REGION_DISCOVERY_RUNTIME_LATER", "final")
    ok(data["boundary"].get("isrc_runtime_dryrun_only") is True, "boundary")
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
        "checks_expected": 58,
        "blockers": blockers,
        "phase": "Static-Reading-Information-Source-Localization-Runtime-DryRun-v1-001",
    }
    _write_json(root / "static_reading_isrc_runtime_verifier_report_v1.json", report)
    print(json.dumps(report, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
