from __future__ import annotations

import argparse
import json
import os
import sys
import time
from typing import Any, Dict, List

_REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

from capabilities.world_model.world_context_evidence_candidate_v0 import run_world_context_evidence_candidate_v0


def _ensure_dir(p: str) -> None:
    os.makedirs(p, exist_ok=True)


def _write_json(path: str, obj: Any) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)


def _write_jsonl(path: str, rows: List[Dict[str, Any]]) -> None:
    with open(path, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def _now_tag() -> str:
    return time.strftime("%Y%m%d_%H%M%S", time.localtime())


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input-root", default=None)
    ap.add_argument("--input-type", required=True, choices=["midplatform_ocr_bridge_root", "scene_delta_root", "sample_matrix"])
    ap.add_argument("--sample-input", default=None)
    ap.add_argument("--output-root", required=True)
    args = ap.parse_args()

    out_root = args.output_root.replace("<timestamp>", _now_tag())
    _ensure_dir(out_root)

    sample_matrix = None
    if args.input_type == "sample_matrix":
        if not args.sample_input:
            raise SystemExit("missing --sample-input")
        with open(args.sample_input, "r", encoding="utf-8") as f:
            sample_matrix = json.load(f)

    res = run_world_context_evidence_candidate_v0(
        input_type=args.input_type,
        midplatform_root=args.input_root if args.input_type == "midplatform_ocr_bridge_root" else None,
        scene_delta_root=args.input_root if args.input_type == "scene_delta_root" else None,
        sample_matrix=sample_matrix,
    )

    world_candidates = res["world_context_evidence_candidates"]
    commercial_candidates = res["commercial_activity_evidence_candidates"]
    world_change_candidates = res["world_change_event_candidates"]
    trust_lifecycle_records = res["trust_and_lifecycle_records"]

    _write_json(os.path.join(out_root, "world_context_evidence_candidates.json"), world_candidates)
    _write_json(os.path.join(out_root, "commercial_activity_evidence_candidates.json"), commercial_candidates)
    _write_json(os.path.join(out_root, "world_change_event_candidates.json"), world_change_candidates)
    _write_json(os.path.join(out_root, "trust_and_lifecycle_records.json"), trust_lifecycle_records)

    _write_jsonl(os.path.join(out_root, "world_context_evidence_trace.jsonl"), res["trace_rows"])
    _write_jsonl(os.path.join(out_root, "world_context_evidence_replay.jsonl"), res["replay_rows"])
    _write_jsonl(os.path.join(out_root, "world_context_evidence_whitebox.jsonl"), res["whitebox_rows"])

    summary = {
        "phase": "Phase-WorldModel-ContextEvidence-002",
        "component": "WorldContextEvidence Candidate Skeleton v0",
        "input_type": args.input_type,
        "input_root": args.input_root,
        "sample_input": args.sample_input,
        "output_root": out_root,
        "counts": {
            "world_context_evidence_candidates": len(world_candidates),
            "commercial_activity_evidence_candidates": len(commercial_candidates),
            "world_change_event_candidates": len(world_change_candidates),
            "trust_and_lifecycle_records": len(trust_lifecycle_records),
            "trace_rows": len(res["trace_rows"]),
            "replay_rows": len(res["replay_rows"]),
            "whitebox_rows": len(res["whitebox_rows"]),
        },
        "boundaries": {
            "candidate_only": True,
            "world_model_write_invoked": False,
            "hive_upload_invoked": False,
            "navigation_action": None,
            "real_tts_invoked": False,
            "recommendation_invoked": False,
        },
        "alignment": {
            "observed_where_source_enabled": True,
            "source_reference_chain_enabled": True,
            "anchor_degradation_enabled": True
        }
    }
    _write_json(os.path.join(out_root, "world_context_evidence_summary.json"), summary)

    notes = [
        "# WorldContextEvidence Candidate Skeleton v0 — evaluation notes",
        "",
        "本次运行只生成离线候选与可观测日志，不接真实 runtime：",
        "- candidate_only=true",
        "- world_model_write_invoked=false",
        "- hive_upload_invoked=false",
        "- navigation_action=null",
        "- real_tts_invoked=false",
        "- recommendation_invoked=false",
        "",
        "输出文件：",
        "- world_context_evidence_summary.json",
        "- world_context_evidence_candidates.json",
        "- commercial_activity_evidence_candidates.json",
        "- world_change_event_candidates.json",
        "- trust_and_lifecycle_records.json",
        "- world_context_evidence_trace.jsonl",
        "- world_context_evidence_replay.jsonl",
        "- world_context_evidence_whitebox.jsonl",
        "",
    ]
    with open(os.path.join(out_root, "evaluation_notes.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(notes))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

