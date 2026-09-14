#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-Mainline-GuardedTrial-005 — YOLO Stage-1 offline 10-frame dry-run execution (real detector on file video only).
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from capabilities.guarded_trial.yolo_stage1_10_frame_executor_v0 import PHASE, run_yolo_stage1_10_frame_dry_run_execution_v0


def _utc_tag() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%SZ")


def _write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")


def _append_jsonl(path: Path, row: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--approval-root", required=True, help="Phase-004 approval gate output directory")
    ap.add_argument("--input-video", required=True, help="Offline video path (.mp4/.mov/.mkv/.avi)")
    ap.add_argument("--output-root", default="")
    args = ap.parse_args()

    repo = Path(REPO_ROOT)
    appr = Path(args.approval_root)
    if not appr.is_absolute():
        appr = (repo / appr).resolve()

    out = Path(args.output_root) if args.output_root else repo / "logs" / f"yolo_stage1_10_frame_dry_run_execution_005_{_utc_tag()}"

    exec_result = run_yolo_stage1_10_frame_dry_run_execution_v0(
        repo_root=repo,
        input_video_path=args.input_video.strip(),
        approval_root=appr if appr.is_dir() else None,
        max_frames=10,
    )

    iv = exec_result.get("input_video_validation") or {}
    latency = {
        "trial_id": exec_result.get("trial_id"),
        "latency_ms_per_frame": exec_result.get("latency_ms_per_frame") or [],
        "elapsed_sec": exec_result.get("elapsed_sec"),
        "summary_ms": {
            "count": len(exec_result.get("latency_ms_per_frame") or []),
            "p50": None,
            "p95": None,
        },
    }
    lm = list(exec_result.get("latency_ms_per_frame") or [])
    if lm:
        s = sorted(lm)
        latency["summary_ms"]["p50"] = s[len(s) // 2]
        latency["summary_ms"]["p95"] = s[int(max(0, len(s) * 0.95 - 0.0001))]

    schema_agg = {
        "schema_invalid_count": exec_result.get("schema_invalid_count", 0),
        "schema_valid_count": exec_result.get("schema_valid_count", 0),
        "checks": exec_result.get("detection_schema_checks") or [],
    }

    abort_report = {
        "abort_triggered": exec_result.get("abort_triggered"),
        "abort_reason": exec_result.get("abort_reason"),
        "rollback_snapshot": exec_result.get("rollback_snapshot"),
        "detector_error_count": exec_result.get("detector_error_count"),
    }

    post_trial = {
        "trial_id": exec_result.get("trial_id"),
        "post_trial_recommendation": exec_result.get("post_trial_recommendation"),
        "post_trial_notes": exec_result.get("post_trial_notes"),
        "hard_audit": exec_result.get("hard_audit"),
        "approval_root": str(appr),
        "input_video": args.input_video.strip(),
    }

    summary: Dict[str, Any] = {
        "phase": PHASE,
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "repo_root": str(repo.resolve()),
        "output_root": str(out.resolve()),
        "approval_root": str(appr),
        "input_video": args.input_video.strip(),
        **{k: exec_result.get(k) for k in ("trial_id", "execution_mode", "max_frames", "frames_read_from_video", "frames_attempted", "frames_processed", "detector_invoked", "camera_invoked", "video_stream_type", "detection_results_count", "schema_invalid_count", "abort_triggered", "post_trial_recommendation")},
        "hard_audit": exec_result.get("hard_audit"),
        "verdict": {
            "trial_execution": exec_result.get("post_trial_recommendation"),
            "ocr_invoked": exec_result.get("hard_audit", {}).get("ocr_invoked"),
            "qwen_invoked": exec_result.get("hard_audit", {}).get("qwen_invoked"),
        },
    }
    wf = appr / "yolo_stage1_weight_snapshot.json"
    if wf.is_file():
        try:
            summary["approval_weight_snapshot_echo"] = json.loads(wf.read_text(encoding="utf-8"))
        except Exception:
            summary["approval_weight_snapshot_echo"] = {"error": "read_failed"}

    out.mkdir(parents=True, exist_ok=True)

    _write_json(out / "yolo_stage1_10_frame_dry_run_summary.json", summary)
    _write_json(out / "yolo_stage1_10_frame_input_video_validation.json", iv)
    _write_json(out / "yolo_stage1_10_frame_frame_sample_matrix.json", exec_result.get("frame_sample_matrix") or [])
    _write_json(out / "yolo_stage1_10_frame_detection_results.json", exec_result.get("detection_results_by_frame") or [])
    _write_json(out / "yolo_stage1_10_frame_detection_schema_validation.json", schema_agg)
    _write_json(out / "yolo_stage1_10_frame_latency_summary.json", latency)
    _write_json(out / "yolo_stage1_10_frame_abort_rollback_report.json", abort_report)
    _write_json(out / "yolo_stage1_10_frame_post_trial_report.json", post_trial)

    tid = exec_result.get("trial_id", "unknown")

    _append_jsonl(
        out / "yolo_stage1_10_frame_trace.jsonl",
        {"type": "yolo_stage1_10_frame_trace_v0", "trial_id": tid, "phase": PHASE, "frames_processed": exec_result.get("frames_processed")},
    )
    _append_jsonl(
        out / "yolo_stage1_10_frame_replay.jsonl",
        {"type": "yolo_stage1_replay_v0", "trial_id": tid, "input_resolution": iv},
    )
    req_stages = [
        "request_trace.stage.perception.yolo.input_frame",
        "request_trace.stage.perception.yolo.detector_invocation",
        "request_trace.stage.perception.yolo.detection_result",
    ]
    _append_jsonl(
        out / "yolo_stage1_10_frame_whitebox.jsonl",
        {
            "type": "yolo_stage1_whitebox_v0",
            "trial_id": tid,
            "request_trace_shadow_stages": req_stages,
            "hard_audit": exec_result.get("hard_audit"),
        },
    )

    notes = [
        f"# {PHASE} — 10-frame offline YOLO dry-run",
        "",
        f"- approval_root: `{appr}`",
        f"- output_root: `{out}`",
        "",
    ]
    (out / "execution_notes.md").write_text("\n".join(notes), encoding="utf-8")

    print(
        json.dumps(
            {
                "ok": True,
                "output_root": str(out),
                "post_trial_recommendation": exec_result.get("post_trial_recommendation"),
                "abort_triggered": exec_result.get("abort_triggered"),
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
