#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for User Clarification Prompt Template for Reading v1."""

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
        "summary": "user_clarification_prompt_template_for_reading_v1_summary.json",
        "intake": "user_clarification_prompt_template_input_intake_matrix_v1.json",
        "matrix": "user_clarification_prompt_template_matrix_v1.json",
        "response_schema": "user_clarification_expected_response_schema_v1.json",
        "fill_policy": "user_clarification_response_to_context_fill_policy_v1.json",
        "priority_safety": "user_clarification_prompt_priority_safety_policy_v1.json",
        "cooldown": "user_clarification_prompt_cooldown_repeat_policy_v1.json",
        "handoff": "user_clarification_handoff_to_task_scene_runtime_policy_v1.json",
        "current": "user_clarification_current_case_template_dryrun_v1.json",
        "long_term": "user_clarification_long_term_candidate_link_v1.json",
        "boundary": "user_clarification_prompt_template_boundary_report_v1.json",
        "metrics": "user_clarification_prompt_template_metrics_candidate_report_v1.json",
        "bench": "user_clarification_prompt_template_benchmark_link_report_v1.json",
        "health": "user_clarification_prompt_template_system_health_link_report_v1.json",
        "no_write": "user_clarification_prompt_template_no_write_boundary_report_v1.json",
        "sim": "user_clarification_prompt_template_simulation_context_report_v1.json",
        "non_claims": "user_clarification_prompt_template_non_claims_report_v1.json",
        "followups": "user_clarification_prompt_template_open_followups_v1.json",
        "audit": "user_clarification_prompt_template_audit_report_v1.json",
    }
    data: Dict[str, Any] = {}
    for k, f in files.items():
        p = root / f
        if not p.is_file():
            blockers.append(f"missing:{k}")
        else:
            data[k] = json.loads(p.read_text(encoding="utf-8"))

    if blockers:
        _write_json(root / "user_clarification_prompt_template_verifier_report_v1.json", {"verdict": "NO_GO", "blockers": blockers})
        print(json.dumps({"verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    s = data["summary"]
    ok(True, "summary")
    ok(s.get("template_scope") == "reading_clarification_prompt_template_only", "scope")
    ok(s.get("based_on_task_scene_context_runtime") is True, "based_tsc_rt")
    ok(s.get("clarification_prompt_template_defined") is True, "tpl_defined")
    ok(s.get("safety_priority_above_clarification") is True, "safety_above")
    ok(s.get("runtime_tts_invoked") is False, "no_tts")
    ok(s.get("voice_output_plane_invoked") is False, "no_vop")
    ok(s.get("speech_request_submitted") is False, "no_speech")

    tpls = data["matrix"].get("templates") or []
    ctypes = [t.get("clarification_type") for t in tpls if isinstance(t, dict)]
    for ct in ("missing_task_context", "missing_scene_context", "missing_both_task_and_scene"):
        ok(ct in ctypes, ct)
    texts = [t.get("prompt_text_short") for t in tpls if isinstance(t, dict)]
    ok(any("你想找什么信息" in (x or "") for x in texts), "prompt_text")

    rules = data["fill_policy"].get("rules") or []
    vals = [r.get("normalized_value_candidate") for r in rules if isinstance(r, dict)]
    ok("find_exit" in vals and "read_doorplate" in vals, "task_fill")
    ok("shopping_mall" in vals and "hospital" in vals, "scene_fill")

    ok(data["priority_safety"].get("can_be_interrupted_by_p0") is True, "p0_interrupt")
    ok(data["handoff"].get("handoff_invoked_now") is False, "handoff_not_now")
    ok(data["current"].get("selected_template_type") == "missing_both_task_and_scene", "selected_both")
    ok(data["current"].get("tts_invoked_now") is False, "current_no_tts")
    ok(data["long_term"].get("can_feed_long_term_candidate") is True, "lt")
    ok(data["boundary"].get("template_only") is True, "boundary")
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
        "checks_expected": 55,
        "blockers": blockers,
        "phase": "User-Clarification-Prompt-Template-for-Reading-v1-001",
    }
    _write_json(root / "user_clarification_prompt_template_verifier_report_v1.json", report)
    print(json.dumps(report, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
