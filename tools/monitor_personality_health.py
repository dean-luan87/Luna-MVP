#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase4 健康监控报告（CI 入口）。
输入：run_dir（含 rank_report.json、run_manifest、champion suite_report 等）
输出：run_dir/health_report.json + 终端摘要。

指标：determinism_pass, champion_rank_key, champion_id, stress(early_gain_mean, guarded_frames_total, high_risk_frames_total),
overreact_rate, miss_rate, alpha_eff_stats(min/median/p90/max)。
Gate: determinism_pass, early_gain_mean>=4.0, miss_rate==0, overreact_rate<0.60, champion_vol<0.01；失败时写 overall: FAIL 与 reason_codes 供回滚。

分档（--grade）:
  smoke:  determinism 不参与 overall（标记 SKIP），用于 det=1 的 sweep，避免误报。
  release: determinism 必须 PASS（det=3 指纹一致），用于 freeze/tag 发布签字。
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parents[1]
EG_MIN = 4.0
OVERREACT_RATE_MAX = 0.60
CHAMPION_VOL_MAX = 0.01
DETERMINISM_SKIP = "SKIP"  # smoke 档下 determinism 不参与 overall


def _resolve_replay_path(path: str, run_dir: Path, champion_id: str) -> Optional[Path]:
    """解析 replay 路径：优先绝对路径存在则用，否则尝试相对 run_dir。"""
    p = Path(path)
    if p.is_file():
        return p
    if path.startswith("/"):
        return None
    for base in (run_dir, run_dir / champion_id):
        q = (base / path).resolve()
        if q.is_file():
            return q
    return None


def _champion_stress_frame_counts(run_dir: Path, champion_id: Optional[str]) -> Tuple[int, int]:
    """
    从冠军的 stress + stress_responsive 两份 suite_report 汇总：
    (guarded_frames, total_frames)。与 rank_report 的 channels.stress 口径一致（双通道两份都算）。
    """
    if not champion_id:
        return 0, 0
    total_frames = 0
    guarded_frames = 0
    for name in ("suite_report.stress.json", "suite_report.stress_responsive.json"):
        report_path = run_dir / champion_id / name
        if not report_path.is_file():
            continue
        try:
            data = json.loads(report_path.read_text(encoding="utf-8"))
        except Exception:
            continue
        per = data.get("per_episode") or {}
        for ep in per.values():
            raw_path = (ep or {}).get("candidate_replay_path")
            path = _resolve_replay_path(raw_path, run_dir, champion_id) if raw_path else None
            if not path:
                continue
            try:
                lines = path.read_text(encoding="utf-8").strip().splitlines()
                total_frames += len([_ for _ in lines if _.strip()])
                for line in lines:
                    if not line.strip():
                        continue
                    rec = json.loads(line)
                    mode = (rec.get("decision") or {}).get("control_mode") or ""
                    if str(mode).strip().upper() == "GUARDED":
                        guarded_frames += 1
            except Exception:
                pass
    return guarded_frames, total_frames


def _alpha_eff_from_replays(run_dir: Path, champion_id: Optional[str]) -> List[float]:
    """从冠军 stress 相关 replay 的 decision.a3_debug 收集 mod.alpha_eff（或 alpha_effective）。"""
    out: List[float] = []
    if not champion_id:
        return out
    for name in ("suite_report.stress.json", "suite_report.stress_responsive.json"):
        report_path = run_dir / champion_id / name
        if not report_path.is_file():
            continue
        try:
            data = json.loads(report_path.read_text(encoding="utf-8"))
        except Exception:
            continue
        per = data.get("per_episode") or {}
        for ep in per.values():
            raw_path = (ep or {}).get("candidate_replay_path")
            path = _resolve_replay_path(raw_path, run_dir, champion_id) if raw_path else None
            if not path:
                continue
            try:
                for line in path.open(encoding="utf-8"):
                    line = line.strip()
                    if not line:
                        continue
                    rec = json.loads(line)
                    decision = rec.get("decision") or {}
                    debug = decision.get("a3_debug") or {}
                    v = debug.get("mod.alpha_eff")
                    if v is None:
                        v = debug.get("alpha_effective")
                    if v is not None:
                        try:
                            out.append(float(v))
                        except (TypeError, ValueError):
                            pass
            except Exception:
                continue
    return out


def _percentile(sorted_vals: List[float], p: float) -> Optional[float]:
    if not sorted_vals:
        return None
    k = (len(sorted_vals) - 1) * p / 100.0
    lo = int(k)
    hi = min(lo + 1, len(sorted_vals) - 1)
    return sorted_vals[lo] + (k - lo) * (sorted_vals[hi] - sorted_vals[lo])


def run(run_dir: Path, grade: str = "smoke") -> Dict[str, Any]:
    run_dir = Path(run_dir)
    report: Dict[str, Any] = {
        "determinism_pass": False,
        "champion_rank_key": None,
        "champion_id": None,
        "stress": {
            "early_gain_mean": None,
            "guarded_frames_total": None,
            "high_risk_frames_total": None,
            "total_frames_stress": None,
        },
        "overreact_rate": None,
        "miss_rate": None,
        "alpha_eff_stats": {"min": None, "median": None, "p90": None, "max": None},
        "champion_vol": None,
        "gates": {"determinism": False, "early_gain": False, "miss_rate": False, "overreact_rate": False, "champion_vol": False},
        "overall": None,
        "reason_codes": [],
    }

    # run_manifest: determinism_status
    manifest_path = run_dir / "run_manifest.json"
    if manifest_path.is_file():
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            report["determinism_pass"] = (manifest.get("determinism_status") or "") == "PASS"
        except Exception:
            pass

    rp = run_dir / "rank_report.json"
    if not rp.is_file():
        report["error"] = "rank_report.json not found"
        return report

    try:
        data = json.loads(rp.read_text(encoding="utf-8"))
    except Exception as e:
        report["error"] = str(e)
        return report

    ranked = data.get("ranked") or []
    champ = ranked[0] if ranked else {}
    report["champion_id"] = data.get("champion_id") or champ.get("patch_id")
    report["champion_rank_key"] = champ.get("rank_key")

    stress_m = champ.get("stress_metrics") or {}
    stress_sc = champ.get("stress_scorecard") or {}
    ch_stress = (data.get("channels") or {}).get("stress") or {}
    eg = stress_m.get("early_gain_weighted_mean") or stress_sc.get("early_gain_mean")
    gtd = ch_stress.get("guarded_frames_total")
    hrf = ch_stress.get("high_risk_frames_total")
    if gtd is None:
        gtd = champ.get("guarded_frames_total")
    if hrf is None:
        hrf = champ.get("high_risk_frames_total")

    report["stress"]["early_gain_mean"] = eg
    report["stress"]["guarded_frames_total"] = gtd
    report["stress"]["high_risk_frames_total"] = hrf
    reg = champ.get("regular_metrics") or {}
    report["champion_vol"] = reg.get("volatility_mean")

    # 使用冠军自己的 stress 双通道 replay 统计，与 rank_report 口径一致
    champion_guarded, champion_total = _champion_stress_frame_counts(run_dir, report["champion_id"])
    report["stress"]["total_frames_stress"] = champion_total if champion_total > 0 else None
    if champion_total < 1:
        champion_total = max(1, champion_guarded + int(hrf or 0))
    report["overreact_rate"] = round(champion_guarded / champion_total, 4)
    champion_hr = int(stress_sc.get("high_risk_frames_count") or champ.get("stress_high_risk_frames_count") or 0)
    report["miss_rate"] = 1 if (champion_guarded == 0 and champion_hr > 0) else 0

    alpha_vals = _alpha_eff_from_replays(run_dir, report["champion_id"])
    if alpha_vals:
        alpha_vals.sort()
        report["alpha_eff_stats"]["min"] = round(alpha_vals[0], 4)
        report["alpha_eff_stats"]["median"] = round(_percentile(alpha_vals, 50) or 0, 4)
        report["alpha_eff_stats"]["p90"] = round(_percentile(alpha_vals, 90) or 0, 4)
        report["alpha_eff_stats"]["max"] = round(alpha_vals[-1], 4)

    # Gates
    report["gates"]["determinism"] = report["determinism_pass"]
    report["gates"]["early_gain"] = eg is not None and float(eg) >= EG_MIN
    report["gates"]["miss_rate"] = report["miss_rate"] == 0
    report["gates"]["overreact_rate"] = (
        report["overreact_rate"] is not None and report["overreact_rate"] < OVERREACT_RATE_MAX
    )
    vol = report.get("champion_vol")
    report["gates"]["champion_vol"] = (
        vol is not None and float(vol) < CHAMPION_VOL_MAX
    )

    # 分档：smoke 下 determinism 不参与 overall；release 下必须 PASS
    report["grade"] = grade
    if grade == "smoke":
        report["gates"]["determinism"] = DETERMINISM_SKIP
        gates_for_overall = [v for k, v in report["gates"].items() if v is not DETERMINISM_SKIP]
        all_ok = all(gates_for_overall)
        report["reason_codes"] = [k for k, v in report["gates"].items() if v is not DETERMINISM_SKIP and not v]
    else:
        all_ok = all(report["gates"].values())
        report["reason_codes"] = [k for k, v in report["gates"].items() if not v]
    report["overall"] = "PASS" if all_ok else "FAIL"

    return report


def main() -> int:
    import argparse
    ap = argparse.ArgumentParser(description="Phase4 健康监控：输出 health_report.json + 终端摘要")
    ap.add_argument("run_dir", type=Path, help="D1 run 目录（含 rank_report.json）")
    ap.add_argument("--grade", choices=("smoke", "release"), default="smoke",
                    help="smoke=determinism 不参与 overall（det=1 用）；release=determinism 必须 PASS（freeze/tag 用）")
    ap.add_argument("--json-only", action="store_true", help="仅写 JSON，不打印摘要")
    args = ap.parse_args()

    run_dir = Path(args.run_dir).resolve()
    if not run_dir.is_dir():
        print("ERROR: run_dir not found:", run_dir, file=sys.stderr)
        return 2

    report = run(run_dir, grade=args.grade)
    out_path = run_dir / "health_report.json"
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    if args.json_only:
        print(str(out_path))
        return 0

    # 终端摘要
    print("[health] run_dir:", run_dir)
    print("[health] determinism_pass:", report["determinism_pass"])
    print("[health] champion_id:", report["champion_id"])
    print("[health] champion_rank_key:", report["champion_rank_key"])
    print("[health] early_gain_mean:", report["stress"]["early_gain_mean"])
    print("[health] guarded_frames_total:", report["stress"]["guarded_frames_total"])
    print("[health] high_risk_frames_total:", report["stress"]["high_risk_frames_total"])
    print("[health] overreact_rate:", report["overreact_rate"])
    print("[health] miss_rate:", report["miss_rate"])
    print("[health] champion_vol:", report.get("champion_vol"))
    print("[health] alpha_eff_stats:", report["alpha_eff_stats"])
    print("[health] grade=%s gates: determinism=%s early_gain=%s miss_rate=%s overreact_rate=%s champion_vol=%s" % (
        report.get("grade", "smoke"),
        report["gates"]["determinism"],
        report["gates"]["early_gain"],
        report["gates"]["miss_rate"],
        report["gates"]["overreact_rate"],
        report["gates"].get("champion_vol", "?"),
    ))
    all_ok = report.get("overall") == "PASS"
    print("[health] overall:", report.get("overall", "PASS" if all_ok else "FAIL"))
    if report.get("reason_codes"):
        print("[health] reason_codes (for rollback):", report["reason_codes"])
    print("[health] written:", out_path)
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
