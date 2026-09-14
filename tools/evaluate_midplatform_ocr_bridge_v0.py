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

from capabilities.mid_platform.ocr_text_extraction_bridge_v0 import (
    build_midplatform_ocr_evidence_input_v0,
    run_midplatform_ocr_text_extraction_bridge_v0,
)


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


def _load_samples_from_sample_matrix(sample_matrix_path: str) -> List[Dict[str, Any]]:
    data = _read_json(sample_matrix_path)
    samples = data.get("samples")
    if not isinstance(samples, list):
        raise SystemExit("sample_matrix_missing_samples")
    return [s for s in samples if isinstance(s, dict)]


def _load_samples_from_ocr_raw_benchmark_root(root: str) -> List[Dict[str, Any]]:
    # expects logs/*/raw_outputs/<provider_id>/ocr_sample_*.json
    raw_outputs = os.path.join(root, "raw_outputs")
    if not os.path.isdir(raw_outputs):
        raise SystemExit("ocr_benchmark_root_missing_raw_outputs")
    samples: List[Dict[str, Any]] = []
    for provider_dir in sorted(os.listdir(raw_outputs)):
        pdir = os.path.join(raw_outputs, provider_dir)
        if not os.path.isdir(pdir):
            continue
        for fn in sorted(os.listdir(pdir)):
            if not (fn.startswith("ocr_sample_") and fn.endswith(".json")):
                continue
            path = os.path.join(pdir, fn)
            j = _read_json(path)
            # normalize: use raw_output if exists
            raw_output = j.get("raw_output") if isinstance(j.get("raw_output"), dict) else j.get("raw_output") or {}
            if not isinstance(raw_output, dict):
                continue
            raw_text_candidates = raw_output.get("raw_text_candidates") or j.get("raw_output", {}).get("raw_text_candidates") or []
            raw_text_joined = raw_output.get("raw_text_joined") or j.get("pred_raw_text_joined") or ""
            samples.append(
                {
                    "sample_id": raw_output.get("sample_id") or j.get("sample_id") or fn.replace(".json", ""),
                    "frame_id": raw_output.get("sample_id") or j.get("sample_id") or fn.replace(".json", ""),
                    "timestamp_ms": 0,
                    "reading_direction_candidate": "unknown",
                    "line_order_status": "present" if raw_text_candidates else "not_available",
                    "visual_source_hint": None,
                    "raw_text_candidates": raw_text_candidates if isinstance(raw_text_candidates, list) else [],
                    "raw_text_joined": raw_text_joined if isinstance(raw_text_joined, str) else "",
                }
            )
    return samples


def _load_samples_from_yolo_ocr_bridge_root(root: str) -> List[Dict[str, Any]]:
    p = os.path.join(root, "per_sample_yolo_ocr_bridge_results.json")
    if not os.path.isfile(p):
        raise SystemExit("yolo_ocr_bridge_root_missing_per_sample_results")
    per_sample = _read_json(p)
    if not isinstance(per_sample, list):
        raise SystemExit("per_sample_results_not_list")

    out: List[Dict[str, Any]] = []
    for s in per_sample:
        if not isinstance(s, dict):
            continue
        bridge = s.get("bridge") if isinstance(s.get("bridge"), dict) else {}
        results = bridge.get("bridge_results") if isinstance(bridge.get("bridge_results"), list) else []
        for br in results:
            if not isinstance(br, dict):
                continue
            raw_text_candidates = br.get("raw_text_candidates") or []
            raw_text_joined = br.get("raw_text_joined") or ""
            out.append(
                {
                    "sample_id": str(br.get("sample_id") or br.get("frame_id") or ""),
                    "frame_id": str(br.get("frame_id") or br.get("sample_id") or ""),
                    "timestamp_ms": int(br.get("timestamp_ms") or 0),
                    "reading_direction_candidate": br.get("reading_direction_candidate") or "unknown",
                    "line_order_status": br.get("line_order_status") or "present",
                    "visual_source_hint": None,
                    "raw_text_candidates": raw_text_candidates if isinstance(raw_text_candidates, list) else [],
                    "raw_text_joined": raw_text_joined if isinstance(raw_text_joined, str) else "",
                    "evidence_id": str(br.get("bridge_result_id") or br.get("proposal_id") or ""),
                    "source_evidence_id": str(br.get("bridge_result_id") or br.get("proposal_id") or ""),
                }
            )
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input-root", required=True)
    ap.add_argument("--input-type", required=True, choices=["ocr_benchmark_root", "yolo_ocr_bridge_root", "sample_matrix"])
    ap.add_argument("--output-root", required=True)
    args = ap.parse_args()

    input_root = _resolve(args.input_root)
    out_root = _resolve(args.output_root)
    os.makedirs(out_root, exist_ok=True)

    # load evidence seeds
    samples: List[Dict[str, Any]]
    if args.input_type == "sample_matrix":
        samples = _load_samples_from_sample_matrix(input_root)
    elif args.input_type == "yolo_ocr_bridge_root":
        samples = _load_samples_from_yolo_ocr_bridge_root(input_root)
    elif args.input_type == "ocr_benchmark_root":
        samples = _load_samples_from_ocr_raw_benchmark_root(input_root)
    else:
        raise SystemExit("unsupported_input_type")

    evidence_inputs: List[Dict[str, Any]] = []
    notes: List[str] = []

    for idx, s in enumerate(samples):
        if not isinstance(s, dict):
            continue
        raw_text_candidates = s.get("raw_text_candidates") or []
        raw_text_joined = s.get("raw_text_joined") or ""
        if not raw_text_candidates and not raw_text_joined:
            notes.append(f"honest_not_available_evidence_skipped:{s.get('sample_id') or idx}")
            continue

        evidence_id = str(s.get("evidence_id") or f"ocr_evidence_{idx:03d}")
        evidence_inputs.append(
            build_midplatform_ocr_evidence_input_v0(
                evidence_id=evidence_id,
                raw_text_candidates=raw_text_candidates if isinstance(raw_text_candidates, list) else [],
                raw_text_joined=str(raw_text_joined),
                reading_direction_candidate=str(s.get("reading_direction_candidate") or "unknown"),
                line_order_status=str(s.get("line_order_status") or "present"),
                timestamp_ms=int(s.get("timestamp_ms") or 0),
                frame_id=str(s.get("frame_id") or s.get("sample_id") or evidence_id),
                source_evidence_id=str(s.get("source_evidence_id") or s.get("sample_id") or evidence_id),
                user_requested_override=bool(s.get("user_requested_override") or False),
                visual_source_hint=s.get("visual_source_hint"),
            )
        )

    if not evidence_inputs:
        # still write skeleton outputs for verifier to provide NO_GO reason
        _write_json(os.path.join(out_root, "midplatform_ocr_bridge_summary.json"), {"verdict": "NO_GO", "reason": "no_evidence_inputs"})
        with open(os.path.join(out_root, "evaluation_notes.md"), "w", encoding="utf-8") as f:
            f.write("no_evidence_inputs\n")
        return 2

    bridge_out = run_midplatform_ocr_text_extraction_bridge_v0(evidence_inputs=evidence_inputs)

    mid_text_candidates = bridge_out.get("midplatform_text_extraction_candidates") or []
    world_candidates = bridge_out.get("world_context_evidence_candidates") or []
    ambient_candidates = bridge_out.get("ambient_context_candidates") or []

    _write_json(os.path.join(out_root, "midplatform_ocr_bridge_summary.json"), bridge_out_summary := {
        "phase": "Phase-ModelOCR-MidPlatform-Bridge-002",
        "tool": "evaluate_midplatform_ocr_bridge_v0.py",
        "input_root": input_root,
        "input_type": args.input_type,
        "evidence_input_count": len(evidence_inputs),
        "delta_control_results_count": len(bridge_out.get("scene_delta_control_results") or []),
        "filter_results_count": len(bridge_out.get("filter_results") or []),
        "midplatform_text_extraction_candidates_count": len(mid_text_candidates),
        "world_context_evidence_candidates_count": len(world_candidates),
        "ambient_context_candidates_count": len(ambient_candidates),
        "verdict": "GO",
        "notes": notes,
    })

    _write_json(os.path.join(out_root, "midplatform_ocr_evidence_inputs.json"), evidence_inputs)
    _write_json(os.path.join(out_root, "scene_delta_control_results.json"), bridge_out.get("scene_delta_control_results") or [])
    _write_json(os.path.join(out_root, "filter_results.json"), bridge_out.get("filter_results") or [])
    _write_json(os.path.join(out_root, "midplatform_text_extraction_candidates.json"), mid_text_candidates)
    _write_json(os.path.join(out_root, "world_context_evidence_candidates.json"), world_candidates)
    _write_json(os.path.join(out_root, "ambient_context_candidates.json"), ambient_candidates)

    trace_rows = bridge_out.get("trace_rows") or []
    replay_rows = bridge_out.get("replay_rows") or []
    whitebox_rows = bridge_out.get("whitebox_rows") or []

    _write_jsonl(os.path.join(out_root, "midplatform_ocr_bridge_trace.jsonl"), trace_rows)
    _write_jsonl(os.path.join(out_root, "midplatform_ocr_bridge_replay.jsonl"), replay_rows)
    _write_jsonl(os.path.join(out_root, "midplatform_ocr_bridge_whitebox.jsonl"), whitebox_rows)

    with open(os.path.join(out_root, "evaluation_notes.md"), "w", encoding="utf-8") as f:
        f.write("# Evaluation Notes (Phase-ModelOCR-MidPlatform-Bridge-002)\n\n")
        f.write(f"input_type: {args.input_type}\n")
        f.write(f"evidence_inputs: {len(evidence_inputs)}\n")
        f.write(f"task_candidates: {len(mid_text_candidates)}\n")
        f.write(f"world_context_candidates: {len(world_candidates)}\n")
        f.write(f"ambient_context_candidates: {len(ambient_candidates)}\n")
        for n in notes:
            f.write(f"- {n}\n")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

