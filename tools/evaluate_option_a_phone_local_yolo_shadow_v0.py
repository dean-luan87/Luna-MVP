#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Phase-ModelPerception-002B

Evaluate Option A phone_local samples with YOLO Shadow Adapter (shadow-only).

Hard boundaries:
- Does NOT modify existing PerceptionEval/SceneTask/Fusion/Output tools.
- Produces separate YOLO shadow artifacts only.
- Supports disable switch + fallback; never enables default path; no execution outputs.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from typing import Any, Dict, List

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from capabilities.model_perception.yolo_shadow_adapter_v0 import (
    PhoneLocalSampleRefV0,
    YoloShadowAdapterConfigV0,
    run_yolo_shadow_adapter_on_sample_v0,
)


def _ensure_dir(p: str) -> None:
    os.makedirs(p, exist_ok=True)


def _write_json(path: str, obj: Any) -> None:
    _ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2, sort_keys=False)


def _write_jsonl(path: str, record: Dict[str, Any]) -> None:
    _ensure_dir(os.path.dirname(path))
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def _resolve_root(p: str, *, repo_root: str, workspace_root: str) -> str:
    if os.path.isabs(p):
        return p
    # Prefer workspace_root (where sample_matrix points by default)
    cand = os.path.join(workspace_root, p)
    if os.path.exists(cand):
        return cand
    cand2 = os.path.join(repo_root, p)
    if os.path.exists(cand2):
        return cand2
    return os.path.join(workspace_root, p)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sample-matrix", required=True)
    ap.add_argument("--output-root", required=True)
    ap.add_argument("--disable-yolo", default="true", choices=["true", "false"])
    ap.add_argument("--max-frames", type=int, default=60)
    ap.add_argument("--frame-step", type=int, default=10)
    ap.add_argument("--confidence-threshold", type=float, default=0.5)
    ap.add_argument("--model-path", default="yolov5n.pt")
    ap.add_argument("--model-config-id", default="yolo_shadow_v0")
    args = ap.parse_args()

    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    workspace_root = os.path.abspath(os.path.join(repo_root, "..", "Luna-Workspace-Min"))

    sample_matrix_path = _resolve_root(args.sample_matrix, repo_root=repo_root, workspace_root=workspace_root)
    output_root = _resolve_root(args.output_root, repo_root=repo_root, workspace_root=workspace_root)
    _ensure_dir(output_root)

    with open(sample_matrix_path, "r", encoding="utf-8") as f:
        mat = json.load(f)

    samples_in: List[Dict[str, Any]] = mat.get("samples", [])

    cfg = YoloShadowAdapterConfigV0(
        model_config_id=str(args.model_config_id),
        model_path=str(args.model_path),
        max_frames=int(args.max_frames),
        frame_step=int(args.frame_step),
        confidence_threshold=float(args.confidence_threshold),
        disable_yolo=(str(args.disable_yolo).lower() == "true"),
    )

    ts0 = time.time()
    trace_path = os.path.join(output_root, "yolo_shadow_trace.jsonl")
    replay_path = os.path.join(output_root, "yolo_shadow_replay.jsonl")
    whitebox_path = os.path.join(output_root, "yolo_shadow_whitebox.jsonl")
    per_sample_results: List[Dict[str, Any]] = []

    _write_jsonl(trace_path, {"ts": ts0, "kind": "start", "sample_matrix": args.sample_matrix, "disable_yolo": cfg.disable_yolo})

    workspace_roots_for_media = [workspace_root, repo_root]

    for s in samples_in:
        sample = PhoneLocalSampleRefV0(
            sample_id=str(s["sample_id"]),
            source_video_path=str(s["source_video_path"]),
            archive_root=str(s.get("archive_root", "")),
            evidence_type=str(s.get("evidence_type", "")),
            controlled_live_stream=bool(s.get("controlled_live_stream", False)),
            phone_local_capture=bool(s.get("phone_local_capture", True)),
        )

        out = run_yolo_shadow_adapter_on_sample_v0(
            sample=sample,
            cfg=cfg,
            output_root=output_root,
            workspace_roots_for_media=workspace_roots_for_media,
        )
        per_sample_results.append(out)

        _write_jsonl(trace_path, {"ts": time.time(), "kind": "sample_done", "sample_id": sample.sample_id, "fallback_used": out.get("fallback_used")})

    # Summary
    fallback_count = sum(1 for r in per_sample_results if r.get("fallback_used"))
    invoked_count = sum(1 for r in per_sample_results if r.get("yolo_invoked"))
    ok_count = len(per_sample_results) - fallback_count

    summary = {
        "phase": "Phase-ModelPerception-002B",
        "tool": "evaluate_option_a_phone_local_yolo_shadow_v0.py",
        "generated_at_s": time.time(),
        "sample_matrix": args.sample_matrix,
        "resolved_sample_matrix_path": sample_matrix_path,
        "output_root": args.output_root,
        "resolved_output_root": output_root,
        "model_config_id": cfg.model_config_id,
        "disable_yolo": cfg.disable_yolo,
        "invoked_count": invoked_count,
        "fallback_count": fallback_count,
        "ok_count": ok_count,
        "samples_total": len(per_sample_results),
        "safety_leakage": 0,
        "controlled_live_stream": False,
        "not_model_claimed": False,
        "candidate_only": True,
        "notes": [
            "This tool produces YOLO shadow artifacts only; it does not modify upstream evaluation chain outputs.",
            "SceneContext gates are not executed in 002B; outputs are marked gate_required/not_executed.",
        ],
        "artifacts": {
            "trace_jsonl": trace_path,
            "replay_jsonl": replay_path,
            "whitebox_jsonl": whitebox_path,
        },
    }

    _write_json(os.path.join(output_root, "yolo_shadow_summary.json"), summary)
    _write_json(os.path.join(output_root, "per_sample_yolo_shadow_results.json"), {"samples": per_sample_results})

    # Root-level replay/whitebox pointers (per-sample files are inside each sample dir)
    _write_jsonl(replay_path, {"ts": time.time(), "kind": "replay_root", "samples": [r.get("sample_id") for r in per_sample_results]})
    _write_jsonl(whitebox_path, {"ts": time.time(), "kind": "whitebox_root", "disable_yolo": cfg.disable_yolo})

    # Notes file
    notes_md = os.path.join(output_root, "evaluation_notes.md")
    with open(notes_md, "w", encoding="utf-8") as f:
        f.write("# YOLO Shadow Eval Notes (v0)\n\n")
        f.write("- Shadow-only, candidate-only.\n")
        f.write("- No integration into SceneTask/Fusion/Output.\n")
        f.write("- Gates marked required but not executed in 002B.\n")
        f.write(f"- disable_yolo={cfg.disable_yolo}\n")

    _write_jsonl(trace_path, {"ts": time.time(), "kind": "done", "samples_total": len(per_sample_results)})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

