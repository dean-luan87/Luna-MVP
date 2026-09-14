#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for MidPlatform Task State Runtime DryRun v1."""

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
        "summary": "midplatform_task_state_runtime_dryrun_v1_summary.json",
        "intake": "midplatform_task_state_runtime_input_intake_matrix_v1.json",
        "handoff_intake": "midplatform_task_state_handoff_intake_matrix_v1.json",
        "state_schema": "midplatform_task_state_candidate_schema_v1.json",
        "guard_matrix": "midplatform_task_state_transition_guard_matrix_v1.json",
        "state_collection": "midplatform_task_state_candidate_collection_v1.json",
        "lifecycle_collection": "midplatform_task_lifecycle_candidate_collection_v1.json",
        "guidance_collection": "midplatform_task_guidance_need_candidate_collection_v1.json",
        "observation_collection": "midplatform_task_observation_requirement_candidate_collection_v1.json",
        "speech_collection": "midplatform_task_speech_response_candidate_collection_v1.json",
        "confirmation_collection": "midplatform_task_confirmation_context_candidate_collection_v1.json",
        "safety_dryrun": "midplatform_task_state_safety_gate_dryrun_v1.json",
        "blocking_matrix": "midplatform_task_blocking_reason_matrix_v1.json",
        "boundary_check": "midplatform_task_state_boundary_check_v1.json",
        "nav_link_check": "midplatform_task_state_navigation_guidance_link_check_v1.json",
        "dialogue_feedback_check": "midplatform_task_state_dialogue_feedback_link_check_v1.json",
        "trace": "midplatform_task_state_runtime_decision_trace_v1.json",
        "final": "midplatform_task_state_runtime_final_decision_v1.json",
        "boundary": "midplatform_task_state_runtime_boundary_report_v1.json",
        "metrics": "midplatform_task_state_runtime_metrics_candidate_report_v1.json",
        "benchmark_link": "midplatform_task_state_runtime_benchmark_link_report_v1.json",
        "health_report": "midplatform_task_state_runtime_system_health_report_v1.json",
        "no_write": "midplatform_task_state_runtime_no_write_boundary_report_v1.json",
        "sim_report": "midplatform_task_state_runtime_simulation_context_report_v1.json",
        "non_claims": "midplatform_task_state_runtime_non_claims_report_v1.json",
        "followups": "midplatform_task_state_runtime_open_followups_v1.json",
        "audit": "midplatform_task_state_runtime_audit_report_v1.json",
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
            root / "midplatform_task_state_runtime_verifier_report_v1.json",
            {"verdict": "NO_GO", "blockers": blockers},
        )
        print(json.dumps({"verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    s = data["summary"]
    ok(s.get("dryrun_scope") == "midplatform_task_state_runtime_dryrun_only", "scope")
    ok(s.get("based_on_voice_dialogue_runtime") is True, "voice_rt")
    ok(s.get("handoff_candidate_count_observed") == 12, "handoff_12")
    ok(s.get("command_candidate_count_observed") == 12, "cmd_12")
    ok(s.get("task_manager_invoked") is False, "no_tm")
    ok(s.get("task_state_changed_now") is False, "no_change")
    ok(s.get("navigation_action_triggered") is False, "no_nav")

    hi = data["handoff_intake"]
    rows = hi.get("rows") or []
    ok(len(rows) == 12, "handoff_rows_12")
    ok(sum(1 for r in rows if r.get("accepted_for_task_state_dryrun")) == 12, "handoff_accepted_12")

    schema_types = data["state_schema"].get("task_state_types") or []
    ok("TASK_CANCEL_PENDING_CONFIRMATION" in schema_types, "cancel_pending_schema")

    gm = data["guard_matrix"]
    ok(gm.get("rules", {}).get("cancel_requires_confirmation") is True, "cancel_confirm_rule")
    ok(gm.get("task_manager_commit_required") is True, "tm_commit")

    states = data["state_collection"].get("candidates") or []
    ok(len(states) == 12, "state_count_12")
    ok(all(c.get("task_state_changed_now") is False for c in states), "state_not_changed")
    proposed = {c.get("proposed_task_state") for c in states}
    ok("TASK_CANCEL_PENDING_CONFIRMATION" in proposed, "cancel_pending_state")

    lifecycles = data["lifecycle_collection"].get("candidates") or []
    ok(len(lifecycles) > 0, "lifecycle_count")
    ok(all(lc.get("lifecycle_committed_now") is False for lc in lifecycles), "lc_not_committed")

    guidance = data["guidance_collection"].get("candidates") or []
    ok(all(g.get("requires_speech_gate") is True for g in guidance), "guidance_gate")

    obs = data["observation_collection"].get("candidates") or []
    ok(all(o.get("camera_invoked_now") is False for o in obs), "no_camera")
    ok(all(o.get("ocr_invoked_now") is False for o in obs), "no_ocr")

    speech = data["speech_collection"].get("candidates") or []
    ok(all(sp.get("tts_invoked_now") is False for sp in speech), "no_tts")

    confirm = data["confirmation_collection"].get("candidates") or []
    ok(all(c.get("memory_scope") == "short_term_only" for c in confirm), "stm_scope")

    scenarios = data["safety_dryrun"].get("scenarios") or []
    inactive = next((x for x in scenarios if x.get("safety_active") is False), None)
    active = next((x for x in scenarios if x.get("safety_active") is True), None)
    ok(inactive and inactive.get("normal_transition_candidate_allowed") is True, "safety_false")
    ok(active and active.get("low_priority_transition_delayed") is True, "safety_true_delay")

    blk = data["blocking_matrix"]
    reason_ids = {r.get("blocking_reason_id") for r in blk.get("reasons") or []}
    ok("ocr_runtime_disabled" in reason_ids, "ocr_disabled")
    ok("worldmodel_runtime_deferred" in reason_ids, "wm_deferred")

    bc = data["boundary_check"]
    ok(bc.get("midplatform_cannot_commit_task_lifecycle_now") is True, "no_commit")
    ok(bc.get("task_manager_required_for_commit") is True, "tm_required")

    nav = data["nav_link_check"]
    ok(nav.get("navigation_action_triggered") is False, "nav_not_triggered")

    dfc = data["dialogue_feedback_check"]
    ok(dfc.get("speech_response_requires_speech_gate") is True, "speech_gate")

    final = data["final"]
    ok(
        final.get("final_decision")
        == "MIDPLATFORM_TASK_STATE_RUNTIME_DRYRUN_READY_FOR_TASK_MANAGER_CONTRACT",
        "final",
    )

    ok(data["boundary"].get("runtime_dryrun_only") is True, "dryrun_only")
    ok(data["metrics"].get("no_write_boundary_pass_rate") == 1.0, "nw_rate")
    ok(data["no_write"].get("boundary_ok") is True, "nw_ok")
    ok(data["sim_report"].get("simulation_profile_id") == "developer_full", "sim")
    ok(data["audit"].get("midplatform_fact_written") is False, "audit")

    verdict = "GO" if not blockers else "NO_GO"
    report = {
        "verdict": verdict,
        "checks_passed": checks,
        "checks_expected": 66,
        "blockers": blockers,
        "final_decision": final.get("final_decision"),
        "phase": "MidPlatform-Task-State-Runtime-DryRun-v1-001",
    }
    _write_json(root / "midplatform_task_state_runtime_verifier_report_v1.json", report)
    print(json.dumps(report, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
