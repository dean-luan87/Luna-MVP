#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
D2.2 对抗验证：跑完 blind_patch suite 后，根据 suite_report + scorecard 摘要输出审计点。
用于判定 D2.3 是否立刻入场。
"""
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    import argparse
    p = argparse.ArgumentParser(description="Audit blind_patch suite result for D2.3 entry decision")
    p.add_argument("--suite-report", default="", help="Path to suite_report.json (default: latest under outputs/v1.1/sim_suites/)")
    p.add_argument("--out-dir", default=os.path.join(ROOT, "outputs", "v1.1"))
    args = p.parse_args()
    out = Path(args.out_dir)
    if args.suite_report:
        report_path = Path(args.suite_report)
    else:
        suite_dir = out / "sim_suites"
        if not suite_dir.is_dir():
            print("No sim_suites dir:", suite_dir)
            return 1
        subs = sorted(suite_dir.iterdir(), key=lambda p: p.stat().st_mtime, reverse=True)
        if not subs:
            print("No suite runs found under", suite_dir)
            return 1
        report_path = subs[0] / "suite_report.json"
    if not report_path.is_file():
        print("Suite report not found:", report_path)
        return 1
    with open(report_path, "r", encoding="utf-8") as f:
        report = json.load(f)
    print("=== D2.2/D2.3 对抗验证审计 ===\nSuite:", report_path)
    print("Patch:", report.get("patch"))
    print("Overall:", "PASS" if report.get("overall") else "FAIL")
    print("Missing buckets:", report.get("missing_buckets", []))
    per = report.get("per_episode") or {}
    any_degradation = False
    print("\n--- D2.3 Perception 审计 ---")
    for eid in sorted(per.keys()):
        ep = per[eid]
        if not isinstance(ep, dict):
            continue
        scorecard_path = ep.get("scorecard_path")
        if not scorecard_path:
            print(f"  [WARN] missing scorecard_path for {ep.get('episode_id', eid)}")
            continue
        sc_path = Path(scorecard_path)
        if not sc_path.is_file():
            print(f"  [WARN] scorecard not found: {scorecard_path}")
            continue
        try:
            sc = json.loads(sc_path.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"  [WARN] failed to load {scorecard_path}: {e}")
            continue
        perc = sc.get("perception") or {}
        dr = perc.get("degradation_rate", 0)
        if dr > 0:
            any_degradation = True
        passed = ep.get("passed", False)
        print(f"  {eid}: degradation_rate={dr:.4f}" + (" PASS" if passed else " FAIL"))
        if not passed:
            examples = (perc.get("degradation_examples") or [])[:3]
            if examples:
                print(f"    degradation_examples (first 3): {examples}")
    if report.get("overall") and any_degradation:
        print("\n>>> 警告：overall=PASS 但存在 perception.degradation_rate>0 → Gate 配置错误或接线错误，应使 blind_patch FAIL。")
    print("\n--- 审计点 1：Early Gain 坍塌 ---")
    print("(需结合各 episode scorecard 看 early_conservative_action_gain；若 blind_patch 下趋近 0 或比 baseline 更晚 GUARDED → 语义崩坏)")
    print("\n--- 审计点 2：Lookahead 异常平稳 ---")
    print("(需结合 scorecard 的 lookahead_drop_ratio；若为负且 candidate 未缩短前瞻 → 眼瞎刷效率)")
    print("\n--- 审计点 3：Regression 语义漏洞 ---")
    print("(若 overall=PASS 且 baseline 有 CAUTION 的片段被 candidate 抹成 SAFE、且无 GUARDED/短 lookahead → 漏洞成立，立刻 D2.3)")
    all_passed = all((per.get(eid) or {}).get("passed", False) for eid in per)
    if all_passed and per and not any_degradation:
        print("\n>>> 当前 Suite 所有 episode Gate 均为 PASS，且无感知退化。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
