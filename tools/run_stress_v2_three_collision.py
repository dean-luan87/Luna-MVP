#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Stress_v2 三体对撞：用 9 条 slice 跑 baseline / aggressive / conservative 三候选，
输出 diff_frames、early_gain、guarded_ratio_delta、volatility_delta，验证 D1 是否被激活。

三 patch（单维度 risk_density）：
  - baseline: 默认权重（无 patch）
  - aggressive: risk_density × 2 (0.6)
  - conservative: risk_density × 0.5 (0.15)
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from simulation.logic.scorer import score
from simulation.sim_runner import run_episode

REPLAY_FILENAME = "replay_output.jsonl"
DEFAULT_RISK_DENSITY = 0.30


def _resolve_episodes_dir(episodes_dir_arg: str) -> Path:
    """与 validate_stress_v2_quality 一致：支持 YYYYMMDD 占位符。"""
    from datetime import datetime, timezone

    episodes_dir = episodes_dir_arg
    if "YYYYMMDD" in episodes_dir:
        today = datetime.now(timezone.utc).strftime("%Y%m%d")
        try_dir = episodes_dir.replace("YYYYMMDD", today)
        base = ROOT / try_dir if not Path(try_dir).is_absolute() else Path(try_dir)
        if not base.exists():
            parts = Path(episodes_dir).parts
            if "episodes" in parts:
                idx = list(parts).index("episodes")
                prefix = Path(*parts[: idx + 1])
                stem = Path(episodes_dir).name
                if not prefix.is_absolute():
                    prefix = ROOT / prefix
                if prefix.exists():
                    dates = sorted(
                        [p.name for p in prefix.iterdir() if p.is_dir() and p.name.isdigit()],
                        reverse=True,
                    )
                    for d in dates:
                        cand = prefix / d / stem
                        if cand.exists():
                            base = cand
                            episodes_dir = str(cand)
                            break
        if not base.exists():
            base = ROOT / episodes_dir if not Path(episodes_dir).is_absolute() else Path(episodes_dir)
    else:
        base = Path(episodes_dir)
        if not base.is_absolute():
            base = ROOT / base
    if not base.exists():
        raise SystemExit("episodes-dir not found: %s" % base)
    return base


def _load_replay_decisions(bundle_path: str) -> list:
    path = os.path.join(bundle_path.rstrip("/"), REPLAY_FILENAME)
    out = []
    if not os.path.isfile(path):
        return out
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            rec = json.loads(line)
            dec = rec.get("decision") or {}
            out.append({
                "seq": rec.get("seq"),
                "safety_level": dec.get("safety_level"),
                "control_mode": dec.get("control_mode"),
            })
    return out


def _diff_frames(base_dec: list, cand_dec: list) -> int:
    n = max(len(base_dec), len(cand_dec))
    diff = 0
    for i in range(n):
        b = base_dec[i] if i < len(base_dec) else {}
        c = cand_dec[i] if i < len(cand_dec) else {}
        if (b.get("control_mode") != c.get("control_mode")) or (b.get("safety_level") != c.get("safety_level")):
            diff += 1
    return diff


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Stress_v2 三候选对撞：baseline / aggressive(risk_density×2) / conservative(×0.5)，输出分叉统计。"
    )
    ap.add_argument(
        "--episodes-dir",
        required=True,
        help="e.g. library_store/v1.1/episodes/YYYYMMDD/stress_v2_a3_trace",
    )
    ap.add_argument(
        "--base-dir",
        default="library_store",
        help="library_store 根目录（与 episodes-dir 中一致）",
    )
    ap.add_argument(
        "--out-dir",
        default="",
        help="sim 输出目录，默认 outputs/<version>/stress_v2_collision",
    )
    ap.add_argument(
        "--risk-mult-aggressive",
        type=float,
        default=2.0,
        help="aggressive 的 risk_density 倍数（默认 2）",
    )
    ap.add_argument(
        "--risk-mult-conservative",
        type=float,
        default=0.5,
        help="conservative 的 risk_density 倍数（默认 0.5）",
    )
    args = ap.parse_args()

    episodes_dir = _resolve_episodes_dir(args.episodes_dir)
    # base_dir：library_store 的绝对路径；version 与 episode_rel 前缀从路径解析
    # episodes_dir = .../library_store/v1.1/episodes/YYYYMMDD/stress_v2_xxx
    base_dir = args.base_dir.rstrip("/")
    if not Path(base_dir).is_absolute():
        base_dir = str(ROOT / base_dir)
    if not os.path.isdir(base_dir):
        print("ERROR: base-dir not found:", base_dir, file=sys.stderr)
        return 2

    # version_tag = v1.1；episode_rel 前缀 = v1.1/episodes/<date>/<stress_name>
    try:
        # .../library_store/v1.1/episodes/20260213/stress_v2_a3_trace
        version_tag = episodes_dir.parent.parent.parent.name
        date_dir = episodes_dir.parent.name
        stress_name = episodes_dir.name
        rel_prefix = f"{version_tag}/episodes/{date_dir}/{stress_name}"
    except Exception:
        print("ERROR: could not infer version/rel from episodes-dir:", episodes_dir, file=sys.stderr)
        return 2

    slice_dirs = sorted(
        [p for p in episodes_dir.iterdir() if p.is_dir() and (p / "records.jsonl").exists()]
    )
    if not slice_dirs:
        print("ERROR: no slice episodes under", episodes_dir, file=sys.stderr)
        return 2

    out_dir = args.out_dir.strip() or os.path.join("outputs", version_tag, "stress_v2_collision")
    os.makedirs(out_dir, exist_ok=True)

    # 临时 patch 文件（仅 risk_density）
    w_agg = DEFAULT_RISK_DENSITY * args.risk_mult_aggressive
    w_cons = DEFAULT_RISK_DENSITY * args.risk_mult_conservative
    with tempfile.TemporaryDirectory(prefix="stress_v2_patches_") as tmp:
        aggressive_patch = os.path.join(tmp, "aggressive.json")
        conservative_patch = os.path.join(tmp, "conservative.json")
        with open(aggressive_patch, "w", encoding="utf-8") as f:
            json.dump({"weights.risk_density": w_agg}, f)
        with open(conservative_patch, "w", encoding="utf-8") as f:
            json.dump({"weights.risk_density": w_cons}, f)

        results = []
        for slice_dir in slice_dirs:
            slice_id = slice_dir.name
            episode_rel_path = f"{rel_prefix}/{slice_id}"

            # 1) baseline
            baseline_bundle = run_episode(
                base_dir, version_tag, episode_rel_path, "",
                out_dir, bundle_episode_id=slice_id, mode="recompute",
            )
            # 2) aggressive
            agg_bundle = run_episode(
                base_dir, version_tag, episode_rel_path, aggressive_patch,
                out_dir, bundle_episode_id=slice_id, baseline_bundle_path=baseline_bundle, mode="recompute",
            )
            # 3) conservative
            cons_bundle = run_episode(
                base_dir, version_tag, episode_rel_path, conservative_patch,
                out_dir, bundle_episode_id=slice_id, baseline_bundle_path=baseline_bundle, mode="recompute",
            )

            base_dec = _load_replay_decisions(baseline_bundle)
            agg_dec = _load_replay_decisions(agg_bundle)
            cons_dec = _load_replay_decisions(cons_bundle)

            diff_frames_agg = _diff_frames(base_dec, agg_dec)
            diff_frames_cons = _diff_frames(base_dec, cons_dec)

            sc_baseline = score(baseline_bundle, baseline_bundle)
            sc_agg = score(baseline_bundle, agg_bundle)
            sc_cons = score(baseline_bundle, cons_bundle)

            vol_baseline = sc_baseline.get("volatility_index") or 0.0
            early_agg = sc_agg.get("early_conservative_action_gain")
            early_cons = sc_cons.get("early_conservative_action_gain")
            gr_agg = (sc_agg.get("efficiency") or {}).get("guarded_ratio_delta")
            gr_cons = (sc_cons.get("efficiency") or {}).get("guarded_ratio_delta")
            vol_agg = sc_agg.get("volatility_index") or 0.0
            vol_cons = sc_cons.get("volatility_index") or 0.0
            volatility_delta_agg = (vol_agg - vol_baseline) if vol_baseline is not None else None
            volatility_delta_cons = (vol_cons - vol_baseline) if vol_baseline is not None else None

            results.append({
                "slice_id": slice_id,
                "diff_frames_agg": diff_frames_agg,
                "diff_frames_cons": diff_frames_cons,
                "early_gain_agg": early_agg,
                "early_gain_cons": early_cons,
                "guarded_ratio_delta_agg": gr_agg,
                "guarded_ratio_delta_cons": gr_cons,
                "volatility_delta_agg": volatility_delta_agg,
                "volatility_delta_cons": volatility_delta_cons,
                "frames": len(base_dec),
            })

        # 输出
        print("=== STRESS_V2 THREE-COLLISION ===")
        print("episodes_dir=%s slices=%d" % (episodes_dir, len(results)))
        print("patches: baseline(default) | aggressive(risk_density=%.2f) | conservative(%.2f)" % (w_agg, w_cons))
        print("-" * 100)
        print(
            "%-32s | diff_agg diff_cons | early_agg early_cons | gr_delta_agg gr_delta_cons | vol_delta_agg vol_delta_cons | frames"
            % "slice_id"
        )
        print("-" * 100)

        any_diff = False
        for r in results:
            any_diff = any_diff or (r["diff_frames_agg"] > 0 or r["diff_frames_cons"] > 0)
            print(
                "%-32s | %7d %9d | %9s %10s | %11s %12s | %12s %13s | %d"
                % (
                    r["slice_id"][:32],
                    r["diff_frames_agg"],
                    r["diff_frames_cons"],
                    str(r["early_gain_agg"]) if r["early_gain_agg"] is not None else "-",
                    str(r["early_gain_cons"]) if r["early_gain_cons"] is not None else "-",
                    str(r["guarded_ratio_delta_agg"]) if r["guarded_ratio_delta_agg"] is not None else "-",
                    str(r["guarded_ratio_delta_cons"]) if r["guarded_ratio_delta_cons"] is not None else "-",
                    str(r["volatility_delta_agg"]) if r["volatility_delta_agg"] is not None else "-",
                    str(r["volatility_delta_cons"]) if r["volatility_delta_cons"] is not None else "-",
                    r["frames"],
                )
            )

        print("-" * 100)
        total_diff_agg = sum(r["diff_frames_agg"] for r in results)
        total_diff_cons = sum(r["diff_frames_cons"] for r in results)
        print("total diff_frames (vs aggressive): %d" % total_diff_agg)
        print("total diff_frames (vs conservative): %d" % total_diff_cons)

        if any_diff:
            print("[D1] 情况 A：出现分叉（diff_frames > 0），stress_v2 成功把 A3 推到边缘区，D1 已激活。")
        else:
            print(
                "[D1] 情况 B：仍为 0。A3 风险尺度处于线性安全区，stress_v2 的 p95 尚未触及决策阈值；可考虑阈值/尺度再校准。"
            )

        # 方向性：aggressive 是否更保守（guarded_ratio_delta 更大 / early_gain 更高）
        gr_agg_vals = [r["guarded_ratio_delta_agg"] for r in results if r["guarded_ratio_delta_agg"] is not None]
        gr_cons_vals = [r["guarded_ratio_delta_cons"] for r in results if r["guarded_ratio_delta_cons"] is not None]
        if gr_agg_vals and gr_cons_vals:
            mean_gr_agg = sum(gr_agg_vals) / len(gr_agg_vals)
            mean_gr_cons = sum(gr_cons_vals) / len(gr_cons_vals)
            print("guarded_ratio_delta mean: aggressive=%.4f conservative=%.4f (aggressive > conservative => 方向一致)" % (mean_gr_agg, mean_gr_cons))

        report_path = Path(out_dir) / "collision_report.json"
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "episodes_dir": str(episodes_dir),
                    "any_diff": any_diff,
                    "total_diff_agg": total_diff_agg,
                    "total_diff_cons": total_diff_cons,
                    "results": results,
                },
                f,
                ensure_ascii=False,
                indent=2,
            )
        print("[OK] report=%s" % report_path.resolve())

    return 0


if __name__ == "__main__":
    sys.exit(main())
