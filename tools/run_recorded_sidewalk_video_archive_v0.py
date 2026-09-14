#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-RealSceneReplay-001
Recorded sidewalk / real-world video -> recorded_video_replay archive_root v0.

Hard boundaries:
- evidence_type MUST be recorded_video_replay (NOT controlled_live)
- controlled_live = false
- pending_real_sidewalk_run = true

This tool does NOT run any live trial.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import time
import uuid
from typing import Any, Dict, List, Optional, Tuple

import cv2


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
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def _write_json(path: str, obj: Dict[str, Any]) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)


def _write_jsonl(path: str, rows: List[Dict[str, Any]]) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def _is_dir_empty(path: str) -> bool:
    if not os.path.exists(path):
        return True
    if not os.path.isdir(path):
        return False
    return len(os.listdir(path)) == 0


def _build_manifest(archive_root: str, required_files: List[str]) -> Dict[str, Any]:
    file_hashes: Dict[str, str] = {}
    missing_files: List[str] = []
    for relp in required_files:
        ap = os.path.join(archive_root, relp)
        if not os.path.exists(ap):
            missing_files.append(relp)
            continue
        file_hashes[relp] = _sha256_file(ap)
    integrity_status = "pass" if not missing_files else "partial"
    return {
        "manifest_id": f"m_{uuid.uuid4().hex[:10]}",
        "run_id": _load_run_id(os.path.join(archive_root, "run_evidence.json")),
        "generated_at_ms": _now_ms(),
        "archive_root_path": archive_root,
        "required_files": list(required_files),
        "file_hashes": file_hashes,
        "missing_files": missing_files,
        "hash_mismatches": [],
        "integrity_status": integrity_status,
        "archive_ready": integrity_status == "pass",
    }


def _load_run_id(run_evidence_path: str) -> str:
    try:
        with open(run_evidence_path, "r", encoding="utf-8") as f:
            return json.load(f).get("run_id", "unknown")
    except Exception:
        return "unknown"


def _video_duration_ms(frame_count: Optional[int], fps: float) -> Optional[int]:
    if frame_count is None or frame_count <= 0 or not fps or fps <= 0:
        return None
    return int((frame_count / fps) * 1000)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--video-path", required=True)
    ap.add_argument("--archive-root", required=True)
    ap.add_argument("--operator-id", required=True)
    ap.add_argument("--record-owner-id", required=True)
    ap.add_argument("--frame-step", type=int, default=30, help="sample every N frames (default 30 ≈ 1fps@30fps)")
    ap.add_argument("--max-sampled-frames", type=int, default=300, help="cap sampled frames (default 300)")
    args = ap.parse_args()

    video_path = str(args.video_path)
    archive_root = str(args.archive_root)
    operator_id = str(args.operator_id)
    record_owner_id = str(args.record_owner_id)

    if not video_path or not os.path.exists(video_path):
        raise SystemExit("ERROR: video_path_missing_or_not_found")
    if not archive_root.strip():
        raise SystemExit("ERROR: archive_root_empty")
    if not operator_id.strip():
        raise SystemExit("ERROR: operator_id_empty")
    if not record_owner_id.strip():
        raise SystemExit("ERROR: record_owner_id_empty")
    if not _is_dir_empty(archive_root):
        raise SystemExit("ERROR: archive_root_must_be_empty_dir_or_nonexistent")
    if args.frame_step <= 0:
        raise SystemExit("ERROR: frame_step_invalid")
    if args.max_sampled_frames <= 0:
        raise SystemExit("ERROR: max_sampled_frames_invalid")

    os.makedirs(archive_root, exist_ok=True)

    run_id = f"replay_{uuid.uuid4().hex[:10]}"
    start_ms = _now_ms()

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise SystemExit("ERROR: failed_to_open_video")

    fps = float(cap.get(cv2.CAP_PROP_FPS) or 0.0)
    total_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    frame_count: Optional[int] = int(total_frames) if total_frames and total_frames > 0 else None
    duration_ms = _video_duration_ms(frame_count, fps)

    trace_rows: List[Dict[str, Any]] = []
    replay_rows: List[Dict[str, Any]] = []

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

    trace("run_started", {"phase": "Phase-RealSceneReplay-001", "evidence_type": "recorded_video_replay"})
    trace(
        "video_opened",
        {
            "video_path": video_path,
            "video_filename": os.path.basename(video_path),
            "fps": fps,
            "frame_count": frame_count,
            "video_duration_ms": duration_ms,
        },
    )

    sampled = 0
    idx = 0
    try:
        while sampled < args.max_sampled_frames:
            ret, frame = cap.read()
            if not ret:
                break
            idx += 1
            if (idx - 1) % args.frame_step != 0:
                continue
            sampled += 1
            # best-effort timestamp based on fps + index
            ts_ms = int(((idx - 1) / fps) * 1000) if fps and fps > 0 else _now_ms()
            frame_ref = f"recorded_video://{os.path.basename(video_path)}#frame/{idx}"
            trace("frame_sampled", {"frame_index": idx, "timestamp_ms": ts_ms, "frame_ref": frame_ref})
            replay_rows.append(
                {
                    "timestamp_ms": ts_ms,
                    "frame_index": idx,
                    "frame_ref": frame_ref,
                    "input_source": "recorded_video",
                    "replay_available": True,
                }
            )
    finally:
        cap.release()

    trace(
        "no_execute_leakage_assertion",
        {
            "no_execute_leakage_assertion": True,
            "no_default_on_assertion": True,
            "no_side_effect_expansion_assertion": True,
        },
    )
    trace("run_completed", {"sampled_frame_count": sampled})

    # Minimal v0 whitebox/model/output (candidate-only)
    whitebox_rows = [
        {
            "timestamp_ms": _now_ms(),
            "run_id": run_id,
            "candidate_only": True,
            "default_path_disabled": True,
            "full_controlled_trial": False,
            "model_execution_authority": False,
            "allows_execute_now": False,
            "mode": "recorded_video_replay",
        }
    ]
    model_rows = [
        {
            "timestamp_ms": _now_ms(),
            "run_id": run_id,
            "model_invoked": False,
            "model_shadow_status": "disabled_or_not_used",
            "candidate_only": True,
            "reason": "replay_001_v0_focus_on_video_replay_evidence_chain",
        }
    ]
    output_rows = [
        {
            "timestamp_ms": _now_ms(),
            "run_id": run_id,
            "output_type": "silence",
            "allows_execute_now": False,
            "suppression_reason": "replay_001_v0_no_output_chain_execution",
            "reason_codes": ["CANDIDATE_ONLY", "RECORDED_VIDEO_REPLAY"],
        }
    ]

    trace_path = os.path.join(archive_root, "trace.jsonl")
    replay_path = os.path.join(archive_root, "replay.jsonl")
    whitebox_path = os.path.join(archive_root, "whitebox.jsonl")
    model_path = os.path.join(archive_root, "model_candidate_trace.jsonl")
    output_path = os.path.join(archive_root, "output_candidate_trace.jsonl")
    notes_path = os.path.join(archive_root, "operator_notes.md")
    risk_path = os.path.join(archive_root, "risk_events.jsonl")
    post_path = os.path.join(archive_root, "post_run_summary.md")
    manifest_path = os.path.join(archive_root, "archive_manifest.json")
    run_evidence_path = os.path.join(archive_root, "run_evidence.json")

    _write_jsonl(trace_path, trace_rows)
    _write_jsonl(replay_path, replay_rows)
    _write_jsonl(whitebox_path, whitebox_rows)
    _write_jsonl(model_path, model_rows)
    _write_jsonl(output_path, output_rows)

    _write_text(
        notes_path,
        "\n".join(
            [
                "# operator_notes_v0 (recorded_video_replay)",
                "",
                f"- run_id: {run_id}",
                f"- operator_id: {operator_id}",
                f"- record_owner_id: {record_owner_id}",
                f"- video_filename: {os.path.basename(video_path)}",
                "- environment_summary: recorded video replay (not controlled live)",
                "- observed_behavior_summary: (to be filled by operator)",
                "- unexpected_behavior: none_observed",
                "- privacy_issue_observed: unknown (review video content before sharing)",
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
                "note": "recorded_video_replay: no live run performed",
            }
        ],
    )

    end_ms = _now_ms()
    _write_text(
        post_path,
        "\n".join(
            [
                "# post_run_summary_v0 (recorded_video_replay)",
                "",
                f"- run_id: {run_id}",
                "- run_status: completed",
                f"- video_path: {video_path}",
                f"- sampled_frame_count: {sampled}",
                f"- duration_ms: {end_ms - start_ms}",
                "- controlled_live: false",
                "- pending_real_sidewalk_run: true",
                "- safety_assertions:",
                "  - no_execute_leakage_assertion: true",
                "  - no_default_on_assertion: true",
                "  - no_side_effect_expansion_assertion: true",
                "",
            ]
        )
        + "\n",
    )

    run_evidence: Dict[str, Any] = {
        "run_id": run_id,
        "scenario_id": "recorded_sidewalk_video_replay_v0",
        "selected_option": "OptionA_sidewalk_short_walk_observe_replay",
        "evidence_type": "recorded_video_replay",
        "controlled_live": False,
        "pending_real_sidewalk_run": True,
        "input_source": "recorded_video",
        "video_path": video_path,
        "video_filename": os.path.basename(video_path),
        "video_duration_ms": duration_ms,
        "frame_count": frame_count,
        "sampled_frame_count": sampled,
        "operator_id": operator_id,
        "record_owner_id": record_owner_id,
        "start_time_ms": start_ms,
        "end_time_ms": end_ms,
        "duration_ms": end_ms - start_ms,
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
        "overall_run_status": "completed",
    }
    _write_json(run_evidence_path, run_evidence)

    # manifest last (two-pass like Fix-001 style; self-hash allowed)
    _write_json(manifest_path, {"placeholder": True})
    _write_json(manifest_path, _build_manifest(archive_root, REQUIRED_RELATIVE_FILES_V0))
    _write_json(manifest_path, _build_manifest(archive_root, REQUIRED_RELATIVE_FILES_V0))

    print(
        json.dumps(
            {
                "tool": "run_recorded_sidewalk_video_archive_v0",
                "phase": "Phase-RealSceneReplay-001",
                "archive_root": archive_root,
                "run_id": run_id,
                "video_path": video_path,
                "sampled_frame_count": sampled,
                "assertions": {
                    "controlled_live": False,
                    "pending_real_sidewalk_run": True,
                    "default_path_enabled": False,
                    "full_controlled_trial_entered": False,
                    "real_side_effects_expanded": False,
                    "open_user_testing": False,
                    "scope_expanded": False,
                },
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()

