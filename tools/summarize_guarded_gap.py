#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Guarded 机制取证：统计 stress replay 目录下 control_mode 分布、risk/a3_debug 统计、
是否存在 guarded 阈值/计数器，以及单 replay 的连续 run length。
输出：guarded_gap_report.json + 终端摘要。
"""
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def load_jsonl(path: Path) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    if not path.is_file():
        return out
    for line in path.read_text(encoding="utf-8").strip().splitlines():
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return out


def collect_stress_replays(dir_root: Path) -> List[Path]:
    """收集目录下所有 *_stress* 的 replay_output.jsonl。"""
    dir_root = Path(dir_root)
    if not dir_root.is_dir():
        return []
    files: List[Path] = []
    for f in dir_root.rglob("replay_output.jsonl"):
        if "_stress" in str(f):
            files.append(f)
    return sorted(files)


def run_lengths(risks: List[float], thr: float) -> List[int]:
    """连续 risk >= thr 的每段长度。"""
    lengths: List[int] = []
    n = 0
    for r in risks:
        if r >= thr:
            n += 1
        else:
            if n:
                lengths.append(n)
            n = 0
    if n:
        lengths.append(n)
    return lengths


def summarize_one_replay(records: List[Dict[str, Any]]) -> Dict[str, Any]:
    control_counts: Dict[str, int] = {}
    risk_all: List[float] = []
    risk_high: List[float] = []
    ema_all: List[float] = []
    peak_hold_all: List[float] = []
    x_hold_all: List[float] = []
    a3_debug_keys: Optional[List[str]] = None

    for r in records:
        dec = r.get("decision") or {}
        mode = (dec.get("control_mode") or "").strip().upper() or "UNKNOWN"
        control_counts[mode] = control_counts.get(mode, 0) + 1

        risk = r.get("risk_used_for_decision")
        if risk is not None:
            try:
                v = float(risk)
                risk_all.append(v)
                if r.get("high_risk") is True or v >= 0.38:
                    risk_high.append(v)
            except (TypeError, ValueError):
                pass

        ad = dec.get("a3_debug") or {}
        if isinstance(ad, dict):
            if a3_debug_keys is None:
                a3_debug_keys = sorted(ad.keys())
            ema = ad.get("ema")
            if ema is not None:
                try:
                    ema_all.append(float(ema))
                except (TypeError, ValueError):
                    pass
            ph = ad.get("peak_hold_value")
            if ph is not None:
                try:
                    peak_hold_all.append(float(ph))
                except (TypeError, ValueError):
                    pass
            xh = ad.get("x_hold")
            if xh is not None:
                try:
                    x_hold_all.append(float(xh))
                except (TypeError, ValueError):
                    pass

    def stats(vals: List[float]) -> Dict[str, float]:
        if not vals:
            return {"max": None, "p95": None, "mean": None}
        s = sorted(vals)
        n = len(s)
        p95_i = min(int(n * 0.95), n - 1) if n else 0
        return {
            "max": round(max(vals), 4),
            "p95": round(s[p95_i], 4),
            "mean": round(sum(vals) / n, 4),
        }

    return {
        "control_mode_counts": control_counts,
        "risk_used_for_decision_all": stats(risk_all),
        "risk_used_for_decision_high_risk_frames": stats(risk_high),
        "a3_debug_ema_max": max(ema_all) if ema_all else None,
        "a3_debug_peak_hold_value_max": max(peak_hold_all) if peak_hold_all else None,
        "a3_debug_x_hold_max": max(x_hold_all) if x_hold_all else None,
        "a3_debug_keys_sample": a3_debug_keys,
        "total_frames": len(records),
        "high_risk_frames_count": len(risk_high),
    }


def run_length_report(records: List[Dict[str, Any]]) -> Dict[str, Any]:
    """单 replay 的 seq / risk / control_mode 序列 + 连续 run length。"""
    risks: List[float] = []
    for r in records:
        v = r.get("risk_used_for_decision")
        if v is not None:
            try:
                risks.append(float(v))
            except (TypeError, ValueError):
                risks.append(0.0)
        else:
            risks.append(0.0)

    rl_038 = run_lengths(risks, 0.38)
    rl_060 = run_lengths(risks, 0.60)
    rl_075 = run_lengths(risks, 0.75)

    # 前 3 条序列：seq, risk_used_for_decision, control_mode（可选 peak_hold/x_hold）
    seqs = [r.get("seq") for r in records[:200]]
    risk_vals = [r.get("risk_used_for_decision") for r in records[:200]]
    modes = [(r.get("decision") or {}).get("control_mode") for r in records[:200]]
    peak_holds = []
    x_holds = []
    for r in records[:200]:
        ad = (r.get("decision") or {}).get("a3_debug") or {}
        peak_holds.append(ad.get("peak_hold_value"))
        x_holds.append(ad.get("x_hold"))

    return {
        "consecutive_run_lengths": {
            "risk_ge_0.38": {"max": max(rl_038) if rl_038 else 0, "all_lengths": rl_038[:20]},
            "risk_ge_0.60": {"max": max(rl_060) if rl_060 else 0, "all_lengths": rl_060[:20]},
            "risk_ge_0.75": {"max": max(rl_075) if rl_075 else 0, "all_lengths": rl_075[:20]},
        },
        "timeline_sample_first_200": {
            "seq": seqs,
            "risk_used_for_decision": risk_vals,
            "control_mode": modes,
            "peak_hold_value": peak_holds,
            "x_hold": x_holds,
        },
    }


def main() -> int:
    import argparse
    p = argparse.ArgumentParser(description="Guarded 机制取证：stress replay 目录 → guarded_gap_report.json + 摘要")
    p.add_argument("dir", nargs="?", default="", help="stress replay 根目录（如 run 的 sim_out/simulations）")
    p.add_argument("--out", default="guarded_gap_report.json", help="输出 JSON 路径")
    p.add_argument("--single-clip", default="", help="可选：只分析该 replay 文件并输出 run length（路径）")
    args = p.parse_args()

    if args.single_clip:
        path = Path(args.single_clip)
        if not path.is_absolute():
            path = ROOT / args.single_clip
        if not path.is_file():
            print("ERROR: file not found:", path, file=sys.stderr)
            return 2
        records = load_jsonl(path)
        if not records:
            print("ERROR: no records", file=sys.stderr)
            return 2
        one = summarize_one_replay(records)
        rl = run_length_report(records)
        report = {"source": str(path), "summary": one, "run_length": rl}
        out_path = Path(args.out)
        if not out_path.is_absolute():
            out_path = Path.cwd() / out_path
        out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        print("[guarded_gap] single-clip report:", out_path)
        print("control_mode_counts:", one["control_mode_counts"])
        print("risk_used all max/p95/mean:", one["risk_used_for_decision_all"])
        print("risk_used high_risk max/p95/mean:", one["risk_used_for_decision_high_risk_frames"])
        print("a3_debug_keys_sample:", one["a3_debug_keys_sample"])
        print("consecutive run length (risk>=0.38): max =", rl["consecutive_run_lengths"]["risk_ge_0.38"]["max"])
        print("consecutive run length (risk>=0.60): max =", rl["consecutive_run_lengths"]["risk_ge_0.60"]["max"])
        print("consecutive run length (risk>=0.75): max =", rl["consecutive_run_lengths"]["risk_ge_0.75"]["max"])
        return 0

    dir_root = args.dir or ""
    if not dir_root:
        print("ERROR: need dir or --single-clip", file=sys.stderr)
        return 2
    dir_path = Path(dir_root)
    if not dir_path.is_absolute():
        dir_path = ROOT / dir_root
    if not dir_path.is_dir():
        print("ERROR: dir not found:", dir_path, file=sys.stderr)
        return 2

    replays = collect_stress_replays(dir_path)
    if not replays:
        print("ERROR: no *_stress* replay_output.jsonl under", dir_path, file=sys.stderr)
        return 2

    # 聚合所有 stress replay
    all_control: Dict[str, int] = {}
    all_risk: List[float] = []
    all_risk_high: List[float] = []
    all_ema: List[float] = []
    a3_keys: Optional[List[str]] = None
    total_frames = 0

    for rp in replays:
        recs = load_jsonl(rp)
        if not recs:
            continue
        s = summarize_one_replay(recs)
        total_frames += s["total_frames"]
        for k, v in (s.get("control_mode_counts") or {}).items():
            all_control[k] = all_control.get(k, 0) + v
        for r in recs:
            v = r.get("risk_used_for_decision")
            if v is not None:
                try:
                    fv = float(v)
                    all_risk.append(fv)
                    if r.get("high_risk") is True or fv >= 0.38:
                        all_risk_high.append(fv)
                except (TypeError, ValueError):
                    pass
        ema_max = s.get("a3_debug_ema_max")
        if ema_max is not None:
            all_ema.append(ema_max)
        if s.get("a3_debug_keys_sample"):
            a3_keys = s["a3_debug_keys_sample"]

    def p95(vals: List[float]) -> Optional[float]:
        if not vals:
            return None
        s = sorted(vals)
        i = min(int(len(s) * 0.95), len(s) - 1)
        return round(s[i], 4)

    report: Dict[str, Any] = {
        "source_dir": str(dir_path),
        "replay_count": len(replays),
        "total_frames": total_frames,
        "control_mode_counts": all_control,
        "risk_used_for_decision": {
            "all_frames": {"max": round(max(all_risk), 4) if all_risk else None, "p95": p95(all_risk), "mean": round(sum(all_risk) / len(all_risk), 4) if all_risk else None},
            "high_risk_frames_only": {"max": round(max(all_risk_high), 4) if all_risk_high else None, "p95": p95(all_risk_high), "mean": round(sum(all_risk_high) / len(all_risk_high), 4) if all_risk_high else None},
        },
        "a3_debug_ema_max_over_replays": max(all_ema) if all_ema else None,
        "a3_debug_keys_sample": a3_keys,
        "guarded_related_keys": [k for k in (a3_keys or []) if "guarded" in k.lower() or "consecutive" in k.lower() or "dwell" in k.lower() or "enter" in k.lower()],
    }

    out_path = Path(args.out)
    if not out_path.is_absolute():
        out_path = ROOT / args.out
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    # 终端摘要
    print("[guarded_gap] report:", out_path)
    print("1) control_mode 分布:", report["control_mode_counts"])
    print("2) a3_debug keys (样本):", report["a3_debug_keys_sample"])
    print("   guarded 相关键:", report["guarded_related_keys"] or "(无)")
    print("3) risk_used_for_decision all: max=%s p95=%s mean=%s" % (
        report["risk_used_for_decision"]["all_frames"]["max"],
        report["risk_used_for_decision"]["all_frames"]["p95"],
        report["risk_used_for_decision"]["all_frames"]["mean"],
    ))
    print("   risk_used high_risk only: max=%s p95=%s mean=%s" % (
        report["risk_used_for_decision"]["high_risk_frames_only"]["max"],
        report["risk_used_for_decision"]["high_risk_frames_only"]["p95"],
        report["risk_used_for_decision"]["high_risk_frames_only"]["mean"],
    ))
    print("   a3_debug_ema max (over replays):", report["a3_debug_ema_max_over_replays"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
