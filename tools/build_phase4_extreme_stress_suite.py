#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase4 极端应力 suite：高密度风险爆发（risk_density_ema 连续高压 20–30 帧），用于物理边界测试。

从已有 sweep 产出的 replay_output.jsonl 中筛选「连续 15 帧以上 risk ≥ 0.55」的片段（extreme v1.1，务实口径），
生成 library_store/v1.1/high_burst_v1，供 run_d1_phase4_seed_sweep.sh --regular-suite high_burst_v1 使用。

目标：强制 alpha_eff 推到接近上限，观察 overreact_rate、early_gain、champion_vol、determinism 是否突破阈值。

用法:
  # 需先有含 replay_output.jsonl 的 sweep 目录（例如某次 tournament 或 phase4 sweep 产出）
  python3 tools/build_phase4_extreme_stress_suite.py --sweep-output-dir outputs/d1_runs/phase4_seed_sweep/lam_0.40/seed_42
  # 或指定源 golden（供 recompute 时取 OBS_V1 切片）
  python3 tools/build_phase4_extreme_stress_suite.py --sweep-output-dir <path> --source-golden-suite-dir library_store/v1.1/golden_stress_v2

产出: library_store/v1.1/high_burst_v1/
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_SUITE_REL = "library_store/v1.1/high_burst_v1"
SUITE_NAME = "high_burst_v1"

# 高密度爆发口径（extreme v1.1）：连续 15 帧 risk ≥ 0.55，risk_max_min 0.58，避免 golden 脉冲型下 0 clip
MIN_CONSECUTIVE_OVER = "0.55:15"
RISK_MAX_MIN = 0.58
CLIP_PRE = 30
CLIP_POST = 30
MAX_CLIPS = 25


def main() -> int:
    p = argparse.ArgumentParser(
        description="Phase4 极端应力 suite：从 sweep 生成 high_burst_v1（extreme v1.1：连续 15 帧 ≥0.55）"
    )
    p.add_argument("--sweep-output-dir", required=True, help="含 **/replay_output.jsonl 的 sweep 目录")
    p.add_argument(
        "--source-golden-suite-dir",
        default="library_store/v1.1/golden_stress_v2",
        help="源 episode golden 目录，供 recompute 取 OBS_V1 切片（默认 golden_stress_v2）",
    )
    p.add_argument("--max-clips", type=int, default=MAX_CLIPS, help="最多保留 clip 数（默认 %d）" % MAX_CLIPS)
    p.add_argument("--diagnose", action="store_true", help="仅诊断 replay 的 risk_max / 连续高压段，不写 suite")
    p.add_argument("--min-consecutive-over", default=None, metavar="THR:FRAMES", help="覆盖连续高压规则，如 0.5:10（10 帧≥0.5）；0 clip 时可试此放宽")
    p.add_argument("--risk-max-min", type=float, default=None, metavar="FLOAT", help="覆盖 risk_max_min；0 clip 时可试 0.5 或 0.45")
    args = p.parse_args()

    sweep_dir = Path(args.sweep_output_dir)
    if not sweep_dir.is_absolute():
        sweep_dir = ROOT / sweep_dir
    if not sweep_dir.is_dir():
        print("ERROR: sweep-output-dir not found:", sweep_dir, file=sys.stderr)
        return 2

    out_suite = ROOT / OUT_SUITE_REL.replace("\\", "/").strip("/")
    source_golden = args.source_golden_suite_dir.strip()
    if source_golden and not Path(source_golden).is_absolute():
        source_golden = str(ROOT / source_golden)

    min_consec = (args.min_consecutive_over or "").strip() or MIN_CONSECUTIVE_OVER
    risk_min = args.risk_max_min if args.risk_max_min is not None else RISK_MAX_MIN

    cmd = [
        sys.executable,
        str(ROOT / "tools" / "build_powerclips_suite.py"),
        "--sweep-output-dir", str(sweep_dir),
        "--out-suite-dir", str(out_suite),
        "--suite-name", SUITE_NAME,
        "--source-golden-suite-dir", source_golden,
        "--min-consecutive-over", min_consec,
        "--risk-max-min", str(risk_min),
        "--clip-pre", str(CLIP_PRE),
        "--clip-post", str(CLIP_POST),
        "--max-clips", str(args.max_clips),
    ]
    if args.diagnose:
        cmd.append("--diagnose")

    parts = min_consec.split(":")
    thr_str = parts[0] if len(parts) >= 1 else "?"
    frames_str = parts[1] if len(parts) >= 2 else "?"
    print("[phase4_extreme_stress] building", SUITE_NAME, "from", sweep_dir)
    print("[phase4_extreme_stress] rules: consecutive risk>=" + thr_str + " for >=" + frames_str + " frames, risk_max_min=" + str(risk_min))
    ret = subprocess.run(cmd, cwd=str(ROOT))
    if ret.returncode != 0:
        return ret.returncode
    # 确认 suite 非空，否则 sweep 会得到 no regular suite_report / Champion None
    manifest_path = out_suite / "suite_manifest.json"
    if manifest_path.is_file():
        import json
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        n_clips = manifest.get("total_clips", 0)
        if n_clips == 0:
            print("[phase4_extreme_stress] WARN: suite has 0 clips. D1 will get no regular suite_report -> Champion None.", file=sys.stderr)
            print("[phase4_extreme_stress] Try: --diagnose 看分布；或放宽规则: --min-consecutive-over 0.5:10 --risk-max-min 0.5", file=sys.stderr)
            return 1
        print("[phase4_extreme_stress] ok: %d clips. Run: bash tools/run_d1_phase4_seed_sweep.sh --lam 0.40 --seeds \"42 123 777\" --det 3 --regular-suite high_burst_v1" % n_clips)
    return 0


if __name__ == "__main__":
    sys.exit(main())
