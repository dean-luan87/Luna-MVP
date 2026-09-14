#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase 3.3-D0: 一条命令跑完 baseline replay -> candidate replay -> comparator -> scorer -> gate。
不碰 runtime，不写 library_store。PASS 返回 0，FAIL 返回 2。
"""
import argparse
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from simulation.logic.gate import is_gate_passed
from simulation.logic.scorer import score
from simulation.sim_runner import run_episode


def main():
    parser = argparse.ArgumentParser(
        description="D0: run baseline + candidate replay, then compare and gate."
    )
    parser.add_argument("--base-dir", default="library_store", help="Base dir for episodes")
    parser.add_argument("--version-tag", default="v1.1", help="Version tag")
    parser.add_argument("--episode", required=True, help="Episode path relative to base_dir (e.g. v1.1/episodes/...)")
    parser.add_argument("--patch", required=True, help="Path to param_patch.json (use empty file for baseline)")
    parser.add_argument("--out-dir", default="outputs", help="Output directory (simulations under out_dir/version_tag/simulations)")
    parser.add_argument("--baseline", default="", help="Optional: path to existing baseline replay bundle; if set, skip baseline run")
    parser.add_argument("--mode", choices=["replay", "recompute"], default="replay", help="replay=record passthrough; recompute=A3 headless")
    args = parser.parse_args()

    base_dir = args.base_dir.rstrip("/")
    version = args.version_tag
    out_version = os.path.join(args.out_dir.rstrip("/"), version)
    sim_dir = os.path.join(out_version, "simulations")
    os.makedirs(sim_dir, exist_ok=True)

    if args.baseline:
        baseline_bundle = args.baseline.rstrip("/")
        if not os.path.isdir(baseline_bundle):
            print("ERROR: --baseline is not a directory:", baseline_bundle, file=sys.stderr)
            return 2
    else:
        baseline_bundle = run_episode(
            base_dir=base_dir,
            version_tag=version,
            episode_rel_path=args.episode,
            patch_path="",
            out_dir=sim_dir,
            mode=args.mode,
        )
    candidate_bundle = run_episode(
        base_dir=base_dir,
        version_tag=version,
        episode_rel_path=args.episode,
        patch_path=args.patch,
        out_dir=sim_dir,
        baseline_bundle_path=baseline_bundle,
        mode=args.mode,
    )

    scorecard = score(
        baseline_path=baseline_bundle,
        candidate_path=candidate_bundle,
        explain_baseline_path=None,
        explain_candidate_path=None,
    )
    scorecard_path = os.path.join(candidate_bundle, "scorecard.json")
    with open(scorecard_path, "w", encoding="utf-8") as f:
        json.dump(scorecard, f, ensure_ascii=False, indent=2)

    passed, reasons = is_gate_passed(scorecard)
    gate_result_path = os.path.join(candidate_bundle, "gate_result.json")
    with open(gate_result_path, "w", encoding="utf-8") as f:
        json.dump({"passed": passed, "reasons": reasons}, f, ensure_ascii=False, indent=2)
    reg = scorecard.get("regression_count", 0)
    vol = scorecard.get("volatility_index", 0)
    comp_delta = scorecard.get("explain_completeness_delta", 0)
    early_gain = scorecard.get("early_conservative_action_gain", 0)
    danger_delta = scorecard.get("danger_delta", 0)
    eff = scorecard.get("efficiency") or {}
    cov = scorecard.get("coverage") or {}
    gr_delta = eff.get("guarded_ratio_delta")
    lookahead_drop = eff.get("lookahead_drop_ratio")
    dec_cov_delta = scorecard.get("decision_coverage_delta")
    la_cov_delta = scorecard.get("lookahead_coverage_delta")

    print("REGRESSION:", reg)
    print("VOLATILITY:", vol)
    print("COMPLETENESS_DELTA:", f"{comp_delta:+.2f}")
    print("EARLY_CONSERVATIVE_ACTION_GAIN:", early_gain)
    print("DANGER_DELTA:", danger_delta)
    if gr_delta is not None:
        print("GUARDED_RATIO_DELTA:", gr_delta)
    if lookahead_drop is not None:
        print("LOOKAHEAD_DROP_RATIO:", lookahead_drop)
    if dec_cov_delta is not None:
        print("DECISION_COVERAGE_DELTA:", dec_cov_delta)
    if la_cov_delta is not None:
        print("LOOKAHEAD_COVERAGE_DELTA:", la_cov_delta)
    print("GATE:", "PASS" if passed else "FAIL")
    if reasons:
        for r in reasons:
            print("  ", r)

    return 0 if passed else 2


if __name__ == "__main__":
    sys.exit(main())
