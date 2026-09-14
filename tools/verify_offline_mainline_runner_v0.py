#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-EngineeringFlow-004
Verify unified offline mainline runner v0.
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


def _read_json(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _write_json(path: str, obj: Dict[str, Any]) -> None:
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)


def _case(name: str, ok: bool, details: Dict[str, Any]) -> Dict[str, Any]:
    return {"case": name, "ok": bool(ok), "details": details}


def _verify_one_run(root: str, expect_source: str) -> List[Dict[str, Any]]:
    cases: List[Dict[str, Any]] = []
    root = os.path.abspath(root)
    summ_p = os.path.join(root, "mainline_summary.json")
    per_p = os.path.join(root, "per_sample_mainline_results.json")
    trace_p = os.path.join(root, "mainline_trace.jsonl")
    replay_p = os.path.join(root, "mainline_replay_index.json")
    whitebox_p = os.path.join(root, "mainline_whitebox_index.json")

    cases.append(_case("H_trace_index_exists", os.path.exists(trace_p), {"path": trace_p}))
    cases.append(_case("H_replay_index_exists", os.path.exists(replay_p), {"path": replay_p}))
    cases.append(_case("H_whitebox_index_exists", os.path.exists(whitebox_p), {"path": whitebox_p}))

    if not (os.path.exists(summ_p) and os.path.exists(per_p)):
        cases.append(_case("I_stage_output_missing_no_go", False, {"missing": [p for p in [summ_p, per_p] if not os.path.exists(p)]}))
        return cases

    summ = _read_json(summ_p)
    per = _read_json(per_p)
    samples = per.get("samples") or []
    n = len(samples) if isinstance(samples, list) else 0

    # A/B: chain complete (rates 1.0) for all stages
    scr = summ.get("stage_complete_rates") or {}
    ok_chain = all(float(scr.get(k) or 0.0) == 1.0 for k in ["perception", "scene_context", "scene_task", "fusion", "output"])
    cases.append(_case("A_or_B_chain_complete_rates_all_1", ok_chain, {"stage_complete_rates": scr}))

    # D/E: no real TTS; no execute
    cases.append(_case("D_real_tts_invoked_false_rate_1", float(summ.get("real_tts_invoked_false_rate") or 0.0) == 1.0, {"real_tts_invoked_false_rate": summ.get("real_tts_invoked_false_rate")}))
    cases.append(_case("E_allows_execute_now_false_rate_1", float(summ.get("allows_execute_now_false_all_stages_rate") or 0.0) == 1.0, {"allows_execute_now_false_all_stages_rate": summ.get("allows_execute_now_false_all_stages_rate")}))

    # F: pending remains true
    ebr = summ.get("evidence_boundary_rates") or {}
    cases.append(_case("F_pending_real_sidewalk_run_true_rate_1", float(ebr.get("pending_real_sidewalk_run_true") or 0.0) == 1.0, {"evidence_boundary_rates": ebr}))

    # G: controlled_live_stream must be false
    cases.append(_case("G_controlled_live_stream_false_rate_1", float(ebr.get("controlled_live_stream_false") or 0.0) == 1.0, {"evidence_boundary_rates": ebr}))

    # Source policy expectations
    dist = summ.get("source_selected_distribution") or {}
    ok_src = (str(list(dist.keys())[0]) == expect_source) if isinstance(dist, dict) and dist else False
    cases.append(_case("source_selected_distribution_matches_expectation", ok_src, {"distribution": dist, "expect": expect_source}))

    # Per-sample refs exist
    ok_refs = True
    missing_refs: List[str] = []
    for s in samples if isinstance(samples, list) else []:
        for k in ["scene_task_result_ref", "fusion_result_ref", "output_result_ref"]:
            rel = s.get(k)
            if not isinstance(rel, str) or not rel:
                ok_refs = False
                missing_refs.append(f"{s.get('sample_id')}:{k}:missing")
                continue
            ap = os.path.join(root, rel)
            if not os.path.exists(ap):
                ok_refs = False
                missing_refs.append(f"{s.get('sample_id')}:{k}:{ap}")
    cases.append(_case("stage_output_refs_exist", ok_refs, {"missing": missing_refs[:50], "checked_samples": n}))

    return cases


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--normal-root", required=True)
    ap.add_argument("--fallback-root", required=True)
    ap.add_argument("--output-json", required=True)
    args = ap.parse_args()

    cases: List[Dict[str, Any]] = []
    cases.extend(_verify_one_run(args.normal_root, expect_source="yolo_shadow"))
    cases.extend(_verify_one_run(args.fallback_root, expect_source="baseline_mock"))

    ok_all = all(c["ok"] for c in cases)
    report = {
        "phase": "Phase-EngineeringFlow-004",
        "tool": "verify_offline_mainline_runner_v0.py",
        "generated_at_s": time.time(),
        "inputs": {"normal_root": args.normal_root, "fallback_root": args.fallback_root},
        "summary": {"case_count": len(cases), "pass_count": sum(1 for c in cases if c["ok"]), "fail_count": sum(1 for c in cases if not c["ok"]), "ok": ok_all},
        "cases": cases,
        "notes": ["Verifier checks offline-only safety/evidence boundary/index existence and chain completeness."],
    }
    _write_json(args.output_json, report)
    print(args.output_json)
    return 0 if ok_all else 2


if __name__ == "__main__":
    raise SystemExit(main())

