#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations

import argparse
import json
import os
from typing import Any, Dict, List, Optional

REPO_ROOT = os.path.abspath(os.environ.get("LUNA_REPO_ROOT") or os.getcwd())
if REPO_ROOT not in __import__("sys").path:
    __import__("sys").path.insert(0, REPO_ROOT)

from capabilities.mid_platform.scene_delta_control_v0 import run_scene_delta_control_v0


def _read_json(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _write_json(path: str, obj: Any) -> None:
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
        f.write("\n")


def _write_jsonl(path: str, rows: List[Dict[str, Any]]) -> None:
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def _resolve(p: str) -> str:
    return p if os.path.isabs(p) else os.path.abspath(os.path.join(REPO_ROOT, p))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sample-input", required=True)
    ap.add_argument("--output-root", required=True)
    args = ap.parse_args()

    sample_path = _resolve(args.sample_input)
    out_root = _resolve(args.output_root)
    os.makedirs(out_root, exist_ok=True)

    data = _read_json(sample_path)
    samples = data.get("samples")
    if not isinstance(samples, list):
        raise SystemExit("sample_matrix_missing_samples")

    inputs_out: List[Dict[str, Any]] = []
    states_out: List[Dict[str, Any]] = []
    anchors_out: List[Dict[str, Any]] = []
    decisions_out: List[Dict[str, Any]] = []
    compress_out: List[Dict[str, Any]] = []

    trace_rows: List[Dict[str, Any]] = []
    replay_rows: List[Dict[str, Any]] = []
    whitebox_rows: List[Dict[str, Any]] = []

    notes: List[str] = []

    for s in samples:
        if not isinstance(s, dict):
            continue
        sample_id = str(s.get("sample_id") or "")
        cur = s.get("current_input") if isinstance(s.get("current_input"), dict) else None
        prev = s.get("previous_state") if isinstance(s.get("previous_state"), dict) else None
        if not cur or not sample_id:
            notes.append("skipped_invalid_sample")
            continue

        task_context_changed = bool(s.get("task_context_changed") or (s.get("current_input") or {}).get("task_context_changed") or False)
        is_duplicate_in_window = bool(s.get("is_duplicate_in_window") or False)

        out = run_scene_delta_control_v0(
            sample_id=sample_id,
            current_input=cur,
            previous_state=prev,
            task_context_changed=task_context_changed,
            is_duplicate_in_window=is_duplicate_in_window,
        )

        inputs_out.append(out["scene_delta_input"])
        states_out.append(out["scene_processed_state"])
        anchors_out.append(out["spatiotemporal_delta_anchor"])
        decisions_out.append(out["scene_delta_decision"])
        if out.get("repeated_evidence_compression_record") is not None:
            compress_out.append(out["repeated_evidence_compression_record"])

        trace_rows.append(out["trace_row"])
        replay_rows.append(out["replay_row"])
        whitebox_rows.append(out["whitebox_row"])

    summary = {
        "phase": "Phase-MidPlatform-SceneDelta-002",
        "tool": "evaluate_scene_delta_control_v0.py",
        "sample_input": sample_path,
        "sample_count": len(samples),
        "processed_count": len(inputs_out),
        "anchors_count": len(anchors_out),
        "decisions_count": len(decisions_out),
        "compression_records_count": len(compress_out),
        "verdict": "GO",
        "notes": notes,
    }

    _write_json(os.path.join(out_root, "scene_delta_summary.json"), summary)
    _write_json(os.path.join(out_root, "scene_delta_inputs.json"), inputs_out)
    _write_json(os.path.join(out_root, "scene_processed_states.json"), states_out)
    _write_json(os.path.join(out_root, "spatiotemporal_delta_anchors.json"), anchors_out)
    _write_json(os.path.join(out_root, "scene_delta_decisions.json"), decisions_out)
    _write_json(os.path.join(out_root, "repeated_evidence_compression_records.json"), compress_out)

    _write_jsonl(os.path.join(out_root, "scene_delta_trace.jsonl"), trace_rows)
    _write_jsonl(os.path.join(out_root, "scene_delta_replay.jsonl"), replay_rows)
    _write_jsonl(os.path.join(out_root, "scene_delta_whitebox.jsonl"), whitebox_rows)

    with open(os.path.join(out_root, "evaluation_notes.md"), "w", encoding="utf-8") as f:
        f.write("# Evaluation Notes (Phase-MidPlatform-SceneDelta-002)\n\n")
        f.write(f"sample_input: {sample_path}\n")
        f.write(f"processed_samples: {len(inputs_out)}\n")
        for n in notes:
            f.write(f"- {n}\n")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

