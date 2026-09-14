#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations

import argparse
import json
import os
import time
from typing import Any, Dict, List

REPO_ROOT = os.path.abspath(os.environ.get("LUNA_REPO_ROOT") or os.getcwd())
if REPO_ROOT not in __import__("sys").path:
    __import__("sys").path.insert(0, REPO_ROOT)


def _resolve(p: str) -> str:
    return p if os.path.isabs(p) else os.path.abspath(os.path.join(REPO_ROOT, p))


def _read_json(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _read_jsonl_count(path: str) -> int:
    if not os.path.isfile(path):
        return 0
    c = 0
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                c += 1
    return c


def _write_json(path: str, obj: Any) -> None:
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
        f.write("\n")


def _scan_for_boundary_violations(trace_rows: List[Dict[str, Any]]) -> Dict[str, int]:
    counts = {
        "world_model_write_invoked_true": 0,
        "hive_upload_invoked_true": 0,
        "navigation_action_nonnull": 0,
        "real_tts_invoked_true": 0,
    }
    for r in trace_rows:
        if not isinstance(r, dict):
            continue
        if r.get("world_model_write_invoked") is True:
            counts["world_model_write_invoked_true"] += 1
        if r.get("hive_upload_invoked") is True:
            counts["hive_upload_invoked_true"] += 1
        if r.get("navigation_action") is not None:
            counts["navigation_action_nonnull"] += 1
        if r.get("real_tts_invoked") is True:
            counts["real_tts_invoked_true"] += 1
    return counts


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input-root", required=True)
    ap.add_argument("--output-root", required=True)
    args = ap.parse_args()

    in_root = _resolve(args.input_root)
    out_root = _resolve(args.output_root)
    os.makedirs(out_root, exist_ok=True)

    required_files = [
        "scene_delta_summary.json",
        "scene_delta_inputs.json",
        "scene_processed_states.json",
        "spatiotemporal_delta_anchors.json",
        "scene_delta_decisions.json",
        "repeated_evidence_compression_records.json",
        "scene_delta_trace.jsonl",
        "scene_delta_replay.jsonl",
        "scene_delta_whitebox.jsonl",
        "evaluation_notes.md",
        "verification_result.json",
    ]

    hard_blockers: List[str] = []
    if not os.path.isdir(in_root):
        hard_blockers.append("input_root_not_readable")
    missing = [f for f in required_files if not os.path.isfile(os.path.join(in_root, f))]
    if missing:
        hard_blockers.append(f"missing_required_files:{len(missing)}")

    # Best-effort loads
    summary = _read_json(os.path.join(in_root, "scene_delta_summary.json")) if os.path.isfile(os.path.join(in_root, "scene_delta_summary.json")) else {}
    decisions = _read_json(os.path.join(in_root, "scene_delta_decisions.json")) if os.path.isfile(os.path.join(in_root, "scene_delta_decisions.json")) else []
    compress = _read_json(os.path.join(in_root, "repeated_evidence_compression_records.json")) if os.path.isfile(os.path.join(in_root, "repeated_evidence_compression_records.json")) else []
    base_verifier = _read_json(os.path.join(in_root, "verification_result.json")) if os.path.isfile(os.path.join(in_root, "verification_result.json")) else {}

    trace_count = _read_jsonl_count(os.path.join(in_root, "scene_delta_trace.jsonl"))
    replay_count = _read_jsonl_count(os.path.join(in_root, "scene_delta_replay.jsonl"))
    whitebox_count = _read_jsonl_count(os.path.join(in_root, "scene_delta_whitebox.jsonl"))

    # For boundary scan, load trace rows JSONL (cheap enough)
    trace_rows: List[Dict[str, Any]] = []
    trace_path = os.path.join(in_root, "scene_delta_trace.jsonl")
    if os.path.isfile(trace_path):
        with open(trace_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                    if isinstance(obj, dict):
                        trace_rows.append(obj)
                except Exception:
                    continue

    boundary_counts = _scan_for_boundary_violations(trace_rows)

    # Status/action distributions
    status_dist: Dict[str, int] = {}
    action_dist: Dict[str, int] = {}
    if isinstance(decisions, list):
        for d in decisions:
            if not isinstance(d, dict):
                continue
            s = str(d.get("delta_status") or "")
            a = str(d.get("delta_action") or "")
            status_dist[s] = status_dist.get(s, 0) + 1
            action_dist[a] = action_dist.get(a, 0) + 1

    status_action_matrix = {"delta_status_distribution": status_dist, "delta_action_distribution": action_dist}

    # Compression audit summary
    compression_audit = {
        "compression_record_count": len(compress) if isinstance(compress, list) else None,
        "canonical_missing_count": 0,
        "duplicate_count_missing_count": 0,
        "first_last_seen_missing_count": 0,
    }
    if isinstance(compress, list):
        for r in compress:
            if not isinstance(r, dict):
                continue
            if not r.get("canonical_evidence_ref"):
                compression_audit["canonical_missing_count"] += 1
            if "duplicate_count" not in r:
                compression_audit["duplicate_count_missing_count"] += 1
            if "first_seen_at" not in r or "last_seen_at" not in r:
                compression_audit["first_last_seen_missing_count"] += 1

    # Presence checks for core statuses
    present_statuses = set(status_dist.keys())
    required_statuses = [
        "same_content_same_place",
        "new_content_same_place",
        "content_replaced",
        "content_removed",
        "expired",
        "task_context_changed",
        "uncertain",
        "duplicate",
    ]
    status_presence = {k: (k in present_statuses) for k in required_statuses}

    regression_matrix = {
        "input_root": args.input_root,
        "input_root_abs": in_root,
        "base_verifier_verdict": (base_verifier.get("verdict") if isinstance(base_verifier, dict) else None),
        "missing_required_files": missing,
        "counts": {
            "processed_count": summary.get("processed_count") if isinstance(summary, dict) else None,
            "anchors_count": summary.get("anchors_count") if isinstance(summary, dict) else None,
            "decisions_count": summary.get("decisions_count") if isinstance(summary, dict) else None,
            "compression_records_count": summary.get("compression_records_count") if isinstance(summary, dict) else None,
            "trace": trace_count,
            "replay": replay_count,
            "whitebox": whitebox_count,
        },
        "status_presence": status_presence,
        "boundary_counts": boundary_counts,
    }

    boundary_summary = {"boundary_counts": boundary_counts, "boundary_ok": all(v == 0 for v in boundary_counts.values())}
    trw_summary = {"trace": trace_count, "replay": replay_count, "whitebox": whitebox_count, "all_nonempty": trace_count > 0 and replay_count > 0 and whitebox_count > 0}

    regression_summary = {
        "phase": "Phase-MidPlatform-SceneDelta-003",
        "tool": "run_scene_delta_regression_v0.py",
        "input_root": args.input_root,
        "generated_at_ms": int(time.time() * 1000),
        "hard_blockers": hard_blockers,
        "verdict_hint": "GO" if not hard_blockers else "NO_GO",
    }

    _write_json(os.path.join(out_root, "scene_delta_regression_summary.json"), regression_summary)
    _write_json(os.path.join(out_root, "scene_delta_regression_matrix.json"), regression_matrix)
    _write_json(os.path.join(out_root, "scene_delta_status_action_matrix.json"), status_action_matrix)
    _write_json(os.path.join(out_root, "scene_delta_compression_audit_summary.json"), compression_audit)
    _write_json(os.path.join(out_root, "scene_delta_boundary_summary.json"), boundary_summary)
    _write_json(os.path.join(out_root, "scene_delta_trace_replay_whitebox_summary.json"), trw_summary)

    notes = []
    notes.append("# Scene Delta Regression Notes (Phase-MidPlatform-SceneDelta-003)\n\n")
    notes.append(f"- input_root: {args.input_root}\n")
    notes.append(f"- generated_at_ms: {regression_summary['generated_at_ms']}\n")
    notes.append(f"- base_verifier_verdict: {regression_matrix['base_verifier_verdict']}\n")
    notes.append(f"- hard_blockers: {hard_blockers if hard_blockers else 'none'}\n")
    notes.append("\n## Status presence\n")
    for k, v in status_presence.items():
        notes.append(f"- {k}: {v}\n")
    notes.append("\n## Boundary counts\n")
    for k, v in boundary_counts.items():
        notes.append(f"- {k}: {v}\n")
    with open(os.path.join(out_root, "regression_notes.md"), "w", encoding="utf-8") as f:
        f.write("".join(notes))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

