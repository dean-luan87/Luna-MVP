#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Phase-Mainline-GuardedTrial-005 10-frame dry-run outputs."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, Tuple

EXPECTED = [
    "yolo_stage1_10_frame_dry_run_summary.json",
    "yolo_stage1_10_frame_input_video_validation.json",
    "yolo_stage1_10_frame_frame_sample_matrix.json",
    "yolo_stage1_10_frame_detection_results.json",
    "yolo_stage1_10_frame_detection_schema_validation.json",
    "yolo_stage1_10_frame_latency_summary.json",
    "yolo_stage1_10_frame_abort_rollback_report.json",
    "yolo_stage1_10_frame_post_trial_report.json",
    "yolo_stage1_10_frame_trace.jsonl",
    "yolo_stage1_10_frame_replay.jsonl",
    "yolo_stage1_10_frame_whitebox.jsonl",
    "execution_notes.md",
]

ALLOWED_EXT = {".mp4", ".mov", ".mkv", ".avi"}


def _load(p: Path) -> Any:
    return json.loads(p.read_text(encoding="utf-8"))


def _nj(p: Path) -> bool:
    return p.is_file() and bool(p.read_text(encoding="utf-8").strip())


def verify(*, output_root: Path) -> Tuple[bool, Dict[str, Any]]:
    checks: Dict[str, Any] = {}

    for name in EXPECTED:
        k = f"A_{name}"
        checks[k] = (output_root / name).is_file()

    summ = _load(output_root / "yolo_stage1_10_frame_dry_run_summary.json")
    iv = _load(output_root / "yolo_stage1_10_frame_input_video_validation.json")
    ha = summ.get("hard_audit") or {}
    sv = _load(output_root / "yolo_stage1_10_frame_detection_schema_validation.json")

    ar = summ.get("approval_root")
    checks["B_approval_root_readable"] = isinstance(ar, str) and Path(ar).is_dir()
    checks["C_input_video_validation_exists"] = isinstance(iv, dict) and len(iv) > 0
    ext = (iv.get("extension") or "").lower()
    checks["D_extension_allowed"] = iv.get("valid") is True and ext in ALLOWED_EXT
    checks["E_camera_like_false"] = iv.get("camera_like") is not True

    fp = int(summ.get("frames_processed") or 0)
    mf = int(summ.get("max_frames") or 10)
    di = summ.get("detector_invoked")
    abort_flag = bool(summ.get("abort_triggered"))
    rec = summ.get("post_trial_recommendation")
    checks["F_frames_processed_lte_10"] = fp <= 10
    checks["G_detector_invoked_consistent_with_frames"] = (fp == 0 and di is False) or (fp > 0 and di is True)

    checks["H_detection_results_exists"] = (output_root / "yolo_stage1_10_frame_detection_results.json").is_file()
    checks["I_schema_validation_exists"] = isinstance(sv, dict) and ("schema_invalid_count" in sv)
    checks["J_schema_invalid_zero"] = int(sv.get("schema_invalid_count") or 0) == 0

    checks["K_downstream_invocation_zero"] = int(ha.get("downstream_invocation_count") or 0) == 0
    checks["L_navigation_action_null"] = ha.get("navigation_action") is None
    checks["M_real_tts_invoked_false"] = ha.get("real_tts_invoked") is False
    checks["N_qwen_invoked_false"] = ha.get("qwen_invoked") is False
    checks["O_ocr_invoked_false"] = ha.get("ocr_invoked") is False
    checks["P_world_write_false"] = ha.get("world_write_invoked") is False
    checks["Q_hive_upload_false"] = ha.get("hive_upload_invoked") is False

    checks["R_model_inference_matches_detector"] = ha.get("model_inference_invoked") == di
    checks["E2_camera_invoked_false"] = ha.get("camera_invoked") is False
    checks["E3_video_stream_offline"] = summ.get("video_stream_type") == "offline_file"
    checks["E4_real_yolo_consistent"] = (ha.get("real_yolo_execution") is True) == (fp > 0 and di is True)

    pt = _load(output_root / "yolo_stage1_10_frame_post_trial_report.json")
    checks["S_post_trial_exists"] = isinstance(pt, dict) and len(pt) > 0

    checks["T_trace_replay_whitebox_nonempty"] = (
        _nj(output_root / "yolo_stage1_10_frame_trace.jsonl")
        and _nj(output_root / "yolo_stage1_10_frame_replay.jsonl")
        and _nj(output_root / "yolo_stage1_10_frame_whitebox.jsonl")
    )

    ok_all = all(bool(v) for v in checks.values())

    if abort_flag or rec == "NO_GO_rollback_and_fix":
        trial_verdict = "NO_GO"
    elif rec == "GO_next_window" and not abort_flag and fp == mf:
        trial_verdict = "GO"
    elif rec == "CONDITIONAL_GO_repeat" and not abort_flag:
        trial_verdict = "CONDITIONAL_GO"
    else:
        trial_verdict = "NO_GO"

    return ok_all, {
        "checks": checks,
        "artifact_integrity": "GO" if ok_all else "NO_GO",
        "trial_verdict": trial_verdict,
        "post_trial_recommendation": rec,
        "abort_triggered": abort_flag,
        "frames_processed": fp,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-root", required=True)
    args = ap.parse_args()
    out = Path(args.output_root).resolve()
    try:
        ok, report = verify(output_root=out)
    except Exception as e:
        print(json.dumps({"ok": False, "error": str(e)}, ensure_ascii=False))
        return 2
    print(json.dumps({"ok": ok, **report}, ensure_ascii=False, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
