#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for User Clarification Response Parsing DryRun for Reading v1."""

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
        "summary": "user_clarification_response_parsing_dryrun_for_reading_v1_summary.json",
        "intake": "user_clarification_response_parsing_input_intake_matrix_v1.json",
        "simulated_set": "user_clarification_simulated_response_set_v1.json",
        "matrix": "user_clarification_response_parsing_matrix_v1.json",
        "task_candidates": "user_clarification_task_context_candidate_collection_v1.json",
        "scene_candidates": "user_clarification_scene_context_candidate_collection_v1.json",
        "human_assist": "user_clarification_response_human_staff_assistance_candidate_v1.json",
        "confidence_eval": "user_clarification_response_confidence_uncertainty_evaluation_v1.json",
        "handoff": "user_clarification_response_to_tsc_handoff_candidate_v1.json",
        "reentry": "user_clarification_response_tsc_reentry_preconditions_v1.json",
        "long_term": "user_clarification_response_long_term_candidate_link_v1.json",
        "trace": "user_clarification_response_parsing_decision_trace_v1.json",
        "final": "user_clarification_response_parsing_final_decision_v1.json",
        "boundary": "user_clarification_response_parsing_boundary_report_v1.json",
        "metrics": "user_clarification_response_parsing_metrics_candidate_report_v1.json",
        "bench": "user_clarification_response_parsing_benchmark_link_report_v1.json",
        "health": "user_clarification_response_parsing_system_health_link_report_v1.json",
        "no_write": "user_clarification_response_parsing_no_write_boundary_report_v1.json",
        "sim": "user_clarification_response_parsing_simulation_context_report_v1.json",
        "non_claims": "user_clarification_response_parsing_non_claims_report_v1.json",
        "followups": "user_clarification_response_parsing_open_followups_v1.json",
        "audit": "user_clarification_response_parsing_audit_report_v1.json",
    }
    data: Dict[str, Any] = {}
    for k, f in files.items():
        p = root / f
        if not p.is_file():
            blockers.append(f"missing:{k}")
        else:
            data[k] = json.loads(p.read_text(encoding="utf-8"))

    if blockers:
        _write_json(root / "user_clarification_response_parsing_verifier_report_v1.json", {"verdict": "NO_GO", "blockers": blockers})
        print(json.dumps({"verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    s = data["summary"]
    ok(True, "summary")
    ok(s.get("dryrun_scope") == "reading_clarification_response_parsing_dryrun_only", "scope")
    ok(s.get("based_on_clarification_prompt_runtime") is True, "based_rt")
    ok(s.get("simulated_response_set_defined") is True, "sim_set")
    ok(s.get("task_context_candidate_generated") is True, "task_cand")
    ok(s.get("scene_context_candidate_generated") is True, "scene_cand")
    ok(s.get("handoff_to_tsc_runtime_candidate_generated") is True, "handoff")
    ok(s.get("tsc_runtime_reentry_allowed_later") is True, "reentry_later")
    ok(s.get("tsc_runtime_reentry_invoked_now") is False, "reentry_not_now")
    ok(s.get("asr_invoked") is False, "no_asr")
    ok(s.get("llm_invoked") is False, "no_llm")
    ok(s.get("information_source_runtime_invoked_now") is False, "no_isrc")
    ok(s.get("readable_region_runtime_invoked_now") is False, "no_rrd")

    sim = data["simulated_set"].get("responses") or []
    ok(any("找出口，商场" in (r.get("raw_user_response") or "") for r in sim if isinstance(r, dict)), "sim_exit_mall")

    m = data["matrix"]
    r1 = _find_row(m, "找出口，商场")
    ok(r1.get("possible_task_type") == "find_exit" and r1.get("possible_scene_type") == "shopping_mall", "exit_mall_parse")
    ok(r1.get("fills_both") is True, "fills_both")

    r2 = _find_row(m, "门牌")
    ok(r2.get("possible_task_type") == "read_doorplate", "doorplate")

    r3 = _find_row(m, "医院里找科室")
    ok(r3.get("possible_task_type") == "find_department" and r3.get("possible_scene_type") == "hospital", "hospital_dept")

    r4 = _find_row(m, "读这段字")
    ok(r4.get("possible_task_type") == "user_explicit_read_this", "explicit_read")

    r7 = _find_row(m, "洗手间")
    ok(r7.get("possible_task_type") == "find_restroom" and r7.get("possible_scene_type") == "shopping_mall", "restroom_mall")

    r8 = _find_row(m, "几号线")
    ok(r8.get("possible_task_type") == "find_transit_line" and r8.get("possible_scene_type") == "transit_station", "transit")

    ok(all(c.get("task_context_written_now") is False for c in data["task_candidates"].get("candidates") or [] if isinstance(c, dict)), "task_not_written")
    ok(all(c.get("scene_context_written_now") is False for c in data["scene_candidates"].get("candidates") or [] if isinstance(c, dict)), "scene_not_written")

    ok(data["human_assist"].get("human_staff_assistance_candidate_generated") is True, "human")
    ok(data["confidence_eval"].get("requires_confirmation_count", 0) >= 1, "req_conf_count")
    ok(data["handoff"].get("handoff_invoked_now") is False, "handoff_not_now")
    ok(data["reentry"].get("information_source_runtime_invoked_now") is False, "isrc_blocked")
    ok(data["reentry"].get("readable_region_runtime_invoked_now") is False, "rrd_blocked")
    ok(data["long_term"].get("can_feed_long_term_candidate") is True, "lt")
    ok(data["final"].get("final_decision") == "READY_FOR_TSC_REEVALUATION_LATER", "final_decision")
    ok(data["boundary"].get("parsing_dryrun_only") is True, "boundary")
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
        "checks_expected": 62,
        "blockers": blockers,
        "phase": "User-Clarification-Response-Parsing-DryRun-for-Reading-v1-001",
    }
    _write_json(root / "user_clarification_response_parsing_verifier_report_v1.json", report)
    print(json.dumps(report, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
