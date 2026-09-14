#!/usr/bin/env python3
"""
B2 view_conf gate 汇总：按 (floor,k) 分组，输出 7 指标。
显式按列名输出，避免列串位；sanity check 越界即 raise。
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "outputs" / "d1_runs" / "phase3_b2_view_conf"

# 列顺序与类型： (表头, 键, 格式或 "int")
_COLUMNS = [
    ("floor", "floor", "s"),
    ("k", "k", "s"),
    ("champion_eg_mean", "champion_eg_mean", "%.4f"),
    ("eg_var", "champion_eg_var", "%.6f"),
    ("champion_vol_max", "champion_vol_max", "%.4f"),
    ("exploit_win_rate", "exploit_win_rate", "%.2f"),
    ("guarded_total", "guarded_frames_total", "d"),
    ("eligible_hr", "eligible_early_gain_frames_total", "d"),
]


def _sanity_row(r: dict) -> None:
    """越界则 raise，保证证据链可信。"""
    er = r.get("exploit_win_rate")
    if er is not None and not (0 <= float(er) <= 1):
        raise ValueError("exploit_win_rate 越界: %s (应在 [0,1])" % er)
    gt = r.get("guarded_frames_total")
    if gt is not None:
        gti = int(gt) if isinstance(gt, (int, float)) else 0
        if gti <= 0:
            raise ValueError("guarded_frames_total 应为正整数: %s" % gt)
    eh = r.get("eligible_early_gain_frames_total")
    if eh is not None:
        ehi = int(eh) if isinstance(eh, (int, float)) else 0
        if ehi <= 0:
            raise ValueError("eligible_early_gain_frames_total 应为正整数: %s" % eh)
    vol = r.get("champion_vol_max")
    if vol is not None:
        vf = float(vol)
        if vf < 0:
            raise ValueError("champion_vol_max 非负: %s" % vol)
        if vf > 0.1:
            raise ValueError("champion_vol_max 异常大(>0.1): %s" % vol)


def _get_bucket(run_dir: Path, patch_id: str) -> str:
    if patch_id in ("conservative", "responsive"):
        return patch_id
    for name in ("effective_patch.stress_responsive.json", "effective_patch.stress.json"):
        p = run_dir / patch_id / name
        if p.is_file():
            try:
                d = json.loads(p.read_text(encoding="utf-8"))
                return (d.get("metadata") or {}).get("bucket") or "—"
            except Exception:
                pass
    return "—"


def _get_seed(run_dir: Path) -> int:
    mp = run_dir / "run_manifest.json"
    if mp.is_file():
        return int(json.loads(mp.read_text()).get("seed", 0))
    return 0


def main() -> None:
    if not BASE.is_dir():
        print("B2 base not found:", BASE, file=sys.stderr)
        sys.exit(1)

    rows = []
    m = re.compile(r"floor([0-9.]+)_k([0-9.]+)")
    for group_dir in sorted(BASE.iterdir()):
        if not group_dir.is_dir() or group_dir.name == "patches":
            continue
        mo = m.match(group_dir.name)
        if not mo:
            continue
        floor, k = mo.group(1), mo.group(2)
        run_dirs = sorted(
            [d for d in group_dir.iterdir() if d.is_dir() and (d / "rank_report.json").is_file()],
            key=lambda p: _get_seed(p),
        )
        if len(run_dirs) < 3:
            continue
        eg_list = []
        vol_list = []
        exploit_wins = 0
        guarded_total: int = 0
        eligible_hr: int = 0
        for rd in run_dirs:
            rp = rd / "rank_report.json"
            d = json.loads(rp.read_text())
            ranked = d.get("ranked") or []
            champ = ranked[0] if ranked else {}
            cid = d.get("champion_id") or champ.get("patch_id")
            reg = champ.get("regular_metrics") or {}
            stress_m = champ.get("stress_metrics") or {}
            eg = stress_m.get("early_gain_weighted_mean")
            vol = reg.get("volatility_mean")
            if eg is not None:
                eg_list.append(float(eg))
            if vol is not None:
                vol_list.append(float(vol))
            if cid and _get_bucket(rd, cid) == "exploit":
                exploit_wins += 1
            ch = (d.get("channels") or {}).get("stress") or {}
            guarded_total = int(ch.get("guarded_frames_total") or 0)
            eligible_hr = int(ch.get("high_risk_frames_total") or 0)

        eg_mean = sum(eg_list) / len(eg_list) if eg_list else 0.0
        eg_var = sum((x - eg_mean) ** 2 for x in eg_list) / len(eg_list) if eg_list else 0.0
        vol_max = max(vol_list) if vol_list else 0.0
        exploit_rate = exploit_wins / len(run_dirs) if run_dirs else 0.0
        row = {
            "floor": floor,
            "k": k,
            "champion_eg_mean": eg_mean,
            "champion_eg_var": eg_var,
            "champion_vol_max": vol_max,
            "exploit_win_rate": exploit_rate,
            "guarded_frames_total": guarded_total,
            "eligible_early_gain_frames_total": eligible_hr,
        }
        _sanity_row(row)
        rows.append(row)

    # 表头：显式按 _COLUMNS 顺序
    header_cells = [h for h, _k, _f in _COLUMNS]
    print("| " + " | ".join(header_cells) + " |")
    print("| " + " | ".join(["---"] * len(header_cells)) + " |")
    for r in rows:
        cells = []
        for _head, key, fmt in _COLUMNS:
            val = r[key]
            if fmt == "s":
                cells.append(str(val))
            elif fmt == "d":
                cells.append(str(int(val)))
            else:
                cells.append(fmt % val)
        print("| " + " | ".join(cells) + " |")

    eg_vals = [r["champion_eg_mean"] for r in rows]
    vol_vals = [r["champion_vol_max"] for r in rows]
    print()
    print("B2 Gate: champion_eg>=4.06? %s  champion_vol<0.01? %s" % (
        "PASS" if min(eg_vals) >= 4.0617 else "FAIL",
        "PASS" if max(vol_vals) < 0.01 else "FAIL",
    ))


if __name__ == "__main__":
    main()
