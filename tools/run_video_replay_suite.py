#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
6 个测试视频批量跑 run_video_replay + exit_latency 审计，汇总结果。
用于 Guardian Discipline 放大测试：全部通过即可冻结该块。
视频列表与 docs/Test_Videos_Inventory.md 一致。
"""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

# 与 Test_Videos_Inventory.md 一致的 6 个视频（项目根目录）
VIDEO_LIST = [
    "test_video.mp4",
    "test_video_complex_6m42s.mp4",
    "test_video_empty_street_1m01s_60fps.mp4",
    "test_video_follow_crowd_crossing_6m14s_60fps.mp4",
    "test_video_traffic_light_crossing_1m01s_60fps.mp4",
    "test_video_park_pond_edge_2m01s_60fps.mp4",
]

# Gate 红线（与 simulation/logic/gate.py 一致）
EXIT_LATENCY_P95_LIMIT = 6
EXIT_LATENCY_MAX_LIMIT = 12
HYSTERESIS_EFFICIENCY_MIN = 0.90


def _guardian_pass(summary: dict) -> tuple:
    """返回 (passed: bool, reason: str)。"""
    p95 = summary.get("exit_latency_p95")
    max_lat = summary.get("exit_latency_max")
    eff = summary.get("hysteresis_efficiency")
    if p95 is not None and p95 > EXIT_LATENCY_P95_LIMIT:
        return False, f"exit_latency_p95={p95}>6"
    if max_lat is not None and max_lat > EXIT_LATENCY_MAX_LIMIT:
        return False, f"exit_latency_max={max_lat}>12"
    if eff is not None and eff < HYSTERESIS_EFFICIENCY_MIN:
        return False, f"hysteresis_efficiency={eff}<0.90"
    return True, ""


def main() -> int:
    import argparse
    p = argparse.ArgumentParser(description="6 视频批量跑 video_replay + 审计，汇总 Guardian Discipline")
    p.add_argument("--config", default="patches/d1_conservative.json", help="Guardian patch")
    p.add_argument("--max-frames", type=int, default=600, help="每个视频最多处理帧数（默认 600≈20s）")
    p.add_argument("--out-dir", default="outputs/video_replay_suite_6videos", help="汇总输出目录")
    p.add_argument("--videos", nargs="*", default=None, help="覆盖默认列表，只跑指定视频名")
    args = p.parse_args()

    config_path = Path(args.config)
    if not config_path.is_file():
        config_path = ROOT / args.config
    if not config_path.is_file():
        print("ERROR: config 不存在:", args.config, file=sys.stderr)
        return 2

    videos = args.videos if args.videos else VIDEO_LIST
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    results = []
    for i, name in enumerate(videos, 1):
        video_path = ROOT / name
        if not video_path.is_file():
            print(f"[{i}/{len(videos)}] SKIP (文件不存在): {name}")
            results.append({
                "video": name,
                "skipped": True,
                "reason": "file_not_found",
            })
            continue
        print(f"[{i}/{len(videos)}] 跑: {name} ...")
        cmd = [
            sys.executable,
            str(ROOT / "tools" / "run_video_replay.py"),
            "--video", str(video_path.resolve()),
            "--config", str(config_path.resolve()),
            "--max-frames", str(args.max_frames),
            "--out", str(out_dir / name.replace(".mp4", "")),
        ]
        rc = subprocess.run(cmd, cwd=str(ROOT), capture_output=True, text=True, timeout=600)
        if rc.returncode != 0:
            print(f"  FAIL 命令退出码 {rc.returncode}: {rc.stderr[:300]}")
            results.append({
                "video": name,
                "skipped": False,
                "run_ok": False,
                "stderr": (rc.stderr or "")[:500],
            })
            continue
        # 读该视频对应的 candidate 目录下的 exit_audit_report.json（目录名 video_replay_<patch_stem>）
        stem = name.replace(".mp4", "")
        patch_stem = config_path.stem
        candidate_dir = out_dir / stem / f"video_replay_{patch_stem}"
        if not candidate_dir.is_dir():
            subdirs = [d for d in (out_dir / stem).iterdir() if d.is_dir() and "baseline" not in d.name]
            candidate_dir = subdirs[0] if subdirs else candidate_dir
        report_path = candidate_dir / "exit_audit_report.json"
        if not report_path.is_file():
            results.append({"video": name, "skipped": False, "run_ok": True, "audit_missing": True})
            continue
        summary = json.loads(report_path.read_text(encoding="utf-8")).get("summary", {})
        passed, reason = _guardian_pass(summary)
        results.append({
            "video": name,
            "skipped": False,
            "run_ok": True,
            "guardian_pass": passed,
            "guardian_reason": reason,
            "summary": summary,
        })
        p95 = summary.get("exit_latency_p95", "-")
        eff = summary.get("hysteresis_efficiency", "-")
        status = "PASS" if passed else "FAIL"
        print(f"  {status}  p95={p95} eff={eff}")

    # 汇总表
    suite_report = {
        "config": str(config_path),
        "max_frames": args.max_frames,
        "per_video": results,
        "all_passed": all(
            r.get("guardian_pass", True) for r in results if not r.get("skipped") and r.get("run_ok") and "audit_missing" not in r
        ),
    }
    report_path = out_dir / "suite_report.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(suite_report, f, ensure_ascii=False, indent=2)

    print("---")
    print("汇总:", report_path)
    n_ok = sum(1 for r in results if r.get("guardian_pass"))
    n_run = sum(1 for r in results if not r.get("skipped") and r.get("run_ok") and "audit_missing" not in r)
    print(f"Guardian 通过: {n_ok}/{n_run} 条视频")
    if suite_report["all_passed"]:
        print("全部通过，可冻结 Guardian Discipline Phase 1 视频测试。")
        return 0
    print("存在未通过项，请查看 suite_report.json 中 per_video[].guardian_reason。")
    return 1


if __name__ == "__main__":
    sys.exit(main())
