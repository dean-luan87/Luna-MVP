#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-Mainline-GuardedTrial-004 — Freeze weight/deps/input/env/runbook and emit 10-frame approval gate (no execution).
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

from capabilities.guarded_trial.yolo_stage1_dependency_snapshot_v0 import (
    PHASE,
    run_yolo_stage1_dependency_snapshot_v0,
    validate_yolo_dependency_snapshot_v0,
    validate_yolo_weight_snapshot_v0,
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


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--static-config-root", required=True)
    ap.add_argument("--output-root", default="")
    ap.add_argument("--input-video", default="", help="Offline video file path (never opened in this phase)")
    args = ap.parse_args()

    repo = Path(REPO_ROOT)
    cfg_root = Path(args.static_config_root)
    if not cfg_root.is_absolute():
        cfg_root = (repo / cfg_root).resolve()
    else:
        cfg_root = cfg_root.resolve()

    out = Path(args.output_root) if args.output_root else repo / "logs" / f"yolo_stage1_10_frame_approval_gate_004_{_utc_tag()}"

    if not cfg_root.is_dir():
        print(json.dumps({"ok": False, "error": "static_config_root_not_readable", "path": str(cfg_root)}, ensure_ascii=False))
        return 2

    runbook_p = cfg_root / "yolo_stage1_10_frame_dry_run_runbook.json"
    if not runbook_p.is_file():
        print(json.dumps({"ok": False, "error": "missing_runbook_in_static_config_root", "path": str(runbook_p)}, ensure_ascii=False))
        return 2

    inp_video = args.input_video.strip() or None
    snap = run_yolo_stage1_dependency_snapshot_v0(
        repo_root=repo,
        static_config_root=cfg_root,
        input_video_path=inp_video,
    )

    weights_only = validate_yolo_weight_snapshot_v0(repo_root=repo)
    deps_only = validate_yolo_dependency_snapshot_v0()
    summary: Dict[str, Any] = {
        "phase": PHASE,
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "repo_root": str(repo.resolve()),
        "output_root": str(out.resolve()),
        "static_config_root": str(cfg_root),
        "snapshot_id": snap.get("snapshot_id"),
        "approval_gate_result": snap.get("approval_gate_result"),
        "blockers": snap.get("blockers"),
        "warnings": snap.get("warnings"),
        "yolo_stage1_trial_preparation_status": snap.get("yolo_stage1_trial_preparation_status"),
        "real_yolo_execution": snap.get("real_yolo_execution"),
        "ten_frame_dry_run_execution": snap.get("ten_frame_dry_run_execution"),
        "real_yolo_execution_allowed_by_this_phase": snap.get("real_yolo_execution_allowed_by_this_phase"),
        "ten_frame_dry_run_allowed_by_this_phase": snap.get("ten_frame_dry_run_allowed_by_this_phase"),
        "hard_audit": snap.get("hard_audit"),
    }

    detector_ep = snap.get("detector_entrypoint") or {}
    gate_report = dict(snap)
    gate_report["input_video_cli"] = inp_video

    _write_json(out / "yolo_stage1_10_frame_approval_summary.json", summary)
    _write_json(
        out / "yolo_stage1_weight_snapshot.json",
        {
            **weights_only,
            "weights_summary": snap.get("weights"),
            "frozen_at_repo": str(repo.resolve()),
        },
    )
    _write_json(out / "yolo_stage1_dependency_snapshot.json", {"dependencies": deps_only})
    _write_json(out / "yolo_stage1_detector_entrypoint_snapshot.json", detector_ep)
    _write_json(out / "yolo_stage1_input_source_snapshot.json", snap.get("input_source") or {})
    _write_json(out / "yolo_stage1_env_flag_snapshot.json", {"env_flags_for_next_phase": snap.get("env_flags_for_next_phase")})
    _write_json(out / "yolo_stage1_abort_rollback_snapshot.json", snap.get("abort_rollback_snapshot") or {})
    _write_json(out / "yolo_stage1_10_frame_approval_gate_report.json", gate_report)

    _append_jsonl(
        out / "yolo_stage1_10_frame_approval_trace.jsonl",
        {"type": "yolo_stage1_approval_trace_v0", "snapshot_id": snap.get("snapshot_id"), "phase": PHASE},
    )
    _append_jsonl(
        out / "yolo_stage1_10_frame_approval_replay.jsonl",
        {"type": "yolo_stage1_approval_replay_v0", "approval_gate_result": snap.get("approval_gate_result")},
    )
    _append_jsonl(
        out / "yolo_stage1_10_frame_approval_whitebox.jsonl",
        {
            "type": "yolo_stage1_approval_whitebox_v0",
            "no_inference": True,
            "hard_audit": snap.get("hard_audit"),
        },
    )

    notes = [
        f"# {PHASE} — 10-frame dry-run approval gate (freeze only)",
        "",
        f"- static_config_root: `{cfg_root}`",
        f"- output_root: `{out}`",
        "- No detector, no inference, no camera, no VideoCapture.",
        "",
    ]
    (out / "approval_notes.md").write_text("\n".join(notes), encoding="utf-8")

    print(
        json.dumps(
            {"ok": True, "output_root": str(out), "approval_gate_result": snap.get("approval_gate_result")},
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
