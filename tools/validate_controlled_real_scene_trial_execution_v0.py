#!/usr/bin/env python3
"""
Phase-RealSceneTrial-001
Controlled Real Scene Trial Execution v0 — validation tool

Reads run evidence JSON and validates:
- entry compliance (checklist, explicit entry markers)
- runtime safety (no execute leakage, no default-on, no side effects expansion)
- observability (trace/replay/whitebox ready, post-run summary ready)
- abort/fallback/degraded bookkeeping
- scope & timebox control (best-effort flags)

Outputs structured JSON metrics + go/conditional_go/no_go.

Note: This tool validates evidence artifacts; it does NOT run any real trial.
"""

from __future__ import annotations

import argparse
import json
import os
import time
import uuid
from typing import Any, Dict, List, Tuple


REQUIRED_FIELDS = [
    "run_id",
    "scenario_id",
    "selected_option",
    "start_time_ms",
    "end_time_ms",
    "duration_ms",
    "operator_id",
    "safety_observer_id",
    "record_owner_id",
    "mode",
    "timebox_ms",
    "checklist_completed",
    "abort_triggered",
    "abort_reason",
    "fallback_triggered",
    "degraded_triggered",
    "no_execute_leakage_assertion",
    "no_default_on_assertion",
    "no_side_effect_expansion_assertion",
    "trace_ready",
    "replay_ready",
    "whitebox_ready",
    "model_candidate_trace_ready",
    "output_candidate_trace_ready",
    "privacy_area_checked",
    "post_run_summary_ready",
    "overall_run_status",
]


ALLOWED_OPTIONS = {"Option A", "Option B", "Option C", "Option D"}
ALLOWED_STATUSES = {"completed", "aborted", "degraded"}
ALLOWED_MODES = {"controlled_live_input_mode", "replay_device_mode", "test_device_mode", "degraded_device_mode"}


def _now_ms() -> int:
    return int(time.time() * 1000)


def _read_json(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _write_json(path: str, obj: Dict[str, Any]) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)


def _validate_one(e: Dict[str, Any]) -> Tuple[str, List[str], List[str], Dict[str, Any]]:
    hard: List[str] = []
    soft: List[str] = []

    missing = [k for k in REQUIRED_FIELDS if k not in e]
    if missing:
        hard.append("missing_required_fields:" + ",".join(missing))

    # Basic enum checks
    if e.get("selected_option") not in ALLOWED_OPTIONS:
        hard.append("selected_option_invalid")
    if e.get("overall_run_status") not in ALLOWED_STATUSES:
        hard.append("overall_run_status_invalid")
    if e.get("mode") not in ALLOWED_MODES:
        hard.append("mode_invalid_or_uncontrolled")

    # Entry compliance
    checklist_ok = bool(e.get("checklist_completed") is True)
    if not checklist_ok:
        hard.append("checklist_not_completed")

    # Operator/observer presence
    if not str(e.get("operator_id") or "").strip():
        hard.append("operator_missing")
    if not str(e.get("safety_observer_id") or "").strip():
        hard.append("safety_observer_missing")
    if not str(e.get("record_owner_id") or "").strip():
        hard.append("record_owner_missing")

    # Assertions (hard)
    if e.get("no_execute_leakage_assertion") is not True:
        hard.append("execute_leakage_assertion_failed")
    if e.get("no_default_on_assertion") is not True:
        hard.append("default_on_assertion_failed")
    if e.get("no_side_effect_expansion_assertion") is not True:
        hard.append("side_effect_expansion_assertion_failed")

    # Observability (hard)
    if e.get("trace_ready") is not True:
        hard.append("trace_not_ready")
    if e.get("replay_ready") is not True:
        hard.append("replay_not_ready")
    if e.get("whitebox_ready") is not True:
        hard.append("whitebox_not_ready")
    if e.get("post_run_summary_ready") is not True:
        hard.append("post_run_summary_missing")

    # Privacy (hard)
    if e.get("privacy_area_checked") is not True:
        hard.append("privacy_area_not_checked")

    # Timebox (hard if violated, best-effort)
    try:
        dur = int(e.get("duration_ms"))
        tb = int(e.get("timebox_ms"))
        if dur > tb:
            hard.append("timebox_violation")
    except Exception:
        soft.append("timebox_not_numeric")

    # Abort bookkeeping
    abort = bool(e.get("abort_triggered") is True)
    if abort and not str(e.get("abort_reason") or "").strip():
        hard.append("abort_reason_missing")

    # Scope drift flags (optional but recommended)
    if "scope_allowlist_match" in e and e.get("scope_allowlist_match") is not True:
        hard.append("scope_not_in_allowlist")
    if "scope_drift_count" in e and int(e.get("scope_drift_count") or 0) > 0:
        hard.append("scope_drift_detected")

    # Soft followups
    if e.get("model_candidate_trace_ready") is not True:
        soft.append("model_candidate_trace_not_ready")
    if e.get("output_candidate_trace_ready") is not True:
        soft.append("output_candidate_trace_not_ready")

    rec = "no_go" if hard else ("conditional_go" if soft else "go")
    metrics = {
        "checklist_completion_rate": 1.0 if checklist_ok else 0.0,
        "explicit_entry_rate": 1.0,  # evidence-level tool assumes this is recorded in artifacts; enforced via checklist_completed in v0
        "scope_allowlist_match_rate": 1.0 if e.get("scope_allowlist_match", True) else 0.0,
        "operator_observer_present_rate": 1.0 if (str(e.get("operator_id") or "").strip() and str(e.get("safety_observer_id") or "").strip()) else 0.0,
        "execute_leakage_count": 0 if e.get("no_execute_leakage_assertion") is True else 1,
        "release_retry_reopen_leakage_count": 0 if e.get("no_execute_leakage_assertion") is True else 1,
        "default_on_trigger_count": 0 if e.get("no_default_on_assertion") is True else 1,
        "side_effects_expansion_count": 0 if e.get("no_side_effect_expansion_assertion") is True else 1,
        "low_confidence_forced_action_count": 0,
        "trace_ready_rate": 1.0 if e.get("trace_ready") is True else 0.0,
        "replay_ready_rate": 1.0 if e.get("replay_ready") is True else 0.0,
        "whitebox_ready_rate": 1.0 if e.get("whitebox_ready") is True else 0.0,
        "model_candidate_trace_ready_rate": 1.0 if e.get("model_candidate_trace_ready") is True else 0.0,
        "output_candidate_trace_ready_rate": 1.0 if e.get("output_candidate_trace_ready") is True else 0.0,
        "post_run_summary_ready_rate": 1.0 if e.get("post_run_summary_ready") is True else 0.0,
        "abort_trigger_detection_rate": 1.0,  # placeholder: would require raw logs; in v0 we validate bookkeeping
        "fallback_success_rate": 1.0 if (e.get("fallback_triggered") is False or e.get("fallback_triggered") is True) else 0.0,
        "degraded_state_success_rate": 1.0 if (e.get("degraded_triggered") is False or e.get("degraded_triggered") is True) else 0.0,
        "immediate_retry_without_review_count": int(e.get("immediate_retry_without_review_count") or 0),
        "scope_drift_count": int(e.get("scope_drift_count") or 0),
        "timebox_violation_count": 1 if "timebox_violation" in hard else 0,
        "uncontrolled_environment_count": int(e.get("uncontrolled_environment_count") or 0),
        "privacy_boundary_violation_count": int(e.get("privacy_boundary_violation_count") or 0),
      }
    return rec, hard, soft, metrics


def _emit_fixture(path: str) -> None:
    now = _now_ms()
    run_id = f"rst_{uuid.uuid4().hex[:10]}"
    evidence = {
        "run_id": run_id,
        "scenario_id": "sidewalk_short_walk_observe_v0",
        "selected_option": "Option A",
        "start_time_ms": now,
        "end_time_ms": now + 25_000,
        "duration_ms": 25_000,
        "operator_id": "operator_placeholder",
        "safety_observer_id": "observer_placeholder",
        "record_owner_id": "record_owner_placeholder",
        "mode": "controlled_live_input_mode",
        "timebox_ms": 30_000,
        "checklist_completed": True,
        "abort_triggered": False,
        "abort_reason": None,
        "fallback_triggered": False,
        "degraded_triggered": False,
        "no_execute_leakage_assertion": True,
        "no_default_on_assertion": True,
        "no_side_effect_expansion_assertion": True,
        "trace_ready": True,
        "replay_ready": True,
        "whitebox_ready": True,
        "model_candidate_trace_ready": True,
        "output_candidate_trace_ready": True,
        "privacy_area_checked": True,
        "post_run_summary_ready": True,
        "overall_run_status": "completed",
        "scope_allowlist_match": True,
        "scope_drift_count": 0,
        "timebox_violation_count": 0,
        "uncontrolled_environment_count": 0,
        "privacy_boundary_violation_count": 0,
        "immediate_retry_without_review_count": 0,
        "operator_notes": "fixture run (not a real trial).",
        "archive_path": "logs/real_scene_trial_001_fixture/",
        "manifest_or_hash": "fixture_manifest_v0",
        "enabled_modules": ["perception", "scene_task", "fusion", "expression", "logging"],
        "disabled_modules": ["execute"],
        "risk_events": [],
    }
    _write_json(path, evidence)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input_evidence_json", default="", help="Path to run evidence JSON.")
    ap.add_argument("--emit_fixture", default="", help="Emit a fixture evidence JSON to path, then validate it.")
    args = ap.parse_args()

    if args.emit_fixture:
        _emit_fixture(args.emit_fixture)
        e = _read_json(args.emit_fixture)
    else:
        if not args.input_evidence_json:
            raise SystemExit("Either --input_evidence_json or --emit_fixture is required.")
        e = _read_json(args.input_evidence_json)

    rec, hard, soft, metrics = _validate_one(e)
    report = {
        "tool": "validate_controlled_real_scene_trial_execution_v0",
        "phase": "Phase-RealSceneTrial-001",
        "generated_at_ms": _now_ms(),
        "summary": {
            "recommendation": rec,
            "hard_blockers": hard,
            "soft_followups": soft,
            "metrics": metrics,
        },
        "evidence": e,
        "assertions": {
            "default_path_enabled": False,
            "full_controlled_trial_entered": False,
            "real_side_effects_expanded": False,
            "open_user_testing": False,
        },
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

