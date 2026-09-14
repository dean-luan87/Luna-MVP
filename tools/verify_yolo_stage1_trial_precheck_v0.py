#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verify Phase-Mainline-GuardedTrial-002 YOLO Stage-1 precheck outputs.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

EXPECTED = [
    "yolo_stage1_trial_precheck_summary.json",
    "yolo_stage1_trial_env_snapshot.json",
    "yolo_stage1_trial_precheck_result.json",
    "yolo_stage1_trial_runner_skeleton.json",
    "yolo_stage1_trial_abort_rollback_plan.json",
    "yolo_stage1_trial_trace.jsonl",
    "yolo_stage1_trial_replay.jsonl",
    "yolo_stage1_trial_whitebox.jsonl",
    "precheck_notes.md",
]


def _load(p: Path) -> Any:
    return json.loads(p.read_text(encoding="utf-8"))


def _jsonl_nonempty(p: Path) -> bool:
    if not p.is_file():
        return False
    return bool(p.read_text(encoding="utf-8").strip())


def verify(*, output_root: Path) -> Tuple[bool, Dict[str, Any]]:
    checks: Dict[str, Any] = {}
    ok_all = True

    for name in EXPECTED:
        checks[f"A_file_{name}"] = (output_root / name).is_file()
        if not checks[f"A_file_{name}"]:
            ok_all = False

    pr_path = output_root / "yolo_stage1_trial_precheck_result.json"
    rs_path = output_root / "yolo_stage1_trial_runner_skeleton.json"
    ar_path = output_root / "yolo_stage1_trial_abort_rollback_plan.json"
    sm_path = output_root / "yolo_stage1_trial_precheck_summary.json"

    checks["B_precheck_result_exists"] = pr_path.is_file()
    checks["C_runner_skeleton_exists"] = rs_path.is_file()

    sm = _load(sm_path) if sm_path.is_file() else {}
    pr = _load(pr_path) if pr_path.is_file() else {}
    rs = _load(rs_path) if rs_path.is_file() else {}
    ar = _load(ar_path) if ar_path.is_file() else {}

    env_path = output_root / "yolo_stage1_trial_env_snapshot.json"
    env = _load(env_path) if env_path.is_file() else {}
    checks["D_global_kill_switch_represented"] = "LUNA_DISABLE_ALL_GUARDED_TRIALS" in json.dumps(env, ensure_ascii=False)

    checks["E_entry_flag_default_false"] = pr.get("entry_flag_enabled") is False

    ha = pr.get("hard_audit") or {}
    checks["F_detector_invoked_false"] = pr.get("detector_invoked") is False
    checks["G_camera_invoked_false"] = pr.get("camera_invoked") is False
    checks["H_would_execute_detector_false"] = pr.get("would_execute_detector") is False
    checks["I_provider_invoked_false"] = ha.get("provider_invoked") is False
    checks["J_playback_invoked_false"] = ha.get("playback_invoked") is False
    checks["K_downstream_invocation_zero"] = int(ha.get("downstream_invocation_count") or 0) == 0
    checks["L_navigation_action_null"] = ha.get("navigation_action") is None
    checks["M_world_write_invoked_false"] = ha.get("world_write_invoked") is False

    rp = ar.get("rollback_plan") if isinstance(ar, dict) else {}
    checks["N_rollback_plan_exists"] = isinstance(rp, dict) and rp.get("rollback_action") == "disable_yolo_trial" and bool(
        rp.get("commands")
    )

    checks["O_abort_conditions_registered"] = isinstance(ar.get("abort_evaluation"), dict)

    checks["P_trace_replay_whitebox_nonempty"] = (
        _jsonl_nonempty(output_root / "yolo_stage1_trial_trace.jsonl")
        and _jsonl_nonempty(output_root / "yolo_stage1_trial_replay.jsonl")
        and _jsonl_nonempty(output_root / "yolo_stage1_trial_whitebox.jsonl")
    )

    checks["Q_no_ocr_qwen_trial_active"] = sm.get("ocr_entry_active") is False and sm.get("qwen_entry_active") is False

    checks["R_no_real_trial_execution"] = sm.get("real_trial_execution") is False and rs.get(
        "execution_result"
    ) == "not_executed_skeleton_only"

    for k, v in checks.items():
        if not k.startswith("A_file_") and k != "A_files_all":
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
