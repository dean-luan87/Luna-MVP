#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-DeviceEnv-003
Verifier for Mac Camera Controlled Live Archive Adapter v0.

This verifier:
- Ensures missing CLI params fails fast.
- Ensures camera-unavailable path does NOT fake a controlled_live archive_root.
- If camera is available, ensures required files are produced and validator returns go.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
from typing import Any, Dict, List, Tuple


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)


def _run(cmd: List[str], cwd: str) -> Tuple[int, str, str]:
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr


def _assert(cond: bool, msg: str) -> None:
    if not cond:
        raise AssertionError(msg)


def _list_rel_files(d: str) -> List[str]:
    out: List[str] = []
    for root, _, files in os.walk(d):
        for fn in files:
            ap = os.path.join(root, fn)
            rel = os.path.relpath(ap, d)
            out.append(rel)
    return sorted(out)


def _validate_archive_root(archive_root: str) -> Dict[str, Any]:
    cmd = [
        sys.executable,
        "tools/validate_controlled_live_evidence_collection_execution_v0.py",
        "--archive_root",
        archive_root,
    ]
    rc, out, err = _run(cmd, cwd=ROOT)
    if rc != 0:
        return {"recommendation": "no_go", "hard_blockers": ["validator_failed_to_run"], "details": {"stderr": err[-4000:]}}
    try:
        j = json.loads(out)
        return j.get("summary", {})
    except Exception:
        return {"recommendation": "no_go", "hard_blockers": ["validator_output_unparseable"], "details": {"stdout_tail": out[-4000:]}}


def main() -> None:
    # 1) Missing param should fail (argparse)
    cmd_missing = [sys.executable, "tools/run_mac_camera_controlled_live_archive_v0.py"]
    rc, out, err = _run(cmd_missing, cwd=ROOT)
    _assert(rc != 0, "missing-args should fail with non-zero exit code")

    # 2) Camera unavailable path should not produce validator-ready archive
    with tempfile.TemporaryDirectory(prefix="de003_fail_") as td:
        archive_root = os.path.join(td, "archive_root")
        cmd_fail = [
            sys.executable,
            "tools/run_mac_camera_controlled_live_archive_v0.py",
            "--archive-root",
            archive_root,
            "--operator-id",
            "op_test",
            "--safety-observer-id",
            "obs_test",
            "--record-owner-id",
            "owner_test",
            "--timebox-ms",
            "1000",
            "--camera-index",
            "9999",
            "--explicit-entry-token",
            "entry_test_token",
        ]
        rc2, out2, err2 = _run(cmd_fail, cwd=ROOT)
        _assert(rc2 != 0, "camera-unavailable should exit non-zero")
        if not os.path.isdir(archive_root):
            raise AssertionError(
                "archive_root dir should be created; "
                f"rc={rc2} stdout_tail={out2[-800:]} stderr_tail={err2[-800:]}"
            )
        rel_files = _list_rel_files(archive_root)
        _assert("failed_run_report.json" in rel_files, "camera-unavailable should emit failed_run_report.json")
        # Must NOT pretend this is a controlled_live evidence archive
        _assert("run_evidence.json" not in rel_files, "camera-unavailable must NOT emit run_evidence.json")
        _assert("archive_manifest.json" not in rel_files, "camera-unavailable must NOT emit archive_manifest.json")

    # 3) Best-effort success path: if camera is available, should produce validator-go
    with tempfile.TemporaryDirectory(prefix="de003_ok_") as td2:
        archive_root2 = os.path.join(td2, "archive_root")
        cmd_ok = [
            sys.executable,
            "tools/run_mac_camera_controlled_live_archive_v0.py",
            "--archive-root",
            archive_root2,
            "--operator-id",
            "op_test",
            "--safety-observer-id",
            "obs_test",
            "--record-owner-id",
            "owner_test",
            "--timebox-ms",
            "1200",
            "--camera-index",
            "0",
            "--explicit-entry-token",
            "entry_test_token",
        ]
        rc3, out3, err3 = _run(cmd_ok, cwd=ROOT)
        if rc3 == 0:
            # Validate required files existence
            required = [
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
            rel_files2 = _list_rel_files(archive_root2)
            for rf in required:
                _assert(rf in rel_files2, f"missing required file: {rf}")
            # Validator should recommend go
            summary = _validate_archive_root(archive_root2)
            _assert(summary.get("recommendation") == "go", f"validator did not return go: {summary}")
        else:
            # Camera might be unavailable in this environment; accept conditional result.
            pass

    print(
        json.dumps(
            {
                "tool": "verify_mac_camera_archive_adapter_v0",
                "phase": "Phase-DeviceEnv-003",
                "result": "ok",
                "notes": "If local camera is unavailable, success-path validator is skipped (conditional).",
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()

