#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Stress_v2 参数网格 sweep（Peak Hold + 可选 Conditional Alpha）：
在同一套 stress_v2 episodes 上做组合测试，输出 report.json / report.md 及 PASS 判定。

目标：在实验室模式下逼出分叉（diff_frames > 0），且不靠抖动（volatility_delta 可控）、不靠全程 GUARDED。
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

from tools.trace_risk_scale_step1 import run_trace_stats

REPLAY_FILENAME = "replay_output.jsonl"
BASE_DIR_DEFAULT = "library_store"
VERSION_TAG_DEFAULT = "v1.1"
STRESS_DIR_DEFAULT = "20260213/stress_v2_a3_trace"
PATCH_AGGRESSIVE = "patches/d1_aggressive.json"
PATCH_CONSERVATIVE = "patches/d1_conservative.json"

# PASS 判定
DIVERGENCE_RATE_MIN = 0.30
VOLATILITY_DELTA_MAX = 0.02
GUARDED_RATIO_DELTA_MAX = 0.15


def _parse_list(s: str, typ=float):
    if not s or not s.strip():
        return []
    return [typ(x.strip()) for x in s.split(",") if x.strip()]


def _records_seq_range(records_path) -> tuple:
    """Read first/last seq from OBS_V1 records. Returns (first_seq, last_seq) or (None, None)."""
    first_seq, last_seq = None, None
    p = Path(records_path)
    if not p.is_file():
        return (first_seq, last_seq)
    with open(p, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            try:
                r = json.loads(line)
            except json.JSONDecodeError:
                continue
            if (r.get("record_type") or "").strip() != "OBS_V1":
                continue
            seq = r.get("seq")
            if seq is None:
                continue
            if first_seq is None:
                first_seq = seq
            last_seq = seq
    return (first_seq, last_seq)


def load_decisions(bundle_path: str) -> dict:
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
            decisions[seq] = {"safety_level": dec.get("safety_level"), "control_mode": dec.get("control_mode")}
    return decisions


def compare(baseline: dict, candidate: dict) -> list:
    diff = []
    for seq in baseline:
        if baseline[seq] != candidate.get(seq):
            diff.append(seq)
    return sorted(diff)


def summarize_metrics(scorecard: dict) -> dict:
    out = {}
    if scorecard.get("diff_frames") is not None:
        out["diff_frames"] = scorecard["diff_frames"]
    if scorecard.get("first_diff_seq") is not None:
        out["first_diff_seq"] = scorecard["first_diff_seq"]
    if scorecard.get("guarded_ratio") is not None:
        out["guarded_ratio"] = scorecard["guarded_ratio"]
    if scorecard.get("early_gain") is not None:
        out["early_gain"] = scorecard["early_gain"]
    if scorecard.get("volatility") is not None:
        out["volatility"] = scorecard["volatility"]
    return out


def run_one_combo(
    base_dir: str,
    version_tag: str,
    stress_dir: str,
    episodes: list,
    combo_id: str,
    baseline_patch_path: str,
    agg_patch_path: str,
    cons_patch_path: str,
    sim_dir: str,
    first_episode_records_path: Path,
    risk_processing: dict,
    write_debug_trace: bool,
    out_dir: Path,
) -> dict:
    """跑一个 combo：baseline / aggressive / conservative 对所有 episodes，并做首 episode trace。"""
    results_per_episode = []
    for ep_id in episodes:
        episode_rel = "%s/episodes/%s/%s" % (version_tag, stress_dir.strip("/"), ep_id)
        baseline_bundle = run_episode(base_dir, version_tag, episode_rel, baseline_patch_path, sim_dir, bundle_episode_id=ep_id, mode="recompute")
        agg_bundle = run_episode(base_dir, version_tag, episode_rel, agg_patch_path, sim_dir, bundle_episode_id=ep_id, baseline_bundle_path=baseline_bundle, mode="recompute")
        cons_bundle = run_episode(base_dir, version_tag, episode_rel, cons_patch_path, sim_dir, bundle_episode_id=ep_id, baseline_bundle_path=baseline_bundle, mode="recompute")
        base_dec = load_decisions(baseline_bundle)
        agg_dec = load_decisions(agg_bundle)
        cons_dec = load_decisions(cons_bundle)
        sc_base = score(baseline_bundle, baseline_bundle)
        sc_agg = score(baseline_bundle, agg_bundle)
        sc_cons = score(baseline_bundle, cons_bundle)
        m_base = summarize_metrics(sc_base)
        m_agg = summarize_metrics(sc_agg)
        m_cons = summarize_metrics(sc_cons)
        diff_agg = compare(base_dec, agg_dec)
        diff_cons = compare(base_dec, cons_dec)
        base_gr = m_base.get("guarded_ratio") or 0
        base_vol = m_base.get("volatility") or 0
        results_per_episode.append({
            "episode": ep_id,
            "diff_frames_agg": len(diff_agg),
            "diff_frames_cons": len(diff_cons),
            "first_diff_seq_agg": min(diff_agg) if diff_agg else None,
            "first_diff_seq_cons": min(diff_cons) if diff_cons else None,
            "guarded_ratio_delta_agg": (m_agg.get("guarded_ratio") or 0) - base_gr,
            "guarded_ratio_delta_cons": (m_cons.get("guarded_ratio") or 0) - base_gr,
            "volatility_delta_agg": (m_agg.get("volatility") or 0) - base_vol,
            "volatility_delta_cons": (m_cons.get("volatility") or 0) - base_vol,
        })
    # 使用 baseline patch 对首条 episode 做 trace，得到 clamp_hit_ratio、ema_max、ema_p95
    trace_stats = run_trace_stats(first_episode_records_path, risk_processing, max_frames=0)
    if write_debug_trace and episodes and Path(baseline_patch_path).exists():
        trace_path = out_dir / ("debug_trace_%s_%s.jsonl" % (combo_id.replace(".", "_"), episodes[0]))
        import subprocess
        subprocess.run([
            sys.executable, str(ROOT / "tools" / "trace_risk_scale_step1.py"),
            "--records", str(first_episode_records_path),
            "--patch", baseline_patch_path,
            "--out-trace", str(trace_path),
        ], cwd=str(ROOT), check=False, capture_output=True)

    n_ep = len(results_per_episode)
    any_diff_agg = sum(1 for r in results_per_episode if (r["diff_frames_agg"] or 0) > 0)
    any_diff_cons = sum(1 for r in results_per_episode if (r["diff_frames_cons"] or 0) > 0)
    divergence_episodes = max(any_diff_agg, any_diff_cons)  # 至少一方有分叉的 episode 数
    divergence_rate = divergence_episodes / n_ep if n_ep else 0.0
    avg_diff_frames = (sum(r["diff_frames_agg"] or 0 for r in results_per_episode) + sum(r["diff_frames_cons"] or 0 for r in results_per_episode)) / max(1, n_ep * 2)
    first_diffs = [r["first_diff_seq_agg"] for r in results_per_episode if r.get("first_diff_seq_agg") is not None] + [r["first_diff_seq_cons"] for r in results_per_episode if r.get("first_diff_seq_cons") is not None]
    avg_first_diff_seq = sum(first_diffs) / len(first_diffs) if first_diffs else None
    vol_deltas = [r["volatility_delta_agg"] for r in results_per_episode] + [r["volatility_delta_cons"] for r in results_per_episode]
    guard_deltas = [r["guarded_ratio_delta_agg"] for r in results_per_episode] + [r["guarded_ratio_delta_cons"] for r in results_per_episode]
    avg_volatility_delta = sum(vol_deltas) / len(vol_deltas) if vol_deltas else 0.0
    avg_guarded_ratio_delta = sum(guard_deltas) / len(guard_deltas) if guard_deltas else 0.0

    trace_first_seq, trace_last_seq = _records_seq_range(first_episode_records_path)
    risk_processing_audit = {
        "peak_hold_frames": risk_processing.get("smoothing.peak_hold_frames", 0),
        "peak_decay": risk_processing.get("smoothing.peak_decay"),
        "alpha_high_enabled": risk_processing.get("smoothing.alpha_high") is not None,
        "clamp_hit_ratio": trace_stats.get("clamp_hit_ratio"),
    }
    return {
        "combo_id": combo_id,
        "risk_processing": risk_processing,
        "risk_processing_audit": risk_processing_audit,
        "divergence_rate": divergence_rate,
        "divergence_episodes": divergence_episodes,
        "n_episodes": n_ep,
        "avg_diff_frames": avg_diff_frames,
        "avg_first_diff_seq": avg_first_diff_seq,
        "avg_volatility_delta": avg_volatility_delta,
        "avg_guarded_ratio_delta": avg_guarded_ratio_delta,
        "clamp_hit_ratio": trace_stats.get("clamp_hit_ratio"),
        "ema_max": trace_stats.get("ema_max"),
        "ema_p95": trace_stats.get("ema_p95"),
        "n_frames_trace": trace_stats.get("n_frames"),
        "trace_records_path": str(first_episode_records_path.resolve()),
        "trace_frame_count": trace_stats.get("n_frames"),
        "trace_first_seq": trace_first_seq,
        "trace_last_seq": trace_last_seq,
        "per_episode": results_per_episode,
    }


def main():
    import argparse
    ap = argparse.ArgumentParser(
        description="Stress_v2 sweep: Peak Hold + optional Conditional Alpha",
        epilog="Example with debug trace (do NOT pass literal '...' as argument):\n  %(prog)s --peak-hold-frames 2 --peak-decay 0.9 --out-dir outputs/stress_v2_sweep_v2 --write-debug-trace",
    )
    ap.add_argument("--base-dir", default=BASE_DIR_DEFAULT)
    ap.add_argument("--version-tag", default=VERSION_TAG_DEFAULT)
    ap.add_argument("--stress-dir", default=STRESS_DIR_DEFAULT)
    ap.add_argument("--patch-baseline", default="", help="baseline patch path (default empty)")
    ap.add_argument("--candidates", default="aggressive,conservative")
    ap.add_argument("--risk-scale", type=float, default=5.0)
    ap.add_argument("--peak-hold-frames", default="0,1,2,3", help="comma list, e.g. 0,1,2,3")
    ap.add_argument("--peak-decay", default="0.85,0.9,0.92", help="comma list")
    ap.add_argument("--alpha-base", type=float, default=0.25)
    ap.add_argument("--alpha-high", default="", help="comma list e.g. 0.35,0.45 or empty to disable conditional")
    ap.add_argument("--alpha-switch-at", type=float, default=0.85)
    ap.add_argument("--out-dir", default="outputs/stress_v2_sweep_v2")
    ap.add_argument("--write-debug-trace", action="store_true", help="write one episode trace per combo (debug_trace_<combo>_<ep>.jsonl)")
    ap.add_argument("--print-effective-patch-keys", action="store_true", help="print effective patch key list per combo (risk_scale*, threshold*, clamp*, smoothing*)")
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

    first_episode_records = stress_path / episodes[0] / "records.jsonl"
    out_dir = Path(args.out_dir)
    if not out_dir.is_absolute():
        out_dir = ROOT / out_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    sim_dir = str(out_dir / "sim")
    (out_dir / "patches").mkdir(parents=True, exist_ok=True)
    (out_dir / "effective_patches").mkdir(parents=True, exist_ok=True)

    hold_frames_list = [int(x) for x in _parse_list(args.peak_hold_frames, float)]
    if not hold_frames_list:
        hold_frames_list = [0]
    decay_list = _parse_list(args.peak_decay)
    if not decay_list:
        decay_list = [0.9]
    alpha_high_list = _parse_list(args.alpha_high) if args.alpha_high.strip() else [None]

    combos = []
    for hold_f in hold_frames_list:
        for dec in decay_list:
            for ah in alpha_high_list:
                risk_processing = {
                    "risk_scale_factor": args.risk_scale,
                    "smoothing.peak_hold_frames": hold_f,
                    "smoothing.peak_decay": dec,
                    "smoothing.alpha": args.alpha_base,
                }
                if ah is not None:
                    risk_processing["smoothing.alpha_high"] = ah
                    risk_processing["smoothing.alpha_switch_at"] = args.alpha_switch_at
                combo_id = "hold%d_decay%g" % (hold_f, dec)
                if ah is not None:
                    combo_id += "_ah%g" % ah
                combos.append((combo_id, risk_processing))

    baseline_patch_base = {}
    if args.patch_baseline and Path(args.patch_baseline).is_file():
        with open(args.patch_baseline, "r", encoding="utf-8") as f:
            baseline_patch_base = json.load(f)

    report_rows = []
    for combo_id, risk_processing in combos:
        patch_full = {**baseline_patch_base, **risk_processing}
        patch_dir = out_dir / "patches"
        tag = combo_id.replace(".", "_")
        base_patch_path = str(patch_dir / ("%s_baseline.json" % tag))
        with open(base_patch_path, "w", encoding="utf-8") as f:
            json.dump(patch_full, f, indent=2)
        agg_patch = dict(patch_full)
        if (ROOT / PATCH_AGGRESSIVE).is_file():
            with open(ROOT / PATCH_AGGRESSIVE, "r", encoding="utf-8") as f:
                agg_patch.update(json.load(f))
        agg_patch_path = str(patch_dir / ("%s_aggressive.json" % tag))
        with open(agg_patch_path, "w", encoding="utf-8") as f:
            json.dump(agg_patch, f, indent=2)
        cons_patch = dict(patch_full)
        if (ROOT / PATCH_CONSERVATIVE).is_file():
            with open(ROOT / PATCH_CONSERVATIVE, "r", encoding="utf-8") as f:
                cons_patch.update(json.load(f))
        cons_patch_path = str(patch_dir / ("%s_conservative.json" % tag))
        with open(cons_patch_path, "w", encoding="utf-8") as f:
            json.dump(cons_patch, f, indent=2)

        # 落盘 effective_patch（与传入 sim_runner 的 baseline 一致，供 spark 复现）
        effective_patches_dir = out_dir / "effective_patches"
        effective_path = effective_patches_dir / ("%s.json" % tag)
        with open(effective_path, "w", encoding="utf-8") as f:
            json.dump(patch_full, f, ensure_ascii=False, indent=2)
        if getattr(args, "print_effective_patch_keys", False):
            keys = sorted(patch_full.keys())
            print("[sweep] effective_patch keys (%s): %s" % (combo_id, keys), flush=True)

        print("[sweep] combo=%s" % combo_id, flush=True)
        res = run_one_combo(
            base_dir,
            args.version_tag,
            args.stress_dir,
            episodes,
            combo_id,
            base_patch_path,
            agg_patch_path,
            cons_patch_path,
            sim_dir,
            first_episode_records,
            risk_processing,
            args.write_debug_trace,
            out_dir,
        )
        res["effective_patch_path"] = str(effective_path.resolve())
        report_rows.append(res)
        print("  divergence_rate=%.2f avg_vol_delta=%.4f avg_guard_delta=%.4f ema_max=%s" % (
            res["divergence_rate"], res["avg_volatility_delta"], res["avg_guarded_ratio_delta"], res.get("ema_max")), flush=True)

    # PASS 判定
    for r in report_rows:
        r["PASS"] = (
            r["divergence_rate"] >= DIVERGENCE_RATE_MIN
            and r["avg_volatility_delta"] < VOLATILITY_DELTA_MAX
            and r["avg_guarded_ratio_delta"] < GUARDED_RATIO_DELTA_MAX
        )
        if not r["PASS"]:
            reasons = []
            if r["divergence_rate"] < DIVERGENCE_RATE_MIN:
                reasons.append("分叉不足(divergence_rate<%.0f%%)" % (DIVERGENCE_RATE_MIN * 100))
            if r["avg_volatility_delta"] >= VOLATILITY_DELTA_MAX:
                reasons.append("抖动过大(volatility_delta>=%.2f)" % VOLATILITY_DELTA_MAX)
            if r["avg_guarded_ratio_delta"] >= GUARDED_RATIO_DELTA_MAX:
                reasons.append("过度保守(guarded_ratio_delta>=%.2f)" % GUARDED_RATIO_DELTA_MAX)
            r["FAIL_reason"] = "; ".join(reasons)

    report = {
        "meta": {
            "risk_scale": args.risk_scale,
            "peak_hold_frames": args.peak_hold_frames,
            "peak_decay": args.peak_decay,
            "alpha_high": args.alpha_high,
            "PASS_criteria": {
                "divergence_rate_min": DIVERGENCE_RATE_MIN,
                "volatility_delta_max": VOLATILITY_DELTA_MAX,
                "guarded_ratio_delta_max": GUARDED_RATIO_DELTA_MAX,
            },
        },
        "combos": report_rows,
        "best": max(report_rows, key=lambda x: (x["PASS"], x["divergence_rate"], -x["avg_volatility_delta"])) if report_rows else None,
    }

    report_json = out_dir / "report.json"
    with open(report_json, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print("\n[OK] report.json=%s" % report_json.resolve())

    # report.md
    md_lines = [
        "# Stress_v2 Sweep v2 Report",
        "",
        "## PASS 判定",
        "- divergence_rate >= %.0f%%" % (DIVERGENCE_RATE_MIN * 100),
        "- avg_volatility_delta < %.2f" % VOLATILITY_DELTA_MAX,
        "- avg_guarded_ratio_delta < %.2f" % GUARDED_RATIO_DELTA_MAX,
        "",
        "## Combos",
        "| combo_id | divergence_rate | avg_diff_frames | avg_volatility_delta | avg_guarded_ratio_delta | ema_max | clamp_hit_ratio | PASS |",
        "|----------|-----------------|-----------------|----------------------|--------------------------|---------|-----------------|------|",
    ]
    for r in report_rows:
        md_lines.append("| %s | %.2f | %.1f | %.4f | %.4f | %s | %s | %s |" % (
            r["combo_id"],
            r["divergence_rate"],
            r["avg_diff_frames"],
            r["avg_volatility_delta"],
            r["avg_guarded_ratio_delta"],
            r.get("ema_max") if r.get("ema_max") is not None else "-",
            r.get("clamp_hit_ratio") if r.get("clamp_hit_ratio") is not None else "-",
            "PASS" if r.get("PASS") else ("FAIL: " + r.get("FAIL_reason", "")),
        ))
    md_lines.extend(["", "## Best combo", ""])
    if report.get("best"):
        b = report["best"]
        md_lines.append("- **%s** (PASS=%s)" % (b["combo_id"], b.get("PASS")))
        md_lines.append("- risk_processing: %s" % json.dumps(b.get("risk_processing", {}), ensure_ascii=False))
    else:
        md_lines.append("(none)")
    report_md = out_dir / "report.md"
    with open(report_md, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))
    print("[OK] report.md=%s" % report_md.resolve())

    any_pass = any(r.get("PASS") for r in report_rows)
    if any_pass:
        print("[D1] 至少一个 combo PASS，可进入 D1。")
    else:
        print("[D1] 无 combo PASS，见 FAIL_reason。")
    return 0 if any_pass else 1


if __name__ == "__main__":
    sys.exit(main())
