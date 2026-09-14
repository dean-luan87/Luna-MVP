#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-Mainline-GuardedTrial-002 — Run YOLO Stage-1 dry-run precheck (no detector, no camera).

Writes summary, env snapshot, precheck result, runner skeleton, rollback plan, jsonl artifacts.
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

from capabilities.guarded_trial.yolo_stage1_trial_precheck_v0 import (
    YoloStage1TrialPrecheckInput,
    read_yolo_stage1_trial_env_snapshot_v0,
    run_yolo_stage1_trial_precheck_v0,
    validate_yolo_stage1_trial_preconditions_v0,
    build_yolo_stage1_trial_id_v0,
    build_yolo_stage1_rollback_plan_v0,
)
from capabilities.guarded_trial.yolo_stage1_trial_runner_skeleton_v0 import (
    run_yolo_stage1_trial_runner_skeleton_v0,
)
from capabilities.runtime_readiness.guarded_trial_abort_rollback_hooks_v0 import (
    evaluate_guarded_trial_abort_conditions_v0,
)

PHASE = "Phase-Mainline-GuardedTrial-002"


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
    ap.add_argument("--output-root", default="")
    args = ap.parse_args()

    repo = Path(REPO_ROOT)
    out = Path(args.output_root) if args.output_root else repo / "logs" / f"yolo_stage1_trial_precheck_002_{_utc_tag()}"
    out.mkdir(parents=True, exist_ok=True)

    rt_dir = out / "request_trace"
    trw_dir = out / "trace_replay_whitebox"
    trw_payload: Dict[str, Any] = {
        "request_id": "yolo_stage1_precheck_req",
        "hard_audit": {"phase": "GuardedTrial-002", "precheck_only": True},
        "runtime_run_id": "yolo_stage1_precheck_run",
        "pending_ref": True,
    }

    inp = YoloStage1TrialPrecheckInput(
        output_root=str(out.resolve()),
        request_trace_dir=str(rt_dir.resolve()),
        trace_replay_whitebox_dir=str(trw_dir.resolve()),
        trw_payload=trw_payload,
        env_override=None,
    )

    trial_id = build_yolo_stage1_trial_id_v0()
    result = run_yolo_stage1_trial_precheck_v0(inp, trial_id=trial_id)
    env_snap = read_yolo_stage1_trial_env_snapshot_v0(None)

    pre_mid = validate_yolo_stage1_trial_preconditions_v0(inp, trial_id=trial_id)
    gate_decision = (pre_mid.get("gate_decision") or {}).get("decision") or "disabled"
    abort_eval = evaluate_guarded_trial_abort_conditions_v0(
        gate_decision=str(gate_decision),
        trial_capability="yolo",
        signals={},
    )
    rollback_plan = build_yolo_stage1_rollback_plan_v0(gate_decision=str(gate_decision))

    runner = run_yolo_stage1_trial_runner_skeleton_v0(trial_id=trial_id, max_frames_planned=10)

    summary: Dict[str, Any] = {
        "phase": PHASE,
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "repo_root": str(repo.resolve()),
        "output_root": str(out.resolve()),
        "trial_id": trial_id,
        "precheck_result": result.precheck_result,
        "real_trial_execution": False,
        "detector_invoked": False,
        "camera_invoked": False,
        "ocr_entry_active": bool(pre_mid.get("ocr_entry_active")),
        "qwen_entry_active": bool(pre_mid.get("qwen_entry_active")),
        "constraints": {
            "no_detector": True,
            "no_camera": True,
            "no_ocr_midplatform_downstream": True,
            "no_playback_tts_qwen": True,
        },
        "verdict": {
            "precheck": result.precheck_result,
            "runner_skeleton": "GO",
            "real_yolo_trial": "NO_GO",
        },
    }

    _write_json(out / "yolo_stage1_trial_precheck_summary.json", summary)
    _write_json(out / "yolo_stage1_trial_env_snapshot.json", env_snap.to_dict())
    _write_json(out / "yolo_stage1_trial_precheck_result.json", result.to_dict())
    _write_json(out / "yolo_stage1_trial_runner_skeleton.json", runner)
    _write_json(
        out / "yolo_stage1_trial_abort_rollback_plan.json",
        {"abort_evaluation": abort_eval, "rollback_plan": rollback_plan},
    )

    _append_jsonl(
        out / "yolo_stage1_trial_trace.jsonl",
        {"type": "yolo_stage1_precheck_trace_v0", "trial_id": trial_id, "phase": PHASE},
    )
    _append_jsonl(
        out / "yolo_stage1_trial_replay.jsonl",
        {"type": "yolo_stage1_precheck_replay_v0", "trial_id": trial_id, "precheck_result": result.precheck_result},
    )
    _append_jsonl(
        out / "yolo_stage1_trial_whitebox.jsonl",
        {
            "type": "yolo_stage1_precheck_whitebox_v0",
            "trial_id": trial_id,
            "why_no_detector": True,
            "hard_audit": result.hard_audit,
        },
    )

    notes = [
        f"# {PHASE} — YOLO Stage-1 dry-run precheck",
        "",
        f"- output_root: `{out}`",
        "- No detector invocation; no camera frame ingestion.",
        "",
    ]
    (out / "precheck_notes.md").write_text("\n".join(notes), encoding="utf-8")

    print(json.dumps({"ok": True, "output_root": str(out), "precheck_result": result.precheck_result}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
