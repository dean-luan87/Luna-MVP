#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verify Phase-Mainline-GuardedTrial-003 static config validation outputs.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

EXPECTED = [
    "yolo_stage1_static_config_summary.json",
    "yolo_stage1_detector_entrypoint_matrix.json",
    "yolo_stage1_frame_source_candidate_matrix.json",
    "yolo_stage1_model_config_candidate_matrix.json",
    "yolo_stage1_detection_schema_validation.json",
    "yolo_stage1_trw_output_contract_validation.json",
    "yolo_stage1_10_frame_dry_run_runbook.json",
    "yolo_stage1_static_config_trace.jsonl",
    "yolo_stage1_static_config_replay.jsonl",
    "yolo_stage1_static_config_whitebox.jsonl",
    "validation_notes.md",
]


def _load(p: Path) -> Any:
    return json.loads(p.read_text(encoding="utf-8"))


def _jsonl_nonempty(p: Path) -> bool:
    return p.is_file() and bool(p.read_text(encoding="utf-8").strip())


def verify(*, output_root: Path) -> Tuple[bool, Dict[str, Any]]:
    checks: Dict[str, Any] = {}
    ok_all = True

    for name in EXPECTED:
        key = f"A_file_{name}"
        checks[key] = (output_root / name).is_file()
        if not checks[key]:
            ok_all = False

    summ_path = output_root / "yolo_stage1_static_config_summary.json"
    ha = {}
    if summ_path.is_file():
        sm = _load(summ_path)
        ha = sm.get("hard_audit") or {}

    checks["B_detector_matrix_exists"] = (output_root / "yolo_stage1_detector_entrypoint_matrix.json").is_file()
    checks["C_frame_matrix_exists"] = (output_root / "yolo_stage1_frame_source_candidate_matrix.json").is_file()
    checks["D_model_matrix_exists"] = (output_root / "yolo_stage1_model_config_candidate_matrix.json").is_file()
    checks["E_schema_validation_exists"] = (output_root / "yolo_stage1_detection_schema_validation.json").is_file()
    checks["F_trw_contract_exists"] = (output_root / "yolo_stage1_trw_output_contract_validation.json").is_file()
    checks["G_runbook_exists"] = (output_root / "yolo_stage1_10_frame_dry_run_runbook.json").is_file()

    checks["H_detector_invoked_false"] = ha.get("detector_invoked") is False
    checks["I_camera_invoked_false"] = ha.get("camera_invoked") is False
    checks["J_video_stream_opened_false"] = ha.get("video_stream_opened") is False
    checks["K_downstream_zero"] = int(ha.get("downstream_invocation_count") or 0) == 0
    checks["L_navigation_null"] = ha.get("navigation_action") is None
    checks["M_world_write_false"] = ha.get("world_write_invoked") is False

    checks["N_trace_replay_whitebox_nonempty"] = (
        _jsonl_nonempty(output_root / "yolo_stage1_static_config_trace.jsonl")
        and _jsonl_nonempty(output_root / "yolo_stage1_static_config_replay.jsonl")
        and _jsonl_nonempty(output_root / "yolo_stage1_static_config_whitebox.jsonl")
    )

    sm = _load(summ_path) if summ_path.is_file() else {}
    checks["O_no_ocr_qwen_downstream_activated"] = sm.get("ocr_entry_active_env") is False and sm.get("qwen_entry_active_env") is False

    verdict = sm.get("verdict") or {}
    checks["P_no_real_trial_execution"] = verdict.get("real_yolo_execution") == "NO_GO"

    for k, v in checks.items():
        if k.startswith("A_file_"):
            continue
        if not v:
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
