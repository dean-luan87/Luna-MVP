#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-Mainline-GuardedTrial-006 — Serial multi-window offline YOLO slice trial (50 / 100 / 200), gated.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

_TOOLS = Path(__file__).resolve().parent
REPO_ROOT = str(_TOOLS.parent)
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from capabilities.guarded_trial.yolo_stage1_multi_window_executor_v0 import (  # noqa: E402
    PHASE,
    run_yolo_stage1_multi_window_offline_slice_trial_v0,
)


def _utc_tag() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%SZ")


def _write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")


def _append_jsonl(path: Path, row: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def _parse_windows(s: str) -> List[int]:
    return [int(p.strip()) for p in (s or "").split(",") if p.strip()]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--baseline-10-root", required=True, help="Phase-005 10-frame execution directory (dry-run summary)")
    ap.add_argument("--input-video", required=True, help="Same offline video as baseline (.mp4/.mov/.mkv/.avi)")
    ap.add_argument("--windows", default="50,100", help="Comma list; must be prefix chain of 50,100,200 (default 50,100)")
    ap.add_argument("--approval-root", default="", help="Optional Phase-004 root (passed through to executor)")
    ap.add_argument("--output-root", default="")
    args = ap.parse_args()

    repo = Path(REPO_ROOT).resolve()
    bl = Path(args.baseline_10_root.strip()).expanduser()
    if not bl.is_absolute():
        bl = (repo / bl).resolve()
    else:
        bl = bl.resolve()

    out = Path(args.output_root) if args.output_root.strip() else repo / "logs" / f"yolo_stage1_multi_window_offline_trial_006_{_utc_tag()}"
    if not out.is_absolute():
        out = (repo / out).resolve()
    else:
        out = out.resolve()

    windows = _parse_windows(args.windows)
    appr = Path(args.approval_root.strip()).expanduser() if args.approval_root.strip() else None
    if appr is not None:
        appr = appr.resolve() if appr.is_absolute() else (repo / appr).resolve()
        appr = appr if appr.is_dir() else None

    def _must_write(kind: str, fn, *a, **k):
        try:
            fn(*a, **k)
        except Exception as e:  # noqa: BLE001
            print(json.dumps({"ok": False, "error": f"{kind}_write_failed", "detail": str(e)}, ensure_ascii=False))
            raise SystemExit(2) from e

    out.mkdir(parents=True, exist_ok=True)

    result = run_yolo_stage1_multi_window_offline_slice_trial_v0(
        repo_root=repo,
        baseline_10_root=bl,
        input_video_path=args.input_video.strip(),
        windows=windows,
        approval_root=appr,
    )

    plan = result.get("plan") or {}
    summ = result.get("summary") or {}
    reports: Dict[int, Dict[str, Any]] = dict(result.get("window_reports") or {})

    vid_path = ""
    ig = result.get("input_gate") or {}
    if ig.get("video_validation"):
        vid_path = ig["video_validation"].get("path_resolved") or ""

    latency_rows: Dict[str, Any] = {str(k): {"window_frames": k, **(v.get("latency") or {})} for k, v in reports.items()}
    schema_rows: Dict[str, Any] = {
        str(k): {
            "window_frames": k,
            "schema_valid_count": v.get("schema_valid_count"),
            "schema_invalid_count": v.get("schema_invalid_count"),
            "detector_error_count": v.get("detector_error_count"),
        }
        for k, v in reports.items()
    }
    abort_roll = {
        "stop_reason": summ.get("stop_reason"),
        "windows_executed": summ.get("windows_executed"),
        "per_window": {str(k): {"abort_triggered": v.get("abort_triggered"), "abort_reason": v.get("abort_reason")} for k, v in reports.items()},
    }
    ha_sum = {
        "all_hard_audit_ok": summ.get("all_hard_audit_ok"),
        "side_effect_detected": summ.get("side_effect_detected"),
        "per_window": {str(k): v.get("hard_audit") for k, v in reports.items()},
    }

    _must_write("json", _write_json, out / "yolo_stage1_multi_window_summary.json", summ)
    _must_write("json", _write_json, out / "yolo_stage1_multi_window_plan.json", {**plan, "multi_window_trial_id": result.get("multi_window_trial_id")})
    _must_write("json", _write_json, out / "yolo_stage1_multi_window_full_result.json", result)

    for w in (50, 100, 200):
        p = out / f"yolo_stage1_window_{w}_report.json"
        if w in reports:
            _must_write("json", _write_json, p, reports[w])
        else:
            placeholder = {"window_frames": w, "executed": False, "note": "skipped_or_not_requested"}
            _must_write("json", _write_json, p, placeholder)

    _must_write("json", _write_json, out / "yolo_stage1_multi_window_latency_summary.json", latency_rows)
    _must_write("json", _write_json, out / "yolo_stage1_multi_window_schema_validation_summary.json", schema_rows)
    _must_write("json", _write_json, out / "yolo_stage1_multi_window_abort_rollback_report.json", abort_roll)
    _must_write("json", _write_json, out / "yolo_stage1_multi_window_hard_audit_summary.json", ha_sum)

    mw_tid = result.get("multi_window_trial_id", "unknown")
    _must_write(
        "jsonl",
        _append_jsonl,
        out / "yolo_stage1_multi_window_trace.jsonl",
        {"type": "yolo_multi_window_trace_v0", "trial_id": mw_tid, "phase": PHASE, "windows_executed": summ.get("windows_executed")},
    )
    _must_write(
        "jsonl",
        _append_jsonl,
        out / "yolo_stage1_multi_window_replay.jsonl",
        {
            "type": "yolo_multi_window_replay_v0",
            "trial_id": mw_tid,
            "windows_requested": summ.get("windows_requested"),
            "baseline_10_root": str(bl),
            "input_video_resolved": vid_path,
        },
    )
    _must_write(
        "jsonl",
        _append_jsonl,
        out / "yolo_stage1_multi_window_whitebox.jsonl",
        {
            "type": "yolo_multi_window_whitebox_v0",
            "trial_id": mw_tid,
            "gates": {"50_before_100": True, "100_before_200": True, "conditional_stops_upgrade": True},
            "final_recommendation": summ.get("final_recommendation"),
        },
    )

    notes = [
        f"# {PHASE}",
        "",
        f"- baseline_10_root: `{bl}`",
        f"- output_root: `{out}`",
        f"- windows: `{args.windows.strip()}`",
        "",
        "串行逐级门控：50 GO → 100；100 GO → 200。任一 NO_GO 或 CONDITIONAL_GO 立即停止更大窗口。",
        "",
    ]
    def _write_notes() -> None:
        (out / "execution_notes.md").write_text("\n".join(notes), encoding="utf-8")

    _must_write("md", _write_notes)

    final_go = summ.get("final_recommendation") == "GO_next_phase"
    print(
        json.dumps(
            {
                "ok": True,
                "output_root": str(out),
                "multi_window_trial_id": mw_tid,
                "final_recommendation": summ.get("final_recommendation"),
                "windows_executed": summ.get("windows_executed"),
                "stop_reason": summ.get("stop_reason"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if final_go else 3


if __name__ == "__main__":
    raise SystemExit(main())
