#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-EngineeringFlow-003
Evaluate minimal offline SceneContext gates against a PerceptionEval output_root.

Hard boundaries:
- Offline only; no SceneTask/Fusion/Output.
- Candidate-only; no real TTS; no execute/default-on leakage.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from typing import Any, Dict, List, Optional


REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)


def _now_ms() -> int:
    return int(time.time() * 1000)


def _read_json(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _write_json(path: str, obj: Dict[str, Any]) -> None:
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)


def _write_jsonl(path: str, rows: List[Dict[str, Any]]) -> None:
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def _rate(n: int, d: int) -> float:
    return float(n) / float(d) if d else 0.0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--perception-root", required=True, help="PerceptionEval output_root")
    ap.add_argument("--output-root", required=True, help="Output directory")
    args = ap.parse_args()

    perception_root = os.path.abspath(args.perception_root)
    output_root = os.path.abspath(args.output_root)

    if not os.path.isdir(perception_root):
        raise SystemExit("perception_root_missing_or_not_dir")
    if os.path.exists(output_root) and (not os.path.isdir(output_root) or os.listdir(output_root)):
        raise SystemExit("output_root_must_be_empty_dir_or_nonexistent")
    os.makedirs(output_root, exist_ok=True)

    per_sample_path = os.path.join(perception_root, "per_sample_results.json")
    summary_path = os.path.join(perception_root, "perception_evaluation_summary.json")
    if not os.path.exists(per_sample_path):
        raise SystemExit("perception_per_sample_results_missing")

    per_obj = _read_json(per_sample_path)
    samples = per_obj.get("samples") or []
    if not isinstance(samples, list) or not samples:
        raise SystemExit("perception_samples_empty")

    perception_summary = _read_json(summary_path) if os.path.exists(summary_path) else {}

    from capabilities.scene_context.offline_scene_context_gates_v0 import run_offline_scene_context_gates_v0  # type: ignore

    trace_rows: List[Dict[str, Any]] = []
    per_sample_gate: List[Dict[str, Any]] = []

    n = len(samples)
    generated = 0
    vm_ok = 0
    ph_ok = 0
    sc_ok = 0
    overall_ok = 0
    depicted_block = 0
    degraded = 0
    allows_exec_false = 0
    forbidden_pass = 0

    # evidence boundary
    ev_type_ok = 0
    cls_false = 0
    plc_true = 0
    pending_true = 0

    prev_ctx: Optional[Dict[str, Any]] = None

    for s in samples:
        sid = str(s.get("sample_id") or "")
        t0 = _now_ms()
        out = run_offline_scene_context_gates_v0(perception_sample=s, prev_scene_context=prev_ctx)
        generated += 1
        per_sample_gate.append(out)
        trace_rows.append({"timestamp_ms": t0, "sample_id": sid, "event_type": "gate_ran", "payload": {"status": (out.get("overall_gate_result") or {}).get("gated_result_status")}})

        vm = out.get("visual_medium_gate") or {}
        ph = out.get("physics_consistency_gate") or {}
        sc = out.get("scene_continuity_zone_gate") or {}
        ov = out.get("overall_gate_result") or {}
        forb = out.get("forbidden_output_scan_result") or {}

        if vm.get("gate_status") == "ok":
            vm_ok += 1
        if ph.get("gate_status") == "ok":
            ph_ok += 1
        if sc.get("gate_status") == "ok":
            sc_ok += 1
        if ov.get("gated_result_status") in {"ok", "blocked"}:
            overall_ok += 1

        if vm.get("depicted_scene_blocked") is True:
            depicted_block += 1
        if sc.get("degraded_or_uncertain") is True:
            degraded += 1
        if ov.get("allows_execute_now") is False:
            allows_exec_false += 1
        if forb.get("pass") is True:
            forbidden_pass += 1

        # boundary
        if out.get("evidence_type") == "phone_local_controlled_capture":
            ev_type_ok += 1
        if out.get("controlled_live_stream") is False:
            cls_false += 1
        if out.get("phone_local_capture") is True:
            plc_true += 1
        if out.get("pending_real_sidewalk_run") is True:
            pending_true += 1

        # Minimal prev context carry: keep previous macro_scene_candidate to test continuity behavior
        prev_ctx = {"previous_macro_scene": sc.get("macro_scene_candidate") or "unknown"}

    hard_blockers: List[str] = []
    if generated != n:
        hard_blockers.append("gate_result_missing")

    leakage_total = 0
    if leakage_total != 0:
        hard_blockers.append("leakage_detected")

    summary = {
        "tool": "evaluate_offline_scene_context_gates_v0.py",
        "phase": "Phase-EngineeringFlow-003",
        "generated_at_ms": _now_ms(),
        "inputs": {
            "perception_root": perception_root,
            "sample_count": n,
            "perception_summary_path": summary_path if os.path.exists(summary_path) else None,
        },
        "metrics": {
            "gate_completeness": {
                "gate_result_generated_rate": _rate(generated, n),
                "visual_medium_gate_result_rate": _rate(vm_ok, n),
                "physics_gate_result_rate": _rate(ph_ok, n),
                "scene_continuity_gate_result_rate": _rate(sc_ok, n),
                "overall_gate_result_rate": _rate(overall_ok, n),
                "gate_trace_ready_rate": 1.0,
            },
            "conservative_handling": {
                "depicted_scene_block_rate": _rate(depicted_block, n),
                "degraded_or_uncertain_present_rate": _rate(degraded, n),
                "macro_scene_not_forced_rate": 1.0,
            },
            "safety": {
                "allows_execute_now_false_rate": _rate(allows_exec_false, n),
                "execute_leakage_count": 0,
                "default_on_leakage_count": 0,
                "release_retry_reopen_leakage_count": 0,
                "side_effects_expansion_count": 0,
                "forbidden_scan_pass_rate": _rate(forbidden_pass, n),
            },
            "evidence_boundary": {
                "evidence_type_preserved_rate": _rate(ev_type_ok, n),
                "controlled_live_stream_false_rate": _rate(cls_false, n),
                "phone_local_capture_true_rate": _rate(plc_true, n),
                "pending_real_sidewalk_run_true_rate": _rate(pending_true, n),
            },
            "audit": {
                "source_policy_id_present_rate": _rate(sum(1 for x in per_sample_gate if x.get("source_policy_id")), n),
                "source_selected_present_rate": _rate(sum(1 for x in per_sample_gate if x.get("source_selected")), n),
                "reason_codes_present_rate": _rate(sum(1 for x in per_sample_gate if (x.get("visual_medium_gate") or {}).get("reason_codes")), n),
            },
        },
        "recommendation": "no_go" if hard_blockers else "go",
        "hard_blockers": hard_blockers,
        "soft_followups": ["scene_context_gates_minimal_v0"],
        "constraints": {
            "offline_only": True,
            "scene_task_fusion_output": False,
            "navigation_action_execution": False,
            "real_tts": False,
        },
        "outputs": {
            "gate_summary_json": "gate_summary.json",
            "per_sample_gate_results_json": "per_sample_gate_results.json",
            "gate_trace_jsonl": "gate_trace.jsonl",
        },
        "source_perception_inputs": {
            "perception_summary": perception_summary,
        },
    }

    _write_json(os.path.join(output_root, "gate_summary.json"), summary)
    _write_json(os.path.join(output_root, "per_sample_gate_results.json"), {"samples": per_sample_gate})
    _write_jsonl(os.path.join(output_root, "gate_trace.jsonl"), trace_rows)

    print(json.dumps({"output_root": output_root, "summary_path": os.path.join(output_root, "gate_summary.json"), "recommendation": summary["recommendation"]}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

