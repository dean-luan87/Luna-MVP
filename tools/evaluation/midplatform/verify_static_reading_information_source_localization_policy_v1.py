#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for Static Reading Information Source Localization Policy v1."""

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
        "summary": "static_reading_information_source_localization_policy_v1_summary.json",
        "intake": "static_reading_information_source_input_intake_matrix_v1.json",
        "wm": "static_reading_worldmodel_first_lookup_policy_v1.json",
        "scene_fb": "static_reading_scene_recognition_fallback_policy_v1.json",
        "task": "static_reading_task_information_need_mapping_v1.json",
        "matrix": "static_reading_scene_information_source_matrix_v1.json",
        "schema": "static_reading_candidate_information_source_schema_v1.json",
        "ranking": "static_reading_candidate_source_ranking_policy_v1.json",
        "excl": "static_reading_not_worth_reading_exclusion_policy_v1.json",
        "human": "static_reading_human_staff_assistance_fallback_policy_v1.json",
        "handoff": "static_reading_readable_region_discovery_handoff_policy_v1.json",
        "current": "static_reading_information_source_current_case_dryrun_v1.json",
        "boundary": "static_reading_information_source_boundary_report_v1.json",
        "metrics": "static_reading_information_source_metrics_candidate_report_v1.json",
        "bench": "static_reading_information_source_benchmark_link_report_v1.json",
        "health": "static_reading_information_source_system_health_link_report_v1.json",
        "no_write": "static_reading_information_source_no_write_boundary_report_v1.json",
        "sim": "static_reading_information_source_simulation_context_report_v1.json",
        "non_claims": "static_reading_information_source_non_claims_report_v1.json",
        "followups": "static_reading_information_source_open_followups_v1.json",
        "audit": "static_reading_information_source_audit_report_v1.json",
    }
    data: Dict[str, Any] = {}
    for k, f in files.items():
        p = root / f
        if not p.is_file():
            blockers.append(f"missing:{k}")
        else:
            data[k] = json.loads(p.read_text(encoding="utf-8"))

    if blockers:
        _write_json(root / "static_reading_information_source_verifier_report_v1.json", {"verdict": "NO_GO", "blockers": blockers})
        print(json.dumps({"verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    s = data["summary"]
    intake = data["intake"]
    wm = data["wm"]
    scene_fb = data["scene_fb"]
    task = data["task"]
    matrix = data["matrix"]
    schema = data["schema"]
    ranking = data["ranking"]
    excl = data["excl"]
    human = data["human"]
    handoff = data["handoff"]
    current = data["current"]
    boundary = data["boundary"]
    metrics = data["metrics"]
    bench = data["bench"]
    health = data["health"]
    no_write = data["no_write"]
    sim = data["sim"]
    audit = data["audit"]

    ok(True, "summary")
    ok(s.get("policy_scope") == "information_source_localization_policy_only", "scope")
    ok(s.get("based_on_assisted_static_reading_runtime") is True, "based_asm_rt")
    ok(s.get("worldmodel_first_lookup_policy_defined") is True, "wm_def")
    ok(s.get("global_text_search_forbidden_by_default") is True, "no_global")
    ok(s.get("ocr_invoked") is False, "no_ocr")
    ok(s.get("runtime_camera_invoked") is False, "no_cam")

    wm_rows = intake.get("rows") or []
    scene_reg = next((r for r in wm_rows if r.get("intake_id") == "scene_registry"), {})
    ok(scene_reg.get("intake_status") == "optional_missing", "scene_reg_missing_ok")

    entries = wm.get("entries") or []
    sources = [e.get("lookup_source") for e in entries if isinstance(e, dict)]
    ok("unresolved_history_slot" in sources, "unresolved_slot")

    scenes = [x.get("scene_type") for x in scene_fb.get("scenes") or [] if isinstance(x, dict)]
    for st in ("street", "shopping_mall", "hospital", "transit_station", "unknown_scene"):
        ok(st in scenes, st)

    tasks = [t.get("task_type") for t in task.get("tasks") or [] if isinstance(t, dict)]
    for tt in ("restroom_search", "exit_search", "user_explicit_read_this"):
        ok(tt in tasks, tt)

    mrows = matrix.get("rows") or []
    mall = [r for r in mrows if r.get("scene_type") == "shopping_mall"]
    hosp = [r for r in mrows if r.get("scene_type") == "hospital"]
    ok(any(r.get("information_source_area") == "restroom_sign" for r in mall if isinstance(r, dict)), "mall_restroom")
    ok(any(r.get("information_source_area") == "room_doorplate" for r in hosp if isinstance(r, dict)), "hosp_door")

    ok(schema.get("ocr_readiness_unknown_by_default") is True, "ocr_unknown_default")
    dims = [d.get("ranking_dimension") for d in ranking.get("dimensions") or [] if isinstance(d, dict)]
    ok("task_relevance" in dims and "distance" in dims and "safety" in dims, "rank_dims")

    reasons = [r.get("exclusion_reason") for r in excl.get("rules") or [] if isinstance(r, dict)]
    ok("advertising_unrelated_to_task" in reasons, "excl_ad")

    atypes = [c.get("assistance_type") for c in human.get("candidates") or [] if isinstance(c, dict)]
    ok("ask_staff_for_location" in atypes, "ask_staff")

    ok(handoff.get("readable_region_discovery_invoked_now") is False, "rrd_not_now")
    ok(current.get("if_task_scene_missing_then_policy_status") == "requires_task_and_scene_context", "needs_context")
    ok(
        current.get("information_source_localization_decision") in (
            "WAIT_FOR_TASK_SCENE_CONTEXT",
            "LOCALIZE_BY_AVAILABLE_CONTEXT",
        ),
        "loc_decision",
    )
    ok(boundary.get("policy_only") is True, "boundary_policy")
    ok(metrics.get("no_write_boundary_pass_rate") == 1.0, "metrics_pass")
    ok(bench.get("benchmark_score_generated") is False, "no_bench")
    ok(health.get("recovery_action_committed") is False, "no_recovery")
    ok(no_write.get("boundary_ok") is True, "nw_ok")
    ok(no_write.get("violations") == [], "nw_violations")
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
        "checks_expected": 59,
        "blockers": blockers,
        "phase": "Static-Reading-Information-Source-Localization-Policy-v1-001",
    }
    _write_json(root / "static_reading_information_source_verifier_report_v1.json", report)
    print(json.dumps(report, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
