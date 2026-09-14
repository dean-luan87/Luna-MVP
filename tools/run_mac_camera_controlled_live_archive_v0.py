#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-DeviceEnv-003
CLI entry: Mac camera live input -> RealScene archive_root required_files (Fix-001 compatible).

This tool runs a short, timeboxed capture for evidence generation only.
It does NOT run a full controlled trial and does NOT enable any execution authority.
"""

from __future__ import annotations

import argparse
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from capabilities.device_env.mac_camera_archive_adapter_v0 import (
    RunParams,
    run_mac_camera_controlled_live_archive_v0,
)


def _die(msg: str, code: int = 2) -> None:
    print(msg, file=sys.stderr)
    raise SystemExit(code)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--archive-root", required=True)
    ap.add_argument("--operator-id", required=True)
    ap.add_argument("--safety-observer-id", required=True)
    ap.add_argument("--record-owner-id", required=True)
    ap.add_argument("--timebox-ms", required=True, type=int)
    ap.add_argument("--camera-index", required=True, type=int)
    ap.add_argument("--explicit-entry-token", required=True)
    args = ap.parse_args()

    archive_root = str(args.archive_root)
    if not archive_root.strip():
        _die("ERROR: --archive-root empty")
    if not str(args.operator_id).strip():
        _die("ERROR: --operator-id empty")
    if not str(args.safety_observer_id).strip():
        _die("ERROR: --safety-observer-id empty")
    if not str(args.record_owner_id).strip():
        _die("ERROR: --record-owner-id empty")
    if not str(args.explicit_entry_token).strip():
        _die("ERROR: --explicit-entry-token empty")

    # Must be empty directory or nonexistent (prevent overwriting/merging evidence)
    if os.path.exists(archive_root):
        if not os.path.isdir(archive_root):
            _die("ERROR: archive_root exists but is not a directory")
        if os.listdir(archive_root):
            _die("ERROR: archive_root must be empty (refusing to merge evidence)")

    params = RunParams(
        archive_root=archive_root,
        operator_id=str(args.operator_id),
        safety_observer_id=str(args.safety_observer_id),
        record_owner_id=str(args.record_owner_id),
        timebox_ms=int(args.timebox_ms),
        camera_index=int(args.camera_index),
        explicit_entry_token=str(args.explicit_entry_token),
    )

    try:
        res = run_mac_camera_controlled_live_archive_v0(params)
    except Exception as e:
        _die(f"ERROR: adapter_failed: {type(e).__name__}: {e}", code=3)

    # Print structured summary (do not claim validator-go here)
    print(
        json.dumps(
            {
                "tool": "run_mac_camera_controlled_live_archive_v0",
                "phase": "Phase-DeviceEnv-003",
                "archive_root": res.archive_root,
                "run_id": res.run_id,
                "overall_run_status": res.overall_run_status,
                "camera_opened": res.camera_opened,
                "frame_count": res.frame_count,
                "start_time_ms": res.start_time_ms,
                "end_time_ms": res.end_time_ms,
                "failure_reason": res.failure_reason,
                "assertions": {
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

    # Exit code: 0 only for completed capture; failures are non-zero.
    if res.overall_run_status != "completed":
        raise SystemExit(10)


if __name__ == "__main__":
    main()

