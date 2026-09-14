#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A/B 判死：early_gain 全员同分是 (A) 真实平台期 还是 (B) 指标链路偷懒。
Step 1: 确认 stress_responsive 报告存在
Step 2: baseline vs 一候选，同集 per_episode/scorecard 的 first_guarded / early_gain_weighted 对照
Step 3: 从 replay 复算 first_guarded，与 report 对比
用法: python3 tools/diagnose_early_gain_ab.py outputs/d1_runs/phase2_production_lock/20260216071808
"""
import json
import os
import sys
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("usage: python3 tools/diagnose_early_gain_ab.py <run_dir>", file=sys.stderr)
        sys.exit(2)
    run_dir = Path(sys.argv[1]).resolve()
    if not run_dir.is_dir():
        print("run_dir not found:", run_dir, file=sys.stderr)
        sys.exit(1)

    cands = ["baseline", "d1_candidate_000"]
    # Step 1
    print("[Step 1] stress_responsive 报告")
    for c in cands:
        p = run_dir / c / "suite_report.stress_responsive.json"
        print("  %s: %s" % (c, "OK" if p.is_file() else "MISSING"))
    baseline_rep = run_dir / "baseline" / "suite_report.stress_responsive.json"
    cand_rep = run_dir / "d1_candidate_000" / "suite_report.stress_responsive.json"
    if not baseline_rep.is_file() or not cand_rep.is_file():
        print("[Step 1] 缺少 stress_responsive 报告，先修链路。")
        sys.exit(1)

    # Step 2: 从各候选的 suite_report -> per_episode -> scorecard_path 读 early 块
    print("\n[Step 2] baseline vs d1_candidate_000 同集 scorecard early 对照（前 5 集）")
    base_per = json.loads(baseline_rep.read_text(encoding="utf-8")).get("per_episode") or {}
    cand_per = json.loads(cand_rep.read_text(encoding="utf-8")).get("per_episode") or {}
    ep_ids = sorted(set(base_per.keys()) & set(cand_per.keys()))[:5]
    if not ep_ids:
        print("  无共同 episode_id")
        sys.exit(1)
    for ep in ep_ids:
        print("\n  EP: %s" % ep)
        for pid in cands:
            per = base_per if pid == "baseline" else cand_per
            ep_data = per.get(ep) or {}
            sc_path = ep_data.get("scorecard_path")
            if not sc_path or not Path(sc_path).is_file():
                print("    %s: no scorecard" % pid)
                continue
            sc = json.loads(Path(sc_path).read_text(encoding="utf-8"))
            early = sc.get("early") or {}
            fg_b = early.get("baseline_first_guarded_in_high_risk")
            fg_c = early.get("candidate_first_guarded_in_high_risk")
            eg = early.get("early_gain_weighted")
            hr = early.get("high_risk_seq_count")
            print("    %s: first_guarded_baseline=%s candidate=%s early_gain_weighted=%s high_risk_seq_count=%s" % (pid, fg_b, fg_c, eg, hr))

    # Step 3: 从 replay 复算 first_guarded（candidate 轨）
    print("\n[Step 3] 从 replay 复算 first_guarded（同集 0350aa9041e7555b）")
    ep = ep_ids[0]
    base_ep = base_per.get(ep) or {}
    cand_ep = cand_per.get(ep) or {}

    def first_guarded_seq(replay_path: str):
        p = Path(replay_path)
        if not p.is_file():
            return None
        with open(p, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    r = json.loads(line)
                except Exception:
                    continue
                d = r.get("decision") or {}
                if d.get("control_mode") == "GUARDED":
                    return r.get("seq")
        return None

    base_replay_b = base_ep.get("baseline_replay_path")
    base_replay_c = base_ep.get("candidate_replay_path")
    cand_replay_b = cand_ep.get("baseline_replay_path")
    cand_replay_c = cand_ep.get("candidate_replay_path")
    print("  baseline 的 baseline_replay  first_guarded seq:", first_guarded_seq(base_replay_b or ""))
    print("  baseline 的 candidate_replay first_guarded seq:", first_guarded_seq(base_replay_c or ""))
    print("  d1_candidate_000 的 baseline_replay  first_guarded seq:", first_guarded_seq(cand_replay_b or ""))
    print("  d1_candidate_000 的 candidate_replay first_guarded seq:", first_guarded_seq(cand_replay_c or ""))

    # 判定
    base_cand_seq = first_guarded_seq(base_replay_c or "")
    cand_cand_seq = first_guarded_seq(cand_replay_c or "")
    base_sc = json.loads(Path(base_ep.get("scorecard_path")).read_text(encoding="utf-8"))
    cand_sc = json.loads(Path(cand_ep.get("scorecard_path")).read_text(encoding="utf-8"))
    base_eg = (base_sc.get("early") or {}).get("early_gain_weighted")
    cand_eg = (cand_sc.get("early") or {}).get("early_gain_weighted")
    print("\n[判死]")
    if base_cand_seq != cand_cand_seq:
        print("  replay 层面: baseline candidate 与 d1_candidate_000 candidate 的 first_guarded 不同 -> 有差异信号")
        if base_eg == cand_eg:
            print("  report 层面: early_gain_weighted 却相同 -> B) 指标链路偷懒/取错来源")
        else:
            print("  report 层面: early_gain_weighted 也不同 -> 链路正常，需查聚合")
    else:
        print("  replay 层面: 两 candidate 的 first_guarded 相同 -> 权重未改变进入 Guarded 的帧")
        if base_eg == cand_eg:
            print("  report 层面: early_gain_weighted 也相同 -> A) 真实平台期（候选空间对 early_gain 不敏感）")
        else:
            print("  report 层面: early_gain_weighted 不同 -> 异常，early_gain 计算或来源需查")


if __name__ == "__main__":
    main()
