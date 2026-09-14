#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Phase-Mainline-GuardedTrial-006 multi-window offline trial outputs."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List, Tuple

EXPECTED = [
    "yolo_stage1_multi_window_full_result.json",
    "yolo_stage1_multi_window_summary.json",
    "yolo_stage1_multi_window_plan.json",
    "yolo_stage1_window_50_report.json",
    "yolo_stage1_window_100_report.json",
    "yolo_stage1_window_200_report.json",
    "yolo_stage1_multi_window_latency_summary.json",
    "yolo_stage1_multi_window_schema_validation_summary.json",
    "yolo_stage1_multi_window_abort_rollback_report.json",
    "yolo_stage1_multi_window_hard_audit_summary.json",
    "yolo_stage1_multi_window_trace.jsonl",
    "yolo_stage1_multi_window_replay.jsonl",
    "yolo_stage1_multi_window_whitebox.jsonl",
    "execution_notes.md",
]


def _load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _nj(path: Path) -> bool:
    return path.is_file() and bool(path.read_text(encoding="utf-8").strip())


def verify(*, output_root: Path) -> Tuple[bool, Dict[str, Any]]:
    checks: Dict[str, Any] = {}
    full_path = output_root / "yolo_stage1_multi_window_full_result.json"
    summ_path = output_root / "yolo_stage1_multi_window_summary.json"

    for name in EXPECTED:
        checks[f"A_{name}"] = (output_root / name).is_file()

    if not summ_path.is_file():
        checks["fatal_no_summary"] = False
        return False, {"checks": checks, "artifact_integrity": "NO_GO", "trial_phase_verdict": "NO_GO"}

    summ = _load(summ_path)
    full: Dict[str, Any] = {}
    if full_path.is_file():
        try:
            full = _load(full_path)
        except Exception:
            full = {}

    base = full.get("baseline_load") or {}
    ig = full.get("input_gate") or {}
    vid = ig.get("video_validation") if isinstance(ig, dict) else None

    replay = {}
    rp = output_root / "yolo_stage1_multi_window_replay.jsonl"
    if rp.is_file():
        try:
            line = rp.read_text(encoding="utf-8").strip().splitlines()[-1]
            replay = json.loads(line)
        except Exception:
            replay = {}

    baseline_root_txt = replay.get("baseline_10_root") or str(base.get("baseline_root") or "")
    checks["B_baseline_root_readable"] = bool(baseline_root_txt) and Path(baseline_root_txt).is_dir()
    checks["C_baseline_status_go"] = summ.get("baseline_10_frame_status") == "GO"

    checks["D_input_video_offline_gate"] = vid is None or vid.get("valid") is True
    checks["Vx_final_recommendation_present"] = bool(summ.get("final_recommendation"))

    wre = list(summ.get("windows_executed") or [])
    wrq = list(summ.get("windows_requested") or [])
    checks["E_windows_sorted_subsequence"] = wre == sorted(wre) and all(w in wrq for w in wre)

    wr = full.get("window_reports") or {}
    canon = [50, 100, 200]

    def _rep(w: int) -> Dict[str, Any]:
        r = wr.get(w) if isinstance(wr, dict) else {}
        if not r and isinstance(w, int):
            try:
                r = json.loads((output_root / f"yolo_stage1_window_{w}_report.json").read_text(encoding="utf-8"))
            except Exception:
                r = {}
        return r if isinstance(r, dict) else {}

    # F/G gating
    checks["F_100_requires_50_go"] = True
    checks["G_200_requires_100_go"] = True
    if 100 in wre:
        r50 = _rep(50)
        checks["F_100_requires_50_go"] = 50 in wre and r50.get("post_trial_recommendation") == "GO_next_window"
    if 200 in wre:
        r100 = _rep(100)
        checks["G_200_requires_100_go"] = (
            100 in wre and r100.get("post_trial_recommendation") == "GO_next_window" and 50 in wre
        )

    checks["Hi_frames_lte_window"] = True
    checks["Ii_detector_when_executed"] = True
    checks["Jj_schema_zero_on_go_windows"] = True
    checks["Kk_detector_errors_acceptable_for_go"] = True

    for w in wre:
        if w not in canon:
            checks["Hi_frames_lte_window"] = False
            continue
        rep = _rep(w)
        fp = int(rep.get("frames_processed") or 0)
        wf = int(rep.get("window_frames") or w)
        di = rep.get("detector_invoked")
        rec = rep.get("post_trial_recommendation")
        sce = int(rep.get("schema_invalid_count") or 0)
        derr = int(rep.get("detector_error_count") or 0)
        checks["Hi_frames_lte_window"] = checks["Hi_frames_lte_window"] and fp <= wf
        checks["Ii_detector_when_executed"] = checks["Ii_detector_when_executed"] and (fp <= 0 or di is True)
        if fp > 0 and di is not True:
            checks["Ii_detector_when_executed"] = False
        if rec == "GO_next_window":
            checks["Jj_schema_zero_on_go_windows"] = checks["Jj_schema_zero_on_go_windows"] and sce == 0
            checks["Kk_detector_errors_acceptable_for_go"] = checks["Kk_detector_errors_acceptable_for_go"] and derr == 0

    checks["Lc_camera_false"] = True
    checks["Md_ocr_false"] = True
    checks["Ne_qwen_false"] = True
    checks["Of_tts_false"] = True
    checks["Pg_playback_false"] = True
    checks["Qh_downstream_zero"] = True
    checks["Ri_nav_null"] = True
    checks["Sj_world_false"] = True
    checks["Tk_hive_false"] = True

    for w in wre:
        ha = _rep(w).get("hard_audit") or {}
        checks["Lc_camera_false"] = checks["Lc_camera_false"] and ha.get("camera_invoked") is not True
        checks["Md_ocr_false"] = checks["Md_ocr_false"] and ha.get("ocr_invoked") is not True
        checks["Ne_qwen_false"] = checks["Ne_qwen_false"] and ha.get("qwen_invoked") is not True
        checks["Of_tts_false"] = checks["Of_tts_false"] and ha.get("real_tts_invoked") is not True
        checks["Pg_playback_false"] = checks["Pg_playback_false"] and ha.get("playback_invoked") is not True
        checks["Qh_downstream_zero"] = checks["Qh_downstream_zero"] and int(ha.get("downstream_invocation_count") or 0) == 0
        checks["Ri_nav_null"] = checks["Ri_nav_null"] and ha.get("navigation_action") is None
        checks["Sj_world_false"] = checks["Sj_world_false"] and ha.get("world_write_invoked") is not True
        checks["Tk_hive_false"] = checks["Tk_hive_false"] and ha.get("hive_upload_invoked") is not True

    checks["Um_trw_nonempty"] = (
        _nj(output_root / "yolo_stage1_multi_window_trace.jsonl")
        and _nj(output_root / "yolo_stage1_multi_window_replay.jsonl")
        and _nj(output_root / "yolo_stage1_multi_window_whitebox.jsonl")
    )

    ok_art = all(bool(v) for v in checks.values())
    phase_go = summ.get("final_recommendation") == "GO_next_phase"
    trial_phase_verdict = "GO" if phase_go else ("CONDITIONAL_GO" if summ.get("stop_reason") == "conditional_go_stop_no_upgrade" else "NO_GO")

    return ok_art, {
        "checks": checks,
        "artifact_integrity": "GO" if ok_art else "NO_GO",
        "trial_phase_verdict": trial_phase_verdict,
        "final_recommendation": summ.get("final_recommendation"),
        "windows_executed": wre,
        "stop_reason": summ.get("stop_reason"),
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
