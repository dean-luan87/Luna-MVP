#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
压力普查：对 sweep 目录下所有 replay_output.jsonl 做应力密度统计。
用于判断这批 stress replay 是「重工业钢材」还是「泡沫塑料」，再决定是否 build PowerClips 或提高 risk_scale。

输入：--sweep-output-dir（与 build_powerclips_suite 同口径）
输出：replay_count, avg_risk_max, p95_risk_max, avg_high_risk_frames, high_risk_frames_p95, eligible_early_gain_frames_total
"""
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

# 与 scorer / PowerClips 一致的高压阈值
HIGH_RISK_THRESHOLD = 0.38
# 军检硬条件：PowerClips 只收这批
POWERCLIP_HARD_RISK_MAX_MIN = 0.6
POWERCLIP_HARD_MIN_HIGH_RISK_FRAMES = 30


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


def _risk_value(rec: Dict[str, Any]) -> Optional[float]:
    """与 build_powerclips_suite 一致：优先 risk_used_for_decision，否则 decision.a3_debug.ema 等。"""
    v = rec.get("risk_used_for_decision")
    if v is not None:
        try:
            return float(v)
        except (TypeError, ValueError):
            pass
    dec = rec.get("decision") or {}
    if isinstance(dec, dict):
        debug = dec.get("a3_debug") or {}
        if isinstance(debug, dict):
            for key in ("ema", "raw_effective", "complexity_score"):
                v = debug.get(key)
                if v is not None:
                    try:
                        return float(v)
                    except (TypeError, ValueError):
                        pass
    v = rec.get("complexity_score")
    if v is not None:
        try:
            return float(v)
        except (TypeError, ValueError):
            pass
    return None


def collect_replay_files(sweep_dir: Path) -> List[Path]:
    files = sorted(sweep_dir.glob("**/replay_output.jsonl"))
    return [f for f in files if f.is_file()]


def _p95(values: List[float]) -> float:
    if not values:
        return 0.0
    s = sorted(values)
    i = min(int(len(s) * 0.95), len(s) - 1)
    return s[i]


def run_census(sweep_dir: Path) -> Dict[str, Any]:
    """
    对 sweep_dir 下所有 replay_output.jsonl 做压力普查。
    仅统计含风险数据的 replay（无 risk_used_for_decision / ema 的 replay 不计入 risk 统计，但计入 replay_count）。
    """
    paths = collect_replay_files(sweep_dir)
    replay_count = len(paths)

    risk_max_list: List[float] = []
    high_risk_frames_list: List[int] = []
    eligible_early_gain_frames_total = 0
    no_risk_count = 0
    replay_count_meeting_hard = 0  # risk_max >= 0.6 AND high_risk_frames >= 30

    for replay_path in paths:
        records = load_jsonl(replay_path)
        risk_values = []
        for r in records:
            v = _risk_value(r)
            if v is not None:
                risk_values.append(v)
        high_risk_count = sum(
            1 for r in records
            if r.get("high_risk") is True or (_risk_value(r) or 0) >= HIGH_RISK_THRESHOLD
        )

        if not risk_values:
            no_risk_count += 1
            continue
        risk_max = max(risk_values)
        risk_max_list.append(risk_max)
        high_risk_frames_list.append(high_risk_count)
        eligible_early_gain_frames_total += high_risk_count
        if risk_max >= POWERCLIP_HARD_RISK_MAX_MIN and high_risk_count >= POWERCLIP_HARD_MIN_HIGH_RISK_FRAMES:
            replay_count_meeting_hard += 1

    n = len(risk_max_list)
    if n == 0:
        return {
            "replay_count": replay_count,
            "replay_with_risk_data": 0,
            "no_risk_data_count": no_risk_count,
            "replay_count_meeting_hard": 0,
            "avg_risk_max": 0.0,
            "p95_risk_max": 0.0,
            "avg_high_risk_frames": 0.0,
            "high_risk_frames_p95": 0.0,
            "eligible_early_gain_frames_total": 0,
        }
    return {
        "replay_count": replay_count,
        "replay_with_risk_data": n,
        "no_risk_data_count": no_risk_count,
        "replay_count_meeting_hard": replay_count_meeting_hard,
        "avg_risk_max": round(sum(risk_max_list) / n, 4),
        "p95_risk_max": round(_p95(risk_max_list), 4),
        "avg_high_risk_frames": round(sum(high_risk_frames_list) / n, 2),
        "high_risk_frames_p95": round(_p95([float(x) for x in high_risk_frames_list]), 2),
        "eligible_early_gain_frames_total": eligible_early_gain_frames_total,
    }


def main() -> int:
    import argparse
    p = argparse.ArgumentParser(description="压力普查：sweep 目录下 replay 的 risk_max / high_risk_frames 分布")
    p.add_argument("--sweep-output-dir", required=True, help="含 **/replay_output.jsonl 的目录，如 D1 run 的 sim_out/simulations")
    args = p.parse_args()

    sweep_dir = Path(args.sweep_output_dir)
    if not sweep_dir.is_dir():
        sweep_dir = ROOT / args.sweep_output_dir.strip()
    if not sweep_dir.is_dir():
        print("ERROR: sweep_output_dir not found:", args.sweep_output_dir, file=sys.stderr)
        return 2

    census = run_census(sweep_dir)
    print("[stress_density] replay_count:", census["replay_count"])
    print("[stress_density] replay_with_risk_data:", census["replay_with_risk_data"])
    print("[stress_density] no_risk_data_count:", census["no_risk_data_count"])
    print("[stress_density] avg_risk_max:", census["avg_risk_max"])
    print("[stress_density] p95_risk_max:", census["p95_risk_max"])
    print("[stress_density] avg_high_risk_frames:", census["avg_high_risk_frames"])
    print("[stress_density] high_risk_frames_p95:", census["high_risk_frames_p95"])
    print("[stress_density] eligible_early_gain_frames_total:", census["eligible_early_gain_frames_total"])
    print("[stress_density] replay_count_meeting_hard (risk_max>=0.6 AND high_risk_frames>=30):", census["replay_count_meeting_hard"])

    out_path = sweep_dir / "stress_density_census.json"
    out_path.write_text(json.dumps(census, indent=2, ensure_ascii=False, sort_keys=True), encoding="utf-8")
    print("[stress_density] wrote", str(out_path))
    return 0


if __name__ == "__main__":
    sys.exit(main())
