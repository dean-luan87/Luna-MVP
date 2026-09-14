#!/usr/bin/env python3
"""
Phase-Device-001
On-Device Closed-Loop Validation v0 — validation tool

This tool validates exported device logs (JSONL) or replay fixtures (JSONL) for:
- closed-loop chain completeness (required stages appear)
- candidate-only integrity (no execute/release/retry/reopen semantics)
- no default-on / no uncontrolled live
- trace/replay/whitebox minimum fields
- degraded/fallback evidence
- minimal latency/resource observation record readiness

Output: structured JSON report with metrics + go/conditional_go/no_go.
"""

from __future__ import annotations

import argparse
import json
import os
import statistics
import time
import uuid
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional, Set, Tuple


FORBIDDEN_TOKENS = (
    "execute",
    "release",
    "retry",
    "reopen",
    "open_release_window",
    "enable_default_path",
    "override_governance",
    "grant_control",
)


REQUIRED_STAGES = [
    "input_event",
    "perception_signal",
    "scene_state",
    "task_state",
    "fusion_decision_candidate",
    "navigation_output_candidate",
    "output_suppression_or_emit_candidate",
    "whitebox_trace",
    "replay_record",
    "fallback_or_degraded_state",
]


ALLOWED_MODES = {
    "replay_device_mode",
    "test_device_mode",
    "controlled_live_input_mode",
    "degraded_device_mode",
}


def _now_ms() -> int:
    return int(time.time() * 1000)


def _contains_forbidden_semantics(obj: Any) -> bool:
    # Recursively scan string values for forbidden tokens.
    if obj is None:
        return False
    if isinstance(obj, str):
        s = obj.lower()
        return any(t in s for t in FORBIDDEN_TOKENS)
    if isinstance(obj, (int, float, bool)):
        return False
    if isinstance(obj, list):
        return any(_contains_forbidden_semantics(x) for x in obj)
    if isinstance(obj, dict):
        return any(_contains_forbidden_semantics(v) for v in obj.values())
    return False


def _read_jsonl(path: str) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            out.append(json.loads(line))
    return out


def _safe_get(d: Dict[str, Any], key: str, default: Any = None) -> Any:
    return d.get(key, default)


def _is_mode_entry_event(e: Dict[str, Any]) -> bool:
    return e.get("event_type") == "mode_entry_event"


def _is_stage_event(e: Dict[str, Any]) -> bool:
    return e.get("event_type") == "stage_event"


def _event_run_id(e: Dict[str, Any]) -> Optional[str]:
    rid = e.get("run_id")
    return str(rid) if rid is not None else None


def _event_stage(e: Dict[str, Any]) -> Optional[str]:
    return e.get("source_stage") or e.get("stage")  # tolerate older keys


def _event_mode(e: Dict[str, Any]) -> Optional[str]:
    m = e.get("mode")
    return str(m) if m is not None else None


def _event_ts(e: Dict[str, Any]) -> Optional[int]:
    ts = e.get("timestamp_ms")
    if ts is None:
        return None
    try:
        return int(ts)
    except Exception:
        return None


def _event_frame_id(e: Dict[str, Any]) -> Optional[str]:
    fid = e.get("frame_or_event_id")
    return str(fid) if fid is not None else None


def _has_reason_codes(e: Dict[str, Any]) -> bool:
    rc = e.get("reason_codes")
    return isinstance(rc, list) and len(rc) > 0


def _is_default_on(e: Dict[str, Any]) -> bool:
    # Accept either default_on at top-level, or inside payload.
    if e.get("default_on") is True:
        return True
    p = e.get("payload") or {}
    if isinstance(p, dict) and p.get("default_on") is True:
        return True
    return False


def _extract_latency_ms(e: Dict[str, Any]) -> Optional[float]:
    p = e.get("payload") or {}
    if not isinstance(p, dict):
        return None
    v = p.get("end_to_end_latency_ms")
    if v is None:
        return None
    try:
        return float(v)
    except Exception:
        return None


def _extract_resource_ok(e: Dict[str, Any]) -> bool:
    p = e.get("payload") or {}
    if not isinstance(p, dict):
        return False
    # v0: accept presence of either cpu_pct or mem_mb
    return (p.get("cpu_pct") is not None) or (p.get("mem_mb") is not None)


@dataclass
class ValidationSummary:
    recommendation: str
    hard_blockers: List[str]
    soft_followups: List[str]
    metrics: Dict[str, Any]


def validate_events(events: List[Dict[str, Any]]) -> Tuple[ValidationSummary, Dict[str, Any]]:
    hard_blockers: List[str] = []
    soft_followups: List[str] = []

    # Basic parsing & grouping
    run_ids: Set[str] = set()
    modes_seen: Set[str] = set()
    mode_entry_by_run: Dict[str, List[Dict[str, Any]]] = {}
    stage_seen_by_run: Dict[str, Set[str]] = {}
    stage_events_by_run: Dict[str, List[Dict[str, Any]]] = {}

    reason_codes_present = 0
    total_events = len(events)

    execute_leakage_count = 0
    release_retry_reopen_leakage_count = 0
    default_on_trigger_count = 0
    low_confidence_forced_action_count = 0
    device_error_count = 0

    degraded_trigger_count = 0
    fallback_success_count = 0
    model_disabled_baseline_success_count = 0
    perception_failure_safe_degrade_count = 0

    latency_values: List[float] = []
    cpu_mem_records = 0

    # required field readiness
    trace_ready = 0
    replay_ready = 0
    whitebox_ready = 0

    missing_required_fields_count = 0

    for e in events:
        rid = _event_run_id(e)
        if rid:
            run_ids.add(rid)
        else:
            missing_required_fields_count += 1
            continue

        mode = _event_mode(e)
        if not mode or mode not in ALLOWED_MODES:
            missing_required_fields_count += 1
        else:
            modes_seen.add(mode)

        ts = _event_ts(e)
        fid = _event_frame_id(e)
        if ts is None or fid is None:
            missing_required_fields_count += 1

        if _has_reason_codes(e):
            reason_codes_present += 1

        # Forbidden semantics scanning across event content
        if _contains_forbidden_semantics(e):
            execute_leakage_count += 1
            # classify release/retry/reopen subset (best-effort)
            s = json.dumps(e, ensure_ascii=False).lower()
            if any(t in s for t in ("release", "retry", "reopen")):
                release_retry_reopen_leakage_count += 1

        if _is_default_on(e):
            default_on_trigger_count += 1

        # Group by run & stages
        if _is_mode_entry_event(e):
            mode_entry_by_run.setdefault(rid, []).append(e)
        if _is_stage_event(e):
            st = _event_stage(e)
            if st:
                stage_seen_by_run.setdefault(rid, set()).add(st)
                stage_events_by_run.setdefault(rid, []).append(e)

                # Observability per stage
                if st == "whitebox_trace":
                    p = e.get("payload") or {}
                    if isinstance(p, dict) and p.get("whitebox_trace_id") and isinstance(p.get("errors", []), list):
                        whitebox_ready += 1
                if st == "replay_record":
                    p = e.get("payload") or {}
                    if isinstance(p, dict) and p.get("replay_record_id") and p.get("replay_index") is not None:
                        replay_ready += 1
                if st == "whitebox_trace":
                    trace_ready += 1  # v0: trace event itself counts as ready

                # Degraded/fallback evidence
                if st == "fallback_or_degraded_state":
                    p = e.get("payload") or {}
                    if isinstance(p, dict):
                        if p.get("degraded") is True:
                            degraded_trigger_count += 1
                        if p.get("fallback_success") is True:
                            fallback_success_count += 1
                        if p.get("model_disabled_baseline_success") is True:
                            model_disabled_baseline_success_count += 1
                        if p.get("perception_failure_safe_degrade") is True:
                            perception_failure_safe_degrade_count += 1

                # Low-confidence forced action guard (best-effort)
                if st == "navigation_output_candidate":
                    # If output is a navigation instruction while confidence is low and no uncertainty markers, count as forced action.
                    p = e.get("payload") or {}
                    if isinstance(p, dict):
                        conf = p.get("confidence")
                        txt = str(p.get("message_text_candidate") or "")
                        otype = p.get("output_type")
                        if conf is not None:
                            try:
                                conf_f = float(conf)
                            except Exception:
                                conf_f = None
                            if conf_f is not None and conf_f < 0.55 and otype == "navigation_instruction_candidate":
                                if all(k not in txt for k in ("不确定", "可能", "建议", "先观察")):
                                    low_confidence_forced_action_count += 1

                # Latency/resource observations
                lat = _extract_latency_ms(e)
                if lat is not None:
                    latency_values.append(lat)
                if _extract_resource_ok(e):
                    cpu_mem_records += 1

                # device errors
                p = e.get("payload") or {}
                if isinstance(p, dict) and p.get("device_error") is True:
                    device_error_count += 1

    # Evaluate per-run closed loop completeness
    runs_total = len(run_ids)
    runs_closed_ok = 0
    stage_chain_completeness_sum = 0.0
    missing_stage_count = 0
    candidate_only_ok_count = 0

    for rid in run_ids:
        stages = stage_seen_by_run.get(rid, set())
        present = sum(1 for s in REQUIRED_STAGES if s in stages)
        stage_chain_completeness_sum += present / len(REQUIRED_STAGES)
        missing = [s for s in REQUIRED_STAGES if s not in stages]
        missing_stage_count += len(missing)
        if len(missing) == 0:
            runs_closed_ok += 1

        # candidate-only integrity: if no forbidden semantics and no default-on in that run
        # (best effort: global counts already capture, but we approximate per-run by scanning those events)
        run_events = stage_events_by_run.get(rid, [])
        if not any(_contains_forbidden_semantics(ev) for ev in run_events) and not any(_is_default_on(ev) for ev in run_events):
            candidate_only_ok_count += 1

    closed_loop_success_rate = (runs_closed_ok / runs_total) if runs_total else 0.0
    stage_chain_completeness_rate = (stage_chain_completeness_sum / runs_total) if runs_total else 0.0
    candidate_only_integrity_rate = (candidate_only_ok_count / runs_total) if runs_total else 0.0

    reason_codes_present_rate = (reason_codes_present / total_events) if total_events else 0.0
    device_trace_ready_rate = (trace_ready / max(1, total_events)) if total_events else 0.0
    device_replay_ready_rate = (replay_ready / max(1, total_events)) if total_events else 0.0
    whitebox_record_ready_rate = (whitebox_ready / max(1, total_events)) if total_events else 0.0

    latency_record_ready_rate = 1.0 if len(latency_values) > 0 else 0.0
    cpu_memory_record_ready_rate = 1.0 if cpu_mem_records > 0 else 0.0
    avg_latency = float(statistics.mean(latency_values)) if latency_values else None
    max_latency = float(max(latency_values)) if latency_values else None

    degraded_mode_trigger_rate = (degraded_trigger_count / max(1, runs_total)) if runs_total else 0.0
    fallback_success_rate = (fallback_success_count / max(1, runs_total)) if runs_total else 0.0
    model_disabled_baseline_success_rate = (model_disabled_baseline_success_count / max(1, runs_total)) if runs_total else 0.0
    perception_failure_safe_degrade_rate = (perception_failure_safe_degrade_count / max(1, runs_total)) if runs_total else 0.0

    # Hard blockers (NO_GO)
    if execute_leakage_count > 0:
        hard_blockers.append("execute_leakage_detected")
    if release_retry_reopen_leakage_count > 0:
        hard_blockers.append("release_retry_reopen_leakage_detected")
    if default_on_trigger_count > 0:
        hard_blockers.append("default_on_triggered")
    if low_confidence_forced_action_count > 0:
        hard_blockers.append("low_confidence_forced_action")
    if stage_chain_completeness_rate < 1.0:
        hard_blockers.append("stage_chain_incomplete")
    if device_replay_ready_rate == 0.0:
        hard_blockers.append("replay_missing")
    if whitebox_record_ready_rate == 0.0:
        hard_blockers.append("whitebox_missing")
    if missing_required_fields_count > 0:
        hard_blockers.append("missing_required_fields")

    # Soft followups (allowed under conditional_go)
    if latency_record_ready_rate == 0.0:
        soft_followups.append("latency_not_recorded")
    if cpu_memory_record_ready_rate == 0.0:
        soft_followups.append("cpu_memory_not_recorded")
    if device_error_count > 0:
        soft_followups.append("device_errors_observed")

    if hard_blockers:
        rec = "no_go"
    else:
        # conditional if only observation gaps exist
        rec = "go" if not soft_followups else "conditional_go"

    metrics = {
        "closed_loop_success_rate": closed_loop_success_rate,
        "stage_chain_completeness_rate": stage_chain_completeness_rate,
        "missing_stage_count": missing_stage_count,
        "candidate_only_integrity_rate": candidate_only_integrity_rate,
        "execute_leakage_count": execute_leakage_count,
        "release_retry_reopen_leakage_count": release_retry_reopen_leakage_count,
        "default_on_trigger_count": default_on_trigger_count,
        "low_confidence_forced_action_count": low_confidence_forced_action_count,
        "device_trace_ready_rate": device_trace_ready_rate,
        "device_replay_ready_rate": device_replay_ready_rate,
        "whitebox_record_ready_rate": whitebox_record_ready_rate,
        "reason_codes_present_rate": reason_codes_present_rate,
        "degraded_mode_trigger_rate": degraded_mode_trigger_rate,
        "fallback_success_rate": fallback_success_rate,
        "model_disabled_baseline_success_rate": model_disabled_baseline_success_rate,
        "perception_failure_safe_degrade_rate": perception_failure_safe_degrade_rate,
        "average_end_to_end_latency_ms": avg_latency,
        "max_end_to_end_latency_ms": max_latency,
        "latency_record_ready_rate": latency_record_ready_rate,
        "cpu_memory_record_ready_rate": cpu_memory_record_ready_rate,
        "device_error_count": device_error_count,
        "runs_total": runs_total,
        "modes_seen": sorted(list(modes_seen)),
    }

    summary = ValidationSummary(
        recommendation=rec,
        hard_blockers=hard_blockers,
        soft_followups=soft_followups,
        metrics=metrics,
    )
    report = {
        "tool": "validate_on_device_closed_loop_v0",
        "phase": "Phase-Device-001",
        "generated_at_ms": _now_ms(),
        "summary": {
            "recommendation": rec,
            "hard_blockers": hard_blockers,
            "soft_followups": soft_followups,
            "metrics": metrics,
        },
    }
    return summary, report


def _emit_fixture(path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    run_id = f"run_{uuid.uuid4().hex[:10]}"
    t0 = _now_ms()

    def w(obj: Dict[str, Any]) -> None:
        with open(path, "a", encoding="utf-8") as f:
            f.write(json.dumps(obj, ensure_ascii=False) + "\n")

    # mode entry
    w(
        {
            "event_type": "mode_entry_event",
            "run_id": run_id,
            "timestamp_ms": t0,
            "frame_or_event_id": "mode_entry_0",
            "mode": "replay_device_mode",
            "explicit_entry": True,
            "operator_intent": "manual_test",
            "default_on": False,
            "no_execute_leakage": True,
            "reason_codes": ["fixture_entry"],
            "payload": {},
        }
    )

    # stage chain (single frame)
    frame_id = "frame_0001"
    stages_payload = {
        "input_event": {"replay_source": "fixture", "replay_index": 1, "payload_ref": "fixture://frame/1", "end_to_end_latency_ms": 35.0, "cpu_pct": 12.0, "mem_mb": 180.0},
        "perception_signal": {"confidence": 0.8, "reason_codes": ["perception_ok"]},
        "scene_state": {"confidence": 0.8, "reason_codes": ["scene_sidewalk"]},
        "task_state": {"confidence": 0.8, "reason_codes": ["task_follow_path"]},
        "fusion_decision_candidate": {"confidence": 0.8, "reason_codes": ["fusion_ok"], "allows_execute_now": False},
        "navigation_output_candidate": {
            "output_type": "navigation_instruction_candidate",
            "message_text_candidate": "向前走约五米，然后左转。",
            "confidence": 0.85,
            "reason_codes": ["nav_step"],
            "allows_execute_now": False,
        },
        "output_suppression_or_emit_candidate": {"emitted": True, "suppression_reason": None, "reason_codes": ["emit_ok"]},
        "whitebox_trace": {"whitebox_trace_id": f"wb_{uuid.uuid4().hex[:8]}", "errors": [], "fallback_events": [], "stage_timings_ms": {"perception": 8, "fusion": 5, "expression": 3}},
        "replay_record": {"replay_record_id": f"rp_{uuid.uuid4().hex[:8]}", "replay_source": "fixture", "replay_index": 1, "payload_ref": "fixture://frame/1"},
        "fallback_or_degraded_state": {"degraded": False, "fallback_success": True, "model_disabled_baseline_success": False, "perception_failure_safe_degrade": False, "reason_codes": ["ok"]},
    }

    for i, st in enumerate(REQUIRED_STAGES):
        payload = stages_payload.get(st, {})
        w(
            {
                "event_type": "stage_event",
                "run_id": run_id,
                "timestamp_ms": t0 + 10 + i,
                "frame_or_event_id": frame_id,
                "mode": "replay_device_mode",
                "source_stage": st,
                "downstream_stage": "next",
                "reason_codes": (payload.get("reason_codes") if isinstance(payload, dict) and payload.get("reason_codes") else ["fixture"]),
                "confidence": (payload.get("confidence") if isinstance(payload, dict) else None),
                "no_execute_leakage": True,
                "closed_safe_or_candidate_only_status": "candidate_only",
                "payload": payload,
            }
        )


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input_jsonl", default="", help="Path to device-exported JSONL log.")
    ap.add_argument("--emit_fixture", default="", help="Emit a minimal fixture JSONL to path, then validate it.")
    args = ap.parse_args()

    if args.emit_fixture:
        # reset file
        if os.path.exists(args.emit_fixture):
            os.remove(args.emit_fixture)
        _emit_fixture(args.emit_fixture)
        events = _read_jsonl(args.emit_fixture)
    else:
        if not args.input_jsonl:
            raise SystemExit("Either --input_jsonl or --emit_fixture is required.")
        events = _read_jsonl(args.input_jsonl)

    _, report = validate_events(events)
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

