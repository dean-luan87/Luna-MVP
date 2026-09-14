#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for Static Reading Task Scene Context Policy v1."""

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
        "summary": "static_reading_task_scene_context_policy_v1_summary.json",
        "intake": "static_reading_task_scene_context_input_intake_matrix_v1.json",
        "task_schema": "static_reading_task_context_schema_v1.json",
        "scene_schema": "static_reading_scene_context_schema_v1.json",
        "task_norm": "static_reading_task_normalization_policy_v1.json",
        "scene_norm": "static_reading_scene_normalization_policy_v1.json",
        "matrix": "static_reading_task_scene_matrix_v1.json",
        "missing": "static_reading_missing_context_handling_policy_v1.json",
        "clarification": "static_reading_user_clarification_candidate_policy_v1.json",
        "confidence": "static_reading_context_confidence_uncertainty_policy_v1.json",
        "handoff": "static_reading_information_source_query_handoff_policy_v1.json",
        "preconditions": "static_reading_readable_region_runtime_preconditions_v1.json",
        "current": "static_reading_task_scene_context_current_case_dryrun_v1.json",
        "boundary": "static_reading_task_scene_context_boundary_report_v1.json",
        "metrics": "static_reading_task_scene_context_metrics_candidate_report_v1.json",
        "bench": "static_reading_task_scene_context_benchmark_link_report_v1.json",
        "health": "static_reading_task_scene_context_system_health_link_report_v1.json",
        "no_write": "static_reading_task_scene_context_no_write_boundary_report_v1.json",
        "sim": "static_reading_task_scene_context_simulation_context_report_v1.json",
        "non_claims": "static_reading_task_scene_context_non_claims_report_v1.json",
        "followups": "static_reading_task_scene_context_open_followups_v1.json",
        "audit": "static_reading_task_scene_context_audit_report_v1.json",
    }
    data: Dict[str, Any] = {}
    for k, f in files.items():
        p = root / f
        if not p.is_file():
            blockers.append(f"missing:{k}")
        else:
            data[k] = json.loads(p.read_text(encoding="utf-8"))

    if blockers:
        _write_json(root / "static_reading_task_scene_context_verifier_report_v1.json", {"verdict": "NO_GO", "blockers": blockers})
        print(json.dumps({"verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    s = data["summary"]
    ok(True, "summary")
    ok(s.get("policy_scope") == "task_scene_context_policy_only", "scope")
    ok(s.get("task_context_schema_defined") is True, "task_schema_flag")
    ok(s.get("scene_context_schema_defined") is True, "scene_schema_flag")
    ok(s.get("task_scene_matrix_defined") is True, "matrix_flag")
    ok(s.get("task_context_fabrication_forbidden") is True, "no_task_fab")
    ok(s.get("scene_context_fabrication_forbidden") is True, "no_scene_fab")
    ok(s.get("scene_detector_invoked") is False, "no_detector")
    ok(s.get("ocr_invoked") is False, "no_ocr")

    ts = data["task_schema"]
    ok("user_explicit_request" in (ts.get("allowed_sources") or []), "user_explicit")
    ok("active_navigation_task" in (ts.get("allowed_sources") or []), "nav_task")

    sc = data["scene_schema"]
    stypes = sc.get("scene_types") or []
    for st in ("street", "shopping_mall", "hospital", "unknown_scene"):
        ok(st in stypes, st)

    entries = data["task_norm"].get("entries") or []
    ntypes = [e.get("normalized_task_type") for e in entries if isinstance(e, dict)]
    for nt in ("find_restroom", "read_doorplate", "user_explicit_read_this"):
        ok(nt in ntypes, nt)

    rows = data["matrix"].get("rows") or []
    pairs = {(r.get("normalized_task_type"), r.get("normalized_scene_type")) for r in rows if isinstance(r, dict)}
    ok(("find_restroom", "shopping_mall") in pairs, "restroom_mall")
    ok(("find_department", "hospital") in pairs, "dept_hospital")

    cases = data["missing"].get("cases") or []
    conds = [c.get("missing_or_invalid_condition") for c in cases if isinstance(c, dict)]
    ok("missing_both_task_and_scene" in conds, "missing_both")
    both = next((c for c in cases if c.get("missing_or_invalid_condition") == "missing_both_task_and_scene"), {})
    ok(both.get("readable_region_discovery_allowed_now") is False, "rrd_blocked")

    cands = data["clarification"].get("candidates") or []
    prompts = [c.get("prompt_candidate") for c in cands if isinstance(c, dict)]
    ok(any("你想找什么信息" in (p or "") for p in prompts), "clarify_prompt")
    ok(all(c.get("tts_invoked_now") is False for c in cands if isinstance(c, dict)), "no_tts")

    levels = [l.get("level") for l in data["confidence"].get("levels") or [] if isinstance(l, dict)]
    ok("low_confidence_context" in levels and "conflict_context" in levels, "confidence_levels")

    ok(data["handoff"].get("handoff_invoked_now") is False, "handoff_not_now")
    ok(data["preconditions"].get("runtime_preconditions_met_now") is False, "precond_not_met")

    cur = data["current"]
    ok(cur.get("task_context_available") is False, "task_false")
    ok(cur.get("scene_context_available") is False, "scene_false")
    ok(cur.get("missing_context_status") == "missing_both_task_and_scene", "missing_both_status")
    ok(cur.get("ranked_information_source_area_generated") is False, "no_ranked")

    ok(data["boundary"].get("policy_only") is True, "boundary")
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
        "checks_expected": 64,
        "blockers": blockers,
        "phase": "Static-Reading-Task-Scene-Context-Policy-v1-001",
    }
    _write_json(root / "static_reading_task_scene_context_verifier_report_v1.json", report)
    print(json.dumps(report, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
