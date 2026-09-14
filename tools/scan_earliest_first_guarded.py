#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
扫出 run 里「最早进入 GUARDED」的候选：从 stress_responsive 的 candidate_replay 读绝对 seq，
按各 patch 所有 episode 中「第一次 GUARDED 的 seq」的最小值排序，找 first_guarded_seq < 3961 的赢家。
用法: python3 tools/scan_earliest_first_guarded.py outputs/d1_runs/phase2_production_lock/20260216073053
"""
import json
import sys
from pathlib import Path


def first_guarded_seq_from_replay(replay_path: str):
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
            if (r.get("decision") or {}).get("control_mode") == "GUARDED":
                return r.get("seq")
    return None


def main():
    if len(sys.argv) < 2:
        print("usage: python3 tools/scan_earliest_first_guarded.py <run_dir>", file=sys.stderr)
        sys.exit(2)
    run_dir = Path(sys.argv[1]).resolve()
    if not run_dir.is_dir():
        print("run_dir not found:", run_dir, file=sys.stderr)
        sys.exit(1)

    report_path = run_dir / "rank_report.json"
    if not report_path.is_file():
        print("rank_report.json not found", file=sys.stderr)
        sys.exit(1)
    d = json.loads(report_path.read_text(encoding="utf-8"))
    ranked = d.get("ranked") or []

    rows = []
    for r in ranked:
        pid = r.get("patch_id", "")
        suite_path = run_dir / pid / "suite_report.stress_responsive.json"
        if not suite_path.is_file():
            rows.append((None, pid, (r.get("stress_metrics") or {}).get("early_gain_weighted_mean")))
            continue
        per = (json.loads(suite_path.read_text(encoding="utf-8")) or {}).get("per_episode") or {}
        seqs = []
        for ep_id, ep_data in per.items():
            replay_path = ep_data.get("candidate_replay_path")
            if not replay_path:
                continue
            seq = first_guarded_seq_from_replay(replay_path)
            if seq is not None:
                seqs.append(seq)
        best = min(seqs) if seqs else None
        eg = (r.get("stress_metrics") or {}).get("early_gain_weighted_mean")
        rows.append((best, pid, eg))

    # 最小 first_guarded seq 排前（None 视为无穷大）
    rows.sort(key=lambda x: (10**18 if x[0] is None else x[0], x[1]))
    print("Top candidates by earliest first_guarded seq (from replay; None = never GUARDED):")
    print("  baseline reference: first_guarded seq=3961 in episode 0350aa9041e7555b")
    for i, (fg, pid, eg) in enumerate(rows[:20], 1):
        mark = "  <-- earlier than 3961!" if fg is not None and fg < 3961 else ""
        print("  %2d. first_guarded_seq=%s  patch=%s  early_gain_mean=%s%s" % (i, fg, pid, eg, mark))
    earlier = [x for x in rows if x[0] is not None and x[0] < 3961]
    if earlier:
        print("\n[OK] %d patch(es) with first_guarded_seq < 3961 (positive gradient)." % len(earlier))
    else:
        print("\n[--] No patch with first_guarded_seq < 3961; narrow alpha band and/or add peak_hold.")


if __name__ == "__main__":
    main()
