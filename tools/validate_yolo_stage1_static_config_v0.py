#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-Mainline-GuardedTrial-003 — Run YOLO Stage-1 static config validation (no detector, no camera).
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

from capabilities.guarded_trial.yolo_stage1_static_config_validator_v0 import (
    PHASE,
    run_yolo_stage1_static_config_validation_v0,
)
from capabilities.runtime_readiness.guarded_trial_gate_v0 import read_guarded_trial_env_snapshot_v0


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
    out = Path(args.output_root) if args.output_root else repo / "logs" / f"yolo_stage1_static_config_validation_003_{_utc_tag()}"
    out.mkdir(parents=True, exist_ok=True)

    full = run_yolo_stage1_static_config_validation_v0(repo_root=repo)
    det = full.pop("detector_entrypoint_matrix")
    frame = full.pop("frame_source_candidate_matrix")
    model = full.pop("model_config_candidate_matrix")
    schema = full.pop("detection_schema_validation")
    trw = full.pop("trw_output_contract_validation")
    runbook = full.pop("dry_run_10_frame_runbook")

    snap = read_guarded_trial_env_snapshot_v0(None)
    ocr_on = (snap.LUNA_ENABLE_OCR_GUARDED_TRIAL_V1 or "").strip().lower() in {"1", "true", "yes", "on"}
    qwen_on = (snap.LUNA_ENABLE_QWEN_VOICE_GUARDED_TRIAL_V1 or "").strip().lower() in {"1", "true", "yes", "on"}

    summary: Dict[str, Any] = {
        "phase": PHASE,
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "repo_root": str(repo.resolve()),
        "output_root": str(out.resolve()),
        "validation_id": full.get("validation_id"),
        "static_validation_result": full.get("static_validation_result"),
        "blockers": full.get("blockers"),
        "warnings": full.get("warnings"),
        "hard_audit": full.get("hard_audit"),
        "ocr_entry_active_env": ocr_on,
        "qwen_entry_active_env": qwen_on,
        "verdict": {
            "static_config": full.get("static_validation_result"),
            "real_yolo_execution": "NO_GO",
            "ten_frame_dry_run_execution": "NO_GO",
        },
    }

    _write_json(out / "yolo_stage1_static_config_summary.json", summary)
    _write_json(out / "yolo_stage1_detector_entrypoint_matrix.json", det)
    _write_json(out / "yolo_stage1_frame_source_candidate_matrix.json", frame)
    _write_json(out / "yolo_stage1_model_config_candidate_matrix.json", model)
    _write_json(out / "yolo_stage1_detection_schema_validation.json", schema)
    _write_json(out / "yolo_stage1_trw_output_contract_validation.json", trw)
    _write_json(out / "yolo_stage1_10_frame_dry_run_runbook.json", runbook)

    _append_jsonl(out / "yolo_stage1_static_config_trace.jsonl", {"type": "static_config_trace_v0", "validation_id": full.get("validation_id"), "phase": PHASE})
    _append_jsonl(
        out / "yolo_stage1_static_config_replay.jsonl",
        {"type": "static_config_replay_v0", "result": full.get("static_validation_result"), "blockers": full.get("blockers")},
    )
    _append_jsonl(
        out / "yolo_stage1_static_config_whitebox.jsonl",
        {"type": "static_config_whitebox_v0", "why_no_inference": True, "hard_audit": full.get("hard_audit")},
    )

    notes = [
        f"# {PHASE} — YOLO Stage-1 static configuration validation",
        "",
        f"- output_root: `{out}`",
        "- No detector call; no camera; no VideoCapture open.",
        "",
    ]
    (out / "validation_notes.md").write_text("\n".join(notes), encoding="utf-8")

    print(
        json.dumps(
            {"ok": True, "output_root": str(out), "static_validation_result": full.get("static_validation_result")},
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
