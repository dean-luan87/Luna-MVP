#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Stress_v2 分叉测试：验证 stress_v2 是否把 A3 推到决策边缘，产生 D1 分叉。

目标：只看是否产生决策差异，不看 PASS/FAIL / Gate。
输出五指标：diff_frames, first_diff_seq, guarded_ratio_delta, early_gain_delta, volatility_delta。

三候选：baseline(empty) | aggressive(risk×2) | conservative(risk×0.5)。
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from simulation.logic.scorer import score
from simulation.sim_runner import run_episode

REPLAY_FILENAME = "replay_output.jsonl"

# 默认路径（可被 CLI 覆盖）
BASE_DIR = "library_store"
VERSION_TAG = "v1.1"
STRESS_DIR = "20260213/stress_v2_a3_trace"

PATCHES = {
    "baseline": "",  # 无 patch，run_episode 用 ""
    "aggressive": "patches/d1_aggressive.json",
    "conservative": "patches/d1_conservative.json",
}


def _patch_path(name: str) -> str:
    if name == "baseline":
        return ""
    p = ROOT / PATCHES[name]
    return str(p) if p.is_file() else ""


def _merge_scale_patches(output_root: Path, risk_scale: float) -> tuple:
    """当 --risk-scale 时：写 baseline/aggressive/conservative 的合并 patch 到 output_root/patches/，返回 (baseline_path, agg_path, cons_path)。"""
    patch_dir = output_root / "patches"
    patch_dir.mkdir(parents=True, exist_ok=True)
    scale_only = {"risk_scale_factor": risk_scale}
    tag = ("%g" % risk_scale).replace(".", "_")
    base_path = patch_dir / ("baseline_scale%s.json" % tag)
    with open(base_path, "w", encoding="utf-8") as f:
        json.dump(scale_only, f, indent=2)
    agg_src = ROOT / PATCHES["aggressive"]
    agg_merged = {**scale_only}
    if agg_src.is_file():
        with open(agg_src, "r", encoding="utf-8") as f:
            agg_merged.update(json.load(f))
    agg_path = patch_dir / ("aggressive_scale%s.json" % tag)
    with open(agg_path, "w", encoding="utf-8") as f:
        json.dump(agg_merged, f, indent=2)
    cons_src = ROOT / PATCHES["conservative"]
    cons_merged = {**scale_only}
    if cons_src.is_file():
        with open(cons_src, "r", encoding="utf-8") as f:
            cons_merged.update(json.load(f))
    cons_path = patch_dir / ("conservative_scale%s.json" % tag)
    with open(cons_path, "w", encoding="utf-8") as f:
        json.dump(cons_merged, f, indent=2)
    return str(base_path), str(agg_path), str(cons_path)


def load_decisions(bundle_path: str) -> dict:
    """从 bundle 的 replay_output.jsonl 读出 seq -> decision（用于比较）。"""
    path = os.path.join(bundle_path.rstrip("/"), REPLAY_FILENAME)
    decisions = {}
    if not os.path.isfile(path):
        return decisions
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            try:
                r = json.loads(line)
            except json.JSONDecodeError:
                continue
            seq = r.get("seq")
            if seq is None:
                continue
            dec = r.get("decision") or {}
            # 只比较影响决策的字段
            decisions[seq] = {
                "safety_level": dec.get("safety_level"),
                "control_mode": dec.get("control_mode"),
            }
    return decisions


def compare(baseline: dict, candidate: dict) -> list:
    """返回与 baseline 决策不同的 seq 列表（按 seq 排序，first_diff 即首项）。"""
    diff = []
    for seq in baseline:
        if baseline[seq] != candidate.get(seq):
            diff.append(seq)
    return sorted(diff)


def summarize_metrics(scorecard: dict) -> dict:
    """从 scorecard 抽出 guarded_ratio / early_gain / volatility（与现有 scorer 结构一致）。"""
    eff = scorecard.get("efficiency") or {}
    return {
        "guarded_ratio": eff.get("guarded_ratio_candidate"),
        "early_gain": scorecard.get("early_conservative_action_gain"),
        "volatility": scorecard.get("volatility_index"),
    }


def main() -> int:
    import argparse
    ap = argparse.ArgumentParser(description="Stress_v2 三候选分叉测试：diff_frames / first_diff_seq / guarded_ratio_delta / early_gain_delta / volatility_delta")
    ap.add_argument("--base-dir", default=BASE_DIR, help="library_store 根目录")
    ap.add_argument("--version-tag", default=VERSION_TAG)
    ap.add_argument("--stress-dir", default=STRESS_DIR, help="e.g. 20260213/stress_v2_a3_trace")
    ap.add_argument("--out-dir", default=None, help="默认 outputs/stress_v2_divergence")
    ap.add_argument("--risk-scale", type=float, default=None, metavar="F", help="量纲校准：risk_scale_factor，如 5.0；与 baseline/aggressive/conservative 合并后跑")
    args = ap.parse_args()

    base_dir = args.base_dir.rstrip("/")
    if not Path(base_dir).is_absolute():
        base_dir = str(ROOT / base_dir)
    if not os.path.isdir(base_dir):
        print("ERROR: base-dir not found:", base_dir, file=sys.stderr)
        return 2

    stress_path = Path(base_dir) / args.version_tag / "episodes" / args.stress_dir
    if not stress_path.is_dir():
        print("ERROR: stress dir not found:", stress_path, file=sys.stderr)
        return 2

    episodes = sorted([p.name for p in stress_path.iterdir() if p.is_dir() and (p / "records.jsonl").exists()])
    if not episodes:
        print("ERROR: no slice episodes under", stress_path, file=sys.stderr)
        return 2

    output_root = Path(args.out_dir or os.path.join(ROOT, "outputs", "stress_v2_divergence"))
    output_root.mkdir(parents=True, exist_ok=True)
    sim_dir = str(output_root)
    # run_episode 会在 sim_dir 下创建 bundle 子目录

    if args.risk_scale is not None:
        baseline_patch, agg_patch, cons_patch = _merge_scale_patches(output_root, args.risk_scale)
        print("[risk_scale=%.1f] 已合并 patch：baseline=%s aggressive=%s conservative=%s" % (args.risk_scale, baseline_patch, agg_patch, cons_patch), flush=True)
    else:
        baseline_patch = ""
        agg_patch = _patch_path("aggressive")
        cons_patch = _patch_path("conservative")

    results = []

    for ep_id in episodes:
        print("\n=== Episode: %s ===" % ep_id, flush=True)
        episode_rel = "%s/episodes/%s/%s" % (args.version_tag, args.stress_dir.strip("/"), ep_id)

        # 1) baseline
        baseline_bundle = run_episode(
            base_dir,
            args.version_tag,
            episode_rel,
            baseline_patch,
            sim_dir,
            bundle_episode_id=ep_id,
            mode="recompute",
        )
        # 2) aggressive
        agg_bundle = run_episode(
            base_dir,
            args.version_tag,
            episode_rel,
            agg_patch,
            sim_dir,
            bundle_episode_id=ep_id,
            baseline_bundle_path=baseline_bundle,
            mode="recompute",
        )
        # 3) conservative
        cons_bundle = run_episode(
            base_dir,
            args.version_tag,
            episode_rel,
            cons_patch,
            sim_dir,
            bundle_episode_id=ep_id,
            baseline_bundle_path=baseline_bundle,
            mode="recompute",
        )

        baseline_dec = load_decisions(baseline_bundle)
        agg_dec = load_decisions(agg_bundle)
        cons_dec = load_decisions(cons_bundle)

        # Scorecards：baseline 自身 + baseline vs aggressive / baseline vs conservative
        sc_baseline = score(baseline_bundle, baseline_bundle)
        sc_agg = score(baseline_bundle, agg_bundle)
        sc_cons = score(baseline_bundle, cons_bundle)

        scorecards = {
            "baseline": summarize_metrics(sc_baseline),
            "aggressive": summarize_metrics(sc_agg),
            "conservative": summarize_metrics(sc_cons),
        }

        for name, cand_dec in [("aggressive", agg_dec), ("conservative", cons_dec)]:
            diffs = compare(baseline_dec, cand_dec)
            first_diff_seq = min(diffs) if diffs else None

            gr_base = scorecards["baseline"].get("guarded_ratio")
            gr_cand = scorecards[name].get("guarded_ratio")
            guarded_ratio_delta = (gr_cand - gr_base) if gr_base is not None and gr_cand is not None else None

            eg_base = scorecards["baseline"].get("early_gain") or 0.0
            eg_cand = scorecards[name].get("early_gain")
            early_gain_delta = (eg_cand - eg_base) if eg_cand is not None else None

            vol_base = scorecards["baseline"].get("volatility")
            vol_cand = scorecards[name].get("volatility")
            volatility_delta = (vol_cand - vol_base) if vol_base is not None and vol_cand is not None else None

            result = {
                "episode": ep_id,
                "candidate": name,
                "diff_frames": len(diffs),
                "first_diff_seq": first_diff_seq,
                "guarded_ratio_delta": guarded_ratio_delta,
                "early_gain_delta": early_gain_delta,
                "volatility_delta": volatility_delta,
            }
            print(result, flush=True)
            results.append(result)

    summary_path = output_root / "summary.json"
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print("\n[OK] summary=%s" % summary_path.resolve())

    any_diff = any(r["diff_frames"] > 0 for r in results)
    if any_diff:
        print("[D1] 出现分叉（至少一条 slice diff_frames > 0），D1 已激活。")
    else:
        print("[D1] 所有 diff_frames = 0：stress_v2 仍不足以推动 A3 跨越决策边界，应动 risk_score 量纲。")

    return 0


if __name__ == "__main__":
    sys.exit(main())
