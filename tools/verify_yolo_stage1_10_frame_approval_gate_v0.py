#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verify Phase-Mainline-GuardedTrial-004 approval gate outputs.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

EXPECTED = [
    "yolo_stage1_10_frame_approval_summary.json",
    "yolo_stage1_weight_snapshot.json",
    "yolo_stage1_dependency_snapshot.json",
    "yolo_stage1_detector_entrypoint_snapshot.json",
    "yolo_stage1_input_source_snapshot.json",
    "yolo_stage1_env_flag_snapshot.json",
    "yolo_stage1_abort_rollback_snapshot.json",
    "yolo_stage1_10_frame_approval_gate_report.json",
    "yolo_stage1_10_frame_approval_trace.jsonl",
    "yolo_stage1_10_frame_approval_replay.jsonl",
    "yolo_stage1_10_frame_approval_whitebox.jsonl",
    "approval_notes.md",
]


def _load(p: Path) -> Any:
    return json.loads(p.read_text(encoding="utf-8"))


def _nonempty_jsonl(p: Path) -> bool:
    return p.is_file() and bool(p.read_text(encoding="utf-8").strip())


def verify(*, output_root: Path) -> Tuple[bool, Dict[str, Any]]:
    checks: Dict[str, Any] = {}
    ok_all = True

    for name in EXPECTED:
        key = f"A_file_{name}"
        checks[key] = (output_root / name).is_file()
        if not checks[key]:
            ok_all = False

    summ = _load(output_root / "yolo_stage1_10_frame_approval_summary.json") if (output_root / "yolo_stage1_10_frame_approval_summary.json").is_file() else {}
    ha = summ.get("hard_audit") or {}
    wpath = output_root / "yolo_stage1_weight_snapshot.json"
    wj = _load(wpath) if wpath.is_file() else {}

    scr = summ.get("static_config_root")
    checks["B_static_config_root_readable"] = isinstance(scr, str) and Path(scr).is_dir()
    checks["C_weight_snapshot_exists"] = wpath.is_file()

    exists = bool(wj.get("exists"))
    sha = wj.get("sha256") or (wj.get("weights") or {}).get("sha256")
    checks["D_weight_hash_present_when_exists"] = (not exists) or (isinstance(sha, str) and len(sha) == 64)

    checks["E_dependency_snapshot_exists"] = (output_root / "yolo_stage1_dependency_snapshot.json").is_file()
    checks["F_detector_entrypoint_snapshot_exists"] = (output_root / "yolo_stage1_detector_entrypoint_snapshot.json").is_file()
    checks["G_input_source_snapshot_exists"] = (output_root / "yolo_stage1_input_source_snapshot.json").is_file()
    checks["H_env_flag_snapshot_exists"] = (output_root / "yolo_stage1_env_flag_snapshot.json").is_file()
    checks["I_abort_rollback_snapshot_exists"] = (output_root / "yolo_stage1_abort_rollback_snapshot.json").is_file()
    checks["J_approval_gate_report_exists"] = (output_root / "yolo_stage1_10_frame_approval_gate_report.json").is_file()

    checks["K_detector_invoked_false"] = ha.get("detector_invoked") is False
    checks["L_model_inference_invoked_false"] = ha.get("model_inference_invoked") is False
    checks["M_camera_invoked_false"] = ha.get("camera_invoked") is False
    checks["N_video_stream_opened_false"] = ha.get("video_stream_opened") is False
    checks["O_downstream_zero"] = int(ha.get("downstream_invocation_count") or 0) == 0
    checks["P_navigation_null"] = ha.get("navigation_action") is None
    checks["Q_world_write_false"] = ha.get("world_write_invoked") is False
    checks["R_ten_frame_not_allowed_this_phase"] = summ.get("ten_frame_dry_run_allowed_by_this_phase") is False

    checks["S_trace_replay_whitebox_nonempty"] = (
        _nonempty_jsonl(output_root / "yolo_stage1_10_frame_approval_trace.jsonl")
        and _nonempty_jsonl(output_root / "yolo_stage1_10_frame_approval_replay.jsonl")
        and _nonempty_jsonl(output_root / "yolo_stage1_10_frame_approval_whitebox.jsonl")
    )

    for k, v in checks.items():
        if k.startswith("A_file_"):
            continue
        if v is False:
            ok_all = False

    return ok_all, {"verdict": "GO" if ok_all else "NO_GO", "checks": checks, "output_root": str(output_root)}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-root", required=True)
    args = ap.parse_args()
    out = Path(args.output_root).resolve()
    ok, report = verify(output_root=out)
    print(json.dumps({"ok": ok, **report}, ensure_ascii=False, indent=2))
    return 0 if ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
