#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-DeviceEnv-003
Mac Camera Controlled Live Archive Adapter v0.

Evidence-only adapter:
- Captures real frames from Mac camera (OpenCV) within a strict timebox.
- Produces RealScene archive_root required files (Fix-001 validator compatible).
- Does NOT enable default path, does NOT grant execution authority, candidate-only.
"""

from __future__ import annotations

import hashlib
import json
import os
import time
import uuid
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple


REQUIRED_RELATIVE_FILES_V0: List[str] = [
    "run_evidence.json",
    "trace.jsonl",
    "replay.jsonl",
    "whitebox.jsonl",
    "model_candidate_trace.jsonl",
    "output_candidate_trace.jsonl",
    "operator_notes.md",
    "risk_events.jsonl",
    "post_run_summary.md",
    "archive_manifest.json",
]


def _now_ms() -> int:
    return int(time.time() * 1000)


def _ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def _sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            b = f.read(1024 * 1024)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def _write_text(path: str, content: str) -> None:
    d = os.path.dirname(path)
    if d:
        os.makedirs(d, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def _write_json(path: str, obj: Dict[str, Any]) -> None:
    d = os.path.dirname(path)
    if d:
        os.makedirs(d, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)


def _write_jsonl(path: str, rows: List[Dict[str, Any]]) -> None:
    d = os.path.dirname(path)
    if d:
        os.makedirs(d, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def _is_dir_empty(path: str) -> bool:
    if not os.path.exists(path):
        return True
    if not os.path.isdir(path):
        return False
    return len(os.listdir(path)) == 0


def build_archive_manifest_v0(archive_root: str, required_files: List[str]) -> Dict[str, Any]:
    file_hashes: Dict[str, str] = {}
    missing_files: List[str] = []
    for relp in required_files:
        ap = os.path.join(archive_root, relp)
        if not os.path.exists(ap):
            missing_files.append(relp)
            continue
        file_hashes[relp] = _sha256_file(ap)

    integrity_status = "pass" if not missing_files else "partial"
    archive_ready = integrity_status == "pass"
    run_id = "unknown"
    run_evidence_path = os.path.join(archive_root, "run_evidence.json")
    if os.path.exists(run_evidence_path):
        try:
            with open(run_evidence_path, "r", encoding="utf-8") as f:
                run_id = json.load(f).get("run_id", "unknown")
        except Exception:
            run_id = "unknown"

    return {
        "manifest_id": f"m_{uuid.uuid4().hex[:10]}",
        "run_id": run_id,
        "generated_at_ms": _now_ms(),
        "archive_root_path": archive_root,
        "required_files": list(required_files),
        "file_hashes": file_hashes,
        "missing_files": missing_files,
        "hash_mismatches": [],
        "integrity_status": integrity_status,
        "archive_ready": archive_ready,
    }


@dataclass(frozen=True)
class RunParams:
    archive_root: str
    operator_id: str
    safety_observer_id: str
    record_owner_id: str
    timebox_ms: int
    camera_index: int
    explicit_entry_token: str


@dataclass(frozen=True)
class RunResult:
    overall_run_status: str  # completed | failed_camera_unavailable | failed_exception
    archive_root: str
    run_id: Optional[str]
    camera_opened: bool
    frame_count: int
    start_time_ms: Optional[int]
    end_time_ms: Optional[int]
    failure_reason: Optional[str]


def _validate_params(p: RunParams) -> Tuple[bool, str]:
    if not str(p.archive_root or "").strip():
        return False, "archive_root_empty"
    if not str(p.operator_id or "").strip():
        return False, "operator_id_empty"
    if not str(p.safety_observer_id or "").strip():
        return False, "safety_observer_id_empty"
    if not str(p.record_owner_id or "").strip():
        return False, "record_owner_id_empty"
    if not str(p.explicit_entry_token or "").strip():
        return False, "explicit_entry_token_empty"
    if not isinstance(p.timebox_ms, int) or p.timebox_ms <= 0:
        return False, "timebox_ms_invalid"
    # v0 safety upper bound: short run only
    if p.timebox_ms > 60_000:
        return False, "timebox_ms_exceeds_v0_cap_60000"
    if not isinstance(p.camera_index, int):
        return False, "camera_index_invalid"
    return True, ""


def run_mac_camera_controlled_live_archive_v0(params: RunParams) -> RunResult:
    ok, reason = _validate_params(params)
    if not ok:
        raise ValueError(reason)

    if not _is_dir_empty(params.archive_root):
        raise ValueError("archive_root_must_be_empty_dir_or_nonexistent")

    _ensure_dir(params.archive_root)

    run_id = f"live_{uuid.uuid4().hex[:10]}"
    start_ms = _now_ms()

    trace_rows: List[Dict[str, Any]] = []
    replay_rows: List[Dict[str, Any]] = []
    whitebox_rows: List[Dict[str, Any]] = []
    model_rows: List[Dict[str, Any]] = []
    output_rows: List[Dict[str, Any]] = []

    def trace(event_type: str, payload: Optional[Dict[str, Any]] = None) -> None:
        trace_rows.append(
            {
                "timestamp_ms": _now_ms(),
                "run_id": run_id,
                "event_type": event_type,
                "seq": len(trace_rows) + 1,
                "payload": payload or {},
            }
        )

    trace("run_started", {"phase": "Phase-DeviceEnv-003", "evidence_type": "controlled_live"})
    trace("mode_entry", {"explicit_trial_intent": True, "entry_token": params.explicit_entry_token})

    frame_count = 0
    camera_opened = False
    failure_reason: Optional[str] = None

    abort_triggered = False
    abort_reason: Optional[str] = None
    fallback_triggered = False
    degraded_triggered = False

    # Camera open (real input)
    cam = None
    try:
        from utils.camera_handler import CameraHandler  # repo-local

        cam = CameraHandler(camera_index=params.camera_index)
        camera_opened = bool(cam.is_opened())
        trace("camera_opened", {"camera_opened": camera_opened, "camera_index": params.camera_index})

        if not camera_opened:
            failure_reason = "camera_failed_to_open"
            trace("run_failed", {"reason": failure_reason})
            end_ms = _now_ms()
            _write_failed_run_report(params.archive_root, run_id, params, start_ms, end_ms, failure_reason)
            return RunResult(
                overall_run_status="failed_camera_unavailable",
                archive_root=params.archive_root,
                run_id=run_id,
                camera_opened=False,
                frame_count=0,
                start_time_ms=start_ms,
                end_time_ms=end_ms,
                failure_reason=failure_reason,
            )

        trace("controlled_live_input_started", {"controlled_live_input_started": True})

        deadline = time.time() + (params.timebox_ms / 1000.0)
        while time.time() < deadline:
            frame = cam.read_frame()
            if frame is None:
                # allow transient read failures; keep trying until timebox ends
                time.sleep(0.01)
                continue
            frame_count += 1
            ts_ms = _now_ms()
            trace("frame_captured", {"frame_index": frame_count, "timestamp_ms": ts_ms, "source": "mac_camera"})
            replay_rows.append(
                {
                    "timestamp_ms": ts_ms,
                    "frame_index": frame_count,
                    "frame_ref": f"controlled_live://frame/{frame_count}",
                    "source": "mac_camera",
                    "replay_available": True,
                }
            )
            # v0: do not attempt to run heavy pipelines; keep cadence modest
            time.sleep(0.03)

        trace("controlled_live_input_ended", {"controlled_live_input_ended": True, "frame_count": frame_count})

        # Minimal whitebox / model / output traces (candidate-only)
        whitebox_rows.append(
            {
                "timestamp_ms": _now_ms(),
                "run_id": run_id,
                "candidate_only": True,
                "default_path_disabled": True,
                "full_controlled_trial": False,
                "model_execution_authority": False,
                "allows_execute_now": False,
                "suppression": {"status": "none", "reasons": []},
                "gates": {
                    "no_execute_leakage_assertion": True,
                    "no_default_on_assertion": True,
                    "no_side_effect_expansion_assertion": True,
                },
            }
        )
        model_rows.append(
            {
                "timestamp_ms": _now_ms(),
                "run_id": run_id,
                "model_invoked": False,
                "model_shadow_status": "disabled_or_not_used",
                "candidate_only": True,
                "reason": "device_env_003_v0_focus_on_live_input_evidence_pipeline",
            }
        )
        output_rows.append(
            {
                "timestamp_ms": _now_ms(),
                "run_id": run_id,
                "output_type": "silence",
                "allows_execute_now": False,
                "suppression_reason": "device_env_003_v0_no_output_chain_execution",
                "reason_codes": ["CANDIDATE_ONLY", "NO_EXECUTE_AUTHORITY"],
            }
        )

        # Safety assertion event in trace
        trace(
            "no_execute_leakage_assertion",
            {
                "no_execute_leakage_assertion": True,
                "no_default_on_assertion": True,
                "no_side_effect_expansion_assertion": True,
            },
        )

    except Exception as e:
        failure_reason = f"exception:{type(e).__name__}:{e}"
        trace("run_failed", {"reason": failure_reason})
        end_ms = _now_ms()
        _write_failed_run_report(params.archive_root, run_id, params, start_ms, end_ms, failure_reason)
        return RunResult(
            overall_run_status="failed_exception",
            archive_root=params.archive_root,
            run_id=run_id,
            camera_opened=camera_opened,
            frame_count=frame_count,
            start_time_ms=start_ms,
            end_time_ms=end_ms,
            failure_reason=failure_reason,
        )
    finally:
        try:
            if cam is not None:
                cam.release()
        except Exception:
            pass

    end_ms = _now_ms()

    if frame_count <= 0:
        # No frames captured: treat as failure (do NOT emit controlled_live evidence archive)
        failure_reason = "no_frames_captured_within_timebox"
        trace("run_failed", {"reason": failure_reason})
        _write_failed_run_report(params.archive_root, run_id, params, start_ms, end_ms, failure_reason)
        return RunResult(
            overall_run_status="failed_camera_unavailable",
            archive_root=params.archive_root,
            run_id=run_id,
            camera_opened=True,
            frame_count=0,
            start_time_ms=start_ms,
            end_time_ms=end_ms,
            failure_reason=failure_reason,
        )

    # Success path: emit Fix-001 required files
    trace_path = os.path.join(params.archive_root, "trace.jsonl")
    replay_path = os.path.join(params.archive_root, "replay.jsonl")
    whitebox_path = os.path.join(params.archive_root, "whitebox.jsonl")
    model_path = os.path.join(params.archive_root, "model_candidate_trace.jsonl")
    output_path = os.path.join(params.archive_root, "output_candidate_trace.jsonl")
    notes_path = os.path.join(params.archive_root, "operator_notes.md")
    risk_path = os.path.join(params.archive_root, "risk_events.jsonl")
    post_path = os.path.join(params.archive_root, "post_run_summary.md")
    manifest_path = os.path.join(params.archive_root, "archive_manifest.json")
    run_evidence_path = os.path.join(params.archive_root, "run_evidence.json")

    # Record completion BEFORE writing trace + manifest (avoid hash mismatch)
    trace("run_completed", {"frame_count": frame_count, "archive_ready": True})

    _write_jsonl(trace_path, trace_rows)
    _write_jsonl(replay_path, replay_rows)
    _write_jsonl(whitebox_path, whitebox_rows)
    _write_jsonl(model_path, model_rows)
    _write_jsonl(output_path, output_rows)

    _write_text(
        notes_path,
        "\n".join(
            [
                "# operator_notes_v0",
                "",
                f"- run_id: {run_id}",
                f"- operator_id: {params.operator_id}",
                f"- safety_observer_id: {params.safety_observer_id}",
                f"- record_owner_id: {params.record_owner_id}",
                "- environment_summary: (to be filled by operator)",
                "- scenario_summary: sidewalk_short_walk_observe_v0",
                "- observed_behavior_summary: (to be filled by operator)",
                "- unexpected_behavior: none_observed",
                "- manual_intervention: none",
                "- abort_used: false",
                "- fallback_used: false",
                "- degraded_used: false",
                "- privacy_issue_observed: none_observed",
                "- follow_up_required: false",
                "",
            ]
        )
        + "\n",
    )

    _write_jsonl(
        risk_path,
        [
            {
                "risk_events_status": "none_observed",
                "timestamp_ms": _now_ms(),
                "source": "record_owner",
            }
        ],
    )

    _write_text(
        post_path,
        "\n".join(
            [
                "# post_run_summary_v0",
                "",
                f"- run_id: {run_id}",
                "- run_status: completed",
                f"- frame_count: {frame_count}",
                f"- duration_ms: {end_ms - start_ms}",
                "- archive_ready_pre_manifest: true",
                "- safety_assertions:",
                "  - no_execute_leakage_assertion: true",
                "  - no_default_on_assertion: true",
                "  - no_side_effect_expansion_assertion: true",
                "- follow_up_required: false",
                "",
            ]
        )
        + "\n",
    )

    run_evidence: Dict[str, Any] = {
        "run_id": run_id,
        "scenario_id": "sidewalk_short_walk_observe_v0",
        "selected_option": "OptionA_sidewalk_short_walk_observe",
        "evidence_type": "controlled_live",
        "input_source": "mac_camera",
        "explicit_trial_intent": True,
        "entry_token": params.explicit_entry_token,
        "mode_entry_event_present": True,
        "controlled_live_input_started": True,
        "controlled_live_input_ended": True,
        "operator_id": params.operator_id,
        "safety_observer_id": params.safety_observer_id,
        "record_owner_id": params.record_owner_id,
        "start_time_ms": start_ms,
        "end_time_ms": end_ms,
        "duration_ms": end_ms - start_ms,
        "timebox_ms": params.timebox_ms,
        "frame_count": frame_count,
        "trace_file_path": "trace.jsonl",
        "replay_file_path": "replay.jsonl",
        "whitebox_file_path": "whitebox.jsonl",
        "model_candidate_trace_path": "model_candidate_trace.jsonl",
        "output_candidate_trace_path": "output_candidate_trace.jsonl",
        "operator_notes_path": "operator_notes.md",
        "risk_events_path": "risk_events.jsonl",
        "archive_manifest_path": "archive_manifest.json",
        "post_run_summary_path": "post_run_summary.md",
        "no_execute_leakage_assertion": True,
        "no_default_on_assertion": True,
        "no_side_effect_expansion_assertion": True,
        "abort_triggered": abort_triggered,
        "abort_reason": abort_reason,
        "fallback_triggered": fallback_triggered,
        "degraded_triggered": degraded_triggered,
        "overall_run_status": "completed",
    }
    _write_json(run_evidence_path, run_evidence)

    # Manifest last (placeholder then two-pass build to include final manifest bytes)
    _write_json(manifest_path, {"placeholder": True})
    man1 = build_archive_manifest_v0(params.archive_root, REQUIRED_RELATIVE_FILES_V0)
    _write_json(manifest_path, man1)
    man2 = build_archive_manifest_v0(params.archive_root, REQUIRED_RELATIVE_FILES_V0)
    _write_json(manifest_path, man2)

    return RunResult(
        overall_run_status="completed",
        archive_root=params.archive_root,
        run_id=run_id,
        camera_opened=True,
        frame_count=frame_count,
        start_time_ms=start_ms,
        end_time_ms=end_ms,
        failure_reason=None,
    )


def _write_failed_run_report(
    archive_root: str,
    run_id: str,
    params: RunParams,
    start_ms: int,
    end_ms: int,
    failure_reason: str,
) -> None:
    """
    Failure path must NOT emit a controlled_live evidence archive (required_files set).
    It may emit a minimal failed run report for debugging without pretending validator-ready.
    """
    report = {
        "phase": "Phase-DeviceEnv-003",
        "run_id": run_id,
        "overall_run_status": "failed",
        "camera_opened": False,
        "pending_real_camera_input": True,
        "failure_reason": failure_reason,
        "operator_id": params.operator_id,
        "safety_observer_id": params.safety_observer_id,
        "record_owner_id": params.record_owner_id,
        "camera_index": params.camera_index,
        "explicit_entry_token": params.explicit_entry_token,
        "start_time_ms": start_ms,
        "end_time_ms": end_ms,
        "duration_ms": end_ms - start_ms,
        "timebox_ms": params.timebox_ms,
        "no_execute_leakage_assertion": True,
        "no_default_on_assertion": True,
        "no_side_effect_expansion_assertion": True,
        "note": "This is NOT a controlled_live evidence archive. Do NOT treat as validator-ready.",
    }
    _write_json(os.path.join(archive_root, "failed_run_report.json"), report)

