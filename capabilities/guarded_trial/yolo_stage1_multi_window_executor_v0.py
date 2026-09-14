# -*- coding: utf-8 -*-
"""
Phase-Mainline-GuardedTrial-006 — Multi-window offline YOLO slice trial (serial, gated).

Reuses Phase-005 execution core with variable max_frames; enforces strict window ordering and stop rules.
"""

from __future__ import annotations

import json
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

PHASE = "Phase-Mainline-GuardedTrial-006"

CANONICAL_WINDOWS = [50, 100, 200]


def validate_yolo_multi_window_input_v0(*, windows: Sequence[int], input_video_path: str) -> Dict[str, Any]:
    """Validate window chain is a prefix of [50,100,200]; delegate video to Phase-005 validator."""
    from capabilities.guarded_trial.yolo_stage1_10_frame_executor_v0 import (
        validate_yolo_stage1_input_video_for_execution_v0,
    )

    ws = sorted(set(int(x) for x in windows))
    out: Dict[str, Any] = {
        "valid": False,
        "windows_requested": ws,
        "reason_code": "",
        "video_validation": None,
    }
    if not ws:
        out["reason_code"] = "empty_windows"
        return out
    for i, v in enumerate(ws):
        if i >= len(CANONICAL_WINDOWS) or v != CANONICAL_WINDOWS[i]:
            out["reason_code"] = "windows_not_monotonic_prefix_of_50_100_200"
            return out
    vid = validate_yolo_stage1_input_video_for_execution_v0(input_video_path)
    out["video_validation"] = vid
    if not vid.get("valid"):
        out["reason_code"] = vid.get("reason_code") or "video_invalid"
        return out
    out["valid"] = True
    out["reason_code"] = "ok"
    return out


def load_yolo_10_frame_baseline_v0(baseline_root: Path) -> Dict[str, Any]:
    """
    Load Phase-005 10-frame dry-run summary; require GO_next_window and full 10 frames with detector.
    """
    p = baseline_root / "yolo_stage1_10_frame_dry_run_summary.json"
    out: Dict[str, Any] = {
        "ok": False,
        "baseline_root": str(baseline_root),
        "summary_path": str(p),
        "baseline_10_frame_status": "UNKNOWN",
        "summary": {},
    }
    if not p.is_file():
        out["reason"] = "missing_yolo_stage1_10_frame_dry_run_summary"
        return out
    try:
        s = json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        out["reason"] = f"summary_json_invalid:{type(e).__name__}"
        return out
    out["summary"] = s
    go = (
        s.get("post_trial_recommendation") == "GO_next_window"
        and s.get("abort_triggered") is not True
        and int(s.get("frames_processed") or 0) == 10
        and int(s.get("schema_invalid_count") or 0) == 0
        and s.get("detector_invoked") is True
    )
    out["baseline_10_frame_status"] = "GO" if go else "NO_GO"
    out["ok"] = bool(go)
    if not go:
        out["reason"] = "baseline_not_go_or_incomplete"
    return out


def baseline_video_matches_input_v0(baseline_summary: Mapping[str, Any], path_resolved: str) -> bool:
    bv = baseline_summary.get("input_video")
    try:
        return bool(bv) and Path(str(bv)).resolve() == Path(path_resolved).resolve()
    except Exception:
        return False


def build_yolo_multi_window_trial_plan_v0(*, windows: Sequence[int]) -> Dict[str, Any]:
    ws = sorted(set(int(x) for x in windows))
    return {
        "phase": PHASE,
        "canonical_chain": list(CANONICAL_WINDOWS),
        "windows_requested": ws,
        "execution_order": ws,
        "serial_only": True,
    }


def _latency_aggregate_v0(lat_ms: List[float]) -> Dict[str, Any]:
    if not lat_ms:
        return {"avg_ms": 0.0, "p50_ms": 0.0, "p95_ms": 0.0, "max_ms": 0.0}
    s = sorted(lat_ms)
    n = len(s)
    p50 = s[n // 2]
    p95 = s[int(max(0, n * 0.95 - 0.0001))]
    return {
        "avg_ms": sum(s) / n,
        "p50_ms": p50,
        "p95_ms": p95,
        "max_ms": s[-1],
    }


def validate_yolo_window_trial_result_v0(window_frames: int, raw: Mapping[str, Any]) -> Dict[str, Any]:
    """Shape single-window report from Phase-005 raw dict."""
    fp = int(raw.get("frames_processed") or 0)
    ha = raw.get("hard_audit") or {}
    lat = list(raw.get("latency_ms_per_frame") or [])
    violation = fp > window_frames
    return {
        "trial_id": raw.get("trial_id"),
        "phase": PHASE,
        "window_frames": window_frames,
        "input_video": (raw.get("input_video_validation") or {}).get("path_resolved"),
        "execution_mode": "offline_slice_trial",
        "frames_attempted": raw.get("frames_attempted"),
        "frames_processed": fp,
        "detector_invoked": raw.get("detector_invoked"),
        "camera_invoked": raw.get("camera_invoked"),
        "video_stream_type": raw.get("video_stream_type"),
        "detection_results_count": raw.get("detection_results_count"),
        "schema_valid_count": raw.get("schema_valid_count"),
        "schema_invalid_count": raw.get("schema_invalid_count"),
        "detector_error_count": raw.get("detector_error_count"),
        "latency": _latency_aggregate_v0(lat),
        "abort_triggered": raw.get("abort_triggered"),
        "abort_reason": raw.get("abort_reason"),
        "post_trial_recommendation": raw.get("post_trial_recommendation"),
        "hard_audit": ha,
        "frames_over_window_violation": violation,
        "rollback_snapshot": raw.get("rollback_snapshot"),
    }


def run_yolo_stage1_window_trial_v0(
    *,
    repo_root: Path,
    input_video_path: str,
    window_frames: int,
    approval_root: Optional[Path] = None,
) -> Dict[str, Any]:
    from capabilities.guarded_trial.yolo_stage1_10_frame_executor_v0 import (
        run_yolo_stage1_10_frame_dry_run_execution_v0,
    )

    return run_yolo_stage1_10_frame_dry_run_execution_v0(
        repo_root=repo_root,
        input_video_path=input_video_path,
        approval_root=approval_root,
        max_frames=window_frames,
    )


def build_yolo_multi_window_summary_v0(
    *,
    multi_window_trial_id: str,
    baseline_status: str,
    windows_requested: List[int],
    windows_executed: List[int],
    windows_skipped: List[Dict[str, Any]],
    window_reports: Dict[int, Dict[str, Any]],
    stop_reason: Optional[str],
) -> Dict[str, Any]:
    final_w = windows_executed[-1] if windows_executed else None
    last_rec = window_reports[final_w]["post_trial_recommendation"] if final_w and final_w in window_reports else None

    side_effect = any(
        (wr.get("hard_audit") or {}).get("downstream_invocation_count", 0) > 0
        or (wr.get("hard_audit") or {}).get("ocr_invoked")
        for wr in window_reports.values()
    )
    all_ha_ok = all(
        not (wr.get("hard_audit") or {}).get("camera_invoked")
        and int((wr.get("hard_audit") or {}).get("downstream_invocation_count") or 0) == 0
        for wr in window_reports.values()
    )

    if stop_reason and "no_go" in stop_reason.lower():
        final_rec = "NO_GO_rollback_and_fix"
    elif stop_reason == "conditional_go_stop_no_upgrade":
        final_rec = "CONDITIONAL_GO_repeat_last_window"
    elif len(windows_executed) == len(windows_requested) and all(
        window_reports[w].get("post_trial_recommendation") == "GO_next_window" for w in windows_executed
    ):
        final_rec = "GO_next_phase"
    elif last_rec == "CONDITIONAL_GO_repeat":
        final_rec = "CONDITIONAL_GO_repeat_last_window"
    else:
        final_rec = "NO_GO_rollback_and_fix"

    return {
        "multi_window_trial_id": multi_window_trial_id,
        "phase": PHASE,
        "baseline_10_frame_status": baseline_status,
        "windows_requested": windows_requested,
        "windows_executed": windows_executed,
        "windows_skipped": windows_skipped,
        "final_window_completed": final_w,
        "final_recommendation": final_rec,
        "stop_reason": stop_reason,
        "side_effect_detected": bool(side_effect),
        "all_hard_audit_ok": bool(all_ha_ok and window_reports),
    }


def run_yolo_stage1_multi_window_offline_slice_trial_v0(
    *,
    repo_root: Path,
    baseline_10_root: Path,
    input_video_path: str,
    windows: Sequence[int],
    approval_root: Optional[Path] = None,
) -> Dict[str, Any]:
    """
    Serial gated execution: baseline must be GO; each window must GO_next_window to proceed.
    NO_GO or CONDITIONAL_GO stops further windows (no auto-upgrade).
    """
    mw_id = f"yolo_s1_mw006_{uuid.uuid4().hex[:12]}"
    gate = validate_yolo_multi_window_input_v0(windows=windows, input_video_path=input_video_path)
    if not gate.get("valid"):
        return {
            "multi_window_trial_id": mw_id,
            "phase": PHASE,
            "gate_preflight_failed": True,
            "gate": gate,
            "window_reports": {},
            "summary": build_yolo_multi_window_summary_v0(
                multi_window_trial_id=mw_id,
                baseline_status="NOT_CHECKED",
                windows_requested=sorted(set(int(x) for x in windows)),
                windows_executed=[],
                windows_skipped=[{"window": w, "reason": "preflight_failed"} for w in sorted(set(int(x) for x in windows))],
                window_reports={},
                stop_reason="multi_window_input_invalid",
            ),
        }

    bl = load_yolo_10_frame_baseline_v0(baseline_10_root)
    if not bl.get("ok"):
        return {
            "multi_window_trial_id": mw_id,
            "phase": PHASE,
            "baseline_load": bl,
            "window_reports": {},
            "summary": build_yolo_multi_window_summary_v0(
                multi_window_trial_id=mw_id,
                baseline_status=bl.get("baseline_10_frame_status", "NO_GO"),
                windows_requested=gate["windows_requested"],
                windows_executed=[],
                windows_skipped=[{"window": w, "reason": "baseline_10_not_go"} for w in gate["windows_requested"]],
                window_reports={},
                stop_reason="baseline_10_frame_not_go",
            ),
        }

    path_resolved = str((gate["video_validation"] or {}).get("path_resolved") or "")
    if path_resolved and not baseline_video_matches_input_v0(bl.get("summary") or {}, path_resolved):
        return {
            "multi_window_trial_id": mw_id,
            "phase": PHASE,
            "baseline_load": bl,
            "video_mismatch": {
                "baseline_input": (bl.get("summary") or {}).get("input_video"),
                "current_resolved": path_resolved,
            },
            "window_reports": {},
            "summary": build_yolo_multi_window_summary_v0(
                multi_window_trial_id=mw_id,
                baseline_status="GO",
                windows_requested=gate["windows_requested"],
                windows_executed=[],
                windows_skipped=[{"window": w, "reason": "input_video_mismatch_vs_baseline"} for w in gate["windows_requested"]],
                window_reports={},
                stop_reason="baseline_video_path_mismatch",
            ),
        }

    plan = build_yolo_multi_window_trial_plan_v0(windows=gate["windows_requested"])
    ws_list = list(plan["windows_requested"])
    executed: List[int] = []
    skipped: List[Dict[str, Any]] = []
    reports: Dict[int, Dict[str, Any]] = {}
    stop_reason: Optional[str] = None
    prev_gate_ok = True

    for w in ws_list:
        if not prev_gate_ok:
            skipped.append({"window": w, "reason": "previous_window_did_not_reach_go"})
            continue

        raw = run_yolo_stage1_window_trial_v0(
            repo_root=repo_root,
            input_video_path=input_video_path,
            window_frames=w,
            approval_root=approval_root,
        )
        wr = validate_yolo_window_trial_result_v0(w, raw)
        if wr.get("frames_over_window_violation"):
            stop_reason = "frames_processed_exceeds_window"
            wr["post_trial_recommendation"] = "NO_GO_rollback_and_fix"
        reports[w] = wr
        executed.append(w)

        rec = wr.get("post_trial_recommendation")
        if rec == "NO_GO_rollback_and_fix" or wr.get("abort_triggered"):
            stop_reason = stop_reason or "window_no_go"
            prev_gate_ok = False
            for w2 in ws_list:
                if w2 > w and all(s.get("window") != w2 for s in skipped):
                    skipped.append({"window": w2, "reason": "stopped_after_no_go"})
            break
        if rec == "CONDITIONAL_GO_repeat":
            stop_reason = "conditional_go_stop_no_upgrade"
            prev_gate_ok = False
            for w2 in ws_list:
                if w2 > w and all(s.get("window") != w2 for s in skipped):
                    skipped.append({"window": w2, "reason": "stopped_after_conditional_go_no_upgrade"})
            break
        if rec == "GO_next_window":
            prev_gate_ok = True
            continue

        stop_reason = stop_reason or "unexpected_recommendation"
        prev_gate_ok = False
        break

    summary = build_yolo_multi_window_summary_v0(
        multi_window_trial_id=mw_id,
        baseline_status="GO",
        windows_requested=ws_list,
        windows_executed=executed,
        windows_skipped=skipped,
        window_reports=reports,
        stop_reason=stop_reason,
    )

    return {
        "multi_window_trial_id": mw_id,
        "phase": PHASE,
        "plan": plan,
        "baseline_load": bl,
        "input_gate": gate,
        "window_reports": reports,
        "summary": summary,
    }
